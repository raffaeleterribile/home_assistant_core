"""Conversation support for the AI device agent."""

from __future__ import annotations

import re
from typing import Literal, override

from homeassistant.components import conversation
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import MATCH_ALL
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import DOMAIN, SUPPORTED_DOMAINS


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the conversation entity for the config entry."""
    async_add_entities([AiDeviceAgentConversationEntity(config_entry)])


class AiDeviceAgentConversationEntity(
    conversation.ConversationEntity,
    conversation.AbstractConversationAgent,
):
    """A simple light and switch conversation agent."""

    _attr_has_entity_name = True
    _attr_name = "AI Device Agent"

    def __init__(self, entry: ConfigEntry) -> None:
        """Initialize the agent."""
        self.entry = entry

    @property
    @override
    def supported_languages(self) -> list[str] | Literal["*"]:
        """Return a list of supported languages."""
        return MATCH_ALL

    @override
    async def async_added_to_hass(self) -> None:
        """When entity is added to Home Assistant."""
        await super().async_added_to_hass()
        conversation.async_set_agent(self.hass, self.entry, self)

    @override
    async def async_will_remove_from_hass(self) -> None:
        """When entity will be removed from Home Assistant."""
        conversation.async_unset_agent(self.hass, self.entry)
        await super().async_will_remove_from_hass()

    @override
    async def _async_handle_message(
        self,
        user_input: conversation.ConversationInput,
        chat_log: conversation.ChatLog,
    ) -> conversation.ConversationResult:
        """Handle a simple text command."""
        text = user_input.text.strip().lower()
        if not text:
            response = conversation.IntentResponse(language=user_input.language)
            response.async_set_speech("Please say what you want me to do.")
            return conversation.ConversationResult(response=response)

        if any(keyword in text for keyword in ("which devices", "devices are configured", "list")):
            entities = _collect_supported_entities(self.hass)
            if not entities:
                response = conversation.IntentResponse(language=user_input.language)
                response.async_set_speech("I do not see any supported lights or switches configured.")
                return conversation.ConversationResult(response=response)

            labels = ", ".join(entity.split(".", 1)[1].replace("_", " ") for entity in entities)
            response = conversation.IntentResponse(language=user_input.language)
            response.async_set_speech(f"I can control: {labels}.")
            return conversation.ConversationResult(response=response)

        target = _extract_target(text)
        if target is None:
            response = conversation.IntentResponse(language=user_input.language)
            response.async_set_speech("I can only handle light and switch commands in this release.")
            return conversation.ConversationResult(response=response)

        entity_id = _match_entity(self.hass, target)
        if entity_id is None:
            response = conversation.IntentResponse(language=user_input.language)
            response.async_set_speech(f"I could not find a supported light or switch named '{target}'.")
            return conversation.ConversationResult(response=response)

        action = "turn_on" if "turn on" in text or "on" in text else "turn_off"
        state = self.hass.states.get(entity_id)

        if not state:
            response = conversation.IntentResponse(language=user_input.language)
            response.async_set_speech(f"The target '{target}' is unavailable right now.")
            return conversation.ConversationResult(response=response)

        if user_input.context.user_id is not None:
            user = await self.hass.auth.async_get_user(user_input.context.user_id)
            if user is not None and not user.is_admin:
                err = conversation.IntentResponseErrorCode.UNKNOWN
                response = conversation.IntentResponse(language=user_input.language)
                response.async_set_error(err, "Permission denied: only an administrator can control devices.")
                return conversation.ConversationResult(response=response)

        service_data = {"entity_id": entity_id}
        await self.hass.services.async_call("homeassistant", action, service_data, blocking=True, context=user_input.context)

        response = conversation.IntentResponse(language=user_input.language)
        response.async_set_speech(f"I turned {target} {action.replace('turn_', '')}.")
        return conversation.ConversationResult(response=response)


def _collect_supported_entities(hass: HomeAssistant) -> list[str]:
    """Collect configured light and switch entity ids."""
    entities: list[str] = []
    for entity_id in hass.states.async_entity_ids():
        domain = entity_id.split(".", 1)[0]
        if domain in SUPPORTED_DOMAINS:
            entities.append(entity_id)
    return sorted(entities)


def _extract_target(text: str) -> str | None:
    """Pull the likely entity name from a command."""
    for pattern in (
        r"turn (?:on|off)\s+([a-z0-9_\- ]+)",
        r"(?:on|off)\s+([a-z0-9_\- ]+)",
        r"([a-z0-9_\- ]+)\s+(?:light|switch)",
    ):
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
    return None


def _match_entity(hass: HomeAssistant, target: str) -> str | None:
    """Match a requested label to a supported entity."""
    normalized_target = target.replace(" ", "_")
    for entity_id in _collect_supported_entities(hass):
        if entity_id.endswith(f".{normalized_target}"):
            return entity_id
        friendly = entity_id.split(".", 1)[1].replace("_", " ")
        if friendly == target:
            return entity_id
    return None

"""Conversation support for the AI device agent."""

from __future__ import annotations

import logging
import re
from typing import Literal, override
from uuid import uuid4

from homeassistant.components import conversation
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_ENTITY_ID, MATCH_ALL
from homeassistant.core import HomeAssistant
from homeassistant.helpers import intent
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import get_runtime
from .const import (
    BACKEND_UNAVAILABLE_MESSAGE,
    DOMAIN,
    SUPPORTED_DOMAINS,
    UNSUPPORTED_DOMAIN_KEYWORDS,
)
from .coordinator import BackendUnavailableError
from .intent_resolver import resolve_targets
from .models import (
    CommandExecution,
    CommandRequest,
    ConversationSession,
    ResolutionStatus,
)
from .policy import requires_admin, requires_confirmation

_LOGGER = logging.getLogger(__name__)


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
    """Conversation agent for light/switch text commands."""

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
        """Handle incoming text command."""
        runtime = get_runtime(self.hass, self.entry.entry_id)
        text = user_input.text.strip()
        text_l = text.lower()

        if not text:
            return _speech(user_input.language, "Please say what you want me to do.")

        if any(
            keyword in text_l
            for keyword in ("which devices", "devices are configured", "list")
        ):
            labels = _collect_supported_labels(self.hass)
            if not labels:
                return _speech(
                    user_input.language,
                    "I do not see any supported lights or switches configured.",
                )
            return _speech(user_input.language, f"I can control: {', '.join(labels)}.")

        if any(keyword in text_l for keyword in UNSUPPORTED_DOMAIN_KEYWORDS):
            return _speech(
                user_input.language,
                "I can only handle light and switch commands in this release.",
            )

        action = _extract_action(text_l)
        target_hint, area_name = _extract_target_hint(text_l)
        session = _session_for_input(runtime.sessions, user_input)

        if (
            session.candidate_entity_ids
            and target_hint
            and action in {"turn_on", "turn_off", "toggle"}
        ):
            clarified = _resolve_candidate_selection(
                target_hint,
                session.candidate_entity_ids,
                session.candidate_labels,
            )
            if clarified is not None:
                target_hint = clarified
                session.candidate_entity_ids.clear()
                session.candidate_labels.clear()
                session.pending_clarification_request_id = None

        request = CommandRequest(
            request_id=str(uuid4()),
            raw_text=text,
            user_id=user_input.context.user_id,
            requested_action=action,
            target_hint=target_hint,
            conversation_context_id=session.session_id,
        )

        try:
            await runtime.coordinator.async_interpret(request)
        except BackendUnavailableError:
            _log_outcome(
                request,
                action,
                [],
                "backend_unavailable",
                "backend_error",
                [],
                [],
            )
            return _speech(user_input.language, BACKEND_UNAVAILABLE_MESSAGE)

        resolved = resolve_targets(self.hass, target_hint, area_name=area_name)

        if resolved.resolution_status == ResolutionStatus.AMBIGUOUS:
            session.pending_clarification_request_id = request.request_id
            session.candidate_entity_ids = resolved.candidate_entity_ids
            session.candidate_labels = resolved.candidate_labels
            choices = "; ".join(
                f"{index + 1}) {label}"
                for index, label in enumerate(resolved.candidate_labels)
            )
            _log_outcome(
                request,
                action,
                [],
                "clarification_required",
                resolved.reason,
                [],
                [],
            )
            return _speech(
                user_input.language,
                f"{resolved.reason} Options: {choices}. Reply with number or name.",
            )

        if resolved.resolution_status == ResolutionStatus.UNSUPPORTED:
            _log_outcome(
                request,
                action,
                [],
                "unsupported",
                resolved.reason,
                resolved.excluded_entity_ids,
                [],
            )
            return _speech(user_input.language, resolved.reason)

        if resolved.resolution_status == ResolutionStatus.UNAVAILABLE:
            _log_outcome(
                request,
                action,
                [],
                "unavailable",
                resolved.reason,
                resolved.excluded_entity_ids,
                resolved.excluded_unavailable_entity_ids,
            )
            return _speech(user_input.language, resolved.reason)

        resolved_domains = {
            entity_id.split(".", 1)[0] for entity_id in resolved.entity_ids
        }
        if requires_admin(action) and user_input.context.user_id is not None:
            user = await self.hass.auth.async_get_user(user_input.context.user_id)
            if user is not None and not user.is_admin:
                _log_outcome(
                    request,
                    action,
                    resolved.entity_ids,
                    "unauthorized",
                    "admin_required",
                    resolved.excluded_entity_ids,
                    resolved.excluded_unavailable_entity_ids,
                )
                return _speech(
                    user_input.language,
                    "Permission denied: only administrators can execute that action.",
                )

        if requires_confirmation(action, resolved_domains):
            _log_outcome(
                request,
                action,
                resolved.entity_ids,
                "confirmation_required",
                "policy_confirmation",
                resolved.excluded_entity_ids,
                resolved.excluded_unavailable_entity_ids,
            )
            return _speech(
                user_input.language,
                "This action requires confirmation and is not available in this release.",
            )

        if not resolved.entity_ids:
            return _speech(
                user_input.language, "No executable supported targets were found."
            )

        await self.hass.services.async_call(
            "homeassistant",
            action,
            {ATTR_ENTITY_ID: resolved.entity_ids},
            blocking=True,
            context=user_input.context,
        )

        execution = CommandExecution(
            execution_id=str(uuid4()),
            request_id=request.request_id,
            entity_ids=resolved.entity_ids,
            service_domain="homeassistant",
            service_name=action,
            status="executed",
            result_message=_format_success_message(action, resolved.entity_ids),
            excluded_entity_ids=resolved.excluded_entity_ids,
            excluded_unavailable_entity_ids=resolved.excluded_unavailable_entity_ids,
        )
        _log_outcome(
            request,
            action,
            execution.entity_ids,
            execution.status,
            "",
            execution.excluded_entity_ids,
            execution.excluded_unavailable_entity_ids,
        )

        extra_parts: list[str] = []
        if execution.excluded_entity_ids:
            extra_parts.append(
                "unsupported targets excluded: "
                + ", ".join(execution.excluded_entity_ids)
            )
        if execution.excluded_unavailable_entity_ids:
            extra_parts.append(
                "unavailable targets excluded: "
                + ", ".join(execution.excluded_unavailable_entity_ids)
            )

        message = execution.result_message
        if extra_parts:
            message = f"{message} Also, {'. '.join(extra_parts)}."
        return _speech(user_input.language, message)


def _speech(language: str | None, message: str) -> conversation.ConversationResult:
    response = intent.IntentResponse(language=language)
    response.async_set_speech(message)
    return conversation.ConversationResult(response=response)


def _session_for_input(
    sessions: dict[str, ConversationSession],
    user_input: conversation.ConversationInput,
) -> ConversationSession:
    session_id = (
        user_input.conversation_id or f"user:{user_input.context.user_id or 'anon'}"
    )
    session = sessions.get(session_id)
    if session is None:
        session = ConversationSession(
            session_id=session_id, user_id=user_input.context.user_id
        )
        sessions[session_id] = session
    return session


def _collect_supported_labels(hass: HomeAssistant) -> list[str]:
    labels: list[str] = []
    for entity_id in sorted(hass.states.async_entity_ids()):
        if entity_id.split(".", 1)[0] not in SUPPORTED_DOMAINS:
            continue
        state = hass.states.get(entity_id)
        if state is None:
            continue
        label = state.attributes.get("friendly_name") or entity_id.split(".", 1)[
            1
        ].replace("_", " ")
        labels.append(str(label))
    return labels


def _extract_action(text: str) -> str:
    if "turn on" in text or text.startswith("on "):
        return "turn_on"
    if "turn off" in text or text.startswith("off "):
        return "turn_off"
    if "toggle" in text:
        return "toggle"
    return "query"


def _extract_target_hint(text: str) -> tuple[str, str | None]:
    area_match = re.search(r"\bin\s+([a-z0-9_\- ]+)$", text)
    area_name = area_match.group(1).strip() if area_match else None

    cleaned = re.sub(r"^(turn\s+on|turn\s+off|toggle|list|show)\s+", "", text)
    cleaned = re.sub(r"\b(light|lights|switch|switches)\b", "", cleaned)
    cleaned = re.sub(r"\bin\s+[a-z0-9_\- ]+$", "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" .")

    return cleaned, area_name


def _resolve_candidate_selection(
    selection_text: str,
    candidate_entity_ids: list[str],
    candidate_labels: list[str],
) -> str | None:
    if selection_text.isdigit():
        index = int(selection_text) - 1
        if 0 <= index < len(candidate_entity_ids):
            return candidate_entity_ids[index].split(".", 1)[1].replace("_", " ")

    for entity_id, label in zip(candidate_entity_ids, candidate_labels, strict=False):
        if selection_text == label or selection_text == entity_id.split(".", 1)[
            1
        ].replace("_", " "):
            return entity_id.split(".", 1)[1].replace("_", " ")

    return None


def _format_success_message(action: str, entity_ids: list[str]) -> str:
    labels = ", ".join(
        entity_id.split(".", 1)[1].replace("_", " ") for entity_id in entity_ids
    )
    if action == "turn_on":
        verb = "on"
    elif action == "turn_off":
        verb = "off"
    else:
        verb = action
    return f"I turned {labels} {verb}."


def _log_outcome(
    request: CommandRequest,
    action: str,
    resolved_target: list[str],
    outcome: str,
    refusal_reason: str,
    excluded_entity_ids: list[str],
    excluded_unavailable_entity_ids: list[str],
) -> None:
    _LOGGER.info(
        "AI device command text=%s action=%s resolved_target=%s outcome=%s refusal_reason=%s excluded=%s excluded_unavailable=%s",
        request.raw_text,
        action,
        resolved_target,
        outcome,
        refusal_reason,
        excluded_entity_ids,
        excluded_unavailable_entity_ids,
    )

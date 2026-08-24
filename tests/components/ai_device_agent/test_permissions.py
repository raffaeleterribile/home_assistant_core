"""Tests for AI device agent permissions."""

from homeassistant.components import conversation
from homeassistant.core import Context, HomeAssistant
from homeassistant.helpers import intent
from homeassistant.setup import async_setup_component

from homeassistant.components.ai_device_agent.const import DOMAIN

from tests.common import MockConfigEntry


async def test_non_admin_can_execute_standard_light_switch_action(
    hass: HomeAssistant,
) -> None:
    """Non-admin users can execute standard light/switch actions."""
    user = await hass.auth.async_create_user("User")
    entry = MockConfigEntry(domain=DOMAIN, data={})
    entry.add_to_hass(hass)
    assert await async_setup_component(hass, "homeassistant", {})
    assert await async_setup_component(hass, "conversation", {})
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    hass.states.async_set("switch.fan", "off")

    result = await conversation.async_converse(
        hass,
        "turn on fan switch",
        None,
        Context(user_id=user.id),
        agent_id="conversation.ai_device_agent",
    )

    assert result.response.response_type == intent.IntentResponseType.ACTION_DONE


async def test_unsupported_domain_is_rejected(hass: HomeAssistant) -> None:
    """Unsupported domains are rejected with clear message."""
    user = await hass.auth.async_create_user("User")
    entry = MockConfigEntry(domain=DOMAIN, data={})
    entry.add_to_hass(hass)
    assert await async_setup_component(hass, "homeassistant", {})
    assert await async_setup_component(hass, "conversation", {})
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    result = await conversation.async_converse(
        hass,
        "set climate thermostat to 21",
        None,
        Context(user_id=user.id),
        agent_id="conversation.ai_device_agent",
    )

    assert result.response.response_type == intent.IntentResponseType.ACTION_DONE
    assert "only handle light and switch" in result.response.speech["plain"]["speech"].lower()

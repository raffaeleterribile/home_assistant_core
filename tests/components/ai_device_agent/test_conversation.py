"""Tests for the AI device agent conversation flow."""

from homeassistant.components import conversation
from homeassistant.const import ATTR_ENTITY_ID
from homeassistant.core import Context, HomeAssistant
from homeassistant.setup import async_setup_component

from tests.common import MockConfigEntry

from homeassistant.components.ai_device_agent.const import DOMAIN


async def test_list_supported_devices(hass: HomeAssistant) -> None:
    """The agent exposes light/switch targets in discovery queries."""
    entry = MockConfigEntry(domain=DOMAIN, data={"name": "Test Agent"})
    entry.add_to_hass(hass)
    assert await async_setup_component(hass, "conversation", {})
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    hass.states.async_set("light.kitchen", "off")
    hass.states.async_set("switch.fan", "off")
    hass.states.async_set("climate.thermostat", "heat")

    result = await conversation.async_converse(
        hass,
        "which devices are configured?",
        None,
        Context(user_id="user-1"),
        agent_id="conversation.ai_device_agent",
    )

    assert result.response.response_type.name == "OK"
    text = result.response.speech[0]["text"]
    assert "kitchen" in text.lower()
    assert "fan" in text.lower()
    assert "thermostat" not in text.lower()


async def test_turn_on_single_target(hass: HomeAssistant) -> None:
    """The agent turns on a single supported target."""
    entry = MockConfigEntry(domain=DOMAIN, data={"name": "Test Agent"})
    entry.add_to_hass(hass)
    assert await async_setup_component(hass, "conversation", {})
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    hass.states.async_set("light.kitchen", "off")
    hass.states.async_set("switch.fan", "off")

    result = await conversation.async_converse(
        hass,
        "turn on kitchen light",
        None,
        Context(user_id="user-1"),
        agent_id="conversation.ai_device_agent",
    )

    assert result.response.response_type.name == "OK"
    assert hass.states.get("light.kitchen").state == "on"
    assert "kitchen" in result.response.speech[0]["text"].lower()

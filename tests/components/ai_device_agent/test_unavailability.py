"""Tests for AI Device Agent backend unavailability behavior."""

from homeassistant.components import conversation
from homeassistant.core import Context, HomeAssistant
from homeassistant.helpers import intent
from homeassistant.setup import async_setup_component

from homeassistant.components.ai_device_agent import get_runtime
from homeassistant.components.ai_device_agent.const import DOMAIN

from tests.common import MockConfigEntry


async def test_backend_unavailability_refuses_execution(hass: HomeAssistant) -> None:
    """When backend is unavailable, no service execution occurs."""
    entry = MockConfigEntry(domain=DOMAIN, data={})
    entry.add_to_hass(hass)

    assert await async_setup_component(hass, "homeassistant", {})
    assert await async_setup_component(hass, "conversation", {})
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    hass.states.async_set("light.kitchen", "off")
    runtime = get_runtime(hass, entry.entry_id)
    runtime.coordinator.adapter.set_unavailable()

    result = await conversation.async_converse(
        hass,
        "turn on kitchen light",
        None,
        Context(user_id="user-1"),
        agent_id="conversation.ai_device_agent",
    )

    assert result.response.response_type == intent.IntentResponseType.ACTION_DONE
    assert "temporarily unavailable" in result.response.speech["plain"]["speech"].lower()
    assert hass.states.get("light.kitchen").state == "off"

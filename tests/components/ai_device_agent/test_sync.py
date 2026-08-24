"""Tests for AI Device Agent synchronization behavior."""

from homeassistant.components import conversation
from homeassistant.core import Context, HomeAssistant
from homeassistant.setup import async_setup_component

from homeassistant.components.ai_device_agent.const import DOMAIN

from tests.common import MockConfigEntry


async def test_inventory_refresh_reflects_later_changes(hass: HomeAssistant) -> None:
    """Later conversation reflects recently added and removed targets."""
    entry = MockConfigEntry(domain=DOMAIN, data={})
    entry.add_to_hass(hass)

    assert await async_setup_component(hass, "homeassistant", {})
    assert await async_setup_component(hass, "conversation", {})
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    hass.states.async_set("light.kitchen", "off")
    await hass.async_block_till_done()

    first = await conversation.async_converse(
        hass,
        "which devices are configured?",
        None,
        Context(user_id="user-1"),
        agent_id="conversation.ai_device_agent",
    )
    assert "kitchen" in first.response.speech["plain"]["speech"].lower()

    hass.states.async_set("switch.garden", "off")
    hass.states.async_remove("light.kitchen")
    await hass.async_block_till_done()

    second = await conversation.async_converse(
        hass,
        "which devices are configured?",
        None,
        Context(user_id="user-1"),
        agent_id="conversation.ai_device_agent",
    )
    text = second.response.speech["plain"]["speech"].lower()
    assert "garden" in text
    assert "kitchen" not in text

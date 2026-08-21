"""Tests for AI device agent permissions."""

from homeassistant.components import conversation
from homeassistant.core import Context, HomeAssistant
from homeassistant.setup import async_setup_component

from homeassistant.components.ai_device_agent.const import DOMAIN

from tests.common import MockConfigEntry, MockUser


async def test_non_admin_cannot_execute_sensitive_action(hass: HomeAssistant) -> None:
    """Non-admin users cannot execute sensitive actions."""
    user = await hass.auth.async_create_user(name="User", is_admin=False)
    entry = MockConfigEntry(domain=DOMAIN, data={"name": "Test Agent"})
    entry.add_to_hass(hass)
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

    assert result.response.response_type.name == "ERROR"
    assert "permission" in result.response.error_code.lower()

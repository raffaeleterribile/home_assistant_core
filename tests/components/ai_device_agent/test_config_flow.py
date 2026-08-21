"""Tests for the AI device agent config flow."""

from typing import Any

from homeassistant import config_entries
from homeassistant.core import HomeAssistant

from homeassistant.components.ai_device_agent.const import DOMAIN

from tests.common import MockConfigEntry


async def test_user_flow_creates_entry(hass: HomeAssistant) -> None:
    """Test the user flow creates a config entry."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_USER},
        data={"name": "Test Agent"},
    )

    assert result["type"] == "create_entry"
    assert result["title"] == "Test Agent"
    assert result["data"] == {"name": "Test Agent"}


async def test_user_flow_reuses_existing_entry(hass: HomeAssistant) -> None:
    """Test duplicate entries are rejected."""
    entry = MockConfigEntry(domain=DOMAIN, data={"name": "Test Agent"})
    entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_USER},
        data={"name": "Test Agent"},
    )

    assert result["type"] == "abort"
    assert result["reason"] == "already_configured"

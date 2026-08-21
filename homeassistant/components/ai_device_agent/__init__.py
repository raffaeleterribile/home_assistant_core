"""The AI Device Agent integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN

PLATFORMS = (Platform.CONVERSATION,)
CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

type AiDeviceAgentConfigEntry = ConfigEntry


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the AI device agent integration."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: AiDeviceAgentConfigEntry) -> bool:
    """Set up AI device agent from a config entry."""
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: AiDeviceAgentConfigEntry) -> bool:
    """Unload an AI device agent config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

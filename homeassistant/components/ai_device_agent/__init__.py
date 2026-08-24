"""The AI Device Agent integration.

Local-first constraints:
- Home Assistant registries and state remain the only runtime source of truth.
- The backend adapter is interpretation-only and cannot directly execute services.
- Backend outages fail closed and never trigger queued or fallback actuation.
- First release supports only light/switch discovery and actuation.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EVENT_STATE_CHANGED, Platform
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import area_registry as ar
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .coordinator import AiDeviceAgentCoordinator, BackendAdapter
from .models import ConversationSession

PLATFORMS = (Platform.CONVERSATION,)
CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)
_LOGGER = logging.getLogger(__name__)


type AiDeviceAgentConfigEntry = ConfigEntry


@dataclass(slots=True)
class AiDeviceAgentRuntime:
    """Runtime objects stored per config entry."""

    coordinator: AiDeviceAgentCoordinator
    sessions: dict[str, ConversationSession] = field(default_factory=dict)
    unsub_listeners: list[Callable[[], None]] = field(default_factory=list)


def get_runtime(hass: HomeAssistant, entry_id: str) -> AiDeviceAgentRuntime:
    """Return runtime for a config entry."""
    return hass.data[DOMAIN][entry_id]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the AI device agent integration."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(
    hass: HomeAssistant, entry: AiDeviceAgentConfigEntry
) -> bool:
    """Set up AI device agent from a config entry."""
    adapter = BackendAdapter()
    coordinator = AiDeviceAgentCoordinator(hass=hass, adapter=adapter)
    await coordinator.async_refresh_inventory()

    runtime = AiDeviceAgentRuntime(coordinator=coordinator)
    hass.data[DOMAIN][entry.entry_id] = runtime

    @callback
    def _async_schedule_refresh(*_: object) -> None:
        """Refresh inventory snapshot after HA inventory/state changes."""
        hass.async_create_task(coordinator.async_refresh_inventory())

    runtime.unsub_listeners = [
        hass.bus.async_listen(ar.EVENT_AREA_REGISTRY_UPDATED, _async_schedule_refresh),
        hass.bus.async_listen(
            dr.EVENT_DEVICE_REGISTRY_UPDATED, _async_schedule_refresh
        ),
        hass.bus.async_listen(
            er.EVENT_ENTITY_REGISTRY_UPDATED, _async_schedule_refresh
        ),
        hass.bus.async_listen(EVENT_STATE_CHANGED, _async_schedule_refresh),
    ]

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    _LOGGER.debug("AI Device Agent entry %s initialized", entry.entry_id)
    return True


async def async_unload_entry(
    hass: HomeAssistant, entry: AiDeviceAgentConfigEntry
) -> bool:
    """Unload an AI device agent config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    runtime = hass.data[DOMAIN].pop(entry.entry_id, None)
    if runtime is not None:
        for unsub in runtime.unsub_listeners:
            unsub()

    return unload_ok

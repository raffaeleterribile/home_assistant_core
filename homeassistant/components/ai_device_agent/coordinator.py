"""Backend adapter and synchronization coordinator for AI Device Agent."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from homeassistant.core import HomeAssistant

from .const import SUPPORTED_DOMAINS
from .models import CommandRequest


class BackendAvailability(StrEnum):
    """Availability states for the backend adapter."""

    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"


class BackendUnavailableError(RuntimeError):
    """Raised when backend adapter is unavailable."""


@dataclass(slots=True)
class BackendAdapter:
    """Thin adapter over the orchestration backend contract."""

    availability: BackendAvailability = BackendAvailability.AVAILABLE

    def set_unavailable(self) -> None:
        """Mark adapter unavailable for fail-closed behavior."""
        self.availability = BackendAvailability.UNAVAILABLE

    def set_available(self) -> None:
        """Mark adapter available."""
        self.availability = BackendAvailability.AVAILABLE

    async def async_interpret(self, request: CommandRequest) -> dict[str, str]:
        """Return a lightweight proposal used by local deterministic logic."""
        if self.availability == BackendAvailability.UNAVAILABLE:
            raise BackendUnavailableError("Backend temporarily unavailable")

        return {
            "proposed_action": request.requested_action,
            "target_reference_text": request.target_hint,
        }


@dataclass(slots=True)
class AiDeviceAgentCoordinator:
    """Coordinator for runtime snapshot and backend availability handling."""

    hass: HomeAssistant
    adapter: BackendAdapter
    inventory_snapshot: list[str] = field(default_factory=list)

    async def async_refresh_inventory(self) -> None:
        """Refresh a deterministic supported-target snapshot."""
        self.inventory_snapshot = sorted(
            entity_id
            for entity_id in self.hass.states.async_entity_ids()
            if entity_id.split(".", 1)[0] in SUPPORTED_DOMAINS
        )

    async def async_interpret(self, request: CommandRequest) -> dict[str, str]:
        """Interpret a request through the backend adapter."""
        return await self.adapter.async_interpret(request)

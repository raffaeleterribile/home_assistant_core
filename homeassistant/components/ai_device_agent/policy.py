"""Policy checks for the AI Device Agent integration."""

from __future__ import annotations

from .const import SUPPORTED_DOMAINS


def is_supported_entity(entity_id: str) -> bool:
    """Return if entity belongs to a supported domain."""
    return entity_id.split(".", 1)[0] in SUPPORTED_DOMAINS


def requires_admin(action: str) -> bool:
    """Return if an action class is admin-only."""
    return action in {"configure", "reconfigure", "remove", "delete"}


def requires_confirmation(action: str, domains: set[str]) -> bool:
    """Return if an action requires explicit confirmation.

    First release intentionally skips extra confirmation for standard
    light/switch actions after resolution and permission checks.
    """
    if action in {"turn_on", "turn_off", "toggle", "query"} and domains.issubset(
        SUPPORTED_DOMAINS
    ):
        return False
    return action not in {"query"}

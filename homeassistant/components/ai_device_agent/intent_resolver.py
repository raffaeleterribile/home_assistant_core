"""Deterministic target resolution helpers for AI Device Agent."""

from __future__ import annotations

import re

from homeassistant.core import HomeAssistant, State
from homeassistant.helpers import area_registry as ar
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er

from .const import SUPPORTED_DOMAINS
from .models import ResolvedTarget, ResolutionStatus


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def _candidate_label(state: State) -> str:
    friendly = state.attributes.get("friendly_name")
    if isinstance(friendly, str) and friendly:
        return friendly.lower()
    return state.entity_id.split(".", 1)[1].replace("_", " ").lower()


def _iter_supported_states(hass: HomeAssistant) -> list[State]:
    states: list[State] = []
    for entity_id in hass.states.async_entity_ids():
        if entity_id.split(".", 1)[0] not in SUPPORTED_DOMAINS:
            continue
        state = hass.states.get(entity_id)
        if state is not None:
            states.append(state)
    return states


def _area_entity_ids(hass: HomeAssistant, area_name: str) -> set[str]:
    area_reg = ar.async_get(hass)
    entity_reg = er.async_get(hass)
    device_reg = dr.async_get(hass)

    area_name_norm = _normalize(area_name)
    area = next(
        (
            item
            for item in area_reg.areas.values()
            if _normalize(item.name) == area_name_norm
        ),
        None,
    )
    if area is None:
        return set()

    matched_entity_ids: set[str] = set()
    for entry in entity_reg.entities.values():
        if entry.disabled_by is not None:
            continue

        entity_area_id = entry.area_id
        if entity_area_id is None and entry.device_id is not None:
            device = device_reg.devices.get(entry.device_id)
            entity_area_id = device.area_id if device else None

        if entity_area_id == area.id:
            matched_entity_ids.add(entry.entity_id)

    return matched_entity_ids


def _match_candidates(states: list[State], target: str) -> list[State]:
    norm_target = _normalize(target).replace("_", " ")
    exact: list[State] = []
    partial: list[State] = []

    for state in states:
        object_name = state.entity_id.split(".", 1)[1].replace("_", " ")
        friendly = _candidate_label(state)
        if norm_target in {object_name, friendly}:
            exact.append(state)
            continue
        if norm_target and (norm_target in object_name or norm_target in friendly):
            partial.append(state)

    if exact:
        return sorted(exact, key=lambda item: item.entity_id)
    return sorted(partial, key=lambda item: item.entity_id)


def resolve_targets(
    hass: HomeAssistant,
    target_hint: str,
    *,
    area_name: str | None = None,
) -> ResolvedTarget:
    """Resolve target entities deterministically from runtime state."""
    supported_states = _iter_supported_states(hass)

    if area_name:
        allowed_entity_ids = _area_entity_ids(hass, area_name)
        supported_states = [
            state for state in supported_states if state.entity_id in allowed_entity_ids
        ]

    if not target_hint and area_name:
        available = [
            state.entity_id
            for state in supported_states
            if state.state not in {"unavailable", "unknown"}
        ]
        unavailable = [
            state.entity_id
            for state in supported_states
            if state.state in {"unavailable", "unknown"}
        ]
        if not available and unavailable:
            return ResolvedTarget(
                resolution_status=ResolutionStatus.UNAVAILABLE,
                excluded_unavailable_entity_ids=unavailable,
                reason="No available supported targets in that area.",
            )
        if available:
            return ResolvedTarget(
                resolution_status=ResolutionStatus.RESOLVED,
                entity_ids=sorted(available),
                excluded_unavailable_entity_ids=sorted(unavailable),
            )

    raw_parts = [
        part.strip() for part in re.split(r",|\band\b", target_hint) if part.strip()
    ]
    if not raw_parts:
        raw_parts = [target_hint.strip()] if target_hint.strip() else []

    resolved: list[str] = []
    excluded: list[str] = []
    excluded_unavailable: list[str] = []

    for token in raw_parts:
        candidates = _match_candidates(supported_states, token)
        if not candidates:
            excluded.append(token)
            continue

        if len(candidates) > 1:
            labels = [_candidate_label(candidate) for candidate in candidates]
            return ResolvedTarget(
                resolution_status=ResolutionStatus.AMBIGUOUS,
                candidate_entity_ids=[candidate.entity_id for candidate in candidates],
                candidate_labels=labels,
                reason="I found multiple matching targets. Please choose one.",
            )

        matched = candidates[0]
        if matched.state in {"unavailable", "unknown"}:
            excluded_unavailable.append(matched.entity_id)
            continue
        resolved.append(matched.entity_id)

    if not resolved and excluded_unavailable:
        return ResolvedTarget(
            resolution_status=ResolutionStatus.UNAVAILABLE,
            excluded_entity_ids=excluded,
            excluded_unavailable_entity_ids=excluded_unavailable,
            reason="Matched targets are currently unavailable.",
        )

    if not resolved:
        return ResolvedTarget(
            resolution_status=ResolutionStatus.UNSUPPORTED,
            excluded_entity_ids=excluded,
            reason="No supported light or switch target matched your request.",
        )

    return ResolvedTarget(
        resolution_status=ResolutionStatus.RESOLVED,
        entity_ids=sorted(set(resolved)),
        excluded_entity_ids=sorted(set(excluded)),
        excluded_unavailable_entity_ids=sorted(set(excluded_unavailable)),
    )

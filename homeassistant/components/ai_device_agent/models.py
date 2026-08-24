"""Runtime models for the AI Device Agent integration."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class ResolutionStatus(StrEnum):
    """Resolution outcome for an incoming command."""

    RESOLVED = "resolved"
    AMBIGUOUS = "ambiguous"
    UNSUPPORTED = "unsupported"
    UNAUTHORIZED = "unauthorized"
    UNAVAILABLE = "unavailable"
    BACKEND_UNAVAILABLE = "backend_unavailable"


@dataclass(slots=True)
class CommandRequest:
    """Normalized user command request."""

    request_id: str
    raw_text: str
    user_id: str | None
    requested_action: str
    target_hint: str
    conversation_context_id: str


@dataclass(slots=True)
class ResolvedTarget:
    """Resolution result for command execution."""

    resolution_status: ResolutionStatus
    entity_ids: list[str] = field(default_factory=list)
    excluded_entity_ids: list[str] = field(default_factory=list)
    excluded_unavailable_entity_ids: list[str] = field(default_factory=list)
    candidate_entity_ids: list[str] = field(default_factory=list)
    candidate_labels: list[str] = field(default_factory=list)
    reason: str = ""
    needs_confirmation: bool = False


@dataclass(slots=True)
class CommandExecution:
    """Execution outcome for a command."""

    execution_id: str
    request_id: str
    entity_ids: list[str]
    service_domain: str
    service_name: str
    status: str
    result_message: str
    excluded_entity_ids: list[str] = field(default_factory=list)
    excluded_unavailable_entity_ids: list[str] = field(default_factory=list)


@dataclass(slots=True)
class ConversationSession:
    """Conversation state used for clarification prompts."""

    session_id: str
    user_id: str | None
    pending_clarification_request_id: str | None = None
    candidate_entity_ids: list[str] = field(default_factory=list)
    candidate_labels: list[str] = field(default_factory=list)

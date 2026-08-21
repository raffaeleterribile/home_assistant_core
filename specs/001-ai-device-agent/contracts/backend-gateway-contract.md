# Contract: Backend Gateway

## Purpose
Defines the adapter boundary between Home Assistant-side orchestration and the
external model/orchestration backend used in the first release.

## Request Contract

### Required Fields
- `request_id`
- `session_id`
- `user_text`
- `supported_domains`
- `available_targets_context`
- `policy_hints`

### Request Rules
- Only the minimum conversational context required for interpretation may be
  sent.
- Permission decisions must not be delegated as final authority to the backend.
- The backend must not receive a direct capability to execute Home Assistant
  services.

## Response Contract

### Expected Response Types
- `intent_proposal`
- `clarification_needed`
- `cannot_comply`
- `backend_error`

### Intent Proposal Fields
- `proposed_action`
- `target_reference_text`
- `confidence_notes` (optional)

### Error Semantics
- Timeout, connectivity, or provider errors map to `backend_error`.
- `backend_error` must be translated by Home Assistant into a temporary
  unavailability response.

## Enforcement Rules
- Final target resolution occurs inside Home Assistant.
- Final permission enforcement occurs inside Home Assistant.
- Final confirmation policy enforcement occurs inside Home Assistant.
- Backend responses must be treated as proposals, not executable commands.

## Availability Contract
- The adapter must fail closed.
- No queued replay is allowed in the first release.
- No implicit local actuation fallback is allowed when the backend is down.
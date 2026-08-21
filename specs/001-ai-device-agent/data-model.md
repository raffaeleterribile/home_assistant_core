# Data Model: AI Device Agent

## ConfiguredIntegrationInventory

### Purpose
Represents the configured Home Assistant integrations visible to the agent as
sources of available device ecosystems.

### Fields
- `entry_id`: unique config entry identifier
- `domain`: integration domain
- `title`: user-visible integration title
- `state`: loaded, unloaded, unavailable, or disabled
- `supports_devices`: whether the integration exposes devices/entities relevant
  to the first release

### Relationships
- One configured integration can own many managed devices.

### Validation Rules
- Derived only from Home Assistant config entries.
- Disabled or unavailable entries remain visible only when needed to explain why
  a target cannot be acted upon.

## ManagedDeviceInventory

### Purpose
Represents Home Assistant devices known to the agent.

### Fields
- `device_id`: unique device identifier
- `name`: canonical display name
- `area_id`: optional area assignment
- `config_entry_id`: owning integration entry
- `availability`: available, unavailable, removed
- `labels`: optional labels used for discovery

### Relationships
- One managed device can map to many commandable entities.
- Each managed device belongs to one configured integration entry at runtime.

### Validation Rules
- Derived only from the device registry.
- Removed devices are no longer command targets.

## CommandableEntity

### Purpose
Represents the actual Home Assistant control surface used for light/switch
queries and actions.

### Fields
- `entity_id`: unique entity identifier
- `domain`: entity domain, initially `light` or `switch`
- `device_id`: linked device identifier
- `friendly_name`: display name used in conversations
- `current_state`: latest known state from Home Assistant
- `is_supported`: whether the entity is inside the first-release domain policy
- `is_permitted_for_user`: whether the current user can operate the entity

### Relationships
- Many entities can point to one device.
- One entity can appear in many command resolutions over time.

### Validation Rules
- Domain must be `light` or `switch` in the first release.
- Permission must be checked before execution, not cached as a static truth.

## SupportedDomainPolicy

### Purpose
Defines which Home Assistant domains can be queried or controlled in the current
release and which actions need confirmation.

### Fields
- `supported_domains`: set of allowed domains
- `confirmation_policy`: mapping from action type to confirmation requirement
- `admin_only_actions`: set of action classes restricted to admin users

### Relationships
- Used by command resolution and execution policy checks.

### Validation Rules
- First release domain set is fixed to `light` and `switch`.
- Unsupported domains must produce a clear defer/reject response.

## CommandRequest

### Purpose
Represents a normalized user request before execution.

### Fields
- `request_id`: unique identifier
- `raw_text`: original user utterance
- `user_id`: requesting user
- `requested_action`: normalized action such as query, turn_on, turn_off, toggle
- `target_hint`: free-form target text from the user
- `conversation_context_id`: conversation/session identifier

### Relationships
- One command request can produce zero or one resolved target in the first
  release.

### Validation Rules
- Must preserve the original text for auditability.
- Must not be executed until target resolution and policy checks pass.

## ResolvedTarget

### Purpose
Represents the deterministic resolution result after combining user intent with
Home Assistant inventory.

### Fields
- `resolution_status`: resolved, ambiguous, unsupported, unauthorized,
  unavailable, backend_unavailable
- `entity_id`: resolved entity when available
- `device_id`: resolved device when available
- `reason`: explanation used for user feedback
- `needs_confirmation`: whether explicit confirmation is required

### Relationships
- Produced from one command request.
- Feeds one command execution attempt when status is `resolved`.

### Validation Rules
- Exactly one actionable target may proceed to execution in the first release.
- Ambiguous or unsupported resolutions must never trigger execution.

## CommandExecution

### Purpose
Represents an attempted or completed device action.

### Fields
- `execution_id`: unique identifier
- `request_id`: originating request
- `entity_id`: executed entity
- `service_domain`: Home Assistant service domain
- `service_name`: Home Assistant service name
- `status`: pending_confirmation, executed, rejected, failed, unavailable
- `result_message`: user-facing outcome

### Relationships
- One execution belongs to one request and one resolved target.

### Validation Rules
- Must carry the caller context into Home Assistant service execution.
- Must not transition from `unavailable` or `rejected` to `executed` in the
  first release.

## ConversationSession

### Purpose
Tracks the interaction context for clarification, confirmation, and results.

### Fields
- `session_id`: unique identifier
- `user_id`: associated user
- `last_request_id`: most recent request
- `pending_confirmation_execution_id`: optional execution awaiting confirmation
- `pending_clarification_request_id`: optional request awaiting clarification

### Relationships
- One session can include many requests over time.

### Validation Rules
- Only one pending confirmation should exist at a time for the first release.
- Clarification and confirmation state must be cleared once resolved.

## State Transitions

### CommandRequest / ResolvedTarget
- `received` → `resolved`
- `received` → `ambiguous`
- `received` → `unsupported`
- `received` → `unauthorized`
- `received` → `unavailable`
- `received` → `backend_unavailable`

### CommandExecution
- `ready` → `pending_confirmation`
- `ready` → `executed`
- `ready` → `rejected`
- `ready` → `failed`
- `ready` → `unavailable`
- `pending_confirmation` → `executed`
- `pending_confirmation` → `rejected`
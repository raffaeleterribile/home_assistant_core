# Research: AI Device Agent

## Decision: Build the first slice as a dedicated Home Assistant conversation integration

### Rationale
- Home Assistant already has a conversation stack and agent lifecycle, so the
  cleanest insertion point is a dedicated integration that plugs into the
  existing conversation manager rather than inventing a separate control API.
- The default conversation agent already proves that listening to registry and
  state-change signals is the right synchronization pattern.
- A dedicated integration keeps feature ownership, configuration, tests, and
  future voice evolution localized.

### Alternatives considered
- Add the feature directly inside the existing `conversation` component: rejected
  because it would couple experimental agent-specific behavior to the generic
  conversation core.
- Build a parallel HTTP or WebSocket control surface: rejected because it would
  bypass the established conversation and permission patterns.

## Decision: Use Home Assistant registries, state machine, and service dispatch as the only runtime truth

### Rationale
- `ConfigEntries`, `DeviceRegistry`, `EntityRegistry`, `state_changed`, and the
  service layer already define configured integrations, inventory, runtime
  updates, and actuation.
- Maintaining an internal agent-side catalog would create drift, duplicate
  policy logic, and violate the constitution.
- Deterministic target resolution can be derived from those sources while still
  letting the model interpret user phrasing.

### Alternatives considered
- Keep a custom mirrored device catalog for the agent: rejected because it risks
  stale data and doubles inventory logic.
- Resolve targets directly inside model prompts without a deterministic layer:
  rejected because permissions and ambiguity handling must not depend on model
  behavior.

## Decision: Keep orchestration thin and place policy enforcement outside the model

### Rationale
- For the first release, the model should only help interpret the request; a
  deterministic resolver should map the result to Home Assistant targets,
  permissions, confirmations, and service calls.
- This keeps unsupported domains, ambiguity handling, and safety enforcement
  predictable and testable.
- It also keeps the design ready for a later voice channel without duplicating
  business logic.

### Alternatives considered
- Multi-step autonomous agent orchestration: rejected for the first slice as it
  raises failure modes and makes validation harder.
- Let tools enforce policy on their own: rejected because policy must be a final
  guardrail independent of model or adapter behavior.

## Decision: Prototype against a single external OpenAI-compatible gateway, but hide it behind a local adapter contract

### Rationale
- A single adapter allows early experimentation while keeping the Home
  Assistant-side contract stable.
- The adapter can centralize timeout, availability classification, telemetry,
  and future migration to a more internalized hosting model.
- The plan remains compatible with Microsoft-oriented orchestration/model
  infrastructure later without leaking those details into the user-facing
  specification.

### Alternatives considered
- Bind Home Assistant directly to one specific provider implementation: rejected
  because it would make later migration harder.
- Support multiple providers in the first slice: rejected because it expands the
  test matrix before the light/switch flow is stable.

## Decision: Fail closed when the external backend is unavailable

### Rationale
- The specification now fixes the behavior: refuse commands temporarily and
  return a clear unavailability message.
- This is aligned with local-first expectations because Home Assistant manual
  controls continue working independently.
- It avoids delayed or partially inferred actuation when the external reasoning
  layer is down.

### Alternatives considered
- Queue commands for later execution: rejected because delayed actuation is risky
  in a home-control context.
- Execute partial local fallbacks: rejected for the first release because it
  introduces a second control path with different semantics.

## Decision: Limit the first release to light and switch domains

### Rationale
- Lights and switches are common, comparatively low-risk, and align well with
  Home Assistant's existing entity and service patterns.
- The domain boundary keeps prompts, target resolution, tests, and safety policy
  small enough for a reliable first delivery.
- Unsupported domains can be rejected clearly, preserving room for progressive
  expansion.

### Alternatives considered
- Cover all commandable domains from the start: rejected because it makes policy,
  ambiguity resolution, and testing too broad.
- Read-only first release: rejected because it would delay the primary value of
  conversational control.

## Decision: Ask for confirmation only on sensitive, high-impact, or poorly reversible actions

### Rationale
- Always asking for confirmation would make ordinary light and switch control too
  cumbersome.
- Never asking for confirmation would conflict with the safety model for
  higher-risk actions as the domain set expands.
- A policy-based confirmation layer can be reused by the future voice channel.

### Alternatives considered
- Confirm every state-changing action: rejected because it hurts usability.
- Never confirm once a target is resolved: rejected because it is too weak for
  future higher-impact actions.
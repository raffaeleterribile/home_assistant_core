# Tasks: AI Device Agent

**Input**: Design documents from `/specs/001-ai-device-agent/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Tests are required for this feature because it changes conversation behavior, registry synchronization, permissions, and device actuation.

**Organization**: Tasks are grouped by user story so each story remains independently implementable and testable.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (`US1`, `US2`, `US3`)
- Every task includes exact file paths

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create the integration skeleton and shared files needed before runtime behavior is added.

- [ ] T001 Create the integration skeleton in `homeassistant/components/ai_device_agent/__init__.py`, `homeassistant/components/ai_device_agent/manifest.json`, and `tests/components/ai_device_agent/__init__.py`.
- [ ] T002 Create shared constants and typed runtime models in `homeassistant/components/ai_device_agent/const.py` and `homeassistant/components/ai_device_agent/models.py`.
- [ ] T003 [P] Add configuration and translation scaffolding in `homeassistant/components/ai_device_agent/strings.json` and generate `homeassistant/components/ai_device_agent/translations/en.json`.
- [ ] T004 Capture local-first, privacy, supported-domain, and backend-unavailability constraints in module-level setup comments and logger wiring inside `homeassistant/components/ai_device_agent/__init__.py` and `homeassistant/components/ai_device_agent/coordinator.py`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Build the infrastructure all user stories depend on.

**⚠️ CRITICAL**: No user story work should start until this phase is complete.

- [ ] T005 Create the config entry setup and validation flow in `homeassistant/components/ai_device_agent/config_flow.py` and `tests/components/ai_device_agent/test_config_flow.py`.
- [ ] T006 [P] Implement the backend adapter and availability classification layer in `homeassistant/components/ai_device_agent/coordinator.py`.
- [ ] T007 [P] Implement permission, confirmation, and admin-only policy checks in `homeassistant/components/ai_device_agent/policy.py`.
- [ ] T008 [P] Implement deterministic inventory snapshot and target resolution primitives in `homeassistant/components/ai_device_agent/intent_resolver.py`.
- [ ] T009 Implement integration setup, unload, and conversation agent registration in `homeassistant/components/ai_device_agent/__init__.py` and `homeassistant/components/ai_device_agent/conversation.py`.
- [ ] T010 Configure audit-friendly outcome logging and structured backend failure handling in `homeassistant/components/ai_device_agent/conversation.py` and `homeassistant/components/ai_device_agent/coordinator.py`, including full command text, resolved target, attempted action, outcome, and refusal reason.

**Checkpoint**: Foundation ready. User story implementation can now proceed.

---

## Phase 3: User Story 1 - Control Devices With Text Commands (Priority: P1) 🎯 MVP

**Goal**: Let users query and control lights and switches through text commands, including supported area-based and multi-target requests, with deterministic target resolution, permission checks, and safe confirmation behavior.

**Independent Test**: A user can ask to list, describe, and control supported lights and switches through conversation, including area-based or multi-target requests, get clarification for ambiguity, and see successful or rejected results without touching the manual UI.

### Tests for User Story 1 ⚠️

- [ ] T011 [P] [US1] Add conversation tests for supported light and switch listing, description, single-target commands, area-based or multi-target commands, mixed supported/unsupported target sets, mixed available/unavailable target sets, and explicit candidate-list ambiguity handling with selection by index or by name in `tests/components/ai_device_agent/test_conversation.py`.
- [ ] T012 [P] [US1] Add policy tests for permission enforcement, no-confirmation execution for supported light/switch actions, and unsupported-domain rejection in `tests/components/ai_device_agent/test_permissions.py`.
- [ ] T012A [P] [US1] Add a mock discovery agent harness for the question “which devices are configured?” and validate the response against the real Home Assistant registry data in `tests/components/ai_device_agent/test_conversation.py`.
- [ ] T012B [P] [US2] Add a mock lifecycle agent harness that simulates device add/remove operations and verifies registry-driven discovery changes in `tests/components/ai_device_agent/test_sync.py`.
- [ ] T012C [P] [US2] Add a mock event/service agent harness that simulates device event ingestion and service dispatch for command execution in `tests/components/ai_device_agent/test_sync.py` and `tests/components/ai_device_agent/test_unavailability.py`.

### Implementation for User Story 1

- [ ] T013 [P] [US1] Implement `CommandRequest`, `ResolvedTarget`, and `CommandExecution` runtime models in `homeassistant/components/ai_device_agent/models.py`.
- [ ] T014 [P] [US1] Implement light and switch target selection, supported-target discovery, area-based and multi-target resolution, mixed-set partitioning, ambiguity detection with explicit candidate lists, candidate ordering, and unsupported-domain handling in `homeassistant/components/ai_device_agent/intent_resolver.py`.
- [ ] T015 [US1] Implement the text conversation flow for light and switch discovery and actuation in `homeassistant/components/ai_device_agent/conversation.py`.
- [ ] T016 [US1] Wire resolved single-target and multi-target actions to `hass.services.async_call` with preserved user context in `homeassistant/components/ai_device_agent/conversation.py`.
- [ ] T017 [US1] Enforce no-confirmation execution for supported light/switch actions and admin gating for sensitive or configurative actions in `homeassistant/components/ai_device_agent/policy.py` and `homeassistant/components/ai_device_agent/conversation.py`.
- [ ] T018 [US1] Add user-facing outcome messages and trace-friendly logging for text command execution in `homeassistant/components/ai_device_agent/conversation.py`, including full command text in operator traces and explicit reporting of excluded unsupported or unavailable targets in mixed-set execution.

**Checkpoint**: User Story 1 should now be fully functional and independently testable.

---

## Phase 4: User Story 2 - Stay Synchronized With Home Assistant Changes (Priority: P2)

**Goal**: Keep the agent aligned with config entries, device/entity registry updates, and state changes so later text interactions reflect current Home Assistant reality.

**Independent Test**: Adding, removing, renaming, enabling, disabling, or changing a relevant target is reflected in later conversations without manual rebuild or restart.

### Tests for User Story 2 ⚠️

- [ ] T019 [P] [US2] Add synchronization tests for config entries, device registry, entity registry, area-derived target sets, availability changes, and state changes in `tests/components/ai_device_agent/test_sync.py`.
- [ ] T020 [P] [US2] Add backend-unavailability and lifecycle tests in `tests/components/ai_device_agent/test_unavailability.py`.

### Implementation for User Story 2

- [ ] T021 [P] [US2] Implement inventory snapshot refresh and cache invalidation for config entries, devices, entities, and state in `homeassistant/components/ai_device_agent/coordinator.py`.
- [ ] T022 [US2] Subscribe and unsubscribe listeners for registry and state updates in `homeassistant/components/ai_device_agent/__init__.py` and `homeassistant/components/ai_device_agent/conversation.py`.
- [ ] T023 [US2] Implement temporary unavailability responses when the backend adapter fails in `homeassistant/components/ai_device_agent/coordinator.py` and `homeassistant/components/ai_device_agent/conversation.py`.
- [ ] T024 [US2] Integrate config entry reload, unload, and re-registration behavior in `homeassistant/components/ai_device_agent/__init__.py` and `homeassistant/components/ai_device_agent/config_flow.py`.

**Checkpoint**: User Stories 1 and 2 should both work independently.

---

## Phase 5: User Story 3 - Keep The Design Reusable For Future Voice Support (Priority: P3)

**Goal**: Preserve a channel-neutral command, clarification, and confirmation model that a later voice adapter can reuse without changing business logic.

**Independent Test**: The conversation flow exposes reusable request/session/response abstractions and confirmation logic that are not tied to text-only assumptions.

### Tests for User Story 3 ⚠️

- [ ] T025 [P] [US3] Add tests for channel-neutral clarification state handling and future-ready confirmation hooks in `tests/components/ai_device_agent/test_conversation.py`.
- [ ] T026 [P] [US3] Add tests proving response/session models remain reusable for future voice adapters in `tests/components/ai_device_agent/test_conversation.py` and `tests/components/ai_device_agent/test_sync.py`.

### Implementation for User Story 3

- [ ] T027 [P] [US3] Refine channel-neutral conversation session and response abstractions in `homeassistant/components/ai_device_agent/models.py`.
- [ ] T028 [US3] Extract reusable clarification response builders with explicit candidate lists and selection by index or name, plus future confirmation response builders in `homeassistant/components/ai_device_agent/conversation.py`.
- [ ] T029 [US3] Isolate backend request/response shaping behind the adapter contract in `homeassistant/components/ai_device_agent/coordinator.py` and `homeassistant/components/ai_device_agent/conversation.py`.

**Checkpoint**: All planned user stories should now be independently functional.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Finish documentation, validation, and release-readiness work across stories.

- [ ] T030 [P] Regenerate translations for the integration with `python3 -m script.translations develop --integration ai_device_agent` after finalizing `homeassistant/components/ai_device_agent/strings.json`.
- [ ] T031 Run focused pytest validation for the new integration with `uv run --no-sync pytest tests/components/ai_device_agent -q` and record timing observations as non-blocking operational targets.
- [ ] T032 Run targeted lint/format validation for touched files with `uv run --no-sync prek run --files homeassistant/components/ai_device_agent tests/components/ai_device_agent`.
- [ ] T033 Review privacy, logging, and unsupported-domain messaging across `homeassistant/components/ai_device_agent/conversation.py`, `homeassistant/components/ai_device_agent/coordinator.py`, and `homeassistant/components/ai_device_agent/policy.py`, confirming that full command-text tracing matches the approved scope.
- [ ] T034 Validate the manual flow in `specs/001-ai-device-agent/quickstart.md` against the implemented feature.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1: Setup**: no dependencies, starts immediately.
- **Phase 2: Foundational**: depends on Phase 1 and blocks all user stories.
- **Phase 3: User Story 1**: depends on Phase 2 and provides the MVP.
- **Phase 4: User Story 2**: depends on Phase 3 foundations and may share the same runtime primitives.
- **Phase 5: User Story 3**: depends on the conversation/runtime flow established in Phases 3 and 4.
- **Phase 6: Polish**: depends on all desired user stories being complete.

### User Story Dependencies

- **US1**: can start as soon as Phase 2 is complete.
- **US2**: depends on the agent registration and execution flow established for US1.
- **US3**: depends on the request/response/session flow already working for US1 and US2.

### Within Each User Story

- Tests should be written before or alongside implementation so failures are observable before the story is considered done.
- Runtime models and deterministic resolution should land before full conversation orchestration.
- Policy checks must be in place before service execution is considered complete.
- Story-specific validation should run before moving to the next story.

### Parallel Opportunities

- `T003` can run in parallel with `T002` once the integration skeleton exists.
- `T006`, `T007`, and `T008` can run in parallel after Phase 1.
- `T011` and `T012` can run in parallel.
- `T013` and `T014` can run in parallel.
- `T019` and `T020` can run in parallel.
- `T025` and `T026` can run in parallel.

---

## Parallel Example: User Story 1

```text
T011 [US1] tests/components/ai_device_agent/test_conversation.py
T012 [US1] tests/components/ai_device_agent/test_permissions.py
T013 [US1] homeassistant/components/ai_device_agent/models.py
T014 [US1] homeassistant/components/ai_device_agent/intent_resolver.py
```

---

## Implementation Strategy

### MVP First

1. Complete Phase 1 and Phase 2.
2. Deliver User Story 1 for text-based light and switch control.
3. Run `T031` for focused validation.
4. Stop and demo the MVP before expanding synchronization and future-voice readiness.

### Incremental Delivery

1. Setup + Foundation
2. US1 → validate text control
3. US2 → validate synchronization and unavailable-backend behavior
4. US3 → validate reusable conversation/session abstractions for future voice support
5. Polish → translations, lint, quickstart validation

### Team Strategy

With multiple developers:

1. One developer prepares setup and config flow.
2. One developer builds policy + resolver primitives.
3. One developer prepares tests in parallel once Phase 2 is stable.

---

## Notes

- Keep `ConfigEntries`, `DeviceRegistry`, `EntityRegistry`, the state machine, and service dispatch as the only sources of truth.
- Do not add queued command execution or implicit local actuation fallback for backend outages.
- Restrict first-release actuation to `light` and `switch` domains.
- Preserve caller context for every service execution path.
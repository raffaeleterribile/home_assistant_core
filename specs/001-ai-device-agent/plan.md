# Implementation Plan: AI Device Agent

**Branch**: `[001-ai-device-agent]` | **Date**: 2026-08-21 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-ai-device-agent/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Deliver a first conversational control slice for Home Assistant that supports
text-based discovery and actuation of lights and switches while staying aligned
with Home Assistant registries, config entries, permissions, and service
dispatch. The design uses a dedicated Home Assistant integration layered onto
the conversation stack, a deterministic target-resolution/policy-enforcement
path around the model, and a fail-closed backend adapter that returns a clear
unavailability message when the external model or orchestration backend is down.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.14  
**Primary Dependencies**: Home Assistant conversation framework, config entries, device/entity registries, intent/service APIs, external OpenAI-compatible model gateway, agent orchestration adapter  
**Storage**: Existing Home Assistant config entries, registries, and state machine; no new first-phase persistent store  
**Testing**: `pytest`, targeted Home Assistant component integration tests, conversation flow tests  
**Target Platform**: Local Home Assistant Core installations on Linux-class hosts, including Raspberry Pi deployments
**Project Type**: Home Assistant core integration/component with conversational agent surface  
**Performance Goals**: Successful text query/action in under 30 seconds; inventory/state changes reflected in later conversations within 5 seconds; explicit refusal on backend unavailability  
**Constraints**: Local-first/privacy-first, async-first runtime code, first release limited to lights and switches, existing HA permission model reused, admin required for sensitive/configurative actions, confirmation only for high-impact actions, no queued execution or implicit fallback actuation when backend is unavailable  
**Scale/Scope**: First release is text-only, supports light and switch actuation, synchronizes against all configured integrations and relevant runtime updates, and preserves a design path for future voice support

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- PASS: Remote model/orchestration remains optional; when unavailable the agent
  refuses commands explicitly and does not break existing Home Assistant manual
  controls.
- PASS: Privacy-sensitive data flow is bounded to the minimum conversational
  context required by the external model adapter and is documented for the
  design.
- PASS: The design keeps `ConfigEntries`, `DeviceRegistry`, `EntityRegistry`,
  the state machine, and service dispatch as the only sources of truth and
  control.
- PASS: Sensitive or device-mutating actions use Home Assistant permission
  boundaries, with admin requirements for sensitive/configurative operations and
  confirmation for high-impact actions.
- PASS: Validation covers conversation flow, registry/state synchronization,
  permissions, unsupported domains, and backend-unavailable behavior.
- PASS: Resource expectations remain compatible with local Home Assistant
  installations, including Raspberry Pi class hardware, because the runtime core
  stays async-first and rejects unavailable backend work quickly.

**Post-Phase 1 Re-check**

- PASS: Phase 1 design keeps voice as an adapter concern, avoiding a second
  business-logic path.
- PASS: Contracts and data model enforce deterministic target resolution and
  policy checks outside the model.
- PASS: No constitutional violations or complexity exceptions are required.

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-device-agent/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/
│   ├── backend-gateway-contract.md
│   └── conversation-agent-contract.md
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
homeassistant/
├── components/
│   ├── ai_device_agent/
│   │   ├── __init__.py
│   │   ├── config_flow.py
│   │   ├── conversation.py
│   │   ├── coordinator.py
│   │   ├── intent_resolver.py
│   │   ├── manifest.json
│   │   ├── models.py
│   │   ├── policy.py
│   │   └── strings.json
│   └── conversation/
│       └── [reuse existing conversation manager/agent hooks]
└── helpers/
  └── [reuse existing intent/service/registry helpers]

tests/
└── components/
  └── ai_device_agent/
    ├── test_config_flow.py
    ├── test_conversation.py
    ├── test_permissions.py
    ├── test_sync.py
    └── test_unavailability.py
```

**Structure Decision**: [Document the selected structure and reference the real
directories captured above]

**Structure Decision**: Implement the feature as a dedicated Home Assistant
integration under `homeassistant/components/ai_device_agent/` that plugs into
the existing conversation stack instead of creating a parallel HTTP/WebSocket
surface. Tests live in `tests/components/ai_device_agent/`, while Home
Assistant core registries, services, and state management remain reused rather
than wrapped or duplicated.

## Complexity Tracking

No constitutional violations identified.

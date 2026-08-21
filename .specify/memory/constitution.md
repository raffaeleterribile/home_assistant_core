<!--
Sync Impact Report
Version change: template -> 1.0.0
Modified principles:
- Template Principle 1 -> I. Local-First, Privacy-First Automation
- Template Principle 2 -> II. Integration-Native Architecture
- Template Principle 3 -> III. Safe, Explicit Device Actuation
- Template Principle 4 -> IV. Verification Before Merge
- Template Principle 5 -> V. Incremental Open Source Maintainability
Added sections:
- System Constraints
- Development Workflow
Removed sections:
- None
Templates requiring updates:
- ✅ .specify/templates/plan-template.md
- ✅ .specify/templates/spec-template.md
- ✅ .specify/templates/tasks-template.md
- ✅ .specify/templates/commands/*.md (not present in this repository; no update required)
Follow-up TODOs:
- None
-->
# Home Assistant Core Constitution

## Core Principles

### I. Local-First, Privacy-First Automation
Home Assistant Core MUST preserve local control and privacy as default product
properties. New capabilities MUST work on locally installed systems, including
resource-constrained deployments such as Raspberry Pi class hardware, unless the
feature is explicitly documented as optional cloud augmentation. Remote services,
LLMs, or speech providers MUST be opt-in, MUST disclose what data leaves the
system, and MUST fail without breaking primary local home-control flows.

### II. Integration-Native Architecture
Features MUST build on Home Assistant's established abstractions: config entries
for configured integrations, device and entity registries for inventory,
services for commands, and the event bus/state machine for observation. New
features MUST NOT introduce parallel sources of truth for devices or entity
state. Cross-integration coupling MUST remain minimal, and any deviation from
core abstractions MUST be justified in the implementation plan.

### III. Safe, Explicit Device Actuation
Any feature that can change device state, configuration, or security posture
MUST resolve targets explicitly and use established service or entity control
paths. Sensitive or destructive operations MUST enforce the correct permission
boundary, normally admin-only when configuration or security is affected.
Ambiguous user intent, especially in text or voice interfaces, MUST resolve to a
safe clarification path rather than silent guessing.

### IV. Verification Before Merge
Behavior-changing work MUST ship with executable verification. Changes to
registries, service routing, config entry behavior, event handling, or device
actuation MUST include targeted tests at the narrowest meaningful scope, with
integration tests whenever multiple Home Assistant subsystems interact. A task,
plan, or pull request is incomplete until it identifies and runs the relevant
validation commands.

### V. Incremental Open Source Maintainability
Specifications, plans, and tasks MUST break work into independently valuable and
testable slices. Changes MUST stay minimal, understandable, and aligned with the
existing Home Assistant architecture so maintainers can review them without
reverse-engineering hidden behavior. User-visible contract changes, migration
impacts, or breaking changes MUST be documented before implementation is
approved.

## System Constraints

- Runtime truth for configured integrations, devices, entities, services, and
	state MUST remain in Home Assistant core managers such as ConfigEntries,
	DeviceRegistry, EntityRegistry, ServiceRegistry, and the state machine.
- New automation or AI-facing features MUST treat those managers as the only
	authoritative inventory and control surfaces.
- Async-first design is mandatory for runtime code; blocking or heavyweight work
	MUST be isolated so local installations remain responsive.
- Features intended for everyday use MUST document expected behavior when cloud
	access, external AI providers, microphones, or speakers are unavailable.

## Development Workflow

- Every spec MUST identify the user-facing scenario, the local/privacy impact,
	the primary Home Assistant abstractions involved, and the fallback behavior
	when optional remote dependencies are unavailable.
- Every implementation plan MUST include a Constitution Check covering local
	control, privacy/data flow, use of core Home Assistant abstractions,
	permissions for sensitive actions, test strategy, and resource impact on local
	deployments.
- Every task list MUST include explicit validation tasks for the affected user
	stories and MUST call out privacy, permission, or performance work when those
	concerns are in scope.
- Reviews MUST reject work that bypasses core registries/services without
	justification, weakens local control, or omits executable verification for
	changed behavior.

## Governance
This constitution supersedes ad hoc workflow preferences for feature design in
this repository. Amendments MUST be made in the same change that updates the
dependent Spec Kit templates when those templates encode constitutional rules.
Versioning follows semantic versioning for governance: MAJOR for incompatible
principle changes or removals, MINOR for new principles or materially expanded
requirements, PATCH for clarifications that do not change expected behavior.
Compliance MUST be checked during specification, planning, task generation, code
review, and final validation. Runtime implementation guidance in AGENTS.md and
.github/copilot-instructions.md MUST remain consistent with this constitution.

**Version**: 1.0.0 | **Ratified**: 2026-08-21 | **Last Amended**: 2026-08-21

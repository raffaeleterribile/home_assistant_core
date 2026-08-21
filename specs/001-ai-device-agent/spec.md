# Feature Specification: AI Device Agent

**Feature Branch**: `[001-ai-device-agent]`  
**Created**: 2026-08-21  
**Status**: Draft  
**Input**: User description: "Sviluppare un agente AI per la gestione completa dei dispositivi registrati in Home Assistant, con una prima fase basata su comandi testuali, una fase successiva dedicata ai comandi vocali e integrazione con i componenti Home Assistant già analizzati per inventario, sincronizzazione eventi e invio comandi."

## Clarifications

### Session 2026-08-21

- Q: Quale modello di autorizzazione deve usare l'agente per i comandi ai dispositivi? → A: I comandi seguono i permessi esistenti di Home Assistant; le azioni sensibili o configurative richiedono admin.
- Q: Quale deve essere il perimetro del primo rilascio? → A: Il primo rilascio copre un sottoinsieme di domini comuni e sicuri, poi si estende progressivamente.
- Q: Quando l'agente deve chiedere conferma prima di eseguire un'azione? → A: L'agente chiede conferma solo per azioni sensibili, ad alto impatto o poco reversibili.
- Q: Quali domini devono essere inclusi nel primo rilascio? → A: Solo luci e switch.
- Q: Come deve comportarsi l'agente quando il modello o l'orchestrazione esterna non sono disponibili? → A: L'agente rifiuta temporaneamente i comandi e restituisce un messaggio chiaro di indisponibilità.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Control Devices With Text Commands (Priority: P1)

As a Home Assistant user, I want to issue natural-language text commands to inspect and control any registered device so that I can manage my home from a single conversational interface without manually navigating individual dashboards.

**Why this priority**: This is the first deliverable phase and the minimum valuable slice. If text command discovery and actuation work for lights and switches, the project already provides practical value before voice support or broader domain coverage is added.

**Independent Test**: Can be fully tested by connecting the agent to an existing Home Assistant instance, requesting device information or actions by text, and confirming that the intended device state or response is produced without using existing manual UI flows.

**Acceptance Scenarios**:

1. **Given** a user has configured integrations and registered devices, **When** the user asks the agent to list, find, or describe devices in text, **Then** the agent returns results derived from the current Home Assistant inventories.
2. **Given** a user issues a valid text command for a controllable light or switch in the supported first-release domain set, **When** the target device and action are unambiguous, **Then** the system executes the action and reports the outcome.
3. **Given** a user references a device or action ambiguously, **When** the agent cannot safely determine the intended target or command, **Then** the system asks for clarification instead of guessing.

---

### User Story 2 - Stay Synchronized With Home Assistant Changes (Priority: P2)

As a Home Assistant user, I want the agent to stay synchronized with device additions, removals, entity changes, and state changes so that conversational responses always reflect the current system.

**Why this priority**: A conversational controller is not trustworthy if its device map goes stale. This story ensures the text agent remains aligned with the live Home Assistant installation.

**Independent Test**: Can be fully tested by adding, removing, renaming, enabling, disabling, or changing devices/entities in Home Assistant and verifying that subsequent text interactions reflect the updated state without rebuilding the agent manually.

**Acceptance Scenarios**:

1. **Given** a new device or integration is added to Home Assistant, **When** the relevant Home Assistant inventories are updated, **Then** the agent includes the new capability in later text interactions.
2. **Given** a device, entity, or integration is removed or becomes unavailable, **When** the Home Assistant change is processed, **Then** the agent stops presenting that target as available for control.
3. **Given** a device state changes outside the agent, **When** the user asks about that device afterward, **Then** the response reflects the latest known state.

---

### User Story 3 - Extend The Same Control Model To Voice (Priority: P3)

As a Home Assistant user, I want the same device control model to support voice input in a later phase so that I can move from text commands to spoken commands without relearning how to interact with the system.

**Why this priority**: Voice support is explicitly deferred, but the first-phase design must not make a later voice channel harder or require a different device-control model.

**Independent Test**: Can be fully tested by validating that the text-based command model, confirmations, clarifications, and permissions are defined in a way that a later voice interface can reuse them without changing the user-facing device semantics.

**Acceptance Scenarios**:

1. **Given** the first phase delivers text control only, **When** voice support is introduced later, **Then** the same device discovery, clarification, permission, and actuation behaviors can be reused.

### Edge Cases

- What happens when the external model endpoint or orchestration dependency is unavailable while Home Assistant itself remains available?
- How does the system behave when multiple devices share similar names, areas, or functions?
- How does the system handle requests for devices that are registered but currently unavailable or disconnected?
- How does the system behave when a user asks for an action that exists in Home Assistant but requires elevated permissions or affects configuration rather than runtime device state?
- What happens when Home Assistant inventories change while a conversational session is in progress?
- How does the system respond when a request targets a valid Home Assistant domain that is intentionally outside the supported first-release subset?
- How does the system classify which actions require an explicit confirmation because they are sensitive, high-impact, or not easily reversible?
- What response does the system give when the user requests control of supported entities outside the initial lights-and-switches release scope, such as climate or cover?
- How does the system refuse commands cleanly when the external model or orchestration backend is temporarily unavailable?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST allow users to discover and control Home Assistant devices through natural-language text commands in the first delivery phase.
- **FR-002**: The system MUST treat the configured integration inventory and the device inventory already maintained by Home Assistant as the authoritative source of available capabilities.
- **FR-003**: The system MUST derive commandable targets from the current Home Assistant representation of devices, entities, and services rather than maintaining a separate manual catalog.
- **FR-004**: The system MUST stay synchronized with additions, removals, and updates affecting configured integrations, devices, entities, and device state.
- **FR-005**: The system MUST execute device actions through the established Home Assistant command surfaces for those devices.
- **FR-006**: The system MUST provide clear feedback after each user command, including success, refusal, failure, or clarification required.
- **FR-007**: The system MUST ask for clarification when the requested device, area, entity, or action is ambiguous.
- **FR-008**: The system MUST prevent unsafe or unauthorized actions from being executed silently.
- **FR-013**: The system MUST reuse Home Assistant's existing permission model for standard device commands.
- **FR-014**: The system MUST require administrator-level authorization for sensitive or configurative actions.
- **FR-009**: The system MUST keep existing Home Assistant manual control paths usable even when the agent subsystem or model endpoint is unavailable.
- **FR-010**: The system MUST be designed so that a later voice-input phase can reuse the same device discovery, resolution, permission, and actuation behavior introduced for text commands.
- **FR-011**: The first-phase specification MUST record the already identified Home Assistant components that provide inventory, update, event, and command responsibilities relevant to the agent.
- **FR-012**: The system MUST expose enough traceability for operators to understand what command was attempted, which target was resolved, and why the result succeeded, failed, or required clarification.
- **FR-015**: The first release MUST support only a deliberately bounded subset of common, low-risk Home Assistant domains and MUST reject or clearly defer unsupported domains.
- **FR-016**: The supported first-release domain set MUST be documented explicitly before implementation planning is completed.
- **FR-017**: The system MUST request explicit confirmation before executing actions classified as sensitive, high-impact, or not easily reversible.
- **FR-018**: The system MUST execute low-risk, unambiguous commands without an extra confirmation step.
- **FR-019**: The supported first-release domain set MUST be limited to lights and switches.
- **FR-020**: The system MUST clearly indicate when a requested domain is not yet supported in the current release.
- **FR-021**: When the external model or orchestration backend is unavailable, the system MUST refuse agent commands temporarily and return a clear unavailability message.
- **FR-022**: Backend unavailability MUST NOT trigger queued execution or implicit fallback actuation in the first release.

### Key Entities *(include if feature involves data)*

- **Configured Integration Inventory**: The current set of configured Home Assistant integrations that determines what device ecosystems and capabilities are present.
- **Managed Device Inventory**: The current set of Home Assistant devices available to the user, including metadata needed for discovery, grouping, and targeting.
- **Commandable Entity**: A Home Assistant control surface associated with a device that can report state or accept actions.
- **Device Change Signal**: The stream of device, entity, integration, and state updates that keeps the agent synchronized with Home Assistant.
- **Command Request**: A user-issued instruction that must be resolved into a specific target and action before execution.
- **Conversation Session**: The active interaction context used to ask clarifying questions, maintain user intent, and report results.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: In the first phase, a user can complete a successful text-based device query or device action against a known target in under 30 seconds from opening the conversational interface.
- **SC-002**: At least 95% of valid text commands against known controllable targets produce either a successful result or an explicit clarification request, with no silent failure.
- **SC-003**: Changes to configured integrations, devices, entities, or device state become visible to later conversational interactions within 5 seconds of Home Assistant processing those changes.
- **SC-004**: When the external model or orchestration dependency is unavailable, 100% of affected user attempts receive a clear failure message while existing non-agent Home Assistant control flows remain unaffected.

## Assumptions

- The first release phase covers text-based interaction only; voice input is intentionally deferred to a later phase.
- The first release targets a progressive rollout that starts with lights and switches rather than every commandable Home Assistant domain.
- Users interact with the agent from an authenticated Home Assistant context that can enforce the same permission boundaries expected for sensitive actions.
- Standard device commands inherit the caller's existing Home Assistant permissions, while sensitive or configurative actions are admin-only.
- Only sensitive, high-impact, or poorly reversible actions require an explicit confirmation step before execution.
- If the external model or orchestration backend is unavailable, the first release refuses agent commands instead of attempting a partial fallback.
- Existing Home Assistant abstractions for configured integrations, devices, entities, services, and state are reused as the authoritative runtime inventory and command surfaces.
- Initial technical exploration assumes an agent orchestration layer and model endpoint that can start from an external compatible service and later move into a more internally managed deployment without changing the user-facing behavior.
- Local installations, including Raspberry Pi class deployments, remain a first-class operating environment for the feature.

## Current System Context

### Identified Home Assistant Components

- **Configured integrations manager**: `ConfigEntries` is the manager for configured integrations and exposes the active inventory of config entries used by the system.
- **Device inventory manager**: `DeviceRegistry` is the central registry for devices known to Home Assistant.
- **Entity inventory manager**: `EntityRegistry` is the central registry for entities and the practical bridge between devices and commandable surfaces.
- **Device add, update, and remove signal**: the `device_registry_updated` event represents create, update, and remove activity for devices.
- **Entity add, update, and remove signal**: the `entity_registry_updated` event represents create, update, and remove activity for entities.
- **Live state signal**: the `state_changed` event represents runtime state changes that matter for conversational awareness.
- **Command dispatch surface**: `ServiceRegistry` is the core command-dispatch surface through which Home Assistant executes supported actions.
- **Conversational integration example already present in Home Assistant**: the default conversation agent already listens to registry and state changes, which confirms that these signals are valid synchronization points for conversational features.

### Initial Delivery Direction

- The project is planned as an AI agent capability layered onto Home Assistant rather than a parallel device-control system.
- The first delivery milestone supports text commands only.
- The first delivery milestone supports only the light and switch domains for actuation.
- A later milestone extends the same control model to voice interactions.
- Current delivery planning assumes an agent orchestration layer and a compatible model endpoint, starting from an external prototype deployment and later moving toward a more internalized deployment model.
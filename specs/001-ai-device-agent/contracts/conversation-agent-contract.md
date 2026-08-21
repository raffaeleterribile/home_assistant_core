# Contract: Conversation Agent

## Purpose
Defines the user-facing behavioral contract for the first-release text agent.

## Supported Interaction Scope
- Channel: text only
- Supported domains: `light`, `switch`
- Supported outcome classes: `success`, `clarification_required`,
  `unsupported_domain`, `unauthorized`, `confirmation_required`, `unavailable`,
  `failure`

## Input Contract

### Required Inputs
- Authenticated Home Assistant user context
- Raw text request
- Active Home Assistant inventory and state context

### Example Input Shapes
- `Turn on the kitchen light`
- `List all switches in the garage`
- `Turn off the lamp in the office`

## Output Contract

### Success Response
- Must identify the target it acted upon
- Must identify the action taken
- Must state whether execution completed successfully

### Clarification Response
- Must explain why the request is ambiguous
- Must ask a follow-up question that reduces the ambiguity
- Must not trigger any service call

### Unsupported Domain Response
- Must explain that the requested domain is not supported in the current release
- Must not imply that the device itself is unknown if it exists

### Unauthorized Response
- Must explain that the caller lacks permission for the action
- Must not leak unnecessary protected detail

### Confirmation Response
- Must state which action is about to run
- Must state why confirmation is required
- Must not execute until confirmation is received

### Backend Unavailable Response
- Must state that the agent is temporarily unavailable
- Must not queue the command for later execution
- Must not trigger service execution through any implicit fallback path

## Behavioral Guarantees
- The agent must resolve targets against Home Assistant runtime truth.
- The agent must preserve caller permissions into execution.
- The agent must never guess between multiple plausible targets.
- The agent must reject unsupported domains clearly.

## First-Release Non-Goals
- Voice input/output
- Multi-device fan-out execution from a single vague request
- Delayed or queued execution when the backend is unavailable
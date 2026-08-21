# Quickstart: AI Device Agent First Slice

## Goal
Validate the first-release text agent slice for Home Assistant with light and
switch support.

## Preconditions
- Home Assistant development environment is set up.
- A feature integration exists under `homeassistant/components/ai_device_agent/`.
- Test fixtures include at least one light, one switch, one unsupported domain,
  and one unavailable target.

## Validation Flow

1. Configure the agent integration with a reachable backend adapter.
2. Verify that the agent is selectable through the Home Assistant conversation
   flow.
3. Submit a text request to list or describe supported light/switch targets.
4. Submit a text request to control a known light.
5. Submit a text request to control a known switch.
6. Submit an ambiguous request and confirm that the system asks for
   clarification.
7. Submit a request for an unsupported domain such as climate and confirm the
   response clearly defers or rejects the request.
8. Submit a request that requires elevated permission and confirm the system
   refuses it for a non-admin caller.
9. Simulate backend unavailability and confirm the system returns a temporary
   unavailability response without executing any service.
10. Add, remove, or rename a target and confirm a later conversation reflects
   the change without manual rebuild.

## Suggested Validation Commands

```powershell
uv run --no-sync pytest tests/components/ai_device_agent -q
uv run --no-sync pytest tests/components/ai_device_agent/test_conversation.py -q
uv run --no-sync pytest tests/components/ai_device_agent/test_permissions.py -q
uv run --no-sync pytest tests/components/ai_device_agent/test_sync.py -q
```

## Expected Outcomes
- Only lights and switches are controlled in the first release.
- Ambiguity never results in guessed actuation.
- Sensitive actions require confirmation and/or admin as defined by policy.
- Backend unavailability results in a clear refusal and no queued or fallback
  execution.
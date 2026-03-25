# Session Health Heuristic

## Goal

Define a simple first-pass health model for OPC-bound execution sessions.

---

## Inputs

Health should be inferred from both sides:

### Ledger side
- node status
- node updated_at
- result_summary presence
- recent task events

### Runtime side
- session updatedAt
- session status
- session last message presence

---

## Labels

### `done`
Use when:
- mapped node is `done` / `skipped` / `cancelled`

### `active`
Use when:
- mapped node is `running` or `review_pending`
- and recent task or session activity exists within threshold

### `idle`
Use when:
- session exists
- node is assigned/running
- but no recent useful result has been recorded yet

### `stale`
Use when:
- node is not done
- bound session exists
- last ledger + runtime activity both exceed threshold

---

## Initial threshold

Recommended default:
- `stale_after_minutes = 30`

Later this can become configurable per workflow type.

---

## Workflow-specific nuance

### Research
Can tolerate longer quiet periods during reading/synthesis.

### Coding
Should be monitored closely if node is running but file/result output is absent.

### Social
Needs tight monitoring when external write actions are in progress, especially around post-action verification.

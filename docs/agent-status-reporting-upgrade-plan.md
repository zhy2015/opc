# Agent Status Reporting Upgrade Plan

## Goal

Upgrade OPC reporting from task-level ledger visibility into agent-level operational visibility.

---

## Current baseline

Already available:
- `task-summary`
- `task-brief`
- `task-report`
- `task-events`
- task / node / review / event ledger

This means OPC can already answer:
- what task is active
- which node is done / running / review_pending
- what artifacts were produced

But it still cannot answer well enough:
- which agent is truly active
- which bound session is stale
- which session is hanging without result

---

## Next upgrade targets

### 1. Session activity summary

Add a reporting layer that shows, per bound session:
- session key
- mapped node
- role
- runtime / session mode
- last known ledger update time
- last known session activity time
- last useful output summary
- health label: `active` / `idle` / `stale` / `done`

### 2. Stalled detection

Recommended initial heuristic:
- `active`: node status is `running` and updated recently
- `idle`: session exists but no recent node-level output
- `stale`: bound session has no meaningful update beyond threshold
- `done`: node already completed

Recommended first threshold:
- `stale_after_minutes = 30`

### 3. CEO-facing diagnosis

For each task, report:
- which agents are pushing the task forward
- which agents are just occupying slots
- which nodes need follow-up
- whether review gate is the actual bottleneck

---

## Suggested CLI additions

### `task-agent-status TASK-XXXX`
Output one compact agent/session table-like summary for the task.

### `task-report --with-agents`
Extend detailed report with session health.

### `task-events --stalled-only`
Show nodes/sessions that appear inactive beyond threshold.

---

## Why this matters

Once OPC manages real multi-agent execution, the real question is no longer only:
- what is the task status?

It becomes:
- which agent is actually producing progress?
- who is blocked?
- who needs intervention?

That is the difference between:
- passive ledger
- operational command visibility

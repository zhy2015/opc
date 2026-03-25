# Agent Reporting Commands

## Goal

Document the current OPC reporting surface for task-level and agent-level visibility.

---

## Current commands

### Task-level
- `task-summary`
- `task-brief`
- `task-report`
- `task-events`

### Agent / session-level
- `task-agent-status`
- `task-report --with-agents`

---

## What each command is for

### `task-summary TASK-XXXX`
Machine-friendly JSON summary.

Use when:
- another tool or script needs task status
- you want compact structured output

### `task-brief TASK-XXXX`
Short human-readable status snapshot.

Use when:
- chat asks “现在怎么样了”
- you want one-screen progress

### `task-report TASK-XXXX`
Detailed operator report.

Use when:
- user asks for detailed task progress
- CEO needs node-by-node view
- you need result refs and resume cursor in one place

### `task-events TASK-XXXX --tail N --key-only`
Tail key lifecycle events.

Use when:
- diagnosing stalls
- checking whether review or result writeback happened

### `task-agent-status TASK-XXXX --sessions-file ...`
Session-health oriented view.

Use when:
- user asks “当前 agent 工作情况”
- you need to see health labels like `active / idle / stale / done`

### `task-report TASK-XXXX --with-agents --sessions-file ...`
Full report with node progress plus agent/session health.

Use when:
- you want the most complete current operational picture

---

## Current limitation

Agent/session health is currently based on:
- OPC ledger timestamps
- optional runtime session snapshot via `--sessions-file`

That means the health model already exists, but real-time runtime ingestion is not yet automatic.

---

## Recommended next step

Bridge `sessions_list` output directly into OPC reporting so the CLI can produce near-real-time agent health without a manual snapshot file.

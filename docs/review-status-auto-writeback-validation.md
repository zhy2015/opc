# Review → Node/Task Status Auto-Writeback Validation

## Goal

Validate that review decisions now automatically write back into both node status and task status, reducing manual control-plane syncing.

---

## Change made

In `scripts/opc.py`:
- added `recompute_task_status(task_id)`
- updated `task_review_decision(...)` to call automatic task-status recomputation after review decisions

This means review outcomes no longer need hand-written task status syncing in the common result-gate path.

---

## Validation cases

### Case 1: approve path
Task:
- `TASK-BIND-SESSION-DEMO-CODING`

Action:
- `task-review-decision ... --gate-type result_gate --decision approve`

Verified outcome:
- node status: `review_pending -> done`
- task status: `result_review -> delivered`
- `task-report` shows:
  - task = `delivered`
  - node = `done`
  - progress = `100%`

### Case 2: reject path
Task:
- `TASK-REVIEW-REWORK-DEMO`

Action:
- `task-review-decision ... --gate-type result_gate --decision reject`

Verified outcome:
- node status: `review_pending -> rework`
- task status: `result_review -> rework`
- `task-report` shows:
  - task = `rework`
  - node = `rework`

---

## What this improves

Before this change:
- review result handling partially depended on ad hoc task-level status mutation
- task status progression was less consistently derived from node truth

After this change:
- result-gate decisions propagate through node truth first
- task status is recomputed from node states
- the ledger behaves more like an actual control plane

---

## Remaining gap

The next obvious improvement is operator-facing status views:
- better board / summary views
- faster visibility into active sessions, review queues, and delivery readiness

---

## One-line conclusion

**Review decisions now automatically drive node/task writeback for both approve and reject paths, and the behavior has been verified with real CLI runs.**

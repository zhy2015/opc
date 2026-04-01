# OPC Agent Status View

This file defines the minimal status view the main session should maintain for sub-agents during OPC runs.

## Purpose

The main session should not merely know that sub-agents were spawned.
It should be able to see who is doing what, who is blocked, and where intervention may be needed.

## Minimum fields

For each active sub-agent, track at least:
- `agent_name`
- `task_scope`
- `state`
- `last_update_at`
- `current_blocker`
- `expected_output`
- `needs_intervention` (yes/no)

For creative-production runs, also strongly prefer:
- `lane_type`
- `artifact_level`
- `next_auto_handoff`
- `delivery_path_status`

For task-level closeout visibility, also prefer:
- `delivery_status`
- `delivery_object`
- `delivery_evidence_count`
- `delivery_risk_count`
- `user_consumable_result_ready` (yes/no)

## State vocabulary

Suggested per-agent states:
- `queued`
- `doing`
- `blocked`
- `review`
- `done`
- `cancelled`

Suggested task-level delivery states:
- `not_ready`
- `partial`
- `delivered`
- `fallback_delivered`
- `internal_only`

## Default status-view reflex

The status view should let the main session answer at a glance:
- **who owns what**
- **who is actually moving**
- **who is blocked**
- **who already has usable output**
- **where intervention belongs next**
- **whether a user-consumable result object exists yet**

If it cannot answer those quickly, the status view is too weak.

## Main-session use

The main session should use this view to answer:
- which agent is active?
- which agent is stalled?
- which agent has already produced something usable?
- where is the current bottleneck?
- who needs steering or reassignment?
- is there already a task-level delivery object?
- is that object user-consumable, fallback-only, or still internal?

For creative-production runs, “something usable” should bias toward verified artifacts or verified state changes, not raw claims from a worker or monitor.

## Anti-patterns

- tracking only that an agent exists, but not what it owns
- treating all spawned agents as equally healthy without recent signal
- waiting passively without a visible blocker model
- tracking worker activity but not delivery readiness

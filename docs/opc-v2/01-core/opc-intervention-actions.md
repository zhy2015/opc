# OPC Intervention Actions

This file defines the main intervention actions available to the main session during OPC.

## Core principle

The main session should not only observe.
It should have a clear vocabulary for intervening when delegated work drifts, stalls, or needs consolidation.

## Actions

### `steer`
Use when the agent is still viable but needs clarification, narrowing, or correction.

### `kill`
Use when the agent run is clearly unhelpful, duplicated, unsafe, or badly off-track.

### `reassign`
Use when the task scope should move to another sub-agent or return to the main session.

### `summarize`
Use when the main session needs the current useful partial result without waiting for a full finish.

### `pause`
Use when work should temporarily stop without being cancelled.

### `resume`
Use when paused work should continue.

### `escalate`
Use when the blocker should be surfaced to a higher-level decision rather than handled by the current worker alone.

## Structured intervention payload

When possible, interventions should carry more than an action verb.
Prefer attaching:
- `target_layer` — where the correction belongs (`planning` / `research` / `execution` / `verification` / `delivery_packaging`)
- `reason_type` — why intervention is needed (`missing_evidence` / `delivery_gap` / `runtime_failure` / `quality_failure` / `scope_mismatch` / `stall`)
- `expected_evidence_after_repair` — what should exist if the fix succeeds

This keeps intervention tied to repair shape rather than emotional urgency.

## Default intervention reflex

When a delegated run goes bad, ask in order:
1. **Is the run still viable?** If yes, steer.
2. **Is the scope wrong but the work still useful?** Reassign or summarize.
3. **Is it duplicated, badly off-track, or no longer worth attention?** Kill.

Choose the lightest intervention that restores control.
Do not kill when steering would suffice.
Do not keep steering when the scope itself is wrong and reassignment is cleaner.

When delivery or review gaps are visible, prefer explicit repair-shaped interventions such as:
- send back to `execution` for a delivery gap
- send back to `verification` for missing evidence
- send back to `planning` for scope mismatch
- escalate runtime failure when no honest fallback exists

## Anti-patterns

- passive waiting when a blocker is already visible
- overreacting with kill when a short steer would work
- leaving a duplicated run alive after it clearly lost usefulness
- issuing an intervention without making the repair target and expected evidence clear

# OPC Minimal Run Spec

This file defines the minimum operating spec for OPC runs.

## When to use OPC

Use OPC when the task is complex enough that controlled delegation is likely to outperform a single-threaded main-session run.
Typical signals:
- several meaningful sub-tasks exist
- some parts can run in parallel
- the task would benefit from explicit monitoring and integration
- the main session would otherwise become a bottleneck

Do not use OPC for trivial one-turn tasks.

## Lightweight planning profiles

OPC should not assume that every delegated task needs the heaviest controller shape.
Prefer a small set of lightweight planning profiles so the run shape matches the real task shape.

Recommended profiles:
- `direct_review` — one main execution path plus review; use when decomposition value is modest but review still matters
- `research_execute_review` — use when research materially reduces ambiguity before execution
- `execute_verify_review` — use when execution can start directly but explicit verification is still needed before closeout
- `full_controller` — use when the task has multiple moving lanes, drift risk, or delivery complexity large enough to justify full chief-controller posture

## Profile selection rule

Default to the lightest profile that can still preserve:
- truthfulness
- reviewability
- delivery clarity
- non-overlapping scopes

Do not use a lighter profile if it would hide blockers, collapse verification, or defer delivery thinking until too late.

## Default run posture

- start with the smallest useful number of sub-agents
- prefer staged parallelism over uncontrolled fan-out
- keep sub-task scopes explicit
- keep a visible status view
- expect intervention rather than passive waiting

## Default sub-agent count bias

Prefer fewer, clearer workers over many vague workers.
If two sub-agents are enough, do not spawn five.

Exception: in creative-production workflows with several genuinely independent lanes, under-spawning can be worse than modest fan-out. In those cases, prefer a small set of clearly separated production lanes over a thin planning-only start.

## Progress expectation

Each delegated run should have a clear expected output and a notion of meaningful progress.
The main session should know what signal would count as:
- useful progress
- blocker
- ready-for-review

For creative-production runs, “useful progress” should bias toward artifact-level movement and verified state change, not commentary, retries, or worker optimism.

## Stop condition

Stop or scale down OPC when:
- delegation no longer improves throughput
- blockers dominate progress
- the work is better completed by the main session directly
- enough partial output exists to finish integration without further fan-out

## Closeout

An OPC run should end with:
- integrated result
- explicit remaining work if incomplete
- blocker/risk visibility when relevant
- retention judgment routed back through MMM rather than implied by orchestration alone
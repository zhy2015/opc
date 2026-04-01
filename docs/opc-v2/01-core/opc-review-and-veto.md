# OPC Review and Veto

This file defines the review/veto mechanism for OPC.
The goal is to keep bad decomposition or low-quality sub-results from flowing through unchecked.

## Dispatch-time review gate

Before sub-agents are spawned, the main session should be able to veto dispatch when:
- the decomposition is still fuzzy
- parallelism would create overlap or confusion
- dependencies are unresolved
- expected outputs are unclear

## Result-time review gate

Before final delivery, the main session should be able to veto raw sub-results when:
- outputs overlap or contradict each other
- a blocker was hidden
- the result is incomplete but presented as complete
- integration quality is not yet acceptable
- the claimed task-level delivery object is missing, weakly evidenced, or not actually user-consumable

## Structured send-back object

When review blocks forward motion, prefer a structured send-back object instead of an unshaped "needs more work" judgment.

Suggested fields:
- `sendback_target` — `planning` / `research` / `execution` / `verification` / `delivery_packaging`
- `sendback_reason_type` — `missing_evidence` / `delivery_gap` / `runtime_failure` / `quality_failure` / `scope_mismatch`
- `missing_evidence` — what proof or artifact is still absent
- `required_fix_shape` — what kind of repair is needed next
- `recheck_owner` — who should re-open review after repair

The purpose is not bureaucracy.
The purpose is to make the return path explicit enough that the next correction step is obvious.

## Default review / veto reflex

Use veto in two places by default:
1. **before dispatch** if the split is still fuzzy, overlapping, or missing expected outputs
2. **before delivery** if the result is contradictory, incomplete, hiding blockers, or not yet integration-ready

Review and veto exist to protect final coherence.
They are not bureaucratic theater.
If the result is not ready, it should not flow through as if it were ready.

When veto happens after execution, bias toward answering four questions explicitly:
- what exactly failed review?
- where should the work go back?
- what evidence is still missing?
- who is expected to recheck the repaired result?

## Anti-patterns

- dispatching because the decomposition looks "good enough"
- forwarding sub-agent outputs without final review
- suppressing blockers to make the run look smoother than it was
- issuing a vague send-back without naming target layer or missing evidence

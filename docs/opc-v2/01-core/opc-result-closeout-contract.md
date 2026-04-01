# OPC Result Closeout Contract

This file defines how sub-agent results should be closed out and integrated before user delivery.

## Core rule

Sub-agent output is not the final user-facing answer by default.
The main session is responsible for integration and clean delivery.

## Minimum result structure

For each sub-agent result, the main session should be able to identify:
- what was completed
- what remains incomplete
- blockers or risks
- confidence / review notes when relevant
- what part is ready for final integration

## Default result closeout reflex

Before treating a delegated run as done, check:
- **what is actually complete**
- **what is still missing**
- **what blocker or risk matters**
- **what is directly ready for integration**

If those four are not clear, the run is not cleanly closed out yet.

For production-style runs, also ask one more hard question:
- **has the claimed artifact or delivery path been verified, rather than merely asserted by a worker?**

If the answer is no, treat the result as unverified and keep it below true delivery status.

## Task-level delivery object

Before final closeout, the main session should maintain one explicit task-level delivery object.
This object exists to stop fragmented worker outputs from being mistaken for a finished user result.

The delivery object should answer at least:
- `delivery_object` — what the user can actually receive or open
- `delivery_summary` — what this object materially contains
- `delivery_evidence` — what verified signals support the claimed state
- `delivery_status` — `not_ready` / `partial` / `delivered` / `fallback_delivered` / `internal_only`
- `delivery_risks` — what still limits confidence, access, or completeness

If there is no explicit task-level delivery object yet, the run may still be useful, but it is not cleanly closed out.

## Final delivery contract

The user-facing result should normally separate:
- completed work
- remaining work
- blockers / risks
- recommended next step

For creative-production tasks, do not let intermediate layers masquerade as final delivery. Plans, raw assets, and internal drafts should be labeled honestly. Unless the user explicitly asked for an earlier review layer, completion should mean the result object is directly accessible to the user.

The language of the closeout should not upgrade the state. If only L2 or L3 is verified, the summary must still sound like L2 or L3.
If the current result is only a fallback artifact or internal-only object, the closeout must say so plainly.

## Integration discipline

Before delivering, the main session should:
- resolve overlap between sub-agent outputs
- remove contradictory or duplicated fragments
- convert partial raw results into one coherent answer
- collapse sub-result fragments into one task-level delivery object
- keep claimed delivery state aligned with verified evidence rather than intention

## Anti-patterns

- forwarding raw fragmented sub-agent outputs as the final answer
- hiding blockers that matter
- pretending incomplete parallel work is complete
- losing track of what is done versus what is still pending
- claiming delivery because many sub-results exist, even though no task-level delivery object exists
- upgrading a fallback artifact into true delivered state without saying it is fallback

# OPC Creative SSOT Map

This file defines the current single-source-of-truth layout for creative-production OPC guidance.
Use it to prevent the new protocol from fragmenting back into scattered, half-overlapping rules.

## SSOT top layer

### Primary operating truth
- `references/opc-creative-operating-protocol.md`

This is the main unifying contract.
When guidance overlaps, prefer this file as the top-level creative-production protocol unless a narrower file clearly owns a more specific sub-question.

## Owned sub-questions

### Production skeleton / five-lane launch / completion ladder
Owner:
- `references/opc-creative-production-sop.md`

### Chief-controller self-check during runs
Owner:
- `references/opc-creative-chief-controller-checklist.md`

### Default next-action triggers after sub-results
Owner:
- `references/opc-creative-auto-handoff-map.md`

### Verification before promotion / delivery claims
Owner:
- `references/opc-creative-verification-gate.md`

### Failure pattern catalog
Owner:
- `references/opc-creative-failure-patterns.md`

### Background monitoring / dead-pipeline guardrails
Owner:
- `references/opc-background-monitoring-guardrails.md`

### Delivery/auth failure invalidation
Owner:
- `references/opc-delivery-auth-failure-handling.md`

### Closeout wording / level-accurate language
Owner:
- `references/opc-creative-closeout-language-rules.md`

### Lightweight planning/control template
Owner:
- `references/opc-creative-run-template.md`

## Upstream integration points

These are not the creative SSOT themselves, but they should point toward it rather than competing with it:
- `skills/story-to-video-director/SKILL.md`
- `skills/osv-manager/SKILL.md`
- `skills/osv-project-router/SKILL.md`
- `references/agents-core-detailed-rules.md`
- `references/result-delivery-closeout-checklist.md`
- `references/opc-definition.md`

## Merge / overwrite guidance

When new creative-production guidance appears, ask:
1. does the main protocol already cover it?
2. if not, which owned sub-question does it belong to?
3. should an older overlapping sentence be removed or weakened to a pointer?

Prefer:
- one main protocol
- a small number of specialized owner files
- pointers elsewhere

Avoid:
- repeating full rules in every entry point
- leaving older weaker guidance beside stronger new guidance
- creating parallel “almost the same” creative policy files

## Current normalization progress

Current state:
- main protocol exists
- owner map exists
- most specialized files now point back to SSOT
- upstream entry skills now reference the protocol and SSOT map

Remaining ideal end-state:
- any future overlapping creative guidance should be reduced to owner pointers quickly
- weaker duplicated wording in broader files should continue to be trimmed where safe

See the live remaining-work list in `references/opc-creative-normalization-todo.md`.

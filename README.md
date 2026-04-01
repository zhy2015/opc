# OPC Documentation Snapshot

This folder is a git-friendly document snapshot of the latest OPC system.
It is assembled from the current reference-layer OPC guidance and organized for standalone reading.

## What OPC is

OPC is the main-session orchestration pattern for complex work.
Its core purpose is to turn complex tasks into controlled parallel execution rather than free-form multi-agent chatter.

Core promise:
- delegate only when it creates leverage
- keep delegated work visible and controllable
- intervene when drift appears
- integrate before delivery

## Folder structure

- `core/` — general OPC doctrine
- `creative/` — creative-production OPC protocol stack
- `meta/` — convergence / status artifacts

## Recommended reading order

### General OPC
1. `core/opc-definition.md`
2. `core/opc-minimal-run-spec.md`
3. `core/opc-chief-controller-model.md`
4. `core/opc-dispatch-review-gate.md`
5. `core/opc-state-machine.md`
6. `core/opc-agent-status-view.md`
7. `core/opc-intervention-actions.md`
8. `core/opc-stall-timeout-fallback.md`
9. `core/opc-review-and-veto.md`
10. `core/opc-result-closeout-contract.md`
11. `core/opc-lightweight-board.md`
12. `core/opc-practical-acceptance-checklist.md`
13. `core/opc-mmm-boundary.md`
14. `core/opc-config-environment-boundary.md`

### Creative-production OPC
1. `creative/opc-creative-operating-protocol.md`
2. `creative/opc-creative-ssot-map.md`
3. `creative/opc-creative-production-sop.md`
4. `creative/opc-creative-chief-controller-checklist.md`
5. `creative/opc-creative-auto-handoff-map.md`
6. `creative/opc-creative-verification-gate.md`
7. `creative/opc-creative-failure-patterns.md`
8. `creative/opc-background-monitoring-guardrails.md`
9. `creative/opc-delivery-auth-failure-handling.md`
10. `creative/opc-creative-run-template.md`
11. `creative/opc-creative-closeout-language-rules.md`
12. `creative/opc-creative-acceptance-pass.md`
13. `meta/opc-creative-convergence-decision.md`
14. `meta/opc-creative-normalization-todo.md`

## Notes

- This snapshot keeps the latest reference-layer wording, with light packaging for git submission.
- It does not attempt to export unrelated workspace memory or startup files.
- One cleanup was applied during export: the normalization todo was normalized so it matches its own stated state (`当前无剩余项`).

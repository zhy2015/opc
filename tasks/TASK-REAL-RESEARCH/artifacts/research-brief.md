# OPC Research Brief

## Topic
How OPC should define review gates and resume/recovery constraints in OpenClaw-native multi-agent workflows.

## Primary references
- docs/opc-v1-spec.md
- docs/openclaw-orchestration.md
- docs/opc-control-plane-audit.md
- docs/mvp-usage.md

## Key findings
1. Review gates should default to high-risk transitions only: code changes, external sends, public publishing, long-term memory/doc changes, and sensitive credential/login-state operations.
2. Resume must be artifact-first, not transcript-first. Stable outputs, completed nodes, and next executable nodes should be readable from task state alone.
3. CEO session remains the final authority for dispatch, pause/resume, and delivery. Worker sessions should not mutate task scope.
4. File-led control plane is already sufficient for v1 if dispatch payloads, event logs, and session bindings stay consistent.

## Proposed operating rules
- Plan Gate: required for Type C/D tasks before broad dispatch.
- Result Gate: required before delivery for risky or externally visible outputs.
- Resume rule: completed nodes are skipped by default; blocked/failed nodes must expose clear next action.
- Rework rule: reviewer feedback should create explicit required_changes and keep prior stable artifacts reusable.

## Recommended next step
Use this brief as the source for the synthesis node and then route the final brief through reviewer approval.

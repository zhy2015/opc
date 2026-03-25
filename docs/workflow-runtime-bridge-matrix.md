# Workflow Runtime Bridge Matrix

## Goal

Give one compact comparison view of how research / coding / social workflows map from OPC ledger into real OpenClaw runtime sessions.

| Workflow | Primary execute node | Runtime focus | Key result type | Key review gate | Why bind-session matters |
|---|---|---|---|---|---|
| Research | `NODE-RESEARCH-001` | source collection and synthesis handoff | markdown research artifacts | findings are good enough to synthesize | ties findings to one accountable session |
| Coding | `NODE-CODE-001` | scoped code implementation | code files + review artifact | code must pass reviewer gate before delivery | ties file changes to one accountable session |
| Social | `NODE-OPERATE-001` | real platform-side action + verification | platform workflow assets + verification record | external action must prove real platform result | ties external write action to one accountable session |

---

## Shared bridge pattern

All three workflows now share the same minimum pattern:

1. create task / node ledger
2. render dispatch payload
3. bind node to real session
4. dispatch payload into session
5. record result back into ledger
6. resolve review gate
7. recover final artifacts through resume cursor

---

## Key difference by workflow

### Research
- safest output surface
- strongest emphasis on source quality and synthesis readiness

### Coding
- strongest emphasis on implementation scope and file-level auditability
- review gate protects shipped change quality

### Social
- strongest emphasis on post-action verification
- highest need to distinguish real success from pseudo-success
- strongest need for session accountability when external side effects exist

---

## Suggested reading map

- `docs/task-real-research-bind-session-example.md`
- `docs/task-real-coding-bind-session-example.md`
- `docs/task-real-social-bind-session-example.md`
- `docs/runtime-bridge-checklist.md`

# TASK-REAL-SOCIAL Bind-Session Example

## Goal

Show the minimum bridge from OPC file ledger to a real OpenClaw execution session for the social workflow.

---

## 1. Render dispatch artifact

```bash
python3 scripts/opc.py render-dispatch-payload TASK-REAL-SOCIAL NODE-OPERATE-001
```

Expected artifact:

```text
tasks/TASK-REAL-SOCIAL/artifacts/NODE-OPERATE-001-dispatch.json
```

---

## 2. Bind node to a real session

```bash
python3 scripts/opc.py bind-session TASK-REAL-SOCIAL NODE-OPERATE-001 sess_social_worker_001 --runtime subagent --session-mode session
```

Expected node mutation:

```json
{
  "assigned_session": "sess_social_worker_001",
  "spawned_by": "ceo-session",
  "runtime": "subagent",
  "session_mode": "session"
}
```

---

## 3. CEO runtime actions

After binding, CEO should:

1. create or reuse the target worker session via `sessions_spawn`
2. send the dispatch artifact into that session via `sessions_send`
3. wait for the operator-social session to finish the platform action and post-action verification
4. record stable results back into OPC via `record-result`
5. move the node into `review_pending`
6. let reviewer session approve or reject the result gate

---

## 4. Why this matters

This bridge gives social workflow three things it previously lacked:

- exact session accountability for external write actions
- stable linkage between node ledger and execution session
- auditable proof that platform-side work went through result gate instead of living only in chat history

---

## 5. Suggested next step

Promote the same bind-session pattern to:
- `TASK-REAL-RESEARCH`
- `TASK-REAL-CODING`
- then compare the three workflows under one runtime-bridge checklist

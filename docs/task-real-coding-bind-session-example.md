# TASK-REAL-CODING Bind-Session Example

## Goal

Show the minimum bridge from OPC file ledger to a real OpenClaw execution session for the coding workflow.

---

## 1. Render dispatch artifact

```bash
python3 scripts/opc.py render-dispatch-payload TASK-REAL-CODING NODE-CODE-001
```

Expected artifact:

```text
tasks/TASK-REAL-CODING/artifacts/NODE-CODE-001-dispatch.json
```

---

## 2. Bind node to a real session

```bash
python3 scripts/opc.py bind-session TASK-REAL-CODING NODE-CODE-001 sess_code_worker_001 --runtime subagent --session-mode session
```

Expected node mutation:

```json
{
  "assigned_session": "sess_code_worker_001",
  "spawned_by": "ceo-session",
  "runtime": "subagent",
  "session_mode": "session"
}
```

---

## 3. CEO runtime actions

After binding, CEO should:

1. create or reuse the target coding worker session via `sessions_spawn`
2. send the dispatch artifact into that session via `sessions_send`
3. wait for the worker-code session to finish the scoped implementation
4. record stable results via `record-result`
5. move the node into `review_pending`
6. let reviewer session approve or reject the code result gate

---

## 4. Why this matters

This bridge gives coding workflow:

- exact session accountability for code changes
- stable linkage between implementation node and modified files
- auditable proof that code changes passed reviewer gate before delivery

---

## 5. Suggested next step

Apply the same bridge to reviewer and delivery nodes so the full coding chain becomes session-addressable.

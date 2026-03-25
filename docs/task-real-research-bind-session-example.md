# TASK-REAL-RESEARCH Bind-Session Example

## Goal

Show the minimum bridge from OPC file ledger to a real OpenClaw execution session for the research workflow.

---

## 1. Render dispatch artifact

```bash
python3 scripts/opc.py render-dispatch-payload TASK-REAL-RESEARCH NODE-RESEARCH-001
```

Expected artifact:

```text
tasks/TASK-REAL-RESEARCH/artifacts/NODE-RESEARCH-001-dispatch.json
```

---

## 2. Bind node to a real session

```bash
python3 scripts/opc.py bind-session TASK-REAL-RESEARCH NODE-RESEARCH-001 sess_research_worker_001 --runtime subagent --session-mode session
```

Expected node mutation:

```json
{
  "assigned_session": "sess_research_worker_001",
  "spawned_by": "ceo-session",
  "runtime": "subagent",
  "session_mode": "session"
}
```

---

## 3. CEO runtime actions

After binding, CEO should:

1. create or reuse the target research worker session via `sessions_spawn`
2. send the dispatch artifact into that session via `sessions_send`
3. wait for the worker to collect and structure source findings
4. record stable results via `record-result`
5. move the node into `review_pending`
6. let reviewer session pass or reject the result gate

---

## 4. Why this matters

This bridge gives research workflow:

- exact session accountability for source collection and synthesis handoff
- stable linkage between research node and produced artifact refs
- auditable proof that findings passed review instead of remaining in transient chat history

---

## 5. Suggested next step

Apply the same bridge to writer and reviewer nodes so the whole research chain becomes session-addressable.

# Runtime-Bridge Validation Sheet

## Goal

Compare the three bind-session real-run demos under one compact validation view.

| Lane | Demo task | Bound node | Session key | Reached running | Result written back | Review requested | Verdict |
|---|---|---|---|---|---|---|---|
| Research | `TASK-BIND-SESSION-DEMO-RESEARCH` | `NODE-RESEARCH-001` | `sess_demo_research_001` | yes | yes | yes | pass |
| Coding | `TASK-BIND-SESSION-DEMO-CODING` | `NODE-CODE-001` | `sess_demo_code_001` | yes | yes | yes | pass |
| Social | `TASK-BIND-SESSION-DEMO-SOCIAL` | `NODE-OPERATE-001` | `sess_demo_social_001` | yes | yes | yes | pass |

---

## Shared validated control-plane sequence

1. create task / node
2. render dispatch payload
3. bind node to session
4. move node to running
5. record result with refs
6. request result gate
7. confirm task-report reflects bound session state

---

## Conclusion

All three real OPC lanes now have at least one real bind-session closure demo.
The next gap is no longer “can this bridge work”, but “how much of this writeback and review progression should be automated”.

# OPC Review Gate & Recovery Brief

## Decision baseline
For OPC v1, review gates and resume/recovery should be treated as hard operating rules, not optional prompt habits.

## Review gate rules
### Plan Gate
Trigger by default for:
- Type C multi-node tasks
- Type D persistent-session tasks
- Any task with risky routing ambiguity

Goal:
- validate node breakdown
- validate role boundaries
- validate acceptance criteria and dependencies

### Result Gate
Trigger by default for:
- code changes
- external sends
- public publishing
- long-term memory/document mutations
- sensitive credential or login-state operations

Goal:
- verify acceptance criteria
- decide approve / reject / conditional_approve
- convert reviewer feedback into explicit rework requirements

## Resume / recovery rules
1. Resume from task state, not chat transcript.
2. Completed nodes are skipped by default.
3. Stable artifacts remain reusable unless explicitly invalidated.
4. The next executable nodes must be derivable from dependency state.
5. CEO session can always manually take over blocked or failed nodes.

## Control-plane implication
To support these rules, OPC v1 should keep:
- task / node status machines
- event ledger
- dispatch payload artifacts
- result recording
- session binding
- resume_cursor with completed_nodes / next_nodes / stable_artifacts

## Conclusion
The current OPC control plane is already strong enough to support a first real workflow. The next milestone is not redesign, but repeatedly proving the model across research, coding, and social workflows.

# OPC Stall / Timeout / Fallback Policy

This file defines the default handling of stalled delegated work in OPC.

## Core rule

The main session should not wait forever just because a sub-agent was dispatched.
Stalled work requires explicit policy.

## Default progression

### 1. Detect stall
Treat a sub-agent as stalled when there has been no meaningful progress signal within the expected window for that task class.

### 2. First response: `steer`
If the agent still seems viable, clarify scope, ask for current blocker, or request an intermediate summary.

### 3. Second response: `reassign` or `summarize`
If steering does not restore useful progress, either:
- reassign the scope to another worker
- or force a summarize step and let the main session decide the next move

### 4. Last response: `kill` or main-session takeover
If the run is clearly no longer worth waiting on, stop it and either:
- reassign cleanly
- or pull the task back into the main session

## Default stall reflex

When a run goes quiet, check three things fast:
- **what would count as meaningful progress here?**
- **how long without that signal is too long?**
- **what is the next intervention once that threshold is crossed?**

If those three answers are not explicit, the stall policy is still too vague.

## Practical threshold rule

No single hard timeout fits all tasks.
The main session should set an expectation proportional to task scope.
But it should always keep an explicit answer to:
- what counts as meaningful progress here?
- how long without signal is too long?
- what is the next intervention if that threshold is crossed?

## Anti-patterns

- infinite waiting because "the agent might still be working"
- treating any heartbeat as meaningful progress when no useful output is appearing
- reassigning too early before clarifying the blocker
- refusing main-session takeover even when delegation has clearly failed

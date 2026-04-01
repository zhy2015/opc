# OPC / MMM Boundary

This file defines how OPC and MMM should cooperate without stepping on each other.

## Core rule

OPC governs **controlled parallel execution**.
MMM governs **memory quietness, retention, and convergence judgment**.
They are complementary, not interchangeable.

## OPC owns

- whether a task should enter controlled parallel execution
- sub-task decomposition and dispatch
- live monitoring and intervention
- integration of sub-agent outputs

## MMM owns

- whether prior memory should be loaded
- whether retention is warranted after the run
- whether an outcome belongs in core, references, or daily memory
- whether orchestration residue should be discarded

## Practical coordination

### Before dispatch
OPC asks:
- is parallel execution worth it?
- are the boundaries clear enough?

MMM asks:
- does this task need memory at all?
- if yes, which smallest layer should be read?

### After dispatch / during execution
OPC monitors progress and blockers.
MMM should not be expanded into a live orchestration controller.

### After completion
OPC integrates the result.
MMM judges retention:
- durable lesson?
- `run_snapshot` continuity value?
- discard?

## Anti-patterns

- using MMM to justify unnecessary sub-agent fan-out
- using OPC outputs as automatic reasons to write memory
- promoting orchestration residue into core memory
- letting parallel execution bypass quiet-system read/write discipline

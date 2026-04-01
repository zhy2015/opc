# OPC Background Monitoring Guardrails

Use this file when a creative-production run relies on cron jobs, background exec, delayed polling, or any other background continuation path.

## Core rule

A background monitor is not progress.
A scheduled retry is not progress.
A still-existing job is not progress.

Background continuation only has value if it is attached to a live, checkable production path.

## What monitors must check

When monitoring a production run, prefer checks that answer real liveness questions:
- is the producer process alive?
- are artifacts actually appearing?
- are files non-empty and increasing as expected?
- is authentication still valid?
- is the pipeline blocked on a recoverable state, or dead?
- is the claimed delivery path still valid?

## What monitors must not imply

Do not let a monitor imply:
- that rendering is still happening just because a cron exists
- that delivery is still possible just because a plan exists
- that a run is healthy just because there was no new error message
- that silence equals progress

## Dead-pipeline detection

Background monitoring should detect and surface these conditions clearly:
- auth failure / invalid user / credential rejection
- producer process missing
- all candidate artifacts zero-byte or placeholder-like
- repeated retries with no state change
- monitor instructions referencing stale or wrong paths
- completion flag never appearing while no work is actually running

## Default response to dead-pipeline detection

When a dead pipeline is detected:
1. downgrade any optimistic progress assumption
2. stop implying the background path is still working
3. surface the real blocker briefly and concretely
4. decide whether to retry, repair, re-route, or stop the monitor
5. do not keep zombie monitoring jobs running without purpose

## Repeated monitor failure

If a monitor repeatedly reports the same auth error, dead state, or impossible path:
- treat this as a configuration or pipeline failure, not as a waiting problem
- avoid endless re-announcement loops
- prefer repair or cancellation over ritualized checking

## Creative-production special note

In creative-production tasks, background paths are common, but they are dangerous because they create the illusion of unstoppable progress.
The chief controller should remain skeptical until artifact state changes are verified.

This file owns the background-monitoring slice of the creative operating protocol. For SSOT ownership, see `references/opc-creative-ssot-map.md`.

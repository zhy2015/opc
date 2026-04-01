# OPC Lightweight Board

This file defines the minimum board/timeline view for OPC without requiring a heavy dashboard system.

## Purpose

The main session needs a lightweight control surface for active OPC runs.
A text-first board is enough if it keeps the right fields visible.

## Minimum board columns

For each sub-agent, show:
- agent
- scope
- state
- last update
- blocker
- expected output
- next intervention (if any)

For creative-production runs, also keep these lightweight fields visible when relevant:
- lane type
- delivery ownership
- auto-handoff target
- artifact level reached (plan / asset / draft / preview / delivered)

## Minimum timeline events

Track major milestones only:
- planned
- reviewed
- dispatched
- doing
- blocked
- review
- done / cancelled

## Default board reflex

The board only needs to answer four control questions fast:
- **who is doing what**
- **what state it is in**
- **what is blocked or drifting**
- **where the next intervention belongs**

If the board cannot answer those quickly, it is too vague or too noisy.

For creative-production runs, the board should also make it hard to confuse:
- active production vs background watching
- verified artifacts vs claimed artifacts
- valid delivery paths vs broken-but-still-listed paths

## Usage rule

A lightweight board is for clarity, not ceremony.
Do not turn it into a verbose log dump.
Keep it concise enough that the main session can glance once and know where to act.

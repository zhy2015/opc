# OPC / Config / Environment Boundary

This file defines how OPC should interact with the config and environment layers.

## Core rule

Sub-agents should not each rediscover runtime parameters or local environment facts independently when the main session can provide the correct owner-layer context.

## Config coordination

If delegated work depends on runtime parameters, provider settings, channel behavior, or path conventions:
- check config-zone first
- identify the owner file
- pass the relevant context to the sub-agent rather than letting each worker guess

## Environment coordination

If delegated work depends on local operational reality such as:
- browser / gateway behavior
- shell / permission reality
- proxy fallback facts
- local capability pointers

then:
- check `references/local-environment-facts.md` first
- pass the relevant facts down as scoped working context

## Main-session responsibility

The main session should normalize config/environment truth before delegation when those truths materially affect execution.
This reduces duplicated discovery and inconsistent assumptions across workers.

## Anti-patterns

- letting every sub-agent rediscover the same config fact
- letting logs/state substitute for config truth
- letting memory core absorb config/environment detail just because multiple workers touched it

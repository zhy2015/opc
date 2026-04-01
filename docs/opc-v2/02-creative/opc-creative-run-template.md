# OPC Creative Run Template

Use this as a lightweight planning/control template when an OPC run is clearly a creative production workflow.
The goal is not ceremony.
The goal is to make sure the run starts with enough structure to avoid the common production failures.

## 1. Target result

- user-visible result object:
- earliest acceptable review layer (if not final delivery):
- true completion target by default:

## 2. Lanes

List only lanes that have real work.
Default bias: script/shot, visual generation, render/draft, audio, delivery.

| lane | owner | scope | expected artifact | first trigger to launch | next auto-handoff |
|---|---|---|---|---|---|
| script/shot |  |  |  |  |  |
| visual generation |  |  |  |  |  |
| render/draft |  |  |  |  |  |
| audio |  |  |  |  |  |
| delivery |  |  |  |  |  |

## 3. Parallel vs serial split

### parallelizable units
- 
- 
- 

### serial bridge units
- 
- 

## 4. Delivery planning

- primary delivery path:
- fallback path 1:
- fallback path 2:
- small-file validation done? yes/no
- who owns delivery validation:

## 5. Project truth sync

When these change, update project truth immediately:
- manifest:
- shot inventory:
- concat/output list:
- delivery record:

## 6. Completion ladder tracking

- current level:
- what is missing for next level:
- what is missing for L5 direct access:
- highest verified level:
- highest merely claimed level:

## 7. Main-session control checks

Before going quiet, ask:
- is there any lane that should already be active but is not?
- did a returned result trigger its next action?
- am I about to narrate progress instead of shipping an artifact?
- do I actually know the delivery path?
- if I say “done” now, can the user directly access the requested object?
- am I accidentally treating a claimed state as a verified state?

This template owns the lightweight planning/control-template slice of the broader creative operating protocol.
For SSOT ownership across the creative-production guidance set, see `references/opc-creative-ssot-map.md`.

# OPC Creative Verification Gate

Use this gate before announcing success in creative-production tasks.
It exists to stop the most expensive lie in production workflows: claiming delivery from unverified artifacts.

## Core rule

In creative production, a worker saying “done” is not proof.
A file path mentioned in text is not proof.
A send attempt is not proof.
A cron job existing is not proof.

Only verified artifact state and verified delivery state count.

## Minimum verification checks

Before user-facing success language, verify as many of these as apply:

1. artifact exists at the claimed path
2. artifact is non-empty and plausibly valid for its type
3. artifact is not a placeholder, mock, or test stand-in
4. the artifact corresponds to the claimed stage (asset / draft / preview / final)
5. the delivery path actually succeeded or remains directly accessible
6. any fallback path being claimed was also truly exercised, not just planned

## Delivery-first verification lens

Verification should not stop at "did workers produce outputs?"
It should answer the harder task-level question: "is there now a user-consumable result object with evidence strong enough to justify the claimed completion layer?"

Before completion language, verify:
- a task-level deliverable exists
- the deliverable is the right kind of object for the user's ask
- delivery evidence supports the claimed state
- the result is user-consumable now, or is honestly labeled as fallback/internal/partial
- wording does not upgrade `partial`, `fallback_delivered`, or `internal_only` into true delivered state

## Delivery-specific hard checks

### File delivery
- file exists
- file size is non-zero
- file naming and location match the claimed output

### Link delivery
- link exists in the real destination object
- user can plausibly open it from the delivered location

### Message / send delivery
- send path succeeded in the real channel or account being used
- there is no known auth failure, invalid user state, or attachment incompatibility invalidating the claim
- any background monitor or retry path tied to delivery is still attached to a live, valid path rather than a dead or rejected one

## Downgrade rules

If verification fails:
- do not use completion language
- downgrade the run to the highest honestly verified layer
- surface the real blocker
- continue from the blocker if an internal next step exists

## Examples of forbidden shortcuts

Do not announce completion based only on:
- child result text
- “mocked” outputs
- empty mp4 files
- inferred email delivery
- a script that should have sent something
- a cron monitor that merely exists

## Relationship to other references

This file is a hard gate for creative-production closeout.
It owns the verification-gate slice of the broader creative operating protocol.
Use it together with:
- `references/opc-creative-operating-protocol.md`
- `references/opc-creative-production-sop.md`
- `references/opc-result-closeout-contract.md`
- `references/result-delivery-closeout-checklist.md`
- `references/opc-creative-failure-patterns.md`
- `references/opc-creative-ssot-map.md`
---
title: CNT v2 BREAKOUT V1 ACTIVE ISOLATION DECISION
status: FINAL
language: en
updated: 2026-04-24
tags:
  - cnt
  - breakout_v1
  - active-set
  - isolation
---

# CNT v2 BREAKOUT V1 ACTIVE ISOLATION DECISION

## Summary

`breakout_v1` is removed from the runtime active set.

This is an operational isolation decision, not a strategy deletion.

## Why This Was Done

The latest verified runtime data showed:

- `breakout_v1 expectancy = -0.022198`
- `breakout_v1 profit_factor = 0.17295`
- `breakout_v1 trades_closed = 3`
- overall `LIVE_GATE = FAIL / NON_POSITIVE_EXPECTANCY`

At the same time:

- `pullback_v1` remained positive
- `breakout_v3` shadow observation had already been rebaselined
- shadow/output semantics and portfolio risk sync issues had already been addressed

That means the largest remaining operational problem was no longer observability or state sync.
It was the continued presence of `breakout_v1` in `ACTIVE_STRATEGIES`.

## Decision

The runtime configuration is changed as follows:

- `ACTIVE_STRATEGY = pullback_v1`
- `ACTIVE_STRATEGIES = [pullback_v1]`

`breakout_v1` remains:

- implemented in source
- registered in the strategy registry
- preserved in historical metrics and documents

But it is no longer part of the current live candidate set.

## Scope

This change does **not**:

- activate `breakout_v3`
- modify order policy
- modify risk guard rules
- delete `breakout_v1`
- rewrite ranker logic

This change only isolates the negative strategy from the active runtime set.

## Validation

Required checks after the isolation patch:

1. test suite passes
2. `py_compile` passes
3. one-shot runtime via `run.ps1` completes
4. runtime action remains valid
5. no execution-path regression appears

## Operational Interpretation

This decision should be interpreted as:

- `pullback_v1` = current live strategy
- `breakout_v1` = inactive archived reference
- `breakout_v3` = shadow-only observation strategy

## Conclusion

The active-set isolation of `breakout_v1` is the smallest valid operational change that directly addresses the remaining live performance contamination source.

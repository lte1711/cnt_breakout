---
title: CNT v2 BREAKOUT V1 ACTIVE ISOLATION IMPLEMENTATION REPORT
status: FINAL
language: en
updated: 2026-04-24
---

# CNT v2 BREAKOUT V1 ACTIVE ISOLATION IMPLEMENTATION REPORT

## Change Summary

The runtime active set was reduced from:

- `breakout_v1`
- `pullback_v1`

to:

- `pullback_v1` only

The config change was:

- `ACTIVE_STRATEGY = "pullback_v1"`
- `ACTIVE_STRATEGIES = ["pullback_v1"]`

## Why This Patch Was Applied

At the time of the patch:

- `breakout_v1` had strongly negative observed expectancy
- `pullback_v1` remained positive
- `breakout_v3` shadow semantics had already been cleaned and rebaselined
- `portfolio_state` risk metric sync had already been fixed

That left `breakout_v1` active runtime participation as the largest remaining live contamination source.

## Files Changed

- `config.py`
- `docs/CNT v2 BREAKOUT V1 ACTIVE ISOLATION DECISION.md`
- `docs/ko/CNT v2 BREAKOUT V1 ACTIVE ISOLATION DECISION KO.md`
- `docs/CNT v2 BREAKOUT V1 ACTIVE ISOLATION IMPLEMENTATION REPORT.md`
- `docs/ko/CNT v2 BREAKOUT V1 ACTIVE ISOLATION IMPLEMENTATION REPORT KO.md`

## Validation

### Tests

- `PYTHONPATH=. python -m pytest -q`
- result: `56 passed`

### Compile

- `python -m py_compile config.py src\engine.py src\strategy_manager.py tests\test_signal_ranker.py tests\test_engine_cycle_smoke.py`
- result: `OK`

### Runtime

Entry chain validation was executed via:

- `run.ps1`

Observed result:

- `data/state.json.strategy_name = pullback_v1`
- `data/state.json.action = NO_ENTRY_SIGNAL`
- `data/portfolio_state.json.daily_loss_count = 3`
- `data/portfolio_state.json.consecutive_losses = 3`

Runtime log evidence:

- previous entries still show historical `breakout_v1`
- latest isolated run shows:
  - `strategy_name = pullback_v1`
  - `reason = no_ranked_signal`

Signal log evidence:

- latest one-shot appended only `pullback_v1`
- historical `breakout_v1` lines remain as past evidence

## What Did Not Change

This patch did not:

- delete `breakout_v1`
- remove `breakout_v1` from the registry
- activate `breakout_v3`
- modify risk guard thresholds
- modify exchange/order flow

## Operational Interpretation

After this patch:

- `pullback_v1` is the only live active strategy
- `breakout_v1` remains a preserved historical strategy, but not a current runtime candidate
- `breakout_v3` remains shadow-only

## Conclusion

The active-set isolation patch was applied successfully without breaking tests, compile checks, or the entry-chain runtime flow.

## Obsidian Links

- [[CNT v2 BREAKOUT QUALITY EVALUATION REPORT]]


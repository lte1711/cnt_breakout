---
tags:
  - cnt
  - breakout
  - shadow
  - review
aliases:
  - CNT v2 BREAKOUT V2 EXPANDED SHADOW OBSERVATION REVIEW
---

# CNT v2 BREAKOUT V2 EXPANDED SHADOW OBSERVATION REVIEW

## Review Status

- status = `FINALIZED`
- lock_state = `LOCKED`
- breakout_v2 classification = `FAILED_DESIGN_IN_CURRENT_FORM`

## Summary

- current label = `LIVE_READY_WITH_SINGLE_STRATEGY_DEPENDENCE`
- breakout_v2 status = `FAILED_DESIGN_IN_CURRENT_FORM`
- activation decision = `DO NOT ACTIVATE`
- tuning decision = `STILL PROHIBITED`

This review uses the latest expanded shadow schema events, where each event includes:

- `secondary_fail_reasons`
- `evaluated_stage_trace`
- `stage_flags`

That means this review is no longer limited to first-blocker inspection only. It separates:

1. first blocker view
2. downstream blocker view

## Baseline

### Mixed Portfolio

- snapshot timestamp = `2026-04-24 01:14:02`
- live gate = `LIVE_READY / ALL_GATES_PASSED`
- closed trades = `33`
- expectancy = `0.0005057575757575136`
- net pnl = `0.016689999999997984`
- profit factor = `1.0584152628686754`

### Strategy Context

- `pullback_v1` remains the only positive driver
  - trades_closed = `30`
  - win_rate = `56.67%`
  - expectancy = `0.002776133333333231`
  - profit_factor = `1.405881292246791`
- `breakout_v1` remains negative reference
  - trades_closed = `3`
  - expectancy = `-0.022197999999999656`
  - profit_factor = `0.17295081967214201`

### breakout_v2 Shadow Baseline

- total shadow signals = `180`
- filtered_signal_count = `180`
- allowed_signal_count = `0`
- allowed_signal_ratio = `0.0`
- hypothetical_trades_count = `0`
- expanded schema events = `127`

## First-Blocker View

Expanded-schema first blocker distribution:

- `market_not_trend_up = 53`
- `range_without_upward_bias = 30`
- `volatility_not_high = 21`
- `range_bias_up_but_entry_trend_not_up = 15`
- `breakout_not_confirmed = 3`
- `rsi_overheat = 2`
- `band_width_too_narrow = 1`
- `rsi_below_entry_threshold = 1`
- `price_not_above_vwap = 1`

### Interpretation

- In the expanded sample, `market_not_trend_up` is now the dominant first blocker.
- `volatility_not_high` is still present, but it is no longer strong enough to be treated as the single leading explanation.
- This is a material shift from the earlier first-blocker-only review, where volatility looked more dominant.

## Downstream-Blocker View

Expanded-schema secondary fail distribution:

- `band_width_too_narrow = 109`
- `breakout_not_confirmed = 102`
- `volume_not_confirmed = 104`
- `band_not_expanding = 87`
- `rsi_below_entry_threshold = 82`
- `price_not_above_vwap = 65`
- `ema_fast_not_above_slow = 56`
- `volatility_not_high = 54`
- `range_without_upward_bias = 53`
- `vwap_distance_too_small = 45`

Expanded-schema stage false counts:

- `band_width_pass = false` -> `110`
- `vwap_distance_pass = false` -> `111`
- `breakout_confirmed = false` -> `105`
- `volume_pass = false` -> `104`
- `band_expansion_pass = false` -> `87`
- `rsi_threshold_pass = false` -> `85`
- `market_bias_pass = false` -> `83`
- `volatility_pass = false` -> `75`
- `ema_pass = false` -> `71`

### Interpretation

- The dominant downstream blockers are now `band width`, `VWAP distance`, `breakout confirmation`, and `volume`.
- `band expansion` and `RSI threshold` also fail at structurally high rates.
- `volatility_pass = false` still matters, but it is clearly not sufficient to describe the whole structure.

## Gate Dependency Interpretation

The expanded sample now supports a stronger conclusion than the earlier first-blocker reviews:

- breakout_v2 is **not** blocked by one simple threshold
- breakout_v2 is blocked by a **multi-stage chain**

Current blocking structure is best described as:

1. market bias often fails first
2. even when market bias passes, breakout confirmation often fails
3. even after that, VWAP distance, volume, and band width still remove many candidates

This means:

- single-gate relaxation is not justified
- volatility-only relaxation is not justified
- band-width-only relaxation is not justified

## Decision

### Fixed Decision

- `breakout_v2 activation = PROHIBITED`
- `threshold tuning = PROHIBITED`
- `single-gate relaxation = PROHIBITED`

### Current Strategy Reading

- `breakout_v2` has now accumulated enough shadow evidence to move beyond early observation status
- it still has `allowed_signal_count = 0` after a materially sufficient shadow sample
- therefore the correct status is:
  - `QUALITY = FAILED_DESIGN_IN_CURRENT_FORM`
  - `USABILITY = NON_VIABLE_CANDIDATE_GENERATION`

## Final Verdict

The expanded shadow sample shows that `breakout_v2` is blocked by a multi-stage filter chain, not by one dominant threshold alone.

The most accurate current conclusion is:

> `breakout_v2` is a failed design in its current form, and the observed failure structure is jointly driven by market bias, breakout confirmation, VWAP distance, band width, band expansion, and volume checks.

## Next Step

The next safe step is **not** activation or tuning.

The next safe step is:

1. keep `breakout_v2` in shadow-only mode
2. preserve current gate and runtime policy
3. treat `breakout_v2` as an inactive experimental strategy
4. move to redesign-preparation, not tuning

That means:

- no activation
- no threshold relaxation
- no single-gate experiment
- redesign options must be documented before any future implementation

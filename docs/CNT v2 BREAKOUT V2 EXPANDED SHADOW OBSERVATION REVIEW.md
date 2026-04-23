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

## Summary

- current label = `STRUCTURALLY_HEALTHY, PERFORMANCE_DEGRADED`
- breakout_v2 status = `SHADOW_ONLY`
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

- snapshot timestamp = `2026-04-23 13:44:04`
- live gate = `FAIL / NON_POSITIVE_EXPECTANCY`
- closed trades = `31`
- expectancy = `-0.000059161290322620394`
- net pnl = `-0.0018340000000012235`
- profit factor = `0.9932960240378069`

### Strategy Context

- `pullback_v1` remains the only positive driver
  - trades_closed = `28`
  - win_rate = `57.14%`
  - expectancy = `0.002312857142857062`
  - profit_factor = `1.335458873135821`
- `breakout_v1` remains negative reference
  - trades_closed = `3`
  - expectancy = `-0.022197999999999656`
  - profit_factor = `0.17295081967214201`

### breakout_v2 Shadow Baseline

- total shadow signals = `114`
- filtered_signal_count = `114`
- allowed_signal_count = `0`
- allowed_signal_ratio = `0.0`
- hypothetical_trades_count = `0`
- expanded schema events = `61`

## First-Blocker View

Expanded-schema first blocker distribution:

- `market_not_trend_up = 34`
- `range_without_upward_bias = 16`
- `volatility_not_high = 5`
- `range_bias_up_but_entry_trend_not_up = 4`
- `breakout_not_confirmed = 1`
- `rsi_overheat = 1`

### Interpretation

- In the expanded sample, `market_not_trend_up` is now the dominant first blocker.
- `volatility_not_high` is still present, but it is no longer strong enough to be treated as the single leading explanation.
- This is a material shift from the earlier first-blocker-only review, where volatility looked more dominant.

## Downstream-Blocker View

Expanded-schema secondary fail distribution:

- `breakout_not_confirmed = 52`
- `volume_not_confirmed = 50`
- `band_width_too_narrow = 49`
- `rsi_below_entry_threshold = 43`
- `band_not_expanding = 43`
- `ema_fast_not_above_slow = 34`
- `range_without_upward_bias = 34`
- `price_not_above_vwap = 31`
- `volatility_not_high = 30`
- `vwap_distance_too_small = 21`

Expanded-schema stage false counts:

- `breakout_confirmed = false` -> `53`
- `vwap_distance_pass = false` -> `52`
- `market_bias_pass = false` -> `50`
- `volume_pass = false` -> `50`
- `band_width_pass = false` -> `49`
- `rsi_threshold_pass = false` -> `44`
- `band_expansion_pass = false` -> `43`
- `ema_pass = false` -> `38`
- `volatility_pass = false` -> `35`

### Interpretation

- The dominant downstream blocker is now `breakout confirmation`.
- `VWAP distance`, `volume`, and `band width` also fail at very high rates.
- `band expansion` is still a meaningful blocker, but it is part of a broader failure chain rather than an isolated root cause.
- `volatility_pass = false` still matters, but it is no longer sufficient to describe the whole structure.

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

- `breakout_v2` is not yet a proven bad strategy in execution terms, because it has generated no allowed candidates
- but it **is** currently an over-filtered strategy in usability terms
- therefore the correct status is:
  - `QUALITY = UNPROVEN`
  - `USABILITY = TOO RESTRICTIVE`

## Final Verdict

The expanded shadow sample shows that `breakout_v2` is blocked by a multi-stage filter chain, not by one dominant threshold alone.

The most accurate current conclusion is:

> `breakout_v2` remains over-filtered, and the observed failure structure is jointly driven by market bias, breakout confirmation, VWAP distance, band width, band expansion, and volume checks.

## Next Step

The next safe step is **not** activation or tuning.

The next safe step is:

1. keep `breakout_v2` in shadow-only mode
2. preserve current gate and runtime policy
3. review whether shadow snapshot/report aggregation should expose expanded fields directly, such as:
   - expanded_event_count
   - secondary_fail_distribution
   - stage_false_counts

That is a reporting/observability improvement, not a strategy tuning step.

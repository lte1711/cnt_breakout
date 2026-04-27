---
title: CNT v2 BREAKOUT V3 FIRST SHADOW OBSERVATION REVIEW
status: FINAL
language: en
updated: 2026-04-24
---

# CNT v2 BREAKOUT V3 FIRST SHADOW OBSERVATION REVIEW

## Review Metadata

- strategy = `breakout_v3`
- phase = `shadow_observation`
- window_start = `2026-04-24T02:04:04+09:00`
- baseline_commit = `8b6e772`
- review_time = `2026-04-24T12:54:04+09:00`
- status = `completed`

## Summary

- `signal_count = 41`
- `allowed_signal_count = 2`
- `allowed_signal_ratio = 0.04878048780487805`
- `expanded_event_count = 41`

## Final Judgement

`STRUCTURE_IMPROVING`

## Why This Is The Correct First Judgement

This is not a `STILL_OVER_FILTERED` result.

The current shadow window already shows:

- `allowed_signal_count > 0`
- repeated `soft_pass_count >= 3`
- multiple stage transitions beyond simple regime failure

At the same time, this is **not** activation-ready:

- `allowed_signal_ratio` is still below the preferred `5%` threshold
- `setup_not_ready` remains the dominant blocker
- the total allowed count is still too small to treat as stable evidence

So the correct interpretation is:

- the structure is no longer dead-on-arrival
- but the observation window still needs more evidence

## First Blocker Distribution

- `setup_not_ready = 19`
- `market_not_trend_up = 17`
- `breakout_not_confirmed = 3`

Interpretation:

- there is no single catastrophic blocker above 50%
- the dominant blocker is currently `setup_not_ready`
- regime failure is still meaningful, but not exclusively dominant

## Hard And Soft Structure

### Hard blocker interpretation

The current hard blocker distribution matches the first blocker distribution:

- `setup_not_ready = 19`
- `market_not_trend_up = 17`
- `breakout_not_confirmed = 3`

### Soft pass distribution

- `0 = 6`
- `1 = 13`
- `2 = 10`
- `3 = 6`
- `4 = 6`

Interpretation:

- the distribution is not collapsed at `0 to 1`
- `soft_pass_count >= 3` occurs in `12` cases
- quality-stage viability exists, even though not enough cases survive all earlier stages

## Stage Analysis

### Stage pass counts

- `regime = 24`
- `setup = 4`
- `trigger = 11`
- `quality = 12`

### Stage fail counts

- `regime = 17`
- `setup = 37`
- `trigger = 30`
- `quality = 29`

Interpretation:

- regime is no longer the only meaningful gate
- setup is the largest current bottleneck
- trigger and quality still reject many cases, but they are not structurally impossible

## Secondary Blockers

- `vwap_distance_fail = 34`
- `band_width_fail = 33`
- `volume_fail = 32`
- `band_expansion_fail = 30`
- `rsi_threshold_fail = 22`
- `ema_fail = 20`

Interpretation:

- secondary failures are still broad
- no single soft condition should be relaxed in isolation at this stage
- the current evidence supports continued observation, not tuning

## V2 Versus V3 Interpretation

Compared with `breakout_v2`, the current `breakout_v3` window is structurally better in three ways:

1. allowed signals now exist
2. downstream stage evaluation is active
3. `soft_pass_count >= 3` occurs repeatedly

So even though the official answer is not yet candidate-ready, the current observation supports `v3 > v2` in structural viability.

## Decision

### Activation

`PROHIBITED`

### Tuning

`PROHIBITED`

### Next Step

`continue_observation`

## Operational Conclusion

The first valid observation review does **not** support activation.

However, it also does **not** support the conclusion that `breakout_v3` is still structurally dead.

The correct next step is:

- keep `pullback_v1` as the only active runtime strategy
- keep `breakout_v3` shadow-only
- continue the current observation window
- wait for a larger sample before any structural redesign or activation discussion

## Obsidian Links

- [[CNT v2 BREAKOUT V3 SHADOW OBSERVATION WINDOW START]]

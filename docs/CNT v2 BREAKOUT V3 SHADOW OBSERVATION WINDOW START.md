---
tags:
  - cnt
  - type/documentation
  - status/active
  - market-context
  - type/operation
  - strategy/breakout_v3
  - cnt-v2-breakout-v3-shadow-observation-window-start
---

# CNT v2 BREAKOUT V3 SHADOW OBSERVATION WINDOW START

## Status

- status = `ACTIVE`
- runtime_mode = `SHADOW_ONLY`
- activation = `PROHIBITED`
- tuning = `PROHIBITED`

## Start Point

- baseline_commit = `8b6e772`
- window_start_time = `2026-04-24T02:04:04+09:00`
- verification_source = CNT v2 BREAKOUT V3 SHADOW RUNTIME ONE-SHOT VERIFICATION

This observation window starts only after:

1. `breakout_v3` shadow evaluator skeleton implementation
2. runtime integration skeleton
3. one-shot runtime output verification

All three conditions are now satisfied.

## Baseline Snapshot

### Breakout v3 shadow baseline

- `signal_count = 1`
- `allowed_signal_count = 0`
- `allowed_signal_ratio = 0.0`
- `expanded_event_count = 1`
- `first_blocker_distribution.market_not_trend_up = 1`
- `soft_pass_count_distribution.2 = 1`
- `stage_fail_counts.regime = 1`
- `stage_fail_counts.setup = 1`
- `stage_fail_counts.trigger = 1`
- `stage_fail_counts.quality = 1`

### System baseline

- performance snapshot timestamp = `2026-04-24 02:04:04`
- live gate = `LIVE_READY / ALL_GATES_PASSED`
- mixed portfolio:
  - `closed_trades = 34`
  - `expectancy = 0.00013499999999991123`
  - `net_pnl = 0.004589999999996985`
  - `profit_factor = 1.0154123560757822`
- current runtime state:
  - `strategy_name = breakout_v1`
  - `action = NO_ENTRY_SIGNAL`
  - `pending_order = null`
  - `open_trade = null`
  - `daily_loss_count = 2`

## Observation Objectives

This window is intended to answer the following questions:

1. Does `breakout_v3` generate real shadow candidates at all?
2. Which stage dominates the first blocker distribution over time?
3. How often do hard gates pass while the soft pool still blocks?
4. Does the `soft_pass_count` distribution suggest a viable future candidate range?
5. Are downstream failures concentrated in a small subset or still broadly distributed?

## Required Tracking

The following fields must be tracked as the observation window progresses:

- `signal_count`
- `allowed_signal_count`
- `allowed_signal_ratio`
- `first_blocker_distribution`
- `hard_blocker_distribution`
- `secondary_blocker_distribution`
- `soft_pass_count_distribution`
- `stage_pass_counts`
- `stage_fail_counts`

## Observation Rules

- `breakout_v3` remains `shadow-only`
- `ACTIVE_STRATEGIES` remains unchanged
- no order routing is allowed
- no ranking participation is allowed
- no parameter tuning is allowed during the initial window
- no single-gate shortcut relaxation is allowed during the initial window

## Initial Interpretation Rule

Early data must be treated as directional only.

No structural judgment should be finalized until a meaningful shadow sample accumulates beyond the one-shot verification baseline.

## Next Review Trigger

The next formal review should occur after a meaningful new shadow sample is accumulated.

Recommended minimum:

- `20 to 30 additional breakout_v3 shadow events`

At that point the project should produce a dedicated observation review covering:

- blocker distributions
- hard-pass vs soft-fail behavior
- whether `breakout_v3` appears viable as a future candidate or remains structurally blocked

## Final Record

`breakout_v3` is now in a valid shadow observation phase.

It is connected to runtime, producing observation outputs, and remains completely separated from live execution behavior.

## Obsidian Links

- [[CNT v2 BREAKOUT V3 DESIGN DRAFT]]


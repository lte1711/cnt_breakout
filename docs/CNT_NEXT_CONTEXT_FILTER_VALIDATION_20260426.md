---
tags:
  - cnt
  - offline-validation
  - context-filter
  - post-logging
  - type/documentation
  - status/active
  - market-context
  - pre-runup
  - offline-experiment
  - type/validation
  - type/operation
  - risk
  - strategy/pullback_v1
  - status/completed
---

# CNT Next Context Filter Validation 20260426

## Verdict

```text
VALIDATION_TYPE = FORWARD_SIGNAL_QUALITY_CHECK
RUNTIME_CHANGE = NO
LIVE_CHANGE = NO
CONFIG_CHANGE = NO
NEW_CLOSED_TRADES = 0
POST_LOGGING_BLOCKED_SIGNALS_REVIEWED = 11
SOURCE = logs/portfolio.log + market_features + Binance Spot Testnet klines
```

## Scope

FACT:
- `pullback_v1` closed trades remain 39.
- Total closed trades remain 42.
- No new post-logging closed trade exists yet.
- Daily risk remains blocked by `DAILY_LOSS_LIMIT`.
- This validation checks new signal quality only, not realized strategy performance.

UNKNOWN:
- These blocked signals were not executed, so their actual fills, stops, targets, and slippage are unknown.
- Latest forward 30m/60m data is incomplete for the newest records.

## Current Runtime State

```text
LAST_RUN_TIME = 2026-04-26 20:44:00
LAST_ACTION = EXECUTION_BLOCKED_BY_RISK
DAILY_LOSS_COUNT = 3
PENDING_ORDER = NONE
OPEN_TRADE = NONE
SCHEDULER_GAP = FALSE
```

## Candidate Filter Replay On New Signals

The offline experiment candidate filters were applied to new post-logging blocked signals with `decision_id` and `market_features`.

```text
POST_LOGGING_SIGNAL_COUNT = 11
CORE_RISK_SET_BLOCKED = 9
CORE_PLUS_VOLUME_BLOCKED = 11
```

Definitions:

```text
CORE_RISK_SET =
  PRE_RUNUP_30M
  or ENTRY_UP_CONTEXT
  or DEAD_RANGE_CANDLE

CORE_PLUS_VOLUME =
  CORE_RISK_SET
  or VOLUME_CONTRACTION
```

## Breakdown By Signal

| Signal | Count | Core Risk | Core Plus Volume |
| --- | ---: | ---: | ---: |
| near_trend_pullback_reentry / 0.58 | 5 | 3 | 5 |
| trend_pullback_reentry / 0.74 | 3 | 3 | 3 |
| trend_pullback_reentry_relaxed_rsi / 0.64 | 3 | 3 | 3 |

Interpretation:
- Every new `0.74` signal was `PRIMARY_UP_ENTRY_UP`.
- Every new `0.64` signal was `PRIMARY_UP_ENTRY_UP` and mostly dead-range or low-volume.
- `0.58` signals were mostly low-volume or dead-range; two were caught only after volume contraction was added.

## Individual Signal Review

| Time | Signal | Context | Entry RSI | Entry Vol Ratio | Primary Vol Ratio | Issues | Core | Plus |
| --- | --- | --- | ---: | ---: | ---: | --- | --- | --- |
| 2026-04-26 16:44:04 | 0.58 near | PRIMARY_UP_ENTRY_DOWN | 40.235550 | 0.049253 | 0.036688 | DEAD_RANGE, LOW_VOLUME | yes | yes |
| 2026-04-26 17:24:04 | 0.58 near | PRIMARY_UP_ENTRY_DOWN | 41.571150 | 0.043192 | 1.281606 | DEAD_RANGE, VOLUME_CONTRACTION, LOW_VOLUME | yes | yes |
| 2026-04-26 17:44:04 | 0.74 core | PRIMARY_UP_ENTRY_UP | 48.734080 | 2.674967 | 2.435407 | ENTRY_UP | yes | yes |
| 2026-04-26 17:54:04 | 0.58 near | PRIMARY_UP_ENTRY_DOWN | 42.713008 | 0.012932 | 0.570996 | DEAD_RANGE, LOW_VOLUME | yes | yes |
| 2026-04-26 18:04:04 | 0.58 near | PRIMARY_UP_ENTRY_DOWN | 43.400038 | 0.664623 | 3.537035 | VOLUME_CONTRACTION | no | yes |
| 2026-04-26 18:14:04 | 0.58 near | PRIMARY_UP_ENTRY_DOWN | 44.816884 | 0.056319 | 0.448146 | VOLUME_CONTRACTION, LOW_VOLUME | no | yes |
| 2026-04-26 18:34:04 | 0.74 core | PRIMARY_UP_ENTRY_UP | 44.056379 | 0.025913 | 0.593459 | ENTRY_UP, LOW_VOLUME | yes | yes |
| 2026-04-26 19:04:04 | 0.74 core | PRIMARY_UP_ENTRY_UP | 44.836820 | 1.224773 | 0.085178 | ENTRY_UP | yes | yes |
| 2026-04-26 19:24:04 | 0.64 relaxed | PRIMARY_UP_ENTRY_UP | 52.136536 | 0.516638 | 0.584173 | ENTRY_UP, DEAD_RANGE, RELAXED_RSI | yes | yes |
| 2026-04-26 20:24:04 | 0.64 relaxed | PRIMARY_UP_ENTRY_UP | 53.242904 | 0.014173 | 0.112755 | ENTRY_UP, DEAD_RANGE, LOW_VOLUME, RELAXED_RSI | yes | yes |
| 2026-04-26 20:44:04 | 0.64 relaxed | PRIMARY_UP_ENTRY_UP | 54.013162 | 0.074917 | 0.624628 | ENTRY_UP, DEAD_RANGE, LOW_VOLUME, RELAXED_RSI | yes | yes |

## Interpretation

VERIFIED:
- The next validation did not produce new closed trades.
- The new post-logging signals are mostly weak-context signals.
- The candidate filter family correctly flags the current blocked signals as high-risk or low-quality.
- The risk engine blocking these signals is aligned with the offline context-filter hypothesis.

Important:

```text
THIS_IS_NOT_PERFORMANCE_CONFIRMATION
```

This validation only confirms that the newly logged signals are the kind of conditions the offline filter experiment wanted to avoid.
It does not prove that the filter improves real performance because no new executed/closed trades exist.

## Decision

```text
FILTER_PROMOTION = NO
CONFIG_CHANGE = NO
RUNTIME_STRATEGY_TUNING = HOLD
CONTINUE_COLLECTION = TRUE
```

NEXT_REQUIRED:
1. Wait for daily risk reset.
2. Allow unchanged testnet runtime to collect real post-logging trades.
3. Re-run all-trade feature decomposition after at least 5 new closed trades.
4. Re-run full filter experiment after at least 10 new post-logging closed trades.

## Design Summary

This is a forward signal-quality validation. It reads new `decision_id` and `market_features` records from `portfolio.log`, compares them against the offline filter candidates, and checks exchange 1m klines for pre-runup and volume-change context. It does not change runtime code, config, strategy logic, order routing, or risk rules.

## Validation Result

```text
VALIDATION = PASS
POST_LOGGING_SIGNALS = 11
CORE_RISK_SET_BLOCKED = 9
CORE_PLUS_VOLUME_BLOCKED = 11
OUTPUT_JSON = reports/cnt_next_context_filter_validation_20260426.json
RUNTIME_CODE_CHANGED = NO
CONFIG_CHANGED = NO
```

## Record Text

2026-04-26: The next validation was run against new post-logging blocked signals. No new closed trades were available, so performance validation remains pending. Signal-quality validation supports the current hypothesis: the latest signals are mostly ENTRY_UP, dead-range, low-volume, volume-contraction, or relaxed-RSI contexts. Runtime strategy remains unchanged.

Related:
- [[CNT_CONTEXT_FILTER_EXPERIMENT_20260426]]
- [[CNT_ALL_TRADE_WIN_LOSS_FEATURE_DECOMPOSITION_20260426]]
- [[CNT_EXCHANGE_REPLAY_MARKET_CONTEXT_REVIEW_20260426]]
- [[CNT_MARKET_CONTEXT_LOGGING_LAYER_IMPLEMENTATION_20260426]]

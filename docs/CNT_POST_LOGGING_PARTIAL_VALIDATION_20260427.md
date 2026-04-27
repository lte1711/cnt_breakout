---
tags:
  - cnt
  - post-logging
  - partial-validation
  - market-context
  - type/documentation
  - status/active
  - pre-runup
  - type/validation
  - type/operation
  - strategy/pullback_v1
  - type/analysis
---

# CNT Post Logging Partial Validation 20260427

## Verdict

```text
REPORT_STATUS = VERIFIED_WITH_LOCAL_POST_LOGGING_CLOSE_RECORDS
RUNTIME_CHANGE = NO
CONFIG_CHANGE = NO
STRATEGY_CHANGE = NO
SOURCE = logs/portfolio.log
POST_LOGGING_CLOSED_TRADES = 9
BASELINE_TOTAL_CLOSED = 42
CURRENT_TOTAL_CLOSED = 51
```

## Scope

FACT:
- This report evaluates closed trades that contain both `decision_id` and `market_features`.
- It uses the new decision-time logging layer.
- It does not fetch exchange klines and therefore does not reconstruct exact `PRE_RUNUP_30M` or `FAST_ADVERSE_MOVE`.

UNKNOWN:
- Exact exchange-replayed pre-runup and path MFE/MAE for these 9 trades.
- Whether the 9-trade sample is stable enough for parameter or runtime promotion.

## Aggregate

| Metric | Value |
| --- | ---: |
| Trades | 9 |
| Wins | 6 |
| Losses | 3 |
| Win rate | 0.666667 |
| Net PnL | 0.004060 |
| Expectancy | 0.000451 |
| Profit factor | 1.078215 |

## Context Split

| Group | Trades | Wins | Losses | Expectancy | PF | Net PnL |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| PRIMARY_DOWN_ENTRY_UP | 3 | 3 | 0 | 0.009328 | NA | 0.027984 |
| PRIMARY_UP_ENTRY_UP | 3 | 1 | 2 | -0.010241 | 0.232909 | -0.030722 |
| PRIMARY_UP_ENTRY_DOWN | 2 | 1 | 1 | -0.001254 | 0.788497 | -0.002508 |
| PRIMARY_DOWN_ENTRY_DOWN | 1 | 1 | 0 | 0.009306 | NA | 0.009306 |

## Signal Split

| Group | Trades | Wins | Losses | Expectancy | PF | Net PnL |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| trend_pullback_reentry_relaxed_rsi | 5 | 3 | 2 | -0.002413 | 0.698727 | -0.012066 |
| near_trend_pullback_reentry | 3 | 2 | 1 | 0.002266 | 1.573284 | 0.006798 |
| trend_pullback_reentry | 1 | 1 | 0 | 0.009328 | NA | 0.009328 |

## Local Issue Split

| Group | Trades | Wins | Losses | Expectancy | PF | Net PnL |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| ENTRY_UP_CONTEXT | 6 | 4 | 2 | -0.000456 | 0.931635 | -0.002738 |
| VOLUME_CONTRACTION | 6 | 4 | 2 | -0.000456 | 0.931635 | -0.002738 |
| LARGE_BODY_ENTRY | 5 | 3 | 2 | -0.001676 | 0.769789 | -0.008382 |
| DEAD_RANGE_CANDLE | 4 | 3 | 1 | 0.000858 | 1.139785 | 0.003432 |
| LOW_ENTRY_VOLUME | 3 | 2 | 1 | -0.001973 | 0.758961 | -0.005918 |
| PRIMARY_EMA_EXTENSION | 3 | 2 | 1 | 0.001060 | 1.205188 | 0.003180 |
| PRIMARY_RSI_OVERHEATED | 2 | 2 | 0 | 0.009339 | NA | 0.018678 |
| ENTRY_ATR_EXPANDED | 1 | 0 | 1 | -0.015498 | 0.000000 | -0.015498 |
| NO_LOCAL_ISSUE | 1 | 1 | 0 | 0.009306 | NA | 0.009306 |

## Trade Rows

| Close Time | Result | PnL | Signal | Context | Entry RSI | Entry Vol Ratio | Issues |
| --- | --- | ---: | --- | --- | ---: | ---: | --- |
| 2026-04-27 02:04:03 | LOSS | -0.011858 | near_trend_pullback_reentry / 0.580000 | PRIMARY_UP_ENTRY_DOWN | 47.095995 | 1.170655 | LARGE_BODY_ENTRY |
| 2026-04-27 03:04:04 | WIN | 0.009284 | trend_pullback_reentry_relaxed_rsi / 0.640000 | PRIMARY_DOWN_ENTRY_UP | 52.988192 | 0.005559 | ENTRY_UP_CONTEXT, DEAD_RANGE_CANDLE, LOW_ENTRY_VOLUME, VOLUME_CONTRACTION |
| 2026-04-27 04:14:03 | WIN | 0.009328 | trend_pullback_reentry / 0.740000 | PRIMARY_UP_ENTRY_UP | 51.311616 | 0.435478 | ENTRY_UP_CONTEXT, LARGE_BODY_ENTRY, VOLUME_CONTRACTION, PRIMARY_RSI_OVERHEATED, PRIMARY_EMA_EXTENSION |
| 2026-04-27 04:54:04 | WIN | 0.009350 | near_trend_pullback_reentry / 0.580000 | PRIMARY_UP_ENTRY_DOWN | 45.302426 | 0.292905 | DEAD_RANGE_CANDLE, LARGE_BODY_ENTRY, VOLUME_CONTRACTION, PRIMARY_RSI_OVERHEATED, PRIMARY_EMA_EXTENSION |
| 2026-04-27 06:34:03 | LOSS | -0.024552 | trend_pullback_reentry_relaxed_rsi / 0.640000 | PRIMARY_UP_ENTRY_UP | 52.938583 | 0.135723 | ENTRY_UP_CONTEXT, DEAD_RANGE_CANDLE, LARGE_BODY_ENTRY, LOW_ENTRY_VOLUME, VOLUME_CONTRACTION |
| 2026-04-27 07:04:04 | WIN | 0.009306 | near_trend_pullback_reentry / 0.580000 | PRIMARY_DOWN_ENTRY_DOWN | 40.379194 | 1.470594 | NONE |
| 2026-04-27 08:24:04 | WIN | 0.009350 | trend_pullback_reentry_relaxed_rsi / 0.640000 | PRIMARY_DOWN_ENTRY_UP | 52.136527 | 0.045362 | ENTRY_UP_CONTEXT, DEAD_RANGE_CANDLE, LARGE_BODY_ENTRY, LOW_ENTRY_VOLUME, VOLUME_CONTRACTION |
| 2026-04-27 09:04:04 | WIN | 0.009350 | trend_pullback_reentry_relaxed_rsi / 0.640000 | PRIMARY_DOWN_ENTRY_UP | 55.274558 | 1.012840 | ENTRY_UP_CONTEXT |
| 2026-04-27 10:34:02 | LOSS | -0.015498 | trend_pullback_reentry_relaxed_rsi / 0.640000 | PRIMARY_UP_ENTRY_UP | 53.874839 | 0.422002 | ENTRY_UP_CONTEXT, VOLUME_CONTRACTION, PRIMARY_EMA_EXTENSION, ENTRY_ATR_EXPANDED |

## Interpretation

VERIFIED:
- The post-logging sample is net positive but small.
- `PRIMARY_UP_ENTRY_UP` produced both wins and losses, confirming that upward entry context alone is not a reliable bullish condition.
- The largest loss is in `PRIMARY_UP_ENTRY_UP` with high primary RSI and EMA extension, matching the late-chase risk thesis.
- Low entry volume appears in both winners and losers, so volume level alone remains insufficient.
- The sample supports continued context validation, not live/config mutation.

FACT:
- Partial validation trigger is met because new closed trades are greater than or equal to 5.
- Full filter rerun trigger is not met if the threshold is 10 new post-logging closed trades.

## Decision

```text
PARTIAL_VALIDATION = COMPLETE
FULL_FILTER_RERUN = WAIT_FOR_1_MORE_CLOSED_TRADE
FILTER_PROMOTION = NO
RUNTIME_STRATEGY_TUNING = HOLD
CONFIG_CHANGE = HOLD
LIVE_TRANSITION = HOLD
```

## Design Summary

Add a read-only local validation report for post-logging closed trades. The report uses only persisted `decision_id` and `market_features` from `portfolio.log`.

## Validation Result

```text
VALIDATION = PASS
OUTPUT_JSON = reports/cnt_post_logging_partial_validation_20260427.json
OUTPUT_DOC = docs/CNT_POST_LOGGING_PARTIAL_VALIDATION_20260427.md
```

## Record Text

2026-04-27: The 9 post-logging closed trades were partially validated. The sample is positive overall but still confirms context sensitivity. The next required step is one more post-logging closed trade followed by full filter experiment rerun with exchange replay if available.

Related:
- [[CNT_NEXT_CONTEXT_FILTER_VALIDATION_20260426]]
- [[CNT_CONTEXT_FILTER_EXPERIMENT_20260426]]
- [[CNT_ALL_TRADE_WIN_LOSS_FEATURE_DECOMPOSITION_20260426]]

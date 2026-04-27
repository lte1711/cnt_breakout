---
tags:
  - cnt
  - market-context
  - pre-runup
  - threshold-analysis
  - type/documentation
  - status/active
  - post-logging
  - offline-experiment
  - type/operation
  - type/analysis
---

# CNT Pre Runup Threshold Analysis 20260427

## Verdict

```text
REPORT_STATUS = VERIFIED_WITH_EXISTING_EXCHANGE_REPLAY_DATASET
RUNTIME_CHANGE = NO
CONFIG_CHANGE = NO
STRATEGY_CHANGE = NO
SOURCE = reports/cnt_all_trade_exchange_feature_analysis_20260426.json
```

## Scope

FACT:
- The source dataset has 42 matched closed trades.
- It already includes exchange-replayed `ret30`, `mfe`, `mae`, candle body, and issue tags.
- This report searches for offline threshold candidates only.

UNKNOWN:
- Whether the same threshold remains valid on the 9 newer post-logging trades, because those need exchange replay refresh.
- Whether a threshold should be promoted to runtime logic.

## Baseline

| Metric | Value |
| --- | ---: |
| Trades | 42 |
| Wins | 21 |
| Losses | 21 |
| Win rate | 0.500000 |
| Net PnL | -0.024296 |
| Expectancy | -0.000578 |
| Profit factor | 0.931389 |
| Avg ret30 | 0.000369 |
| Avg MFE | 0.004761 |
| Avg MAE | -0.008895 |
| Avg body | 0.691952 |

## Context Path Quality

| Group | Trades | Wins | Losses | Expectancy | PF | Avg ret30 | Avg MFE | Avg MAE |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| UNKNOWN | 12 | 4 | 8 | -0.002404 | 0.701503 | 0.001061 | 0.005432 | -0.016028 |
| RANGE/DOWN/MEDIUM | 10 | 5 | 5 | 0.000426 | 1.054411 | -0.000627 | 0.005091 | -0.002362 |
| TREND_UP/UNKNOWN/MEDIUM | 10 | 9 | 1 | 0.011806 | 11.797238 | -0.000434 | 0.006524 | -0.010325 |
| TREND_UP/UP/MEDIUM | 8 | 3 | 5 | -0.004656 | 0.575537 | 0.000411 | 0.002182 | -0.004463 |
| TREND_UP/UP/HIGH | 1 | 0 | 1 | -0.011044 | 0.000000 | 0.002030 | 0.000000 | -0.002120 |
| TREND_UP/UP/LOW | 1 | 0 | 1 | -0.069476 | 0.000000 | 0.008070 | 0.001190 | -0.016550 |

## Issue Path Quality

| Group | Trades | Wins | Losses | Expectancy | PF | Avg ret30 | Avg MFE | Avg MAE |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| LARGE_BODY_ENTRY | 4 | 3 | 1 | 0.008666 | 4.296215 | -0.002805 | 0.004063 | -0.000947 |
| PRE_RUNUP_30M,SHORT_TERM_CHASE,LARGE_BODY_ENTRY | 3 | 3 | 0 | 0.011447 | NA | 0.003820 | 0.008373 | -0.000887 |
| FAST_ADVERSE_MOVE,NEAR_TREND_SIGNAL | 2 | 2 | 0 | 0.017980 | NA | -0.001325 | 0.005525 | -0.003220 |
| LOW_ENTRY_VOLUME | 2 | 2 | 0 | 0.018894 | NA | 0.000375 | 0.006240 | -0.000030 |
| LOW_ENTRY_VOLUME,DEAD_RANGE_CANDLE,NEAR_TREND_SIGNAL | 2 | 1 | 1 | 0.000071 | 1.015799 | -0.001210 | 0.002570 | -0.001130 |
| LOW_ENTRY_VOLUME,VOLUME_CONTRACTION,DEAD_RANGE_CANDLE,NEAR_TREND_SIGNAL | 2 | 0 | 2 | -0.013717 | 0.000000 | -0.002715 | 0.010420 | -0.002210 |
| NO_ISSUE | 2 | 2 | 0 | 0.022352 | NA | -0.002390 | 0.018030 | -0.001350 |
| PRE_RUNUP_30M,FAST_ADVERSE_MOVE | 2 | 0 | 2 | -0.018051 | 0.000000 | 0.002595 | 0.000265 | -0.004945 |
| ENTRY_UP_CONTEXT | 1 | 1 | 0 | 0.030668 | NA | -0.001120 | 0.006190 | -0.000190 |
| ENTRY_UP_CONTEXT,RELAXED_RSI_SIGNAL | 1 | 1 | 0 | 0.010710 | NA | -0.004170 | 0.004610 | -0.000460 |
| FAST_ADVERSE_MOVE | 1 | 0 | 1 | -0.012958 | 0.000000 | 0.001480 | 0.000400 | -0.168940 |
| LARGE_BODY_ENTRY,DEAD_RANGE_CANDLE | 1 | 0 | 1 | -0.008602 | 0.000000 | 0.000800 | 0.000670 | -0.002300 |
| LARGE_BODY_ENTRY,DEAD_RANGE_CANDLE,FAST_ADVERSE_MOVE,ENTRY_UP_CONTEXT | 1 | 1 | 0 | 0.009130 | NA | -0.000320 | 0.002500 | -0.007830 |
| LARGE_BODY_ENTRY,ENTRY_UP_CONTEXT,RELAXED_RSI_SIGNAL | 1 | 0 | 1 | -0.012100 | 0.000000 | -0.001510 | 0.001930 | -0.002570 |
| LARGE_BODY_ENTRY,FAST_ADVERSE_MOVE,ENTRY_UP_CONTEXT | 1 | 0 | 1 | -0.019162 | 0.000000 | 0.000420 | 0.000410 | -0.005360 |
| LARGE_BODY_ENTRY,FAST_ADVERSE_MOVE,NEAR_TREND_SIGNAL | 1 | 0 | 1 | -0.017451 | 0.000000 | -0.000560 | 0.001420 | -0.004440 |
| LARGE_BODY_ENTRY,NEAR_TREND_SIGNAL | 1 | 1 | 0 | 0.013734 | NA | 0.000760 | 0.005890 | 0.000000 |
| LOW_ENTRY_VOLUME,DEAD_RANGE_CANDLE | 1 | 0 | 1 | -0.008492 | 0.000000 | 0.000620 | 0.000610 | -0.001700 |
| LOW_ENTRY_VOLUME,LARGE_BODY_ENTRY,FAST_ADVERSE_MOVE | 1 | 1 | 0 | 0.014806 | NA | 0.000260 | 0.012360 | -0.095230 |
| LOW_ENTRY_VOLUME,PRE_RUNUP_30M,SHORT_TERM_CHASE,LARGE_BODY_ENTRY,FAST_ADVERSE_MOVE,ENTRY_UP_CONTEXT | 1 | 0 | 1 | -0.016324 | 0.000000 | 0.002420 | 0.000980 | -0.005570 |
| LOW_ENTRY_VOLUME,VOLUME_CONTRACTION,DEAD_RANGE_CANDLE | 1 | 0 | 1 | -0.008030 | 0.000000 | 0.000440 | 0.002450 | -0.001650 |
| LOW_ENTRY_VOLUME,VOLUME_CONTRACTION,LARGE_BODY_ENTRY,DEAD_RANGE_CANDLE | 1 | 1 | 0 | 0.009086 | NA | -0.000130 | 0.002660 | -0.000570 |
| LOW_ENTRY_VOLUME,VOLUME_CONTRACTION,PRE_RUNUP_30M,LARGE_BODY_ENTRY | 1 | 1 | 0 | 0.010868 | NA | 0.002520 | 0.018680 | -0.001020 |
| LOW_ENTRY_VOLUME,VOLUME_CONTRACTION,PRE_RUNUP_30M,LARGE_BODY_ENTRY,DEAD_RANGE_CANDLE | 1 | 0 | 1 | -0.011924 | 0.000000 | 0.002530 | 0.000610 | -0.002590 |
| PRE_RUNUP_30M,LARGE_BODY_ENTRY | 1 | 0 | 1 | -0.011044 | 0.000000 | 0.002030 | 0.000000 | -0.002120 |
| PRE_RUNUP_30M,LARGE_BODY_ENTRY,FAST_ADVERSE_MOVE,ENTRY_UP_CONTEXT,RELAXED_RSI_SIGNAL | 1 | 0 | 1 | -0.012144 | 0.000000 | 0.003070 | 0.000000 | -0.003310 |
| PRE_RUNUP_30M,LARGE_BODY_ENTRY,FAST_ADVERSE_MOVE,NEAR_TREND_SIGNAL | 1 | 0 | 1 | -0.024402 | 0.000000 | 0.005470 | 0.001510 | -0.005680 |
| PRE_RUNUP_30M,SHORT_TERM_CHASE,FAST_ADVERSE_MOVE | 1 | 0 | 1 | -0.069476 | 0.000000 | 0.008070 | 0.001190 | -0.016550 |
| PRE_RUNUP_30M,SHORT_TERM_CHASE,LARGE_BODY_ENTRY,FAST_ADVERSE_MOVE,ENTRY_UP_CONTEXT | 1 | 0 | 1 | -0.028028 | 0.000000 | 0.004500 | 0.000840 | -0.010410 |
| SHORT_TERM_CHASE,LARGE_BODY_ENTRY,NEAR_TREND_SIGNAL | 1 | 1 | 0 | 0.023709 | NA | -0.001440 | 0.005060 | -0.000380 |
| VOLUME_CONTRACTION,LARGE_BODY_ENTRY | 1 | 0 | 1 | -0.010934 | 0.000000 | -0.001530 | 0.001540 | -0.002480 |

## All Trade PRE_RUNUP Threshold Candidates

| Candidate | Retained | Missed Winners | Blocked Losers | Retained Expectancy | Retained PF | Retained Net PnL |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all_ret30_gte_-0.0010 | 11 | 15 | 16 | 0.007427 | 2.374092 | 0.081698 |
| all_ret30_gte_-0.0005 | 12 | 15 | 15 | 0.005354 | 1.835386 | 0.064247 |
| all_ret30_gte_0.0000 | 16 | 11 | 15 | 0.006455 | 2.342856 | 0.103275 |
| all_ret30_gte_0.0005 | 20 | 9 | 13 | 0.004999 | 1.960384 | 0.099975 |
| all_ret30_gte_0.0010 | 25 | 6 | 11 | 0.005388 | 2.111360 | 0.134689 |
| all_ret30_gte_0.0015 | 29 | 4 | 9 | 0.004825 | 1.967311 | 0.139938 |
| all_ret30_gte_0.0020 | 29 | 4 | 9 | 0.004825 | 1.967311 | 0.139938 |
| all_ret30_gte_0.0025 | 32 | 4 | 6 | 0.003105 | 1.536454 | 0.099370 |
| all_ret30_gte_0.0030 | 36 | 2 | 4 | 0.002392 | 1.391273 | 0.086104 |
| all_ret30_gte_0.0040 | 38 | 1 | 3 | 0.002202 | 1.360388 | 0.083684 |

## ENTRY_UP PRE_RUNUP Threshold Candidates

| Candidate | Retained | Missed Winners | Blocked Losers | Retained Expectancy | Retained PF | Retained Net PnL |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| entry_up_ret30_gte_-0.0010 | 3 | 1 | 6 | 0.009759 | 3.419669 | 0.029278 |
| entry_up_ret30_gte_-0.0005 | 3 | 1 | 6 | 0.009759 | 3.419669 | 0.029278 |
| entry_up_ret30_gte_0.0000 | 4 | 0 | 6 | 0.009602 | 4.174215 | 0.038408 |
| entry_up_ret30_gte_0.0005 | 5 | 0 | 5 | 0.003849 | 1.615636 | 0.019246 |
| entry_up_ret30_gte_0.0010 | 5 | 0 | 5 | 0.003849 | 1.615636 | 0.019246 |
| entry_up_ret30_gte_0.0015 | 5 | 0 | 5 | 0.003849 | 1.615636 | 0.019246 |
| entry_up_ret30_gte_0.0020 | 5 | 0 | 5 | 0.003849 | 1.615636 | 0.019246 |
| entry_up_ret30_gte_0.0025 | 7 | 0 | 3 | -0.001160 | 0.861470 | -0.008122 |
| entry_up_ret30_gte_0.0030 | 7 | 0 | 3 | -0.001160 | 0.861470 | -0.008122 |
| entry_up_ret30_gte_0.0040 | 8 | 0 | 2 | -0.002533 | 0.713652 | -0.020266 |

## Best Offline Candidates

```text
BEST_ALL_TRADES_THRESHOLD = all_ret30_gte_-0.0010
BEST_ALL_RETAINED_EXPECTANCY = 0.007427
BEST_ENTRY_UP_THRESHOLD = entry_up_ret30_gte_-0.0010
BEST_ENTRY_UP_RETAINED_EXPECTANCY = 0.009759
PRACTICAL_ENTRY_UP_ZERO_MISSED_WINNER = entry_up_ret30_gte_0.0000 / retained_expectancy=0.009602
```

## ENTRY_UP Trade Rows

| Entry | Result | PnL | Signal | Context | ret30 | MFE | MAE | Issues |
| --- | --- | ---: | --- | --- | ---: | ---: | ---: | --- |
| 2026-04-20 17:34 | LOSS | -0.011044 | trend_up_high_volatility_breakout / 0.820000 | TREND_UP/UP/HIGH | 0.002030 | 0.000000 | -0.002120 | PRE_RUNUP_30M, LARGE_BODY_ENTRY |
| 2026-04-21 01:14 | LOSS | -0.019162 | trend_pullback_reentry / 0.740000 | TREND_UP/UP/MEDIUM | 0.000420 | 0.000410 | -0.005360 | LARGE_BODY_ENTRY, FAST_ADVERSE_MOVE, ENTRY_UP_CONTEXT |
| 2026-04-22 01:34 | LOSS | -0.028028 | trend_pullback_reentry / 0.740000 | TREND_UP/UP/MEDIUM | 0.004500 | 0.000840 | -0.010410 | PRE_RUNUP_30M, SHORT_TERM_CHASE, LARGE_BODY_ENTRY, FAST_ADVERSE_MOVE, ENTRY_UP_CONTEXT |
| 2026-04-22 04:24 | LOSS | -0.069476 | trend_up_relaxed_volatility_breakout / 0.680000 | TREND_UP/UP/LOW | 0.008070 | 0.001190 | -0.016550 | PRE_RUNUP_30M, SHORT_TERM_CHASE, FAST_ADVERSE_MOVE |
| 2026-04-23 01:54 | WIN | 0.010710 | trend_pullback_reentry_relaxed_rsi / 0.640000 | TREND_UP/UP/MEDIUM | -0.004170 | 0.004610 | -0.000460 | ENTRY_UP_CONTEXT, RELAXED_RSI_SIGNAL |
| 2026-04-24 00:14 | WIN | 0.030668 | trend_pullback_reentry / 0.740000 | TREND_UP/UP/MEDIUM | -0.001120 | 0.006190 | -0.000190 | ENTRY_UP_CONTEXT |
| 2026-04-24 00:44 | LOSS | -0.012144 | trend_pullback_reentry_relaxed_rsi / 0.640000 | TREND_UP/UP/MEDIUM | 0.003070 | 0.000000 | -0.003310 | PRE_RUNUP_30M, LARGE_BODY_ENTRY, FAST_ADVERSE_MOVE, ENTRY_UP_CONTEXT, RELAXED_RSI_SIGNAL |
| 2026-04-24 01:04 | LOSS | -0.012100 | trend_pullback_reentry_relaxed_rsi / 0.640000 | TREND_UP/UP/MEDIUM | -0.001510 | 0.001930 | -0.002570 | LARGE_BODY_ENTRY, ENTRY_UP_CONTEXT, RELAXED_RSI_SIGNAL |
| 2026-04-24 03:34 | LOSS | -0.016324 | trend_pullback_reentry / 0.740000 | TREND_UP/UP/MEDIUM | 0.002420 | 0.000980 | -0.005570 | LOW_ENTRY_VOLUME, PRE_RUNUP_30M, SHORT_TERM_CHASE, LARGE_BODY_ENTRY, FAST_ADVERSE_MOVE, ENTRY_UP_CONTEXT |
| 2026-04-26 02:13 | WIN | 0.009130 | trend_pullback_reentry / 0.740000 | TREND_UP/UP/MEDIUM | -0.000320 | 0.002500 | -0.007830 | LARGE_BODY_ENTRY, DEAD_RANGE_CANDLE, FAST_ADVERSE_MOVE, ENTRY_UP_CONTEXT |

## Interpretation

VERIFIED:
- `TREND_UP/UP` style contexts are worse than the overall baseline.
- Losses show higher `ret30` and worse MFE/MAE path quality than wins in the existing exchange replay dataset.
- `PRE_RUNUP_30M`, `ENTRY_UP_CONTEXT`, and `FAST_ADVERSE_MOVE` remain the strongest late-chase evidence cluster.
- A pure `ret30` cutoff can improve historical retained expectancy, but it also blocks some winners.
- For ENTRY_UP trades, `ret30 >= 0.0000` is the strongest practical threshold in this dataset because it blocks 6 losers and misses 0 winners.

FACT:
- This supports a filter hypothesis.
- It does not approve a runtime filter.
- The next high-value work is to refresh exchange replay for the 9 post-logging trades once the 10-trade trigger is met.

## Decision

```text
PRE_RUNUP_THRESHOLD_CANDIDATE = OBSERVATIONAL_ONLY
FILTER_PROMOTION = NO
CONFIG_CHANGE = HOLD
RUNTIME_STRATEGY_TUNING = HOLD
NEXT_REQUIRED = exchange replay refresh after 1 more post-logging closed trade
```

## Design Summary

Add a read-only threshold analysis over the existing all-trade exchange replay dataset. The tool computes retained performance after candidate `ret30` cutoffs and isolates ENTRY_UP contexts.

## Validation Result

```text
VALIDATION = PASS
OUTPUT_JSON = reports/cnt_pre_runup_threshold_analysis_20260427.json
OUTPUT_DOC = docs/CNT_PRE_RUNUP_THRESHOLD_ANALYSIS_20260427.md
```

## Record Text

2026-04-27: PRE_RUNUP threshold candidates were evaluated offline against the 42-trade exchange replay dataset. The result confirms late-chase risk but remains observational until the post-logging exchange replay sample reaches at least 10 closed trades.

Related:
- [[CNT_ALL_TRADE_WIN_LOSS_FEATURE_DECOMPOSITION_20260426]]
- [[CNT_CONTEXT_FILTER_EXPERIMENT_20260426]]
- [[CNT_POST_LOGGING_PARTIAL_VALIDATION_20260427]]

---
tags:
  - cnt
  - full-filter-rerun
  - exchange-replay
created: 2026-04-27
---

# CNT Full Filter Rerun 20260427

## Verdict

```text
REPORT_STATUS = VERIFIED_WITH_BINANCE_SPOT_TESTNET_1M_KLINES
RUNTIME_CHANGE = NO
CONFIG_CHANGE = NO
STRATEGY_CHANGE = NO
POST_LOGGING_CLOSED_TRADES = 9
```

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
| Avg ret30 | 0.000378 |
| Avg MFE | 0.003250 |
| Avg MAE | -0.002625 |

## Context Split

| Group | Trades | Wins | Losses | Expectancy | PF | Avg ret30 | Avg MFE | Avg MAE |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| PRIMARY_DOWN_ENTRY_UP | 3 | 3 | 0 | 0.009328 | NA | -0.000924 | 0.004902 | -0.003271 |
| PRIMARY_UP_ENTRY_UP | 3 | 1 | 2 | -0.010241 | 0.232909 | 0.003402 | 0.001454 | -0.003220 |
| PRIMARY_UP_ENTRY_DOWN | 2 | 1 | 1 | -0.001254 | 0.788497 | 0.000522 | 0.001675 | -0.001390 |
| PRIMARY_DOWN_ENTRY_DOWN | 1 | 1 | 0 | 0.009306 | NA | -0.005075 | 0.006833 | -0.001376 |

## Issue Split

| Group | Trades | Wins | Losses | Expectancy | PF | Avg ret30 | Avg MFE | Avg MAE |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| ENTRY_UP_CONTEXT | 6 | 4 | 2 | -0.000456 | 0.931635 | 0.001239 | 0.003178 | -0.003245 |
| NO_ISSUE | 3 | 2 | 1 | 0.002266 | 1.573284 | -0.001343 | 0.003395 | -0.001385 |
| PRE_RUNUP_30M | 3 | 2 | 1 | 0.001060 | 1.205188 | 0.003757 | 0.002781 | -0.000947 |
| FAST_ADVERSE_MOVE | 1 | 0 | 1 | -0.015498 | 0.000000 | 0.005191 | -0.000323 | -0.003652 |
| SHORT_TERM_CHASE | 1 | 0 | 1 | -0.015498 | 0.000000 | 0.005191 | -0.000323 | -0.003652 |
| VOLUME_CONTRACTION | 1 | 1 | 0 | 0.009284 | NA | -0.000128 | 0.007109 | -0.009011 |

## Candidate Filters

| Filter | Retained | Missed Winners | Blocked Losers | Retained Expectancy | Retained PF |
| --- | ---: | ---: | ---: | ---: | ---: |
| block_PRE_RUNUP_30M | 6 | 2 | 1 | 0.000147 | 1.024169 |
| block_ENTRY_NEAR_HIGH | 9 | 0 | 0 | 0.000451 | 1.078215 |
| block_ENTRY_UP_CONTEXT | 3 | 4 | 2 | 0.002266 | 1.573284 |
| block_FAST_ADVERSE_MOVE | 8 | 0 | 1 | 0.002445 | 1.537160 |
| block_PRE_RUNUP_OR_ENTRY_NEAR_HIGH | 6 | 2 | 1 | 0.000147 | 1.024169 |
| block_LATE_CHASE_SET | 3 | 4 | 2 | 0.002266 | 1.573284 |
| block_FULL_RISK_SET | 3 | 4 | 2 | 0.002266 | 1.573284 |

## Trade Rows

| Entry | Close | Result | PnL | Context | ret30 | High Dist | MFE | MAE | Issues |
| --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: | --- |
| 2026-04-27 00:14:05 | 2026-04-27 02:04:03 | LOSS | -0.011858 | PRIMARY_UP_ENTRY_DOWN | -0.000320 | 0.001692 | 0.001168 | -0.002357 | NONE |
| 2026-04-27 02:14:05 | 2026-04-27 03:04:04 | WIN | 0.009284 | PRIMARY_DOWN_ENTRY_UP | -0.000128 | 0.000742 | 0.007109 | -0.009011 | ENTRY_UP_CONTEXT, VOLUME_CONTRACTION |
| 2026-04-27 03:34:05 | 2026-04-27 04:14:03 | WIN | 0.009328 | PRIMARY_UP_ENTRY_UP | 0.004162 | 0.003081 | 0.002983 | -0.000606 | PRE_RUNUP_30M, ENTRY_UP_CONTEXT |
| 2026-04-27 04:34:05 | 2026-04-27 04:54:04 | WIN | 0.009350 | PRIMARY_UP_ENTRY_DOWN | 0.001364 | 0.004572 | 0.002182 | -0.000423 | NONE |
| 2026-04-27 05:14:02 | 2026-04-27 06:34:03 | LOSS | -0.024552 | PRIMARY_UP_ENTRY_UP | 0.000854 | 0.001394 | 0.001702 | -0.005402 | ENTRY_UP_CONTEXT |
| 2026-04-27 06:54:05 | 2026-04-27 07:04:04 | WIN | 0.009306 | PRIMARY_DOWN_ENTRY_DOWN | -0.005075 | 0.005551 | 0.006833 | -0.001376 | NONE |
| 2026-04-27 07:54:05 | 2026-04-27 08:24:04 | WIN | 0.009350 | PRIMARY_DOWN_ENTRY_UP | -0.004564 | 0.005152 | 0.001914 | -0.002218 | ENTRY_UP_CONTEXT |
| 2026-04-27 08:44:02 | 2026-04-27 09:04:04 | WIN | 0.009350 | PRIMARY_DOWN_ENTRY_UP | 0.001919 | 0.003154 | 0.005682 | 0.001416 | PRE_RUNUP_30M, ENTRY_UP_CONTEXT |
| 2026-04-27 10:24:01 | 2026-04-27 10:34:02 | LOSS | -0.015498 | PRIMARY_UP_ENTRY_UP | 0.005191 | 0.011342 | -0.000323 | -0.003652 | PRE_RUNUP_30M, SHORT_TERM_CHASE, ENTRY_UP_CONTEXT, FAST_ADVERSE_MOVE |

## Decision

```text
FILTER_PROMOTION = NO
RUNTIME_STRATEGY_TUNING = HOLD
CONFIG_CHANGE = HOLD
LIVE_TRANSITION = HOLD
```

## Record Text

2026-04-27: Full filter rerun was executed on post-logging closed trades using Binance Spot Testnet 1m klines. This report is an offline validation artifact only.

Related:
- [[CNT_POST_LOGGING_PARTIAL_VALIDATION_20260427]]
- [[CNT_PRE_RUNUP_THRESHOLD_ANALYSIS_20260427]]

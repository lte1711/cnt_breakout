---
tags:
  - cnt
  - reproducibility
  - edge-validation
created: 2026-04-26
---

# CNT Conditional Edge Reproducibility Review 20260426

## Verdict

```text
NEXT_PHASE = CONDITIONAL_EDGE_VALIDATION
PRIMARY_EDGE_CLUSTER = trend_pullback_reentry / confidence 0.74
REPRODUCIBILITY_STATUS = PARTIAL_MIXED
EDGE_CONFIRMED = NO
EDGE_REJECTED = NO
RUNTIME_CHANGE = NONE
CONFIG_CHANGE = NONE
```

## Scope

This review checks whether the current positive cluster is reproducible across time slices using existing local logs.

Source:

```text
logs/signal.log
logs/runtime.log
logs/portfolio.log
tools/analyze_pullback_market_context.py
```

Limitation:

```text
Pre-market_features trades do not contain deep decision-time features.
This is a historical log correlation test, not a replay backtest.
```

## Aggregate 0.74 Cluster

VERIFIED:

```text
cluster = trend_pullback_reentry / confidence 0.74
trades = 23
wins = 13
losses = 10
win_rate = 0.565217
net_pnl = 0.059053
expectancy = 0.002568
profit_factor = 1.382369
```

Initial reading:

```text
EDGE_CANDIDATE = YES
```

But aggregate alone is insufficient because the time-split result is mixed.

## Chronological Split

First half:

```text
trades = 11
wins = 8
losses = 3
win_rate = 0.727273
net_pnl = 0.077379
expectancy = 0.007034
profit_factor = 3.086137
```

Second half:

```text
trades = 12
wins = 5
losses = 7
win_rate = 0.416667
net_pnl = -0.018326
expectancy = -0.001527
profit_factor = 0.843832
```

Interpretation:

```text
REPRODUCIBILITY_ACROSS_TIME = NOT_CONFIRMED
```

The same 0.74 label did not remain consistently positive in the later half.

## Five-Trade Rolling Chunks

```text
chunk_1: trades=5, wins=3, losses=2, expectancy=0.001813, profit_factor=1.346510
chunk_2: trades=5, wins=4, losses=1, expectancy=0.011489, profit_factor=6.253978
chunk_3: trades=5, wins=3, losses=2, expectancy=-0.001518, profit_factor=0.819561
chunk_4: trades=5, wins=2, losses=3, expectancy=0.003164, profit_factor=1.313426
chunk_5: trades=3, wins=1, losses=2, expectancy=-0.005229, profit_factor=0.367908
```

Interpretation:

```text
REPRODUCIBILITY_BY_SMALL_WINDOW = MIXED
```

The edge signal appears in several windows, but it is unstable and deteriorates in the latest small window.

## Day Split

```text
2026-04-19: trades=5, wins=3, losses=2, expectancy=0.001813, profit_factor=1.346510
2026-04-20: trades=9, wins=7, losses=2, expectancy=0.007669, profit_factor=3.039810
2026-04-21: trades=3, wins=0, losses=3, expectancy=-0.013867, profit_factor=0.000000
2026-04-22: trades=2, wins=1, losses=1, expectancy=0.003795, profit_factor=1.270801
2026-04-24: trades=2, wins=1, losses=1, expectancy=0.007172, profit_factor=1.878706
2026-04-26: trades=2, wins=1, losses=1, expectancy=0.000319, profit_factor=1.075130
```

Interpretation:

```text
REPRODUCIBILITY_BY_DAY = PARTIAL
BAD_DAY_DETECTED = 2026-04-21
```

The cluster was positive on most observed days, but one day fully failed. Some days have only 2 to 3 samples and cannot be treated as statistically reliable.

## Market Context Caveat

The earlier strong group contains `TREND_UP/UNKNOWN/MEDIUM`.

```text
TREND_UP/UNKNOWN/MEDIUM: trades=14, wins=10, losses=4, expectancy=0.005577, profit_factor=2.301513
TREND_UP/UP/MEDIUM: trades=12, wins=4, losses=8, expectancy=-0.002714, profit_factor=0.725638
```

Interpretation:

```text
UNKNOWN_TREND_BIAS_IS_SCHEMA_ARTIFACT = LIKELY
```

The positive historical segment overlaps with an earlier logging period where `trend_bias` was not always available. Therefore, the current labels alone cannot prove a stable market condition.

## Reproducibility Decision

```text
EDGE_STATUS_PREVIOUS = CONDITIONAL_POSSIBLE
EDGE_STATUS_CURRENT = CONDITIONAL_POSSIBLE_BUT_UNSTABLE
REPRODUCIBILITY_VALIDATION = IN_PROGRESS
```

The 0.74 cluster remains the best candidate, but it has not passed reproducibility validation.

## Required Next Evidence

Reproducibility requires new post-logging samples:

```text
minimum_new_0_74_closed_trades = 10
preferred_new_0_74_closed_trades = 20
must_include_market_features = TRUE
must_split_by_market_context = TRUE
```

Pass candidate:

```text
new_0_74_expectancy > 0
new_0_74_profit_factor >= 1.15
no single day dominates total profit
loss day remains controlled by DAILY_LOSS_LIMIT
```

Fail candidate:

```text
new_0_74_expectancy <= 0
new_0_74_profit_factor < 1.0
profit depends on one isolated burst only
bad days erase multiple good days
```

## Operational Decision

```text
DO_NOT_TUNE_NOW = TRUE
DO_NOT_PROMOTE_TO_LIVE = TRUE
DO_NOT_CREATE_0_74_FILTER = TRUE
CONTINUE_TESTNET_COLLECTION = TRUE
```

Reason:
- The aggregate 0.74 cluster is positive.
- Time-split reproducibility is not yet stable.
- New market-feature tagged trades are required before turning this into a strategy rule.

## Design Summary

This review performs historical reproducibility analysis using existing logs. It adds no runtime behavior, changes no config, and does not alter strategy selection or risk controls.

## Validation Result

```text
HISTORICAL_LOG_MATCHING = PASS
TIME_SPLIT_ANALYSIS = PASS
DAY_SPLIT_ANALYSIS = PASS
RUNTIME_CHANGE = NONE
```

## Record Text

2026-04-26: Conditional edge reproducibility validation began. The 0.74 pullback cluster remains the best positive candidate, but time-split analysis is mixed. The correct next step is to collect new market-feature tagged 0.74 closed trades after normal risk reset.

Related:
- [[CNT_POSITIVE_EDGE_EVIDENCE_FROM_BLOCKED_STATE_20260426]]
- [[CNT_PULLBACK_MARKET_CONTEXT_ANALYSIS_20260426]]
- [[CNT_MARKET_CONTEXT_LOGGING_LAYER_IMPLEMENTATION_20260426]]

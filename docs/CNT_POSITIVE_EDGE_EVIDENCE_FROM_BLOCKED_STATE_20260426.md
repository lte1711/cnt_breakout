---
tags:
  - cnt
  - edge-evidence
  - market-context
  - type/documentation
  - status/active
  - type/operation
  - strategy/pullback_v1
---

# CNT Positive Edge Evidence From Blocked State 20260426

## Purpose

User request:

```text
Find the reasons it can work from the reasons it cannot trade now.
Secure the information.
```

## Verdict

```text
POSITIVE_REASON_FOUND = TRUE
PRIMARY_POSITIVE_SOURCE = trend_pullback_reentry / confidence 0.74
CURRENT_BLOCK_IS_USEFUL = TRUE
CURRENT_LOW_QUALITY_CONTEXT_IS_USEFUL_EVIDENCE = TRUE
RUNTIME_CHANGE = NONE
CONFIG_CHANGE = NONE
```

## Core Finding

The current system is not failing because it cannot trade. It is refusing to trade after a daily loss cluster and while the available signal quality is weak.

This gives two positive facts:

```text
1. The system can identify and stop a bad trading day.
2. Historical pullback data already contains a better-performing signal cluster.
```

## Positive Evidence From Historical Trades

VERIFIED from `docs/CNT_PULLBACK_MARKET_CONTEXT_ANALYSIS_20260426.md`:

```text
pullback_v1 total matched trades = 39
wins = 20
losses = 19
expectancy = 0.001085
profit_factor = 1.154603
```

The positive cluster:

```text
signal_reason = trend_pullback_reentry
confidence    = 0.74
trades        = 23
wins          = 13
losses        = 10
win_rate      = 0.565217
net_pnl       = 0.059053
expectancy    = 0.002568
profit_factor = 1.382369
```

Interpretation:
- This is the current `PRIMARY_EDGE_CANDIDATE`.
- It is not yet proven enough for live trading.
- It is materially better than the weaker signal families.

## Negative Cluster Converted Into Positive Information

Current weak clusters:

```text
near_trend_pullback_reentry / confidence 0.58
trend_pullback_reentry_relaxed_rsi / confidence 0.64
```

Historical result:

```text
0.58 cluster expectancy = -0.000248
0.58 cluster PF         = 0.966062

0.64 cluster expectancy = -0.004511
0.64 cluster PF         = 0.441759
```

Positive information extracted:

```text
Do not treat all pullback signals as equal.
The system works better when signal quality is separated by reason and confidence.
```

This is useful because future tuning can target filtering weak contexts instead of changing the full strategy blindly.

## Current Blocked State Converted Into Positive Information

Current risk facts:

```text
daily_loss_count = 3
MAX_DAILY_LOSS_COUNT = 3
PRIMARY_BLOCKER = DAILY_LOSS_LIMIT
```

Positive information extracted:

```text
The risk engine is preventing repeated exposure during a weak signal environment.
```

This is a working part of the system. It protects the test from converting a weak market day into uncontrolled overtrading.

## Latest Market Features

Latest allowed-but-blocked signal:

```text
timestamp      = 2026-04-26 16:44:02
reason         = near_trend_pullback_reentry
confidence     = 0.58
market_context = PRIMARY_UP_ENTRY_DOWN
entry_rsi      = 40.235550
entry_volume_ratio = 0.049253
primary_volume_ratio = 0.036688
```

Latest no-entry signal:

```text
timestamp      = 2026-04-26 16:54:02
reason         = pullback_rsi_not_in_range
market_context = PRIMARY_UP_ENTRY_UP
entry_rsi      = 75.316426
entry_volume_ratio = 3.283711
primary_volume_ratio = 0.970682
```

Positive information extracted:

```text
The new logging layer can now distinguish two different non-trade states:
1. weak pullback with low volume
2. overextended short-term RSI outside pullback band
```

This is exactly the evidence needed for future market-feature based filtering.

## What Must Happen For Trading To Become Valid Again

Required operational conditions:

```text
daily_loss_count resets normally
pending_order remains null
open_trade remains null
entry gate receives an allowed signal
risk guard passes
```

Preferred signal condition:

```text
signal_reason = trend_pullback_reentry
confidence    = 0.74
market context should not be weak/noise dominated
```

Observed weak conditions to avoid treating as strong:

```text
confidence = 0.58
confidence = 0.64
entry timeframe down while primary timeframe up
very low volume ratio
RSI outside pullback band
```

## Information Secured

```text
CAN_WORK_REASON_1 = There is a historically positive 0.74 pullback cluster.
CAN_WORK_REASON_2 = Risk engine blocks trading during daily loss clusters.
CAN_WORK_REASON_3 = New market_features can separate weak contexts from better contexts.
CAN_WORK_REASON_4 = The system does not need forced entry; it needs better evidence collection.
```

## Do Not Act On This Yet

```text
DO_NOT_TUNE_NOW = TRUE
DO_NOT_RESET_RISK = TRUE
DO_NOT_FORCE_ENTRY = TRUE
DO_NOT_CHANGE_CONFIG = TRUE
```

Reason:
- Positive evidence exists, but sample size remains insufficient.
- The next step is to collect more market-feature tagged trades after normal risk reset.

## Next Evidence To Capture

For every future closed pullback trade, preserve and later compare:

```text
decision_id
signal_reason
confidence
market_context
entry_rsi
entry_ema_gap_pct
entry_ema_slope_pct
entry_atr_pct
entry_volume_ratio
primary_rsi
primary_ema_gap_pct
primary_ema_slope_pct
primary_atr_pct
primary_volume_ratio
close_pnl_estimate
```

## Design Summary

This report extracts positive operating evidence from the current blocked state. It does not change runtime behavior, strategy parameters, config, risk rules, or order routing.

## Validation Result

```text
HISTORICAL_PULLBACK_REVIEW = PASS
CURRENT_STATE_REVIEW = PASS
LATEST_MARKET_FEATURE_REVIEW = PASS
RUNTIME_CHANGE = NONE
```

## Record Text

2026-04-26: The blocked state was analyzed for positive evidence. The main positive source is the `trend_pullback_reentry` confidence `0.74` cluster. The active risk block is also positive because it prevents repeated exposure in a weak signal environment. The new market-feature logs now provide the information needed to compare future winning and losing contexts.

Related:
- [[CNT_TRADE_BLOCK_AND_MARKET_CONTEXT_REVIEW_20260426]]
- [[CNT_PULLBACK_MARKET_CONTEXT_ANALYSIS_20260426]]
- [[CNT_MARKET_CONTEXT_LOGGING_LAYER_IMPLEMENTATION_20260426]]

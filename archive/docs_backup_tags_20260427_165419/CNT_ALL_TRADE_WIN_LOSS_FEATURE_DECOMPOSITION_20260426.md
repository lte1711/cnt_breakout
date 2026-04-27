---
tags:
  - cnt
  - trade-analysis
  - win-loss
  - market-context
created: 2026-04-26
---

# CNT All Trade Win Loss Feature Decomposition 20260426

## Verdict

```text
REPORT_STATUS = VERIFIED_WITH_LOCAL_LOGS_AND_EXCHANGE_KLINES
SCOPE = ALL_MATCHED_CLOSED_TRADES
MATCHED_TRADES = 42
EXCHANGE_SOURCE = Binance Spot Testnet /api/v3/klines
SYMBOL = ETHUSDT
INTERVAL = 1m
RUNTIME_CHANGE = NONE
CONFIG_CHANGE = NONE
STRATEGY_CHANGE = NONE
```

## Purpose

This report answers the specific question:

```text
WHEN_DOES_CNT_WIN?
WHEN_DOES_CNT_LOSE?
WHAT_MARKET_ISSUES_EXIST_AT_WIN_TIME?
WHAT_MARKET_ISSUES_EXIST_AT_LOSS_TIME?
HOW_DOES_VOLUME_CHANGE?
```

The analysis uses:
- local `runtime.log` for entry/open events,
- local `portfolio.log` for close PnL,
- local `signal.log` for signal context when available,
- Binance Spot Testnet public 1 minute klines for exchange-side OHLCV replay.

The generated machine-readable artifact is:

```text
reports/cnt_all_trade_exchange_feature_analysis_20260426.json
```

## Data Caveats

FACT:
- 42 closed trades were matched.
- Aggregate performance exactly matches current project totals.
- Exchange replay used public OHLCV, not signed private order history.

UNKNOWN:
- Historical order book depth and tick-level spread are not reconstructed.
- Some early trades have incomplete signal-context matching and are grouped as `UNKNOWN`.
- Testnet can contain abnormal liquidity and extreme candles; these are treated as context evidence, not exact execution proof.

## Aggregate

| Metric | Value |
| --- | ---: |
| Trades | 42 |
| Wins | 21 |
| Losses | 21 |
| Win rate | 0.500000 |
| Net PnL | -0.024296 |
| Expectancy | -0.000578 |
| Profit factor | 0.931389 |

FINAL:

```text
AGGREGATE_EDGE = NEGATIVE
SYSTEM_EXECUTION_PROBLEM = FALSE
MARKET_CONTEXT_PROBLEM = TRUE
```

## Winners vs Losers

| Feature | Winners | Losers | Interpretation |
| --- | ---: | ---: | --- |
| Avg vol_ratio_30 | 0.735463 | 0.752948 | volume level alone does not separate wins |
| Avg vol_change_5v5 | 0.997927 | 1.364698 | losses often entered after short volume expansion |
| Avg ret30_pre | -0.000472 | 0.001210 | losses entered after stronger prior run-up |
| Avg ret60_pre | -0.001466 | 0.002264 | winners more often followed prior cooling/pullback |
| Avg MFE to close | 0.007620 | 0.001903 | winners quickly had much more upside room |
| Avg MAE to close | -0.005683 | -0.012107 | losses suffered deeper adverse movement |
| Median realized path RR | 7.153846 | 0.266082 | path quality, not signal existence, separates wins |

VERIFIED:
- Winning trades were not defined by higher raw volume.
- Winning trades usually had a better pullback/recovery path: less pre-runup, higher favorable movement, and lower adverse movement.
- Losing trades were often entered after prior upward movement or short-term volume expansion, then failed to continue.

## Main Loss Drivers

| Issue | Trades | Wins | Losses | Expectancy | PF | Reading |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| PRE_RUNUP_30M | 13 | 4 | 9 | -0.012633 | 0.215857 | already moved too far before entry |
| FAST_ADVERSE_MOVE | 14 | 4 | 10 | -0.012582 | 0.253750 | entry was immediately punished |
| VOLUME_CONTRACTION | 7 | 2 | 5 | -0.005481 | 0.342135 | participation dried up |
| ENTRY_UP_CONTEXT | 8 | 3 | 5 | -0.004656 | 0.575537 | late chase risk |
| DEAD_RANGE_CANDLE | 10 | 3 | 7 | -0.004612 | 0.372206 | no useful movement at entry |
| RELAXED_RSI_SIGNAL | 3 | 1 | 2 | -0.004511 | 0.441759 | relaxed condition is weak |

Interpretation:

```text
PRIMARY_LOSS_PATTERN =
  prior run-up
  + entry-up or chase context
  + weak continuation
  + fast adverse movement
```

This confirms the user's diagnosis:

```text
CURRENT_PROBLEM =
  not signal generation,
  but distinguishing real pullback from late chase entry.
```

## Main Win Drivers

| Condition | Evidence |
| --- | --- |
| Prior cooling or pullback | winners avg ret60_pre = -0.001466 |
| Favorable movement after entry | winners avg MFE = 0.007620 |
| Smaller adverse path | winners avg MAE = -0.005683 |
| Strong path quality | winners median path RR = 7.153846 |
| Best context | `TREND_UP/UNKNOWN/MEDIUM`, but this includes historical schema artifact risk |

The strongest historical context:

| Context | Trades | Wins | Losses | Expectancy | PF |
| --- | ---: | ---: | ---: | ---: | ---: |
| TREND_UP/UNKNOWN/MEDIUM | 10 | 9 | 1 | 0.011806 | 11.797238 |

Important caution:

```text
TREND_UP/UNKNOWN/MEDIUM cannot be used as a direct rule.
UNKNOWN is partly a historical data/schema artifact.
```

The practical interpretation is:

```text
GOOD_PULLBACK =
  higher timeframe trend exists
  + entry timeframe is not already chasing upward
  + prior movement cooled
  + entry has room to move favorably before stop pressure
```

## Signal Group Analysis

| Signal | Trades | Wins | Losses | Expectancy | PF | Reading |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| trend_pullback_reentry / 0.74 | 15 | 11 | 4 | 0.006289 | 2.267207 | best matched signal subset |
| near_trend_pullback_reentry / 0.58 | 10 | 5 | 5 | 0.000426 | 1.054411 | mostly flat |
| relaxed_rsi / 0.64 | 3 | 1 | 2 | -0.004511 | 0.441759 | weak |
| breakout high volatility / 0.82 | 1 | 0 | 1 | -0.011044 | 0.000000 | failed |
| breakout relaxed volatility / 0.68 | 1 | 0 | 1 | -0.069476 | 0.000000 | major loss |

Note:
- This strict exchange replay signal match has 12 `UNKNOWN` signal-context rows due historical context gaps.
- The separate local context report still shows 23 historical `0.74` trades from timestamp correlation.
- Both analyses agree that `0.74` is the only meaningful candidate and `0.64` is weak.

## Market Context Analysis

| Context | Trades | Wins | Losses | Expectancy | PF | Reading |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| TREND_UP/UNKNOWN/MEDIUM | 10 | 9 | 1 | 0.011806 | 11.797238 | strongest historical context, artifact caution |
| RANGE/DOWN/MEDIUM | 10 | 5 | 5 | 0.000426 | 1.054411 | flat |
| TREND_UP/UP/MEDIUM | 8 | 3 | 5 | -0.004656 | 0.575537 | chase/late-entry risk |
| TREND_UP/UP/HIGH | 1 | 0 | 1 | -0.011044 | 0.000000 | breakout failed |
| TREND_UP/UP/LOW | 1 | 0 | 1 | -0.069476 | 0.000000 | worst breakout loss |

VERIFIED:
- `TREND_UP/UP` is not automatically bullish for CNT.
- `ENTRY_UP` often means the pullback has already ended and CNT is late.
- The strategy needs evidence to distinguish re-entry after pullback from momentum chase.

## Volume Analysis

FACT:
- Winners avg `vol_ratio_30` = 0.735463.
- Losers avg `vol_ratio_30` = 0.752948.
- Winners avg `vol_change_5v5` = 0.997927.
- Losers avg `vol_change_5v5` = 1.364698.

Interpretation:

```text
VOLUME_LEVEL_ALONE = NOT_DISCRIMINATING
VOLUME_EXPANSION_AFTER_RUNUP = DANGEROUS
VOLUME_CONTRACTION = DANGEROUS
```

Meaning:
- Higher volume did not automatically create wins.
- Losses often had higher immediate volume expansion, but that expansion occurred after a prior run-up and did not continue.
- Extremely low volume or dead-range candles are also bad because targets cannot be reached reliably.

Two bad volume structures exist:

```text
BAD_VOLUME_TYPE_1 =
  low volume
  + dead range
  + no follow-through

BAD_VOLUME_TYPE_2 =
  volume expansion
  + prior run-up
  + late chase
  + reversal
```

## Representative Losses

| Entry | Strategy | PnL | Signal | Context | Key Issues |
| --- | --- | ---: | --- | --- | --- |
| 2026-04-22 04:24 | breakout_v1 | -0.069476 | breakout 0.68 | TREND_UP/UP/LOW | prior run-up, short-term chase, fast adverse move |
| 2026-04-22 01:34 | pullback_v1 | -0.028028 | 0.74 | TREND_UP/UP/MEDIUM | prior run-up, chase, large body, fast adverse move |
| 2026-04-23 00:54 | pullback_v1 | -0.024402 | 0.58 | RANGE/DOWN/MEDIUM | prior run-up, large body, fast adverse move |
| 2026-04-24 03:34 | pullback_v1 | -0.016324 | 0.74 | TREND_UP/UP/MEDIUM | low volume, prior run-up, chase, large body |
| 2026-04-25 21:44 | pullback_v1 | -0.014850 | 0.58 | RANGE/DOWN/MEDIUM | low volume, volume contraction, dead-range candle |

Common loss issue:

```text
LOSS_COMMONALITY =
  entry after prior move
  or no useful liquidity/range
  and insufficient favorable path before adverse move
```

## Representative Wins

| Entry | Strategy | PnL | Signal | Context | Reading |
| --- | --- | ---: | --- | --- | --- |
| 2026-04-22 02:34 | pullback_v1 | 0.035618 | context gap | UNKNOWN | strong favorable path, low adverse movement |
| 2026-04-24 00:14 | pullback_v1 | 0.030668 | 0.74 | TREND_UP/UP/MEDIUM | ENTRY_UP can win only when follow-through is immediate |
| 2026-04-20 15:24 | pullback_v1 | 0.026128 | 0.74 | TREND_UP/UNKNOWN/MEDIUM | very low adverse movement |
| 2026-04-20 07:24 | pullback_v1 | 0.024081 | 0.74 | TREND_UP/UNKNOWN/MEDIUM | prior 30m cooling, strong recovery |
| 2026-04-23 04:14 | pullback_v1 | 0.023709 | 0.58 | RANGE/DOWN/MEDIUM | small adverse move, enough MFE |

Important:
- Some winning rows also contain isolated warning tags.
- The difference is path quality: winners still had enough MFE before damaging MAE.
- Therefore a single feature threshold is not enough yet.

## Answer To The Core Question

### When CNT makes money

```text
CNT_WINS_WHEN =
  entry is not after a strong prior run-up
  + pullback has room to rebound
  + favorable movement appears before adverse movement
  + market is not dead-range
  + entry is not just ENTRY_UP chase
```

### When CNT loses money

```text
CNT_LOSES_WHEN =
  prior 30m run-up is already large
  or 1m context is already UP/chasing
  or volume contracts into a dead candle
  or volume expands after run-up but fails to continue
  or adverse move appears before target path develops
```

## Current Strategy Implication

```text
SIGNAL_GENERATION = WORKING
WIN_LOSS_DISCRIMINATION = INSUFFICIENT
VOLUME_ABSOLUTE_FILTER = INSUFFICIENT
CONTEXT_PATH_FILTER = REQUIRED_BUT_NOT_NOW
```

Do not tune immediately.

Reason:
- Sample size is still small.
- Feature interactions matter more than one feature.
- Some tagged risk conditions also appear inside winning trades.

## Next Evidence To Collect

For each new decision, keep logging:

```text
decision_id
signal reason
confidence
multi_timeframe_trend
entry volume ratio
volume 5v5 change
ret5_pre
ret30_pre
ret60_pre
candle body ratio
range pct
MFE after entry
MAE after entry
close reason
PnL
```

The next evaluation should answer:

```text
Can PRE_RUNUP_30M + ENTRY_UP_CONTEXT + FAST_ADVERSE_MOVE be detected before entry?
Can GOOD_PULLBACK be identified before entry without filtering out the winning 0.74 cases?
```

## Decision

```text
DO_NOT_CHANGE_CONFIG = TRUE
DO_NOT_TUNE_STRATEGY_NOW = TRUE
DO_NOT_FORCE_TRADE = TRUE
DO_NOT_RESET_RISK = TRUE
NEXT_ACTION = collect post-logging trades and re-run this decomposition
```

## Design Summary

This is a read-only all-trade decomposition. It reconstructs the local closed trade sequence and compares each entry/close window against exchange 1 minute OHLCV. It does not alter runtime code, config, strategy rules, order rules, or risk rules.

## Validation Result

```text
VALIDATION = PASS
MATCHED_TRADES = 42
LOCAL_TOTALS_MATCH_PROJECT = TRUE
EXCHANGE_KLINES_FETCHED = TRUE
ANALYSIS_JSON = reports/cnt_all_trade_exchange_feature_analysis_20260426.json
RUNTIME_CODE_CHANGED = NO
CONFIG_CHANGED = NO
ORDER_PATH_CHANGED = NO
```

## Record Text

2026-04-26: All matched closed trades were decomposed into win/loss features using local logs and Binance Spot Testnet 1 minute klines. The result confirms that CNT's issue is not generating signals but separating true pullback re-entry from late chase, dead-range, low-participation, and fast adverse movement conditions.

Related:
- [[CNT_EXCHANGE_REPLAY_MARKET_CONTEXT_REVIEW_20260426]]
- [[CNT_PULLBACK_MARKET_CONTEXT_ANALYSIS_20260426]]
- [[CNT_CONDITIONAL_EDGE_REPRODUCIBILITY_REVIEW_20260426]]
- [[CNT_MARKET_CONTEXT_LOGGING_LAYER_IMPLEMENTATION_20260426]]

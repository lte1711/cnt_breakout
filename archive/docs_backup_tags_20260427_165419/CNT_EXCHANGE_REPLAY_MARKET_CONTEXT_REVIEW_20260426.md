---
tags:
  - cnt
  - exchange-replay
  - market-context
  - pullback-v1
created: 2026-04-26
---

# CNT Exchange Replay Market Context Review 20260426

## Verdict

```text
REPORT_STATUS = VERIFIED_WITH_EXCHANGE_KLINES
EXCHANGE_SOURCE = Binance Spot Testnet public klines
SOURCE_ENDPOINT = https://testnet.binance.vision/api/v3/klines
SYMBOL = ETHUSDT
INTERVAL = 1m
RUNTIME_CHANGE = NONE
CONFIG_CHANGE = NONE
STRATEGY_CHANGE = NONE
```

## Scope

FACT:
- Local matched pullback trades = 39.
- Local pullback selected signals = 242.
- Exchange replay used `ETHUSDT` 1 minute OHLCV around each matched pullback entry time.
- Local log timestamps were treated as KST and converted to UTC milliseconds for Binance kline requests.
- Exchange replay is OHLCV replay, not private account order-history replay.

UNKNOWN:
- Historical raw order book and tick-level spread were not reconstructed.
- Private signed exchange order history was not queried in this review.
- Testnet liquidity can contain abnormal candles; therefore extreme kline wicks are treated as context evidence, not exact execution proof.

## Project Progression Comparison

| Phase | Trades | Wins | Losses | Win Rate | Net PnL | Expectancy | PF | Exchange Reading |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| early_positive_0419_0420 | 14 | 10 | 4 | 0.714286 | 0.078083 | 0.005577 | 2.301513 | 30 minute forward return positive on average |
| degradation_0421_0424 | 18 | 7 | 11 | 0.388889 | -0.023223 | -0.001290 | 0.866245 | forward edge mostly disappeared |
| post_logging_0425_0426 | 7 | 3 | 4 | 0.428571 | -0.012562 | -0.001795 | 0.685746 | low range and low liquidity dominated |

VERIFIED:
- The project moved from an apparently strong early pullback regime into a weaker regime after 2026-04-21.
- This matches the previous conclusion that the system problem is not execution quality but market-context discrimination.
- The latest market context logging implementation was the correct next action because the historical logs had shallow market labels only.

## Existing Report Comparison

The existing local report `CNT_PULLBACK_MARKET_CONTEXT_ANALYSIS_20260426.md` remains consistent.

| Split | Trades | Wins | Losses | Expectancy | PF |
| --- | ---: | ---: | ---: | ---: | ---: |
| pullback_v1 aggregate | 39 | 20 | 19 | 0.001085 | 1.154603 |
| trend_pullback_reentry / 0.74 | 23 | 13 | 10 | 0.002568 | 1.382369 |
| near_trend_pullback_reentry / 0.58 | 13 | 6 | 7 | -0.000248 | 0.966062 |
| relaxed_rsi / 0.64 | 3 | 1 | 2 | -0.004511 | 0.441759 |

Exchange replay adds this:

| Split | Avg Vol Ratio | Avg Body Ratio | Avg Ret 5m Pre | Avg Ret 30m Pre | Avg Fwd 30m Ret | Avg Fwd 30m Max | Avg Fwd 30m Min |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| aggregate | 0.700624 | 0.694077 | -0.000161 | 0.000000 | 0.000522 | 0.004083 | -0.006370 |
| 0.74 core | 0.733803 | 0.773545 | 0.000030 | 0.000338 | 0.000457 | 0.004545 | -0.009576 |
| 0.58 near | 0.646542 | 0.516355 | -0.000292 | -0.000397 | 0.000827 | 0.003704 | -0.001443 |
| 0.64 relaxed | 0.680606 | 0.854958 | -0.001049 | -0.000870 | -0.000299 | 0.002181 | -0.003143 |

Interpretation:
- `0.74` remains the best historical candidate by PnL, but exchange replay does not show it as universally strong.
- `0.64` is confirmed as weak in both local result and exchange replay.
- `0.58` is not a reliable edge by local PnL even though its average forward 30 minute return was mildly positive; this means path risk and stop placement matter more than simple forward direction.

## Market Context Comparison

| Market Context | Trades | Wins | Losses | Expectancy | PF | Exchange Reading |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| TREND_UP/UNKNOWN/MEDIUM | 14 | 10 | 4 | 0.005577 | 2.301513 | strongest historical cluster |
| RANGE/DOWN/MEDIUM | 13 | 6 | 7 | -0.000248 | 0.966062 | weak/flat |
| TREND_UP/UP/MEDIUM | 12 | 4 | 8 | -0.002714 | 0.725638 | confirms chase-entry problem |

Exchange metrics:

| Market Context | Avg Vol Ratio | Avg Body Ratio | Avg Fwd 30m Ret | Avg Fwd 30m Max | Avg Fwd 30m Min |
| --- | ---: | ---: | ---: | ---: | ---: |
| TREND_UP/UNKNOWN/MEDIUM | 0.610328 | 0.779849 | 0.001107 | 0.004198 | -0.014140 |
| RANGE/DOWN/MEDIUM | 0.646542 | 0.516355 | 0.000827 | 0.003704 | -0.001443 |
| TREND_UP/UP/MEDIUM | 0.864559 | 0.786543 | -0.000491 | 0.004358 | -0.002643 |

VERIFIED:
- The weakest performance context is `TREND_UP/UP/MEDIUM`, not absence of higher-timeframe trend.
- This supports the existing diagnosis: the strategy confuses clean pullback re-entry with late chase entry.
- `TREND_UP/UNKNOWN/MEDIUM` must not be converted directly into a rule because `UNKNOWN` is partly a historical schema artifact.

## Daily Comparison

| Date | Trades | Wins | Losses | Expectancy | PF | Exchange Reading |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| 2026-04-19 | 5 | 3 | 2 | 0.001813 | 1.346510 | positive but with abnormal downside wick risk |
| 2026-04-20 | 9 | 7 | 2 | 0.007669 | 3.039810 | strongest day, forward 30m drift positive |
| 2026-04-21 | 3 | 0 | 3 | -0.013867 | 0.000000 | failure day, forward 30m drift negative |
| 2026-04-22 | 4 | 2 | 2 | 0.002843 | 1.280065 | mixed |
| 2026-04-23 | 7 | 4 | 3 | 0.002415 | 1.332507 | modestly positive |
| 2026-04-24 | 4 | 1 | 3 | -0.002475 | 0.755965 | weak |
| 2026-04-25 | 2 | 0 | 2 | -0.011440 | 0.000000 | very low activity/range |
| 2026-04-26 | 5 | 3 | 2 | 0.002064 | 1.603604 | small positive, not enough sample |

## Current Blocked-State Comparison

VERIFIED:
- Current risk state has `DAILY_LOSS_LIMIT` blocking further allowed signals.
- Recent blocked pullback selected signals are dominated by `0.58` and `0.64` contexts.
- Recent exchange replay around blocked signals shows low volume ratio or low range in many cases.

Examples from 2026-04-26:

| Time KST | Signal | Policy | Exchange Reading |
| --- | --- | --- | --- |
| 2026-04-26 16:44:03 | 0.58 near pullback | DAILY_LOSS_LIMIT | volume ratio near 0.03, extremely narrow 1m range |
| 2026-04-26 17:24:04 | 0.58 near pullback | DAILY_LOSS_LIMIT | volume ratio near 0.13, narrow/no-body candle |

Interpretation:
- The risk block is consistent with market context, not a false system failure.
- The current market is not producing the strongest historical edge structure.

## Core Finding

```text
PRIMARY_PROBLEM = GOOD_PULLBACK_VS_CHASE_ENTRY_DISCRIMINATION
EXCHANGE_REPLAY_SUPPORT = TRUE
EXECUTION_SYSTEM_FAILURE = FALSE
RISK_BLOCK_VALIDITY = SUPPORTED
CONFIG_CHANGE_REQUIRED = NO
```

The exchange replay supports the main diagnosis:
- Winning periods had enough continuation after entry.
- Losing periods often had the same higher-timeframe trend label but weaker forward follow-through.
- `TREND_UP/UP/MEDIUM` behaved like late-entry/chase risk.
- The latest blocked signals were not strong enough to justify bypassing risk.

## Decision

```text
DO_NOT_TUNE_NOW = TRUE
DO_NOT_RESET_RISK = TRUE
DO_NOT_FORCE_TRADE = TRUE
DO_NOT_PROMOTE_LIVE = TRUE
NEXT_REQUIRED_EVIDENCE = post-logging market_features on new closed trades
```

NEXT_SAFE_ACTION:
1. Continue testnet operation unchanged.
2. Preserve `decision_id` and `market_features` for every new allowed signal.
3. Re-evaluate after at least 10 new post-logging closed pullback trades.
4. Require 50 total pullback closed trades for first strategy review.

## Design Summary

This review adds a read-only exchange replay comparison. It compares local project progression, signal groups, market context groups, daily performance, and current blocked signals against Binance Spot Testnet public OHLCV at the same times. No runtime behavior is changed.

## Validation Result

```text
VALIDATION = PASS
LOCAL_LOGS_READ = TRUE
EXCHANGE_KLINES_FETCHED = TRUE
MATCHED_PULLBACK_TRADES = 39
RUNTIME_CODE_CHANGED = NO
CONFIG_CHANGED = NO
ORDER_PATH_CHANGED = NO
```

## Record Text

2026-04-26: Historical pullback trades and current blocked signals were compared against Binance Spot Testnet 1 minute klines. Exchange replay supports the existing conclusion that CNT's current weakness is market-context discrimination, especially distinguishing valid pullbacks from late chase entries. No strategy or config change is approved at this stage.

Related:
- [[CNT_PULLBACK_MARKET_CONTEXT_ANALYSIS_20260426]]
- [[CNT_CONDITIONAL_EDGE_REPRODUCIBILITY_REVIEW_20260426]]
- [[CNT_TRADE_BLOCK_AND_MARKET_CONTEXT_REVIEW_20260426]]
- [[CNT_MARKET_CONTEXT_LOGGING_LAYER_IMPLEMENTATION_20260426]]

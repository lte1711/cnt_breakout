---
tags:
  - cnt
  - market-context
  - risk-review
  - type/documentation
  - status/active
  - type/operation
  - risk
  - strategy/pullback_v1
---

# CNT Trade Block And Market Context Review 20260426

## Verdict

```text
TRADE_NOT_OCCURRED_CAUSE = RISK_BLOCK
PRIMARY_BLOCKER = DAILY_LOSS_LIMIT
MARKET_SIGNAL_ABSENCE = FALSE
SYSTEM_FAILURE = FALSE
ORDER_FAILURE = FALSE
CONFIG_CHANGE_REQUIRED = NO
```

## Local Runtime Facts

VERIFIED:
- Last runtime state: `2026-04-26 16:44:00`
- Last action: `EXECUTION_BLOCKED_BY_RISK`
- Last price: `2328.81`
- `pending_order = null`
- `open_trade = null`
- `daily_loss_count = 3`
- `MAX_DAILY_LOSS_COUNT = 3`
- `last_loss_time = 2026-04-26 10:14:01`

FACT:
- Risk guard blocks entries when `daily_loss_count >= MAX_DAILY_LOSS_COUNT`.
- Current state satisfies that block condition.

## Post-Loss Window Review

Window:

```text
FROM = 2026-04-26 10:14
TO   = 2026-04-26 16:44
```

VERIFIED from `logs/portfolio.log`:

```text
selected_pullback_signals = 20
daily_loss_limit_blocks  = 20
loss_cooldown_blocks     = 0
no_ranked_signal_blocks  = 19
```

Selected pullback reason distribution:

```text
trend_pullback_reentry_relaxed_rsi = 8
near_trend_pullback_reentry        = 11
trend_pullback_reentry             = 1
```

No-ranked-signal distribution:

```text
pullback_rsi_not_in_range = 12
trend_not_up              = 7
```

Interpretation:
- The strategy continued to generate executable candidates after the last loss.
- The engine did not submit new orders because the risk guard correctly blocked execution.
- The lack of new trades is not caused by missing signal generation.

## Latest Market Context Snapshot

Latest logged decision:

```text
timestamp      = 2026-04-26 16:44:02
decision_id    = ETHUSDT-pullback_v1-1777189442207
signal_reason  = near_trend_pullback_reentry
confidence     = 0.58
market_context = PRIMARY_UP_ENTRY_DOWN
last_price     = 2328.81
```

Feature snapshot:

```text
primary_trend_bias = UP
entry_trend_bias   = DOWN
entry_rsi          = 40.235550
primary_rsi        = 53.829936
entry_ema_gap_pct  = -0.000116784
primary_ema_gap_pct= 0.000267409
entry_atr_pct      = 0.000111051
primary_atr_pct    = 0.000673503
entry_volume_ratio = 0.049253
primary_volume_ratio = 0.036688
```

Market interpretation:
- Higher timeframe is mildly up.
- Entry timeframe is down or weak.
- RSI is near the lower pullback band.
- Volume ratio is extremely low.
- Candle range and spread proxy are extremely small.

This is a low-energy pullback condition, not a strong continuation setup.

## External Market Comparison

External references checked:
- Polymarket ETH April 26 market references Binance ETH/USDT 1-minute candles as the resolution source and showed the leading range around `2300-2400`.
- CoinMarketCap historical page for April 26 showed broader crypto market cap around `$2.59T`, 24h volume around `$97.32B`, BTC dominance around `59.9%`, ETH dominance around `10.8%`, and Fear and Greed around `43/100`.

Comparison:

```text
LOCAL_ETHUSDT_PRICE = 2328.81
EXTERNAL_RANGE_CONTEXT = 2300-2400
LOCAL_PRICE_MATCHES_EXTERNAL_RANGE = TRUE
MARKET_REGIME = RANGE_OR_WEAK_PULLBACK
```

FACT:
- Local ETHUSDT price sits inside the externally observed 2300-2400 range.
- Local market features show weak short-timeframe momentum and very low local volume.

## Problem Diagnosis

PRIMARY ISSUE:

```text
DAILY_LOSS_LIMIT is active after 3 daily losses.
```

SECONDARY MARKET ISSUE:

```text
The currently selected signals are mostly weaker contexts:
- near_trend_pullback_reentry
- trend_pullback_reentry_relaxed_rsi
```

Important split:

```text
GOOD_REASON = risk guard is preventing additional exposure after a bad daily sequence.
BAD_REASON  = the market is offering mostly weak pullback contexts, not high-quality 0.74 continuation signals.
```

## Decision

```text
DO_NOT_CHANGE_CONFIG = TRUE
DO_NOT_FORCE_TRADE = TRUE
DO_NOT_RESET_RISK_COUNTER = TRUE
DO_NOT_TUNE_PULLBACK_NOW = TRUE
```

The correct action is to let the daily risk block stand. Trading should resume only after normal daily risk reset and only if future signals pass the existing entry and risk gates.

## Design Summary

This review analyzes why new trades are not occurring. No runtime code, config, strategy parameter, order path, or risk rule was changed.

## Validation Result

```text
LOCAL_STATE_READ = PASS
PORTFOLIO_LOG_REVIEW = PASS
SIGNAL_LOG_REVIEW = PASS
EXTERNAL_MARKET_CONTEXT_CHECK = PASS
RUNTIME_CHANGE = NONE
```

## Record Text

2026-04-26: Trade absence was reviewed after market-context logging was added. The cause is not signal absence or engine failure. The immediate blocker is `DAILY_LOSS_LIMIT`, while the current ETHUSDT market context is weak and mostly generating low-confidence pullback candidates. The risk block should remain active.

Related:
- [[CNT_MARKET_CONTEXT_LOGGING_LAYER_IMPLEMENTATION_20260426]]
- [[CNT_PULLBACK_MARKET_CONTEXT_ANALYSIS_20260426]]
- [[CNT v2 TESTNET PERFORMANCE REPORT]]

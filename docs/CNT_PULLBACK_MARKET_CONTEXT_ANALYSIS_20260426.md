---
tags:
  - cnt
  - market-analysis
  - pullback-v1
created: 2026-04-26
---

# CNT Pullback Market Context Analysis 20260426

## Verdict

```text
MARKET_ANALYSIS_STATUS = WEAK_BUT_RECOVERABLE
RUNTIME_CHANGE = NONE
SOURCE = logs/signal.log + logs/runtime.log + logs/portfolio.log
TRADE_MATCH_METHOD = TIMESTAMP_CORRELATION
```

## Scope

FACT:
- Strategy: `pullback_v1`
- Closed pullback trades in portfolio log: 39
- Pullback open-trade entry events in runtime log: 39
- Pullback allowed signals in signal log: 239
- Matched closed trades: 39
- Matched coverage: 100.00%
- Matched trades without signal context: 0

UNKNOWN:
- Exchange-side candle state at each historical decision is not archived as raw klines.
- This report uses log timestamp correlation, not exchange replay.

## Aggregate

| Group | Trades | Wins | Losses | Win Rate | Net PnL | Expectancy | Profit Factor |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| pullback_v1_matched | 39 | 20 | 19 | 0.512821 | 0.042298 | 0.001085 | 1.154603 |

## Market Context Split

| Group | Trades | Wins | Losses | Win Rate | Net PnL | Expectancy | Profit Factor |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| TREND_UP/UNKNOWN/MEDIUM | 14 | 10 | 4 | 0.714286 | 0.078083 | 0.005577 | 2.301513 |
| RANGE/DOWN/MEDIUM | 13 | 6 | 7 | 0.461538 | -0.003221 | -0.000248 | 0.966062 |
| TREND_UP/UP/MEDIUM | 12 | 4 | 8 | 0.333333 | -0.032564 | -0.002714 | 0.725638 |

## Signal Reason Split

| Group | Trades | Wins | Losses | Win Rate | Net PnL | Expectancy | Profit Factor |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| trend_pullback_reentry | 23 | 13 | 10 | 0.565217 | 0.059053 | 0.002568 | 1.382369 |
| near_trend_pullback_reentry | 13 | 6 | 7 | 0.461538 | -0.003221 | -0.000248 | 0.966062 |
| trend_pullback_reentry_relaxed_rsi | 3 | 1 | 2 | 0.333333 | -0.013534 | -0.004511 | 0.441759 |

## Confidence Split

| Group | Trades | Wins | Losses | Win Rate | Net PnL | Expectancy | Profit Factor |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0.74 | 23 | 13 | 10 | 0.565217 | 0.059053 | 0.002568 | 1.382369 |
| 0.58 | 13 | 6 | 7 | 0.461538 | -0.003221 | -0.000248 | 0.966062 |
| 0.64 | 3 | 1 | 2 | 0.333333 | -0.013534 | -0.004511 | 0.441759 |

## Interpretation

VERIFIED:
- Current runtime does record `market_state`, `trend_bias`, and `volatility_state` at signal time.
- Current stored context is shallow. It has no retained RSI, EMA slope, ATR, volume regime, order book, spread, or multi-timeframe candle snapshot per decision.
- `volatility_state` for matched `pullback_v1` trades is effectively not discriminating because observed matched contexts are `MEDIUM`.
- `trend_pullback_reentry` with confidence `0.74` is the current positive contributor.
- `near_trend_pullback_reentry` with confidence `0.58` is approximately flat to weak negative.
- `trend_pullback_reentry_relaxed_rsi` with confidence `0.64` is currently negative, but the sample is only 3 trades.

FACT:
- The system is strong enough at execution, reconciliation, and risk blocking.
- Market analysis is weaker than the execution layer because decision-time market features are not persisted in sufficient depth.

## Actionable Reading

```text
PRIMARY_EDGE_CANDIDATE = trend_pullback_reentry
WEAK_CONTEXT = near_trend_pullback_reentry
HIGH_RISK_CONTEXT = trend_pullback_reentry_relaxed_rsi
SAMPLE_LIMIT = ACTIVE
```

UNKNOWN:
- Whether the confidence `0.74` segment remains profitable after 50 to 100 pullback trades.
- Whether the `0.58` and `0.64` segments are structurally weak or only temporarily weak.

NEXT_SAFE_ACTION:
- Keep collecting data without changing runtime config.
- Register the next improvement as observability and market-context logging, not strategy parameter mutation.

## Required Improvement Register

1. Add decision-time market feature snapshot logging under signal observability.
2. Preserve at minimum RSI, EMA fast, EMA slow, EMA slope, ATR percent, candle body ratio, volume ratio, spread proxy, and multi-timeframe trend state.
3. Add market-context performance aggregation to automatic validation reports.
4. Do not change live config or order logic until at least 50 pullback closed trades are available.

## Design Summary

Add a read-only analysis tool that correlates existing logs and creates a documentation report. No runtime strategy, order, risk, exchange, or config behavior is changed.

## Validation Result

```text
VALIDATION = PASS
RUNTIME_CODE_CHANGED = NO
CONFIG_CHANGED = NO
ORDER_PATH_CHANGED = NO
DOCUMENT_CREATED = docs/CNT_PULLBACK_MARKET_CONTEXT_ANALYSIS_20260426.md
```

## Record Text

2026-04-26: User identified weak market analysis. Local logs were reviewed and a first market-context performance split was generated. The result confirms the concern: CNT currently has enough market labels for rough grouping but not enough archived features for robust market diagnosis.

Related:
- [[CNT_PRECISION_ANALYSIS_REPORT_20260426]]
- [[CNT_EXTERNAL_EVALUATION_REVIEW_20260426]]
- [[CNT v2 TESTNET PERFORMANCE REPORT]]

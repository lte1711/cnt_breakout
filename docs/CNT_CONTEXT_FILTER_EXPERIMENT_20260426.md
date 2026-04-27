---
tags:
  - cnt
  - offline-experiment
  - context-filter
  - pullback-v1
  - type/documentation
  - status/active
  - market-context
  - pre-runup
  - type/operation
  - risk
  - type/analysis
---

# CNT Context Filter Experiment 20260426

## Verdict

```text
RUNTIME_CHANGE = NO
LIVE_CHANGE = NO
CONFIG_CHANGE = NO
EXPERIMENT = YES
MODE = OFFLINE_REPLAY_ONLY
SOURCE = reports/cnt_all_trade_exchange_feature_analysis_20260426.json
```

## Baseline

| Metric | Value |
| --- | ---: |
| Trades | 42 |
| Wins | 21 |
| Losses | 21 |
| Win Rate | 0.500000 |
| Net PnL | -0.024296 |
| Expectancy | -0.000578 |
| Profit Factor | 0.931389 |
| Max Consecutive Losses | 5 |

## Candidate Results

| Filter | Retained | Missed Winners | Blocked Losers | Retained Win Rate | Retained Expectancy | Retained PF | Max CL | Net PnL |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| block_PRE_RUNUP_30M | 29 | 4 | 9 | 0.586207 | 0.004825 | 1.967311 | 3 | 0.139938 |
| block_ENTRY_UP_CONTEXT | 34 | 3 | 5 | 0.529412 | 0.000381 | 1.048635 | 4 | 0.012954 |
| block_DEAD_RANGE_CANDLE | 32 | 3 | 7 | 0.562500 | 0.000682 | 1.077779 | 3 | 0.021828 |
| mark_FAST_ADVERSE_MOVE_block | 28 | 4 | 10 | 0.607143 | 0.005423 | 2.286201 | 4 | 0.151854 |
| block_VOLUME_CONTRACTION | 35 | 2 | 5 | 0.542857 | 0.000402 | 1.047574 | 3 | 0.014072 |
| block_PRE_RUNUP_OR_ENTRY_UP | 24 | 7 | 11 | 0.583333 | 0.005029 | 2.064256 | 4 | 0.120692 |
| block_PRE_RUNUP_OR_DEAD_RANGE | 20 | 7 | 15 | 0.700000 | 0.008707 | 3.094994 | 2 | 0.174138 |
| block_ENTRY_UP_OR_DEAD_RANGE | 25 | 5 | 12 | 0.640000 | 0.002728 | 1.353624 | 1 | 0.068208 |
| block_CORE_RISK_SET | 16 | 9 | 17 | 0.750000 | 0.010251 | 4.162845 | 1 | 0.164022 |
| block_CORE_RISK_PLUS_VOLUME_CONTRACTION | 15 | 9 | 18 | 0.800000 | 0.011664 | 5.275040 | 1 | 0.174956 |
| block_PRE_RUNUP_AND_ENTRY_UP_ONLY | 39 | 0 | 3 | 0.538462 | 0.000826 | 1.108193 | 3 | 0.032200 |

## Best Candidates

```text
BEST_BY_EXPECTANCY = block_CORE_RISK_PLUS_VOLUME_CONTRACTION
BEST_BY_PF = block_CORE_RISK_PLUS_VOLUME_CONTRACTION
```

Interpretation:
- The experiment is a replay calculation only.
- A high retained result is not approval to change `config.py` or live runtime.
- Missed winners are as important as blocked losers.

## Blocked Trade Samples

### block_CORE_RISK_PLUS_VOLUME_CONTRACTION

| Entry | PnL | Win | Signal | Context | Issues |
| --- | ---: | --- | --- | --- | --- |
| 2026-04-19 20:34 | 0.009724 | True | trend_pullback_reentry | TREND_UP/UNKNOWN/MEDIUM | PRE_RUNUP_30M, SHORT_TERM_CHASE, LARGE_BODY_ENTRY |
| 2026-04-19 22:34 | -0.013200 | False | UNKNOWN | UNKNOWN | PRE_RUNUP_30M, FAST_ADVERSE_MOVE |
| 2026-04-19 23:44 | 0.010692 | True | trend_pullback_reentry | TREND_UP/UNKNOWN/MEDIUM | PRE_RUNUP_30M, SHORT_TERM_CHASE, LARGE_BODY_ENTRY |
| 2026-04-20 04:44 | -0.010934 | False | trend_pullback_reentry | TREND_UP/UNKNOWN/MEDIUM | VOLUME_CONTRACTION, LARGE_BODY_ENTRY |
| 2026-04-20 12:44 | 0.009086 | True | trend_pullback_reentry | TREND_UP/UNKNOWN/MEDIUM | LOW_ENTRY_VOLUME, VOLUME_CONTRACTION, LARGE_BODY_ENTRY, DEAD_RANGE_CANDLE |
| 2026-04-20 16:04 | 0.010868 | True | trend_pullback_reentry | TREND_UP/UNKNOWN/MEDIUM | LOW_ENTRY_VOLUME, VOLUME_CONTRACTION, PRE_RUNUP_30M, LARGE_BODY_ENTRY |
| 2026-04-20 17:34 | -0.011044 | False | trend_up_high_volatility_breakout | TREND_UP/UP/HIGH | PRE_RUNUP_30M, LARGE_BODY_ENTRY |
| 2026-04-20 23:34 | -0.022902 | False | UNKNOWN | UNKNOWN | PRE_RUNUP_30M, FAST_ADVERSE_MOVE |
| 2026-04-21 01:14 | -0.019162 | False | trend_pullback_reentry | TREND_UP/UP/MEDIUM | LARGE_BODY_ENTRY, FAST_ADVERSE_MOVE, ENTRY_UP_CONTEXT |
| 2026-04-21 03:04 | 0.013926 | True | UNKNOWN | UNKNOWN | PRE_RUNUP_30M, SHORT_TERM_CHASE, LARGE_BODY_ENTRY |

## Decision

```text
FILTER_PROMOTION = NO
RUNTIME_STRATEGY_TUNING = HOLD
NEXT_REQUIRED = validate on new post-logging trades
```

## Design Summary

This tool applies candidate context filters to the existing 42 matched closed trades. It computes retained trades, missed winners, blocked losers, win rate, expectancy, profit factor, net PnL, and max consecutive losses. It does not change runtime code, config, order logic, or strategy selection.

## Validation Result

```text
VALIDATION = PASS
INPUT_TRADES = 42
OUTPUT_JSON = reports/cnt_context_filter_experiment_20260426.json
OUTPUT_DOC = docs/CNT_CONTEXT_FILTER_EXPERIMENT_20260426.md
RUNTIME_CODE_CHANGED = NO
CONFIG_CHANGED = NO
```

## Record Text

2026-04-26: Offline context filter experiment was run against the 42-trade exchange-feature dataset. Results are for hypothesis ranking only and must be validated on new post-logging trades before any runtime use.

Related:
- [[CNT_ALL_TRADE_WIN_LOSS_FEATURE_DECOMPOSITION_20260426]]
- [[CNT_EXCHANGE_REPLAY_MARKET_CONTEXT_REVIEW_20260426]]
- [[CNT_MARKET_CONTEXT_LOGGING_LAYER_IMPLEMENTATION_20260426]]

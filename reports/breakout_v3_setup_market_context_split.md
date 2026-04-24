---
title: breakout_v3_setup_market_context_split
status: completed
generated_at: 2026-04-24T13:33:02+09:00
---

# Breakout V3 Setup Market Context Split

## Scope

- strategy: `breakout_v3`
- mode: `shadow-only`
- activation: `forbidden`
- tuning: `forbidden`

## Baseline

- snapshot signal_count: `44`
- event log count: `44`
- market context split uses event-level shadow log data

## Core Facts

| key | value |
|---|---:|
| total_event_count | 44 |
| setup_fail_count | 40 |
| setup_pass_count | 4 |
| market_not_trend_up_count | 20 |
| setup_fail_and_market_not_trend_up_count | 20 |
| setup_fail_but_market_trend_up_count | 3 |
| allowed_market_context_count | 2 |
| setup_pass_blocked_market_context_count | 2 |

## Allowed Event Market Context

| key | value |
|---|---:|
| TREND_UP_PASS | 1 |
| RANGE_BIAS_PASS | 1 |

## Setup Pass But Blocked Market Context

| key | value |
|---|---:|
| RANGE_BIAS_PASS | 1 |
| TREND_UP_PASS | 2 |

## breakout_not_confirmed Market Context

| key | value |
|---|---:|
| RANGE_BIAS_PASS | 1 |
| TREND_UP_PASS | 2 |

## Layer Combination Market Context Distribution TOP 10

### VOLATILITY_LAYER + PARTICIPATION_LAYER + POSITION_LAYER + SETUP_STATE_LAYER

| key | value |
|---|---:|
| RANGE_BIAS_PASS | 14 |
| MARKET_NOT_TREND_UP | 12 |
| TREND_UP_PASS | 2 |

### VOLATILITY_LAYER + POSITION_LAYER + SETUP_STATE_LAYER

| key | value |
|---|---:|
| MARKET_NOT_TREND_UP | 5 |
| RANGE_BIAS_PASS | 2 |
| TREND_UP_PASS | 1 |

### VOLATILITY_LAYER + PARTICIPATION_LAYER

| key | value |
|---|---:|
| TREND_UP_PASS | 2 |
| RANGE_BIAS_PASS | 1 |

### VOLATILITY_LAYER + PARTICIPATION_LAYER + SETUP_STATE_LAYER

| key | value |
|---|---:|
| MARKET_NOT_TREND_UP | 3 |

### VOLATILITY_LAYER + POSITION_LAYER

| key | value |
|---|---:|
| TREND_UP_PASS | 1 |

### VOLATILITY_LAYER + SETUP_STATE_LAYER

| key | value |
|---|---:|
| RANGE_BIAS_PASS | 1 |

## Interpretation

- `market_not_trend_up` appears `20` times.
- `setup_fail + market_not_trend_up` appears `20` times.
- `setup_fail + trend_up_pass` still appears `3` times.
- breakout-not-confirmed market context = `RANGE_BIAS_PASS=1, TREND_UP_PASS=2`.

## Final Judgement

`breakout_v3` setup cluster is not only a non-trend regime problem. Setup pressure still survives after trend-up passes, which means the bottleneck is partly market-context-driven and partly intrinsic to the setup layer itself.

## Obsidian Links

- [[CNT v2 BREAKOUT V3 SETUP BOTTLENECK ISOLATION REPORT]]

---
title: breakout_v3_setup_bottleneck_report
status: completed
generated_at: 2026-04-24T13:12:05+09:00
---

# Breakout V3 Setup Bottleneck Report

## Scope

- strategy: `breakout_v3`
- mode: `shadow-only`
- activation: `forbidden`
- tuning: `forbidden`

## Baseline Note

- instruction baseline snapshot signal_count: `42`
- actual log event count at execution time: `42`
- current snapshot signal_count: `42`

## Core Facts

| key | value |
|---|---:|
| total_signal_count | 42 |
| allowed_signal_count | 2 |
| allowed_signal_ratio | 0.047619 |
| setup_pass_count | 4 |
| setup_fail_count | 38 |
| top_setup_fail_reason | vwap_distance_fail |
| allowed_trace_count | 2 |
| setup_pass_blocked_trace_count | 3 |

## Stage Pass Counts

| key | value |
|---|---:|
| regime | 24 |
| quality | 12 |
| trigger | 11 |
| setup | 4 |

## Stage Fail Counts

| key | value |
|---|---:|
| setup | 38 |
| trigger | 31 |
| quality | 30 |
| regime | 18 |

## Setup Stage Internal Fail Counts

| key | value |
|---|---:|
| setup_not_ready | 38 |
| volatility_floor_fail | 29 |
| price_position_fail | 21 |

## Requested Setup Bottleneck Counts

| key | value |
|---|---:|
| vwap_distance_fail | 35 |
| band_width_fail | 34 |
| volume_fail | 33 |
| band_expansion_fail | 31 |
| setup_not_ready | 19 |

## First Blocker Distribution

| key | value |
|---|---:|
| setup_not_ready | 19 |
| market_not_trend_up | 18 |
| breakout_not_confirmed | 3 |

## Secondary Fail Reasons Distribution

| key | value |
|---|---:|
| vwap_distance_fail | 35 |
| band_width_fail | 34 |
| volume_fail | 33 |
| band_expansion_fail | 31 |
| rsi_threshold_fail | 23 |
| ema_fail | 21 |

## Allowed Event Trace Files

- `reports\breakout_v3_allowed_trace.json`
- count: `2`

## Setup Pass But Blocked Trace Files

- `reports\breakout_v3_setup_pass_blocked_trace.json`
- count: `3`

## Interpretation

- setup is the main stage bottleneck by fail count: `38`
- setup pass remains rare: `4 / 42`
- among requested bottleneck keys, the dominant failure is `vwap_distance_fail`
- allowed events were extracted as full raw traces without any tuning or activation change

## Final Judgement

`breakout_v3` is not dead, but it is still passing through a narrow setup-layer bottleneck. The next valid phase is setup bottleneck isolation based on trace evidence, not tuning or activation.

## Obsidian Links

- [[CNT v2 BREAKOUT V3 FIRST SHADOW OBSERVATION REVIEW]]

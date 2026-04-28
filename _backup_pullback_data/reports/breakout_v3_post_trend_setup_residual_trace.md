---
title: breakout_v3_post_trend_setup_residual_trace
status: completed
generated_at: 2026-04-24T13:39:14+09:00
---

# Breakout V3 Post-Trend Setup Residual Trace

## Scope

- strategy: `breakout_v3`
- mode: `shadow-only`
- activation: `forbidden`
- tuning: `forbidden`

## Baseline

- snapshot signal_count: `45`
- event log count: `45`

## Core Facts

| key | value |
|---|---:|
| post_trend_setup_fail_count | 3 |
| setup_pass_breakout_blocked_count | 3 |
| allowed_count | 2 |
| common_layer_between_blocked_groups | VOLATILITY_LAYER |
| common_condition_between_blocked_groups | none |
| allowed_difference_summary | blocked groups share band_expansion_fail, volume_fail while allowed traces do not |

## Group A: trend_up_pass=true + setup_fail=true

| key | value |
|---|---:|
| common_layers | POSITION_LAYER, SETUP_STATE_LAYER, VOLATILITY_LAYER |
| common_conditions | band_width_fail, price_position_fail, setup_not_ready, vwap_distance_fail |

## Group B: setup_pass=true + allowed=false + breakout_not_confirmed

| key | value |
|---|---:|
| common_layers | PARTICIPATION_LAYER, VOLATILITY_LAYER |
| common_conditions | band_expansion_fail, volume_fail |

## Allowed Group

| key | value |
|---|---:|
| common_layers | VOLATILITY_LAYER |
| common_conditions | band_width_fail |

## breakout_confirmed Candidate Conditions

| key | value |
|---|---:|
| band_expansion_fail | 5 |
| volume_fail | 5 |

## Interpretation

- post-trend residual setup failures count = `3`
- setup-pass breakout-blocked count = `3`
- common layer overlap between both blocked groups = `VOLATILITY_LAYER`
- common condition overlap between both blocked groups = `none`
- allowed difference summary = `blocked groups share band_expansion_fail, volume_fail while allowed traces do not`

## Final Judgement

`breakout_v3` still shows a shared blocked root after trend-up. The residual setup-fail group and the breakout-not-confirmed group overlap structurally, which suggests that post-trend setup pressure and breakout confirmation failure are related rather than fully separate problems.

## Obsidian Links

- [[CNT v2 BREAKOUT V3 SETUP BOTTLENECK ISOLATION REPORT]]

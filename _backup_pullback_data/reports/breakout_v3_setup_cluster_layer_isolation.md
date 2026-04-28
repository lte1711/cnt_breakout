---
title: breakout_v3_setup_cluster_layer_isolation
status: completed
generated_at: 2026-04-24T13:29:56+09:00
---

# Breakout V3 Setup Cluster Layer Isolation

## Scope

- strategy: `breakout_v3`
- mode: `shadow-only`
- activation: `forbidden`
- tuning: `forbidden`

## Baseline

- snapshot signal_count: `44`
- event log count: `44`
- layer analysis uses event-level shadow log data

## Core Facts

| key | value |
|---|---:|
| total_event_count | 44 |
| setup_fail_count | 40 |
| setup_pass_count | 4 |
| top_layer_combination | VOLATILITY_LAYER + PARTICIPATION_LAYER + POSITION_LAYER + SETUP_STATE_LAYER |
| top_layer_combination_count | 28 |
| volatility_layer_fail_count | 44 |
| participation_layer_fail_count | 34 |
| position_layer_fail_count | 37 |
| setup_state_layer_fail_count | 40 |
| triple_layer_failure_count | 28 |
| allowed_layer_combination_count | 2 |
| setup_pass_blocked_count | 3 |

## Layer Combination TOP 10

| key | value |
|---|---:|
| VOLATILITY_LAYER + PARTICIPATION_LAYER + POSITION_LAYER + SETUP_STATE_LAYER | 28 |
| VOLATILITY_LAYER + POSITION_LAYER + SETUP_STATE_LAYER | 8 |
| VOLATILITY_LAYER + PARTICIPATION_LAYER | 3 |
| VOLATILITY_LAYER + PARTICIPATION_LAYER + SETUP_STATE_LAYER | 3 |
| VOLATILITY_LAYER + POSITION_LAYER | 1 |
| VOLATILITY_LAYER + SETUP_STATE_LAYER | 1 |

## Allowed Event Layer Combinations

| key | value |
|---|---:|
| VOLATILITY_LAYER + POSITION_LAYER | 1 |
| VOLATILITY_LAYER + SETUP_STATE_LAYER | 1 |

## Setup Pass But Blocked Layer Combinations

| key | value |
|---|---:|
| VOLATILITY_LAYER + PARTICIPATION_LAYER | 3 |

## breakout_not_confirmed Common Layers

| key | value |
|---|---:|
| VOLATILITY_LAYER | 3 |
| PARTICIPATION_LAYER | 3 |

## Interpretation

- The dominant layer combination is `VOLATILITY_LAYER + PARTICIPATION_LAYER + POSITION_LAYER + SETUP_STATE_LAYER` with `28` events.
- VOLATILITY + PARTICIPATION + POSITION simultaneous failure appears `28` times.
- Allowed events span `2` layer combinations.
- Setup-pass-but-blocked events remain `3` and all current blockers are `breakout_not_confirmed`.

## Final Judgement

`breakout_v3` setup pressure is primarily a layered cluster problem. Failures are not isolated to one condition name; they cluster across volatility, participation, position, and setup-state layers.

## Obsidian Links

- [[CNT v2 BREAKOUT V3 SETUP BOTTLENECK ISOLATION REPORT]]

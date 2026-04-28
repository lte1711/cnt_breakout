---
title: breakout_v3_setup_root_cause_matrix
status: completed
generated_at: 2026-04-24T13:27:15+09:00
---

# Breakout V3 Setup Root Cause Matrix

## Scope

- strategy: `breakout_v3`
- mode: `shadow-only`
- activation: `forbidden`
- tuning: `forbidden`

## Baseline

- snapshot signal_count: `44`
- event log count: `44`
- matrix analysis uses event log data to preserve event-level combinations

## Core Facts

| key | value |
|---|---:|
| setup_fail_count | 40 |
| setup_pass_count | 4 |
| allowed_count | 2 |
| setup_pass_blocked_count | 3 |
| top_fail_combination | band_expansion_fail + band_width_fail + setup_not_ready + volatility_floor_fail + volume_fail + vwap_distance_fail |
| top_fail_combination_count | 9 |
| single_dominant_blocker | False |
| multi_condition_failure_detected | True |
| triple_requested_simultaneous_fail_count | 25 |

## Fail Condition Combination TOP 10

| key | value |
|---|---:|
| band_expansion_fail + band_width_fail + setup_not_ready + volatility_floor_fail + volume_fail + vwap_distance_fail | 9 |
| band_width_fail + price_position_fail + setup_not_ready + volatility_floor_fail + volume_fail + vwap_distance_fail | 5 |
| band_expansion_fail + band_width_fail + price_position_fail + setup_not_ready + volatility_floor_fail + volume_fail + vwap_distance_fail | 5 |
| band_expansion_fail + band_width_fail + price_position_fail + setup_not_ready + volume_fail + vwap_distance_fail | 4 |
| band_expansion_fail + band_width_fail + setup_not_ready + volatility_floor_fail + vwap_distance_fail | 2 |
| band_width_fail + price_position_fail + setup_not_ready + vwap_distance_fail | 2 |
| band_expansion_fail + band_width_fail + setup_not_ready + volume_fail + vwap_distance_fail | 2 |
| band_width_fail + setup_not_ready + volatility_floor_fail + volume_fail | 1 |
| band_width_fail + setup_not_ready + volatility_floor_fail | 1 |
| band_expansion_fail + band_width_fail + price_position_fail + setup_not_ready + volatility_floor_fail + vwap_distance_fail | 1 |

## Allowed Event Combinations

| key | value |
|---|---:|
| band_expansion_fail + band_width_fail + vwap_distance_fail | 1 |
| band_width_fail + setup_not_ready + volatility_floor_fail | 1 |

## Setup Pass But Blocked Reasons

| key | value |
|---|---:|
| breakout_not_confirmed | 3 |

## Interpretation

- The top setup-fail combination is `band_expansion_fail + band_width_fail + setup_not_ready + volatility_floor_fail + volume_fail + vwap_distance_fail` with `9` events.
- Multi-condition simultaneous failure detected: `True`.
- The requested triple failure (`vwap_distance_fail + band_width_fail + volume_fail`) appears `25` times.
- Allowed events contain `2` distinct setup-related combinations.
- Setup-pass-but-blocked events remain `3`, and their blockers are dominated by `breakout_not_confirmed`.

## Final Judgement

`breakout_v3` setup pressure is not a single independent failure. It is primarily a simultaneous failure structure, with repeated multi-condition combinations clustering around setup and requested quality-side conditions.

## Obsidian Links

- [[CNT v2 BREAKOUT V3 SETUP BOTTLENECK ISOLATION REPORT]]

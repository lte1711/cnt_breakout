---
tags:
  - cnt
  - type/documentation
  - status/active
  - strategy/breakout_v3
  - type/analysis
  - status/completed
---

# CNT v2 BREAKOUT V3 Setup Bottleneck Isolation Report

## Objective

Lock the current `breakout_v3` setup bottleneck as facts and traces rather than intuition.

## Source

- `data/shadow_breakout_v3_snapshot.json`
- `logs/shadow_breakout_v3.jsonl`
- `reports/breakout_v3_setup_bottleneck_report.md`
- `reports/breakout_v3_allowed_trace.json`
- `reports/breakout_v3_setup_pass_blocked_trace.json`

## Core Facts

| item | value |
|---|---:|
| total_signal_count | 42 |
| allowed_signal_count | 2 |
| allowed_signal_ratio | 0.047619 |
| setup_pass_count | 4 |
| setup_fail_count | 38 |
| setup_pass_blocked_trace_count | 3 |
| allowed_trace_count | 2 |

## Stage Interpretation

- `regime_pass = 24 / 42`
- `setup_pass = 4 / 42`
- `trigger_pass = 11 / 42`
- `quality_pass = 12 / 42`

The dominant stage bottleneck is `setup`, not `trigger`.

## Setup Bottleneck Focus

### Setup Stage Internal Fail Counts

| condition | count |
|---|---:|
| setup_not_ready | 38 |
| volatility_floor_fail | 29 |
| price_position_fail | 21 |

### Requested Bottleneck Keys

| condition | count |
|---|---:|
| vwap_distance_fail | 35 |
| band_width_fail | 34 |
| volume_fail | 33 |
| band_expansion_fail | 31 |
| setup_not_ready | 19 |

## Allowed Trace Interpretation

The allowed trace count is not large enough for activation judgement.

What it proves:
- `breakout_v3` is not dead
- the structure can pass hard and soft conditions in a narrow subset

What it does not prove:
- repeatable edge
- activation readiness
- tuning readiness

## Setup Pass But Blocked Interpretation

`setup_pass = 4`, but `allowed = 2`.

That means the setup bottleneck is severe, and even after setup passes, there are still blocked cases that require trace review.

## Final Judgement

`breakout_v3` is partially alive, but the current structure is still constrained by a narrow setup-layer bottleneck. The next valid phase is setup bottleneck isolation, not activation and not tuning.

## Official Status Lock

```text
FINAL_JUDGEMENT = PARTIALLY_ALIVE_BUT_SETUP_CONSTRAINED
ACTIVATION_READY = NO
TUNING_READY = NO
NEXT_PHASE = CONTINUE_SETUP_BOTTLENECK_ISOLATION
```

## Required Next Phase

- keep `breakout_v3 = SHADOW_ONLY`
- keep `activation = FORBIDDEN`
- keep `tuning = FORBIDDEN`
- use trace evidence to isolate setup-layer pressure before any redesign discussion

## Obsidian Links

- [[CNT v2 BREAKOUT V3 FIRST SHADOW OBSERVATION REVIEW]]
- [[CNT v2 DASHBOARD SETUP BOTTLENECK ISOLATION UPGRADE REPORT]]

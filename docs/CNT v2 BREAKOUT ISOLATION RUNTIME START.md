---
tags:
  - cnt
  - breakout
  - isolation
  - runtime
---

# CNT v2 BREAKOUT ISOLATION RUNTIME START

## Purpose

This document starts the breakout isolation runtime window after the dashboard warning patch and gate/display consistency patch were applied.

The goal is not to disable `breakout_v1` immediately.
The goal is to observe whether breakout remains a negative contributor under the current runtime while keeping the rest of the system unchanged.

## Observation Start

- Baseline commit: `be75061`
- Isolation runtime start time: `2026-04-22 13:40:36`
- Start label: `STRUCTURALLY_HEALTHY, PERFORMANCE_DEGRADED`
- Start gate: `FAIL / NON_POSITIVE_EXPECTANCY`
- Observation start snapshot: `2026-04-22 12:44:03`

## Start Baseline Metrics

- mixed portfolio observed
  - `expectancy = -0.0007807916666668097`
  - `profit_factor = 0.9158659890090017`
  - `execution_rate = 24 / 86 = 27.91%`
  - `execution_block_rate = 62 / 86 = 72.09%`
  - `no_candidate_rate = 244 / 330 = 73.94%`
- breakout observed baseline
  - `trades_closed = 3`
  - `expectancy = -0.022197999999999656`
  - `profit_factor = 0.17295081967214201`
- pullback inferred baseline
  - `trades_closed = 21`
  - `expectancy = 0.0022788095238093107`
  - `profit_factor = 1.3365141201619735`

## Comparison Axes

The runtime review must keep these three views separate:

1. `mixed portfolio`
2. `breakout observed baseline`
3. `pullback inferred baseline`

Important:
- `mixed portfolio` is observed
- `breakout observed baseline` is observed
- `pullback inferred baseline` is inferred from strategy metrics and must not be described as observed portfolio runtime

## Metrics To Track

- expectancy
- profit_factor
- execution_rate
- execution_block_rate
- no_candidate_rate

## Midpoint Check

- midpoint review after `10 additional cycles`
- confirm whether:
  - breakout expectancy is still negative
  - mixed portfolio expectancy is recovering or degrading
  - execution throughput is improving or staying blocked

## End Conditions

End the isolation window with one of the following conclusions only:

1. `breakout quality recover`
2. `breakout remains negative`
3. `insufficient sample`

## Low-Sample Warning

`breakout_v1` still has a low observed sample count.
Do not overstate any conclusion from a small number of added trades.

## Required Reporting Rule

All post-window reporting must preserve:

- the original `LIVE_READY` record
- the current `FAIL / NON_POSITIVE_EXPECTANCY` record
- the difference between observed and inferred baselines

## Obsidian Links

- [[CNT v2 POST-READY DEGRADATION REVIEW]]
- [[CNT v2 BREAKOUT LAST 3 TRADES REVIEW]]
- [[CNT v2 STRATEGY ISOLATION COMPARISON]]
- [[CNT v2 DASHBOARD PATCH TARGET MAPPING]]
- [[CNT v2 GATE DISPLAY ACTUAL PATCH SPEC]]

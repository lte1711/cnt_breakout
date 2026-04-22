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

- Start label: `STRUCTURALLY_HEALTHY, PERFORMANCE_DEGRADED`
- Start gate: `FAIL / NON_POSITIVE_EXPECTANCY`
- Observation start snapshot: `2026-04-22 12:44:03`

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

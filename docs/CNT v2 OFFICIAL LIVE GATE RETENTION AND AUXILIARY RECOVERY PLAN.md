---
title: CNT v2 OFFICIAL LIVE GATE RETENTION AND AUXILIARY RECOVERY PLAN
status: FINAL
language: en
updated: 2026-04-24
tags:
  - cnt
  - gate
  - recovery
  - pullback_v1
  - breakout_v1
  - observation
---

# CNT v2 OFFICIAL LIVE GATE RETENTION AND AUXILIARY RECOVERY PLAN

## Decision

The official CNT live gate must remain unchanged at the current stage.

The next valid change target is **not** the gate condition itself.  
The valid next step is to add and use an **auxiliary recovery evaluation layer** that interprets the current runtime recovery state separately from the historical `breakout_v1` contamination still embedded in the portfolio-wide snapshot.

## Current Gate Rule

The official live gate remains:

1. `closed_trades >= 20`
2. `expectancy > 0`
3. `net_pnl > 0`
4. `max_consecutive_losses <= 5`
5. `risk_guard_observed`

The gate is still evaluated by `src/validation/live_gate_evaluator.py`.

## Why The Gate Should Not Be Modified Now

Current `data/performance_snapshot.json` still contains historical negative contribution from `breakout_v1`.

At report time:

- `closed_trades = 35`
- `expectancy = -0.0003352571428572645`
- `net_pnl = -0.011734000000004186`
- `max_consecutive_losses = 3`
- `risk_trigger_stats.DAILY_LOSS_LIMIT = 348`

This means:

- sample size is sufficient
- risk guard observation exists
- max consecutive losses are still within the allowed range
- the portfolio-level gate fails because historical performance contamination is still present in the aggregate snapshot

Changing the official gate now would blur the difference between:

- real operational recovery
- gate relaxation
- historical contamination still present in the denominator

## Auxiliary Recovery Evaluation Layer

The auxiliary layer is a **secondary interpretation framework**, not a replacement for the official gate.

Its purpose is:

1. keep the official gate conservative
2. avoid rewriting readiness rules during an active observation phase
3. evaluate whether the current post-isolation runtime is stabilizing
4. separate present recovery observation from historical `breakout_v1` damage

## Auxiliary Evaluation Scope

The auxiliary recovery layer should focus on the current post-isolation operating reality:

- `pullback_v1` is the only active live runtime strategy
- `breakout_v1` remains isolated from the active set
- `breakout_v3` remains shadow-only
- portfolio risk synchronization is already fixed
- shadow semantics are already rebaselined and clean

## Auxiliary Evaluation Inputs

The auxiliary layer should use the following artifacts as evidence:

- `data/state.json`
- `data/portfolio_state.json`
- `data/performance_snapshot.json`
- `data/live_gate_decision.json`
- `data/shadow_breakout_v3_snapshot.json`
- `logs/runtime.log`
- `logs/signal.log`

## Auxiliary Recovery Questions

The auxiliary layer should answer the following questions:

1. Is the active runtime still `pullback_v1` only?
2. Are risk counters synchronized between `state.json` and `portfolio_state.json`?
3. Is `breakout_v3` shadow data still semantically clean?
4. Is the post-isolation runtime accumulating observation data without new structural regressions?
5. Is current performance behavior improving even if the official gate is still negative due to historical contamination?

## What The Auxiliary Layer Must Not Do

The auxiliary layer must not:

- change the official live gate
- override `data/live_gate_decision.json`
- activate `breakout_v3`
- reactivate `breakout_v1`
- relax thresholds
- reinterpret historical negative results as if they disappeared

## Operational Interpretation

Until the aggregate portfolio snapshot naturally recovers, the correct interpretation is:

- official gate: still authoritative
- auxiliary layer: explanatory only

This means CNT may remain:

- `official live gate = FAIL`
- `auxiliary recovery status = improving / stable / needs review`

at the same time.

That is valid and expected during a post-isolation recovery window.

## Immediate Next Step

The immediate next step is to operate with this dual interpretation:

- keep the official gate unchanged
- continue the pullback-only observation window
- continue breakout_v3 shadow observation
- document post-isolation recovery through an auxiliary recovery review, not by modifying the official gate rule

## Conclusion

The correct next-phase direction is:

- **retain the official live gate as-is**
- **introduce and use an auxiliary recovery evaluation layer for post-isolation interpretation**

This preserves conservative operational discipline while still allowing accurate recovery tracking.

## Obsidian Links

- [[CNT v2 LIVE READINESS GATE]]
- [[CNT v2 LIVE GATE ALIGNMENT REPORT]]
- [[CNT v2 BREAKOUT V1 ACTIVE ISOLATION DECISION]]
- [[CNT v2 PULLBACK-ONLY OBSERVATION WINDOW EXECUTION REPORT]]
- [[CNT v2 BREAKOUT V3 SHADOW OUTPUT REBASELINE REPORT]]
- [[00 Docs Index|Docs Index]]

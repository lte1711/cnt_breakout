---
aliases:
  - CNT v2 LIVE READY POST-READINESS MONITORING PLAN
---

# CNT v2 LIVE READY POST-READINESS MONITORING PLAN

## Classification

This document is the **fact-based post-readiness operating plan** for CNT after `LIVE_READY` was reached.

It defines the baseline metrics that must remain visible while the system stays in live-ready monitoring mode.

## Baseline Snapshot

Baseline source:

- `data/performance_snapshot.json`
- `data/live_gate_decision.json`

Baseline timestamp:

- `2026-04-22 02:44:03`

Baseline gate decision:

- `LIVE_READY`
- `ALL_GATES_PASSED`

## Fixed Baseline Metrics

- `closed_trades = 21`
- `executed_trades = 22`
- `selected_signals = 62`
- `total_signals = 558`
- `win_rate = 0.5714285714285714`
- `expectancy = 0.0013191904761903238`
- `net_pnl = 0.027702999999996814`
- `profit_factor = 1.196938891574459`
- `selection_rate = 62 / 558 = 11.11%`
- `execution_rate = 22 / 62 = 35.48%`
- `no_ranked_signal_total = 192 + 25 = 217`

Strategy split baseline:

- `pullback_v1 signals_selected = 57`
- `breakout_v1 signals_selected = 5`
- `pullback_share = 91.94%`
- `breakout_share = 8.06%`

## Monitoring Window

The next monitoring window is:

- `20 to 30 additional cycles`

No runtime parameter change should be made during this window unless a separate design and validation record explicitly approves it.

## Primary Tracking Metrics

The following must be tracked continuously:

1. `selection_rate`
2. `execution_rate`
3. `no_ranked_signal`
4. `strategy_split`
5. `LIVE_READY` persistence
6. `profit_factor`
7. `expectancy`

## Interpretation Rule

During this phase, CNT should be interpreted as:

- `LIVE_READY`
- but still throughput-constrained
- and still requiring operating quality stabilization

This means:

- `LIVE_READY` does not mean "fully optimized"
- `LIVE_READY` does mean that minimum readiness gates are satisfied
- the next question is whether the same quality persists under continued runtime evidence

## No-Change Window

The following are frozen during the post-readiness observation window:

- no risk guard loosening
- no new filter loosening
- no symbol expansion
- no multi-position expansion
- no ranker retuning

## Next Review Triggers

Escalate to the next design review if any of the following occur:

1. `profit_factor < 1.1` in repeated snapshots
2. `expectancy <= 0`
3. `LIVE_READY` is lost
4. `breakout_v1 trades_closed >= 5`
5. `no_ranked_signal` changes materially upward or downward

## One-Line Operating Rule

**CNT is now in post-readiness stabilization. Keep configuration fixed, track baseline deltas, and judge persistence before any new optimization step.**

## Obsidian Links

- [[CNT v2 LIVE READINESS GATE]]


---
aliases:
  - CNT v2 POST-READY DEGRADATION REVIEW
---

# CNT v2 POST-READY DEGRADATION REVIEW

## Classification

This document is a fact-based degradation review written after CNT reached `LIVE_READY` and then fell back to `FAIL`.

## Current Label

`STRUCTURALLY_HEALTHY, PERFORMANCE_DEGRADED`

## Current Fail State

Latest verified sources:

- `data/performance_snapshot.json`
- `data/strategy_metrics.json`
- `data/live_gate_decision.json`

Current gate result:

- `status = FAIL`
- `reason = NON_POSITIVE_EXPECTANCY`

Current snapshot at review time:

- `timestamp = 2026-04-22 12:44:03`
- `closed_trades = 24`
- `selected_signals = 86`
- `executed_trades = 24`
- `win_rate = 0.5416666666666666`
- `expectancy = -0.0007807916666668097`
- `net_pnl = -0.018739000000003447`
- `profit_factor = 0.9158659890090017`

## Why This Is Not A Structural Failure

The current `FAIL` state is not explained by engine malfunction.

Still working correctly:

- state persistence
- runtime logging
- strategy selection
- execution counting
- performance snapshot generation
- live gate evaluation

So the current issue is not an orchestration failure.

It is a **performance deterioration** problem.

## Breakout Negative Contribution

`breakout_v1` current observed quality:

- `trades_closed = 3`
- `wins = 1`
- `losses = 2`
- `expectancy = -0.022197999999999656`
- `profit_factor = 0.17295081967214201`
- `gross_profit = 0.01392600000000084`
- `gross_loss = 0.0805199999999998`
- `net_pnl = -0.06659399999999896`

Contribution interpretation:

- breakout accounts for only `3 / 24 = 12.5%` of closed trades
- but its standalone net contribution is `-0.066594`
- the mixed portfolio net is only `-0.018739`

This means breakout losses were large enough to erase pullback's positive edge and push the combined portfolio below zero expectancy.

## Pullback Positive Standalone Quality

`pullback_v1` current standalone quality remains positive:

- `trades_closed = 21`
- `wins = 12`
- `losses = 9`
- `expectancy = 0.0022788095238093107`
- `profit_factor = 1.3365141201619735`
- `gross_profit = 0.19006300000000023`
- `gross_loss = 0.14220800000000472`
- `inferred_net_pnl = +0.04785499999999551`

Interpretation:

- pullback remains viable on its own
- the current combined `FAIL` is not evidence that pullback quality collapsed
- the degradation is dominated by portfolio mixing with a low-quality breakout sample

## Throughput Weakness

Current throughput remains weak even after `LIVE_READY` was reached:

- `selection_rate = 86 / 660 = 13.03%`
- `execution_rate = 24 / 86 = 27.91%`

Blocked-signal evidence:

- `DAILY_LOSS_LIMIT = 62`
- `no_ranked_signal = 219 + 25 = 244`

Derived operating pressure:

- `execution_block_rate = 62 / 86 = 72.09%`
- `no_candidate_rate = 244 / 330 = 73.94%`

This means the system is not only suffering from weak portfolio quality, but also from limited throughput.

## Risk Block Pressure

Observed protection pressure remains high:

- `risk_trigger_stats.DAILY_LOSS_LIMIT = 124`
- `state.risk_metrics.daily_loss_count = 3`
- `state.risk_metrics.consecutive_losses = 2`

Interpretation:

- the risk layer is still active for valid reasons
- this should not be treated as a bug
- it is a sign that recent trade quality has not been stable enough

## Final Review Statement

Current phase should be interpreted as:

- structurally healthy
- not ready for further loosening
- requiring separated quality diagnosis

## Required Conclusion

**portfolio quality degraded but structurally healthy**

## Obsidian Links

- [[CNT v2 BREAKOUT LAST 3 TRADES REVIEW]]


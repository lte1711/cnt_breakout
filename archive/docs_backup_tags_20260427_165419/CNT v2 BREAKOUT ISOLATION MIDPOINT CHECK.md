---
---

# CNT v2 BREAKOUT ISOLATION MIDPOINT CHECK

## Current Check Position

- baseline commit: `be75061`
- isolation runtime start commit: `e27f3b9`
- isolation runtime start time: `2026-04-22 13:40:36`
- midpoint target: `10 additional cycles`
- currently observed additional cycles: `6`
- current snapshot timestamp: `2026-04-22 13:44:03`

## Midpoint Label

- current label: `STRUCTURALLY_HEALTHY, PERFORMANCE_DEGRADED`
- current gate: `FAIL / NON_POSITIVE_EXPECTANCY`
- midpoint status: `insufficient sample`

## Baseline Versus Current

### Mixed Portfolio Observed

- baseline
  - `expectancy = -0.0007807916666668097`
  - `profit_factor = 0.9158659890090017`
  - `execution_rate = 24 / 86 = 27.91%`
  - `execution_block_rate = 62 / 86 = 72.09%`
  - `no_candidate_rate = 244 / 330 = 73.94%`

- current
  - `expectancy = -0.0007807916666668097`
  - `profit_factor = 0.9158659890090017`
  - `execution_rate = 24 / 90 = 26.67%`
  - `execution_block_rate = 66 / 90 = 73.33%`
  - `no_candidate_rate = 246 / 336 = 73.21%`

- delta
  - `expectancy delta = 0.000000`
  - `profit_factor delta = 0.000`
  - `execution_rate delta = -1.24 pts`
  - `execution_block_rate delta = +1.24 pts`
  - `no_candidate_rate delta = -0.73 pts`

### Breakout Observed Baseline

- baseline
  - `trades_closed = 3`
  - `expectancy = -0.022197999999999656`
  - `profit_factor = 0.17295081967214201`

- current
  - `trades_closed = 3`
  - `expectancy = -0.022197999999999656`
  - `profit_factor = 0.17295081967214201`

- delta
  - `trades_closed delta = 0`
  - `expectancy delta = 0.000000`
  - `profit_factor delta = 0.000`

### Pullback Inferred Baseline

- baseline
  - `trades_closed = 21`
  - `expectancy = 0.0022788095238093107`
  - `profit_factor = 1.3365141201619735`

- current
  - `trades_closed = 21`
  - `expectancy = 0.0022788095238093107`
  - `profit_factor = 1.3365141201619735`

- delta
  - `trades_closed delta = 0`
  - `expectancy delta = 0.000000`
  - `profit_factor delta = 0.000`

## Throughput And Block Pressure

- selection rate current
  - `90 / 672 = 13.39%`
- execution rate current
  - `24 / 90 = 26.67%`
- execution block pressure current
  - `66 / 90 = 73.33%`
- no candidate pressure current
  - `246 / 336 = 73.21%`

Interpretation:

- mixed expectancy and PF have not recovered yet
- breakout observed quality has not improved yet
- execution throughput is slightly weaker than the baseline
- no candidate pressure is still high

## Low-Sample Warning

This is not a full midpoint completion.
Only `6` additional cycles have been observed against a `10-cycle` midpoint target.

`breakout_v1` is still low-sample.
No strong conclusion should be drawn from unchanged breakout observed metrics at this point.

## Push Status

- `be75061` push status: not pushed yet
- `e27f3b9` push status: not pushed yet
- local branch status at check time: `ahead of origin/main by 2 commits`

## Midpoint Conclusion

- `insufficient sample`

## Obsidian Links

- [[CNT v2 BREAKOUT QUALITY EVALUATION REPORT]]


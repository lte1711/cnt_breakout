---
---

# CNT v2 BREAKOUT V2 VALIDATION WINDOW START

## Status

- validation window started
- `breakout_v2` is still **not** in `ACTIVE_STRATEGIES`
- production switch is prohibited at this stage

## Start Timestamp

- validation start timestamp: `2026-04-22 14:52:46`

## Baseline Reference

### Breakout_v1 Final Reference

- isolation final review:
  - CNT v2 BREAKOUT ISOLATION FINAL REVIEW
- observed baseline
  - `trades_closed = 3`
  - `expectancy = -0.022197999999999656`
  - `profit_factor = 0.17295081967214201`

### Mixed Portfolio Reference

- snapshot timestamp: `2026-04-22 14:44:04`
- `closed_trades = 24`
- `expectancy = -0.0007807916666668097`
- `profit_factor = 0.9158659890090017`
- `net_pnl = -0.018739000000003447`

### Pullback Reference

- reference type: `inferred`
- `trades_closed = 21`
- `expectancy = 0.0022788095238093107`
- `profit_factor = 1.3365141201619735`

## Comparison Arms

- `A arm = breakout_v1 reference baseline`
- `B arm = breakout_v2 candidate`

## Validation Metrics

The validation window must track:

- `trades_closed`
- `expectancy`
- `profit_factor`
- `net_pnl`
- `win_rate`
- `execution_rate`
- `filtered_signal_ratio`
- `stop_exit_ratio`

## Breakout_v2 Mode

- `BREAKOUT_V2_MODE = off`

Meaning:

- strategy is implemented
- strategy is registered
- strategy is **not** active in production runtime
- candidate validation must start through a later controlled or shadow-style step, not direct production insertion

## Promotion Gate

Promotion review may begin only if:

- minimum sample reached
- `expectancy > 0`
- `profit_factor > 1`
- no severe regression
- no structural or logging issue

## Rejection Gate

Reject for now if:

- sample remains insufficient
- `expectancy <= 0`
- `profit_factor <= 1`
- stop exit pressure remains dominant
- runtime or logging integrity degrades

## Operational Rule

- do not activate `breakout_v2` immediately
- do not remove `breakout_v1`
- do not relax risk guard
- do not change KPI calculation logic

## Obsidian Links

- [[CNT v2 BREAKOUT V2 DESIGN]]


---
aliases:
  - CNT v2 BREAKOUT LAST 3 TRADES REVIEW
---

# CNT v2 BREAKOUT LAST 3 TRADES REVIEW

## Scope

This review is based on `logs/portfolio.log` only.

It pairs the latest three breakout selection events that later produced confirmed close entries.

## Trade 1

- `selection_time = 2026-04-20 17:14:03`
- `reason = trend_up_high_volatility_breakout`
- `confidence = 0.82`
- `selection_expectancy_snapshot = 0.0`
- `close_time = 2026-04-20 17:44:03`
- `close_action = STOP_MARKET_FILLED`
- `close_pnl_estimate = -0.01104399999999996`
- `post_trade_expectancy_snapshot = -0.01104399999999996`
- `post_trade_profit_factor_snapshot = 0.0`

Interpretation:

- first confirmed breakout trade immediately established a negative expectancy baseline
- later breakout selections started from a damaged sample state

## Trade 2

- `selection_time = 2026-04-21 03:04:03`
- `reason = trend_up_high_volatility_breakout`
- `confidence = 0.82`
- `selection_expectancy_snapshot = -0.01104399999999996`
- `close_time = 2026-04-21 03:54:02`
- `close_action = SELL_FILLED`
- `close_pnl_estimate = 0.01392600000000084`
- `post_trade_expectancy_snapshot = 0.0014410000000004402`
- `post_trade_profit_factor_snapshot = 1.2609561752988854`

Interpretation:

- one recovery win existed
- but the sample remained too small to prove stable edge

## Trade 3

- `selection_time = 2026-04-22 04:14:04`
- `reason = trend_up_relaxed_volatility_breakout`
- `confidence = 0.68`
- `selection_expectancy_snapshot = 0.0014410000000004402`
- `close_time = 2026-04-22 04:44:04`
- `close_action = STOP_MARKET_FILLED`
- `close_pnl_estimate = -0.06947599999999984`
- `post_trade_expectancy_snapshot = -0.022197999999999656`
- `post_trade_profit_factor_snapshot = 0.17295081967214201`

Interpretation:

- the third closed breakout trade caused the decisive quality breakdown
- it also means the relaxed breakout path is now represented in actual runtime evidence, not just tests

## Aggregate Reading

Across the last three confirmed breakout trades:

- wins = `1`
- losses = `2`
- net_pnl = `-0.06659399999999896`
- expectancy after trade 3 = `-0.022197999999999656`

## Required Conclusion

**breakout_v1 isolation required**

## Obsidian Links

- [[CNT v2 BREAKOUT QUALITY EVALUATION REPORT]]


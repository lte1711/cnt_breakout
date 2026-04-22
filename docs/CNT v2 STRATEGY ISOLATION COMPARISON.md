---
tags:
  - cnt
  - docs
  - v2
  - strategy
  - comparison
aliases:
  - CNT v2 STRATEGY ISOLATION COMPARISON
---

# CNT v2 STRATEGY ISOLATION COMPARISON

## Scope

This comparison uses:

- `data/strategy_metrics.json`
- `data/performance_snapshot.json`

Current snapshot reference:

- `2026-04-22 12:44:03`

## Comparison Table

| Baseline | Closed Trades | Win Rate | Expectancy | Profit Factor | Net PnL |
| --- | ---: | ---: | ---: | ---: | ---: |
| Mixed portfolio | 24 | 54.17% | -0.0007808 | 0.9159 | -0.0187390 |
| pullback_v1 only inferred baseline | 21 | 57.14% | 0.0022788 | 1.3365 | +0.0478550 |
| breakout_v1 standalone observed baseline | 3 | 33.33% | -0.0221980 | 0.1730 | -0.0665940 |

## Reading

### Mixed Portfolio

The combined portfolio currently fails because:

- expectancy is negative
- PF is below 1
- net PnL is negative

### pullback_v1 Only

The inferred pullback-only baseline remains positive:

- positive expectancy
- PF above 1.3
- positive net contribution

This supports the conclusion that pullback is not the dominant cause of the current portfolio failure.

### breakout_v1 Standalone

The observed breakout-only baseline is decisively weak:

- negative expectancy
- PF far below 1
- negative net contribution larger than the current mixed portfolio loss

## Contribution Math

Net contribution check:

- `pullback net = +0.0478550`
- `breakout net = -0.0665940`
- `mixed net = -0.0187390`

So the breakout contribution explains the transition from positive pullback quality to negative mixed portfolio quality.

## Interpretation

The correct reading is:

- pullback still has a positive standalone edge
- breakout currently degrades combined portfolio quality
- the next diagnosis step must separate breakout quality from pullback quality instead of tuning both together

## Required Conclusion

**breakout_v1 isolation required**

## Obsidian Links

- [[CNT v2 POST-READY DEGRADATION REVIEW]]
- [[CNT v2 BREAKOUT LAST 3 TRADES REVIEW]]
- [[00 Docs Index|Docs Index]]

---
---

# CNT v2 BREAKOUT V2 CANDIDATE VALIDATION START

## Purpose

This document prepares the next validation window for `breakout_v2`.

`breakout_v2` is implemented and registered, but not active.
This document does not activate it.
It defines the start conditions for a later candidate validation window.

Reference:

- current `breakout_v1` final isolation review:
  - CNT v2 BREAKOUT ISOLATION FINAL REVIEW

## Start Condition

The `breakout_v2` candidate validation window may start only after:

- current `breakout_v1` isolation window is closed
- current isolation verdict is fixed
- working tree hygiene is restored
- logging integrity is confirmed
- strategy registry integrity is confirmed
- `ACTIVE_STRATEGIES` remains unchanged before the start decision

Activation is still prohibited until this validation window is explicitly started.

## Sample Target

Recommended minimum:

- `trades_closed >= 5`

Higher confidence target:

- `trades_closed >= 8`

## Metrics

The validation window must track:

- `trades_closed`
- `expectancy`
- `profit_factor`
- `net_pnl`
- `win_rate`
- `execution_rate`
- `filtered_signal_ratio`
- `stop_exit_ratio`

## Promotion Gate

Promotion can be considered only if all of the following are true:

- sample target reached
- `expectancy > 0`
- `profit_factor > 1`
- no severe regression versus current breakout baseline
- no structural or logging issue

## Rejection Gate

Reject the candidate for now if any of the following is true:

- sample remains too low for fair judgment
- `expectancy <= 0`
- `profit_factor <= 1`
- stop exits dominate closed trades
- runtime or logging integrity degrades

## Operational Discipline

At this stage:

- do not activate `breakout_v2`
- do not remove `breakout_v1`
- do not relax risk guard
- do not change KPI calculations

## Obsidian Links

- [[CNT v2 BREAKOUT V2 DESIGN]]


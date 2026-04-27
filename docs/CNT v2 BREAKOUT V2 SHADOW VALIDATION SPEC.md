---
tags:
  - cnt
  - type/documentation
  - status/active
  - context-filter
  - type/validation
  - type/operation
  - strategy/breakout_v3
---

---
---

# CNT v2 BREAKOUT V2 SHADOW VALIDATION SPEC

## Purpose

This document defines the shadow validation mode for `breakout_v2`.

At this stage:

- `breakout_v2` is implemented
- `breakout_v2` is registered
- `breakout_v2` is **not** active in production runtime

The purpose of shadow validation is to compare `breakout_v2` signal quality against the locked `breakout_v1` reference without sending real orders.

## Shadow Validation Mode

### Core Rule

`breakout_v2` signal calculation is allowed.
Actual order submission is forbidden.

### Shadow Output Rule

`breakout_v2` must be treated as a shadow candidate only.

That means:

- signal evaluation may run
- filtering may be recorded
- allowed candidate count may be recorded
- hypothetical trade tracking may be recorded
- no production order may be sent from `breakout_v2`

## Comparison Targets

The shadow validation output must compare:

1. `breakout_v1 final reference`
2. `breakout_v2 shadow candidate`
3. `mixed portfolio baseline`

Important:

- `breakout_v1 final reference` is observed
- `breakout_v2 shadow candidate` is hypothetical
- `mixed portfolio baseline` is observed

## Required Shadow Metrics

The following must be recorded:

- `signal_count`
- `filtered_signal_ratio`
- `allowed_signal_ratio`
- `hypothetical_trades_count`
- `hypothetical_expectancy`
- `hypothetical_profit_factor`
- `stop_exit_ratio`
- `reason_distribution`

## Metric Meaning

### signal_count

Total `breakout_v2` evaluation count inside the validation window.

### filtered_signal_ratio

Filtered `breakout_v2` signals divided by total `breakout_v2` evaluations.

### allowed_signal_ratio

Allowed `breakout_v2` signals divided by total `breakout_v2` evaluations.

### hypothetical_trades_count

Number of shadow entries that would have qualified as hypothetical breakout_v2 trades.

### hypothetical_expectancy

Hypothetical average per-trade return based on the shadow trade record.

### hypothetical_profit_factor

Hypothetical gross profit divided by hypothetical gross loss.

### stop_exit_ratio

Hypothetical stop exits divided by all hypothetical closed trades.

### reason_distribution

Distribution of shadow reasons, including:

- filtered reasons
- allowed reasons
- exit reasons

## Shadow Logging Rule

Shadow validation should preserve a strict distinction between:

- real runtime outcomes
- shadow-only hypothetical outcomes

The shadow candidate must never be reported as an observed production strategy.

## Activation Still Off

`breakout_v2` must remain off until all of the following are satisfied:

- minimum sample reached
- `hypothetical_expectancy > 0`
- `hypothetical_profit_factor > 1`
- no structural or logging issue
- no severe regression risk versus locked references

## Pre-Activation Gate

Before any activation discussion:

- `ACTIVE_STRATEGIES` must remain unchanged
- no risk guard change is allowed
- no KPI calculation change is allowed
- no direct production switch is allowed

## Related References

- CNT v2 BREAKOUT ISOLATION FINAL REVIEW
- CNT v2 BREAKOUT V2 DESIGN
- CNT v2 BREAKOUT A B VALIDATION PLAN
- CNT v2 BREAKOUT V2 VALIDATION WINDOW START

## Obsidian Links

- [[CNT v2 BREAKOUT V2 DESIGN]]


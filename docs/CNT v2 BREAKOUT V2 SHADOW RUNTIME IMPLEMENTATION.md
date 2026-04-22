---
tags:
  - cnt
  - breakout
  - shadow
  - implementation
---

# CNT v2 BREAKOUT V2 SHADOW RUNTIME IMPLEMENTATION

## Summary

`breakout_v2` shadow runtime integration is implemented without changing the production execution path.

Current implementation status:

- `breakout_v2` remains registered but off
- `ACTIVE_STRATEGIES` remains unchanged
- shadow evaluation runs outside execution decision and order routing
- shadow outputs are written to dedicated shadow files only

## Implemented Files

- `src/shadow_eval.py`
- `src/engine.py`
- `tests/test_shadow_eval.py`
- `tests/test_engine_cycle_smoke.py`

## Runtime Hook Location

Shadow evaluation is called in `src/engine.py` after ranked strategy collection is completed and before selected-signal handling proceeds through the live execution branch.

This location was chosen because:

1. runtime market data is already available
2. active strategy evaluation has already happened
3. shadow output can be recorded without mutating live execution flow

## Shadow Output Files

- `logs/shadow_breakout_v2.jsonl`
- `data/shadow_breakout_v2_snapshot.json`

### Append Log Purpose

The jsonl file stores one append-only shadow event per cycle.

### Snapshot Purpose

The snapshot file stores cumulative operator-facing aggregates:

- signal count
- filtered count
- allowed count
- ratios
- hypothetical trade count
- reason distribution

## Exception Handling

Shadow evaluation is intentionally defensive.

- shadow evaluation failure does not stop engine execution
- shadow append failure does not stop engine execution
- shadow snapshot update failure does not stop engine execution

This preserves the main runtime contract:

- live orders continue to depend only on active strategies
- shadow instrumentation is optional and non-blocking

## Why Execution Path Is Unchanged

The shadow result is not forwarded to:

- `execution_decider`
- `order_router`
- live order submission
- pending order state
- open trade state

Therefore:

- no live order can be created from `breakout_v2`
- no state mutation can occur from `breakout_v2`
- no portfolio KPI is changed by the shadow branch

## Known Limitations

Current shadow snapshot is intentionally conservative.

- `hypothetical_expectancy` is placeholder-only at this stage
- `hypothetical_profit_factor` is placeholder-only at this stage
- `stop_exit_ratio` is placeholder-only at this stage

These fields are reserved for later hypothetical trade lifecycle aggregation and must not be interpreted as observed performance yet.

## Validation

Implemented validation coverage includes:

- shadow evaluation schema test
- shadow jsonl append test
- shadow snapshot aggregation test
- engine continuation test when shadow log append fails

## Operational Meaning

This implementation enables:

- runtime shadow observation of `breakout_v2`
- comparison against `breakout_v1` final reference
- comparison against observed mixed portfolio baseline

without promoting `breakout_v2` into production.

## Obsidian Links

- [[CNT v2 BREAKOUT V2 SHADOW RUNTIME INTEGRATION]]
- [[CNT v2 BREAKOUT V2 SHADOW VALIDATION SPEC]]
- [[CNT v2 BREAKOUT V2 VALIDATION WINDOW START]]

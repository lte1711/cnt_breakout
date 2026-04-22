---
tags:
  - cnt
  - breakout
  - shadow
  - runtime
---

# CNT v2 BREAKOUT V2 SHADOW RUNTIME INTEGRATION

## Purpose

This document defines how `breakout_v2` should be integrated as a shadow candidate at runtime without entering the production execution path.

At this stage:

- `breakout_v2` is implemented
- `breakout_v2` is registered
- `breakout_v2` remains off
- direct production activation is prohibited

## Integration Point

`breakout_v2` shadow evaluation should happen **after market context is built** and **outside the execution path**.

Recommended runtime location:

1. market context created
2. active strategies evaluated as usual
3. `breakout_v2` shadow evaluated separately
4. shadow result written to shadow output only
5. execution continues using active strategy output only

This keeps the shadow branch comparable while preserving current runtime behavior.

## Why It Must Stay Outside Execution Path

`breakout_v2` is still a candidate.

If shadow output reaches execution components, it would:

- contaminate the current runtime baseline
- break the current validation discipline
- risk mixing hypothetical and real trades

Therefore:

- no `order_router` connection
- no `execution_decider` connection
- no order submission path

## Why `ACTIVE_STRATEGIES` Remains Unchanged

`ACTIVE_STRATEGIES` must remain unchanged because the current production runtime still depends on:

- `breakout_v1` as reference baseline
- `pullback_v1` as the active profitable strategy

Changing `ACTIVE_STRATEGIES` now would convert validation into production mutation.

## Comparison Logic

The shadow candidate must be compared against:

1. `breakout_v1 final reference`
2. `breakout_v2 shadow candidate`
3. `mixed portfolio baseline`

Important:

- `breakout_v1 final reference` is observed
- `breakout_v2 shadow candidate` is hypothetical
- `mixed portfolio baseline` is observed

## Output File Location

Recommended files:

- `data/shadow_breakout_v2_snapshot.json`
- `logs/shadow_breakout_v2.jsonl`

### Snapshot Purpose

`shadow_breakout_v2_snapshot.json` should hold the latest aggregated summary for operator review and dashboard-style checks.

### Append Log Purpose

`shadow_breakout_v2.jsonl` should hold per-event append-only shadow records for later review and aggregation.

## Logging Schema

Each shadow event record should include at minimum:

- `ts`
- `symbol`
- `strategy`
- `signal_generated`
- `entry_allowed`
- `filter_reason`
- `confidence`
- `vwap`
- `band_width_ratio`
- `band_expansion_ratio`
- `volume_ratio`
- `hypothetical_entry`

## Snapshot Schema

The aggregated snapshot should include at minimum:

- `signal_count`
- `filtered_signal_count`
- `allowed_signal_count`
- `filtered_signal_ratio`
- `allowed_signal_ratio`
- `hypothetical_trades_count`
- `hypothetical_expectancy`
- `hypothetical_profit_factor`
- `stop_exit_ratio`
- `reason_distribution`
- `last_updated`

## Implementation Shape

Recommended helper module:

- `src/shadow_eval.py`

Suggested responsibilities:

- evaluate `breakout_v2` in shadow mode
- append shadow jsonl records
- update shadow snapshot aggregates

## Runtime Boundary Rule

The shadow result must never be forwarded to:

- order validation
- execution decision
- order routing
- pending/open trade state mutation

## Operational Meaning

This design allows:

- runtime-quality signal comparison
- filter behavior analysis
- hypothetical trade quality review

without changing production execution.

## Obsidian Links

- [[CNT v2 BREAKOUT V2 SHADOW VALIDATION SPEC]]
- [[CNT v2 BREAKOUT V2 VALIDATION WINDOW START]]
- [[CNT v2 BREAKOUT ISOLATION FINAL REVIEW]]

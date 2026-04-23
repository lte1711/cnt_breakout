---
tags:
  - cnt
  - breakout
  - shadow
  - snapshot
aliases:
  - CNT v2 BREAKOUT V2 SHADOW SNAPSHOT EXPANSION IMPLEMENTATION
---

# CNT v2 BREAKOUT V2 SHADOW SNAPSHOT EXPANSION IMPLEMENTATION

## Purpose

This change extends `data/shadow_breakout_v2_snapshot.json` so the latest expanded shadow observations can be read directly from the snapshot layer without re-parsing the entire JSONL log each time.

## Added Fields

The following fields were added in an additive, backward-compatible way:

- `expanded_event_count`
- `secondary_fail_distribution`
- `stage_false_counts`

## Why This Was Added

The previous snapshot shape was enough for:

- total signal count
- allowed vs filtered count
- first-blocker distribution

But it was not enough for:

- downstream blocker inspection
- expanded-schema observation review
- quick operator-facing review of stage-level failure patterns

## Backward Compatibility

Existing fields remain unchanged:

- `signal_count`
- `filtered_signal_count`
- `allowed_signal_count`
- `filtered_signal_ratio`
- `allowed_signal_ratio`
- `hypothetical_trades_count`
- `reason_distribution`
- `last_updated`

No existing consumer is required to read the new fields.

## Aggregation Rules

- `expanded_event_count`
  - increments only when the shadow event contains:
    - `secondary_fail_reasons`
    - `evaluated_stage_trace`
    - `stage_flags`
- `secondary_fail_distribution`
  - counts each downstream fail reason from `secondary_fail_reasons`
- `stage_false_counts`
  - counts each `stage_flags` item where the value is `false`

## Safety

- no change to execution path
- no change to `ACTIVE_STRATEGIES`
- no activation of `breakout_v2`
- no tuning or gate relaxation

## Known Limitation

This snapshot still does not compute hypothetical expectancy or hypothetical profit factor from shadow events. It remains an observability layer, not a promotion-decision engine by itself.

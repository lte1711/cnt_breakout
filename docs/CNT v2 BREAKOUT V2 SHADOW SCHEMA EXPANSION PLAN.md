---
tags:
  - cnt
  - breakout
  - shadow
  - schema
  - plan
---

# CNT v2 BREAKOUT V2 SHADOW SCHEMA EXPANSION PLAN

## Purpose

This plan defines a safe schema expansion for `breakout_v2` shadow observation so later tuning decisions can be evidence-based.

This is a schema and observability plan only.

It is **not** an activation plan and it is **not** a tuning plan.

## Expansion Goals

The expanded shadow schema should allow:

- per-event secondary failure visibility
- per-stage pass/fail reconstruction
- better separation between first blocker and downstream blocker

## Proposed Additions

### 1. `secondary_fail_reasons`

Suggested event field:

```json
"secondary_fail_reasons": ["ema_fast_not_above_slow", "band_width_too_narrow"]
```

Purpose:

- preserve additional failures that would have occurred after the first blocker
- support conditional subset review without mutating runtime behavior

### 2. `evaluated_stage_trace`

Suggested event field:

```json
"evaluated_stage_trace": [
  {"stage": "range_bias", "passed": true},
  {"stage": "volatility", "passed": false},
  {"stage": "ema", "passed": false},
  {"stage": "breakout_confirmation", "passed": true}
]
```

Purpose:

- preserve actual evaluation order
- support stage-by-stage decomposition with fewer assumptions

### 3. Optional Per-Stage Pass/Fail Flags

Suggested flat fields if simpler than a trace array:

- `stage_range_bias_passed`
- `stage_volatility_passed`
- `stage_ema_passed`
- `stage_breakout_confirmation_passed`
- `stage_vwap_distance_passed`
- `stage_band_width_passed`
- `stage_band_expansion_passed`
- `stage_volume_passed`

Purpose:

- easier downstream aggregation
- simpler review queries

## Backward Compatibility

Backward compatibility must be preserved.

Rules:

1. existing event keys must remain valid
2. existing snapshot fields must remain valid
3. new fields must be additive only
4. missing new fields in old events must not break log parsing

## Recommended Rollout Shape

1. expand shadow event schema only
2. keep existing snapshot schema intact
3. add optional aggregation later only after enough richer events accumulate

This keeps the rollout conservative and avoids contaminating existing validation baselines.

## What Must Not Change

- `breakout_v2` actual activation remains prohibited
- `ACTIVE_STRATEGIES` remains unchanged
- execution path remains unchanged
- risk guard remains unchanged
- KPI calculation remains unchanged

## Final Recommendation

`schema expansion required before further tuning decisions`

## Obsidian Links

- [[CNT v2 BREAKOUT V2 SHADOW SCHEMA LIMITATION REVIEW]]
- [[CNT v2 BREAKOUT V2 SHADOW RUNTIME INTEGRATION]]
- [[CNT v2 BREAKOUT V2 SHADOW RUNTIME IMPLEMENTATION]]

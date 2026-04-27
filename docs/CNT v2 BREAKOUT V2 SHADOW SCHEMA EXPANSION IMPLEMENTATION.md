---
tags:
  - cnt
  - type/documentation
  - status/active
  - market-context
  - context-filter
  - strategy/breakout_v3
---

---
---

# CNT v2 BREAKOUT V2 SHADOW SCHEMA EXPANSION IMPLEMENTATION

## Summary

The `breakout_v2` shadow event schema is expanded additively so downstream filter-chain analysis becomes possible without changing the production execution path.

## Added Fields

New shadow event fields:

- `secondary_fail_reasons`
- `evaluated_stage_trace`
- `stage_flags`

### `secondary_fail_reasons`

Stores additional failing conditions beyond the primary `filter_reason`.

### `evaluated_stage_trace`

Stores an ordered stage-by-stage trace with:

- `stage`
- `passed`
- `reason`

### `stage_flags`

Stores compact per-stage pass/fail booleans:

- `market_bias_pass`
- `volatility_pass`
- `ema_pass`
- `rsi_threshold_pass`
- `breakout_confirmed`
- `vwap_distance_pass`
- `band_width_pass`
- `band_expansion_pass`
- `volume_pass`

## Why Additive Design Was Chosen

Additive design was chosen so that:

1. existing shadow consumers keep working
2. historical jsonl entries remain readable
3. snapshot aggregation remains stable
4. production execution remains unchanged

## Backward Compatibility Strategy

The following original fields remain unchanged:

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

Snapshot schema remains under the minimum-change rule.

No required snapshot consumer changes were introduced in this step.

## Files Updated

- `src/shadow_eval.py`
- `tests/test_shadow_eval.py`

## Execution Path Safety

This expansion changes shadow event richness only.

It does **not**:

- activate `breakout_v2`
- change `ACTIVE_STRATEGIES`
- route shadow output into execution decision
- route shadow output into order submission

## Known Limitations After Expansion

Even after schema expansion:

- shadow output is still hypothetical
- `hypothetical_expectancy` remains placeholder-only
- `hypothetical_profit_factor` remains placeholder-only
- `stop_exit_ratio` remains placeholder-only

This step improves causal observability, not profitability proof.

## Obsidian Links

- [[CNT v2 BREAKOUT V2 DESIGN]]


---
tags:
  - cnt
  - breakout
  - v3
  - shadow
  - implementation
aliases:
  - CNT v2 BREAKOUT V3 SHADOW RUNTIME INTEGRATION IMPLEMENTATION REPORT
---

# CNT v2 BREAKOUT V3 SHADOW RUNTIME INTEGRATION IMPLEMENTATION REPORT

## Status

- status = `IMPLEMENTED`
- runtime_mode = `SHADOW_ONLY`
- activation = `PROHIBITED`
- execution_path = `UNCHANGED`

## Summary

`breakout_v3` shadow evaluation is now connected to the engine as a non-intrusive observation branch.

The runtime integration only performs:

1. `build_breakout_v3_conditions(...)`
2. `evaluate_breakout_v3_shadow(...)`
3. event serialization
4. jsonl append
5. snapshot aggregation update

It does **not**:

- participate in ranking
- submit orders
- mutate position state
- affect `entry_gate`
- affect `execution_decider`
- affect `risk_guard`

## Integration Point

The insertion point is inside `src/engine.py`, immediately after ranked signal selection and metrics save, alongside the existing `breakout_v2` shadow branch.

Current observation sequence:

1. ranked selection computed
2. strategy metrics saved
3. `breakout_v2` shadow branch runs
4. `breakout_v3` shadow branch runs
5. live selected signal continues through the normal execution path

## Runtime Outputs

The new observation outputs are:

- `logs/shadow_breakout_v3.jsonl`
- `data/shadow_breakout_v3_snapshot.json`

### Event payload

Each event contains the locked shadow schema, including:

- `allowed`
- `summary_reason`
- `first_blocker`
- `hard_blocker`
- `soft_pass_count`
- `stage_flags`
- `condition_flags`
- `secondary_fail_reasons`
- `metadata`

### Snapshot payload

The snapshot is aggregated from the jsonl file and includes:

- `signal_count`
- `allowed_signal_count`
- `allowed_signal_ratio`
- `expanded_event_count`
- `first_blocker_distribution`
- `hard_blocker_distribution`
- `secondary_blocker_distribution`
- `soft_pass_count_distribution`
- `stage_pass_counts`
- `stage_fail_counts`
- `min_soft_pass_required`
- `soft_total_count`
- `aggregation_scope`
- `last_updated`

## Exception Handling

Runtime safety is preserved with guarded execution:

- evaluator failure returns without interrupting engine flow
- jsonl append failure is swallowed and does not affect trading flow
- snapshot update failure is swallowed and does not affect trading flow

This keeps the shadow branch observational only.

## Validation

Validation completed:

- `python -m unittest discover -s tests -p "test_*.py"`
- `python -m py_compile config.py src\\engine.py src\\shadow\\breakout_v3_shadow_eval.py tests\\test_breakout_v3_shadow_eval.py tests\\test_engine_cycle_smoke.py`

Expected guarantees:

- engine still completes one-shot cycles
- `ACTIVE_STRATEGIES` remains unchanged
- order path remains unchanged
- `breakout_v3` remains `shadow-only`

## Known Limitations

- no runtime ranking participation
- no live signal consumption
- no activation logic
- no testnet order-path verification performed in this step
- no module split yet between evaluator, IO, and aggregation

## Final Record

This step implements runtime integration skeleton only.

`breakout_v3` is now observable from the engine, but it remains fully disconnected from live execution behavior.

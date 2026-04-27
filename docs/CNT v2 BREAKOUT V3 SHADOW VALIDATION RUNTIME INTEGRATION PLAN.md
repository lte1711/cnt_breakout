---
tags:
  - cnt
  - type/documentation
  - status/active
  - market-context
  - type/validation
  - type/operation
  - risk
  - strategy/breakout_v3
  - cnt-v2-breakout-v3-shadow-validation-runtime-integration-plan
---

# CNT v2 BREAKOUT V3 SHADOW VALIDATION RUNTIME INTEGRATION PLAN

## Status

- status = `PLANNED`
- implementation = `NOT STARTED`
- runtime_mode = `SHADOW_ONLY`

## 1. Scope Lock

The following scope is fixed for the next step:

- `breakout_v3` remains `shadow-only`
- live activation is prohibited
- order path remains disconnected
- `ACTIVE_STRATEGIES` remains unchanged
- no registry promotion is allowed at this phase

This plan covers runtime observation integration only.

It does **not** authorize:

- live signal consumption
- order submission
- position mutation
- ranking participation

## 2. Integration Point

The planned insertion point is inside the engine observation layer, after market context is available and before any shadow result could influence execution behavior.

Planned runtime flow:

1. market context available
2. `build_breakout_v3_conditions(...)`
3. `evaluate_breakout_v3_shadow(...)`
4. shadow event serialization
5. jsonl append
6. snapshot aggregation update

Required rule:

- this flow must stay outside the live execution path
- it must not feed:
  - `entry_gate`
  - `execution_decider`
  - `order_executor`
  - `risk_guard`
  - `portfolio_risk_manager`

## 3. New Runtime Outputs

Planned shadow outputs:

- `logs/shadow_breakout_v3.jsonl`
- `data/shadow_breakout_v3_snapshot.json`

### Purpose

`logs/shadow_breakout_v3.jsonl`

- append-only event log
- one evaluated shadow event per line
- detailed blocker and stage evidence

`data/shadow_breakout_v3_snapshot.json`

- latest aggregate summary
- operator-facing quick inspection
- downstream review input

## 4. Event Schema Lock

Each jsonl event must contain at minimum:

- `allowed`
- `summary_reason`
- `first_blocker`
- `hard_blocker`
- `soft_pass_count`
- `stage_flags`
- `condition_flags`
- `secondary_fail_reasons`
- `metadata`

Recommended full payload:

- `timestamp`
- `symbol`
- `strategy_name`
- `allowed`
- `summary_reason`
- `first_blocker`
- `hard_blocker`
- `soft_pass_count`
- `soft_fail_count`
- `soft_total_count`
- `min_soft_pass_required`
- `stage_flags`
- `condition_flags`
- `secondary_fail_reasons`
- `metadata`

## 5. Snapshot Schema Lock

The planned snapshot must contain:

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

These fields are required so that:

- first-blocker review is possible
- downstream blocker review is possible
- soft-threshold behavior is visible
- aggregation assumptions remain explicit

## 6. Runtime Safety Rules

The following safety rules are mandatory:

- any shadow exception must not interrupt the engine main flow
- shadow logging failure must not block order logic
- snapshot write failure must degrade gracefully
- `pullback_v1` and `breakout_v1` behavior must remain unchanged
- no shadow event may mutate state or portfolio files

This implies:

- protective try/except around shadow write operations
- no dependency from live decision logic to shadow outputs

## 7. Validation Gate

After runtime integration, the minimum validation set is:

1. jsonl append works
2. snapshot file is created and updated
3. existing test suite still passes
4. runtime `action` behavior is unchanged
5. `ACTIVE_STRATEGIES` remains unchanged
6. no unexpected `pending_order` or `open_trade` mutations occur due to `breakout_v3`

Additional recommended checks:

- event schema contains all locked fields
- snapshot schema contains all locked fields
- engine still completes one-shot cycles normally

## 8. Explicit Prohibitions

The following remain prohibited:

- `breakout_v3` activation
- parameter tuning
- live signal consumption
- `risk_guard` connection
- `order_validator` connection
- execution path connection
- ranking participation

## 9. Module Boundary Note

Current skeleton implementation places:

- evaluator
- event builder
- aggregator

within the same `breakout_v3` shadow module layer.

Planned decision for the next step:

- do **not** split modules yet
- keep the current single-module approach during initial runtime integration
- reconsider module separation only after the first shadow runtime observation window

This keeps the next integration step smaller and lower-risk.

## 10. Planned Next Step

The next implementation step after this plan is:

1. connect `breakout_v3` shadow evaluation to runtime
2. write only to:
   - `logs/shadow_breakout_v3.jsonl`
   - `data/shadow_breakout_v3_snapshot.json`
3. keep all execution behavior unchanged

## Final Plan Statement

`breakout_v3` runtime integration must be observation-only.

It will be inserted as a shadow evaluation branch, not as a trading branch.

No activation, tuning, or live consumption is permitted before a shadow observation window produces evidence.

## Obsidian Links

- [[CNT v2 BREAKOUT V3 DESIGN DRAFT]]


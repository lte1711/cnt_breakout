---
tags:
  - cnt
  - type/documentation
  - status/active
  - market-context
  - type/operation
  - strategy/breakout_v3
  - type/analysis
  - cnt-v2-breakout-v3-shadow-evaluator-implementation-report
---

# CNT v2 BREAKOUT V3 SHADOW EVALUATOR IMPLEMENTATION REPORT

## Scope

This step implements the code skeleton for `breakout_v3` shadow evaluation without changing runtime execution behavior.

## Project Comparison

The proposed design was compared against the current CNT structure.

Current CNT realities:

- `src/models/` is dataclass-oriented
- `src/strategies/` already contains breakout logic helpers and market classification reuse
- `src/shadow_eval.py` currently hosts `breakout_v2` shadow evaluation in a flat module
- `ACTIVE_STRATEGIES` and runtime order flow must remain unchanged

Implementation decision:

- keep `breakout_v3` out of `ACTIVE_STRATEGIES`
- do not connect `breakout_v3` to engine execution
- do not register `breakout_v3` as an active runtime strategy
- implement reusable shadow-evaluation primitives only

## Implemented Files

- `src/models/breakout_v3_eval_result.py`
- `src/strategies/breakout_v3.py`
- `src/shadow/breakout_v3_shadow_eval.py`
- `tests/test_breakout_v3_shadow_eval.py`
- `tests/test_breakout_v3_shadow_aggregator.py`

Updated:

- `config.py`

## What Was Implemented

### Data Models

Added dataclasses for:

- `BreakoutV3Conditions`
- `StageResult`
- `BreakoutV3EvalResult`
- `BreakoutV3ShadowEvent`

### Strategy Layer

Added `build_breakout_v3_conditions(...)` to calculate raw condition flags only.

This layer:

- does not submit orders
- does not create live state
- does not return `StrategySignal`

### Evaluator Layer

Added `evaluate_breakout_v3_shadow(...)` with:

- stage-by-stage hard/soft evaluation
- first blocker ordering
- hard blocker extraction
- soft pass counting
- structured summary reason

### Aggregation Layer

Added `aggregate_breakout_v3_shadow_events(...)` for:

- allowed ratio
- blocker distributions
- stage pass/fail counts
- soft pass count distribution

## What Was Explicitly Not Implemented

- no engine hook
- no shadow jsonl writer for `breakout_v3` yet
- no snapshot file writer for `breakout_v3` yet
- no registry activation
- no runtime trade execution path

These are intentionally deferred to keep this step safe and structurally isolated.

## Validation Result

Validation target:

- evaluator behavior
- blocker ordering
- soft threshold behavior
- aggregation behavior

This step should pass:

- unit tests for evaluator
- unit tests for aggregator
- compile checks

## Safety Statement

This implementation preserves current system safety:

- `pullback_v1` remains the live positive driver
- `breakout_v1` remains the active reference breakout strategy
- `breakout_v2` remains shadow-only
- `breakout_v3` remains implementation scaffolding only

## Conclusion

`breakout_v3` shadow evaluator scaffolding is now implemented in a project-compatible way.

The current state is:

- design -> fixed
- evaluator skeleton -> implemented
- runtime integration -> not started
- activation -> prohibited

## Obsidian Links

- [[CNT v2 BREAKOUT V3 DESIGN DRAFT]]


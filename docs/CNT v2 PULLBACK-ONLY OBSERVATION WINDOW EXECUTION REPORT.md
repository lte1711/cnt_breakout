---
title: CNT v2 PULLBACK-ONLY OBSERVATION WINDOW EXECUTION REPORT
status: FINAL
language: en
updated: 2026-04-24
tags:
  - cnt
  - observation
  - pullback_v1
  - breakout_v3
  - verification
---

# CNT v2 PULLBACK-ONLY OBSERVATION WINDOW EXECUTION REPORT

## Purpose

This report records the immediate execution of the next-stage instruction based on the verified `9a29d34` baseline:

- `pullback_v1` only in the live active runtime set
- `breakout_v1` isolated from active runtime
- `breakout_v3` kept as shadow-only
- no threshold or execution-path tuning during the observation window

## Validation Performed

### Test validation

- `PYTHONPATH=. python -m pytest -q`
- result: `56 passed`

### Compile validation

- `python -m py_compile config.py src\shadow\breakout_v3_shadow_eval.py src\state\state_manager.py`
- result: `OK`

### Runtime validation

- entry chain executed via `run.ps1`
- runtime completed without execution-path regression

## Runtime State After Execution

From `data/state.json`:

- `strategy_name = pullback_v1`
- `action = NO_ENTRY_SIGNAL`
- `last_run_time = 2026-04-24 07:14:00`

This confirms that the current live active runtime strategy is `pullback_v1`.

## Portfolio Risk Consistency

From `data/state.json` and `data/portfolio_state.json`:

- `daily_loss_count = 3`
- `consecutive_losses = 3`

The two state files are synchronized for the preserved risk counters.

## Live Runtime Observation

Latest runtime log entries after active-set isolation show:

- `2026-04-24 06:50:10` -> `strategy_name=pullback_v1`
- `2026-04-24 06:54:00` -> `strategy_name=pullback_v1`
- `2026-04-24 07:04:00` -> `strategy_name=pullback_v1`
- `2026-04-24 07:14:00` -> `strategy_name=pullback_v1`

Historical `breakout_v1` lines remain in the same log file as past evidence, but no new post-isolation runtime action was recorded with `breakout_v1`.

## Signal Observation

Latest appended signal-log rows during the pullback-only window were:

- `pullback_v1 / NO_SETUP / pullback_rsi_not_in_range`
- `pullback_v1 / PULLBACK / trend_pullback_reentry_relaxed_rsi`
- `pullback_v1 / PULLBACK / near_trend_pullback_reentry`
- `pullback_v1 / NO_SETUP / trend_not_up`

No new `breakout_v1` signal line was appended in the post-isolation run window used for this report.

## Breakout V3 Shadow Observation

Current `data/shadow_breakout_v3_snapshot.json` at report time:

- `signal_count = 8`
- `allowed_signal_count = 0`
- `allowed_signal_ratio = 0.0`

### First blocker distribution

- `setup_not_ready = 5`
- `breakout_not_confirmed = 3`

### Soft pass count distribution

- `1 -> 1`
- `2 -> 2`
- `3 -> 2`
- `4 -> 3`

### Stage counts

- `stage_pass_counts`
  - `regime = 8`
  - `setup = 3`
  - `trigger = 2`
  - `quality = 5`
- `stage_fail_counts`
  - `setup = 5`
  - `trigger = 6`
  - `quality = 3`

## Shadow Semantic Consistency

Current clean-log checks over the active post-fix shadow log:

- `allowed=true with blocker = 0`
- `summary_reason / hard_blocker conflict = 0`
- `trend_not_up first_blocker = 0`
- `range_without_upward_bias first_blocker = 0`

This means the current shadow observation data remains semantically clean under the fixed evaluator rules.

## Live Gate Status

`data/live_gate_decision.json` remains:

- `status = FAIL`
- `reason = NON_POSITIVE_EXPECTANCY`

This did not improve yet during this short observation step.

## Interpretation

The current execution confirms:

1. `pullback_v1` remains the only active runtime strategy.
2. portfolio risk counters remain synchronized.
3. `breakout_v3` shadow output remains semantically clean.
4. the shadow observation window is progressing with valid post-fix data.
5. Live Gate still reflects historical negative contamination, which means more observation time is still needed before drawing a post-isolation performance conclusion.

## Review Threshold Status

The next formal review threshold has **not** been reached yet.

Current status:

- `shadow_breakout_v3_snapshot.signal_count = 8`
- review threshold = `>= 20`

## Next Action

Continue the clean observation window without:

- reactivating `breakout_v1`
- activating `breakout_v3`
- changing thresholds
- changing intervals
- changing execution path

The next formal review should be performed when:

- `shadow_breakout_v3_snapshot.signal_count >= 20`, or
- any semantic conflict reappears, or
- any unexpected live runtime behavior appears.

## Conclusion

The next-stage execution instruction was applied successfully.

The current CNT state is now:

- live active runtime = `pullback_v1` only
- `breakout_v3` = shadow-only
- shadow semantics = clean
- portfolio risk sync = preserved
- Live Gate = still negative, pending further post-isolation observation

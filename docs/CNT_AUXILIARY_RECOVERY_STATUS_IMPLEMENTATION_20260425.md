---
tags:
  - cnt
  - implementation
  - recovery
aliases:
  - CNT AUXILIARY RECOVERY STATUS IMPLEMENTATION 20260425
---

# CNT AUXILIARY RECOVERY STATUS IMPLEMENTATION 20260425

```text
DOCUMENT_NAME = cnt_auxiliary_recovery_status_implementation_20260425
PROJECT       = CNT
MODE          = BINANCE_SPOT_TESTNET
STATUS        = IMPLEMENTED_AND_VALIDATED
OFFICIAL_GATE = UNCHANGED
```

---

# 1. Design Summary

This implementation adds a non-authoritative auxiliary recovery status layer.

Purpose:

- keep the official live gate unchanged
- preserve aggregate failure visibility
- separately measure active `pullback_v1` recovery evidence
- expose the effect of excluding historical `breakout_v1` contribution
- record runtime exposure and risk counter synchronization

Files changed:

- `config.py`
- `src/analytics/auxiliary_recovery_status.py`
- `src/engine.py`
- `scripts/generate_performance_report.py`
- `tests/test_auxiliary_recovery_status.py`
- `tests/test_engine_cycle_smoke.py`
- `run.ps1`

Files generated:

- `data/auxiliary_recovery_status.json`

Operational heartbeat support was also added to `run.ps1`:

- target file = `data/scheduler_heartbeat.json`
- gap threshold = `20` minutes
- expected interval = `10` minutes

The heartbeat file will be written by the normal `run.ps1` entry chain on scheduler start, finish, skip, or exception. The engine was not directly executed for this implementation.

---

# 2. Validation Result

## Official Gate

Official gate logic remains in:

- `src/validation/live_gate_evaluator.py`

No official live gate condition was modified.

Current generated auxiliary output records:

- official status = `FAIL`
- official reason = `NON_POSITIVE_EXPECTANCY`
- official expectancy = `-0.0003352571428572645`
- official net pnl = `-0.011734000000004186`
- official closed trades = `35`

## Auxiliary Recovery Output

Generated file:

- `data/auxiliary_recovery_status.json`

Current `pullback_v1` section:

- closed trades = `32`
- wins = `17`
- losses = `15`
- win rate = `0.53125`
- expectancy = `0.0017143749999998367`
- profit factor = `1.234828800986202`
- net pnl = `0.054859999999994774`

Current recovery signal:

- status = `RECOVERY_OBSERVATION_IN_PROGRESS`
- positive expectancy = `true`
- positive net pnl = `true`
- profit factor pass = `true`
- statistically valid = `false`
- min sample required = `50`
- all recovery criteria passed = `false`

Interpretation:

- `pullback_v1` has positive evidence.
- the system remains officially failed.
- recovery is not proven until the minimum sample threshold is reached.

## Scheduler Heartbeat

`run.ps1` now writes scheduler heartbeat JSON during normal entry-chain operation.

Fields include:

- `last_event`
- `current_time`
- `last_start_time`
- `last_finish_time`
- `expected_interval_minutes`
- `gap_threshold_minutes`
- `gap_detected`
- `gap_duration_minutes`
- `exit_code`
- `error_message`

Validation:

- `run.ps1` scriptblock parse check passed.
- `run.ps1` was not executed manually during validation.

## Test Result

Command:

```powershell
python -m pytest
```

Result:

- collected tests = `58`
- passed = `58`
- failed = `0`

Additional validation:

```powershell
python -m py_compile src\analytics\auxiliary_recovery_status.py src\engine.py scripts\generate_performance_report.py
```

Result:

- passed

---

# 3. Record Text

The project now has a separate auxiliary recovery status artifact that can report active `pullback_v1` recovery without changing or weakening the official live gate.

Current state remains:

- official system gate = `FAIL`
- active recovery evidence = positive but statistically incomplete
- recovery proof threshold = `closed_trades >= 50`, `expectancy > 0`, `profit_factor > 1.1`
- `breakout_v1` remains a historical negative contributor
- `breakout_v3` remains shadow-only

During this work, the scheduler appears to have executed normally and produced a current runtime state with an open `pullback_v1` trade. This was not caused by a direct engine invocation from this implementation step.

---

# Obsidian Links

- [[00 Docs Index]]
- [[CNT_NEXT_STEP_DATA_ANALYSIS_20260425]]
- [[CNT_PROJECT_STATUS_RECHECK_20260425]]
- [[CNT v2 OFFICIAL LIVE GATE RETENTION AND AUXILIARY RECOVERY PLAN]]

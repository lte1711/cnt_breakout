---
tags:
  - cnt
  - type/documentation
  - status/active
  - type/validation
  - offline-experiment
  - type/operation
  - strategy/breakout_v3
  - type/analysis
  - status/completed
  - cnt-v2-observability-aggregation-patch-report
---

# CNT v2 OBSERVABILITY AGGREGATION PATCH REPORT

```text
DOCUMENT_NAME = cnt_v2_observability_aggregation_patch_report
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-20
STATUS        = COMPLETE
REFERENCE_1   = CNT v2 OBSERVABILITY IMPLEMENTATION REPORT
REFERENCE_2   = CNT v2 OBSERVABILITY VALIDATION GATE
```

---

# 1. EXECUTIVE SUMMARY

The required observability interpretation fixes were implemented.

Completed in this stage:

* `selected_strategy_counts` aggregation correction
* mixed old/new blocked-signal parsing support
* regression tests for snapshot parsing

Completed in this stage:

* fresh runtime proof of new-format observability lines during a live cycle

Current next step:

```text
breakout_v1 first relaxation experiment is now allowed
```

---

# 2. IMPLEMENTED CODE FIXES

Updated:

* `src/analytics/performance_snapshot.py`

Implemented:

1. `selected_strategy_counts` now counts only lines containing `selection_reason=highest_score`
2. legacy `reason=no_ranked_signal` lines remain supported
3. new `blocked_detail` structures remain supported
4. mixed old/new log streams do not break snapshot generation
5. entry-gate blocked details can be aggregated separately

Added tests:

* `tests/test_performance_snapshot.py`

Covered cases:

1. legacy-only logs
2. new-format logs
3. mixed legacy + new logs
4. `selection_reason=highest_score` selection counting
5. entry-gate blocked-detail aggregation

---

# 3. VALIDATION

Executed:

```text
python -m unittest discover -s tests -p "test_*.py"
```

Result:

```text
Ran 16 tests
OK
```

Also confirmed from current files after fresh validation:

* `data/state.json` shows `pending_order = null`
* `data/state.json` shows `open_trade = null`
* `logs/runtime.log` ends with `NO_ENTRY_SIGNAL` on the fresh validation cycle
* `logs/portfolio.log` now includes new-format observability fields

---

# 4. OPERATIONAL INTERPRETATION

Fresh-cycle observability proof is now confirmed.

Confirmed fresh evidence:

* `blocked_detail=all_filtered`
* `candidate_count=0`
* `rejected_reasons={'market_not_trend_up': 1, 'trend_not_up': 1}`

Snapshot reflection also confirmed:

* `blocked_signal_stats.no_ranked_signal` is now stored as `{all_filtered=1, legacy=25}`

---

# 5. CURRENT STATUS

```text
OBSERVABILITY_CODE_FIX     = COMPLETE
OBSERVABILITY_TEST_FIX     = COMPLETE
FRESH_RUNTIME_PROOF        = COMPLETE
BREAKOUT_EXPERIMENT_STATUS = ALLOWED
```

---

# 6. REQUIRED NEXT STEP

Required next action:

1. start breakout_v1 first relaxation experiment
2. keep observability fields active during the experiment
3. store experiment result and rejection distribution in a dedicated report

---

## Obsidian Links

- [[CNT v2 OBSERVABILITY PRIORITY PLAN]]


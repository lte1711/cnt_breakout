# CNT v2 FRESH CYCLE OBSERVABILITY VALIDATION REPORT

```text
DOCUMENT_NAME = cnt_v2_fresh_cycle_observability_validation_report
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-20
STATUS        = PASS
REFERENCE_1   = CNT v2 OBSERVABILITY VALIDATION GATE
REFERENCE_2   = CNT v2 FRESH CYCLE OBSERVABILITY VALIDATION PLAN
```

---

# 1. EXECUTIVE SUMMARY

Fresh-cycle observability validation was executed and passed.

The new observability format is now confirmed in live runtime output.

This clears the gate for the first breakout relaxation experiment.

---

# 2. VALIDATION EVIDENCE

Fresh runtime evidence captured in `logs/portfolio.log`:

```text
[2026-04-20 00:32:46] symbol=ETHUSDT selected_strategy=NONE reason=no_ranked_signal rank_score=0.0 rank_score_components={} blocked_by_policy=no_ranked_signal blocked_detail=all_filtered total_signals=2 candidate_count=0 rejected_reasons={'market_not_trend_up': 1, 'trend_not_up': 1}
```

Confirmed fields:

* `blocked_detail=all_filtered`
* `candidate_count=0`
* `rejected_reasons={'market_not_trend_up': 1, 'trend_not_up': 1}`

Note:

* `selection_reason=highest_score` and `rank_candidates=...` were not required for PASS once one valid new-format runtime line was captured

---

# 3. SNAPSHOT CONFIRMATION

Updated `data/performance_snapshot.json` confirms mixed-format aggregation:

```text
blocked_signal_stats.no_ranked_signal = {all_filtered=1, legacy=25}
```

Interpretation:

* legacy portfolio logs remain represented
* new-format blocked-detail runtime lines are now also represented
* snapshot generation did not fail on the mixed log stream

---

# 4. TEST CONFIRMATION

Executed:

```text
python -m unittest discover -s tests -p "test_*.py"
```

Result:

```text
Ran 16 tests
OK
```

---

# 5. OPERATIONAL NOTE

During repeated manual launches, one run succeeded and additional parallel manual calls hit a scheduler log write collision while trying to record `scheduler_skip`.

Observed issue:

* `logs/scheduler_stdout.log` can be temporarily locked during overlapping manual invocations

Interpretation:

* this does not invalidate the observability PASS result
* it is a minor scheduler-wrapper operational issue and should be tracked separately if repeated

---

# 6. FINAL RESULT

```text
OBSERVABILITY_RUNTIME_PROOF = PASS
SNAPSHOT_REFLECTION         = PASS
TEST_STATUS                 = PASS
BREAKOUT_EXPERIMENT_GATE    = OPEN
```

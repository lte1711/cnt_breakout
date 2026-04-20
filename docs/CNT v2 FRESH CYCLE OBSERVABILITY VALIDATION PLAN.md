---
tags:
  - cnt
  - docs
  - observability
  - validation
  - plan
  - v2
aliases:
  - CNT v2 FRESH CYCLE OBSERVABILITY VALIDATION PLAN
---

# CNT v2 FRESH CYCLE OBSERVABILITY VALIDATION PLAN

```text
DOCUMENT_NAME = cnt_v2_fresh_cycle_observability_validation_plan
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-20
STATUS        = EXECUTED
PURPOSE       = validate new observability fields in live runtime before breakout experiment
```

---

# 1. PURPOSE

Validate that the newly added observability fields are not only implemented in code,
but are also written during fresh runtime cycles and reflected in the snapshot layer.

---

# 2. STARTING FACTS

Starting facts before validation:

* observability aggregation patch complete
* observability regression tests complete
* current `state.json` had no active pending order
* current `state.json` had no active open trade
* latest state before validation ended with `SELL_FILLED`
* `portfolio.log` had not yet stored new-format observability evidence

---

# 3. EXECUTION STEPS

STEP 1

* run `run.ps1` for 1 to 3 fresh cycles

STEP 2

* inspect `logs/portfolio.log`
* confirm at least one of:
  * `blocked_detail=...`
  * `candidate_count=...`
  * `rejected_reasons=...`
  * `rank_candidates=...`
  * `selection_reason=highest_score`

STEP 3

* inspect `data/performance_snapshot.json`
* confirm that new-format detail is reflected without parse failure

STEP 4

* if PASS, allow breakout first relaxation experiment

---

# 4. PASS RULE

```text
fresh runtime evidence >= 1
snapshot regeneration = normal
test suite = still passing
```

---

# 5. RESULT

```text
RESULT = PASS
NEXT   = breakout_v1 first relaxation experiment
```

---

## Obsidian Links

- [[00 CNT Vault Home|Vault Home]]
- [[00 Docs Index|Docs Index]]

### Related
- [[00 Docs Index|Docs Index]]

---
tags:
  - cnt
  - docs
  - observability
  - plan
  - v2
aliases:
  - CNT v2 OBSERVABILITY PRIORITY PLAN
---

# CNT v2 OBSERVABILITY PRIORITY PLAN

```text
DOCUMENT_NAME = cnt_v2_observability_priority_plan
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-19
STATUS        = APPROVED_NEXT_STEP
ROLE          = PRIORITY_GUIDANCE
```

---

# 1. CURRENT INTERPRETATION

The project is now in a different state than earlier planning phases.

Current meaning:

* baseline behavior is frozen by tests
* runtime evidence is accumulating
* the next constraint is no longer "can it run?"
* the next constraint is "why is a strategy being rejected or not selected?"

---

# 2. PRIORITY DECISION

Confirmed priority order:

```text
PRIORITY_1 = OBSERVABILITY
PRIORITY_2 = BREAKOUT ACTIVATION EXPERIMENT
PRIORITY_3 = STATE STATUS SEMANTIC CLEANUP
PRIORITY_4 = ENGINE DECOMPOSITION
```

Why `OBSERVABILITY` is first:

* breakout is currently generated but not selected
* `no_ranked_signal` is still too coarse as a diagnosis source
* decomposition before better observability would make diagnosis harder, not easier

---

# 3. REQUIRED OBSERVABILITY ADDITIONS

The next implementation step should capture:

1. strategy-level rejection reasons
2. ranker candidate inputs and score components
3. final selection reason and candidate count
4. `no_ranked_signal` subcategories such as:
   * `no_candidate`
   * `all_filtered`

---

# 4. WHAT THIS ENABLES

After the observability layer is added, the project will be able to answer:

* whether `breakout_v1` is truly weak or merely over-filtered
* whether the ranking stage is the bottleneck or the signal-generation stage is the bottleneck
* whether selection scarcity comes from policy blocks or from strategy entry rejection

---

# 5. CURRENT DECISION

```text
NEXT_IMPLEMENTATION = OBSERVABILITY_LAYER
BREAKOUT_TUNING     = DEFER_UNTIL_MORE_VISIBILITY_EXISTS
ENGINE_SPLIT        = DEFER_UNTIL_MORE_VISIBILITY_EXISTS
```

---

## Obsidian Links

- [[00 CNT Vault Home|Vault Home]]
- [[00 Docs Index|Docs Index]]

### Related
- [[00 Docs Index|Docs Index]]

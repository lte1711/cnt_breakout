---
tags:
  - cnt
  - docs
  - plan
  - v2
aliases:
  - CNT v2 ENGINEERING PHASE PLAN
---

# CNT v2 ENGINEERING PHASE PLAN

```text
DOCUMENT_NAME = cnt_v2_engineering_phase_plan
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-19
STATUS        = ACTIVE_ENGINEERING_SEQUENCE
ROLE          = ENGINEERING_PHASE_GUIDANCE
```

---

# 1. CONTEXT

The Unicode filename cleanup is treated as a meaningful stabilization step.

Practical interpretation:

* environment and path risk moved down
* the project can now shift from structure-definition mode into engineering mode

Current high-priority risk order:

1. strategy validation insufficiency
2. missing fine-grained observability
3. oversized `src/engine.py`

---

# 2. SAVED PRIORITY ORDER

The accepted execution order is:

```text
1. tests
2. observability
3. breakout experiment
4. status semantic cleanup
5. engine decomposition
```

Recommended path:

```text
SAFE_PATH = TESTS -> OBSERVATION -> EXPERIMENT -> REFACTOR
```

Fast path of immediate engine decomposition is explicitly treated as higher-risk.

---

# 3. IMMEDIATE STEP

The completed first step from this plan is:

```text
TEST HARNESS ADDITION
```

Minimum expected files:

* `tests/test_signal_ranker.py`
* `tests/test_live_gate.py`
* `tests/test_exit_manager.py`
* `tests/test_engine_cycle_smoke.py`

Purpose:

* freeze current behavior
* reduce refactor regression risk
* make later engine decomposition safer

---

# 4. FOLLOW-UP AFTER TESTS

After the first test harness lands:

* add richer rejection observability for strategy-selection failures
* run controlled `breakout_v1` activation experiments on testnet only
* start extraction work against the engine decomposition design

Confirmed next execution order:

```text
NEXT_1 = OBSERVABILITY
NEXT_2 = BREAKOUT_EXPERIMENT
NEXT_3 = STATUS_SEMANTIC_CLEANUP
NEXT_4 = ENGINE_DECOMPOSITION
```

---

# 5. CURRENT DECISION

```text
ENGINEERING_PHASE = STARTED
CURRENT_STEP      = OBSERVABILITY
REFACTOR          = DEFERRED_UNTIL_BASELINE_IS_TESTED
```

---

## Obsidian Links

- [[00 CNT Vault Home|Vault Home]]
- [[00 Docs Index|Docs Index]]

### Related
- [[00 Docs Index|Docs Index]]

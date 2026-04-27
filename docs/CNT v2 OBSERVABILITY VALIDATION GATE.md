---
tags:
  - cnt
  - type/documentation
  - status/active
  - type/validation
  - offline-experiment
  - type/operation
  - strategy/breakout_v3
  - status/completed
  - cnt-v2-observability-validation-gate
---

# CNT v2 OBSERVABILITY VALIDATION GATE

```text
DOCUMENT_NAME = cnt_v2_observability_validation_gate
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-20
STATUS        = PASS
PURPOSE       = lock observability interpretation before breakout experiment
```

---

# 1. DECISION

Breakout relaxation experiment is conditionally allowed.

It is not allowed to change breakout parameters yet.

Required order:

```text
observability implementation
-> observability aggregation correction
-> observability regression tests
-> 1 to 3 fresh cycles with new-format evidence
-> breakout_v1 relaxation experiment
```

---

# 2. REQUIRED PRECONDITIONS

The following items must be completed before breakout parameter changes:

1. `performance_snapshot.py` must count `selected_strategy_counts` from selection logs only
2. mixed old/new portfolio log parsing must remain stable
3. observability regression tests must pass
4. fresh runtime evidence must include at least one new-format log line

Required fresh runtime evidence:

* `blocked_detail=...`
* `candidate_count=...`
* `rejected_reasons=...`
* `rank_candidates=...`
* or `selection_reason=highest_score`

---

# 3. CURRENT FACTS

Current confirmed facts:

* observability code changes are present
* observability tests pass
* the previous pending SELL state has already been resolved
* fresh runtime evidence has now been captured

Current runtime facts:

* `data/state.json` currently shows `pending_order = null`
* `data/state.json` currently shows `open_trade = null`
* latest stored cycle before validation had closed with `SELL_FILLED`
* fresh validation cycle recorded new observability fields in `logs/portfolio.log`

Implication:

* the previous blocking explanation is no longer current
* STEP 3 fresh runtime proof is now confirmed
* breakout experiment gate is cleared

---

# 4. BREAKOUT EXPERIMENT RULE

Only after the gate is cleared may the first breakout relaxation experiment begin.

Allowed first experiment values:

* `atr_expansion_multiplier: 1.2 -> 1.05`
* `rsi_threshold: 55 -> 53`

Not allowed:

* `atr_expansion_multiplier = 1.0`

Reason:

* current strategy validation requires `atr_expansion_multiplier > 1.0`

---

# 5. PASS / RESULT

```text
STEP 1 = PASS when selection counting and blocked-detail parsing are corrected
STEP 2 = PASS when regression tests pass
STEP 3 = PASS when fresh runtime evidence is captured
CURRENT_RESULT = STEP 1 PASS / STEP 2 PASS / STEP 3 PASS
BREAKOUT_EXPERIMENT = ALLOWED
```

---

## Obsidian Links

- [[00 Docs Index]]


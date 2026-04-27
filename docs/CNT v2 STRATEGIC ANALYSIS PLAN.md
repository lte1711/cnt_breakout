---
tags:
  - cnt
  - type/documentation
  - status/active
  - offline-experiment
  - type/operation
  - strategy/pullback_v1
  - strategy/breakout_v3
  - cnt-v2-strategic-analysis-plan
---

# CNT v2 STRATEGIC ANALYSIS PLAN

```text
DOCUMENT_NAME = cnt_v2_strategic_analysis_plan
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-19
STATUS        = SAVED_AS_PLANNING_REFERENCE
SOURCE_1      = user-provided strategic analysis text
SOURCE_2      = user-referenced PDF plan (정밀 분석 총평.pdf)
ROLE          = PLANNING_DOCUMENT_NOT_RUNTIME_TRUTH
```

---

# 1. DOCUMENT ROLE

This document stores the current high-level strategic analysis as a planning reference.

Interpretation rule:

* repository code, runtime state, and logs remain the primary source of truth
* this document and the referenced PDF are planning / interpretation / prioritization inputs
* any statement here must be treated as a proposal unless confirmed by code or runtime evidence

---

# 2. CURRENT FACT BASELINE

Current repository/runtime facts reflected at the time of saving:

* the project is a one-shot scheduled engine, not a daemon loop
* `live_gate_decision` is still `NOT_READY / INSUFFICIENT_SAMPLE`
* `pullback_v1` is the only strategy with real closed-trade evidence
* `breakout_v1` generates signals but has not yet produced selected/closed trade evidence
* `mean_reversion_v1` remains registered but inactive
* exit handling is structurally stronger than entry selection at this stage
* the largest current technical-debt area is still `src/engine.py`

---

# 3. STORED STRATEGIC CONCLUSIONS

The planning conclusions being preserved are:

1. Phase A: keep the current engine stable and prioritize sample accumulation first
2. Phase B: begin `engine.py` decomposition only after enough observation evidence is secured
3. Phase C: clarify state-model responsibilities between cycle state, portfolio state, and analytics state
4. Phase D: treat `breakout_v1` as an experiment strategy until activation evidence is collected

Operational interpretation:

* main working strategy: `pullback_v1`
* experiment strategy: `breakout_v1`
* inactive strategy: `mean_reversion_v1`

---

# 4. IMMEDIATE PRIORITY ORDER

The priority order saved from the analysis is:

```text
1. accumulate more closed-trade evidence
2. test limited breakout activation relaxations on testnet only
3. start engine decomposition design
4. avoid live-readiness escalation until sample threshold is reached
```

---

# 5. CONSTRAINTS

This planning document does not authorize:

* live deployment
* broad risk parameter retuning
* disruptive pullback logic rewrites
* multi-symbol or multi-position expansion

This planning document does support:

* observation-first operation
* controlled breakout test adjustments on testnet
* engine modularization design work
* clearer state semantics

---

# 6. NEXT STEP LINK

The next concrete follow-up from this planning document is:

```text
CNT v2 ENGINE DECOMPOSITION DESIGN
```

---

## Obsidian Links

- [[00 Docs Index]]


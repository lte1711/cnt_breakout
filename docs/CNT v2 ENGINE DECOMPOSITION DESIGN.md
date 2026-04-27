---
tags:
  - cnt
  - type/documentation
  - status/active
  - market-context
  - context-filter
  - type/operation
  - risk
  - cnt-v2-engine-decomposition-design
---

# CNT v2 ENGINE DECOMPOSITION DESIGN

```text
DOCUMENT_NAME = cnt_v2_engine_decomposition_design
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-19
STATUS        = DESIGN_READY
GOAL          = REDUCE_ENGINE_SIZE_WITHOUT_BREAKING_RUNTIME_RULES
```

---

# 1. DESIGN GOAL

Current issue:

* `src/engine.py` owns too many responsibilities
* this increases regression risk and makes runtime reasoning expensive

Design goal:

* keep the existing entry chain and runtime truth rules intact
* move orchestration details into smaller services
* preserve one-shot scheduler execution model
* reduce `engine.py` toward coordinator-only responsibility

Target interpretation:

```text
engine.py = cycle coordinator
services  = domain behavior owners
```

---

# 2. PROPOSED SPLIT

## 2.1 Pending Reconciliation Service

Proposed file:

* `src/services/pending_reconciliation_service.py`

Ownership:

* normalize pending order state
* exchange-side order lookup
* buy fill promotion
* sell fill resolution
* stale / invalid pending cleanup
* pending status classification

Inputs:

* symbol
* pending order
* open trade

Outputs:

* action
* pending_after
* open_trade_after
* fill_order

---

## 2.2 Trade Lifecycle Service

Proposed file:

* `src/services/trade_lifecycle_service.py`

Ownership:

* open-trade normalization
* runtime field updates
* `highest_price_since_entry`
* `entry_time`
* close pnl estimation
* strategy metrics updates
* risk metrics updates

Inputs:

* open trade
* fill price
* timestamp
* strategy metrics
* risk metrics

Outputs:

* updated open trade
* updated strategy metrics
* updated risk metrics
* close summary payload

---

## 2.3 Execution Service

Proposed file:

* `src/services/execution_service.py`

Ownership:

* entry order submit
* target/time/partial limit submit
* protective market submit
* pending cancel before protective override
* order response normalization

Inputs:

* signal / exit signal
* validated order values
* filters
* current open trade

Outputs:

* action
* pending_after
* open_trade_after
* reason

---

## 2.4 State Persistence Service

Proposed file:

* `src/services/cycle_persistence_service.py`

Ownership:

* state object normalization
* runtime log append
* portfolio state update
* snapshot generation
* report generation
* live gate save

Note:

This is not business logic. It is the cycle writeout layer.

---

# 3. ENGINE AFTER SPLIT

Expected `src/engine.py` responsibilities after decomposition:

1. load current state
2. run prechecks
3. call pending reconciliation service
4. call open-trade reconciliation service
5. call exit evaluation / execution service
6. call signal orchestration / entry decision
7. call persistence service
8. handle top-level exceptions

This means the engine remains the coordinator, but no longer owns detailed reconciliation and execution internals.

---

# 4. PROPOSED MIGRATION ORDER

Recommended order:

```text
Step 1. extract pending reconciliation service
Step 2. extract trade lifecycle service
Step 3. extract execution service
Step 4. extract persistence/update service
Step 5. shrink engine.py to coordinator form
```

Reason:

* pending reconciliation is already clearly bounded
* trade lifecycle math and metrics are separable
* execution logic is the most sensitive area and should move only after helpers exist
* persistence should be extracted last so runtime side effects stay stable during earlier refactors

---

# 5. SAFETY RULES FOR THE REFACTOR

The decomposition must not change:

* entry chain: `run.ps1 -> main.py -> src.engine.start_engine`
* one-shot scheduler model
* exchange-truth-over-local-state rule
* single-position current operating rule
* live gate thresholds
* existing strategy contracts

The decomposition should preserve runtime outputs:

* `state.json`
* `portfolio_state.json`
* `strategy_metrics.json`
* `performance_snapshot.json`
* `live_gate_decision.json`
* `runtime.log`
* `portfolio.log`

---

# 6. STATE-SEMANTIC FOLLOW-UP

One design follow-up worth scheduling after decomposition:

`state.status` should become semantically clearer.

Candidate future values:

* `cycle_completed`
* `waiting_next_schedule`
* `error`
* `pending_reconcile`
* `open_trade_active`

This is not required for the first decomposition pass, but it is a good follow-up after responsibilities are separated.

---

# 7. CURRENT DECISION

```text
DECOMPOSITION = DESIGN_READY
IMPLEMENTATION = NOT_STARTED
PREREQUISITE  = KEEP COLLECTING TESTNET EVIDENCE WHILE REFACTORING CAREFULLY
```

---

## Obsidian Links

- [[CNT v2 VALIDATION REPORT]]


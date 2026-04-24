---
aliases:
  - CNT v2 VALIDATION REPORT
---

﻿# CNT v2 VALIDATION REPORT

```text
DOCUMENT_NAME = cnt_v2_validation_report
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-19
STATUS        = PATCH_PENDING_VALIDATION_BASELINE
BASELINE      = CNT v1.1 (CLOSED)
REFERENCE_1   = cnt_v2_architecture_design
REFERENCE_2   = cnt_v2_implementation_work_instruction
REFERENCE_3   = cnt_v2_validation_checklist
```

---

# 1. EXECUTIVE SUMMARY

CNT v2 initial implementation has been added on top of the closed CNT v1.1 baseline,
but the first validation pass left patch-required gaps between structure and runtime behavior.

Validated scope:

* multi-strategy registry expansion
* multi-strategy signal generation support
* signal ranking support
* strategy_orchestrator integration
* PositionState and PortfolioState models
* portfolio_state sidecar persistence
* portfolio risk manager integration into ExecutionDecision
* spot/futures adapter split
* dry order routing
* portfolio-level logging

---

# 2. VALIDATION RESULTS

## 2.1 Document and structure

PASS

Confirmed:

* `docs/CNT v2 ARCHITECTURE DESIGN DOCUMENT.md`
* `docs/CNT v2 IMPLEMENTATION WORK INSTRUCTION.md`
* `docs/CNT v2 VALIDATION CHECKLIST.md`
* `AGENTS.md` updated with v2 portfolio and market adapter components
* `docs/EXTRA ITEMS REGISTER.md` updated with v2-added files

---

## 2.2 Multi-strategy flow

PASS

Confirmed:

* `strategy_registry` expanded with:
  * `breakout_v1`
  * `pullback_v1`
  * `mean_reversion_v1`
* `generate_all_signals(symbol)` added
* `signal_ranker` chooses the highest-confidence valid signal
* `strategy_orchestrator` returns a single selected signal

Activation note:

* default active strategies in runtime are `breakout_v1` and `pullback_v1`
* `mean_reversion_v1` is registered and parameterized, but remains inactive by default in the current baseline

Observed synthetic ranking result:

```text
selected= pullback_v1 0.8
```

---

## 2.3 Portfolio risk

PARTIAL

Confirmed:

* `portfolio_risk_manager.check_portfolio_risk(...)` added
* `execution_decider.decide_execution(...)` now accepts `portfolio_state`
* portfolio rejection reasons are available in `ExecutionDecision`

Observed synthetic results:

```text
exposure= (False, 'MAX_PORTFOLIO_EXPOSURE_EXCEEDED')
one_per_symbol= (False, 'ONE_PER_SYMBOL_POLICY')
```

Patch note:

* initial v2 build used a surrogate exposure quantity in the first implementation
* this section must not be read as portfolio risk policy fully accurate in runtime until patch validation is completed

---

## 2.4 State persistence

PASS

Confirmed:

* v1.1 runtime state remains at `schema_version=1.0`
* v2 sidecar state persists independently at `schema_version=2.0`

Observed v2 sidecar state:

```json
{
  "schema_version": "2.0",
  "total_exposure": 0.0,
  "open_positions": [],
  "cash_balance": 0.0,
  "daily_loss_count": 0,
  "consecutive_losses": 0
}
```

---

## 2.5 Market adapter

PARTIAL

Confirmed:

* `spot_adapter.submit_order(...)` exists
* `futures_adapter.submit_order(...)` exists
* `execution/order_router.py` routes by market type in dry validation scope

Observed dry routing results:

```text
{'market': 'spot', 'dry_run': True, 'payload': {'symbol': 'ETHUSDT', 'side': 'BUY'}}
{'market': 'futures', 'dry_run': True, 'payload': {'symbol': 'ETHUSDT', 'side': 'BUY', 'leverage': 1, 'margin_mode': 'ISOLATED', 'reduce_only': False}}
```

Patch note:

* `order_router` exists as prepared routing structure
* initial v2 engine runtime path still used direct order submission functions
* therefore runtime routing must be described as `prepared but not yet connected`, not `normal` or `active`

---

## 2.6 Runtime validation

PARTIAL

Completed checks:

* `py_compile` passed for 43 files
* `main.py` and new v2 modules imported successfully
* actual one-shot safe runtime validation completed through `run.ps1`

Safe runtime method:

* temporary `STRATEGY_ENABLED=False`
* run via normal entry chain
* confirm no order path
* restore `STRATEGY_ENABLED=True`

Observed runtime result:

```text
action=NO_ENTRY_SIGNAL
reason=no_ranked_signal
```

Observed portfolio log result:

```text
[2026-04-19 08:47:43] symbol=ETHUSDT selected_strategy=NONE reason=no_ranked_signal
```

Patch note:

* this runtime check confirmed entry-chain continuity and safe no-entry behavior
* it did not, by itself, prove operating readiness for pending reconciliation, routed execution, or loss-policy enforcement

---

## 2.7 Regression validation

PASS

Confirmed baseline preservation:

* `StrategySignal`, `ExecutionDecision`, and `ExitSignal` contracts remain usable
* v1.1 state persistence remains active
* Stage 1 and Stage 2 modules still import and compile
* v1.1 exit paths were not structurally removed

---

# 3. FINAL DECISION

```text
Document and structure: PASS
Multi-strategy flow: PASS
Portfolio risk: PARTIAL
State persistence: PASS
Market adapter: PARTIAL
Runtime validation: PARTIAL
Regression validation: PASS
```

```text
CNT v2 initial implementation complete as a structural baseline
Not approved for operating-readiness claims before mandatory patch completion
```

---

# 4. FORMAL CONCLUSION

CNT v2 initial implementation is a working upper-layer extension over CNT v1.1,
but it must be treated as patch-pending rather than operating-ready.

The current result confirms:

* multiple strategy candidates can be generated and ranked
* portfolio-level risk rejection is structurally separated from single-position risk logic
* portfolio state is persisted independently from the v1.1 runtime state
* spot/futures execution structure is adapter-based and dry-routable, but not yet the active runtime submission path
* the closed v1.1 baseline remains intact inside the validated scope

---

## Obsidian Links

- [[00 Docs Index]]


---
tags:
  - cnt
  - type/documentation
  - status/active
  - type/validation
  - type/operation
  - risk
  - cnt-v2-gate-display-consistency-audit
---

# CNT v2 GATE DISPLAY CONSISTENCY AUDIT

## Scope

Compared files:

- `src/validation/live_gate_evaluator.py`
- `docs/cnt_operations_dashboard.html`

## Evaluator Rule

`live_gate_evaluator.py` currently evaluates in this order:

1. `closed_trades >= 50`
2. `expectancy > 0`
3. `net_pnl > 0`
4. `max_consecutive_losses <= 5`
5. observed risk guard trigger exists:
   - `LOSS_COOLDOWN`
   - or `DAILY_LOSS_LIMIT`

There is **no PF threshold** in the actual evaluator.

## Dashboard Gate Rule Text

The dashboard currently shows this gate rule text:

- `closed trades >= 20 · PF >= 1.1 · expectancy > 0`

The fallback `gateReady(snapshot)` function also uses:

- `closed_trades >= 50`
- `profit_factor >= 1.1`
- `expectancy > 0`

## Displayed Fail Reason Source

The dashboard does this correctly:

- `gateStatus = gate?.status ?? ...`
- `gateReason = gate?.reason ?? ...`

So when `live_gate_decision.json` exists, the displayed fail reason comes from the evaluator output, not from the dashboard fallback text.

## Confirmed Inconsistency

### 1. PF Threshold Inconsistency

Confirmed.

- evaluator does **not** require `PF >= 1.1`
- dashboard fallback and gate text still imply that it does

### 2. Net PnL Visibility Gap

Confirmed.

- evaluator fails when `net_pnl <= 0`
- dashboard gate rule text does not mention net PnL at all

### 3. Display Source Is Mostly Correct

Also confirmed.

- fail status and fail reason will still display correctly when `live_gate_decision.json` is loaded
- however, the rule explanation shown to the operator is still inconsistent with the actual evaluator

### 4. Additional Display Quality Issue

The dashboard footer still contains garbled separator characters in the runtime source line.

This is not the main logical inconsistency, but it is a remaining UI quality defect.

## Audit Result

The current situation is:

- evaluator logic = correct for current policy
- dashboard status source = mostly correct
- dashboard rule explanation = stale / inconsistent

## Required Conclusion

**gate/display consistency patch required**

## Obsidian Links

- [[CNT v2 POST-READY DEGRADATION REVIEW]]


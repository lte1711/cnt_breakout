---
aliases:
  - CNT v2 GATE DISPLAY ACTUAL PATCH SPEC
---

# CNT v2 GATE DISPLAY ACTUAL PATCH SPEC

## Compared Files

- `src/validation/live_gate_evaluator.py`
- `docs/cnt_operations_dashboard.html`

## Evaluator Actual Rule

The evaluator currently uses this real order:

1. `closed_trades >= 20`
2. `expectancy > 0`
3. `net_pnl > 0`
4. `max_consecutive_losses <= 5`
5. observed risk guard trigger exists:
   - `LOSS_COOLDOWN`
   - or `DAILY_LOSS_LIMIT`

## Dashboard Current Rule Display

The dashboard currently implies:

- `closed trades >= 20`
- `PF >= 1.1`
- `expectancy > 0`

The fallback function `gateReady(snapshot)` also uses:

- `profit_factor >= 1.1`

This is stale.

## Exact Stale Items To Remove

### Remove From Visible Rule Text

Delete the current operator-facing rule text that includes:

- `PF >= 1.1`

### Remove From Dashboard Fallback Logic

Delete the `profit_factor >= 1.1` condition from:

- `function gateReady(snapshot)`
- `function gateReasons(snapshot)`

## Final Single Source Of Truth

Adopt evaluator logic as the only valid policy source.

The dashboard should display gate state from:

- `live_gate_decision.json`

The dashboard should explain gate rules using the evaluator criteria only.

## Final Operator-Facing Wording

### Gate Rule Text

Replace current rule text with:

- `closed trades >= 20 · expectancy > 0 · net pnl > 0 · max consecutive losses <= 5 · risk guard observed`

### Gate Explanation Text

Use wording like:

- `Gate status is read from live_gate_decision.json. Runtime status must follow evaluator output, not dashboard fallback heuristics.`

### Fail Reason Text

When fail occurs, prefer:

- `Current fail reason: NON_POSITIVE_EXPECTANCY`

## Should Fallback Stay

Fallback can remain only as a defensive last resort if `live_gate_decision.json` cannot be loaded.

If fallback remains:

- it must mirror evaluator policy exactly
- it must not use a separate PF threshold

## Additional UI Cleanup

Also patch:

- garbled footer separator characters

Recommended footer text:

- `CNT runtime sources: snapshot · metrics · state · live gate`

## Patch Acceptance Criteria

1. dashboard visible gate text matches evaluator logic
2. fallback logic no longer introduces `PF >= 1.1`
3. displayed fail reason still comes from `live_gate_decision.json`
4. operator-facing wording explains net PnL and risk guard requirements

## Required Conclusion

**gate/display actual patch ready**

## Obsidian Links

- [[CNT v2 DASHBOARD PATCH TARGET MAPPING]]


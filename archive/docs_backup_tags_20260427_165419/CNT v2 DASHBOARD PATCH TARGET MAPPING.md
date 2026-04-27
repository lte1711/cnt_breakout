---
aliases:
  - CNT v2 DASHBOARD PATCH TARGET MAPPING
---

# CNT v2 DASHBOARD PATCH TARGET MAPPING

## Target File

- `docs/cnt_operations_dashboard.html`

## Patch Objective

Expose current degradation signals directly in the top dashboard area so the operator can see the current `FAIL` condition without scrolling or reading secondary panels.

## Patch Placement

### Primary Placement

Insert a **new top warning strip** inside the existing hero section:

- location: immediately below the current `Live Gate` and `System Health` cards
- host section: `<section class="hero"> ... </section>`
- recommended insertion point:
  - after the current `<div class="card">System Health</div>`
  - before the first metrics row (`Win Rate / Profit Factor / Expectancy / Net PnL`)

### Secondary Placement

Retain the existing `alerts` container inside the `System Health` card for lower-priority alerts.

Use the new top strip only for direct operator-facing fail and degradation warnings.

## Data Sources

Read only existing runtime sources already used by the dashboard:

- `../data/performance_snapshot.json`
- `../data/strategy_metrics.json`
- `../data/state.json`
- `../data/live_gate_decision.json`

No new runtime file should be introduced for this patch.

## Required Warning Conditions

### 1. FAIL Reason

Source:

- `live_gate_decision.status`
- `live_gate_decision.reason`

Condition:

- `status === "FAIL"`

Display text:

- title: `LIVE GATE FAIL`
- body: `reason = NON_POSITIVE_EXPECTANCY`

The actual reason string must come directly from `live_gate_decision.json`.

### 2. Expectancy Below Zero

Source:

- `performance_snapshot.expectancy`

Condition:

- `expectancy <= 0`

Display text:

- title: `EXPECTANCY BELOW ZERO`
- body: `current expectancy = {value}`

### 3. Net PnL Below Zero

Source:

- `performance_snapshot.net_pnl`

Condition:

- `net_pnl < 0`

Display text:

- title: `NET PNL BELOW ZERO`
- body: `current net pnl = {value}`

### 4. Profit Factor Below One

Source:

- `performance_snapshot.profit_factor`

Condition:

- `profit_factor < 1`

Display text:

- title: `PF BELOW 1`
- body: `current PF = {value}`

### 5. Daily Loss Count Reached

Source:

- `state.risk_metrics.daily_loss_count`

Condition:

- `daily_loss_count >= 3`

Display text:

- title: `DAILY LOSS COUNT REACHED`
- body: `daily_loss_count = 3`

Important:

- this is different from cumulative `DAILY_LOSS_LIMIT` runtime hits
- display both concepts separately if both are shown

### 6. Breakout Negative Expectancy

Source:

- `strategy_metrics.breakout_v1.expectancy`
- `strategy_metrics.breakout_v1.profit_factor`
- `strategy_metrics.breakout_v1.trades_closed`

Condition:

- `breakout_v1.expectancy < 0`

Display text:

- title: `BREAKOUT NEGATIVE EXPECTANCY`
- body: `expectancy = {value}, PF = {value}, trades_closed = {value}`

## Severity Mapping

- `FAIL reason`
  - severity = `bad`
- `expectancy < 0`
  - severity = `bad`
- `net_pnl < 0`
  - severity = `bad`
- `PF < 1`
  - severity = `bad`
- `daily_loss_count reached`
  - severity = `warn`
- `breakout negative expectancy`
  - severity = `warn`

## Display Priority

Top strip order:

1. `LIVE GATE FAIL`
2. `EXPECTANCY BELOW ZERO`
3. `NET PNL BELOW ZERO`
4. `PF BELOW 1`
5. `BREAKOUT NEGATIVE EXPECTANCY`
6. `DAILY LOSS COUNT REACHED`

## Non-Goals

This patch must not:

- change evaluator logic
- change runtime JSON schema
- hide existing lower-priority alerts

## Required Conclusion

**dashboard patch spec ready**

## Obsidian Links

- [[CNT DATA DASHBOARD]]


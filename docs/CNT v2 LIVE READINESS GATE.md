---
tags:
  - cnt
  - live-readiness
  - gate
  - testnet
  - status/active
  - type/documentation
  - type/validation
  - type/operation
  - risk
  - cnt-v2-live-readiness-gate
---

# CNT v2 LIVE READINESS GATE

## Purpose

This document defines the official CNT v2 live readiness gate for Binance Spot Testnet operation.

The gate is not a simple profitability check. It is a conservative operating decision that confirms all of the following from runtime evidence:

- enough closed-trade sample size
- positive expectancy
- positive net PnL
- bounded consecutive loss behavior
- observed operation of the risk protection layer

## Current Rule

The official live gate is evaluated in this order:

1. `closed_trades >= 50`
2. `expectancy > 0`
3. `net_pnl > 0`
4. `max_consecutive_losses <= 5`
5. `risk_trigger_stats` includes at least one observed risk guard trigger:
   - `LOSS_COOLDOWN`
   - `DAILY_LOSS_LIMIT`

The risk guard evidence requirement does not require both guards to trigger. At least one observed trigger is enough to prove that the protection layer is active in runtime logs and snapshot data.

## Reason Codes

- `NOT_READY / INSUFFICIENT_SAMPLE`
- `FAIL / NON_POSITIVE_EXPECTANCY`
- `FAIL / NON_POSITIVE_NET_PNL`
- `FAIL / MAX_CONSECUTIVE_LOSSES_EXCEEDED`
- `FAIL / RISK_GUARD_NOT_OBSERVED`
- `LIVE_READY / ALL_GATES_PASSED`

## Interpretation

- `NOT_READY` means the sample is still insufficient for a final readiness decision.
- `FAIL` means the sample exists, but one or more performance or protection requirements are not satisfied.
- `LIVE_READY` means the system has passed the defined evidence gate. It does not mean profit is guaranteed.

## Current Evidence Sources

The gate must be evaluated from current project evidence, not from summaries alone:

- `data/performance_snapshot.json`
- `data/live_gate_decision.json`
- `logs/runtime.log`
- `logs/portfolio.log`
- `src/validation/live_gate_evaluator.py`

## Current Status Note

As of the verified `2026-04-26 14:34:05` snapshot:

```text
closed_trades = 42
expectancy    = -0.0005784761904763167
net_pnl       = -0.024296000000005313
status        = NOT_READY
reason        = INSUFFICIENT_SAMPLE
```

The correct conclusion is that CNT v2 is still in Testnet data collection and is not live-ready by the official gate.

## Obsidian Links

- [[00 Docs Index]]
- [[CNT v2 TESTNET PERFORMANCE REPORT]]
- [[CNT_PROJECT_STATUS_REPORT_20260426]]
- [[CNT_PRECISION_ANALYSIS_REPORT_20260426]]

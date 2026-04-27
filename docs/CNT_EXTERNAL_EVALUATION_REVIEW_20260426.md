---
tags:
  - cnt
  - evaluation
  - project-status
  - strategy-review
  - status/active
  - type/documentation
  - type/validation
  - type/operation
  - risk
  - strategy/pullback_v1
  - strategy/breakout_v3
  - type/analysis
---

# CNT External Evaluation Review 20260426

## Design Summary

- Scope: review an externally supplied CNT project evaluation against the current repository evidence.
- Repository basis: local `main` synchronized with `origin/main` at commit `9c0a2e9`, with runtime data subsequently updated by the scheduler.
- Evidence sources: `data/live_gate_decision.json`, `data/performance_snapshot.json`, `data/strategy_metrics.json`, `data/auxiliary_recovery_status.json`, `data/state.json`, `data/portfolio_state.json`, `data/shadow_breakout_v3_snapshot.json`, `logs/runtime.log`, `logs/signal.log`, and source structure under `src/`.
- Safety note: no engine execution, order submission, order cancellation, or strategy parameter change was performed for this review.

## Validation Result

The supplied report is directionally correct on architecture, risk-control maturity, and the platform-like nature of CNT. However, several claims are stale or too strong under the current evidence.

Current verified status:

```text
latest_snapshot_time = 2026-04-26 11:44:04
closed_trades        = 42
open_positions       = 0
official_live_gate   = NOT_READY / INSUFFICIENT_SAMPLE
live_gate_sample_min = 50
system_expectancy    = -0.0005784761904763167
system_net_pnl       = -0.024296000000005313
pullback_v1_trades   = 39
pullback_v1_expectancy = 0.0010845641025639396
pullback_v1_profit_factor = 1.1546030388426254
breakout_v1_trades   = 3
breakout_v1_expectancy = -0.022197999999999656
breakout_v3_shadow_events = 79
breakout_v3_allowed_ratio = 0.02531645569620253
```

## Accuracy Assessment

### Correct Or Mostly Correct

- CNT is better described as a strategy validation and controlled execution platform than as a simple trading bot.
- The project has a clear stateful execution flow, separated strategy signal generation, risk/exit handling, performance snapshot generation, live gate evaluation, scheduler operation, and dashboard/reporting.
- The live gate concept is a real operating control layer.
- Shadow observation exists and is being used for breakout strategy research without making it the active execution path.
- The system is structurally strong relative to a simple personal trading bot.
- The aggregate system performance is currently not acceptable for live readiness.
- Adding more architecture before resolving strategy quality would be the wrong priority.

### Needs Correction

- The report says `closed_trades = 41`; current evidence says `closed_trades = 42`.
- The report says live gate is `FAIL / NON_POSITIVE_EXPECTANCY`; current evidence says `NOT_READY / INSUFFICIENT_SAMPLE` because the official minimum sample is now 50 closed trades.
- The report says "strategy itself is unprofitable, confirmed." This is too broad. Aggregate system performance is negative, but `pullback_v1` alone remains positive by current metrics. `breakout_v1` is the major negative contributor.
- The report says gate is excessive because samples can fail early. This was addressed by changing the live gate threshold to 50; the evaluator now returns `NOT_READY` before expectancy failure when sample is insufficient.
- The report says breakout observation needs 20 to 30 events; current breakout v3 shadow count is already 79 events, though the allowed ratio remains low.

### Unsupported Or Inferred

- Claims about current BTC/ETH market regime are not proven from repository evidence alone.
- Claims about ML/adaptive absence being a direct weakness are conceptually plausible but not required by the current AGENTS-defined CNT operating model.
- "Well-built failing system" is a useful shorthand, but the fact-based version is narrower: the aggregate system is not live-ready, while active pullback-only recovery evidence is positive but statistically incomplete.

## Progress Evaluation

Current project phase:

```text
status = ACTIVE_TESTNET_OBSERVATION
official_readiness = NOT_READY
primary_blocker = sample_count_below_50
secondary_blocker = aggregate_expectancy_negative
active_runtime_strategy = pullback_v1
current_position_state = no pending order, no open trade
risk_state = daily_loss_count=3, consecutive_losses=1
```

Architecture progress:

- Execution chain and state machine are implemented.
- Strategy abstraction and ranking are implemented.
- Risk guard and portfolio risk guard are implemented.
- Deterministic exit flow is implemented.
- Performance snapshot, report generation, live gate decision, and auxiliary recovery status are implemented.
- Dashboard data sources are aligned to the official 50-trade live gate threshold.

Strategy progress:

- `pullback_v1` is currently the only active runtime strategy.
- `pullback_v1` has positive expectancy and profit factor but has only 39 closed trades, below the 50-trade recovery sample requirement.
- `breakout_v1` has negative contribution and remains the main aggregate drag.
- `breakout_v3_shadow` has enough events for bottleneck diagnosis, but only 2 of 79 events are allowed, so it is not yet an execution candidate.

## Recommended Next Actions

1. Continue observation until `pullback_v1` reaches at least 50 closed trades.
2. Keep official live gate at `closed_trades >= 50`; do not loosen it again.
3. Do not add structural layers before the strategy question is resolved.
4. Analyze the last 39 `pullback_v1` closed trades by exit type, entry reason, market state, and loss clustering.
5. Keep breakout v3 in shadow mode and use its blocker distributions to simplify the setup gate before considering activation.
6. Treat aggregate live readiness separately from pullback-only recovery evidence until an explicit documented policy approves a strategy-isolated gate.

## Record Text

The supplied evaluation is broadly correct about CNT's identity and architecture, but stale on the latest live gate status and too strong in its conclusion that the strategy is confirmed unprofitable. The official system remains not live-ready. The correct current reason is insufficient sample under the 50-trade gate, with negative aggregate expectancy as a secondary concern. The most accurate conclusion is:

```text
CNT is a structurally mature testnet strategy validation platform.
The aggregate system is not live-ready.
pullback_v1 shows positive but statistically incomplete recovery evidence.
breakout_v1 is the confirmed negative contributor.
breakout_v3 remains a shadow research candidate, not an execution candidate.
```

Related documents:

- [[CNT_LIVE_GATE_THRESHOLD_50_UPDATE_20260426]]
- [[CNT_PROJECT_STATUS_REPORT_20260426]]
- [[CNT v2 TESTNET PERFORMANCE REPORT]]
- [[CNT v2 LIVE READINESS GATE]]
- [[CNT_AUXILIARY_RECOVERY_STATUS_IMPLEMENTATION_20260425]]

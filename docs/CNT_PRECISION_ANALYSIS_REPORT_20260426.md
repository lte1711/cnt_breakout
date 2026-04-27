---
tags:
  - cnt
  - precision-analysis
  - runtime
  - testnet
  - status/active
  - evidence_time:-2026-04-26-14:34:05
  - type/documentation
  - type/validation
  - type/operation
  - risk
  - strategy/pullback_v1
  - strategy/breakout_v3
  - type/analysis
---

# CNT Precision Analysis Report 20260426

## Design Summary

- Scope: CNT Binance Spot Testnet runtime, performance, live gate, risk guard, strategy attribution, shadow strategy, and test status.
- Runtime entry chain was not executed manually for this report.
- No order submission, cancellation, engine code change, or runtime configuration change was performed.
- Evidence sources: `data/state.json`, `data/portfolio_state.json`, `data/performance_snapshot.json`, `data/live_gate_decision.json`, `data/strategy_metrics.json`, `data/auxiliary_recovery_status.json`, `data/scheduler_heartbeat.json`, `data/shadow_breakout_v3_snapshot.json`, `logs/runtime.log`, `logs/portfolio.log`, `logs/signal.log`, `docs/CNT v2 TESTNET PERFORMANCE REPORT.md`, `src/validation/live_gate_evaluator.py`, `src/risk/risk_guard.py`, and local test execution.
- Report rule: FACT means directly observed from files/logs/tests. VERIFIED means cross-checked across at least two project evidence sources. UNKNOWN means not verified in this report.

## Executive Judgment

VERIFIED: CNT is operational and collecting scheduled testnet data, but it is not live-ready under the official gate.

VERIFIED: The immediate blocker is not a broken runtime. The system is currently flat because the risk guard is doing its job after the daily loss count reached the configured limit.

VERIFIED: The aggregate strategy set remains below live readiness because total sample size is still `42 < 50` and aggregate expectancy/net PnL are negative. The negative aggregate result is primarily attributable to `breakout_v1`, while `pullback_v1` is positive but still below the approved recovery sample threshold.

## Runtime State

FACT:

```text
last_run_time          = 2026-04-26 14:34:01
scheduler_finish_time  = 2026-04-26 14:34:05
scheduler_exit_code    = 0
scheduler_gap_detected = false
symbol                 = ETHUSDT
active_strategy        = pullback_v1
last_action            = EXECUTION_BLOCKED_BY_RISK
last_action_reason     = DAILY_LOSS_LIMIT
pending_order          = none
open_trade             = none
open_positions_count   = 0
total_exposure         = 0.0
state_price            = 2329.6
```

VERIFIED: `data/state.json` and `data/portfolio_state.json` agree that there is no local pending order, no open trade, and zero portfolio exposure.

UNKNOWN: This report did not re-run signed Binance Spot Testnet open-order/account queries. The earlier same-day project status report retained historical read-only exchange verification, but this precision report only verifies local evidence.

## Risk Guard Analysis

FACT:

```text
MAX_DAILY_LOSS_COUNT     = 3
LOSS_COOLDOWN_MINUTES    = 60
state_daily_loss_count   = 3
portfolio_daily_loss_cnt = 3
state_consecutive_losses = 1
portfolio_consec_losses  = 1
last_loss_time           = 2026-04-26 10:14:01
```

VERIFIED: `src/risk/risk_guard.py` blocks entries when `daily_loss_count >= MAX_DAILY_LOSS_COUNT`. `config.py` sets `MAX_DAILY_LOSS_COUNT = 3`. Current state has `daily_loss_count = 3`, so `DAILY_LOSS_LIMIT` is the expected result.

FACT from log counts:

```text
runtime_action_lines          = 926
execution_blocked_by_risk     = 205
daily_loss_limit_runtime_hits = 200
loss_cooldown_runtime_hits    = 5
no_entry_signal_runtime_hits  = 408
portfolio_daily_loss_blocks   = 200
portfolio_loss_cooldown_blocks= 5
```

Interpretation:

- VERIFIED: The risk layer is not a secondary issue; it is the current execution governor.
- VERIFIED: After the latest protective stop, valid `pullback_v1` signals still appeared, but execution was blocked by `DAILY_LOSS_LIMIT`.
- FACT: The latest portfolio log at `2026-04-26 14:34:05` selected `pullback_v1` with rank score `0.8048990271740948`, then blocked it by `DAILY_LOSS_LIMIT`.

## Live Gate Analysis

FACT:

```text
official_gate_status = NOT_READY
official_gate_reason = INSUFFICIENT_SAMPLE
closed_trades        = 42
min_required_sample  = 50
expectancy           = -0.0005784761904763167
net_pnl              = -0.024296000000005313
profit_factor        = 0.9313887453369003
max_consecutive_loss = 5
```

VERIFIED: `src/validation/live_gate_evaluator.py` requires `closed_trades >= 50` before evaluating positive expectancy, positive net PnL, max consecutive losses, and observed risk guard triggers. Because current `closed_trades = 42`, the official decision must stop at `NOT_READY / INSUFFICIENT_SAMPLE`.

Interpretation:

- FACT: The gate is not failed by final pass/fail conditions yet; it is not ready by sample size.
- VERIFIED: Even if sample size were ignored, current aggregate expectancy and net PnL are negative, so the aggregate system would still not justify live readiness.

## Strategy Attribution

FACT:

```text
aggregate_closed_trades = 42
aggregate_wins          = 21
aggregate_losses        = 21
aggregate_win_rate      = 0.5000
aggregate_net_pnl       = -0.024296

pullback_v1_closed      = 39
pullback_v1_wins        = 20
pullback_v1_losses      = 19
pullback_v1_win_rate    = 0.5128205128
pullback_v1_expectancy  = 0.0010845641
pullback_v1_profit_fact = 1.1546030388
pullback_v1_net_pnl     = 0.042298

breakout_v1_closed      = 3
breakout_v1_wins        = 1
breakout_v1_losses      = 2
breakout_v1_win_rate    = 0.3333333333
breakout_v1_expectancy  = -0.022198
breakout_v1_profit_fact = 0.1729508197
breakout_v1_net_pnl     = -0.066594
```

VERIFIED: `pullback_v1` has positive expectancy, positive net PnL, and profit factor above `1.1`. `breakout_v1` has strongly negative expectancy and explains the aggregate negative net PnL.

Derived from verified metrics:

```text
pullback_trade_share    = 39 / 42 = 92.86%
breakout_trade_share    = 3 / 42  = 7.14%
pullback_selection_rate = 231 / 644 = 35.87%
breakout_selection_rate = 16 / 550  = 2.91%
```

Interpretation:

- VERIFIED: The system's viable candidate is currently `pullback_v1`, not the combined strategy set.
- VERIFIED: `breakout_v1` should remain non-authoritative for readiness decisions unless separately redesigned or isolated.
- FACT: The auxiliary recovery evaluator agrees that `pullback_v1` is positive but not statistically valid yet because its sample is `39 < 50`.

## Trade Outcome Pattern

FACT from `logs/portfolio.log` close actions:

```text
target_exit_filled_count = 21
stop_market_filled_count = 21
```

Interpretation:

- FACT: The aggregate win/loss count is exactly balanced.
- VERIFIED: The aggregate negative expectancy comes from loss size being larger than win size, not from win rate alone.
- FACT: Aggregate `avg_win = 0.015705`, `avg_loss = 0.016862`.

## Breakout V3 Shadow Analysis

FACT:

```text
strategy                 = breakout_v3_shadow
signal_count             = 96
allowed_signal_count     = 3
allowed_signal_ratio     = 0.03125
expanded_event_count     = 96
min_soft_pass_required   = 3
soft_total_count         = 6
last_updated             = 2026-04-26T14:34:04+09:00
```

FACT:

```text
first_blockers:
  setup_not_ready        = 27
  breakout_not_confirmed = 10
  market_not_trend_up    = 56

stage_pass_counts:
  regime                 = 40
  trigger                = 29
  quality                = 21
  setup                  = 12

stage_fail_counts:
  regime                 = 56
  trigger                = 67
  quality                = 75
  setup                  = 84
```

Interpretation:

- VERIFIED: `breakout_v3_shadow` is still mostly blocked before execution readiness.
- FACT: The dominant hard blocker is `market_not_trend_up`, followed by `setup_not_ready`.
- VERIFIED: Setup is the weakest stage: only `12 / 96` events pass setup.
- Practical implication: `breakout_v3` is not ready to replace or compete with `pullback_v1`; it remains an observation candidate.

## Test And Code Health

FACT:

```text
plain_pytest_q_result         = fail at collection
plain_pytest_failure_reason   = ModuleNotFoundError: No module named 'src'
PYTHONPATH_dot_pytest_result  = 63 passed in 0.28s
```

Interpretation:

- VERIFIED: Current test logic passes when repository root is placed on `PYTHONPATH`.
- FACT: Default test invocation is fragile because import path setup is not self-contained.
- Risk: CI or a different shell may report false failure unless `PYTHONPATH=.` or equivalent pytest path configuration is standardized.

## Key Risks

1. VERIFIED: Official live readiness is blocked by insufficient aggregate sample: `42 / 50`.
2. VERIFIED: Aggregate expectancy and net PnL are negative.
3. VERIFIED: `breakout_v1` is dragging aggregate performance despite small trade count.
4. VERIFIED: Current execution is intentionally halted by `DAILY_LOSS_LIMIT`.
5. FACT: Default `pytest -q` fails without explicit import path setup.
6. UNKNOWN: Current exchange-side open orders and account balances were not re-queried during this report.
7. FACT: `docs/CNT v2 LIVE READINESS GATE.md` appears mojibake-corrupted in the local readout, although the code implementation of the gate is clear.

## Recommended Next Actions

1. Continue scheduled data collection without changing live/order behavior until official sample reaches at least `50` closed trades.
2. Treat `pullback_v1` recovery as observational until `pullback_v1.closed_trades >= 50`.
3. Keep `breakout_v1` excluded from any positive readiness interpretation unless a documented redesign/retirement decision is made.
4. Do not promote `breakout_v3_shadow`; continue shadow observation and focus analysis on setup-stage failure causes.
5. Standardize test invocation by adding an approved pytest path configuration or documenting `PYTHONPATH=.` as the required local validation command.
6. Re-run read-only exchange reconciliation before any activation decision, because this report did not verify exchange-side state.
7. Repair or regenerate the mojibake-corrupted live readiness gate document from the verified code rule and current policy.

## Validation Result

VERIFIED:

- Scheduler: healthy at `2026-04-26 14:34:05`.
- Runtime: no pending order, no open trade, zero exposure.
- Risk guard: currently blocking by intended `DAILY_LOSS_LIMIT`.
- Live gate: `NOT_READY / INSUFFICIENT_SAMPLE`.
- Strategy attribution: `pullback_v1` positive, `breakout_v1` negative, aggregate negative.
- Tests: `63 passed` with `PYTHONPATH=.`.

UNKNOWN:

- Current exchange-side open orders/account balances were not queried in this report.
- Whether `pullback_v1` remains positive at `>= 50` closed trades is not yet knowable from the current sample.

## Record Text

CNT is functioning as a scheduled Binance Spot Testnet data-collection system, not as a live-ready system. The engine state is clean with no pending order or open trade, and the scheduler is current. The current lack of new execution is an expected consequence of the configured daily loss guard, because `daily_loss_count=3` equals `MAX_DAILY_LOSS_COUNT=3`.

The strategic center of gravity has moved to `pullback_v1`. That strategy is positive on the available sample, while `breakout_v1` is negative enough to make the aggregate system negative. However, `pullback_v1` still has only `39` closed trades, and the official aggregate gate has only `42` closed trades against a `50` trade threshold. Therefore the correct operating posture is continued observation, no live activation, and no unverified runtime change.

Related documents:

- [[CNT_PROJECT_STATUS_REPORT_20260426]]
- [[CNT v2 TESTNET PERFORMANCE REPORT]]
- [[CNT_LIVE_GATE_THRESHOLD_50_UPDATE_20260426]]
- [[CNT_AUXILIARY_RECOVERY_STATUS_IMPLEMENTATION_20260425]]
- [[CNT v2 LIVE READINESS GATE]]
- [[00 Docs Index]]

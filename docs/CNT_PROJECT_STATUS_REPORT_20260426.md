---
tags:
  - cnt
  - project-status
  - runtime
  - testnet
status: ACTIVE
created: 2026-04-26
updated: 2026-04-26 14:34:05
---

# CNT Project Status Report 20260426

## Design Summary

- Scope: CNT Binance Spot Testnet project status check.
- Entry chain was not executed manually during this check.
- No order submission, cancellation, engine code modification, or runtime configuration change was performed.
- Evidence sources for this update: `data/*.json`, `logs/*.log`, `docs/CNT v2 TESTNET PERFORMANCE REPORT.md`, and local test execution.
- Previous exchange read-only verification from the earlier same-day check is retained below as historical evidence; it was not re-run during this update.

## Validation Result

- Scheduler heartbeat is current as of `2026-04-26 14:34:05`.
- Last scheduler run finished with `exit_code=0`.
- Runtime state has no open ETHUSDT trade and no local pending order.
- Runtime state last action is `EXECUTION_BLOCKED_BY_RISK` with reason `DAILY_LOSS_LIMIT`.
- Runtime log still records no pending order and no open trade in the latest cycle.
- Binance Spot Testnet read-only verification from the earlier same-day check confirmed entry order `5046114` was `FILLED` before the later protective exit.
- Binance Spot Testnet open-order query from the earlier same-day check confirmed `open_order_count=0` at that time.
- Official live gate is now `NOT_READY` with reason `INSUFFICIENT_SAMPLE` under the corrected `closed_trades >= 50` threshold.
- Auxiliary recovery status is observational only and does not override the official gate.
- Test validation passed with `PYTHONPATH=.`: `63 passed in 0.32s`.
- Plain `pytest -q` without `PYTHONPATH=.` fails at collection because `src` is not importable in that invocation.

## Runtime Status

```text
last_run_time        = 2026-04-26 14:34:01
last_action          = EXECUTION_BLOCKED_BY_RISK
symbol               = ETHUSDT
active_strategy      = pullback_v1
pending_order        = none
open_trade_exists    = false
last_closed_order_id = 5046114
close_action         = STOP_MARKET_FILLED
close_time           = 2026-04-26 10:14:01
last_runtime_price   = 2329.6
daily_loss_count     = 3
consecutive_losses   = 1
```

## Previous Exchange Verification

```text
orderId              = 5046114
exchange_status      = FILLED
side                 = BUY
type                 = LIMIT
price                = 2318.00000000
origQty              = 0.00220000
executedQty          = 0.00220000
cummulativeQuoteQty  = 5.09960000
open_order_count     = 0
```

Account balances observed from the earlier signed read-only query:

```text
USDT free            = 9989.92814500
USDT locked          = 0.00000000
ETH free             = 1.00410000
ETH locked           = 0.00000000
```

## Performance Status

Dashboard/live-gate snapshot generated at `2026-04-26 14:34:05`:

```text
total_signals        = 1194
selected_signals     = 247
executed_trades      = 42
closed_trades        = 42
current_open_pos     = 0
wins                 = 21
losses               = 21
win_rate             = 0.5000
expectancy           = -0.000578
profit_factor        = 0.931389
net_pnl              = -0.024296
official_gate        = NOT_READY / INSUFFICIENT_SAMPLE
```

Strategy metrics after refresh:

```text
pullback_v1 closed_trades=39 wins=20 losses=19 win_rate=0.512821 expectancy=0.001085 profit_factor=1.154603 net_pnl=0.042298
breakout_v1 closed_trades=3 wins=1 losses=2 win_rate=0.333333 expectancy=-0.022198 profit_factor=0.172951
```

## Breakout V3 Shadow Status

```text
signal_count          = 96
allowed_signal_count  = 3
allowed_signal_ratio  = 0.03125
main_blockers         = setup_not_ready=27, breakout_not_confirmed=10, market_not_trend_up=56
last_updated          = 2026-04-26T14:34:04+09:00
```

## Record Text

As of the latest verified local evidence, CNT is actively collecting Binance Spot Testnet runtime data through the scheduled one-shot engine flow. The scheduler heartbeat is current, the latest scheduled run completed successfully, and the current runtime state has no pending order and no open trade.

The project is not live-ready by the official gate because the corrected minimum sample threshold is `closed_trades >= 50` and the current official sample is `42`. Aggregate expectancy also remains negative, but the evaluator stops first at `NOT_READY / INSUFFICIENT_SAMPLE`. The auxiliary recovery view remains encouraging for `pullback_v1`, but it is explicitly observational and does not override the official gate. The main forward task is continued data collection until the official aggregate gate or the approved recovery criteria can support a documented readiness decision.

Related documents:

- [[CNT v2 TESTNET PERFORMANCE REPORT]]
- [[CNT v2 LIVE READINESS GATE]]
- [[CNT_NEXT_STEP_DATA_ANALYSIS_20260425]]
- [[CNT_AUXILIARY_RECOVERY_STATUS_IMPLEMENTATION_20260425]]

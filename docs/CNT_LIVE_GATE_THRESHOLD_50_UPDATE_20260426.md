---
tags:
  - cnt
  - live-gate
  - dashboard
  - validation
  - status/active
  - type/documentation
  - type/validation
  - type/operation
  - type/analysis
---

# CNT Live Gate Threshold 50 Update 20260426

## Design Summary

- Scope: align official live gate sample threshold and dashboard target count with the 50-trade validation target.
- Reason: dashboard and official evaluator still used `closed_trades >= 20`, while recovery validation already used `min_sample_required = 50`.
- Runtime safety: no engine execution, order submission, order cancellation, strategy parameter change, or exchange write action was performed.

## Validation Result

- `src/validation/live_gate_evaluator.py` now uses `MIN_LIVE_GATE_CLOSED_TRADES = 50`.
- `docs/cnt_operations_dashboard.html` now displays and calculates live gate progress as `closed_trades / 50`.
- `scripts/standalone_dashboard.py` now uses the same 50-trade live-ready display threshold.
- `tests/test_live_gate.py` was updated for the new sample threshold.
- `data/live_gate_decision.json` was regenerated after the evaluator change.

Current regenerated official live gate:

```text
status        = NOT_READY
reason        = INSUFFICIENT_SAMPLE
closed_trades = 42
expectancy    = -0.0005784761904763167
net_pnl       = -0.024296000000005313
```

Verification commands:

```text
python -m py_compile src\validation\live_gate_evaluator.py tests\test_live_gate.py scripts\generate_performance_report.py scripts\standalone_dashboard.py
python -m unittest tests.test_live_gate
python scripts\generate_performance_report.py
```

## Record Text

The live gate target count has been corrected from `20` to `50` across the official evaluator, dashboard display, and live gate tests. With the current `closed_trades = 42`, the official gate is no longer reported as `FAIL / NON_POSITIVE_EXPECTANCY`; it is now correctly reported as `NOT_READY / INSUFFICIENT_SAMPLE` because the 50-trade minimum sample has not yet been reached.

Related documents:

- [[CNT v2 LIVE READINESS GATE]]
- [[CNT OPERATIONS DASHBOARD GUIDE]]
- [[CNT v2 TESTNET PERFORMANCE REPORT]]
- [[CNT_PROJECT_STATUS_REPORT_20260426]]

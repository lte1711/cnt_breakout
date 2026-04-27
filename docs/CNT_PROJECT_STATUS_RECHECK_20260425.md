---
tags:
  - cnt
  - status
  - validation
  - cnt-project-status-recheck-20260425
  - type/documentation
  - status/active
  - type/validation
  - type/operation
  - strategy/pullback_v1
---

# CNT PROJECT STATUS RECHECK 20260425

```text
DOCUMENT_NAME = cnt_project_status_recheck_20260425
PROJECT       = CNT
MODE          = BINANCE_SPOT_TESTNET
CHECK_TIME    = 2026-04-25 17:15:26 +09:00
GIT_HEAD      = cf224c4
STATUS        = ACTIVE_BUT_LIVE_GATE_FAIL
```

---

# 1. Design Summary

This recheck reviewed current source structure, entry-chain compliance, runtime state, strategy metrics, live gate output, shadow strategy snapshots, logs, git status, and test results.

Scope:

- repository source files under `src/`, root runtime files, `scripts/`, `tools/`, and `tests/`
- runtime truth files under `data/`
- runtime evidence logs under `logs/`
- status documents under `docs/`

No runtime setting, strategy parameter, order path, or exchange-facing code was changed.

---

# 2. Validation Result

## Source And Entry Chain

- `run.ps1 -> main.py -> src.engine.start_engine` entry chain is present.
- `main.py` only imports and calls `start_engine()`.
- `config.py` remains configured for Binance Spot Testnet with `BINANCE_BASE_URL = https://testnet.binance.vision`.
- active strategy configuration is `ACTIVE_STRATEGY = pullback_v1` and `ACTIVE_STRATEGIES = [pullback_v1]`.

## Runtime State

Verified from `data/state.json`:

- last run time = `2026-04-25 17:14:01`
- symbol = `ETHUSDT`
- last action = `NO_ENTRY_SIGNAL`
- pending order = `null`
- open trade = `null`
- daily loss count = `0`
- consecutive losses = `3`
- last loss time = `2026-04-24 04:04:00`

Verified from `data/portfolio_state.json`:

- total exposure = `0.0`
- open positions = `[]`
- cash balance = `0.0`
- source = `rebuild_from_runtime`

## Performance And Gate

Verified from `data/performance_snapshot.json`:

- total signals = `1145`
- selected signals = `225`
- executed trades = `35`
- closed trades = `35`
- wins = `18`
- losses = `17`
- win rate = `0.5142857142857142`
- expectancy = `-0.0003352571428572645`
- net pnl = `-0.011734000000004186`
- profit factor = `0.962646870632864`
- max consecutive losses = `3`

Verified from `data/live_gate_decision.json`:

- status = `FAIL`
- reason = `NON_POSITIVE_EXPECTANCY`
- closed trades = `35`
- expectancy = `-0.0003352571428572645`
- net pnl = `-0.011734000000004186`

Interpretation:

- previous `LIVE_READY` document state is no longer the current runtime truth.
- current truth is active testnet operation with no open exposure, but live gate failure due to negative aggregate expectancy.

## Strategy Breakdown

Verified from `data/strategy_metrics.json`:

- `pullback_v1`: 32 closed trades, 17 wins, 15 losses, win rate `0.53125`, expectancy `0.0017143749999998367`, profit factor `1.234828800986202`
- `breakout_v1`: 3 closed trades, 1 win, 2 losses, win rate `0.3333333333333333`, expectancy `-0.022197999999999656`, profit factor `0.17295081967214201`

Interpretation:

- `pullback_v1` remains the only positive strategy in the stored metrics.
- aggregate gate failure is driven by total portfolio performance including weak `breakout_v1` results.

## Shadow Strategy Status

Verified from `data/shadow_breakout_v2_snapshot.json`:

- signal count = `251`
- allowed signal count = `0`
- allowed signal ratio = `0.0`

Verified from `data/shadow_breakout_v3_snapshot.json`:

- signal count = `47`
- allowed signal count = `2`
- allowed signal ratio = `0.0425531914893617`
- main blockers include `market_not_trend_up`, `setup_not_ready`, and `breakout_not_confirmed`

Interpretation:

- `breakout_v2` remains fully filtered in shadow evidence.
- `breakout_v3` has limited allowed shadow signals after rebaseline, but it is not active for live execution.

## Test Result

Command:

```powershell
python -m pytest
```

Result:

- collected tests = `56`
- passed = `56`
- failed = `0`

---

# 3. Record Text

Current project status is `ACTIVE_BUT_LIVE_GATE_FAIL`.

CNT is implemented and operational as a Binance Spot Testnet one-shot engine. Source structure, entry chain, state persistence, performance snapshot generation, live gate evaluation, strategy metrics, shadow evaluators, and tests are present and currently passing.

The current runtime condition is conservative:

- no pending order
- no open trade
- no portfolio exposure
- last engine result was `NO_ENTRY_SIGNAL`
- live gate is `FAIL` because aggregate expectancy is non-positive

Recommended next operating direction:

1. Do not loosen strategy or risk parameters until the live gate failure is reviewed.
2. Treat the 2026-04-22 `LIVE_READY` document as historical, not current.
3. Continue using `data/*.json` and `logs/*.log` as the runtime truth.
4. Review whether `breakout_v1` should remain in aggregate gate calculations or be isolated from live-readiness scoring until sample quality improves.
5. Keep `pullback_v1` as the primary positive evidence path unless a separate activation decision is made.

---

# Obsidian Links

- [[00 Docs Index]]
- [[CNT v2 TESTNET PERFORMANCE REPORT]]
- [[CNT v2 CURRENT STATUS ASSESSMENT]]
- [[CNT v2 BREAKOUT V3 SHADOW OUTPUT REBASELINE REPORT]]

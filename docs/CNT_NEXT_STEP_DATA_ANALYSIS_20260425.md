---
tags:
  - cnt
  - analysis
  - next-phase
  - cnt-next-step-data-analysis-20260425
  - type/documentation
  - status/active
  - type/validation
  - type/operation
  - risk
  - strategy/pullback_v1
  - strategy/breakout_v3
  - type/analysis
---

# CNT NEXT STEP DATA ANALYSIS 20260425

```text
DOCUMENT_NAME = cnt_next_step_data_analysis_20260425
PROJECT       = CNT
MODE          = BINANCE_SPOT_TESTNET
CHECK_TIME    = 2026-04-25 17:17:41 +09:00
STATUS        = NEXT_STEP_IDENTIFIED
OFFICIAL_GATE = FAIL / NON_POSITIVE_EXPECTANCY
```

---

# 1. Design Summary

This analysis reviewed all currently accumulated runtime evidence from:

- `data/state.json`
- `data/portfolio_state.json`
- `data/strategy_metrics.json`
- `data/performance_snapshot.json`
- `data/live_gate_decision.json`
- `data/shadow_breakout_v2_snapshot.json`
- `data/shadow_breakout_v3_snapshot.json`
- `logs/runtime.log`
- `logs/portfolio.log`
- `logs/signal.log`
- `logs/shadow_breakout_v2.jsonl`
- `logs/shadow_breakout_v3.jsonl`
- existing phase reports under `docs/` and `reports/`

No strategy parameter, gate rule, risk rule, order path, signing path, or exchange-facing behavior was changed.

---

# 2. Validation Result

## Current Runtime Truth

- current symbol = `ETHUSDT`
- current active runtime strategy = `pullback_v1`
- pending order = `null`
- open trade = `null`
- last runtime action = `NO_ENTRY_SIGNAL`
- last runtime price = `2318.2`
- Binance Spot Testnet public `/api/v3/ping` check returned HTTP `200`
- Binance Spot Testnet public `/api/v3/time` check returned HTTP `200`

Interpretation:

- CNT is connected to Binance Spot Testnet.
- CNT is not currently in an active trade.
- Current one-shot engine execution is conservative and idle because no entry signal passed.

## Official Gate

Current `data/live_gate_decision.json`:

- status = `FAIL`
- reason = `NON_POSITIVE_EXPECTANCY`
- closed trades = `35`
- expectancy = `-0.0003352571428572645`
- net pnl = `-0.011734000000004186`

The official gate should remain unchanged.

## Aggregate Performance

Current `data/performance_snapshot.json`:

- total signals = `1145`
- selected signals = `225`
- executed trades = `35`
- closed trades = `35`
- wins = `18`
- losses = `17`
- win rate = `0.5142857142857142`
- profit factor = `0.962646870632864`
- max consecutive losses = `3`
- risk trigger stats = `DAILY_LOSS_LIMIT: 380`

Interpretation:

- sample size is sufficient for gate judgment.
- aggregate performance is slightly negative.
- official `LIVE_READY` cannot be restored from current aggregate evidence.

## Strategy Contribution

Current `data/strategy_metrics.json`:

### pullback_v1

- signals generated = `595`
- signals selected = `209`
- closed trades = `32`
- wins = `17`
- losses = `15`
- win rate = `0.53125`
- expectancy = `0.0017143749999998367`
- profit factor = `1.234828800986202`
- net contribution from portfolio close logs = `+0.05485999999999477`

### breakout_v1

- signals generated = `550`
- signals selected = `16`
- closed trades = `3`
- wins = `1`
- losses = `2`
- win rate = `0.3333333333333333`
- expectancy = `-0.022197999999999656`
- profit factor = `0.17295081967214201`
- net contribution from portfolio close logs = `-0.06659399999999896`

Interpretation:

- `pullback_v1` is the only positive live-performance path.
- `breakout_v1` is the main negative contaminant in aggregate gate recovery.
- `breakout_v1` has too little and too poor evidence to justify active use.

## Signal And Bottleneck Analysis

From `logs/signal.log`:

### pullback_v1

- total logged signals = `597`
- allowed = `209`
- blocked = `388`
- allowed ratio = approximately `35.0%`
- top blockers:
  - `pullback_rsi_not_in_range = 198`
  - `trend_not_up = 190`

### breakout_v1

- total logged signals = `554`
- allowed = `17`
- blocked = `537`
- allowed ratio = approximately `3.1%`
- top blockers:
  - `market_not_trend_up = 193`
  - `volatility_not_high = 117`
  - `range_without_upward_bias = 98`
  - `range_bias_up_but_entry_trend_not_up = 62`
  - `breakout_not_confirmed = 39`

Interpretation:

- `pullback_v1` is selective but not starved.
- `breakout_v1` remains structurally weak and low-throughput.
- Further loosening is not justified because the weak strategy already produced negative trade quality.

## Runtime Action Distribution

From `logs/runtime.log`:

- `NO_ENTRY_SIGNAL = 381`
- `EXECUTION_BLOCKED_BY_RISK = 190`
- `HOLD_OPEN_TRADE = 66`
- `PENDING_CONFIRMED = 35`
- `STOP_MARKET_FILLED = 22`
- `PROMOTE_TO_OPEN_TRADE = 21`
- `BUY_SUBMITTED = 20`
- `SELL_FILLED = 20`
- `BUY_FILLED = 20`
- `SELL_SUBMITTED = 14`

Primary bottlenecks:

1. no ranked signal
2. daily loss limit blocking
3. weak breakout contribution to aggregate expectancy

## Risk Guard

Evidence:

- `DAILY_LOSS_LIMIT` appeared as runtime action reason `190` times.
- performance snapshot risk trigger stats record `DAILY_LOSS_LIMIT = 380`.
- current state has `daily_loss_count = 0`, `consecutive_losses = 3`, and `last_loss_time = 2026-04-24 04:04:00`.

Interpretation:

- the risk guard is working and should not be loosened.
- the daily loss block prevented additional entries after adverse sequence evidence.
- current risk state is no longer daily-blocked, but consecutive loss history remains meaningful.

## Shadow Strategy Status

### breakout_v2

- signal count = `251`
- allowed signal count = `0`
- allowed signal ratio = `0.0`

Interpretation:

- `breakout_v2` should remain classified as failed/inactive.

### breakout_v3

- signal count = `47`
- allowed signal count = `2`
- allowed signal ratio = `0.0425531914893617`
- latest event at `2026-04-25T17:14:04+09:00` had regime and setup passing, but trigger blocked by `breakout_not_confirmed`.

Interpretation:

- `breakout_v3` is structurally better than `breakout_v2`.
- `breakout_v3` is still not activation-ready.
- current data supports continued shadow observation, not tuning or live activation.

## Test Status

Latest test command:

```powershell
python -m pytest
```

Result:

- collected tests = `56`
- passed = `56`
- failed = `0`

---

# 3. Next Step Decision

The next valid project phase is:

```text
PULLBACK_ONLY_RECOVERY_OBSERVATION_WITH_AUXILIARY_GATE
```

This means:

- keep official live gate unchanged
- keep `pullback_v1` as the only active runtime strategy
- keep `breakout_v1` out of active runtime decisions
- keep `breakout_v2` inactive
- keep `breakout_v3` shadow-only
- add or formalize auxiliary recovery reporting that separates active `pullback_v1` recovery from historical aggregate contamination

---

# 4. Recommended Work Items

## Priority 1 - Auxiliary Recovery Evaluator

Create a non-authoritative recovery evaluator that reports:

- official gate status from `data/live_gate_decision.json`
- active strategy-only status for `pullback_v1`
- current exposure and pending order state
- risk counter synchronization
- post-isolation closed trade count
- post-isolation expectancy, if a reliable boundary can be derived

Important rule:

- this evaluator must not replace `src/validation/live_gate_evaluator.py`
- it must not overwrite `data/live_gate_decision.json`
- it should write a separate artifact, for example `data/auxiliary_recovery_status.json`

## Priority 2 - Performance Snapshot Segmentation

Add a read-only segmented analysis path for:

- aggregate all-history performance
- active-strategy-only performance
- optional post-isolation window performance

Important rule:

- do not delete historical `breakout_v1` data
- do not hide aggregate failure
- expose the reason for difference between aggregate gate and active recovery status

## Priority 3 - Breakout v1 Quarantine Record

Document `breakout_v1` as:

```text
historical_negative_contributor
not active
not eligible for reactivation without new design review
```

Rationale:

- sample count is small, but loss magnitude is large enough to pull the aggregate gate negative.
- current data does not support reactivation or parameter relaxation.

## Priority 4 - Continue Breakout v3 Shadow Observation

Continue observation until at least:

- `signal_count >= 100`
- `allowed_signal_count >= 5`
- allowed signal ratio remains near or above `5%`
- blocker distribution does not collapse into a single dominant structural failure

Only after that should tuning or activation discussion begin.

## Priority 5 - Scheduler Continuity Check

The scheduler log shows a large gap between `2026-04-24 13:44:05` and `2026-04-25 17:04:02`.

Next operational check:

- verify whether Windows Task Scheduler is expected to continue every 10 minutes
- confirm no lock file is stuck
- confirm host uptime and scheduler registration

This is an operations check, not a strategy change.

---

# 5. Non-Recommended Actions

Do not do the following now:

- do not loosen risk guard thresholds
- do not loosen `pullback_v1` RSI or trend filters yet
- do not reactivate `breakout_v1`
- do not activate `breakout_v3`
- do not modify the official live gate to force `LIVE_READY`
- do not reset strategy metrics to erase historical loss

---

# 6. Record Text

Current evidence says CNT is technically operational and testnet-connected, but official live readiness is currently failed by aggregate non-positive expectancy.

The correct next step is not strategy tuning. The correct next step is analytical separation:

1. preserve the official conservative gate
2. measure active `pullback_v1` recovery separately
3. quarantine historical `breakout_v1` negative contribution in interpretation, not by deleting data
4. continue `breakout_v3` shadow observation
5. verify scheduler continuity

This keeps CNT fact-based, conservative, and ready for a later re-entry into `LIVE_READY` only when aggregate or explicitly segmented recovery evidence supports it.

---

# Obsidian Links

- [[00 Docs Index]]
- [[CNT_PROJECT_STATUS_RECHECK_20260425]]
- [[CNT v2 OFFICIAL LIVE GATE RETENTION AND AUXILIARY RECOVERY PLAN]]
- [[CNT v2 TESTNET PERFORMANCE REPORT]]
- [[CNT v2 BREAKOUT V2 STATUS RECLASSIFICATION]]
- [[CNT v2 BREAKOUT V3 FIRST SHADOW OBSERVATION REVIEW]]

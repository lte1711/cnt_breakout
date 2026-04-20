---
tags:
  - cnt
  - docs
  - v2
  - report
  - status
aliases:
  - CNT v2 CURRENT STATUS ASSESSMENT
---

# CNT v2 CURRENT STATUS ASSESSMENT

```text
DOCUMENT_NAME = cnt_v2_current_status_assessment
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-21
STATUS        = ACTIVE_ASSESSMENT_REFINED
REFERENCE_1   = CNT v2 TESTNET PERFORMANCE REPORT
REFERENCE_2   = CNT v2 BREAKOUT FIRST TRADE REVIEW
REFERENCE_3   = CNT v2 LIVE READINESS GATE
```

---

# 1. CURRENT VERIFIED STATE

Verified from current repository state and runtime evidence:

- latest code baseline at assessment time = `ba25dec`
- market mode = `BINANCE_SPOT_TESTNET`
- engine mode = `ONE_SHOT`
- scheduler rhythm = `10 minutes`
- current state = `pending_order = null`, `open_trade = null`
- last action = `NO_ENTRY_SIGNAL`
- live gate = `NOT_READY / INSUFFICIENT_SAMPLE`

---

# 2. PERFORMANCE STATUS

Current testnet performance snapshot:

- total signals = `296`
- selected signals = `15`
- executed trades = `15`
- closed trades = `15`
- wins = `10`
- losses = `5`
- win rate = `0.6667`
- expectancy = `0.0044693`
- net pnl = `0.067039`
- max consecutive losses = `1`

Interpretation:

- `pullback_v1` is producing meaningful positive testnet results
- strategy performance is positive, but live transition is still blocked because sample sufficiency criteria are not yet satisfied

---

# 3. STRATEGY STATUS

## pullback_v1

- `signals_generated = 148`
- `signals_selected = 14`
- `trades_closed = 14`
- current operating strategy in practice
- positive testnet evidence now includes:
  - `win_rate = 0.7143`
  - `profit_factor = 2.3015`
  - `expectancy > 0`
  - `net_pnl > 0`

## breakout_v1

- `signals_generated = 148`
- `signals_selected = 1`
- `trades_closed = 1`
- no longer a dead branch
- first real trade lifecycle has been verified
- current phase is quality evaluation, not activation verification

Interpretation:

- strategy selection path is working
- ranker is not the primary bottleneck
- breakout remains heavily constrained by upstream strategy gating in the aggregate sample
- `selected_strategy_counts` must be interpreted carefully because it reflects only new-format selection-path logs, not total historical selected signals

---

# 4. CURRENT BOTTLENECK INTERPRETATION

Current breakout behavior should be interpreted as:

- previous trend-filter change was valid
- breakout has entered candidate, selection, and trade paths at least once
- lower-gate reasons now appear in runtime evidence
- however, the largest aggregate bottleneck is still `market_not_trend_up`
- recent signal evidence now includes:
  - `market_not_trend_up`
  - `volatility_not_high`
  - `range_without_upward_bias`
  - `range_bias_up_but_entry_trend_not_up`
  - `breakout_not_confirmed`
  - `ema_fast_not_above_slow`
  - `rsi_below_entry_threshold`

Current most important unresolved question:

- whether breakout market regime gating remains too strict for the intended strategy design

---

# 5. CURRENT OPERATING DIRECTION

The correct current order of work is:

1. continue accumulating testnet samples with `pullback_v1`
2. continue treating `breakout_v1` as an experimental strategy
3. continue collecting breakout rejection evidence, especially the share of `market_not_trend_up`
4. review breakout market regime gating before any further breakout parameter loosening

The following are not recommended at this moment:

- additional ATR/RSI loosening
- ranker tuning
- engine decomposition before the current observation question is resolved
- live-readiness escalation

---

# 6. FINAL CONCLUSION

CNT is no longer a design-only repository.

It is now:

- a functioning Binance Spot Testnet operating system
- with active runtime evidence
- with meaningful positive pullback strategy evidence
- with live readiness still on hold
- with breakout quality evaluation still ongoing

One-line conclusion:

**CNT is already operating meaningfully on testnet, `pullback_v1` is showing real positive testnet performance, `breakout_v1` is no longer dead, and the main remaining task is sample expansion plus further breakout quality evaluation under the still-dominant market-regime bottleneck.**

---

## Obsidian Links

- [[CNT v2 TESTNET PERFORMANCE REPORT]]
- [[CNT v2 BREAKOUT FIRST TRADE REVIEW]]
- [[CNT v2 LIVE READINESS GATE]]
- [[00 Docs Index|Docs Index]]

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
LAST_UPDATED  = 2026-04-21 13:24:03
REFERENCE_1   = CNT v2 TESTNET PERFORMANCE REPORT
REFERENCE_2   = CNT v2 BREAKOUT FIRST TRADE REVIEW
REFERENCE_3   = CNT v2 LIVE READINESS GATE
REFERENCE_4   = CNT v2 CANDIDATE RECOVERY STAGE 2 REPORT
```

---

# 1. CURRENT VERIFIED STATE

Verified from current repository state and runtime evidence:

- latest code baseline at assessment time = `a05705e`
- market mode = `BINANCE_SPOT_TESTNET`
- engine mode = `ONE_SHOT`
- scheduler rhythm = `10 minutes`
- current state = `pending_order = null`, `open_trade = null`
- last action = `SELL_FILLED`
- live gate = `NOT_READY / INSUFFICIENT_SAMPLE`

---

# 2. PERFORMANCE STATUS

Current testnet performance snapshot:

- total signals = `420`
- selected signals = `23`
- executed trades = `19`
- closed trades = `19`
- wins = `11`
- losses = `8`
- win rate = `0.5789`
- expectancy = `0.002072`
- net pnl = `0.039363`
- max consecutive losses = `2`

Interpretation:

- `pullback_v1` is producing meaningful positive testnet results
- strategy performance is positive, but live transition is still blocked because sample sufficiency criteria are not yet satisfied

---

# 3. STRATEGY STATUS

## pullback_v1

- `signals_generated = 210`
- `signals_selected = 21`
- `trades_closed = 17`
- current operating strategy in practice
- positive testnet evidence now includes:
  - `win_rate = 0.5882`
  - `profit_factor = 1.3591`
  - `expectancy > 0`
  - `net_pnl > 0`

## breakout_v1

- `signals_generated = 210`
- `signals_selected = 2`
- `trades_closed = 2`
- no longer a dead branch
- first real trade lifecycle has been verified
- current phase is quality evaluation, not activation verification

Interpretation:

- strategy selection path is working
- ranker is not the primary bottleneck
- breakout remains heavily constrained by upstream strategy gating in the aggregate sample
- `selected_strategy_counts` must be interpreted carefully because it reflects only new-format selection-path logs, not total historical selected signals
- stage 2 candidate recovery patch is applied and validated in code/tests, but runtime impact is still in early observation

---

# 4. CURRENT BOTTLENECK INTERPRETATION

Current breakout behavior should be interpreted as:

- previous trend-filter change was valid
- breakout has entered candidate, selection, and trade paths at least twice
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

Stage 2 candidate recovery interpretation:

- patch application is confirmed
- test and compile validation are confirmed
- a new relaxed pullback runtime reason is observed
- but meaningful reduction of `candidate_count=0` or `no_ranked_signal` is not yet proven statistically

Current most important unresolved question:

- whether breakout market regime gating remains too strict for the intended strategy design

---

# 5. CURRENT OPERATING DIRECTION

The correct current order of work is:

1. continue accumulating testnet samples with `pullback_v1`
2. continue treating `breakout_v1` as an experimental strategy
3. continue collecting breakout rejection evidence, especially the share of `market_not_trend_up`
4. continue Stage 3 runtime observation for candidate recovery effectiveness
5. only after runtime evidence is sufficient, decide whether breakout market regime gating or lower-gate tuning needs another change

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

**CNT is already operating meaningfully on testnet, `pullback_v1` is showing real positive testnet performance, `breakout_v1` is no longer dead, and the stage 2 candidate recovery patch is fully applied but still awaiting runtime-effect verification under the still-dominant market-regime bottleneck.**

---

## Obsidian Links

- [[CNT v2 TESTNET PERFORMANCE REPORT]]
- [[CNT v2 BREAKOUT FIRST TRADE REVIEW]]
- [[CNT v2 LIVE READINESS GATE]]
- [[CNT v2 CANDIDATE RECOVERY STAGE 2 REPORT]]
- [[00 Docs Index|Docs Index]]

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
DATE          = 2026-04-20
STATUS        = ACTIVE_ASSESSMENT_SAVED
REFERENCE_1   = CNT v2 TESTNET PERFORMANCE REPORT
REFERENCE_2   = CNT v2 BREAKOUT TREND FILTER CHANGE REPORT
REFERENCE_3   = CNT v2 BREAKOUT V1 RELAXATION EXPERIMENT REPORT
```

---

# 1. CURRENT VERIFIED STATE

Verified from current repository state and runtime evidence:

* latest code baseline = `85c778d`
* market mode = `BINANCE_SPOT_TESTNET`
* engine mode = `ONE_SHOT`
* scheduler rhythm = `10 minutes`
* current state = `pending_order = null`, `open_trade = null`
* last action = `SELL_FILLED`
* live gate = `NOT_READY / INSUFFICIENT_SAMPLE`

---

# 2. PERFORMANCE STATUS

Current testnet performance snapshot:

* total signals = `214`
* selected signals = `10`
* executed trades = `10`
* closed trades = `10`
* wins = `7`
* losses = `3`
* win rate = `0.70`
* expectancy = `0.0066511`
* net pnl = `0.066511`
* max consecutive losses = `1`

Interpretation:

* `pullback_v1` is producing meaningful positive testnet results
* live transition is still blocked because sample sufficiency criteria are not yet satisfied

---

# 3. STRATEGY STATUS

## pullback_v1

* `signals_generated = 107`
* `signals_selected = 10`
* `trades_closed = 10`
* current operating strategy in practice

## breakout_v1

* `signals_generated = 107`
* `signals_selected = 0`
* `trades_closed = 0`
* still failing to enter candidate or selection path

Interpretation:

* strategy selection path is working
* ranker is not the primary bottleneck
* breakout remains blocked by upstream strategy gating

---

# 4. CURRENT BOTTLENECK INTERPRETATION

Current breakout behavior should be interpreted as:

* previous trend-filter change was valid
* bottleneck movement from `market_not_trend_up` to lower filters was partially observed
* breakout has still not entered candidate path

Current most important unresolved question:

* whether breakout market regime gating is too strict for the intended strategy design

---

# 5. CURRENT OPERATING DIRECTION

The correct current order of work is:

1. continue accumulating testnet samples with `pullback_v1`
2. continue treating `breakout_v1` as an experimental strategy
3. continue collecting breakout rejection evidence
4. document and review breakout market regime gate before any further breakout parameter loosening

The following are not recommended at this moment:

* additional ATR/RSI loosening
* ranker tuning
* engine decomposition before the current observation question is resolved
* live-readiness escalation

---

# 6. FINAL CONCLUSION

CNT is no longer a design-only repository.

It is now:

* a functioning Binance Spot Testnet operating system
* with active runtime evidence
* with positive pullback strategy evidence
* with live readiness still on hold
* and with breakout trend-gate analysis still pending

One-line conclusion:

**CNT is already operating meaningfully on testnet, `pullback_v1` is showing positive evidence, and the main remaining task is sample expansion plus breakout trend-gate redesign analysis before any further breakout tuning.**

---

## Obsidian Links

- [[00 CNT Vault Home|Vault Home]]
- [[00 Docs Index|Docs Index]]

### Related
- [[CNT v2 TESTNET PERFORMANCE REPORT]]
- [[CNT v2 BREAKOUT TREND FILTER CHANGE REPORT]]
- [[CNT v2 BREAKOUT V1 RELAXATION EXPERIMENT REPORT]]

---
aliases:
  - CNT v2 CURRENT STATUS ASSESSMENT
---

# CNT v2 CURRENT STATUS ASSESSMENT

```text
DOCUMENT_NAME = cnt_v2_current_status_assessment
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-22
STATUS        = LIVE_READY_POST_READINESS_BASELINE
LAST_UPDATED  = 2026-04-22 02:44:03
REFERENCE_1   = CNT v2 TESTNET PERFORMANCE REPORT
REFERENCE_2   = CNT v2 LIVE READINESS GATE
REFERENCE_3   = CNT v2 LIVE GATE ALIGNMENT REPORT
REFERENCE_4   = CNT v2 LIVE READY POST-READINESS MONITORING PLAN
```

---

# 1. CURRENT VERIFIED STATE

Verified from current repository state and runtime evidence:

- latest code baseline at assessment time = `8718981`
- market mode = `BINANCE_SPOT_TESTNET`
- engine mode = `ONE_SHOT`
- scheduler rhythm = `10 minutes`
- current state includes:
  - `pending SELL TARGET = present`
  - `open_trade = present`
  - `strategy_name = pullback_v1`
- last action = `SELL_SUBMITTED`
- live gate = `LIVE_READY / ALL_GATES_PASSED`

---

# 2. PERFORMANCE STATUS

Current testnet performance snapshot:

- total signals = `558`
- selected signals = `62`
- executed trades = `22`
- closed trades = `21`
- wins = `12`
- losses = `9`
- win rate = `0.5714`
- expectancy = `0.001319`
- net pnl = `0.027703`
- profit factor = `1.1969`
- max consecutive losses = `2`

Interpretation:

- CNT has crossed the minimum readiness gate and is now in post-readiness stabilization
- strategy performance remains positive, but quality is softer than earlier best snapshots
- throughput remains constrained despite the `LIVE_READY` decision

---

# 3. STRATEGY STATUS

## pullback_v1

- `signals_generated = 279`
- `signals_selected = 57`
- `trades_closed = 19`
- current operating strategy in practice
- positive testnet evidence now includes:
  - `win_rate = 0.5789`
  - `profit_factor = 1.1915`
  - `expectancy > 0`
  - `net_pnl > 0`

## breakout_v1

- `signals_generated = 279`
- `signals_selected = 5`
- `trades_closed = 2`
- no longer a dead branch
- first real trade lifecycle has been verified
- current phase is low-sample quality observation, not activation verification

Interpretation:

- strategy selection path is working
- ranker is functioning, but is not the dominant current limiter
- breakout remains heavily constrained by upstream strategy gating in the aggregate sample
- `selected_strategy_counts` must be interpreted carefully because it reflects only new-format selection-path logs, not total historical selected signals
- candidate recovery and gate alignment changes are applied and validated, but throughput remains limited by execution blocks and no-candidate cycles

---

# 4. CURRENT BOTTLENECK INTERPRETATION

Current behavior should be interpreted as:

- `LIVE_READY` is true, but throughput is still not strong
- measured post-readiness baseline:
  - `selection_rate = 62 / 558 = 11.11%`
  - `execution_rate = 22 / 62 = 35.48%`
  - `no_ranked_signal_total = 217`
- the current controlled bottleneck split is:
  - primary = execution blocking driven by observed risk guard activity
  - secondary = no-candidate / no-ranked-signal cycles
- breakout is alive, but still low-sample
- pullback remains the main source of operating evidence

---

# 5. CURRENT OPERATING DIRECTION

The correct current order of work is now:

1. fix the current `LIVE_READY` snapshot as the operating baseline
2. continue collecting post-readiness samples without parameter changes
3. track:
   - `selection_rate`
   - `execution_rate`
   - `no_ranked_signal`
   - `strategy_split`
   - `LIVE_READY` persistence
4. keep `pullback_v1` and `breakout_v1` quality assessment separate
5. review for the next change only after 20 to 30 additional cycles of post-readiness evidence

The following are not recommended at this moment:

- additional filter loosening
- risk guard loosening
- ranker retuning
- symbol expansion
- multi-position expansion

---

# 6. FINAL CONCLUSION

CNT is no longer a design-only repository.

It is now:

- a functioning Binance Spot Testnet operating system
- with active runtime evidence
- with `LIVE_READY` gate alignment restored
- with meaningful positive pullback strategy evidence
- with breakout quality evaluation still ongoing
- with a current focus on post-readiness stabilization rather than new optimization

One-line conclusion:

**CNT is now `LIVE_READY` on a fact-based gate decision, but its post-readiness operating quality is still constrained by low throughput and no-candidate cycles, so the next correct phase is stabilization and baseline persistence monitoring rather than new tuning.**

---

## Obsidian Links

- [[CNT v2 LIVE READINESS GATE]]


---
tags:
  - cnt
  - type/documentation
  - status/active
  - market-context
  - context-filter
  - strategy/breakout_v3
  - type/analysis
  - cnt-v2-breakout-trend-filter-redesign-plan
---

# CNT v2 BREAKOUT TREND FILTER REDESIGN PLAN

```text
DOCUMENT_NAME = cnt_v2_breakout_trend_filter_redesign_plan
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-20
STATUS        = IMPLEMENTATION_APPROVED
REFERENCE_1   = CNT v2 BREAKOUT TREND FILTER REVIEW REPORT
REFERENCE_2   = CNT v2 CURRENT STATUS ASSESSMENT
```

---

# 1. CURRENT BOTTLENECK

Current breakout evidence shows:

* `signals_generated` is sufficient
* `signals_selected = 0`
* `trades_closed = 0`
* dominant rejection reason remains `market_not_trend_up`

Interpretation:

* the limiting factor is the upper market-regime gate
* ATR / RSI are not the first tuning target in this phase

---

# 2. REDESIGN PURPOSE

The redesign goal is not immediate profit optimization.

The goal is to verify whether `breakout_v1` can at least enter:

* candidate path
* selection path

under a controlled and still conservative regime gate.

---

# 3. REDESIGN RULES

## Allowed

* `TREND_UP`
* `RANGE + trend_bias=UP + entry ema_fast > ema_slow`

## Blocked

* `TREND_DOWN`
* `RANGE` without upward bias
* `RANGE + UP_BIAS` but entry trend not up

---

# 4. TARGET REJECTION REASONS

The redesign must make the following reasons analytically visible:

* `market_not_trend_up`
* `range_without_upward_bias`
* `range_bias_up_but_entry_trend_not_up`
* `volatility_not_high`
* `rsi_below_entry_threshold`
* `breakout_not_confirmed`

---

# 5. TEST PLAN

Required test coverage:

1. `TREND_UP` passes upper gate
2. `RANGE + trend_bias=UP + ema_fast > ema_slow` passes upper gate
3. `RANGE + trend_bias!=UP` stays blocked
4. `RANGE + trend_bias=UP + ema_fast <= ema_slow` stays blocked
5. `TREND_DOWN` stays blocked
6. lower-layer reasons still appear after upper-gate pass

---

# 6. OBSERVATION PLAN

After deployment:

* keep `TESTNET_ONLY`
* keep current scheduler rhythm
* do not adjust ATR / RSI
* observe at least `20` post-change breakout cycles
* prefer `30` post-change breakout cycles for stronger interpretation

---

## Obsidian Links

- [[CNT v2 BREAKOUT QUALITY EVALUATION REPORT]]


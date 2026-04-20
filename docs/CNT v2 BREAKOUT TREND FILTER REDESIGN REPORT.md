---
tags:
  - cnt
  - docs
  - breakout
  - report
  - v2
aliases:
  - CNT v2 BREAKOUT TREND FILTER REDESIGN REPORT
---

# CNT v2 BREAKOUT TREND FILTER REDESIGN REPORT

```text
DOCUMENT_NAME = cnt_v2_breakout_trend_filter_redesign_report
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-20
STATUS        = CODE_AND_TEST_UPDATED
REFERENCE_1   = CNT v2 BREAKOUT TREND FILTER REDESIGN PLAN
REFERENCE_2   = CNT v2 BREAKOUT TREND FILTER CHANGE REPORT
```

---

# 1. IMPLEMENTED CHANGE

Implemented in `src/strategies/breakout_v1.py`:

* `TREND_UP` pass path kept intact
* `RANGE + trend_bias=UP + entry ema_fast > ema_slow` allowed through upper gate
* `TREND_DOWN` still blocked
* rejection reasons split for better diagnosis:
  * `market_not_trend_up`
  * `range_without_upward_bias`
  * `range_bias_up_but_entry_trend_not_up`

---

# 2. OBSERVABILITY CHANGE

Implemented in runtime signal logging:

* `trend_bias` is now included in `signal.log`

This improves post-change interpretation without changing engine execution order.

---

# 3. TEST RESULT

Updated test coverage in `tests/test_breakout_trend_filter.py`:

* `TREND_UP` upper-gate pass
* `RANGE + UP_BIAS` pass
* `RANGE without UP_BIAS` block
* `RANGE + UP_BIAS but entry trend not up` block
* `TREND_DOWN` block
* lower-gate rejection propagation:
  * `volatility_not_high`
  * `rsi_below_entry_threshold`
  * `breakout_not_confirmed`

Runtime-safe validation for this step:

* unit and regression tests only
* operational cycle observation continues through scheduler

---

# 4. INITIAL INTERPRETATION

This redesign should be treated as:

* a controlled upper-gate redesign
* not an ATR / RSI loosening step
* not a ranker adjustment
* not a pullback strategy change

Next judgment must depend on post-change runtime evidence.

---

# 5. NEXT DECISION RULE

Post-change success signals include:

* lower rejection reasons increasing
* breakout candidate path appearing
* breakout selection path appearing

If `market_not_trend_up` remains dominant after enough cycles, the next review should focus on:

* market regime classification design
* not ATR / RSI loosening

---

## Obsidian Links

- [[00 CNT Vault Home|Vault Home]]
- [[00 Docs Index|Docs Index]]

### Related
- [[CNT v2 BREAKOUT TREND FILTER REDESIGN PLAN]]
- [[CNT v2 BREAKOUT TREND FILTER CHANGE REPORT]]

---
aliases:
  - CNT v2 BREAKOUT FIRST TRADE REVIEW
---

# CNT v2 BREAKOUT FIRST TRADE REVIEW

```text
DOCUMENT_NAME = cnt_v2_breakout_first_trade_review
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-20
STATUS        = FIRST_BREAKOUT_TRADE_REVIEWED
REFERENCE_1   = CNT v2 BREAKOUT TREND FILTER REDESIGN REPORT
REFERENCE_2   = CNT v2 CURRENT STATUS ASSESSMENT
REFERENCE_3   = CNT v2 TESTNET PERFORMANCE REPORT
```

---

# 1. PURPOSE

This document reviews the first real `breakout_v1` trade after the trend-filter redesign.

The goal is not to optimize yet.

The goal is to answer:

* did breakout actually enter candidate and selection path
* did breakout produce a real trade
* what did the first completed breakout trade tell us about the next bottleneck

---

# 2. VERIFIED FACTS

Current runtime evidence confirms:

* `breakout_v1.signals_selected = 1`
* `breakout_v1.trades_closed = 1`
* `selected_strategy_counts.breakout_v1 = 1`

Selection-path evidence:

* `2026-04-20 17:14:03`
* `selected_strategy=breakout_v1`
* `selection_reason=highest_score`
* `candidate_count=1`
* `rank_score=1.9`

Trade lifecycle evidence:

* `2026-04-20 17:14:00` `BUY_SUBMITTED`
* `2026-04-20 17:34:00` `PROMOTE_TO_OPEN_TRADE`
* `2026-04-20 17:44:00` `STOP_MARKET_FILLED`

---

# 3. FIRST BREAKOUT TRADE SUMMARY

## Entry

* entry price = `2300.0`
* stop price = `2296.55`
* target price = `2304.6`
* strategy = `breakout_v1`

## Close

* close action = `STOP_MARKET_FILLED`
* close pnl estimate = `-0.011044`

## Performance impact

`breakout_v1` current strategy metrics:

* `trades_closed = 1`
* `wins = 0`
* `losses = 1`
* `expectancy = -0.011044`
* `profit_factor = 0.0`

Interpretation:

* breakout is no longer a dead branch
* breakout is now a real but low-sample strategy
* one losing trade is not enough to judge the strategy as failed

---

# 4. IMPORTANT STRUCTURAL RESULT

The redesign succeeded at the structural level.

What is now proven:

1. breakout can reach candidate path
2. breakout can win ranking and be selected
3. breakout can submit a live testnet entry
4. breakout can complete a full trade lifecycle

This means the previous core problem:

* `generated > 0`
* `selected = 0`

has been solved.

---

# 5. NEW BOTTLENECK AFTER ACTIVATION

After the first breakout trade, the observed rejection reasons moved lower:

* `breakout_not_confirmed`
* `ema_fast_not_above_slow`
* `range_bias_up_but_entry_trend_not_up`
* `volatility_not_high`

Interpretation:

* the main issue is no longer simple upper trend exclusion
* the strategy is now being constrained by lower setup quality checks
* this is a healthier failure mode than total non-selection

---

# 6. CURRENT JUDGMENT

## What is now true

* breakout activation objective = achieved
* breakout profitability objective = not yet achieved
* breakout sample size = still too small

## Correct next phase

The correct next phase is:

* continue observation
* collect more breakout samples
* avoid immediate ATR / RSI tuning
* avoid pullback tuning

The next design question should be:

* whether breakout lower-gate quality checks need redesign after enough samples

not:

* whether breakout should be disabled immediately

---

# 7. RECOMMENDATION

Recommended order from this point:

1. keep current breakout redesign active
2. accumulate more breakout trade samples
3. compare breakout rejection distribution after activation
4. only then decide whether the next review should target:
   * volatility gate
   * entry EMA confirmation
   * breakout confirmation strictness

---

# 8. FINAL CONCLUSION

The first breakout trade lost money, but that is not the main conclusion.

The main conclusion is:

**`breakout_v1` is now alive in the real runtime path. The current phase has shifted from activation to quality evaluation.**

---

## Obsidian Links

- [[CNT v2 BREAKOUT QUALITY EVALUATION REPORT]]


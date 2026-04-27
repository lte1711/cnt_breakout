---
aliases:
  - CNT v2 BREAKOUT QUALITY EVALUATION REPORT
---

# CNT v2 BREAKOUT QUALITY EVALUATION REPORT

```text
DOCUMENT_NAME = cnt_v2_breakout_quality_evaluation_report
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-21
STATUS        = QUALITY_EVALUATION_ACTIVE
REFERENCE_1   = CNT v2 BREAKOUT FIRST TRADE REVIEW
REFERENCE_2   = CNT v2 CURRENT STATUS ASSESSMENT
REFERENCE_3   = CNT v2 TESTNET PERFORMANCE REPORT
```

---

# 1. Design Summary

This document evaluates the current quality status of `breakout_v1` after it successfully moved out of dead-branch status.

The goal of this phase is not optimization.

The goal is to answer three questions:

1. Is `breakout_v1` alive in the real runtime path?
2. Where is the dominant bottleneck now?
3. Should the next step be more tuning or more observation?

---

# 2. Validation Result

Verified from the latest snapshot:

- `snapshot timestamp = 2026-04-21 01:04:04`
- `breakout_v1.signals_generated = 149`
- `breakout_v1.signals_selected = 1`
- `breakout_v1.trades_closed = 1`
- `breakout_v1.wins = 0`
- `breakout_v1.losses = 1`
- `breakout_v1.expectancy = -0.011044`
- `selected_strategy_counts.breakout_v1 = 1`

Aggregate rejection distribution from current `signal.log`:

- `market_not_trend_up = 100`
- `volatility_not_high = 29`
- `range_bias_up_but_entry_trend_not_up = 8`
- `range_without_upward_bias = 8`
- `ema_fast_not_above_slow = 3`
- `rsi_below_entry_threshold = 2`
- `breakout_not_confirmed = 1`
- `trend_up_high_volatility_breakout = 1`

Interpretation:

- `breakout_v1` is no longer a dead branch
- lower-gate rejection is now visible in real runtime evidence
- however, the largest aggregate bottleneck is still `market_not_trend_up`
- the most recent additional cycle still did not produce a second breakout selection

---

# 3. Record Text

## 3.1 Current Quality Status

The current quality status of `breakout_v1` should be described as:

- activation objective = completed
- quality evaluation objective = active
- profitability judgment = not yet reliable

This means:

- the answer to "Did breakout become active?" is now `yes`
- the answer to "Is breakout already a good strategy?" is still `not yet judgeable`

## 3.2 What Is Proven

The following has now been proven in real runtime:

1. breakout can enter candidate path
2. breakout can win ranking and be selected
3. breakout can submit a BUY order
4. breakout can complete a full trade lifecycle

This is a meaningful structural success.

## 3.3 What Remains Unresolved

The main unresolved issues are:

1. the dominant aggregate rejection reason is still `market_not_trend_up`
2. breakout has only one closed trade, so profitability is not judgeable
3. lower-gate failures are visible, but still under-sampled

So the next question is not:

- "Should ATR/RSI be loosened again?"

The real next questions are:

- "Is the market regime gate still too restrictive for breakout intent?"
- "Will lower-gate reasons become dominant after more samples?"

## 3.4 Current Operating Recommendation

Recommended operation from this point:

1. keep `pullback_v1` as the main operating strategy
2. keep `breakout_v1` as an experimental strategy
3. accumulate more breakout samples
4. continue tracking the share of `market_not_trend_up`
5. do not perform additional ATR/RSI loosening yet
6. continue checking whether `volatility_not_high` keeps growing in the post-activation window

## 3.5 Final Judgment

The current breakout quality judgment is:

```text
STATUS = QUALITY_EVALUATION_ACTIVE
ACTIVATION = PASSED
PROFITABILITY = NOT_YET_JUDGEABLE
PRIMARY_BOTTLENECK = market_not_trend_up
NEXT_ACTION = CONTINUE_OBSERVATION
```

One-line conclusion:

**`breakout_v1` is now alive in the real runtime path, but the dominant aggregate bottleneck is still `market_not_trend_up`, so the correct next step is more quality-evaluation observation rather than additional tuning.**

---

## Obsidian Links

- [[00 Docs Index]]


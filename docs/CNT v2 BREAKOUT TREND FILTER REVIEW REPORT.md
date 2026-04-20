---
tags:
  - cnt
  - docs
  - breakout
  - report
  - v2
aliases:
  - CNT v2 BREAKOUT TREND FILTER REVIEW REPORT
---

# CNT v2 BREAKOUT TREND FILTER REVIEW REPORT

```text
DOCUMENT_NAME = cnt_v2_breakout_trend_filter_review_report
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-20
STATUS        = COMPLETE
REFERENCE_1   = CNT v2 BREAKOUT TREND FILTER REVIEW INSTRUCTION
REFERENCE_2   = CNT v2 BREAKOUT TIMER JUDGMENT REPORT
```

---

# 1. EXECUTIVE SUMMARY

The current breakout bottleneck is not primarily ATR / RSI scarcity.

The runtime evidence shows that breakout is still blocked almost entirely by the upper trend-alignment filter.

Conclusion:

* this stage should end with a trend-filter design review
* the next engineering action should be a controlled trend-filter revision design
* further ATR / RSI relaxation is not the recommended next move

---

# 2. CURRENT FILTER CHAIN

Current breakout decision path in `src/strategies/breakout_v1.py`:

1. indicator sufficiency on entry timeframe
2. `market_state != TREND_UP` -> `market_not_trend_up`
3. `volatility_state != HIGH` -> `volatility_not_high`
4. `rsi_value >= rsi_overheat` -> `rsi_overheat`
5. `ema_fast <= ema_slow` -> `ema_fast_not_above_slow`
6. `rsi_value < rsi_threshold` -> `rsi_below_entry_threshold`
7. insufficient lookback -> `not_enough_breakout_lookback`
8. no local breakout above recent highs -> `breakout_not_confirmed`
9. otherwise -> `entry_allowed=True`

Filter priority implication:

* `market_not_trend_up` has absolute first rejection priority after indicator sufficiency
* all lower breakout-specific setup checks are skipped when the market-state gate fails
* breakout setup quality is therefore never evaluated in most rejected cycles

---

# 3. TREND / VOLATILITY DEFINITION

Current `market_state` construction:

* if `ema_gap_ratio < ema_gap_threshold` -> `RANGE`
* else if `ema_fast > ema_slow` -> `TREND_UP`
* else -> `TREND_DOWN`

Current `volatility_state` construction:

* `HIGH` only when:
  * `atr_value >= atr_average * atr_expansion_multiplier`
* otherwise:
  * `LOW`

Interpretation:

* the breakout strategy first requires market classification to already be trend-up
* only after that does it allow volatility qualification
* only after that does it evaluate actual breakout setup structure

This means the strategy currently behaves as:

```text
strict trend-first -> strict volatility-next -> breakout setup last
```

---

# 4. LOG-BASED REJECTION EVIDENCE

Latest confirmed snapshot:

* `breakout_v1.signals_generated = 85`
* `breakout_v1.signals_selected = 0`
* `breakout_v1.trades_closed = 0`

Experiment-window breakout rejection distribution:

* `market_not_trend_up = 45`
* `volatility_not_high = 6`
* total observed breakout rejections = `51`

Rejection share:

* `market_not_trend_up = 88.24%`
* `volatility_not_high = 11.76%`

Interpretation:

* the dominant blocker is still upper trend alignment
* only after trend alignment occasionally passes does volatility become visible as the next bottleneck
* ATR / RSI thresholds are not yet the best next lever because the flow rarely reaches them

---

# 5. WHY THIS IS A TREND-FILTER REVIEW, NOT ATR / RSI REVIEW

The reason is structural:

* ATR / RSI checks are downstream
* the overwhelming majority of breakout cycles are rejected before the code reaches those checks

Therefore:

* relaxing ATR / RSI further would mostly change logic that the runtime rarely reaches
* the stronger evidence-based next step is to review the trend qualification layer itself

---

# 6. CHANGE OPTION A

## A. Trend-Filter Relaxation

Direction:

* soften the definition of `TREND_UP`
* or allow a controlled subset of `RANGE` states to continue into breakout setup evaluation

Example concepts:

* allow `RANGE` with positive EMA slope and local breakout pressure
* reduce the strictness of `ema_gap_ratio` threshold in market-state classification

Expected effect:

* more breakout cycles reach downstream setup checks
* more visibility into whether volatility or breakout confirmation is the real next blocker

Risk:

* false positives may increase
* candidate counts may rise quickly
* pullback and breakout may overlap more often

---

# 7. CHANGE OPTION B

## B. Filter-Order Rearrangement

Direction:

* evaluate breakout setup presence before fully enforcing trend/volatility gates

Example concepts:

* compute breakout confirmation first
* if breakout structure exists, then apply softer trend / volatility qualification

Expected effect:

* the engine can learn whether setup quality exists even inside non-ideal trend states
* rejection reasons become more diagnostic

Risk:

* logic becomes less intuitive than the current strict top-down filter
* signal counts may rise in a less predictable way
* ranking interactions may need closer monitoring

---

# 8. IMPACT REVIEW

Any change in this area can affect:

* false positive rate
* total signal volume
* total candidate volume
* pullback vs breakout candidate collisions
* ranker candidate distribution
* downstream rejection reasons seen on testnet

New reasons worth tracking after a future change:

* `breakout_not_confirmed`
* `rsi_below_entry_threshold`
* `volatility_not_high`
* overlap situations where breakout becomes candidate but loses to pullback

---

# 9. RECOMMENDATION

Recommended option:

```text
RECOMMENDATION = OPTION A
```

Reason:

* the data indicates the problem is mainly the absolute strictness of the trend gate, not the order of lower checks
* option A is easier to reason about and safer to validate incrementally on testnet
* option B is more invasive and should be reserved if option A still fails to expose breakout setup behavior

Recommended next stage:

* controlled code change proposal for trend-filter relaxation
* not additional ATR / RSI threshold relaxation

---

# 10. FINAL JUDGMENT

```text
TREND_FILTER_REVIEW_REQUIRED = YES
ATR_RSI_SECOND_RELAXATION    = NOT_RECOMMENDED_YET
RECOMMENDED_OPTION           = A
NEXT_STAGE                   = ACTUAL_TREND_FILTER_CHANGE_DESIGN
```

---

## Obsidian Links

- [[00 CNT Vault Home|Vault Home]]
- [[00 Docs Index|Docs Index]]

### Related
- [[CNT v2 BREAKOUT TREND FILTER REVIEW INSTRUCTION]]
- [[CNT v2 BREAKOUT TIMER JUDGMENT REPORT]]

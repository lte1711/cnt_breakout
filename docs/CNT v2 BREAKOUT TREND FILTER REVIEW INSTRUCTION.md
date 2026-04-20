# CNT v2 BREAKOUT TREND FILTER REVIEW INSTRUCTION

```text
DOCUMENT_NAME = cnt_v2_breakout_trend_filter_review_instruction
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-20
STATUS        = ACTIVE
PURPOSE       = diagnose breakout_v1 upper-entry filter structure before any further parameter relaxation
```

---

# 1. GOAL

Review whether the reason `breakout_v1` still cannot enter candidate path after the first relaxation is located in the upper trend-filter structure rather than in ATR / RSI thresholds.

This stage must produce a design review, not a code patch.

---

# 2. CURRENT FIXED FACTS

Latest confirmed runtime facts:

* `breakout_v1.signals_generated = 85`
* `breakout_v1.signals_selected = 0`
* `breakout_v1.trades_closed = 0`
* `selected_strategy_counts = {'pullback_v1': 3}`
* selection-path observability is working
* breakout still does not enter candidate path

Observed breakout rejection bottlenecks:

* main bottleneck through most of the experiment window:
  * `market_not_trend_up`
* newer visible secondary bottleneck:
  * `volatility_not_high`

---

# 3. REQUIRED WORK

STEP 1

* analyze current breakout filter-chain structure in:
  * `src/strategies/breakout_v1.py`
* document:
  * filter order
  * `market_not_trend_up` decision basis
  * `volatility_not_high` decision basis
  * where the first rejection is decided
  * where the bottleneck moves after `TREND_UP` is satisfied

STEP 2

* write a trend-filter review design note
* assess:
  * whether current `TREND_UP` is too strict
  * whether fully blocking breakout candidates inside `RANGE` is appropriate
  * whether the structure `TREND_UP -> then LOW volatility fail` is intended behavior
  * whether the upper gate should remain:
    * `strict trend-first`
    * or move toward `trend-or-breakout-setup`

STEP 3

* propose at most two change candidates:
  * proposal A = trend-filter relaxation
  * proposal B = filter-order rearrangement

STEP 4

* document expected impact:
  * false-positive increase risk
  * signal-count growth risk
  * pullback collision risk
  * ranker candidate-count change
  * new rejection reasons to observe on testnet

STEP 5

* save review report to:
  * `docs/CNT v2 BREAKOUT TREND FILTER REVIEW REPORT.md`

---

# 4. OUT OF SCOPE

The following are not allowed in this stage:

* further `config.py` threshold changes
* second ATR / RSI relaxation
* ranker modifications
* engine decomposition
* live-trading decision

---

# 5. COMPLETION RULE

This stage is complete only when:

* breakout filter chain is documented
* trend-filter review necessity is explained from logs
* at most two change options are proposed
* one recommendation is selected
* no code is changed


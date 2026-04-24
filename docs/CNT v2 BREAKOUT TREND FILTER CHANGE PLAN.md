---
aliases:
  - CNT v2 BREAKOUT TREND FILTER CHANGE PLAN
---

# CNT v2 BREAKOUT TREND FILTER CHANGE PLAN

```text
DOCUMENT_NAME = cnt_v2_breakout_trend_filter_change_plan
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-20
STATUS        = APPLIED
PURPOSE       = apply the recommended option A trend-filter relaxation for breakout_v1
```

---

# 1. CHANGE TARGET

Target file:

* `src/strategies/breakout_v1.py`

Target scope:

* upper trend filter only

Out of scope:

* ATR / RSI second relaxation
* ranker changes
* engine changes

---

# 2. APPLIED CHANGE

Applied option:

```text
OPTION A = trend-filter relaxation
```

Implemented rule:

* continue allowing `TREND_UP` as before
* additionally allow `RANGE` to proceed into lower breakout checks when:
  * primary trend bias is `UP`
  * entry-frame `ema_fast > ema_slow`

Intent:

* expose lower breakout blockers in cycles that previously stopped at the top trend gate
* keep the change narrow and explainable

---

# 3. REQUIRED VALIDATION

Validation requirements:

1. tests remain green
2. breakout trend-bias behavior is covered by new tests
3. one fresh runtime cycle is executed
4. no claim of success is made unless runtime evidence exists

---

## Obsidian Links

- [[CNT v2 BREAKOUT QUALITY EVALUATION REPORT]]


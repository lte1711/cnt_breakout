---
aliases:
  - CNT v2 BREAKOUT TIMER JUDGMENT REPORT
---

# CNT v2 BREAKOUT TIMER JUDGMENT REPORT

```text
DOCUMENT_NAME = cnt_v2_breakout_timer_judgment_report
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-20
STATUS        = COMPLETE
REFERENCE_1   = CNT v2 BREAKOUT REVIEW TIMER REPORT
REFERENCE_2   = CNT v2 BREAKOUT V1 RELAXATION EXPERIMENT REPORT
```

---

# 1. EXECUTIVE SUMMARY

The 8-hour breakout review timer fired normally and the next judgment was completed.

Result:

* breakout did not reach candidate path
* selection-path observability is now confirmed in the system
* the dominant breakout blocker is `market_not_trend_up`
* the next step is trend-filter review, not further ATR / RSI relaxation

---

# 2. TIMER CONFIRMATION

Timer evidence:

* `data/breakout_review_due.json` exists
* `status = READY_FOR_NEXT_JUDGMENT`
* `timestamp = 2026-04-20 09:10:34`
* `logs/breakout_review_timer.log` contains the due marker

---

# 3. REVIEW FACTS

Snapshot facts:

* `closed_trades = 8`
* `wins = 5`
* `losses = 3`
* `selected_strategy_counts = {'pullback_v1': 3}`

Breakout facts:

* `signals_generated = 82`
* `signals_selected = 0`
* `trades_closed = 0`

Experiment-window breakout rejection distribution:

* `market_not_trend_up = 45`
* `volatility_not_high = 3`
* total = `48`
* `market_not_trend_up share = 93.75%`

---

# 4. DECISION

```text
BREAKOUT_CANDIDATE_PATH = NOT_OBSERVED
BREAKOUT_SELECTION_PATH = NOT_OBSERVED
SELECTION_PATH_SYSTEM   = CONFIRMED
SELECTED_COUNTS_SYSTEM  = CONFIRMED
NEXT_ACTION             = REVIEW_TREND_FILTER
```

---

# 5. OPERATIONAL NOTES

Still tracked, but not blocking this judgment:

1. `scheduler_stdout.log` encoding noise
2. possible log write collision during overlapping manual runs

These did not affect the experiment-window decision.

---

## Obsidian Links

- [[CNT v2 BREAKOUT QUALITY EVALUATION REPORT]]


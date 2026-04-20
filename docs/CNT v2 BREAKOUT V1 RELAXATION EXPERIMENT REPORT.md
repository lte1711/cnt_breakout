---
tags:
  - cnt
  - docs
  - breakout
  - report
  - v1
  - v2
aliases:
  - CNT v2 BREAKOUT V1 RELAXATION EXPERIMENT REPORT
---

# CNT v2 BREAKOUT V1 RELAXATION EXPERIMENT REPORT

```text
DOCUMENT_NAME = cnt_v2_breakout_v1_relaxation_experiment_report
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-20
STATUS        = REVIEW_COMPLETE
REFERENCE_1   = CNT v2 BREAKOUT V1 RELAXATION EXPERIMENT PLAN
REFERENCE_2   = CNT v2 FRESH CYCLE OBSERVABILITY VALIDATION REPORT
```

---

# 1. EXPERIMENT CHANGE

Applied parameter changes:

* `atr_expansion_multiplier: 1.2 -> 1.05`
* `rsi_threshold: 55 -> 53`

No other strategy or risk parameters were changed.

---

# 2. PRE-EXPERIMENT BASELINE

Pre-change baseline from saved runtime evidence:

* `breakout_v1.signals_generated = 34`
* `breakout_v1.signals_selected = 0`
* `breakout_v1.trades_closed = 0`
* fresh observability evidence existed only on `no_ranked_signal` path

Recent rejection evidence before relaxation:

* `market_not_trend_up`
* `trend_not_up`
* `volatility_not_high`

Interpretation:

* the likely bottleneck was still mainly trend-alignment filtering

---

# 3. TRACKED OPERATIONAL ITEMS

The following items remain under observation during the experiment:

1. `selected_strategy_counts` is still `{}` at experiment start
2. `run.ps1` scheduler stdout log collision can occur during overlapping manual launches

Current handling:

* `selected_strategy_counts` will be re-checked once a fresh selection-path log is produced
* overlapping manual launches are avoided during this experiment

---

# 4. INITIAL STATUS

```text
EXPERIMENT_STATE = STARTED
EXECUTION_WINDOW = OPEN
CURRENT_RESULT   = INITIAL_EVIDENCE_RECORDED
```

---

# 5. INITIAL EXECUTION RESULT

Initial post-change validation:

* test suite re-run = PASS
* one fresh cycle executed through `run.ps1`
* no overlapping manual run used during the experiment step

Fresh evidence after the first post-change cycle:

* `logs/signal.log`
  * `breakout_v1 reason=market_not_trend_up`
  * `pullback_v1 reason=pullback_rsi_not_in_range`
* `logs/portfolio.log`
  * `blocked_detail=all_filtered`
  * `candidate_count=0`
  * `rejected_reasons={'market_not_trend_up': 1, 'pullback_rsi_not_in_range': 1}`
* `data/performance_snapshot.json`
  * `blocked_signal_stats.no_ranked_signal = {all_filtered=5, legacy=25}`
  * `selected_strategy_counts = {}`

Current interpretation:

* `breakout_v1` has not yet entered candidate or selection path
* the dominant current breakout blocker is still `market_not_trend_up`
* the first relaxed thresholds did not immediately open the breakout path on the first observed cycle
* this is not yet a failure because the planned observation window is 20 to 50 cycles

Tracked operational notes:

1. `selected_strategy_counts` remains empty because fresh selection-path evidence with `selection_reason=highest_score` has still not been produced
2. `run.ps1` scheduler log collision remains a tracked issue, but it was avoided during this initial experiment step by not overlapping manual runs

Current experiment judgment:

```text
BREAKOUT_CANDIDATE_PATH = NOT_YET_OBSERVED
BREAKOUT_SELECTION_PATH = NOT_YET_OBSERVED
PRIMARY_BLOCKER         = market_not_trend_up
EXPERIMENT_STATUS       = CONTINUE_OBSERVATION
```

---

# 6. CURRENT PHASE DECISION

Current reviewed decision:

* experiment start is valid
* no new blocker was discovered
* the next correct action is to keep the current relaxed parameters unchanged
* additional cycles must be accumulated before deciding whether to further relax thresholds or revisit the trend filter

Current tracked interpretation:

1. `selected_strategy_counts = {}` is not yet treated as a code failure
2. it currently means fresh selection-path evidence with `selection_reason=highest_score` has not yet been produced
3. `scheduler_stdout.log` encoding noise and write-collision risk remain operational follow-up items, not experiment blockers

Current operating rule:

```text
KEEP_CURRENT_VALUES = TRUE
ADDITIONAL_PARAMETER_CHANGE = NOT_ALLOWED_YET
NEXT_REVIEW_POINT = after more scheduler cycles accumulate
```

Required ongoing tracking:

* `market_not_trend_up`
* `trend_not_up`
* `volatility_not_high`
* `pullback_rsi_not_in_range`
* `rsi_below_entry_threshold`
* `breakout_not_confirmed`
* `selection_reason=highest_score`
* `selected_strategy_counts`

---

# 7. TIMER REVIEW RESULT

Timer-triggered review time:

```text
REVIEW_TIME = 2026-04-20 09:10:34
REVIEW_STATUS = EXECUTED
```

Observed experiment-window facts after the first relaxation change:

* `performance_snapshot.closed_trades = 8`
* `performance_snapshot.selected_strategy_counts = {'pullback_v1': 3}`
* breakout remained:
  * `signals_generated = 82`
  * `signals_selected = 0`
  * `trades_closed = 0`

Breakout rejection distribution from experiment-start window:

```text
market_not_trend_up = 45
volatility_not_high = 3
total_breakout_rejections = 48
market_not_trend_up_share = 93.75%
```

Candidate / selection review:

```text
breakout_candidate_count = 0
breakout_selected_count = 0
selection_reason_highest_score_occurrences = 3
selection_reason_highest_score_for_breakout = 0
```

Interpretation:

* fresh selection-path evidence now exists in the system
* `selected_strategy_counts` is no longer empty
* however, the fresh selection-path evidence belongs to `pullback_v1`, not `breakout_v1`
* breakout still failed to enter the candidate path through the review window
* the dominant blocker is decisively the trend-alignment layer, not ATR / RSI threshold scarcity

Decision branch:

```text
CASE = A
candidate 0 retained for breakout
market_not_trend_up share > 70%
NEXT_RECOMMENDATION = REVIEW_TREND_FILTER
```

---

# 8. FINAL JUDGMENT

```text
BREAKOUT_RELAXATION_1_RESULT = NO_BREAKOUT_CANDIDATE_PROGRESS
OBSERVABILITY_SELECTION_PATH = CONFIRMED
SELECTED_STRATEGY_COUNTS     = CONFIRMED_WORKING
PRIMARY_BLOCKER              = market_not_trend_up
NEXT_ACTION                  = REVIEW_TREND_FILTER
```

Recommended next step:

* do not continue lowering ATR / RSI thresholds first
* inspect and redesign the breakout trend qualification layer before a second relaxation pass

---

# 9. REQUIRED FINAL FIELDS

The completed report must later include:

* archived execution cycle count
* archived breakout rejection distribution before/after
* archived breakout candidate count
* archived breakout selected count
* archived `selection_reason=highest_score` occurrence
* archived `selected_strategy_counts` reflection result

---

## Obsidian Links

- [[00 CNT Vault Home|Vault Home]]
- [[00 Docs Index|Docs Index]]

### Related
- [[CNT v2 BREAKOUT V1 RELAXATION EXPERIMENT PLAN]]
- [[CNT v2 FRESH CYCLE OBSERVABILITY VALIDATION REPORT]]

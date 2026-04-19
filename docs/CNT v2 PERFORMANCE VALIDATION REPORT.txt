# CNT v2 PERFORMANCE VALIDATION REPORT

```text
DOCUMENT_NAME = cnt_v2_performance_validation_report
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-19
STATUS        = INSUFFICIENT_SAMPLE
REFERENCE_1   = CNT v2 PERFORMANCE VALIDATION CHECKLIST
REFERENCE_2   = CNT v2 TESTNET PERFORMANCE REPORT
REFERENCE_3   = CNT v2 PERFORMANCE TUNING LOG
```

---

# 1. EXECUTIVE SUMMARY

The performance validation checklist was reviewed against the currently collected CNT v2 testnet evidence.

Current conclusion:

* instrumentation layer: validated
* runtime logging layer: validated
* performance judgment: not yet allowed

Reason:

* closed trades: `0`
* observation window: single safe runtime validation only

This does not satisfy the checklist minimum of either:

* `20` closed trades
* `3` days of operation

---

# 2. CHECKLIST RESULT

## 2.1 Data collection minimum

FAIL

Observed:

* closed trades = `0`
* operating period = less than `3` days

Result:

* no strategy superiority conclusion allowed
* no tuning conclusion allowed

## 2.2 Metrics availability

PASS

Confirmed available now:

* strategy metrics persistence
* rank score logging
* blocked reason logging
* strategy-level aggregate fields

Confirmed not yet meaningful:

* win rate
* expectancy
* net pnl
* strategy-by-strategy closed-trade comparison

## 2.3 Ranker validation

PARTIAL

Confirmed:

* `rank_score` log field exists
* `rank_score_components` log field exists
* fallback ranking path exists and was synthetically validated
* expectancy-aware ranking path exists and was synthetically validated

Not yet confirmed in live testnet evidence:

* dynamic score shifts from accumulated closed-trade data

## 2.4 Risk policy validation

PARTIAL

Confirmed:

* policy logging fields exist
* synthetic validation already covered:
  * `LOSS_COOLDOWN`
  * `DAILY_LOSS_LIMIT`
  * `MAX_PORTFOLIO_EXPOSURE`
  * `ONE_PER_SYMBOL_POLICY`

Not yet confirmed from operating sample:

* real distribution of policy triggers under multi-trade testnet operation

---

# 3. CURRENT OBSERVED DATA

```text
TOTAL_SIGNALS_GENERATED = 2
TOTAL_SELECTED_SIGNALS  = 0
TOTAL_EXECUTED_TRADES   = 0
TOTAL_CLOSED_TRADES     = 0
BLOCKED_REASON_DISTRIBUTION = no_ranked_signal=1
```

Strategy snapshot:

```text
breakout_v1:
  signals_generated = 1
  trades_closed     = 0
  expectancy        = 0.0

pullback_v1:
  signals_generated = 1
  trades_closed     = 0
  expectancy        = 0.0

mean_reversion_v1:
  inactive by default
```

---

# 4. STRATEGY REVIEW SUMMARY

```text
pullback_v1        = HOLD / NEED_SAMPLE
mean_reversion_v1  = INACTIVE / NO_DECISION
breakout_v1        = HOLD / NEED_SAMPLE
```

---

# 5. FORMAL DECISION

```text
STATUS = PERFORMANCE_VALIDATION_IN_PROGRESS
NEXT   = CONTINUE_DATA_COLLECTION
```

Do not tune live parameters yet beyond documented baseline unless one of the checklist minimum sample rules is met.

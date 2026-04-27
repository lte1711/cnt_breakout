---
aliases:
  - CNT v2 LIVE READINESS REPORT
---

# CNT v2 LIVE READINESS REPORT

```text
DOCUMENT_NAME = cnt_v2_live_readiness_report
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-19
STATUS        = NOT_READY
REFERENCE_1   = CNT v2 LIVE READINESS GATE
REFERENCE_2   = CNT v2 PERFORMANCE VALIDATION REPORT
REFERENCE_3   = CNT v2 TESTNET DATA COLLECTION STATUS REPORT
```

---

# 1. EXECUTIVE SUMMARY

The live readiness gate was evaluated against current CNT v2 testnet evidence.

Final result:

* live transition is not approved
* capital allocation decision is not allowed
* the project must return to data collection, not live deployment

---

# 2. PRECONDITION CHECK

## Mandatory preconditions

```text
closed_trades >= 50                    = FAIL
operation_period >= 3 days             = FAIL
strategy_metrics.json persistence      = PASS
portfolio.log field recording          = PASS
risk policy live trigger evidence      = FAIL
```

Immediate gate result:

* preconditions not satisfied

---

# 3. PERFORMANCE GATE CHECK

## Profitability

```text
Net PnL    = not measurable yet
Expectancy = not measurable yet
```

Result:

* FAIL by insufficient sample

## Stability

```text
max_consecutive_losses          = not measurable yet
daily_loss_limit_trigger_count  = not measurable yet
cooldown_trigger_count          = not measurable yet
```

Result:

* FAIL by insufficient sample

## Distribution health

```text
single-strategy concentration = not measurable yet
multi-strategy execution      = not observed yet
```

Result:

* FAIL by insufficient sample

## Risk policy verification

Observed from live-like operating logs:

* `LOSS_COOLDOWN` = not observed
* `DAILY_LOSS_LIMIT` = not observed
* `MAX_PORTFOLIO_EXPOSURE` = not observed
* `ONE_PER_SYMBOL_POLICY` = not observed

Result:

* FAIL for live-readiness purposes

## Ranker verification

Confirmed:

* `rank_score` field exists
* `rank_score_components` field exists

Not yet confirmed in collected operating sample:

* expectancy-adjusted live ranking behavior

Result:

* PARTIAL

---

# 4. FINAL DECISION

```text
STATUS   = NOT_READY
DECISION = RETURN_TO_TUNING
GO_LIVE  = NO
REASON   = PRECONDITIONS_NOT_MET
```

Do not move CNT v2 to live trading while the minimum sample and gate evidence remain unmet.

---

## Obsidian Links

- [[CNT v2 LIVE READINESS GATE]]


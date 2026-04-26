---
aliases:
  - CNT v2 NEXT PHASE PLAN
---

# CNT v2 NEXT PHASE PLAN

## (Post-Validation Data Accumulation Phase)

---

# 1. Phase Definition

Current position:

```text
PERFORMANCE_VALIDATION_IN_PROGRESS
```

Next-stage target:

```text
DATA_SUFFICIENCY_READY -> PERFORMANCE_VALIDATED -> LIVE_READY
```

---

# 2. Core Objectives

## Objective 1 - Data Sufficiency

* `closed_trades >= 50`
* or `>= 3 days`

## Objective 2 - Analysis Automation

* make the system analyzable without constant manual inspection

## Objective 3 - Live Gate Re-Evaluation Readiness

* enable immediate gate judgment once thresholds are met

---

# 3. Strategic Tracks

```text
[Track A] Data Collection
[Track B] Automated Analysis
[Track C] Operational Safety
```

---

# 4. Track A - Data Collection

## Operating Rules

* keep engine operation running
* no strategy changes
* no ranking logic retuning
* no risk parameter retuning

## Per-Cycle Expected Flow

* signal generation
* ranking
* risk check
* execution or blocking
* log persistence

## Required Automation Targets

### 1) Trade Counter

```text
closed_trades
```

### 2) Runtime Duration

```text
operation_time_hours
```

### 3) Validation Readiness Flag

```text
READY_FOR_VALIDATION = closed_trades >= 50 OR runtime >= 72h
```

---

# 5. Track B - Automated Analysis

## Goal

Automatically start structured analysis once sufficient data is accumulated.

## 5.1 Auto Snapshot

Target file:

```text
data/performance_snapshot.json
```

Required content:

* win_rate
* expectancy
* net_pnl
* strategy breakdown
* risk trigger stats

## 5.2 Auto Report Generator

Recommended script:

```text
scripts/generate_performance_report.py
```

Expected functions:

* read `strategy_metrics.json`
* parse `portfolio.log`
* generate `CNT v2 TESTNET PERFORMANCE REPORT`

## 5.3 Auto Gate Evaluator

Recommended module:

```text
src/validation/live_gate_evaluator.py
```

Expected output:

```text
PASS / FAIL / CONDITIONAL_PASS
```

---

# 6. Track C - Operational Safety

## 6.1 Fail-Safe Conditions

Recommended auto-stop rules:

```text
IF consecutive_losses >= 7 -> ENGINE STOP
IF daily_loss_limit_trigger >= 2 -> ENGINE PAUSE
```

## 6.2 Log Anomaly Detection

Recommended detection targets:

* `rank_score` always 0
* same strategy always selected
* excessive `blocked_by_policy`

## 6.3 Data Integrity Checks

Per-cycle integrity targets:

* `strategy_metrics.json` write success
* `portfolio.log` append success

---

# 7. Milestones

## Milestone 1 - First Trade

* first close confirmed
* metrics update confirmed

## Milestone 2 - 5 Trades

* logging normality only

## Milestone 3 - 10 Trades

* distribution anomaly review

## Milestone 4 - 20 Trades

```text
AUTO ANALYSIS TRIGGER
```

---

# 8. Automatic Actions After 20 Trades

Execution order:

1. generate performance snapshot
2. calculate strategy performance
3. analyze ranker impact
4. analyze risk triggers
5. evaluate live gate

---

# 9. Decision Branches

## CASE 1 - PASS

```text
STATUS = LIVE_READY
```

## CASE 2 - CONDITIONAL PASS

```text
STATUS = LIVE_READY_WITH_GUARDRAILS
```

## CASE 3 - FAIL

```text
STATUS = NOT_READY
```

---

# 10. Future Expansion Targets

## 10.1 Capital Allocation Engine

* expectancy-based capital weighting

## 10.2 Strategy Kill Switch

```text
expectancy < 0 AND trades >= 10 -> disable strategy
```

## 10.3 Adaptive Risk

* drawdown-based position sizing

---

# 11. Priority Order

## Immediate

1. performance snapshot generation
2. report generator
3. trade counter automation

## Secondary

4. live gate evaluator
5. fail-safe system

## Tertiary

6. strategy kill logic
7. capital allocation

---

# 12. Core KPI

```text
closed_trades
```

---

# 13. Final Statement

The purpose of this phase is not immediate optimization.

It is:

```text
wait in a measurable way
build automatic judgment on top of accumulating evidence
```

---

## Obsidian Links

- [[00 Docs Index]]


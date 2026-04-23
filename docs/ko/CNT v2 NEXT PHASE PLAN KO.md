---
tags:
  - cnt
  - docs
  - plan
  - v2
  - ko
aliases:
  - CNT v2 NEXT PHASE PLAN KO
---

# CNT v2 다음 단계 계획

## (검증 이후 데이터 누적 단계)

## 1. 단계 정의

현재 위치:

```text
PERFORMANCE_VALIDATION_IN_PROGRESS
```

다음 목표:

```text
DATA_SUFFICIENCY_READY -> PERFORMANCE_VALIDATED -> LIVE_READY
```

## 2. 핵심 목표

### Objective 1 - Data Sufficiency

- `closed_trades >= 20`
- 또는 `>= 3 days`

### Objective 2 - Analysis Automation

- 사람이 계속 들여다보지 않아도 분석 가능한 상태 만들기

### Objective 3 - Live Gate 재평가 준비

- threshold 충족 시 즉시 gate judgement 가능하도록 준비

## 3. 전략 트랙

```text
[Track A] Data Collection
[Track B] Automated Analysis
[Track C] Operational Safety
```

## 4. Track A - Data Collection

### 운영 규칙

- engine operation 유지
- strategy 변경 금지
- ranking logic retuning 금지
- risk parameter retuning 금지

### Per-Cycle 예상 흐름

- signal generation
- ranking
- risk check
- execution or blocking
- log persistence

### Required Automation Targets

1. `closed_trades`
2. `operation_time_hours`
3. `READY_FOR_VALIDATION = closed_trades >= 20 OR runtime >= 72h`

## 5. Track B - Automated Analysis

### 목표

- 충분한 데이터가 쌓이면 구조화된 분석을 자동 시작

### 5.1 Auto Snapshot

대상 파일:

- `data/performance_snapshot.json`

필수 내용:

- win_rate
- expectancy
- net_pnl
- strategy breakdown
- risk trigger stats

### 5.2 Auto Report Generator

권장 스크립트:

- `scripts/generate_performance_report.py`

예상 기능:

- `strategy_metrics.json` 읽기
- `portfolio.log` 파싱
- `CNT v2 TESTNET PERFORMANCE REPORT` 생성

### 5.3 Auto Gate Evaluator

권장 모듈:

- `src/validation/live_gate_evaluator.py`

예상 출력:

- `PASS / FAIL / CONDITIONAL_PASS`

## 6. Track C - Operational Safety

### 6.1 Fail-Safe Conditions

권장 auto-stop 규칙:

```text
IF consecutive_losses >= 7 -> ENGINE STOP
IF daily_loss_limit_trigger >= 2 -> ENGINE PAUSE
```

### 6.2 Log Anomaly Detection

권장 대상:

- `rank_score` always 0
- same strategy always selected
- excessive `blocked_by_policy`

### 6.3 Data Integrity Checks

매 cycle 체크:

- `strategy_metrics.json` write success
- `portfolio.log` append success

## 7. Milestones

### Milestone 1 - First Trade

- first close confirmed
- metrics update confirmed

### Milestone 2 - 5 Trades

- logging normality only

### Milestone 3 - 10 Trades

- distribution anomaly review

### Milestone 4 - 20 Trades

```text
AUTO ANALYSIS TRIGGER
```

## 8. 20 Trades 이후 자동 행동

실행 순서:

1. performance snapshot 생성
2. strategy performance 계산
3. ranker impact 분석
4. risk trigger 분석
5. live gate 평가

## 9. 결정 분기

### CASE 1 - PASS

```text
STATUS = LIVE_READY
```

## 링크

- [[CNT v2 NEXT PHASE PLAN]]
- [[CNT v2 NEXT PHASE PLANNING REPORT KO]]
- [[CNT v2 PERFORMANCE TUNING LOG KO]]

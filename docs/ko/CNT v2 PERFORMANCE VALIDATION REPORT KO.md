---
tags:
  - cnt
  - type/documentation
  - status/active
  - post-logging
  - type/validation
  - type/operation
  - risk
  - strategy/breakout_v3
  - type/analysis
  - status/completed
  - cnt-v2-performance-validation-report-ko
---

# CNT v2 성능 검증 보고서

```text
DOCUMENT_NAME = cnt_v2_performance_validation_report_ko
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-19
STATUS        = INSUFFICIENT_SAMPLE
REFERENCE_1   = CNT v2 PERFORMANCE VALIDATION CHECKLIST
REFERENCE_2   = CNT v2 TESTNET PERFORMANCE REPORT
REFERENCE_3   = CNT v2 PERFORMANCE TUNING LOG
```

## 1. 요약

성능 검증 체크리스트를 현재 수집된 CNT v2 testnet evidence와 대조한 결과:

- instrumentation layer = validated
- runtime logging layer = validated
- performance judgement = 아직 금지

이유:

- closed trades: `0`
- observation window: single safe runtime validation only

즉 아래 최소 조건을 만족하지 못했다.

- `20` closed trades
- `3` days of operation

## 2. 체크리스트 결과

### 2.1 데이터 수집 최소 기준

FAIL

관측:

- closed trades = `0`
- operating period = less than `3` days

결과:

- strategy superiority conclusion 금지
- tuning conclusion 금지

### 2.2 Metrics availability

PASS

현재 사용 가능:

- strategy metrics persistence
- rank score logging
- blocked reason logging
- strategy-level aggregate fields

아직 의미 없는 항목:

- win rate
- expectancy
- net pnl
- strategy-by-strategy closed-trade comparison

### 2.3 Ranker validation

PARTIAL

확인:

- `rank_score` log field 존재
- `rank_score_components` log field 존재
- fallback ranking path 존재 및 synthetic validation 완료
- expectancy-aware ranking path 존재 및 synthetic validation 완료

아직 live testnet evidence에서 확인되지 않은 것:

- accumulated closed-trade data에 따른 dynamic score shift

### 2.4 Risk policy validation

PARTIAL

확인:

- policy logging field 존재
- synthetic validation은 이미 아래 항목 포함
  - `LOSS_COOLDOWN`
  - `DAILY_LOSS_LIMIT`
  - `MAX_PORTFOLIO_EXPOSURE`
  - `ONE_PER_SYMBOL_POLICY`

운영 표본에서 아직 확인되지 않은 것:

- multi-trade testnet operation 하에서의 real distribution of policy triggers

## 3. 당시 관측 데이터

```text
TOTAL_SIGNALS_GENERATED = 2
TOTAL_SELECTED_SIGNALS  = 0
TOTAL_EXECUTED_TRADES   = 0
TOTAL_CLOSED_TRADES     = 0
BLOCKED_REASON_DISTRIBUTION = no_ranked_signal=1
```

전략 스냅샷:

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

## 4. 전략 리뷰 요약

```text
pullback_v1        = HOLD / NEED_SAMPLE
mean_reversion_v1  = INACTIVE / NO_DECISION
breakout_v1        = HOLD / NEED_SAMPLE
```

## 5. 공식 결정

```text
STATUS = PERFORMANCE_VALIDATION_IN_PROGRESS
NEXT   = CONTINUE_DATA_COLLECTION
```

체크리스트 최소 표본 규칙이 충족되기 전까지는 문서화된 baseline 외의 live parameter tuning을 하면 안 된다.

## 링크

- CNT v2 PERFORMANCE VALIDATION REPORT
- CNT v2 TESTNET PERFORMANCE REPORT KO
- CNT v2 TESTNET DATA COLLECTION INSTRUCTION KO

## Obsidian Links

- [[CNT v2 VALIDATION REPORT KO]]



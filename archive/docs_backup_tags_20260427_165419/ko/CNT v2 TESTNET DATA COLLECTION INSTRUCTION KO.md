---
aliases:
  - CNT v2 TESTNET DATA COLLECTION INSTRUCTION KO
---

# CNT v2 TESTNET 데이터 수집 지시서

## 현재 판정

이 지시서가 정의하는 올바른 현재 상태는:

**`PERFORMANCE_VALIDATION_IN_PROGRESS`**

## 현재 상태 정리

### 이미 확정 가능한 것

- 구조 배치 완료
- 운영 정합성 기본 확보
- 계측 계층 추가 완료
- performance-aware ranker 구현 완료
- metrics persistence 가능
- 로그 필드 확보 완료

### 아직 확정 불가능한 것

- 전략 우열
- 실제 expectancy 범위
- 파라미터 수정보다 관측이 우선인지 여부
- broader deployment 가능 여부

### 이유

최소 검증 기준이 아직 충족되지 않았기 때문이다.

- `closed trades = 0`
- 운영 기간 `< 3 days`

즉:

> 지금 단계는 성능 검증이 시작된 상태가 아니라, 성능을 검증할 표본을 모으는 단계다.

## 현재 최종 판정 문구

```text
STATUS   = PERFORMANCE_VALIDATION_IN_PROGRESS
DECISION = HOLD_JUDGMENT
REASON   = INSUFFICIENT_SAMPLE
NEXT     = TESTNET_DATA_COLLECTION
```

## 다음 진행 지시

목표:

- 최소 표본과 운영 정보를 performance validation이 가능한 상태로 만든다

## 종료 조건

아래 둘 중 하나 충족 시 종료:

- `closed_trades >= 50`
- `testnet operation >= 3 days`

## 운영 중 금지

- 전략 order rule 수정 금지
- ranker weight 수정 금지
- risk parameter 수정 금지
- target/stop 임의 조정 금지

## 운영 중 허용

- 로그 수집
- metrics 파일 누적
- 리포트 숫자 갱신
- 명백한 버그 수정

## 매 실행 때 기록할 항목

- total_signals
- selected_signals
- executed_trades
- closed_trades
- blocked_by_policy 분포
- strategy_metrics snapshot
- rank_score sample logs
- close_pnl_estimate sample logs

## 중간 점검 기준

### closed trades 5건 전

- 로그 누락 여부만 점검
- 성능 결론 금지

### closed trades 10건 전후

- 분포 이상치만 점검
- 튜닝 금지

### closed trades 20건 또는 3일 경과

그때부터 처음으로 아래 판단 시작:

- expectancy
- win_rate
- strategy comparison
- tuning 필요 여부

## 필수 결과물

- `CNT v2 TESTNET PERFORMANCE REPORT.md`
- `CNT v2 PERFORMANCE TUNING LOG.md`
- `CNT v2 PERFORMANCE VALIDATION REPORT.md`

## 중간 판정 규칙

표본 충족 전에는 상태를 아래로 유지한다.

```text
PERFORMANCE_VALIDATION_IN_PROGRESS
```

## 핵심 결론

지금 단계에서 가장 중요한 원칙은 다음과 같다.

> 분석은 가능하지만 판단은 아직 금지한다.

즉 다음 목표는 명확하다.

> 신호 구조 검증이 아니라 지표 기반 관측 완료

## 링크

- CNT v2 TESTNET DATA COLLECTION INSTRUCTION
- CNT v2 TESTNET DATA COLLECTION STATUS REPORT KO
- CNT v2 PERFORMANCE VALIDATION REPORT KO

## Obsidian Links

- [[CNT v2 TESTNET PERFORMANCE REPORT KO]]



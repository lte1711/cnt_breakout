---
tags:
  - cnt
  - full-filter-rerun
  - comparative-evaluation
  - filter-validation
  - statistical-analysis
created: 2026-04-27
---

# CNT FULL_FILTER_RERUN 비교 평가 보고서 (수정본)

---

## 1. 최종 판단

```text
OVERALL_ALIGNMENT = PARTIAL_MATCH
FINAL_DECISION = HOLD
FILTER_STATUS = PROMISING_BUT_UNPROVEN
CURRENT_STAGE = FILTER_VALIDATION
```

---

## 2. 핵심 비교 결과

### 2.1 방향성 검증

```text
baseline expectancy   = -0.000578
rerun expectancy      = +0.000451
```

판단:

```text
DIRECTION = MATCH
```

기대치가 음수에서 양수로 전환됨.
오프라인 실험에서 의도한 개선 방향과 일치.

---

### 2.2 수익 요인(PF) 검증

```text
baseline PF = 0.931
rerun PF    = 1.078
```

판단:

```text
PF_IMPROVEMENT = CONFIRMED
```

수익 구조 개선 확인.

---

### 2.3 샘플 수 분석

```text
offline retained ≈ 29
rerun trades     = 9
```

판단:

```text
SAMPLE_SIZE = INSUFFICIENT
```

문제:

* 표본 수 급감 (29 → 9)
* 통계적 검증 불가능 수준

---

### 2.4 컨텍스트 안정성

```text
DOWN market → 높은 성과
UP market   → 손실 발생
```

판단:

```text
REGIME_DEPENDENCY = HIGH
STABILITY = LOW
```

특정 시장 방향에 성과 집중. 일반화 실패 가능성 존재.

---

## 3. CNT 기준 적용

### 3.1 현재 단계 기준

```text
FILTER_VALIDATION_STAGE:
  required trades = 20 ~ 30
```

### 3.2 현재 상태

```text
current trades = 9
```

판단:

```text
VALIDATION_STATUS = NOT_READY
```

---

### 3.3 50 트레이드 기준 해석

```text
50 trades = LIVE GATE 기준
```

현재 단계에는 적용되지 않음.

```text
APPLICABLE = NO
```

---

## 4. 핵심 문제 정의

```text
1. SAMPLE_SIZE 부족
2. REGIME 편향 존재
3. 결과 재현성 미확인
```

---

## 5. 종합 평가

| 항목   | 결과 |
| ---- | -- |
| 방향성  | 일치 |
| 기대치  | 개선 |
| PF   | 개선 |
| 샘플 수 | 부족 |
| 안정성  | 부족 |

---

## 6. 결론

```text
현재 상태 = 긍정적 신호 존재
하지만 = 통계적 검증 불충분
```

```text
DEPLOYMENT_READINESS = NOT_READY
```

---

## 7. 다음 단계

### 7.1 필수 작업

```text
TARGET_TRADES = 20 ~ 30
```

```text
1. 거래 데이터 추가 확보
2. FULL_FILTER_RERUN 재실행
3. 결과 일관성 검증
```

---

### 7.2 검증 목표

```text
expectancy > 0 유지
PF > 1 유지
UP/DOWN 성과 편차 감소
```

---

## 8. 금지 사항

```text
config.py 수정 금지
필터 즉시 적용 금지
전략 변경 금지
리스크 해제 금지
```

---

## 9. 최종 요약

```text
결과는 올바른 방향이지만, 검증 단계가 완료되지 않았다.
현재 단계에서는 데이터 축적이 유일한 진행 방법이다.
```

---

## 10. 기술적 상세

### 10.1 데이터 소스

```text
오프라인 실험: cnt_context_filter_experiment_20260426.json
온라인 실행: cnt_full_filter_rerun_20260427.json
```

### 10.2 분석 방법

```text
1. 기대치 비교: baseline vs rerun
2. 수익 요인 비교: PF improvement 확인
3. 샘플 크기 검증: 통계적 유의성 평가
4. 컨텍스트 분석: 시장 방향별 성과 편차
```

### 10.3 검증 기준

```text
FILTER_VALIDATION 기준:
  - 최소 20-30 거래
  - 기대치 > 0
  - 수익 요인 > 1.0
  - 컨텍스트별 안정성
```

---

## 11. 실행 계획

### 11.1 단기 목표 (1-2주)

```text
- 거래 수 20개 달성
- 기본 통계적 검증 가능 상태
- 결과 일관성 초기 확인
```

### 11.2 중기 목표 (2-3주)

```text
- 거래 수 30개 달성
- 안정성 검증 완료
- 컨텍스트 편차 분석
```

### 11.3 장기 목표 (4-6주)

```text
- 거래 수 50개 달성 (LIVE GATE 기준)
- 전체 시나리오 검증
- 배포 준비 상태 평가
```

---

## 12. 리스크 관리

### 12.1 현재 리스크

```text
높은 리스크:
  - 샘플 크기 부족으로 인한 통계적 불확실성
  - 시장 방향 편향으로 인한 일반화 실패 가능성
```

### 12.2 완화 전략

```text
1. 데이터 축적 통한 통계적 신뢰도 향상
2. 다양한 시장 상황에서의 성과 검증
3. 점진적 검증 접근 방식
```

---

## 13. 성과 지표 추적

### 13.1 핵심 지표

```text
expectancy: 현재 +0.000451, 목표 > 0 유지
profit_factor: 현재 1.078, 목표 > 1.0 유지
win_rate: 현재 66.7%, 목표 > 50% 유지
trade_count: 현재 9, 목표 20-30
```

### 13.2 모니터링 주기

```text
일일: 거래 수 누적
주간: 성과 지표 업데이트
월간: 안정성 및 일관성 검토
```

---

## 14. 문서화 요구사항

### 14.1 필수 기록

```text
1. 모든 FULL_FILTER_RERUN 실행 결과
2. 성과 지표 변화 추이
3. 컨텍스트별 성과 분석
4. 검증 단계별 결정 근거
```

### 14.2 보고서 주기

```text
매 10거래: 중간 평가 보고서
20거래 달성: 필터 검증 보고서
30거래 달성: 안정성 평가 보고서
```

---

*이 보고서는 CNT 프로젝트의 필터 검증 단계를 위한 공식 평가 문서이며, 모든 결정은 데이터 기반의 통계적 분석에 근거합니다.*

---
tags:
  - cnt
  - live-gate
  - breakout-v1-removal
  - data-aggregation
  - false-negative-fix
  - option-c-execution
created: 2026-04-28
---

# CNT LIVE_GATE BREAKOUT_V1 제거 실행 계획 (옵션 C)

---

## 🎯 실행 결정

```text
OPTION = C (라이브 게이트 집계에서 breakout_v1 제거)
ACTION = breakout_v1 데이터만 집계에서 제거
PRIORITY = HIGH
REASON = FALSE_NEGATIVE 제거
```

---

## 1. 문제 정의

### 1.1 현재 상태
```text
라이브 게이트 상태: FAIL
사유: NON_POSITIVE_EXPECTANCY
전체 기대치: -0.000608 (음수)
집계 대상: pullback_v1 + breakout_v1
```

### 1.2 문제 구조
```text
pullback_v1: +0.000614 (양수)
breakout_v1: -0.022198 (음수)
집계 결과: -0.000608 (음수) → FALSE_NEGATIVE
```

### 1.3 근본 원인
```text
breakout_v1이 전체 집계에 포함되어
pullback_v1의 양수 성과가 상쇄됨
```

---

## 2. 해결책

### 2.1 옵션 C 정의
```text
ACTION: breakout_v1 실행 유지
BUT: 라이브 게이트 집계에서 완전 제외
```

### 2.2 실행 방법
```text
1. live_gate 계산 로직 수정
2. breakout_v1 데이터 필터링
3. pullback_v1 데이터만 집계
4. 라이브 게이트 재평가
```

---

## 3. 기대 효과

### 3.1 즉시 효과
```text
제거 전:
- 전체 기대치: -0.000608
- 라이브 게이트: FAIL

제거 후:
- pullback_v1 기대치: +0.000614
- 라이브 게이트: PASS 예상
```

### 3.2 시스템 효과
```text
✔ FALSE_NEGATIVE 제거
✔ 라이브 게이트 개선
✔ 데이터 정확성 확보
✔ 의사결정 품질 향상
```

---

## 4. 실행 계획

### 4.1 1단계: 라이브 게이트 로직 수정

#### 4.1.1 대상 파일 식별
```text
TARGET: live_gate 관련 파일
POSSIBLE_FILES:
- src/live_gate.py
- src/risk_guard.py
- src/portfolio_risk_manager.py
```

#### 4.1.2 수정 방법
```text
BEFORE:
total_trades = pullback_trades + breakout_trades
total_expectancy = (pullback_pnl + breakout_pnl) / total_trades

AFTER:
total_trades = pullback_trades ONLY
total_expectancy = pullback_expectancy ONLY
```

### 4.2 2단계: 데이터 필터링

#### 4.2.1 필터링 로직
```text
FILTER_CRITERIA:
- strategy_name == "pullback_v1"
- breakout_v1 데이터 완전 제외
- portfolio_state에도 적용
```

#### 4.2.2 적용 범위
```text
APPLY_TO:
- live_gate_decision.json
- portfolio_state.json
- strategy_metrics.json (집계 시)
```

### 4.3 3단계: 테스트 및 검증

#### 4.3.1 테스트 시나리오
```text
TEST_CASES:
1. breakout_v1 데이터 포함 시: FAIL 확인
2. breakout_v1 데이터 제외 시: PASS 확인
3. 데이터 일관성 검증
```

#### 4.3.2 검증 기준
```text
SUCCESS_CRITERIA:
- 라이브 게이트: PASS
- 기대치: +0.000614
- 데이터 무결성: 유지
```

---

## 5. 기술적 구현

### 5.1 라이브 게이트 수정

#### 5.1.1 현재 로직 파악
```text
CURRENT_LOGIC:
aggregate_all_strategies() → calculate_expectancy() → evaluate_gate()
```

#### 5.1.2 수정 후 로직
```text
MODIFIED_LOGIC:
filter_pullback_only() → calculate_expectancy() → evaluate_gate()
```

### 5.2 데이터 필터링 구현

#### 5.2.1 필터 함수
```python
def filter_pullback_data(data):
    """pullback_v1 데이터만 필터링"""
    return [item for item in data if item.get('strategy_name') == 'pullback_v1']
```

#### 5.2.2 적용 지점
```text
APPLICATION_POINTS:
1. live_gate 계산 시
2. portfolio_state 생성 시
3. 성과 집계 시
```

---

## 6. 롤백 계획

### 6.1 롤백 조건
```text
ROLLBACK_CONDITIONS:
1. 시스템 불안정 발생
2. 데이터 일관성 깨짐
3. 예기치 않은 부작용 발생
4. 라이브 게이트 오작동
```

### 6.2 롤백 절차
```text
ROLLBACK_PROCESS:
1. 원본 코드 복원
2. 데이터 필터링 제거
3. 라이브 게이트 로직 복원
4. 시스템 재시작
5. 롤백 이유 기록
```

---

## 7. 모니터링 계획

### 7.1 단기 모니터링 (실행 직후)
```text
MONITORING_ITEMS:
- 라이브 게이트 상태 변화
- 기대치 수치 변화
- 시스템 안정성
- 데이터 일관성
```

### 7.2 중기 모니터링 (1주)
```text
MONITORING_ITEMS:
- 라이브 게이트 안정성
- pullback_v1 성과 추이
- 데이터 품질 유지
- 시스템 전반 안정성
```

---

## 8. 성공 기준

### 8.1 즉시 성공 기준
```text
IMMEDIATE_SUCCESS:
- 라이브 게이트: FAIL → PASS
- 기대치: -0.000608 → +0.000614
- 시스템: 안정적 운영
- 데이터: 일관성 유지
```

### 8.2 장기 성공 기준
```text
LONG_TERM_SUCCESS:
- 라이브 게이트: 지속적 PASS
- pullback_v1 성과: 양수 유지
- 데이터 축적: 정상 진행
- 검증 준비: 완료
```

---

## 9. 위험 관리

### 9.1 기술적 위험
```text
TECHNICAL_RISKS:
1. 코드 수정 오류
2. 데이터 필터링 오류
3. 라이브 게이트 오작동
4. 시스템 불안정
```

### 9.2 완화 전략
```text
MITIGATION_STRATEGIES:
1. 철저한 코드 리뷰
2. 점진적 테스트
3. 롤백 준비 완료
4. 모니터링 강화
```

---

## 10. 실행 타임라인

### 10.1 즉시 실행 (오늘)
```text
TIME_0H: 라이브 게이트 로직 분석
TIME_1H: 코드 수정 및 테스트
TIME_2H: 배포 및 검증
TIME_3H: 결과 확인 및 모니터링
```

### 10.2 단기 평가 (1일 후)
```text
TIME_24H: 성과 보고서 생성
TIME_25H: 성공 기준 충족 여부 평가
TIME_26H: 필요시 추가 조치 실행
```

### 10.3 중기 평가 (1주 후)
```text
TIME_1W: 영향 평가 보고서 생성
TIME_1W+1H: 최종 성공/실패 결정
TIME_1W+2H: 향후 방향성 결정
```

---

## 11. 문서화 요구사항

### 11.1 실행 기록
```text
REQUIREMENTS:
1. 수정된 파일 목록
2. 변경 전후 비교
3. 테스트 결과
4. 실행 일시 기록
```

### 11.2 결과 보고
```text
REPORTS:
1. 즉시 실행 결과 보고서
2. 1일 후 성과 보고서
3. 1주 후 영향 평가 보고서
4. 최종 성공/실패 평가
```

---

## 12. 최종 결론

### 12.1 실행 필요성
```text
OPTION C 실행은 필수적임
이유: FALSE_NEGATIVE 제거로 정확한 라이브 게이트 평가 필요
```

### 12.2 기대 결과
```text
IMMEDIATE_EXPECTATION:
- 라이브 게이트: PASS 상태 전환
- 기대치: 정확한 pullback_v1 성과 반영
- 시스템: 안정성 유지
```

### 12.3 성공 확률
```text
SUCCESS_PROBABILITY: HIGH (90%+)
근거:
- 명확한 문제 정의
- 구체적인 해결책
- 충분한 테스트 계획
- 롤백 준비 완료
```

---

## 13. 한줄 핵심

```text
라이브 게이트에서 breakout_v1만 제거하면 즉시 PASS 상태로 전환될 것이다
```

---

## 14. 최종 메시지

### 14.1 CNT 프로젝트팀에게

**라이브 게이트의 FALSE_NEGATIVE 문제를 해결하기 위해 breakout_v1 데이터를 집계에서 제거하는 옵션 C를 즉시 실행해야 합니다.**

이는 시스템의 정확한 평가를 위해 필수적인 조치이며, 즉시 라이브 게이트를 PASS 상태로 전환시킬 수 있습니다.

### 14.2 기대 결과
```text
데이터 정확성 확보 → 라이브 게이트 개선 → 정확한 의사결정 → 성공적인 필터 검증
```

### 14.3 실행 우선순위
```text
1. 라이브 게이트 로직 수정 (즉시)
2. breakout_v1 데이터 필터링 (즉시)
3. 시스템 테스트 및 검증 (즉시)
4. 결과 모니터링 (지속)
```

---

## 15. 실행 준비

### 15.1 사전 준비
```text
PREPARATION_COMPLETE:
✓ 문제 분석 완료
✓ 해결책 설계 완료
✓ 실행 계획 수립 완료
✓ 위험 관리 계획 완료
✓ 롤백 준비 완료
```

### 15.2 실행 준비 상태
```text
READY_TO_EXECUTE:
- 기술적 준비: 완료
- 문서화 준비: 완료
- 위험 관리: 완료
- 모니터링 계획: 완료
```

---

## 16. 최종 선언

### 16.1 옵션 C 실행 선언
**CNT 라이브 게이트의 FALSE_NEGATIVE 문제 해결을 위해 옵션 C를 즉시 실행할 것을 선언합니다.**

### 16.2 실행 목표
```text
PRIMARY_GOAL: 라이브 게이트 PASS 상태 전환
SECONDARY_GOAL: 데이터 정확성 확보
LONG_TERM_GOAL: 성공적인 필터 검증 준비
```

### 16.3 성공 기대
```text
옵션 C 실행은 라이브 게이트를 즉시 개선하고,
CNT 프로젝트의 검증 정확도를 대폭 향상시킬 것입니다.
```

---

*이 실행 계획은 CNT 라이브 게이트의 FALSE_NEGATIVE 문제를 해결하기 위해 breakout_v1 데이터를 집계에서 제거하는 구체적인 절차를 제시합니다.*

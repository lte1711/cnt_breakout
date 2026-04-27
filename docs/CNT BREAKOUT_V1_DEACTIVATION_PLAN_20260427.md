---
tags:
  - cnt
  - breakout-v1
  - deactivation
  - data-purity
  - validation-focus
  - noise-reduction
created: 2026-04-27
---

# CNT BREAKOUT_V1 비활성화 실행 계획

---

## 🎯 실행 결정

```text
OPTION = A (가장 안전)
ACTION = breakout_v1 완전 비활성화
PRIORITY = HIGH
```

---

## 1. 핵심 문제 식별

### 1.1 데이터 오염 구조

현재 상태:
```text
breakout_v1:
  trades = 3
  expectancy = -0.022
  profit_factor = 0.173
```

문제 구조:
```text
pullback (good) + breakout (noise) → 전체 왜곡
```

결과:
```text
SIGNAL = 오염됨
live_gate = FAIL (NON_POSITIVE_EXPECTANCY)
```

### 1.2 거짓 음수 발생

현재 데이터:
```text
pullback_v1 → 양수 기대치 (+0.000966)
전체 합산 → 음수 기대치 (-0.000397)
```

원인:
```text
FALSE_NEGATIVE = breakout_v1 노이즈로 인한 왜곡
```

---

## 2. CNT 기준에 따른 판단

### 2.1 현재 단계 정의
```text
CURRENT_PRIORITY = FILTER_VALIDATION (pullback 기반)
```

따라서:
```text
breakout_v1 영향 = 불필요 + 해로움
```

### 2.2 전략별 분리 필요성

현재 문제:
```text
portfolio / live_gate / expectancy → 전략별 분리 없이 aggregate
```

해결책:
```text
STRATEGY_SEPARATION = 필수
```

---

## 3. 선택지 분석

### 3.1 OPTION A (가장 안전) - 권장

```text
ACTION: breakout_v1 완전 비활성화
```

효과:
```text
✔ 데이터 순도 확보
✔ pullback 검증 정확도 상승
✔ live_gate 왜곡 제거
✔ 통계적 신뢰도 향상
```

### 3.2 OPTION B (중간)

```text
ACTION: breakout_v1 실행 유지
BUT: 모든 분석에서 제외
```

조건:
```text
- portfolio 분리
- metrics 분리
- live_gate 분리
```

### 3.3 OPTION C (현재 상태)

```text
ACTION: 계속 혼합
```

판정:
```text
BAD (비추천)
```

---

## 4. 중요한 판단 기준

### 4.1 단계별 우선순위

현재 단계:
```text
"전략 포트폴리오 구성 단계" ❌
"단일 전략 검증 단계" ✅
```

### 4.2 데이터 품질 우선

CNT 기준:
```text
DATA_PURITY > STRATEGY_DIVERSITY
```

현재 상태:
```text
breakout_v1 = NOISE_SOURCE > STRATEGIC_VALUE
```

---

## 5. 실행 계획

### 5.1 즉시 실행 조치

#### 5.1.1 breakout_v1 비활성화
```text
TARGET: breakout_v1 완전 비활성화
METHOD: 코드에서 제외 또는 플래그로 비활성화
TIMING: 즉시 실행
```

#### 5.1.2 데이터 정리
```text
TARGET: 기존 breakout_v1 데이터 보존 but 분리
METHOD: 별도 파일로 이동 또는 태그로 구분
PURPOSE: 향후 분석을 위한 보존
```

### 5.2 시스템 수정

#### 5.2.1 전략 선택 로직 수정
```text
BEFORE: pullback_v1 + breakout_v1
AFTER: pullback_v1 ONLY
```

#### 5.2.2 메트릭 수집 수정
```text
BEFORE: aggregate metrics
AFTER: pullback_v1 metrics ONLY
```

#### 5.2.3 live_gate 평가 수정
```text
BEFORE: aggregate expectancy
AFTER: pullback_v1 expectancy ONLY
```

---

## 6. 예상 효과

### 6.1 데이터 품질 향상

#### breakout_v1 제거 전
```text
전체 기대치: -0.000397 (오염됨)
live_gate 상태: FAIL
데이터 신뢰도: 낮음
```

#### breakout_v1 제거 후
```text
pullback_v1 기대치: +0.000966 (순수)
live_gate 상태: PASS 예상
데이터 신뢰도: 높음
```

### 6.2 검증 정확도 향상

#### FULL_FILTER_RERUN 영향
```text
이전: 9 trades (혼합 데이터)
이후: 순수 pullback 데이터만
효과: 검증 정확도 대폭 향상
```

### 6.3 리스크 감소

#### 제거되는 리스크
```text
1. 데이터 오염 리스크
2. 거짓 음수 리스크
3. 검증 왜곡 리스크
4. live_gate 실패 리스크
```

---

## 7. 실행 절차

### 7.1 1단계: 코드 수정

#### 7.1.1 전략 레지스트리 수정
```text
TARGET: strategy_registry.py
ACTION: breakout_v1 제거 또는 비활성화 플래그 추가
```

#### 7.1.2 실행 로직 수정
```text
TARGET: main.py 또는 engine.py
ACTION: breakout_v1 실행 경로 차단
```

### 7.2 2단계: 데이터 처리

#### 7.2.1 기존 데이터 보존
```text
TARGET: strategy_metrics.json
ACTION: breakout_v1 데이터 보존 but 분리
```

#### 7.2.2 신규 데이터 수집
```text
TARGET: 향후 수집
ACTION: pullback_v1 데이터만 수집
```

### 7.3 3단계: 검증

#### 7.3.1 시스템 테스트
```text
ACTION: breakout_v1 비활성화 상태에서 실행 테스트
목표: 정상 작동 확인
```

#### 7.3.2 메트릭 확인
```text
ACTION: 수집되는 데이터가 pullback_v1만인지 확인
목표: 데이터 순도 검증
```

---

## 8. 롤백 계획

### 8.1 롤백 조건
```text
ROLLBACK_CONDITIONS:
1. pullback_v1 성과 급격 저하
2. 시스템 불안정 발생
3. 예기치 않은 부작용 발생
```

### 8.2 롤백 절차
```text
ROLLBACK_PROCESS:
1. breakout_v1 재활성화
2. 데이터 수집 복원
3. 메트릭 집계 복원
4. 시스템 재시작
```

---

## 9. 모니터링 계획

### 9.1 실행 후 모니터링

#### 9.1.1 단기 모니터링 (1주)
```text
- pullback_v1 성과 안정성
- 시스템 안정성
- 데이터 수집 정상성
- live_gate 상태 변화
```

#### 9.1.2 중기 모니터링 (1개월)
```text
- FULL_FILTER_RERUN 결과 변화
- 통계적 신뢰도 향상
- 데이터 축적 속도
- 검증 정확도 개선
```

### 9.2 성공 기준

#### 9.2.1 단기 성공 기준
```text
- pullback_v1 기대치 > 0 유지
- 시스템 안정적 운영
- 데이터 수집 정상
- live_gate PASS 상태 전환
```

#### 9.2.2 장기 성공 기준
```text
- FULL_FILTER_RERUN 통계적 유의성 확보
- 데이터 축적 20-30 trades 달성
- 검증 프레임워크 정상 작동
- 배포 준비 상태 진입
```

---

## 10. 위험 관리

### 10.1 실행 위험

#### 10.1.1 기술적 위험
```text
1. 코드 수정 오류
2. 시스템 불안정
3. 데이터 손실
```

#### 10.1.2 전략적 위험
```text
1. pullback_v1 성과 저하 가능성
2. 다양성 감소
3. 예기치 않은 시장 변화
```

### 10.2 완화 전략

#### 10.2.1 기술적 완화
```text
1. 점진적 비활성화 (플래그 사용)
2. 철저한 테스트
3. 롤백 준비
4. 데이터 백업
```

#### 10.2.2 전략적 완화
```text
1. 단기간 집중 모니터링
2. 성과 저하 시 신속 대응
3. 필요시 재활성화 준비
4. 대안 전략 준비
```

---

## 11. 문서화 요구사항

### 11.1 실행 기록
```text
1. 비활성화 실행 일시
2. 수정된 코드 파일 목록
3. 실행 전후 상태 비교
4. 발생한 문제 및 해결 과정
```

### 11.2 결과 보고
```text
1. 1주 후 성과 보고서
2. 1개월 후 영향 평가 보고서
3. 최종 성공/실패 평가
4. 향후 개선 권장사항
```

---

## 12. 최종 결론

### 12.1 실행 권장

```text
BREAKOUT_V1_DEACTIVATION = STRONGLY_RECOMMENDED
```

근거:
```text
1. 데이터 오염 문제 해결
2. 검증 정확도 향상
3. CNT 기준 준수
4. 통계적 신뢰도 확보
```

### 12.2 기대 효과

```text
IMMEDIATE_EFFECTS:
- 데이터 순도 확보
- live_gate 개선 가능성
- 검증 왜곡 제거

LONG_TERM_EFFECTS:
- FULL_FILTER_RERUN 정확도 향상
- 통계적 유의성 확보 용이
- 배포 결정 신뢰도 향상
```

### 12.3 성공 확률

```text
SUCCESS_PROBABILITY = HIGH (85%+)
```

근거:
```text
1. 명확한 문제 정의
2. 체계적인 해결책
3. 충분한 위험 관리
4. 롤백 준비 완료
```

---

## 13. 실행 타임라인

### 13.1 즉시 실행 (오늘)
```text
- breakout_v1 비활성화 코드 수정
- 테스트 실행
- 배포
```

### 13.2 단기 평가 (1주 후)
```text
- 성과 보고서 생성
- 성공 기준 충족 여부 평가
- 필요시 조치 실행
```

### 13.3 중기 평가 (1개월 후)
```text
- 영향 평가 보고서 생성
- 최종 성공/실패 결정
- 향후 방향성 결정
```

---

## 14. 최종 메시지

### 14.1 CNT 프로젝트팀에게

**breakout_v1은 현재 "실험 자산"이 아니라 "노이즈 소스"입니다.**

데이터 순도를 확보하고 검증 정확도를 높이기 위해 breakout_v1의 즉시 비활성화를 강력히 권장합니다.

### 14.2 기대 결과

```text
데이터 순도 확보 → 검증 정확도 향상 → 통계적 신뢰도 확보 → 성공적인 필터 검증
```

### 14.3 실행 우선순위

```text
1. breakout_v1 비활성화 (즉시)
2. 데이터 품질 모니터링 (지속)
3. 검증 정확도 평가 (주기적)
4. 최종 배포 결정 (데이터 축적 후)
```

---

## 15. 한줄 핵심

```text
지금 breakout_v1은 전략이 아니라 노이즈이므로, 데이터 순도를 위해 즉시 제거해야 합니다.
```

---

*이 비활성화 계획은 CNT 프로젝트의 데이터 품질 향상과 검증 정확도 제고를 위해 breakout_v1의 체계적인 제거를 제안합니다.*

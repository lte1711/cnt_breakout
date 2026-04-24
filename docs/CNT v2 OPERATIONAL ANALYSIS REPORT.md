---
aliases:
  - CNT v2 OPERATIONAL ANALYSIS REPORT
---

# CNT v2 OPERATIONAL ANALYSIS REPORT (REVISED)

시스템 버전: CNT v2.0
분석 기준일: 2026-04-19
환경: Binance Testnet (ETHUSDT, 5m / 1m)

---

## 1. SYSTEM STATUS

STATUS = ACTIVE
SCHEDULER = RUNNING (10min interval)
DATA_COLLECTION = STARTED
LIVE_GATE = NOT_READY
REASON = INSUFFICIENT_SAMPLE

현재 시스템은 정상적으로 실행 중이며 데이터 수집 단계에 있다. 운영 차단 요소는 존재하지 않는다.

---

## 2. ARCHITECTURE OVERVIEW

CNT v2는 다음 4단계 파이프라인으로 구성된다.

1. Signal Generation (3 strategies)
2. Signal Ranking (signal_ranker)
3. Risk Evaluation (portfolio + risk_guard)
4. Execution + Exit Management (engine + enhanced_exit_manager)

state.json 기반 상태머신 구조로 pending → open_trade → closed 상태 전이를 관리한다.

---

## 3. STRATEGY STATUS

### 3.1 breakout_v1

상태: NOT_SELECTED
신호 발생: 있음
선택: 0

원인:

* ATR expansion 조건 과도
* pullback 대비 ranking 경쟁 열위
* 동시 신호 발생 빈도 낮음

판정:
문제는 맞지만 구조 오류가 아닌 파라미터/경쟁 문제
Phase 2 이후 조정 대상

---

### 3.2 pullback_v1

상태: ACTIVE
거래: 2
성과: 1 win / 1 loss
expectancy: 양수

판정:
현재 유일한 실행 전략
샘플 부족으로 성능 판단 불가
운영 유지

---

### 3.3 mean_reversion_v1

상태: REGISTERED_NOT_ACTIVE
판정: 별도 검증 후 활성화 필요

---

## 4. EXECUTION FLOW (핵심 요약)

engine.run_cycle() 흐름:

1. 상태 로드 (state.json / portfolio_state.json)
2. pending 처리
3. open_trade exit 평가
4. 신규 진입 평가

---

### EXIT FAILSAFE (중요 패치 반영)

pending 상태에서:

* TARGET LIMIT 존재
* 동시에 STOP/TRAILING 조건 발생 시

동작:

1. 기존 LIMIT 주문 cancel
2. 즉시 MARKET 청산 실행

이 기능은 손절 미실행 문제를 방지하는 핵심 안전장치이다.

---

## 5. PERFORMANCE STATUS

closed_trades = 2
win = 1
loss = 1
expectancy > 0
profit_factor > 1

판정:

현재 데이터는 통계적으로 의미 없음
성능 평가 금지 상태

status = SAMPLE_INSUFFICIENT

---

## 6. ISSUE CLASSIFICATION

### 6.1 실제 문제

1. breakout_v1 선택율 0
   → Phase 2 이후 조정 필요

---

### 6.2 정상 상태 (문제 아님)

1. no_ranked_signal 발생
   → 전략 동시 신호 없음 (정상)

2. 낮은 선택율
   → 초기 데이터 부족 상태

3. expectancy_weighted 비활성
   → sample < 5 (정상 동작)

---

## 7. CURRENT PHASE

CURRENT_PHASE = DATA_COLLECTION_RUNNING

시스템은 이미 실행 중이며 데이터 누적 단계에 있다.
재시작 또는 구조 수정은 필요하지 않다.

---

## 8. NEXT STEP PLAN

### Phase 1 — Data Collection (현재 단계)

조건:

* closed_trades < 20

행동:

* 시스템 지속 실행
* 코드 수정 금지
* 로그 누적 유지

---

### Phase 2 — Ranking Activation

조건:

* closed_trades >= 5

행동:

* expectancy_weighted 활성 확인
* 전략별 성과 비교 시작

---

### Phase 3 — Strategy Adjustment

조건:

* breakout_v1 선택율 0 유지

행동:

* ATR multiplier 완화
* signal_age_limit 조정

---

### Phase 4 — Live Gate Evaluation

조건:

* closed_trades >= 20

행동:

* live_gate_evaluator 실행
* PASS / FAIL 판단

---

### Phase 5 — Risk Expansion

조건:

* LIVE_READY 달성

행동:

* capital allocation
* adaptive risk 적용

---

## 9. FINAL CONCLUSION

현재 상태는 시스템 문제 상태가 아니다.

데이터 부족 상태이며 정상적으로 운영 중이다.

판정:

SYSTEM_STATUS = HEALTHY
OPERATION = CONTINUE
ACTION = NO_CHANGE

---

## 10. IMMEDIATE ACTION

1. 시스템 그대로 유지
2. 스케줄러 지속 실행
3. 로그 모니터링만 수행

금지 사항:

* 전략 파라미터 수정
* 랭커 구조 변경
* 리스크 정책 변경

---

---

## Obsidian Links

- [[00 Docs Index]]


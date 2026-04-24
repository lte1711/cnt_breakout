---
aliases:
  - CNT v2 PHASE 1 OPERATION MONITORING INSTRUCTION KO
---

# CNT v2 PHASE 1 운영 모니터링 지시

이 단계에서는 시스템을 더 손대는 것이 아니라, **관측과 자동 감시 체계를 붙이는 것**이 핵심이다.

즉 Phase 1에서 필요한 것은 단순 데이터 수집이 아니라, 이상 징후를 자동으로 감시하는 구조다.

---

## 1. 목적

```text
목표 = 데이터 누적 + 이상 징후 자동 감시
```

현재 테스트넷이 정상 동작 중이므로, 개입 없이 감시만 하는 구조를 만든다.

---

## 2. 모니터링 대상

### 2.1 거래 누적 상태

* closed_trades
* runtime_hours

판단 기준:

```text
closed_trades >= 20 -> Phase 2 진입 가능
```

### 2.2 랭커 상태

* rank_score
* rank_score_components

이상 조건:

```text
rank_score == 0 이 20회 이상 연속 발생 -> 이상
```

### 2.3 전략 선택 분포

* selected_strategy

이상 조건:

```text
단일 전략만 30회 이상 연속 선택 -> 편향
```

### 2.4 리스크 트리거

* daily_loss_count
* consecutive_losses

이상 조건:

```text
consecutive_losses >= 3 -> 경고
consecutive_losses >= 5 -> 위험
```

### 2.5 exit failsafe 동작 여부

로그 확인:

```text
SELL_SUBMITTED -> cancel -> STOP_MARKET_FILLED
```

이상 조건:

```text
STOP 조건이 발생했는데 LIMIT 주문만 있고 MARKET exit가 없음
```

---

## 3. 자동 감시 스크립트 설계

파일:
`scripts/monitor_runtime.py`

기능:

```python
1. portfolio.log 읽기
2. 최근 구간 분석
3. 이상 조건 검사
4. 결과 출력
```

감시 로직:

#### 1. rank_score 이상

```python
if last_20_rank_scores == 0:
    alert("RANKER_STUCK")
```

#### 2. 전략 편향

```python
if same_strategy_count >= 30:
    alert("STRATEGY_BIAS")
```

#### 3. 거래 없음

```python
if closed_trades == 0 for 6 hours:
    alert("NO_EXECUTION")
```

#### 4. failsafe 실패

```python
if stop_condition_detected and no_market_exit:
    alert("EXIT_FAILSAFE_FAILURE")
```

---

## 4. 실행 방식

### 옵션 A (권장)

Task Scheduler에 추가:

```text
monitor_runtime.py
-> 10분마다 실행
```

### 옵션 B

`run.ps1` 내부에 포함

---

## 5. 출력 형식 예시

```text
[MONITOR REPORT]

status = OK / WARNING / CRITICAL

closed_trades = X
rank_score_zero_streak = X
strategy_bias = NONE / DETECTED
risk_level = NORMAL / WARNING
failsafe = OK / CHECK_REQUIRED
```

---

## 6. 운영 규칙

```text
Phase 1에서는 수정하지 않는다
```

금지:

* 전략 파라미터 수정
* 랭커 수정
* 리스크 정책 수정

허용:

* 로그 분석
* 모니터링 추가

---

## 7. Phase 전환 조건

### Phase 2 진입

```text
closed_trades >= 5
```

### Phase 3 진입

```text
closed_trades >= 20
```

---

## 8. 즉시 실행 순서

1. `monitor_runtime.py` 생성
2. scheduler 등록 (10분 주기)
3. 1~2시간 로그 정상 흐름 확인
4. 이후 개입 없이 유지

---

# 최종 결론

```text
지금 단계 = 시스템 개선 단계가 아님
지금 단계 = 관측 단계
```

## Obsidian Links

- [[CNT v2 VALIDATION REPORT KO]]



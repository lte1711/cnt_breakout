---
tags:
  - cnt
  - type/documentation
  - status/active
  - type/operation
  - risk
  - type/validation
  - status/completed
  - cnt-v2-post-operational-patch-work-instruction
---

좋다. 지금 상태는 “운영 가능”까지 올라왔고, 남은 건 **정밀도/관측 품질/아키텍처 일관성 보완 단계**다.

아래는 바로 적용 가능한 **후속 보완 패치 지시서 (Post-Operational Patch)**다.

---

# CNT v2 POST-OPERATIONAL PATCH WORK INSTRUCTION

문서 목적:
CNT v2가 운영 가능 상태에 도달한 이후,

* 로그 신뢰도 개선
* 리스크/상태 정합성 강화
* 아키텍처 일관성 확보
  를 위한 **2차 보완 패치 수행**

문서 상태:
Post-Patch / Non-blocking but Required for Production Quality

---

# 1. 현재 상태 요약

##  완료

* P0 (운영 차단 버그): 해결됨
* P1 (핵심 기능 결함): 해결됨
* P2 (파라미터 검증): 강화 완료

##  남은 항목

1. error signal → stale_signal 로그 오염
2. risk_metrics 구조 분산 (engine vs risk_guard)
3. order_router 미연결 (구조 vs 실행 불일치)
4. portfolio_state 재구성 기반 구조 (증분 업데이트 없음)

---

# 2. P3 — 로그 및 관측 품질 개선

## P3-1. error signal stale 오염 제거

### 대상

* `src/strategy_manager.py`
* `src/entry_gate.py`

### 문제

```python
signal_age_limit_sec=0
```

→ entry_gate에서 stale 검사 대상이 됨

현재 영향:

* 실제로는 entry 차단이 먼저 걸리지만
* 로그에 `stale_signal` reason이 남을 수 있음

### 수정 요구

#### 방법 A (권장)

```python
signal_age_limit_sec = -1
```

→ "age check skip" 의미로 통일

#### 방법 B

entry_gate에서:

```python
if not signal.entry_allowed:
    return ...
# stale 체크 이전에 종료 유지
```

(이미 되어 있으나 방어 로직 강화 가능)

### 완료 조건

* error signal 발생 시

  * reason이 `strategy_error:*`로만 기록
  * `stale_signal` 로그 발생하지 않음

---

# 3. P3 — Risk Metrics 구조 통합

## P3-2. risk_metrics 단일 책임화

### 대상

* `src/engine.py`
* `src/risk/risk_guard.py`

### 문제

현재:

* engine → risk_metrics 업데이트
* risk_guard → 일부 reset 수행

 책임이 분산됨

---

### 수정 요구

#### 1. risk_metrics 관리 책임을 engine으로 통일

* `risk_guard.py`에서:

  * `_reset_daily_loss_count_if_needed()` 제거 또는 비활성화

* engine만:

  * 증가
  * reset
  * timestamp 관리

---

#### 2. risk_guard는 read-only로 전환

```python
evaluate_risk(risk_metrics)
```

→ 판단만 수행

---

### 완료 조건

* risk_metrics write 경로 = engine 단일화
* risk_guard는 side-effect 없음

---

# 4. P3 — Portfolio State 정확도 강화

## P3-3. portfolio_state 재구성 방식 보완

### 현재 구조

* 매 실행마다 `runtime_state` 기반으로 재구성

### 문제

* intra-cycle 상태 추적 불가
* partial exit / multi-position 확장 시 취약

---

### 수정 요구 (선택적, 권장)

#### 단계 1 (경량 개선)

* `portfolio_state.json`에 아래 필드 추가:

```json
{
  "last_update_time": timestamp,
  "source": "rebuild_from_runtime"
}
```

#### 단계 2 (확장 대비)

* `open_positions`를 단일이 아닌 list 구조 유지 (이미 되어 있음)
* partial exit 시 qty 반영 로직 명확화

---

### 완료 조건

* portfolio_state가 “현재 상태 스냅샷”임이 명확히 표현됨
* 향후 multi-position 확장 시 구조 변경 없이 확장 가능

---

# 5. P3 — Order Router 정합성 개선

## P3-4. order_router 상태 명확화

### 현재 상태

* 코드 존재
* runtime 미연결
* 문서에 명시됨

---

### 선택지

## 선택 A (권장 — 점진적 연결)

### 단계 1

engine 주문 경로:

```python
send_live_testnet_order(...)
```

→

```python
route_order(...)
```

### 단계 2

* 내부에서:

  * spot_adapter
  * futures_adapter

분기

---

## 선택 B (유지)

* 문서에 아래 문구 유지:

```
order_router is prepared but not connected to runtime execution path
```

---

### 완료 조건

* 코드와 문서가 완전히 동일한 상태 설명

---

# 6. P3 — Signal / Strategy 정합성 강화

## P3-5. signal_age_limit 정책 표준화

### 문제

* 일부 전략: `0`
* 일부 전략: `>0`
* 일부: 없음

---

### 수정 요구

표준:

```python
-1 → age check 없음
>0 → 유효 시간
```

### 모든 전략에 적용:

* `pullback_v1`
* `mean_reversion_v1`
* 기타

---

### 완료 조건

* `0` 값 사용 제거
* validate_params에서 강제

---

# 7. P4 — 선택적 고급 개선 (권장)

## P4-1. signal_ranker 고도화

현재:

* 단순 선택

개선:

* 기대값 기반
* volatility weighting
* winrate history 반영

---

## P4-2. exit 전략 v2 통합

현재:

* entry 중심 구조

다음:

* `enhanced_exit_manager` 포트폴리오 레벨 통합

---

# 8. 검증 지시

## 필수

### 로그 검증

* error signal → stale_signal 미출력 확인

### risk 검증

* risk_guard가 write 하지 않는지 확인

### portfolio 검증

* state 재구성 consistency 유지

---

## 선택

### router 연결 시

* spot / futures 분기 테스트

---

# 9. 완료 판정

| 단계       | 상태           |
| -------- | ------------ |
| P3 완료    |  운영 안정화     |
| P4 일부 적용 |  전략 고도화 시작  |
| P4 전체    |  수익화 단계 진입 |

---

# 10. 최종 결론

> CNT v2는 이제
> **"돌아가는 시스템" → "신뢰 가능한 시스템" 단계로 진입했다**

그리고 다음 단계는 명확하다:

>  **이제 문제는 구조가 아니라 성능이다**

---

---

## Obsidian Links

- [[00 Docs Index]]


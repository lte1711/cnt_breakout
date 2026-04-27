---
tags:
  - cnt
  - type/documentation
  - status/active
  - type/operation
  - risk
  - type/validation
  - status/completed
  - cnt-v2-post-operational-patch-work-instruction-ko
---

# CNT v2 운영 후속 패치 작업 지시

문서 목적:

CNT v2가 운영 가능한 상태에 도달한 이후,

* 로그 흐름 개선
* 리스크 상태 정합성 강화
* 아키텍처 의미 명확화

를 위한 **2차 보완 패치 수행 지시**다.

문서 상태:

Post-Patch / Non-blocking but Required for Production Quality

---

# 1. 현재 상태 요약

완료:

* P0 (운영 차단 버그): 해결
* P1 (기능 정합성 결함): 해결
* P2 (파라미터 검증): 강화 완료

남은 항목:

1. error signal과 stale_signal 로그 분리
2. risk_metrics 책임 분산 (engine vs risk_guard)
3. order_router 미연결 상태 명확화
4. portfolio_state 재구성 기반 구조 보완

---

# 2. P3 로그 및 관측 정합성 개선

## P3-1. error signal stale 오염 제거

대상:

* `src/strategy_manager.py`
* `src/entry_gate.py`

문제:

strategy error signal이 stale check와 섞여 `stale_signal` reason으로도 보일 수 있음

수정 요구:

### 방법 A (권장)

```python
signal_age_limit_sec = -1
```

즉 "age check skip" 의미로 통일

### 방법 B

`entry_gate`에서:

```python
if not signal.entry_allowed:
    return ...
```

로 stale check 전에 조기 종료 방어 강화

완료 조건:

* error signal 발생 시 reason은 `strategy_error:*`만 기록
* `stale_signal` 오염 로그가 생기지 않음

---

# 3. P3 Risk Metrics 구조 통합

## P3-2. risk_metrics 단일 책임화

대상:

* `src/engine.py`
* `src/risk/risk_guard.py`

문제:

현재 구조:

* engine이 risk_metrics 업데이트
* risk_guard가 일부 reset 수행

즉 책임이 분산돼 있음

수정 요구:

### 1. risk_metrics 관리 책임을 engine으로 통일

* `risk_guard.py`에서 side-effect 제거
* engine만
  * 증가
  * reset
  * timestamp 관리

### 2. risk_guard는 read-only로 전환

```python
evaluate_risk(risk_metrics)
```

처럼 판단만 수행

완료 조건:

* risk_metrics write 경로 = engine 단일
* risk_guard는 side-effect 없음

---

# 4. P3 Portfolio State 정확성 강화

## P3-3. portfolio_state 재구성 방식 보완

현재 구조:

* 매 실행마다 `runtime_state` 기반으로 재구성

문제:

* intra-cycle 상태 추적 불가
* partial exit / multi-position 확장 시 취약

수정 요구:

### 단계 1 (경량 개선)

`portfolio_state.json`에 아래 필드 추가:

```json
{
  "last_update_time": "timestamp",
  "source": "rebuild_from_runtime"
}
```

### 단계 2 (확장 대비)

* `open_positions`를 단일 값이 아닌 list 구조로 유지
* partial exit 시 qty 반영 로직 명확화

완료 조건:

* portfolio_state가 현재 구현이 snapshot rebuild 결과임을 명확히 표현
* 향후 multi-position 확장 시 구조 재설계 없이 확장 가능

---

# 5. P3 Order Router 정합성 개선

## P3-4. order_router 상태 명확화

현재 상태:

* 코드 존재
* runtime 미연결
* 문서에만 명시

선택지:

## 선택 A (권장 아님 - 실제 엔진 연결)

engine 주문 경로:

```python
send_live_testnet_order(...)
```

를

```python
route_order(...)
```

로 통합

## 선택 B (유지)

문서에 아래 문구 유지:

```text
order_router is prepared but not connected to runtime execution path
```

완료 조건:

* 코드와 문서가 완전히 같은 상태를 설명

---

# 6. P3 Signal / Strategy 정합성 강화

## P3-5. signal_age_limit 정책 통일

문제:

* 일부 전략은 `0`
* 일부 전략은 `>0`
* 일부는 없음

수정 요구:

정책:

```python
-1 -> age check 없음
>0 -> 유효 시간 제한
```

모든 전략에 공통 적용:

* `pullback_v1`
* `mean_reversion_v1`
* 기타 전략

## Obsidian Links

- [[00 Docs Index KO]]



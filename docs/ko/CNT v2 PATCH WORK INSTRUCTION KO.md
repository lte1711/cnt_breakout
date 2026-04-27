---
tags:
  - cnt
  - type/documentation
  - status/active
  - market-context
  - risk
  - strategy/pullback_v1
  - type/validation
  - status/completed
  - cnt-v2-patch-work-instruction-ko
---

# CNT v2 패치 작업 지시

문서 목적:

CNT v2 초기 구현에서 확인된 운영 차단 버그와 구조-구현 불일치를 수정하여, 운영 이전 최소 정합성을 확보하기 위한 패치 지시서다.

문서 상태:

Patch Instruction / Mandatory Fix

적용 우선순위:

P0 -> P1 -> P2 순서로만 진행한다.  
P0 완료 전에는 운영 기준 사용을 금지한다.

---

# 1. 패치 범위 요약

이번 패치의 목표는 아래 6가지다.

1. `engine.py` pending 처리 제어 흐름 복구
2. 손실 확정 시 `risk_metrics` 업데이트 구현
3. portfolio exposure 계산을 실제 주문 수량 기준으로 수정
4. `mean_reversion_v1` 활성 여부를 코드/문서와 일치시킴
5. `order_router`를 실제 엔진 경로에 연결하거나, 미연결 상태를 문서에 명시
6. `pullback_v1`, `mean_reversion_v1` 파라미터 검증 강화

---

# 2. P0 필수 패치

## P0-1. `engine.py` pending 처리 제어 흐름 수정

대상 파일:

* `src/engine.py`

문제:

* pending 처리 블록 안에서 `return` 위치가 잘못되어 일부 분기가 실행되지 않는 경우가 있음
* `PROMOTE_TO_OPEN_TRADE`와 pending action 처리 경로가 정상 도달하지 않을 수 있음

수정 요구:

* `if pending:` 블록 안에서 action별 분기가 모두 독립적으로 도달 가능하도록 제어 흐름을 복구
* 아래 action은 각각 독립적으로 저장 후 종료해야 함
  * `PROMOTE_TO_OPEN_TRADE`
  * `PARTIAL_EXIT_FILLED`
  * 기타 generic pending action save path

권장 구조:

```python
if pending:
    action, reason = evaluate_pending_order(...)

    if action == "PROMOTE_TO_OPEN_TRADE":
        _save_and_finish(...)
        return

    if action == "PARTIAL_EXIT_FILLED":
        _save_and_finish(...)
        return

    _save_and_finish(...)
    return
```

완료 조건:

* `PROMOTE_TO_OPEN_TRADE` 정상 도달
* `PARTIAL_EXIT_FILLED` 정상 도달 및 저장
* 일반 pending action 저장 정상 동작
* log와 state 파일 정합 확인

## P0-2. 손실 카운터 업데이트 구현

대상 파일:

* `src/engine.py`
* 필요 시 `src/risk/risk_guard.py`

문제:

* `daily_loss_count`, `consecutive_losses`, `last_loss_time`가 state에 있긴 하지만 실제 손실 확정 시 갱신되지 않는 상태였음
* 결과적으로 `DAILY_LOSS_LIMIT`, `LOSS_COOLDOWN`이 발동하지 않을 위험이 있었음

수정 요구:

* 손실 종료가 확정되는 action에서 손실 카운터 갱신
* 최소 대상 action
  * `STOP_MARKET_FILLED`
  * `TRAILING_STOP_FILLED`
* 필요 시 `SELL_FILLED`도 실현손익 기준으로 손실 여부 반영

필수 반영 로직:

```python
risk_metrics["daily_loss_count"] += 1
risk_metrics["consecutive_losses"] += 1
risk_metrics["last_loss_time"] = now_ts
```

추가 반영:

* 이익 종료 시

```python
risk_metrics["consecutive_losses"] = 0
```

* 날짜가 바뀌면

```python
risk_metrics["daily_loss_count"] = 0
```

완료 조건:

* 손실 1회 후 `daily_loss_count=1`
* 손실 연속 발생 시 `consecutive_losses` 증가
* `LOSS_COOLDOWN` 차단 확인
* 일일 손실 횟수 초과 시 `DAILY_LOSS_LIMIT` 차단 확인

---

# 3. P1 기능 정합성 패치

## P1-1. portfolio exposure 계산을 실제 수량 기준으로 수정

대상 파일:

* `src/risk/portfolio_risk_manager.py`
* `src/execution_decider.py`

문제:

* 고정 수량 기반 계산 때문에 exposure limit가 실제 주문 규모를 제대로 반영하지 못함

수정 요구:

* 하드코딩된 기준 제거
* 실제 주문 예정 수량 또는 notional 기준으로 exposure 계산

완료 조건:

* 소형 주문 허용 테스트 통과
* 초과 주문 차단 테스트 통과
* `MAX_PORTFOLIO_EXPOSURE`가 실제 주문 크기와 연동됨을 확인

## P1-2. `mean_reversion_v1` 활성 정책 명확화

대상 파일:

* `config.py`
* 관련 문서

문제:

* registry와 params에는 존재하지만 `ACTIVE_STRATEGIES`에는 없어서 실제로는 실행되지 않는 상태

결정 요구:

* 활성 전략인지, 등록만 된 비활성 전략인지 코드와 문서에서 명시적으로 정리

완료 조건:

* 코드와 문서의 활성 범위가 일치
* 실행 범위에 대한 설명이 모호하지 않음

## P1-3. `order_router` 상태 명확화

대상 파일:

* `src/engine.py`
* `src/execution/order_router.py`
* 관련 문서

문제:

* `order_router` 구조는 존재하지만 실제 런타임 경로에서는 사용되지 않는 상태

결정 요구:

* 실제로 연결할지, 아니면 준비만 된 미연결 컴포넌트로 둘지 명시

완료 조건:

* 코드와 문서가 완전히 같은 상태를 설명

---

# 4. P2 파라미터 검증 강화

## P2-1. signal_age_limit 정책 명확화

문제:

* 일부 전략은 `0`
* 일부 전략은 `>0`
* 일부 전략은 없음

수정 요구:

정책:

```python
-1  -> age check 없음
>0  -> 유효 시간 제한
```

모든 전략에 적용:

* `pullback_v1`
* `mean_reversion_v1`
* 기타 전략

완료 조건:

* age policy가 전략 전체에 일관되게 적용

## Obsidian Links

- [[CNT v2 VALIDATION REPORT KO]]



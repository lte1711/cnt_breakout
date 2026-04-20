아래는 바로 적용 가능한 **`CNT v2 PATCH WORK INSTRUCTION.md`** 문안이다.

---

# CNT v2 PATCH WORK INSTRUCTION

문서 목적:
CNT v2 초기 구현에서 확인된 운영 차단 버그와 구조-구현 불일치를 수정하여, 실거래 이전 최소 운영 정합성을 확보한다.

문서 상태:
Patch Instruction / Mandatory Fix

적용 우선순위:
P0 → P1 → P2 순서로만 진행한다.
P0 완료 전에는 운영 기준 사용을 금지한다.

---

# 1. 패치 범위 요약

이번 패치의 목표는 아래 6개다.

1. `engine.py` pending 처리 제어흐름 복구
2. 손실 확정 시 `risk_metrics` 업데이트 구현
3. portfolio exposure 계산을 실제 주문 수량 기준으로 수정
4. `mean_reversion_v1` 활성 여부를 코드/문서에 일치시킴
5. `order_router`를 실제 엔진 경로에 연결하거나 미연결 상태를 문서에 명시
6. `pullback_v1`, `mean_reversion_v1` 파라미터 검증 강화

---

# 2. P0 필수 패치 — 운영 차단 해소

## P0-1. `engine.py` pending 처리 제어흐름 수정

대상 파일:

* `src/engine.py`

문제:

* pending 처리 블록 내부에서 `return` 위치가 잘못되어 일부 분기가 절대 실행되지 않는다.
* `PROMOTE_TO_OPEN_TRADE` 외 pending action 처리 경로가 정상 저장되지 않을 수 있다.

수정 요구:

* `if pending:` 블록 내부에서 action별 분기가 모두 도달 가능하도록 제어흐름을 재구성한다.
* 다음 action은 각각 독립적으로 저장 후 종료되어야 한다.

  * `PROMOTE_TO_OPEN_TRADE`
  * `PARTIAL_EXIT_FILLED`
  * 기타 pending action generic save path

구현 원칙:

* 각 action 처리 분기 안에서 `_save_and_finish(...)` 호출 후 `return`
* 블록 중간의 무조건 `return` 금지
* dead code 금지
* pending 상태 변경이 발생하면 반드시 상태 저장 수행

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

* `PROMOTE_TO_OPEN_TRADE` 정상 저장
* `PARTIAL_EXIT_FILLED` 정상 도달 및 저장
* 일반 pending action 저장 정상 동작
* 로그 및 state 파일 정합성 확인

---

## P0-2. 손실 카운터 업데이트 구현

대상 파일:

* `src/engine.py`
* 필요 시 `src/risk/risk_guard.py`

문제:

* `daily_loss_count`, `consecutive_losses`, `last_loss_time`가 읽히기만 하고 실제 손실 확정 시 갱신되지 않는다.
* 결과적으로 `DAILY_LOSS_LIMIT`, `LOSS_COOLDOWN`이 발동되지 않는다.

수정 요구:

* 손실 종료가 확정되는 action에서 손실 카운터를 갱신한다.
* 최소 대상 action:

  * `STOP_MARKET_FILLED`
  * `TRAILING_STOP_FILLED`
* 필요 시 `SELL_FILLED`도 실현손익 기준으로 손실 여부 판단 후 반영

필수 반영 로직:

```python
risk_metrics["daily_loss_count"] += 1
risk_metrics["consecutive_losses"] += 1
risk_metrics["last_loss_time"] = now_ts
```

추가 반영:

* 이익 종료 시:

```python
risk_metrics["consecutive_losses"] = 0
```

* 날짜가 바뀌면:

```python
risk_metrics["daily_loss_count"] = 0
```

구현 원칙:

* 손실 확정은 “실제 청산 결과” 기준으로 판정한다.
* pending 단계가 아니라 filled 단계에서만 카운트한다.
* 상태 저장 전 `risk_metrics` 값이 업데이트되어야 한다.

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
* 필요 시 관련 model 파일

문제:

* 현재 exposure 계산이 아래처럼 고정 수량에 묶여 있다.

```python
requested_exposure = float(signal.entry_price_hint or 0.0) * 0.001
```

* 실제 주문 수량과 무관하여 exposure limit가 사실상 무의미하다.

수정 요구:

* 하드코딩 `0.001` 제거
* 실제 주문 예정 수량 또는 notional 기준으로 exposure 계산
* portfolio risk check에 아래 중 하나를 전달하도록 변경

  * `requested_qty`
  * `validated_qty`
  * `requested_notional`
  * `notional_value`

권장 방식:

* `execution_decider`에서 계산된 검증 완료 수량/금액을 `portfolio_risk_manager`에 전달
* exposure 계산:

```python
requested_exposure = entry_price * requested_qty
```

또는

```python
requested_exposure = requested_notional
```

완료 조건:

* 소액 주문 허용 테스트 통과
* 초과 주문 차단 테스트 통과
* `MAX_PORTFOLIO_EXPOSURE`가 실제 주문 크기에 따라 작동함을 확인

---

## P1-2. `mean_reversion_v1` 활성 정책 확정

대상 파일:

* `config.py`
* 문서 파일들

문제:

* registry와 params에는 존재하지만 `ACTIVE_STRATEGIES`에 없어 실제 실행되지 않는다.

결정 요구:
아래 둘 중 하나를 명시적으로 선택한다.

### 선택 A. 활성화

```python
ACTIVE_STRATEGIES = [
    "breakout_v1",
    "pullback_v1",
    "mean_reversion_v1",
]
```

### 선택 B. 기본 비활성 유지

* 문서에 “등록만 되어 있으며 기본 활성 전략은 아님” 명시
* validation report에 실행 범위를 정확히 기재

완료 조건:

* 코드와 문서가 일치해야 한다.
* 활성 전략 테스트 결과가 문서와 동일해야 한다.

---

## P1-3. `order_router` 실제 연결 또는 명시적 유보

대상 파일:

* `src/engine.py`
* `src/execution/order_router.py`
* 필요 시 `src/market/spot_adapter.py`, `src/market/futures_adapter.py`
* 문서 파일들

문제:

* `order_router` 구조는 존재하지만 실제 엔진 경로에서는 사용되지 않는다.
* 현재 주문은 직접 주문 함수 호출 경로를 따른다.

결정 요구:
아래 둘 중 하나를 선택한다.

### 선택 A. 실제 연결

* 엔진의 주문 제출 경로를 `order_router`로 통합
* spot/futures 분기 로직이 실제 실행되도록 수정

### 선택 B. 미연결 유지 + 문서 수정

* `order_router`는 v2 준비 코드이며 현재 실행 경로 미사용임을 문서에 명시
* “routing 정상” 같은 표현 제거

완료 조건:

* 아키텍처 설명과 실제 실행 경로가 일치해야 한다.
* 코드가 말하는 것과 문서가 말하는 것이 같아야 한다.

---

# 4. P2 안정성 보강 패치

## P2-1. 전략 파라미터 검증 강화

대상 파일:

* `src/strategies/pullback_v1.py`
* `src/strategies/mean_reversion_v1.py`

문제:

* `breakout_v1` 대비 검증 범위가 지나치게 약하다.
* 비정상 파라미터가 런타임까지 유입될 수 있다.

수정 요구:

### `pullback_v1`

최소 추가 검증:

* `ema_fast_period < ema_slow_period`
* `0 < pullback_rsi_min < 100`
* `0 < pullback_rsi_max < 100`
* `pullback_rsi_min < pullback_rsi_max`
* `target_pct > 0`
* `stop_loss_pct > 0`
* `signal_age_limit_sec >= -1`

### `mean_reversion_v1`

최소 추가 검증:

* `0 < rsi_oversold < 100`
* `target_pct > 0`
* `stop_loss_pct > 0`
* `signal_age_limit_sec >= -1`

완료 조건:

* 잘못된 값 입력 시 즉시 `ValueError`
* 정상 파라미터는 기존 동작 유지

---

# 5. 문서 수정 지시

대상 파일:

* `docs/CNT v2 VALIDATION REPORT.md`
* 필요 시

  * `docs/CNT v2 ARCHITECTURE DESIGN DOCUMENT.md`
  * `docs/CNT v2 IMPLEMENTATION WORK INSTRUCTION.md`
  * `docs/CNT v2 VALIDATION CHECKLIST.md`
  * `AGENTS.md`
  * `docs/EXTRA ITEMS REGISTER.md`

수정 요구:
다음 표현은 코드 수정 완료 전 사용 금지 또는 수정한다.

수정 대상 표현:

* “Risk Block 정책 적용 정확”
* “Routing 정상”
* “구조적으로 완성된 포트폴리오 트레이딩 엔진”
* “운영 준비 완료” 또는 그에 준하는 표현

수정 원칙:

* 문서는 코드 상태를 과장하면 안 된다.
* “구조 존재”와 “실행 경로 연결”을 구분해서 쓴다.
* “정책 존재”와 “실제 발동 가능”을 구분해서 쓴다.

---

# 6. 검증 지시

## 6.1 필수 컴파일 검증

* 전체 python compile 재실행
* 신규 수정 파일 import 검증

필수 통과 기준:

* syntax error 0건
* import error 0건

---

## 6.2 P0 검증

### pending 처리 검증

synthetic 또는 stub 환경에서 아래를 각각 재현한다.

* `PROMOTE_TO_OPEN_TRADE`
* `PARTIAL_EXIT_FILLED`
* 일반 pending action

확인 항목:

* 저장 함수 호출
* `state.json` 반영
* `portfolio_state.json` 반영
* runtime log 기록 정상

### risk guard 검증

손실 종료를 연속 재현하여:

* `daily_loss_count` 증가 확인
* `consecutive_losses` 증가 확인
* `LOSS_COOLDOWN` 발동 확인
* `DAILY_LOSS_LIMIT` 발동 확인

---

## 6.3 P1 검증

### exposure 검증

* 작은 주문: 허용
* 큰 주문: 차단
* 동일 심볼 중복 정책과 함께 동작 확인

### strategy activation 검증

* `ACTIVE_STRATEGIES`에 따른 실제 실행 전략 확인
* 비활성 전략이 실행되지 않는지 확인

### routing 검증

* 실제 연결한 경우: spot/futures 각각 분기 확인
* 미연결 유지한 경우: 문서와 코드 설명이 일치하는지 확인

---

## 6.4 P2 검증

### parameter validation 검증

잘못된 파라미터 입력 케이스별로:

* `ValueError` 발생 확인
* 에러 메시지 명확성 확인

---

# 7. 완료 판정 기준

## P0 완료 기준

* pending 제어흐름 버그 제거
* 손실 카운터 정상 작동
* risk guard 정책 실제 발동 확인

## P1 완료 기준

* exposure 계산이 실제 주문 기준으로 동작
* 전략 활성 범위가 코드와 문서에 일치
* routing 구조 설명이 실제와 일치

## P2 완료 기준

* 전략 파라미터 검증이 비정상 입력을 방어
* 전체 문서가 수정된 코드 상태를 정확히 반영

---

# 8. 최종 운영 판정 규칙

* P0 미완료: 운영 금지
* P0 완료, P1 미완료: 제한적 테스트만 허용
* P0 + P1 완료: 테스트 운영 가능
* P0 + P1 + P2 완료: 운영 전 최종 검증 단계 진입 가능

---

# 9. 핵심 결론

현재 CNT v2는 구조 초안이 아니라 실제 엔진 기반까지 와 있으나, 아직 운영 기준 완성 상태는 아니다.
이번 패치의 본질은 기능 추가가 아니라 **운영 정합성 복구**다.

가장 먼저 처리할 항목은 아래 두 개다.

1. `engine.py` pending 처리 제어흐름 수정
2. 손실 확정 시 `risk_metrics` 업데이트 구현

이 두 항목이 완료되기 전까지는 v2를 운영 기준으로 간주하지 않는다.

---


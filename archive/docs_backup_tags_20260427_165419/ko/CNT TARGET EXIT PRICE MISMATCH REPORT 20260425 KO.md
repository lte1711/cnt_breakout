---
tags:
  - cnt
  - ko
  - incident-review
  - exit
created: 2026-04-25
status: verified
---

# CNT Target Exit Price Mismatch Report 20260425 KO

## 요약

2026-04-25 거래 상태 점검 중, 오픈 포지션의 목표 기준가와 실제 제출된 목표 청산 주문 가격이 다르게 기록된 문제를 확인했다.

- 포지션 목표 기준가: `2322.082238`
- 실제 `SELL LIMIT` 주문 가격: `2322.74000000`
- 차이: `0.657762`
- 수량 `0.0022 ETH` 기준 추가 대기 이익: 약 `0.0014470764 USDT`
- 주문 상태: Binance Spot Testnet 기준 `NEW`, 미체결
- 현재 확인가: `2319.78`

## 확인 결과

이 문제는 거래소 가격 정렬 또는 tick size 보정 때문이 아니다. `ETHUSDT` tick size는 `0.01`이며, 목표 기준가 `2322.082238`를 tick size에 맞춰 floor하면 `2322.08` 수준이어야 한다.

실제 제출 가격 `2322.74`는 `logs/runtime.log`의 `2026-04-25 19:34:00` 실행 가격과 일치한다.

## 원인

`src/risk/enhanced_exit_manager.py`는 목표가 도달 시 `ExitSignal`에 `target_price`를 담아 반환한다.

- `src/risk/enhanced_exit_manager.py:49`
- `return ExitSignal(True, "TARGET", "target_price_triggered", float(target_price), stop_price, None)`

그러나 `src/engine.py`의 목표 청산 주문 생성 분기는 `exit_signal.target_price`를 주문 가격으로 사용하지 않는다. 대신 루프 현재가 `price`를 `auto_adjust_order_inputs()`에 전달하고, 그 결과를 주문 가격으로 사용한다.

- `src/engine.py:1150`
- `adjusted_exit = auto_adjust_order_inputs(price, exit_qty, filters)`
- `src/engine.py:1179`
- `price=float(adjusted_exit["adjusted_price"])`

따라서 목표가 `2322.082238`를 넘은 순간 현재 조회가가 `2322.74`였고, 엔진은 목표 기준가가 아니라 현재가 `2322.74`로 `SELL LIMIT` 주문을 제출했다.

## 영향

현재 상태에서 즉시 손실을 만들지는 않는다. 오히려 주문 가격은 목표 기준가보다 높기 때문에 체결되면 목표 기준보다 약간 더 유리한 가격이다.

다만 운영 의미상 문제는 있다.

- `ExitModel.target_price`가 실제 주문 가격의 기준으로 사용되지 않는다.
- 로그의 `target_exit_limit_submitted`가 목표가 주문처럼 보이지만, 실제로는 트리거 시점 현재가 주문이다.
- 가격이 급등 후 되돌아오면, 목표 기준가는 터치했어도 실제 주문 가격이 높아 미체결 상태로 남을 수 있다.
- 목표가 정책이 `DETERMINISTIC_ONLY`라는 문서 규칙과 구현이 약하게 어긋난다.

## 현재 주문 상태

Binance Spot Testnet 조회 기준:

- 주문 ID: `4967475`
- 심볼: `ETHUSDT`
- 방향: `SELL`
- 유형: `LIMIT`
- 상태: `NEW`
- 가격: `2322.74000000`
- 수량: `0.00220000`
- 체결 수량: `0.00000000`
- 작동 여부: `isWorking=true`

계정 잔고상 `0.0022 ETH`가 locked 상태이므로 주문 수량과 일치한다.

## 판단

문제 유형은 런타임 상태 불일치가 아니라 청산 주문 가격 산정 로직의 구현 불일치다. 로컬 상태와 거래소 상태는 일치하지만, 목표 청산 주문의 기준 가격이 `open_trade.target_price` 또는 `exit_signal.target_price`가 아니라 `current price`로 산정되고 있다.

## 권장 조치

코드 수정 시에는 `TARGET` 청산 주문 가격을 `exit_signal.target_price` 기준으로 만들고, `TIME_EXIT` 또는 `PARTIAL`은 각 exit type별 정책을 명시적으로 분리해야 한다.

예상 수정 방향:

- `TARGET`: `exit_signal.target_price`
- `PARTIAL`: `exit_signal.target_price`
- `TIME_EXIT`: 별도 정책 필요. 현재가 지정가를 유지할지, 시장가 보호 흐름과 분리할지 설계 기록 필요

기존 대기 주문 `4967475`를 취소하거나 재제출하는 행위는 거래소 상태 변경이므로 이 보고서에서는 수행하지 않았다.

## 검증 기록

- `data/state.json` 확인 완료
- `logs/runtime.log` 확인 완료
- `src/risk/enhanced_exit_manager.py` 확인 완료
- `src/engine.py` 확인 완료
- Binance Spot Testnet 주문 조회 완료
- Binance Spot Testnet 현재가 조회 완료

관련 문서: [[CNT TRADING STATUS REPORT 20260425 1948 KO]], [[CNT v2 LIVE READINESS GATE KO]], [[AGENTS]]

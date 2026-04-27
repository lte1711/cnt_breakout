---
tags:
  - cnt
  - ko
  - observation
  - runtime-check
  - status/verified
  - type/documentation
  - status/active
  - type/operation
  - strategy/pullback_v1
  - type/analysis
  - type/validation
  - status/completed
---

# CNT Observation Resume Check 20260425 2007 KO

## 요약

`run.ps1` entry chain으로 관찰 사이클을 1회 재개했고, 신규 목표 청산 주문 `4969485`는 아직 미체결 `NEW` 상태로 확인되었다.

## 거래소 주문 상태

- 주문 ID: `4969485`
- 심볼: `ETHUSDT`
- 방향: `SELL`
- 유형: `LIMIT`
- 가격: `2322.08000000`
- 수량: `0.00220000`
- 체결 수량: `0.00000000`
- 상태: `NEW`
- 작동 여부: `isWorking=true`
- 현재가 확인값: `2318.21`

현재 오픈 주문 목록에는 `4969485`가 유지되고 있다.

## 스케줄러 상태

`data/scheduler_heartbeat.json` 기준:

- last_event: `finish`
- last_start_time: `2026-04-25 20:07:28`
- last_finish_time: `2026-04-25 20:07:30`
- exit_code: `0`
- gap_detected: `false`

## 로컬 상태 정합성

`data/state.json` 기준:

- action: `PENDING_CONFIRMED`
- pending_order.orderId: `4969485`
- pending_order.status: `NEW`
- pending_order.side: `SELL`
- pending_order.exit_type: `TARGET`
- open_trade.status: `OPEN`
- open_trade.target_price: `2322.082238`

`logs/runtime.log`에도 `2026-04-25 20:07:28` 기준 `PENDING_CONFIRMED`가 기록되어 있다.

## 보조 회복 상태

`data/auxiliary_recovery_status.json` 기준:

- official_gate.status: `FAIL`
- official_gate.reason: `NON_POSITIVE_EXPECTANCY`
- pullback_v1.closed_trades: `32`
- pullback_v1.expectancy: `0.0017143749999998367`
- pullback_v1.profit_factor: `1.234828800986202`
- recovery_signal.status: `RECOVERY_OBSERVATION_IN_PROGRESS`
- min_sample_required: `50`

## 판단

주문 `4969485`는 아직 체결되지 않았으므로 체결 후 지표 재계산은 발생하지 않았다. `pullback_v1.closed_trades`는 `32`로 유지된다.

현재 목표는 유지된다.

- 코드-상태-거래소 주문 정합성 유지
- `pullback_v1` 50 closed trades까지 관찰 지속

## 검증 기록

- `.\run.ps1`: 완료
- Binance Spot Testnet 주문 재조회: 완료
- `data/state.json`: 확인 완료
- `data/scheduler_heartbeat.json`: 확인 완료
- `data/auxiliary_recovery_status.json`: 확인 완료
- `logs/runtime.log`: 확인 완료
- `data/strategy_metrics.json`: 확인 완료
- `data/live_gate_decision.json`: 확인 완료

관련 문서: [[CNT TARGET EXIT ORDER REPLACEMENT REPORT 20260425 KO]], [[CNT TARGET EXIT PRICE FIX REPORT 20260425 KO]]

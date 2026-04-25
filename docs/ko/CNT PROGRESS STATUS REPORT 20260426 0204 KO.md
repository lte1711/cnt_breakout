---
tags:
  - cnt
  - ko
  - progress-report
  - runtime-check
created: 2026-04-26
status: verified
---

# CNT Progress Status Report 20260426 0204 KO

## 요약

2026-04-26 02:04 KST 기준, 이전 목표 청산 주문 `4969485`는 목표 체결이 아니라 보호 손절 흐름에서 취소되었다. 이후 포지션은 `STOP_MARKET_FILLED`로 종료되었고, 현재는 새 `BUY LIMIT` 주문 `5009404`가 대기 중이다.

## 거래소 상태

현재가:

- `ETHUSDT`: `2308.95`

이전 목표 청산 주문:

- 주문 ID: `4969485`
- 방향: `SELL`
- 가격: `2322.08000000`
- 상태: `CANCELED`
- 체결 수량: `0.00000000`

현재 오픈 주문:

- 주문 ID: `5009404`
- 방향: `BUY`
- 유형: `LIMIT`
- 가격: `2308.90000000`
- 수량: `0.00220000`
- 상태: `NEW`
- 체결 수량: `0.00000000`
- 작동 여부: `isWorking=true`

## 최근 런타임 흐름

주요 로그:

- `2026-04-25 20:03:43`: `SELL_RESUBMITTED`, 기존 목표 청산 주문 교체 완료
- `2026-04-25 20:24:00`: `STOP_MARKET_FILLED`, `pending_exit_canceled_for_protective_override|protective_stop_market_filled`
- `2026-04-25 21:34:00`: 새 `BUY_SUBMITTED`, 주문 `4979496`
- `2026-04-25 21:44:00`: `PROMOTE_TO_OPEN_TRADE`, 주문 `4979496` 체결 후 오픈 트레이드 승격
- `2026-04-26 00:54:00`: `STOP_MARKET_FILLED`, pullback_v1 포지션 손절 종료
- `2026-04-26 02:04:00`: 새 `BUY_SUBMITTED`, 주문 `5009404`

## 로컬 상태

`data/state.json` 기준:

- last_run_time: `2026-04-26 02:04:00`
- action: `BUY_SUBMITTED`
- pending_order.orderId: `5009404`
- pending_order.side: `BUY`
- pending_order.status: `NEW`
- open_trade: `null`
- stop_price: `2305.43665`
- target_price: `2313.05602`

`data/portfolio_state.json` 기준:

- total_exposure: `0.0`
- open_positions: `[]`
- cash_balance: `9995.002731`
- daily_loss_count: `1`
- consecutive_losses: `5`

## 스케줄러 상태

`data/scheduler_heartbeat.json` 기준:

- last_event: `finish`
- last_start_time: `2026-04-26 02:04:00`
- last_finish_time: `2026-04-26 02:04:05`
- exit_code: `0`
- gap_detected: `false`

## 성과 및 회복 상태

`pullback_v1`:

- closed_trades: `34`
- wins: `17`
- losses: `17`
- win_rate: `0.5`
- expectancy: `0.0009405882352939579`
- profit_factor: `1.124679820816594`
- net_pnl: `0.03197999999999457`

공식 게이트:

- status: `FAIL`
- reason: `NON_POSITIVE_EXPECTANCY`
- closed_trades: `37`
- expectancy: `-0.0009355135135136299`
- net_pnl: `-0.03461400000000442`

보조 회복 상태:

- status: `RECOVERY_OBSERVATION_IN_PROGRESS`
- min_sample_required: `50`
- all_recovery_criteria_passed: `false`

## 판단

현재 시스템은 실행 중이며 스케줄러 gap은 없다. 다만 현재 상태는 오픈 포지션이 아니라 `BUY LIMIT` 대기 상태다. `4969485`는 목표 체결되지 않았고 보호 손절 우선 흐름에서 취소되었다.

현재 관찰 목표는 유지된다.

- 코드-상태-거래소 주문 정합성 유지
- `pullback_v1` 50 closed trades까지 관찰 지속
- 현재 주문 `5009404`의 체결 여부 확인

## 검증 기록

- Binance Spot Testnet 주문 조회: 완료
- `data/state.json`: 확인 완료
- `data/scheduler_heartbeat.json`: 확인 완료
- `data/auxiliary_recovery_status.json`: 확인 완료
- `data/portfolio_state.json`: 확인 완료
- `data/strategy_metrics.json`: 확인 완료
- `logs/runtime.log`: 확인 완료

관련 문서: [[CNT TARGET EXIT ORDER REPLACEMENT REPORT 20260425 KO]], [[CNT OBSERVATION RESUME CHECK 20260425 2007 KO]]

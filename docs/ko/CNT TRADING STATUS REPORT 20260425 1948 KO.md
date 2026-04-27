---
tags:
  - cnt
  - ko
  - trading-status
  - testnet
  - status/verified
  - type/documentation
  - status/active
  - type/operation
  - strategy/pullback_v1
  - type/analysis
---

# CNT Trading Status Report 20260425 1948 KO

## 요약

2026-04-25 19:48 KST 기준, CNT는 Binance Spot Testnet `ETHUSDT`에서 단일 오픈 포지션을 보유 중이며, 목표가 청산용 `SELL LIMIT` 주문 1건이 거래소에서 `NEW` 상태로 대기 중이다.

- 심볼: `ETHUSDT`
- 전략: `pullback_v1`
- 로컬 상태: `OPEN_TRADE` 유지, `SELL` pending order 존재
- 거래소 상태: 주문 `4967475`가 `NEW`, `LIMIT`, `SELL`, `GTC`, `isWorking=true`
- 현재 확인 가격: `2320.01`
- 신규 진입 게이트: `FAIL`, 사유 `NON_POSITIVE_EXPECTANCY`

## 확인된 거래 상태

### 오픈 포지션

`data/state.json` 및 `data/portfolio_state.json` 기준:

- 진입 주문 ID: `4956979`
- 진입 가격: `2317.91`
- 진입 수량: `0.0022 ETH`
- 진입 시각: `2026-04-25 17:24:07`
- 포지션 상태: `OPEN`
- 전략명: `pullback_v1`
- 손절 기준가: `2314.4331349999998`
- 목표 기준가: `2322.082238`
- 최고 기록 가격: `2322.74`

### 대기 주문

거래소 조회 기준:

- 주문 ID: `4967475`
- 주문 방향: `SELL`
- 주문 유형: `LIMIT`
- 주문 가격: `2322.74000000`
- 주문 수량: `0.00220000`
- 체결 수량: `0.00000000`
- 누적 체결 금액: `0.00000000`
- 상태: `NEW`
- 작동 여부: `isWorking=true`

이는 로컬 `data/state.json`의 `pending_order.status=NEW`, `side=SELL`, `exit_type=TARGET`와 일치한다.

## 계정 잔고 확인

거래소 계정 조회 기준:

- `ETH`: free `1.0019`, locked `0.0022`, total `1.0041`
- `USDT`: free `9989.926209`, locked `0.0`, total `9989.926209`

`0.0022 ETH`가 locked 상태이므로 현재 대기 중인 `SELL LIMIT` 주문 수량과 일치한다.

## 최근 실행 흐름

`logs/runtime.log` 기준:

- `2026-04-25 17:24:01`: `BUY_FILLED`, 진입 체결 확인
- `2026-04-25 17:34:01`부터 `19:24:00`까지: `HOLD_OPEN_TRADE`, 청산 조건 미충족
- `2026-04-25 19:34:00`: `SELL_SUBMITTED`, `target_exit_limit_submitted`
- `2026-04-25 19:44:01`: `PENDING_CONFIRMED`, 대기 매도 주문 확인

스케줄러 하트비트 기준 마지막 실행은 `2026-04-25 19:44:00` 시작, `19:44:03` 종료, `exit_code=0`이다. `gap_detected=false`로 기록되어 있다.

## 성과 및 게이트 상태

`data/live_gate_decision.json` 기준:

- 상태: `FAIL`
- 사유: `NON_POSITIVE_EXPECTANCY`
- closed trades: `35`
- expectancy: `-0.0003352571428572645`
- net PnL: `-0.011734000000004186`

이는 신규 진입 확장 또는 실전 전환 관점에서 보수적인 상태로 해석해야 한다. 현재 이미 열린 포지션의 목표가 청산 대기와는 별개로, 전략 성과 게이트는 통과하지 못한 상태다.

## 평가

현재 상태는 정상적인 단일 포지션 관리 흐름으로 보인다. 로컬 상태와 거래소 조회가 모두 같은 대기 주문을 가리키며, `ETH` locked 수량도 주문 수량과 일치한다.

주의할 점은 목표 모델 기준가 `2322.082238`보다 실제 제출된 `SELL LIMIT` 가격 `2322.74`가 높다는 점이다. 로그상 제출 사유는 `target_exit_limit_submitted`이며, 주문은 아직 미체결 상태다. 이 차이가 의도된 가격 조정인지 별도 검토 대상이다.

## 검증 결과

- 로컬 상태 파일 확인: 완료
- 포트폴리오 상태 파일 확인: 완료
- 런타임 로그 확인: 완료
- 시그널 로그 확인: 완료
- 스케줄러 하트비트 확인: 완료
- Binance Spot Testnet 주문 조회: 완료
- Binance Spot Testnet 오픈 주문 조회: 완료
- Binance Spot Testnet 계정 잔고 조회: 완료

## 기록

본 보고서는 [[AGENTS]]의 `EXCHANGE_STATE_IS_PRIMARY` 원칙에 따라 거래소 조회를 최종 확인 근거로 삼았다. 관련 운영 문서는 [[CNT v2 TESTNET PERFORMANCE REPORT KO]], [[CNT v2 LIVE READINESS GATE KO]], [[CNT DATA DASHBOARD KO]]를 참조한다.

---
tags:
  - cnt
  - ko
  - operations-report
  - exit
  - status/verified
  - type/documentation
  - status/active
  - type/validation
  - type/operation
  - type/analysis
  - status/completed
---

# CNT Target Exit Order Replacement Report 20260425 KO

## 요약

목표가 청산 주문 가격 전달 오류로 생성된 기존 `SELL LIMIT` 주문을 취소하고, 목표 기준가에 맞춘 새 `SELL LIMIT` 주문을 재제출했다.

## 실행 전 확인

기존 주문 `4967475` 재조회 결과:

- 심볼: `ETHUSDT`
- 방향: `SELL`
- 유형: `LIMIT`
- 상태: `NEW`
- 가격: `2322.74000000`
- 수량: `0.00220000`
- 체결 수량: `0.00000000`
- 작동 여부: `isWorking=true`

따라서 취소 및 재제출 가능한 상태로 판정했다.

## 재제출 기준

오픈 포지션 기준:

- 목표 기준가: `2322.082238`
- 진입 수량: `0.0022`

필터 보정 결과:

- 재제출 가격: `2322.08`
- 재제출 수량: `0.0022`
- notional: `5.108576`
- validation: `PASS`

## 실행 결과

기존 주문:

- 주문 ID: `4967475`
- 최종 상태: `CANCELED`
- 체결 수량: `0.00000000`

신규 주문:

- 주문 ID: `4969485`
- 심볼: `ETHUSDT`
- 방향: `SELL`
- 유형: `LIMIT`
- 상태: `NEW`
- 가격: `2322.08000000`
- 수량: `0.00220000`
- 체결 수량: `0.00000000`
- 작동 여부: `isWorking=true`

현재 거래소 오픈 주문 목록에는 `4969485`만 확인된다.

## 로컬 상태 반영

`data/state.json`의 `pending_order`를 새 주문 기준으로 갱신했다.

- `orderId`: `4969485`
- `status`: `NEW`
- `side`: `SELL`
- `exit_type`: `TARGET`
- `action`: `SELL_RESUBMITTED`

`logs/runtime.log`에 `target_exit_limit_replaced` 기록을 추가했다.

## 검증 결과

- 기존 주문 재조회: 완료
- 기존 주문 취소: 완료
- 취소 상태 확인: 완료
- `/api/v3/order/test` 검증: 완료
- 신규 `SELL LIMIT` 제출: 완료
- 신규 주문 재조회: 완료
- 오픈 주문 목록 확인: 완료
- 로컬 `state.json` 갱신 확인: 완료
- `runtime.log` 기록 확인: 완료

## 기록

관련 수정 보고서: [[CNT TARGET EXIT PRICE FIX REPORT 20260425 KO]]

관련 원인 보고서: [[CNT TARGET EXIT PRICE MISMATCH REPORT 20260425 KO]]

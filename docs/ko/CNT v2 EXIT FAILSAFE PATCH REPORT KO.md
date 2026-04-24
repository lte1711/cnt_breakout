---
tags:
  - cnt
  - docs
  - report
  - v2
aliases:
  - CNT v2 EXIT FAILSAFE PATCH REPORT KO
---

# CNT v2 EXIT FAILSAFE PATCH REPORT KO

```text
DOCUMENT_NAME = cnt_v2_exit_failsafe_patch_report_ko
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-19
STATUS        = PATCH_APPLIED_AND_SYNTHETICALLY_VALIDATED
SCOPE         = TARGET_LIMIT_STUCK_PROTECTION
```

## 1. 이슈

관찰된 runtime behavior:

- target limit에 대해 `SELL_SUBMITTED`
- 반복되는 `PENDING_CONFIRMED`
- stop 이하로 가격이 내려가도 protective exit가 takeover하지 못함

즉 pending target-limit order가 protective stop / trailing exit를 막는 문제가 있었다.

## 2. 패치

적용된 변경:

- `binance_client.py`에 signed cancel support 추가
- `src/order_cancel.py` 추가
- `src/engine.py` 갱신:
  - pending target/time-exit/partial sell order를 override 가능한 limit exit로 감지
  - 그런 pending order가 있는 상태에서 stop 또는 trailing-stop 조건이 오면 먼저 pending exit order cancel 시도
  - cancel 성공 후 즉시 protective market exit logic 실행

## 3. 검증

- 수정 모듈 `py_compile` 통과
- synthetic override test 통과:
  - pending target sell 인식
  - pending order cancel path 실행
  - protective market exit path 실행
  - resulting action = `STOP_MARKET_FILLED`
  - risk metrics가 loss-close로 갱신

## 4. 현재 해석

```text
EXIT_FAILSAFE = PATCHED
LIVE_STATUS   = STILL_NOT_READY
NEXT          = CONTINUE TESTNET OBSERVATION WITH PATCHED EXIT OVERRIDE
```

## 링크

- [[CNT v2 EXIT FAILSAFE OPERATION CHECKLIST KO]]
- [[CNT v2 EXIT FAILSAFE OPERATION REPORT KO]]
- [[00 Docs Index KO]]

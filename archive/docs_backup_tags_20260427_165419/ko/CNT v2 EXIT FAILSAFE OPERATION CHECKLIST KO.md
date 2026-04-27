---
aliases:
  - CNT v2 EXIT FAILSAFE OPERATION CHECKLIST KO
---

# CNT v2 EXIT FAILSAFE OPERATION CHECKLIST KO

```text
DOCUMENT_NAME = cnt_v2_exit_failsafe_operation_checklist_ko
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-19
STATUS        = ACTIVE
PURPOSE       = VERIFY_PROTECTIVE_OVERRIDE_DURING_PENDING_LIMIT_EXIT
```

## 1. 목적

```text
pending LIMIT가 있을 때 STOP/TRAILING 보호 청산이 정상 동작하는지 확인
```

## 2. PASS 조건

모든 항목이 만족되어야 한다.

1. pending 존재

```text
SELL_SUBMITTED -> PENDING_CONFIRMED
```

2. 가격이 stop 이하 구간에 진입
3. cancel 시도 발생

```text
CANCEL request log
```

4. cancel 성공
5. 보호 청산 즉시 실행

```text
STOP_MARKET_FILLED or TRAILING_STOP_FILLED
```

6. 포지션 종료

```text
open_trade=None
```

## 3. FAIL 조건

다음 중 하나라도 발생하면 FAIL:

- stop 구간에 들어갔는데 `PENDING_CONFIRMED`만 반복
- cancel 시도 없음
- cancel 실패 후 protective follow-up 없음
- STOP/TRAILING 대신 `HOLD` 지속

## 4. 결정 규칙

```text
1 PASS  -> 정상 동작으로 보기 시작할 수 있음
3 PASS  -> 운영 검증 완료
1 FAIL  -> 즉시 patch 재검토
```

## 5. 핵심 규칙

```text
pending가 있어도 stop이 먼저 필요하면 보호 청산이 실행되면 PASS
```

## 링크

- CNT v2 EXIT FAILSAFE PATCH REPORT KO
- CNT v2 EXIT FAILSAFE OPERATION REPORT KO
- 00 Docs Index KO

## Obsidian Links

- [[CNT v2 VALIDATION REPORT KO]]



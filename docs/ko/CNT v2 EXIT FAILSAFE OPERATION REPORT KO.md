---
aliases:
  - CNT v2 EXIT FAILSAFE OPERATION REPORT KO
---

# CNT v2 EXIT FAILSAFE OPERATION REPORT KO

```text
DOCUMENT_NAME = cnt_v2_exit_failsafe_operation_report_ko
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-19
STATUS        = OBSERVATION_OPEN
```

## 1. 요약

exit failsafe patch는 적용됐고 synthetic validation도 통과했다.

다음으로 필요한 것은 운영 증거다.

- 실제 `SELL_SUBMITTED -> PENDING_CONFIRMED` 사례
- 가격 반전으로 stop 또는 trailing-stop 구간 진입
- pending exit cancel 시도
- 즉시 protective override

이 보고서는 그 운영 검증 단계를 명시적으로 유지하기 위해 존재한다.

## 2. 현재 상태

```text
PATCH_STATUS        = APPLIED
SYNTHETIC_STATUS    = PASS
OPERATIONAL_STATUS  = NOT_YET_CONFIRMED
LIVE_STATUS         = STILL_NOT_READY
```

## 3. 필요한 운영 증거

runtime evidence에서 다음을 확인해야 한다.

1. `SELL_SUBMITTED`
2. 반복되는 `PENDING_CONFIRMED`
3. stop 또는 trailing trigger 구간 진입
4. pending exit order에 대한 cancel 시도
5. `STOP_MARKET_FILLED` 또는 `TRAILING_STOP_FILLED`
6. `open_trade=None`
7. `risk_metrics` 일관 업데이트

## 4. PASS / FAIL 규칙

```text
1 PASS  = 정상 동작으로 보기 시작 가능
3 PASS  = 운영 검증 완료
1 FAIL  = 즉시 재검토 필요
```

## 5. 현재 결정

```text
EXIT_FAILSAFE_PATCH         = PRESENT
EXIT_FAILSAFE_RUNTIME_PROOF = PENDING
NEXT                        = CONTINUE TESTNET OBSERVATION UNTIL FIRST QUALIFYING CASE
```

## 링크

- CNT v2 EXIT FAILSAFE PATCH REPORT KO
- CNT v2 EXIT FAILSAFE OPERATION CHECKLIST KO
- 00 Docs Index KO

## Obsidian Links

- [[CNT v2 VALIDATION REPORT KO]]



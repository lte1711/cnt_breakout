---
tags:
  - cnt
  - type/documentation
  - status/active
  - context-filter
  - type/validation
  - type/operation
  - risk
  - strategy/pullback_v1
  - strategy/breakout_v3
  - type/analysis
  - cnt-v2-post-operational-patch-validation-report-ko
---

# CNT v2 운영 후속 패치 검증 보고

```text
DOCUMENT_NAME = cnt_v2_post_operational_patch_validation_report_ko
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-19
STATUS        = POST_OPERATIONAL_PATCH_VALIDATED
REFERENCE_1   = CNT v2 POST-OPERATIONAL PATCH WORK INSTRUCTION
REFERENCE_2   = CNT v2 VALIDATION REPORT
```

---

# 1. 요약

이 보고서는 CNT v2 baseline patch 이후 적용된 non-blocking post-operational consistency patch를 검증한다.

검증 대상:

* error signal stale filtering cleanup
* risk metric responsibility consolidation
* portfolio state snapshot metadata
* signal age policy standardization
* runtime routing wording consistency

---

# 2. 검증 결과

## 2.1 Error signal stale pollution

PASS

확인:

* strategy error signal은 이제 `signal_age_limit_sec=-1` 사용
* `entry_gate`는 `signal_age_limit_sec > 0`일 때만 stale check 수행
* strategy error reason은 계속 `strategy_error:*`

## 2.2 Risk metric ownership

PASS

확인:

* `engine.py`만 risk metric reset과 update의 write path로 남음
* `risk_guard.py`는 read-only이며 날짜 normalize나 counter mutation을 하지 않음

## 2.3 Portfolio state snapshot clarity

PASS

확인:

* `PortfolioState`는 이제 아래를 포함
  * `last_update_time`
  * `source`
* `state_manager.build_portfolio_state(...)`는 `source=rebuild_from_runtime` 메타데이터를 기록

## 2.4 Signal age policy

PASS

확인:

* `-1`은 age-check skip
* `>0`은 bounded validity window
* `0`은 strategy parameter validation에서 거부

검증된 전략:

* `breakout_v1`
* `pullback_v1`
* `mean_reversion_v1`

## 2.5 Routing status wording

PASS

확인:

* 코드 상태는 그대로: `order_router`는 준비돼 있지만 runtime execution path에는 연결되지 않음
* 문서도 같은 표현을 사용

---

# 3. 검증 증거

실행된 확인:

* `compileall` success
* import validation success
* synthetic `entry_gate` validation for strategy error signal
* synthetic `risk_guard` non-mutation check
* synthetic portfolio state build/save/load check
* synthetic strategy parameter validation check for `signal_age_limit_sec`

---

# 4. 공식 결론

```text
Error signal stale cleanup: PASS
Risk metric ownership: PASS
Portfolio state metadata: PASS
Signal age policy: PASS
Routing wording consistency: PASS
```

```text
CNT v2 post-operational patch complete
Ready for further performance-oriented improvements
```

## Obsidian Links

- [[CNT v2 POST-OPERATIONAL PATCH WORK INSTRUCTION KO]]



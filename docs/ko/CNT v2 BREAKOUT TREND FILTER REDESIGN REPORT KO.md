---
tags:
  - cnt
  - type/documentation
  - status/active
  - market-context
  - post-logging
  - context-filter
  - type/validation
  - type/operation
  - strategy/pullback_v1
  - strategy/breakout_v3
  - obsidian
  - type/analysis
  - cnt-v2-breakout-trend-filter-redesign-report-ko
---

# CNT v2 BREAKOUT 추세 필터 재설계 보고

```text
DOCUMENT_NAME = cnt_v2_breakout_trend_filter_redesign_report_ko
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-20
STATUS        = CODE_AND_TEST_UPDATED
REFERENCE_1   = CNT v2 BREAKOUT TREND FILTER REDESIGN PLAN
REFERENCE_2   = CNT v2 BREAKOUT TREND FILTER CHANGE REPORT
```

---

# 1. 구현된 변경

`src/strategies/breakout_v1.py`에 구현된 내용:

* 기존 `TREND_UP` pass path는 유지
* `RANGE + trend_bias=UP + entry ema_fast > ema_slow`는 상위 gate 통과 허용
* `TREND_DOWN`는 계속 차단
* 진단을 쉽게 하기 위해 rejection reason을 분리
  * `market_not_trend_up`
  * `range_without_upward_bias`
  * `range_bias_up_but_entry_trend_not_up`

---

# 2. 관측성 변경

런타임 signal logging에도 다음 변경이 적용됐다.

* `trend_bias`가 이제 `signal.log`에 포함됨

이건 engine 실행 순서는 바꾸지 않으면서, post-change 해석 품질을 높여 준다.

---

# 3. 테스트 결과

`tests/test_breakout_trend_filter.py` 테스트 커버리지 업데이트:

* `TREND_UP` upper-gate pass
* `RANGE + UP_BIAS` pass
* `RANGE without UP_BIAS` block
* `RANGE + UP_BIAS but entry trend not up` block
* `TREND_DOWN` block
* lower-gate rejection propagation
  * `volatility_not_high`
  * `rsi_below_entry_threshold`
  * `breakout_not_confirmed`

이 단계의 runtime-safe validation:

* unit / regression tests only
* 실제 운영 cycle 관측은 계속 scheduler를 통해 진행

---

# 4. 초기 해석

이 재설계는 다음처럼 해석해야 한다.

* controlled upper-gate redesign
* ATR / RSI 완화 단계가 아님
* ranker adjustment가 아님
* pullback 전략 변경도 아님

다음 판단은 반드시 post-change runtime evidence에 따라야 한다.

---

# 5. 다음 결정 규칙

Post-change 성공 신호는 다음과 같다.

* lower rejection reason 증가
* breakout candidate path 등장
* breakout selection path 등장

만약 충분한 cycle 이후에도 `market_not_trend_up`가 계속 지배적이면, 다음 리뷰는:

* market regime classification design
* ATR / RSI 완화가 아님

을 다뤄야 한다.

## Obsidian Links

- [[CNT v2 BREAKOUT QUALITY EVALUATION REPORT KO]]



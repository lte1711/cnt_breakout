---
tags:
  - cnt
  - type/documentation
  - status/active
  - market-context
  - context-filter
  - strategy/breakout_v3
  - obsidian
  - type/analysis
  - cnt-v2-breakout-trend-filter-redesign-plan-ko
---

# CNT v2 BREAKOUT 추세 필터 재설계 계획

```text
DOCUMENT_NAME = cnt_v2_breakout_trend_filter_redesign_plan_ko
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-20
STATUS        = IMPLEMENTATION_APPROVED
REFERENCE_1   = CNT v2 BREAKOUT TREND FILTER REVIEW REPORT
REFERENCE_2   = CNT v2 CURRENT STATUS ASSESSMENT
```

---

# 1. 현재 병목

현재 breakout 증거는 다음을 보여준다.

* `signals_generated`는 충분함
* `signals_selected = 0`
* `trades_closed = 0`
* 지배적인 rejection reason은 여전히 `market_not_trend_up`

해석:

* 제한 요인은 상위 market-regime gate
* 현재 단계에서 ATR / RSI는 첫 번째 튜닝 대상이 아님

---

# 2. 재설계 목적

이 재설계의 목표는 즉시 수익 최적화가 아니다.

목표는 최소한 `breakout_v1`가 아래 경로에 들어갈 수 있는지 확인하는 것이다.

* candidate path
* selection path

단, 이 확인은 통제되고 여전히 보수적인 regime gate 아래에서 이뤄져야 한다.

---

# 3. 재설계 규칙

## 허용

* `TREND_UP`
* `RANGE + trend_bias=UP + entry ema_fast > ema_slow`

## 차단

* `TREND_DOWN`
* upward bias가 없는 `RANGE`
* `RANGE + UP_BIAS`지만 entry trend가 up이 아닌 경우

---

# 4. 목표 rejection reason

이번 재설계는 아래 reason들을 분석 가능하게 드러내야 한다.

* `market_not_trend_up`
* `range_without_upward_bias`
* `range_bias_up_but_entry_trend_not_up`
* `volatility_not_high`
* `rsi_below_entry_threshold`
* `breakout_not_confirmed`

---

# 5. 테스트 계획

필수 테스트 커버리지:

1. `TREND_UP`가 상위 gate를 통과
2. `RANGE + trend_bias=UP + ema_fast > ema_slow`가 상위 gate 통과
3. `RANGE + trend_bias!=UP`는 계속 차단
4. `RANGE + trend_bias=UP + ema_fast <= ema_slow`는 계속 차단
5. `TREND_DOWN`는 계속 차단
6. 상위 gate 통과 뒤에도 하위 rejection reason이 실제로 나타남

---

# 6. 관측 계획

배포 후:

* `TESTNET_ONLY` 유지
* 현재 scheduler rhythm 유지
* ATR / RSI는 건드리지 않음
* 최소 `20` post-change breakout cycles 관측
* 더 강한 해석을 위해서는 `30` post-change breakout cycles 권장

## Obsidian Links

- [[CNT v2 BREAKOUT QUALITY EVALUATION REPORT KO]]



---
tags:
  - cnt
  - type/documentation
  - status/active
  - market-context
  - context-filter
  - strategy/breakout_v3
  - type/analysis
  - status/completed
  - cnt-v2-breakout-trend-filter-review-report-ko
---

# CNT v2 BREAKOUT 추세 필터 리뷰 보고

```text
DOCUMENT_NAME = cnt_v2_breakout_trend_filter_review_report_ko
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-20
STATUS        = COMPLETE
REFERENCE_1   = CNT v2 BREAKOUT TREND FILTER REVIEW INSTRUCTION
REFERENCE_2   = CNT v2 BREAKOUT TIMER JUDGMENT REPORT
```

---

# 1. 요약

현재 breakout 병목은 주로 ATR / RSI 부족이 아니다.

실제 런타임 증거는 breakout이 거의 전부 상위 trend-alignment filter에서 막히고 있음을 보여준다.

결론:

* 이 단계는 trend-filter design review로 끝나야 한다
* 다음 engineering action은 controlled trend-filter revision design이어야 한다
* 추가 ATR / RSI 완화는 권장되는 다음 단계가 아니다

---

# 2. 현재 필터 체인

`src/strategies/breakout_v1.py`의 current breakout decision path:

1. entry timeframe indicator sufficiency
2. `market_state != TREND_UP` -> `market_not_trend_up`
3. `volatility_state != HIGH` -> `volatility_not_high`
4. `rsi_value >= rsi_overheat` -> `rsi_overheat`
5. `ema_fast <= ema_slow` -> `ema_fast_not_above_slow`
6. `rsi_value < rsi_threshold` -> `rsi_below_entry_threshold`
7. insufficient lookback -> `not_enough_breakout_lookback`
8. no local breakout above recent highs -> `breakout_not_confirmed`
9. 그 외 -> `entry_allowed=True`

Filter priority 의미:

* `market_not_trend_up`가 indicator sufficiency 이후 절대적인 첫 rejection priority를 가진다
* market-state gate가 실패하면 모든 하위 breakout-specific setup check는 건너뛴다
* 따라서 대부분의 reject cycle에서는 breakout setup quality가 전혀 평가되지 않는다

---

# 3. 추세 / 변동성 정의

현재 `market_state` 구성:

* `ema_gap_ratio < ema_gap_threshold` 이면 `RANGE`
* 아니고 `ema_fast > ema_slow` 이면 `TREND_UP`
* 그 외는 `TREND_DOWN`

현재 `volatility_state` 구성:

* 아래를 만족할 때만 `HIGH`
  * `atr_value >= atr_average * atr_expansion_multiplier`
* 그렇지 않으면
  * `LOW`

해석:

* breakout 전략은 먼저 시장이 이미 trend-up으로 분류되어야 함
* 그 다음에야 volatility qualification으로 내려감
* 그 다음에야 실제 breakout setup structure를 평가함

즉 현재 전략 동작은 사실상:

```text
strict trend-first -> strict volatility-next -> breakout setup last
```

---

# 4. 로그 기반 rejection 증거

최신 확인 snapshot:

* `breakout_v1.signals_generated = 85`
* `breakout_v1.signals_selected = 0`
* `trades_closed = 0`

실험 구간 breakout rejection distribution:

* `market_not_trend_up = 45`
* `volatility_not_high = 6`
* total observed breakout rejections = `51`

Rejection share:

* `market_not_trend_up = 88.24%`
* `volatility_not_high = 11.76%`

해석:

* 지배적인 blocker는 여전히 upper trend alignment
* trend alignment가 간헐적으로 통과한 뒤에야 volatility가 다음 bottleneck으로 보인다
* 따라서 현재 단계에서 ATR / RSI는 최선의 다음 레버가 아니다

---

# 5. 왜 이 단계는 ATR / RSI 리뷰가 아니라 추세 필터 리뷰인가

이유는 구조적이다.

* ATR / RSI 체크는 downstream
* breakout cycle의 압도적 다수는 그 전에 reject된다

따라서:

* ATR / RSI를 더 완화해도 실제 런타임이 거의 도달하지 못하는 로직을 바꾸는 셈이 된다
* 더 강한 근거 기반 다음 단계는 trend qualification layer 자체를 리뷰하는 것이다

---

# 6. 변경 옵션 A

## A. Trend-Filter Relaxation

방향:

* `TREND_UP` 정의를 완화
* 또는 통제된 일부 `RANGE` 상태를 breakout setup evaluation으로 내려보냄

예시 개념:

* positive EMA slope와 local breakout pressure가 있는 `RANGE` 허용
* market-state classification에서 `ema_gap_ratio` threshold 엄격도 완화

예상 효과:

* 더 많은 breakout cycle이 downstream setup check까지 도달
* volatility나 breakout confirmation이 실제 다음 blocker인지 더 잘 보이게 됨

위험:

* false positive 증가
* candidate count 급증 가능
* pullback과 breakout overlap 증가 가능

---

# 7. 변경 옵션 B

## B. Filter-Order Rearrangement

방향:

* trend/volatility gate를 완전히 강제하기 전에 breakout setup presence를 먼저 평가

예시 개념:

* breakout confirmation을 먼저 계산
* breakout structure가 있으면 그 다음 softer trend / volatility qualification 적용

예상 효과:

* engine이 non-ideal trend state 안에서도 setup quality 존재 여부를 학습 가능
* rejection reason이 더 진단적으로 변함

위험:

* 현재의 strict top-down filter보다 직관성이 떨어짐
* signal count 증가가 덜 예측 가능
* ranking interaction을 더 촘촘히 봐야 함

---

# 8. 영향 검토

이 영역의 변경은 아래에 영향을 줄 수 있다.

* false positive rate
* total signal volume
* total candidate volume
* pullback vs breakout candidate collision
* ranker candidate distribution
* testnet에서 관찰되는 downstream rejection reason

향후 변경 후 추적할 새 reason:

* `breakout_not_confirmed`
* `rsi_below_entry_threshold`
* `volatility_not_high`
* breakout이 candidate가 됐지만 pullback에 밀리는 overlap 상황

---

# 9. 권장안

권장 옵션:

```text
RECOMMENDATION = OPTION A
```

이유:

* 데이터는 문제의 핵심이 lower check 순서보다 trend gate의 절대 엄격도에 있음을 보여준다
* option A가 더 설명 가능하고 testnet에서 점진 검증이 쉽다
* option B는 더 침습적이며, option A가 breakout setup behavior를 충분히 드러내지 못할 때 예비안으로 남기는 것이 맞다

권장 다음 단계:

* controlled code change proposal for trend-filter relaxation
* 추가 ATR / RSI 완화가 아님

---

# 10. 최종 판단

```text
TREND_FILTER_REVIEW_REQUIRED = YES
ATR_RSI_SECOND_RELAXATION    = NOT_RECOMMENDED_YET
RECOMMENDED_OPTION           = A
NEXT_STAGE                   = ACTUAL_TREND_FILTER_CHANGE_DESIGN
```

## Obsidian Links

- [[CNT v2 BREAKOUT QUALITY EVALUATION REPORT KO]]



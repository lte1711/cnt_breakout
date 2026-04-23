---
tags:
  - cnt
  - breakout
  - shadow
  - review
  - ko
aliases:
  - CNT v2 BREAKOUT V2 EXPANDED SHADOW OBSERVATION REVIEW KO
---

# CNT v2 BREAKOUT V2 확장 Shadow 관측 리뷰

## 리뷰 상태

- status = `FINALIZED`
- lock_state = `LOCKED`
- breakout_v2 classification = `FAILED_DESIGN_IN_CURRENT_FORM`

## 요약

- current label = `LIVE_READY_WITH_SINGLE_STRATEGY_DEPENDENCE`
- breakout_v2 status = `FAILED_DESIGN_IN_CURRENT_FORM`
- activation decision = `DO NOT ACTIVATE`
- tuning decision = `STILL PROHIBITED`

이 리뷰는 각 이벤트가 아래 필드를 포함하는 최신 expanded shadow schema 표본을 사용한다.

- `secondary_fail_reasons`
- `evaluated_stage_trace`
- `stage_flags`

즉 이 리뷰는 더 이상 first-blocker만 보는 수준이 아니고, 아래 두 관점을 분리한다.

1. first blocker view
2. downstream blocker view

## 기준선

### Mixed Portfolio

- snapshot timestamp = `2026-04-24 01:14:02`
- live gate = `LIVE_READY / ALL_GATES_PASSED`
- closed trades = `33`
- expectancy = `0.0005057575757575136`
- net pnl = `0.016689999999997984`
- profit factor = `1.0584152628686754`

### Strategy Context

- `pullback_v1`는 여전히 유일한 양수 드라이버
  - trades_closed = `30`
  - win_rate = `56.67%`
  - expectancy = `0.002776133333333231`
  - profit_factor = `1.405881292246791`
- `breakout_v1`는 여전히 음수 reference
  - trades_closed = `3`
  - expectancy = `-0.022197999999999656`
  - profit_factor = `0.17295081967214201`

### breakout_v2 Shadow Baseline

- total shadow signals = `180`
- filtered_signal_count = `180`
- allowed_signal_count = `0`
- allowed_signal_ratio = `0.0`
- hypothetical_trades_count = `0`
- expanded schema events = `127`

## First-Blocker View

Expanded-schema first blocker 분포:

- `market_not_trend_up = 53`
- `range_without_upward_bias = 30`
- `volatility_not_high = 21`
- `range_bias_up_but_entry_trend_not_up = 15`
- `breakout_not_confirmed = 3`
- `rsi_overheat = 2`
- `band_width_too_narrow = 1`
- `rsi_below_entry_threshold = 1`
- `price_not_above_vwap = 1`

### 해석

- expanded sample에서는 `market_not_trend_up`가 이제 dominant first blocker다.
- `volatility_not_high`도 여전히 존재하지만, 더 이상 단일 선행 원인으로 볼 수 있을 정도로 강하지 않다.
- 이것은 초기 first-blocker-only review에서 volatility가 더 강하게 보이던 상태와 비교해 의미 있는 변화다.

## Downstream-Blocker View

Expanded-schema secondary fail 분포:

- `band_width_too_narrow = 109`
- `breakout_not_confirmed = 102`
- `volume_not_confirmed = 104`
- `band_not_expanding = 87`
- `rsi_below_entry_threshold = 82`
- `price_not_above_vwap = 65`
- `ema_fast_not_above_slow = 56`
- `volatility_not_high = 54`
- `range_without_upward_bias = 53`
- `vwap_distance_too_small = 45`

Expanded-schema stage false counts:

- `band_width_pass = false` -> `110`
- `vwap_distance_pass = false` -> `111`
- `breakout_confirmed = false` -> `105`
- `volume_pass = false` -> `104`
- `band_expansion_pass = false` -> `87`
- `rsi_threshold_pass = false` -> `85`
- `market_bias_pass = false` -> `83`
- `volatility_pass = false` -> `75`
- `ema_pass = false` -> `71`

### 해석

- 현재 dominant downstream blocker는 `band width`, `VWAP distance`, `breakout confirmation`, `volume`이다.
- `band expansion`과 `RSI threshold`도 구조적으로 높은 실패율을 보인다.
- `volatility_pass = false`도 중요하지만, 이 구조 전체를 설명하기에는 명백히 부족하다.

## Gate Dependency 해석

expanded sample은 초기 first-blocker review보다 더 강한 결론을 뒷받침한다.

- breakout_v2는 단일 threshold 하나에 막히는 전략이 아니다
- breakout_v2는 **multi-stage chain**에 막히는 전략이다

현재 blocking structure를 가장 잘 설명하는 순서는 아래와 같다.

1. market bias가 자주 first fail이 된다
2. market bias가 통과돼도 breakout confirmation이 자주 실패한다
3. 그 다음에도 VWAP distance, volume, band width가 많은 후보를 제거한다

즉 아래는 정당화되지 않는다.

- single-gate relaxation
- volatility-only relaxation
- band-width-only relaxation

## 결정

### 고정 결정

- `breakout_v2 activation = PROHIBITED`
- `threshold tuning = PROHIBITED`
- `single-gate relaxation = PROHIBITED`

### 현재 전략 해석

- `breakout_v2`는 이제 초기 관측 단계를 넘어설 만큼 충분한 shadow evidence를 누적했다
- 충분한 shadow sample 이후에도 `allowed_signal_count = 0`이다
- 따라서 올바른 현재 상태는 다음과 같다.
  - `QUALITY = FAILED_DESIGN_IN_CURRENT_FORM`
  - `USABILITY = NON_VIABLE_CANDIDATE_GENERATION`

## 최종 판정

expanded shadow sample은 `breakout_v2`가 하나의 dominant threshold가 아니라 다단계 filter chain에 의해 막힌다는 점을 보여준다.

가장 정확한 현재 결론:

> `breakout_v2`는 현재 형태에서 실패한 설계이며, 관측된 실패 구조는 market bias, breakout confirmation, VWAP distance, band width, band expansion, volume check가 함께 만든 결과다.

## 다음 단계

다음 안전한 단계는 activation이나 tuning이 아니다.

다음 안전한 단계:

1. `breakout_v2`를 shadow-only 모드로 유지
2. 현재 gate와 runtime policy 보존
3. `breakout_v2`를 inactive experimental strategy로 간주
4. tuning이 아니라 redesign preparation으로 이동

즉:

- no activation
- no threshold relaxation
- no single-gate experiment
- 향후 구현 전에 redesign option 문서화 필요

## 링크

- [[CNT v2 BREAKOUT V2 EXPANDED SHADOW OBSERVATION REVIEW]]
- [[CNT v2 BREAKOUT V2 STATUS RECLASSIFICATION KO]]
- [[CNT v2 BREAKOUT V2 REDESIGN PREPARATION KO]]

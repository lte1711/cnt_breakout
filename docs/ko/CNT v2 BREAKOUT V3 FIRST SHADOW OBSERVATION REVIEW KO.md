---
tags:
  - cnt
  - type/documentation
  - status/active
  - market-context
  - context-filter
  - strategy/breakout_v3
  - status/completed
  - status/final
  - language:-ko
---

# CNT v2 BREAKOUT V3 첫 번째 Shadow Observation Review

## 리뷰 메타데이터

- strategy = `breakout_v3`
- phase = `shadow_observation`
- window_start = `2026-04-24T02:04:04+09:00`
- baseline_commit = `8b6e772`
- review_time = `2026-04-24T12:54:04+09:00`
- status = `completed`

## 요약

- `signal_count = 41`
- `allowed_signal_count = 2`
- `allowed_signal_ratio = 0.04878048780487805`
- `expanded_event_count = 41`

## 최종 판정

`STRUCTURE_IMPROVING`

## 왜 이 판정이 맞는가

이번 결과는 `STILL_OVER_FILTERED`로 보기 어렵다.

현재 shadow window에서는 이미 다음이 확인된다.

- `allowed_signal_count > 0`
- `soft_pass_count >= 3` 반복 발생
- 단순 regime fail만이 아니라 하위 stage까지 실제로 평가가 내려감

반대로 이것이 곧 activation 가능 상태라는 뜻은 아니다.

- `allowed_signal_ratio`는 아직 선호 기준인 `5%`에 약간 못 미친다
- `setup_not_ready`가 아직 최다 blocker다
- allowed 표본 자체는 아직 너무 적다

따라서 현재 해석은 다음이 맞다.

- 구조는 더 이상 dead-on-arrival이 아니다
- 하지만 observation을 더 이어가야 한다

## First Blocker 분포

- `setup_not_ready = 19`
- `market_not_trend_up = 17`
- `breakout_not_confirmed = 3`

해석:

- 50%를 넘는 단일 catastrophic blocker는 없다
- 현재 최다 blocker는 `setup_not_ready`
- regime fail도 여전히 크지만, 단독 지배 상태는 아니다

## Hard / Soft 구조 해석

### Hard blocker

현재 hard blocker 분포는 first blocker 분포와 동일하다.

- `setup_not_ready = 19`
- `market_not_trend_up = 17`
- `breakout_not_confirmed = 3`

### Soft pass 분포

- `0 = 6`
- `1 = 13`
- `2 = 10`
- `3 = 6`
- `4 = 6`

해석:

- 분포가 `0~1`에 완전히 붕괴되어 있지 않다
- `soft_pass_count >= 3`이 `12건` 발생한다
- quality stage 자체가 불가능한 구조는 아니다

## Stage 분석

### Stage pass counts

- `regime = 24`
- `setup = 4`
- `trigger = 11`
- `quality = 12`

### Stage fail counts

- `regime = 17`
- `setup = 37`
- `trigger = 30`
- `quality = 29`

해석:

- regime은 이제 유일한 병목이 아니다
- 현재 최대 병목은 setup stage다
- trigger와 quality도 많은 케이스를 탈락시키지만, 구조적으로 불가능한 단계는 아니다

## Secondary Blocker

- `vwap_distance_fail = 34`
- `band_width_fail = 33`
- `volume_fail = 32`
- `band_expansion_fail = 30`
- `rsi_threshold_fail = 22`
- `ema_fail = 20`

해석:

- secondary fail은 여전히 넓게 분산되어 있다
- 지금 단계에서 soft 조건 하나만 따로 완화하는 것은 맞지 않다
- 현재 증거는 tuning이 아니라 continued observation을 지지한다

## V2 대비 V3 해석

`breakout_v2`와 비교하면 현재 `breakout_v3`는 세 가지 점에서 더 낫다.

1. allowed signal이 실제로 발생한다
2. downstream stage 평가가 실제로 돌아간다
3. `soft_pass_count >= 3`이 반복된다

즉 아직 candidate-ready라고 할 수는 없지만, 구조적 생존성은 분명히 `v3 > v2`다.

## 결정

### Activation

`PROHIBITED`

### Tuning

`PROHIBITED`

### 다음 단계

`continue_observation`

## 운영 결론

이번 첫 observation review는 activation을 지지하지 않는다.

하지만 동시에 `breakout_v3`가 아직도 structurally dead라는 결론도 지지하지 않는다.

따라서 현재 맞는 다음 단계는 다음이다.

- `pullback_v1`만 active runtime으로 유지
- `breakout_v3`는 shadow-only 유지
- 현재 observation window 계속 누적
- 더 큰 표본이 쌓이기 전까지 redesign나 activation 논의를 하지 않음

## Obsidian Links

- [[CNT v2 BREAKOUT V3 SHADOW OBSERVATION WINDOW START KO]]

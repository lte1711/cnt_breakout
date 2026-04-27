---
tags:
  - cnt
  - type/documentation
  - status/active
  - context-filter
  - strategy/breakout_v3
---

---
---

# CNT v2 BREAKOUT V2 VOLATILITY BLOCKED SUBSET REVIEW KO

## 범위

이 문서는 51-event `breakout_v2` shadow dataset에서 `volatility_not_high` first-blocker subset만 분리해 검토한다.

목표:

- volatility-only relaxation이 viable candidate를 만들 수 있는지 확인
- volatility-blocked subset 내부 downstream blocking 측정

## subset 크기

- total shadow signals = `51`
- volatility-blocked subset = `28`

## review limitation

현재 shadow log schema는 다음만 보존한다.

- first blocker reason
- `band_width_ratio`
- `band_expansion_ratio`
- `volume_ratio`

다음 per-event downstream boolean은 보존하지 않는다.

- EMA trend gate
- breakout confirmation gate
- VWAP distance gate

즉 이 subset review는 측정 가능한 shadow field에 대해서만 downstream bottleneck을 직접 확인할 수 있고, 나머지는 보수적으로만 추론 가능하다.

## volatility-blocked set 내부 secondary blockers

### measured post-volatility checks

28개 volatility-blocked event 중:

- `EMA fail count = 직접 관측 불가`
- `breakout confirmation fail count = 직접 관측 불가`
- `band width fail count = 28`
- `band expansion fail count = 19`
- `volume fail count = 20`

### threshold summary

- `band_expansion_ratio >= 1.03` -> `9 / 28`
- `volume_ratio >= 1.5` -> `8 / 28`
- `band_width_ratio >= 0.006` -> `0 / 28`

가장 강한 관찰 결과:

`band width는 28개 전부 threshold 미달`

## conditional pass-through

가정:

- volatility gate만 relax
- 뒤 gate는 그대로 유지

측정된 subset 기준 survivors:

- `band_expansion` 통과 가능: `9`
- `volume` 통과 가능: `8`
- `band_width` 통과 가능: `0`
- 측정된 later threshold 전부 동시 통과: `0`

## 의미

volatility만 완화해도:

- 일부 event는 band expansion은 충분할 수 있고
- 일부 event는 volume도 충분할 수 있지만
- 28개 전부 `band_width_ratio >= 0.006`는 통과하지 못한다

즉 subset은 최종 candidate 이전에 다시 붕괴한다.

## 해석

이 결과는 volatility가 중요하지 않다는 뜻은 아니다.

더 좁게 말하면:

`volatility relaxation alone is insufficient`

이유:

1. volatility는 dominant first blocker다
2. 하지만 그 subset 안에서 `band_width`가 전부를 다시 막는다
3. EMA / breakout confirmation은 아직 non-issue라고 증명되지 않았다

## 최종 결론

`subset still collapses in later filters`

보조 해석:

- volatility는 primary first blocker로 남아 있지만
- volatility-only relaxation으로는 measured survivor가 0이다

## 다음 안전한 분석 후보

즉각적인 config change는 정당화되지 않는다.

가장 안전한 다음 분석 후보:

- `volatility_not_high`와 `band_width_too_narrow`의 관계 검토

실무적으로는:

- volatility gate와 band-width gate가 부분적으로 중복인지 확인
- 향후 설계 검토에서 어느 쪽이 더 지배적인 gate가 되어야 하는지 판단

## 링크

- CNT v2 BREAKOUT V2 FILTER STACK DECOMPOSITION REVIEW KO
- CNT v2 BREAKOUT V2 SHADOW RUNTIME VERIFICATION KO
- CNT v2 BREAKOUT V2 DESIGN KO

## Obsidian Links

- [[CNT v2 BREAKOUT V2 DESIGN KO]]



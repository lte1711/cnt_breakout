---
aliases:
  - CNT v2 BREAKOUT V2 GATE REDUNDANCY REVIEW KO
---

# CNT v2 BREAKOUT V2 게이트 중복성 리뷰

## 범위

이 리뷰는 `breakout_v2`에서 `volatility_not_high` gate와 `band_width_too_narrow` gate의 관계를 평가한다.

목표는 어느 gate를 튜닝하는 것이 아니다.

목표는 두 gate가 아래 중 어느 상태에 가까운지 판단하는 것이다.

- structurally redundant
- structurally dependent
- 또는 더 강한 결론을 내리기엔 아직 증거 부족

## 관측 사실

completed shadow window 기준 고정 사실:

- total shadow signals = `51`
- first blocker `volatility_not_high = 28`
- volatility-blocked subset = `28`
- 그 subset 내부:
  - `band_width_ratio >= 0.006` 발생 `0 / 28`
  - `band_expansion_ratio >= 1.03` 발생 `9 / 28`
  - `volume_ratio >= 1.5` 발생 `8 / 28`
- hypothetical survivors after volatility-only relaxation = `0`

## Overlap 관측

가장 강한 overlap 사실:

- `volatility_not_high`가 `28`개 이벤트를 막음
- 그 `28`개 모두 `band_width_ratio < 0.006`

즉 volatility-blocked subset 안에서는:

- volatility gate를 우회해도 current band-width threshold가 전부를 다시 거절한다

## Same-Market-State 가설

이 패턴은 두 gate가 같은 underlying market condition에 반응하고 있을 가능성을 강하게 시사한다.

- weak volatility regime
- narrow range structure
- insufficient breakout expansion context

하지만 현재 증거는 proof가 아니라 hypothesis 수준이다.

아직 증명되지 않은 이유:

- current shadow schema는 first blocker와 numeric ratio 중심이다
- 모든 gate의 full per-stage boolean trace를 완전히 담고 있지 않다
- 따라서 exact dependency direction은 아직 직접 관측되지 않았다

## Redundancy Candidate 평가

가능한 해석:

1. `volatility_not_high`와 `band_width_too_narrow`는 부분적으로 redundant하다
2. `volatility_not_high`는 coarse upstream regime gate이고, `band_width_too_narrow`는 narrower downstream structure gate다

현재 증거는 두 번째 해석 쪽이 더 강하다.

## Dependency 평가

현재 best-fit 해석:

`volatility_not_high` and `band_width_too_narrow` are dependent but not yet proven redundant

이유:

- reviewed subset에서 두 조건은 강하게 함께 나타난다
- 하지만 개념 계층은 다르다
  - volatility gate = regime filter
  - band width gate = local structure filter
- full per-event stage trace가 없어서 한 gate가 다른 gate 역할을 완전히 대체할 수 있는지는 아직 증명되지 않았다

## Representative Gate 후보

현 단계에서는 어떤 gate도 제거하면 안 된다.

다만 future design review를 위한 대표 후보는 아래와 같다.

- `volatility_not_high` = upstream representative regime gate 후보
- `band_width_too_narrow` = downstream local-structure gate 후보

더 풍부한 shadow schema가 한 gate가 다른 gate 역할까지 흡수할 수 있다고 보여주기 전까지 이 구분은 유지해야 한다.

## 왜 즉시 Threshold Tuning이 금지되는가

즉시 튜닝이 정당화되지 않는 이유:

1. volatility-only relaxation도 measured survivor를 0건으로 남긴다
2. band-width-only relaxation은 아직 검증되지 않았다
3. 두 gate의 dependency 구조가 아직 fully traced되지 않았다
4. downstream EMA와 breakout confirmation 상호작용도 부분적으로만 관측됐다

## 최종 결론

`volatility and band_width are dependent but not yet proven redundant`

## 링크

- CNT v2 BREAKOUT V2 GATE REDUNDANCY REVIEW
- CNT v2 BREAKOUT V2 FILTER STACK DECOMPOSITION REVIEW KO
- CNT v2 BREAKOUT V2 SHADOW SCHEMA EXPANSION IMPLEMENTATION KO

## Obsidian Links

- [[CNT v2 BREAKOUT V2 DESIGN KO]]



---
aliases:
  - CNT v2 BREAKOUT V3 DESIGN DRAFT KO
---

# CNT v2 BREAKOUT V3 설계 초안

## 상태

- status = `DRAFT`
- implementation = `NOT STARTED`
- validation_mode = `SHADOW_ONLY_REQUIRED_BEFORE_ANY_ACTIVATION`

## 목적

`breakout_v3`는 현재 형태의 실패 설계로 판정된 `breakout_v2` 이후에 정의된 구조 재설계 후보이다.

목표는 `breakout_v2`를 미세 조정하는 것이 아니다.

목표는 아래 조건을 동시에 만족하는 breakout 구조를 새로 정의하는 것이다.

1. 실제 후보를 생성할 수 있어야 한다
2. 신호 품질을 유지해야 한다
3. stage별로 설명 가능해야 한다
4. CNT의 기존 validation 체계에 무리 없이 들어가야 한다

## breakout_v2 실패에서 얻은 교훈

`breakout_v2` shadow review에서 확인된 핵심 교훈은 다음과 같다.

- 충분한 shadow 표본에서도 allowed signal이 0건이었다
- first blocker가 하나의 단일 원인으로 안정적으로 고정되지 않았다
- downstream blocker 구조가 강한 다단계 형태였다
- 전략 전체가 과도한 all-gates-pass 구조로 동작했다

대표 실패 패턴:

- market bias 실패
- breakout confirmation 실패
- VWAP distance 실패
- band width 실패
- band expansion 실패
- volume confirmation 실패

즉 다음 설계는 모든 품질 조건을 동시에 AND로 묶는 구조를 피해야 한다.

## 핵심 설계 원칙

`breakout_v3`는 `breakout_v2`를 조정한 연장선이 아니다.

이 설계는 `breakout_v2`의 과도한 all-gates-pass 구조를 대체하기 위한 구조 재설계다.

핵심 원칙은 sequential confirmation이다.

`market regime -> setup formation -> breakout trigger -> entry quality confirmation -> execution decision`

여기서:

- market regime
- breakout confirmation

은 hard requirement로 유지한다.

반면 보조 품질 조건은 strict all-pass 체인이 아니라 soft confirmation group으로 평가한다.

설계 단계에서는 activation이 금지된다.

초기 검증은 반드시 shadow-only여야 한다.

## 설계 원칙 세부

### 1. Sequential Confirmation

시장 조건은 실제 시장에서 형성되는 순서대로 평가해야 한다.

아직 breakout이 구조적으로 형성되지도 않았는데 모든 확인 조건을 같은 시점에 요구해서는 안 된다.

### 2. Hard / Soft 분리

가장 핵심적인 구조 조건만 hard gate로 남긴다.

그 외의 보조 품질 조건은 soft confirmation layer로 묶는다.

### 3. 설명 가능성 우선

모든 실패 후보는 stage 기준으로 설명 가능해야 한다.

즉 아래 가시성을 유지해야 한다.

- first blocker readability
- downstream blocker readability
- shadow-only validation compatibility

### 4. 즉시 scoring-only 구조로 가지 않음

순수 weighted scoring 구조는 첫 단계 채택안이 아니다.

이유:

- validation 가정이 한 번에 너무 많이 바뀐다
- 설명 가능성이 약해진다
- 초기 재설계 검증에서 실패 원인 추적이 어려워진다

## 제안 평가 흐름

## Stage 0 - Market Regime Filter

목적:

- 명백히 불리한 시장 상태를 배제
- 강한 상위 배제 규칙만 유지

예상 체크:

- `market_not_trend_up` 또는 동등한 regime rejection
- `range_without_upward_bias` 또는 동등한 bias rejection

규칙:

- 이 stage는 “이 시장이 breakout 관측 대상으로 구조적으로 적격한가”만 답해야 한다
- 미세 품질 필터를 과도하게 넣지 않는다

## Stage 1 - Setup Formation

목적:

- breakout 준비 구조가 형성되고 있는지 판단

후보 체크:

- minimum volatility floor
- minimum band width
- acceptable price location
- acceptable directional bias continuation

출력:

- `setup_ready = true/false`

중요:

- 이 stage에서는 entry permission을 주지 않는다
- trigger confirmation도 여기서 하지 않는다

## Stage 2 - Trigger Confirmation

목적:

- 실제 breakout trigger가 발생했는지 확인

후보 체크:

- 최근 trigger level 상단에서 breakout confirmed
- trigger 시점에도 구조가 유효함

중요:

- 이 stage는 downstream quality check와 분리되어야 한다
- `breakout_confirmed`는 hard requirement다

## Stage 3 - Entry Quality Confirmation

목적:

- trigger된 breakout이 entry candidate로 볼 만큼 충분한지 평가

후보 체크:

- `volume_pass`
- `vwap_distance_pass`
- `rsi_threshold_pass`
- `ema_pass`
- `band_expansion_pass`
- `band_width_pass`

중요:

- trigger confirmation 이후에 체크한다
- strict all-pass chain으로 구현하지 않는다

## Stage 4 - Execution Decision

목적:

- breakout candidate가 실제 entry consideration으로 넘어갈지를 판단

설계 단계에서는 여전히 shadow-only decision이다.

## 제안 gating 모델

### Hard Gates

반드시 유지되는 조건:

- `market_bias_pass == true`
- `breakout_confirmed == true`

### Soft Confirmation Pool

아래 조건은 pooled quality layer로 이동한다.

- `band_width_pass`
- `band_expansion_pass`
- `volume_pass`
- `vwap_distance_pass`
- `rsi_threshold_pass`
- `ema_pass`

### 초기 초안 규칙

Entry candidate는 아래를 모두 만족할 때만 허용한다.

- 모든 hard gate 통과
- soft confirmation pass count >= `3 of 6`

이 규칙은 설계 초안이며, 승인된 runtime 규칙이 아니다.

## 왜 3 of 6 인가

이유:

- `breakout_v2`는 allowed candidate가 0건이었다
- 지나치게 보수적인 기준은 같은 실패를 반복할 수 있다
- 너무 느슨하면 품질이 빠르게 무너질 수 있다

그래서 `3 of 6`은 production 기준이 아니라 draft validation starting point다.

## 왜 이 방향을 선택했는가

### 채택

- `Sequential Confirmation`
- `Partial Gate Reduction`

### 보류

- `Weighted Scoring`를 핵심 구조로 즉시 채택

이유:

- 현재 CNT는 이미 live runtime과 validation 구조를 가지고 있다
- 첫 재설계 검증에서는 설명 가능하고 비침투적인 방향이 더 적절하다

## 명시적 금지사항

이 단계에서 다음은 금지된다.

- `breakout_v3` 직접 activation
- `breakout_v1` 또는 `breakout_v2`에서 바로 production switch
- `breakout_v2` 현장 튜닝
- single-gate shortcut relaxation
- volatility-only relaxation
- band-width-only relaxation
- 단계 검증 없는 scoring-only rewrite

## Shadow-only validation 계획

구현이 시작되면 `breakout_v3`는 반드시 아래 상태로 시작한다.

- `shadow_only = true`
- `activation = prohibited`

## 링크

- CNT v2 BREAKOUT V3 DESIGN DRAFT
- CNT v2 BREAKOUT V3 SHADOW OBSERVATION WINDOW START KO
- CNT DOCS KOREAN MIRROR POLICY KO

## Obsidian Links

- [[00 Docs Index KO]]



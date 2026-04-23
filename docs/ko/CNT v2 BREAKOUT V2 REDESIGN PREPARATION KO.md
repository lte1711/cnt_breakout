---
tags:
  - cnt
  - breakout
  - redesign
  - plan
  - ko
aliases:
  - CNT v2 BREAKOUT V2 REDESIGN PREPARATION KO
---

# CNT v2 BREAKOUT V2 재설계 준비

## 현재 상태

- `breakout_v2` = `FAILED_DESIGN_IN_CURRENT_FORM`
- runtime mode = `SHADOW_ONLY`
- activation = `PROHIBITED`
- tuning = `PROHIBITED`

이 문서는 implementation instruction이 아니라 redesign-preparation note다.

## 왜 재설계가 필요한가

최신 expanded shadow evidence가 보여주는 것:

- 충분한 shadow sample
- `allowed_signal_count = 0`
- hypothetical trade generation 없음
- 아래 항목에 걸친 multi-stage failure structure
  - market bias
  - breakout confirmation
  - VWAP distance
  - band width
  - band expansion
  - volume

즉 현재 설계는 threshold adjustment 수준이 아니라 구조 재검토가 필요하다.

## 재설계 제약

다음은 계속 고정된다.

- `breakout_v2` activation 금지
- `ACTIVE_STRATEGIES` unchanged
- `risk guard` 변경 금지
- `live gate evaluator` 완화 금지
- `pullback_v1`는 active positive driver 유지
- `breakout_v1`는 negative reference strategy 유지

## 후보 재설계 방향

### Option A: Gate Reduction

hard mandatory condition은 더 작은 집합만 남기고, 나머지는 scoring 또는 confidence shaping으로 이동한다.

가능한 구조:

- hard gate:
  - market bias
  - breakout confirmation
- soft score:
  - VWAP distance
  - band width
  - band expansion
  - volume

### Option B: Sequential Confirmation

설계를 아래 3단계로 분리한다.

1. breakout trigger detection
2. confirmation stage
3. entry permission stage

이 방식은 현재의 all-at-once AND-stack 행동을 줄일 수 있다.

### Option C: Weighted Scoring

strict AND stacking을 weighted quality scoring으로 대체한다.

가능한 구조:

- breakout detected
- 각 확인 요소가 score에 기여
- aggregate score가 threshold를 넘을 때만 entry

## 다음에 일어나면 안 되는 것

아래는 명시적으로 금지된다.

- volatility-only relaxation
- band-width-only relaxation
- partial ad hoc threshold edit
- direct production activation

## 즉시 가능한 다음 설계 산출물

다음 안전한 산출물은 runtime behavior를 바꾸지 않는 redesign option review다.

비교 대상:

- gate reduction
- sequential confirmation
- weighted scoring

## 권장 상태 라벨

저장소와 운영 해석 기준으로 올바른 현재 라벨:

> `breakout_v2 = failed design (inactive experimental strategy)`

## 링크

- [[CNT v2 BREAKOUT V2 REDESIGN PREPARATION]]
- [[CNT v2 BREAKOUT V2 EXPANDED SHADOW OBSERVATION REVIEW KO]]
- [[CNT v2 BREAKOUT V3 DESIGN DRAFT KO]]

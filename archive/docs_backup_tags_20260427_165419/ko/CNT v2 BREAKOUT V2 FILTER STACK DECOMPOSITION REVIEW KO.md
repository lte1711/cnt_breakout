---
aliases:
  - CNT v2 BREAKOUT V2 FILTER STACK DECOMPOSITION REVIEW KO
---

# CNT v2 BREAKOUT V2 필터 스택 분해 리뷰

## 범위

이 리뷰는 완료된 shadow collection window를 기준으로 `breakout_v2` shadow filter stack을 분해한다.

고정 baseline facts:

- total shadow signals = `51`
- allowed signals = `0`
- filtered signals = `51`
- `breakout_v2` actual activation remains prohibited

## 현재 결과

`breakout_v2`는 51-signal shadow window 동안 allowed candidate를 1건도 만들지 못했다.

현재 해석:

- quality는 아직 증명되지 않았다
- usability는 현재 너무 제한적이다
- candidate generation은 계속 차단되어 있다

## Filter Stack 순서

breakout_v2 코드상의 실제 순서:

1. range / upward bias gate
2. volatility gate
3. EMA trend gate
4. RSI threshold gate
5. breakout confirmation gate
6. VWAP distance gate
7. band width gate
8. band expansion gate
9. volume gate

## First Filter Fail 분포

`logs/shadow_breakout_v2.jsonl` 기준 observed first-blocker 분포:

- `volatility_not_high = 28`
- `range_without_upward_bias = 7`
- `ema_fast_not_above_slow = 6`
- `range_bias_up_but_entry_trend_not_up = 5`
- `breakout_not_confirmed = 3`
- `vwap_distance_too_small = 1`
- `band_width_too_narrow = 1`
- `band_not_expanding = 0`
- `volume_not_confirmed = 0`

## 단계별 누적 Pass / Fail

### Stage 1: Range / Upward Bias Gate

- fail count = `12`
  - `range_without_upward_bias = 7`
  - `range_bias_up_but_entry_trend_not_up = 5`
- remaining after stage 1 = `39`

### Stage 2: Volatility Gate

- fail count = `28`
- remaining after stage 2 = `11`

### Stage 3: EMA Trend Gate

- fail count = `6`
- remaining after stage 3 = `5`

### Stage 4: RSI Threshold Gate

- observed first failures = `0`
- remaining after stage 4 = `5`

### Stage 5: Breakout Confirmation Gate

- fail count = `3`
- remaining after stage 5 = `2`

### Stage 6: VWAP Distance Gate

- fail count = `1`
- remaining after stage 6 = `1`

### Stage 7: Band Width Gate

- fail count = `1`
- remaining after stage 7 = `0`

### Stage 8: Band Expansion Gate

- observed first failures = `0`
- remaining after stage 8 = `0`

### Stage 9: Volume Gate

- observed first failures = `0`
- remaining after stage 9 = `0`

## Conditional Analysis

### Volatility Gate를 가정상 우회하면

현재 dominant first blocker는 `volatility_not_high`다.

만약 volatility gate만 우회하고 나머지 조건을 그대로 둔다면:

- raw first-blocker survivors from stage 2 onward = `23`
  - 계산: `51 total - 28 volatility failures = 23`

하지만 이 23은 allowed candidate를 뜻하지 않는다.

이미 non-volatility failure 분포에서 다음이 확인된다.

- `12`는 market/range 구조에서 계속 막힘
- `6`은 EMA trend에서 막힘
- `3`은 breakout confirmation에서 막힘
- `1`은 VWAP distance에서 막힘
- `1`은 band width에서 막힘

따라서 volatility-only relaxation이 viable allowed candidate를 만든다고 증명된 것은 아니다.

### Later-Stage Threshold 증거

shadow event 수치 증거:

- `band_expansion_ratio >= 1.03` 발생 `15`회
- `volume_ratio >= 1.5` 발생 `13`회
- `band_width_ratio >= 0.006` 발생 `1`회

즉:

- band expansion만으로는 부족하다
- volume strength만으로도 부족하다
- band width는 대부분 샘플에서 구조적으로 좁다

### Allowed Signal이 0인 이유

zero-allowed 결과는 하나의 metric만으로 설명되지 않는다.

실제 순서:

1. range/upward bias가 상당한 기반층을 차단
2. volatility가 가장 큰 단일 층을 차단
3. EMA trend가 잔여 샘플을 더 줄임
4. breakout confirmation이 또 줄임
5. 마지막 narrow-band 조건이 남은 경로를 끊음

## Dominant Blocker 식별

주요 first blocker:

- `volatility_not_high`

하지만 이것만으로 volatility가 유일한 structural bottleneck이라고 결론 내릴 수는 없다.

보다 정확한 표현:

`volatility_not_high`는 dominant first blocker이지만, candidate generation 실패는 여러 downstream filter가 함께 만든 결과다.

## Single Or Multi-Blocker 판정

최종 판정:

`multi-stage filtering is jointly blocking candidate generation`

이유:

- 뚜렷한 dominant first blocker는 있다
- 그러나 cumulative pass-through를 보면 결국 0에 도달한다
- later-stage metric은 간헐적 threshold 성공이 있어도 allowed candidate를 만들지 못했다

## Safe Next Adjustment Candidate

즉시 파라미터 변경은 아직 안전하지 않다.

향후 review 대상으로 가장 안전한 후보는:

- **volatility gate를 먼저 검토**

하지만 현재 증거는 아래를 지지하지 않는다.

- immediate volatility-only relaxation
- immediate activation
- immediate parameter tuning

다음 안전한 행동은 mutation이 아니라 analysis다.

## 최종 결론

`breakout_v2 remains too restrictive without a single dominant bottleneck`

보조 설명:

- `volatility_not_high`는 primary first blocker다
- 하지만 candidate generation failure는 여러 downstream gate가 함께 강제하고 있다

## 링크

- CNT v2 BREAKOUT V2 FILTER STACK DECOMPOSITION REVIEW
- CNT v2 BREAKOUT V2 GATE REDUNDANCY REVIEW KO
- CNT v2 BREAKOUT V2 SHADOW SCHEMA EXPANSION PLAN KO

## Obsidian Links

- [[CNT v2 BREAKOUT V2 DESIGN KO]]



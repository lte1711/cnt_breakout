---
---

# CNT v2 BREAKOUT V2 DESIGN KO

## 목적

`breakout_v2`는 현재 `breakout_v1` isolation baseline을 깨지 않기 위해 별도 전략 설계로 도입되었다.

목표는 현재 observation window 중 `breakout_v1`를 바꾸는 것이 아니라, 다음 검증 단계용으로 더 엄격한 breakout 후보를 준비하는 것이다.

## 왜 `breakout_v1`를 그대로 두는가

`breakout_v1`는 현재 isolation observation 대상이다.

지금 `breakout_v1`를 바꾸면:

- isolation baseline이 깨지고
- 현재 degradation 기록 해석이 어려워지며
- `breakout_v1 observed`와 `breakout_v2 candidate`를 깨끗하게 비교할 수 없게 된다

따라서:

- `breakout_v1`는 그대로 유지
- `breakout_v2`는 별도로 추가

## 핵심 차이

### `breakout_v1`

현재 breakout 로직은 주로 다음에 기반한다.

- market classification
- EMA alignment
- RSI threshold
- ATR / high-volatility confirmation
- recent-high breakout

이 구조는 breakout을 감지할 수는 있지만, breakout 품질 전체를 충분히 판단하지는 못한다.

### `breakout_v2`

`breakout_v2`는 breakout 구조를 유지하되 진입 전 품질 필터를 추가한다.

- VWAP direction filter
- VWAP distance filter
- Bollinger band width filter
- Bollinger band expansion filter
- volume confirmation filter

## 새 필터 목록

### 1. VWAP Direction

롱 breakout은:

- `price > vwap`

차단 사유:

- `price_not_above_vwap`

### 2. VWAP Distance

breakout은 VWAP 위로 충분히 떨어져 있어야 한다.

- `vwap_distance_ratio >= min_vwap_distance_ratio`

차단 사유:

- `vwap_distance_too_small`

### 3. Bollinger Band Width

breakout은 최소 밴드 폭이 필요하다.

- `band_width_ratio >= min_band_width_ratio`

차단 사유:

- `band_width_too_narrow`

### 4. Bollinger Band Expansion

현재 밴드 폭은 이전 폭보다 최소 비율 이상 넓어져야 한다.

- `band_width_ratio >= previous_band_width_ratio * min_band_expansion_ratio`

차단 사유:

- `band_not_expanding`

### 5. Volume Confirmation

현재 거래량이 breakout을 확인해야 한다.

- `current_volume >= average_volume * min_volume_multiplier`

차단 사유:

- `volume_not_confirmed`

## 왜 VWAP / Bollinger / Volume이 필요한가

### VWAP

VWAP은 공정 intraday 위치보다 아래이거나 너무 가까운 약한 breakout을 걸러낸다.

### Bollinger Width / Expansion

좁은 밴드, 비확장 구간에서 생기는 false breakout을 줄이는 데 도움을 준다.

### Volume

참여 없는 breakout을 걸러낸다.

## 등록 정책

`breakout_v2`는:

- 구현됨
- 파라미터화됨
- strategy registry에 등록됨

하지만 즉시 활성화되지는 않는다.

이유:

- 현재 isolation runtime을 유지해야 하고
- 현재 `breakout_v1` 기록이 비교 가능해야 하며
- `breakout_v2`는 조용한 교체가 아니라 별도 검증 단계로 들어가야 하기 때문이다

## 활성화 규칙

현재 단계에서:

- `breakout_v2`는 등록만 됨
- `ACTIVE_STRATEGIES`는 그대로 유지

## 링크

- CNT v2 BREAKOUT ISOLATION RUNTIME START KO
- CNT v2 POST-READY DEGRADATION REVIEW KO
- CNT v2 STRATEGY ISOLATION COMPARISON KO

## Obsidian Links

- [[00 Docs Index KO]]



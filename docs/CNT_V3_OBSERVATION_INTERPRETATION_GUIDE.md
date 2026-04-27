---
tags:
  - cnt
  - type/documentation
  - status/active
  - market-context
  - strategy/breakout_v3
  - type/validation
---

# Breakout_v3 Observation 해석 가이드

**목적**: 20~30 이벤트 관찰 구간에서 나타나는 신호를 정확히 읽는 방법  
**적용**: shadow_breakout_v3_snapshot.json 분석 시

---

## Part 1: Regime 게이트 개방 신호 해석

###  Trigger 1 — "market_bias_pass = TRUE" 첫 출현

#### 신호 정의

```json
{
  "market_bias_pass": true,
  "trend_up_pass": false,
  "range_bias_pass": true,
  "first_blocker_distribution": {
    "market_not_trend_up": 12,
    "range_bias_pass": 1
  }
}
```

또는:

```json
{
  "market_bias_pass": true,
  "trend_up_pass": true,
  "range_bias_pass": false,
  "first_blocker_distribution": {
    "market_not_trend_up": 12,
    "trend_up_pass": 1
  }
}
```

#### 해석

| 경우 | 코드 | 의미 |
|------|------|------|
| A | `trend_up_pass=true` | 5m EMA_fast > EMA_slow AND gap >= 0.001 |
| B | `range_bias_pass=true` | 5m (RANGE AND EMA_fast > EMA_slow) |

**둘 중 어느 것이든**: regime gate 해제 

---

###  이 신호의 중요도

```
강도: 매우 높음 (이때부터 v3 진짜 검증 시작)
의미: "시장 최상단 필터 통과"
다음: setup_ready 체크로 진행
```

---

###  추적 방법

#### 현재 상태
```
event [[1-13]]:
  first_blocker_distribution: {
    market_not_trend_up: 13
  }
```

#### 변화 지점 찾기
```
event [[14-30]]:
  "first_blocker_distribution" 변경 여부 추적
  
  target: 
  {
    market_not_trend_up: 12,
    range_bias_pass: 1,
    ...
  }
```

---

###  혼동 주의

####  틀린 해석
> "allowed_signal_count가 0이면 전략이 동작 안 하는 건가?"

####  올바른 해석
> "allowed_signal_count = 0은 regime gate 때문
> regime 풀리는 이벤트가 언제 나타나는가가 핵심
> 그 이벤트가 최종적으로 allowed=1 되는가가 검증"

---

## Part 2: Setup Ready 통과 신호

###  Trigger 2 — "regime PASS 후 setup_ready 상태"

#### 로그에서 확인할 항목

```json
{
  "setup_ready": true,
  "market_bias_pass": true,
  "volatility_floor_pass": true,
  "price_position_pass": true,
  "hard_blocker_distribution": {
    "market_not_trend_up": 13
  }
}
```

#### 해석

regime 풀린 후:

```
AND market_bias_pass = TRUE  ← regime 통과
AND volatility_floor_pass = TRUE  ← HIGH 변동성
AND price_position_pass = TRUE  ← price > VWAP
↓
setup_ready = TRUE  ← 이 조건을 만족하는 이벤트 몇 개?
```

---

###  기대값

```
현재: setup_ready 출현 기회 = 0 (regime 때문)

기대 (regime 풀린 후):
├─ setup_ready = TRUE → 10~30% 
│  (volatility + vwap 조건도 맞아야 함)
└─ setup_ready = FALSE → 70~90%
   (regime은 풀렸지만 나머지 조건 불만족)
```

###  이 단계에서 일어날 수 있는 일

#### 시나리오 1 (긍정적)
```
regime: pass
setup: pass 3/15 events
→ "regime 풀린 후 setup 통과율 꽤 높네"
→ v3 설계가 정상 수준
```

#### 시나리오 2 (중립적)
```
regime: pass 2/20 events
setup: 0/2 (둘 다 fail)
→ "regime 너무 드물거나, setup도 조건 높음"
→ 아직 데이터 부족, 계속 관찰
```

#### 시나리오 3 (경고)
```
regime: pass 5/20 events
setup: 0/5 (모두 fail)
→ "regime은 풀리는데 setup이 항상 실패"
→ volatility_floor_pass 또는 price_position_pass 문제
→ 파라미터 재검토 필요할 수 있음
```

---

## Part 3: Soft Pass Distribution 읽는 법

###  Trigger 3 — "softpass >= 3 달성"

#### 데이터 구조

```json
{
  "soft_pass_count_distribution": {
    "5": 1,
    "4": 2,
    "3": 4,
    "2": 3,
    "1": 2,
    "0": 1
  },
  "secondary_blocker_distribution": {
    "band_width_fail": 3,
    "vwap_distance_fail": 5,
    "rsi_threshold_fail": 4,
    "ema_fail": 2,
    "band_expansion_fail": 6,
    "volume_fail": 3
  },
  "allowed_signal_count": 7
}
```

---

###  읽는 방법

#### Step 1: soft_pass >= 3인 이벤트 계산

```python
soft_pass >= 3:
  "5": 1
  "4": 2
  "3": 4
  --------
  TOTAL = 7 events

soft_pass < 3:
  "2": 3
  "1": 2
  "0": 1
  --------
  TOTAL = 6 events

통과율 = 7 / 13 = 53.8%
```

#### Step 2: secondary blocker 분포 해석

```
6개 quality filter 중 어렵나?

band_expansion_fail: 6 ← 가장 자주 실패 (46%)
  → "밴드 확장 조건이 제한적"
  
rsi_threshold_fail: 4 (31%)
vwap_distance_fail: 5 (38%)
  → "RSI/VWAP이 중간 수준 어려움"

band_width_fail: 3 (23%)
volume_fail: 3 (23%)
ema_fail: 2 (15%)
  → "상대적으로 덜 어려움"
```

---

###  이것이 의미하는 것

#### 해석 1: 설계가 정상인가?

```
allowed_signal_count > 0 AND soft_pass >= 3 (7개)
→ "설계가 의도한 필터링 작동 중 "
```

#### 해석 2: 어느 필터가 가장 엄격한가?

```
band_expansion_fail이 최다 (6개)
→ "새로운 밴드 확장이 드물거나"
→ "min_band_expansion_ratio=1.03이 적절하거나"
→ "또는 시장이 평범한 변동성"
```

#### 해석 3: 전체 품질은?

```
Soft pass >= 3: 53.8%
→ "반 이상이 기본 품질 통과"
→ "5m regime이 자주 나오면 허용율 증가 예상"
```

---

###  기대 수렴값 (최종)

```
이상적 관찰 결과 (30 events 후):

regime 통과: 5~8 events (17~27%)
  └─ setup_ready: 3~5 events (60~75% of regime)
      └─ soft_pass >= 3: 2~3 events (60% of setup)
          → allowed_signal_count = 2~3
          → 최종 통과율 = 2~3 / 30 = 6~10%

이것이 "정상 v3" 예상 동작
```

---

## Part 4: 이상 신호

###  Red Flag: allowed_signal_count가 30 event 이후에도 0

```
시나리오:
  30 events 수집
  첫 market_bias_pass 아직 안 나옴
  
해석:
  Case A: 시장이 진짜 문제 
    → "5m이 진짜 구조적으로 약세"
    → 다른 symbol 시도 고려
  
  Case B: 설정 문제 의심
    → 그때 "파라미터 재검토"
    → 단, 30 event는 너무 적을 수 있음
```

---

###  Red Flag: soft_pass < 3가 70% 이상

```
시나리오:
  regime 통과 이벤트 10개
  그 중 soft_pass >= 3: 2개 (20%)
  
해석:
  Case A: 품질 필터가 과하게 엄격 (가능성 낮음)
  Case B: 시장 조건이 v3 파라미터와 불일치
    → "특정 필터 (e.g. band_expansion) 부분 조정 필요할 수 있음"
    → 단, 아직 데이터 부족 상태에서 결론 금지
```

---

## Part 5: Observation Review 작성 준비

### 자동 계산 template

```markdown
## Shadow Observation Report
**기간**: 2026-04-24 ~ 2026-04-27
**이벤트 수**: 13 → 35 events

### Regime Gate 진행
- Event #13: market_not_trend_up (100%)
- Event #20: **range_bias_pass 첫 출현** ← 주목
- Event #35: first_blocker_distribution 변화

### Setup Ready 진행
- regime pass 이벤트: 8 events (23%)
- setup ready 이벤트: 5 events (62.5% of regime)

### Soft Pass 결과
- soft_pass >= 3: 3 events
- allowed_signal_count: 3
- **최종 허용율: 3 / 35 = 8.6%**

### 검증
 regime gate 정상 작동
 setup filter 정상 작동
 soft_pass threshold 정상 작동
 최종 출력: v3 설계 검증 가능
```

---

## Summary

| 신호 | 찾는 방법 | 의미 |
|------|---------|------|
| Regime open | `first_blocker` 변화 | 시장이 상방 조건 제공 시작 |
| Setup pass | `setup_ready=true` 개수 | regime 풀린 후 실행 가능도 |
| Quality pass | `soft_pass >= 3` 개수 | 최종 거래 신호 품질 |
| Flow check | `allowed_signal_count` | 누적 허용 신호 수 |

---

**다음**: 이 가이드로 Observation Review 작성 시작

## Obsidian Links

- [[00 Docs Index]]

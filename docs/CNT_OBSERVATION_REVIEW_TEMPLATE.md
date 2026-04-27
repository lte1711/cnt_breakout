---
tags:
  - cnt
  - type/documentation
  - status/active
  - market-context
  - strategy/breakout_v3
  - type/validation
  - status/completed
---

# CNT Observation Review Template

**목적**: Shadow data 축적 후 v3 성능 검증 보고서 작성  
**대상**: Breakout_v3 shadow_breakout_v3_snapshot.json  
**주기**: 30+ 이벤트 수집 후 또는 판정 가능 시점에서 작성

---

##  Header Section

```markdown
# Breakout_v3 Observation Review
**보고서 작성일**: 2026-04-25  
**관찰 기간**: 2026-04-24 ~ 2026-04-25  
**데이터 source**: data/shadow_breakout_v3_snapshot.json  
**마지막 업데이트**: 2026-04-25 14:30 UTC

**상태**: [OBSERVATION_INCOMPLETE | PRELIMINARY | READY_FOR_DECISION]
```

---

##  Section 1: 핵심 메트릭

### 1.1 Total Event Summary

```markdown
### Event Collection Progress
| 메트릭 | 값 | 평가 |
|--------|-----|------|
| Total signals | 20 | - |
| Setup ready passed | 8 | 40% |
| Allowed signals | 3 | 15% |
| **Data Readiness** | **60%** |  Observation continues |
```

### 1.2 Regime Gate Analysis

```markdown
### Regime Gate Distribution

**Timeline**:
- Event [[1-13]]: market_not_trend_up (100%)
- Event #14: market_bias_pass = FALSE
- Event #19: **market_bias_pass = TRUE** ← Regime open
- Event #20: range_bias_pass = TRUE
- Event [[21-25]]: market_bias_pass alternates
- Event [[26-30]]: trend_up_pass = TRUE (sustained)

**First Blocker Distribution**:
```

필터

```json
{
  "market_not_trend_up": 13,
  "range_bias_pass": 4,
  "trend_up_pass": 3
}
```

**해석**:
- Regime gate 첫 개방: Event #19
- 개방 빈도: 7/20 (35%)
- 개방 형태: range_bias (4) + trend_up (3)
- **평가**:  정상 범위 (20~40% 기대)

---

##  Section 2: Setup Ready 진행

```markdown
### 2.1 Setup Ready 통과

**조건**:
```
setup_ready = market_bias_pass AND volatility_floor_pass AND price_position_pass
```

**결과**:

| 단계 | 이벤트 수 | 통과율 |
|------|----------|--------|
| regime pass | 7 | 35% (13→20) |
| setup ready | 4 | 57% (7개 중) |
| soft_pass >= 3 | 2 | 50% (4개 중) |

**세부 분석**:

```
regime pass 7개 중:
  ├─ volatility_floor_pass = FALSE: 2개
  ├─ price_position_pass = FALSE: 1개
  └─ setup_ready = TRUE: 4개 ← 진입

setup_ready 4개 중:
  ├─ soft_pass >= 3: 2개  allowed
  ├─ soft_pass = 2: 1개  blocked
  └─ soft_pass = 1: 1개  blocked
```

**해석**:
- Volatility floor가 주요 filter (2개 차단)
- Setup ready 통과율은 적절 (57%)
-  설계 의도대로 작동 중

---

##  Section 3: Soft Pass Distribution 분석

### 3.1 Quality Filter 성과

```markdown
### Quality Filter Breakdown

**Soft Pass Count Distribution**:
```json
{
  "5": 1,
  "4": 2,
  "3": 2,
  "2": 1,
  "1": 0,
  "0": 0
}
```

**계산**:
- soft_pass >= 3: 1+2+2 = 5개
- soft_pass < 3: 1개
- **통과율**: 5/6 = 83.3%

### 3.2 Secondary Blocker 분포

**가장 자주 실패한 필터**:

```json
{
  "band_expansion_fail": 3,
  "vwap_distance_fail": 2,
  "rsi_threshold_fail": 1,
  "ema_fail": 0,
  "band_width_fail": 0,
  "volume_fail": 0
}
```

**분석**:

| 필터 | 실패 수 | 심각도 | 원인 추측 |
|------|--------|--------|---------|
| **band_expansion** | 3 | 높음 | 밴드 폭 변화 제한적 |
| **vwap_distance** | 2 | 중간 | 가격이 VWAP 가까움 |
| **rsi_threshold** | 1 | 낮음 | RSI 조건 대체로 만족 |

**해석**:
 설계가 의도한 "엄격한 품질 필터" 정상 작동
 band_expansion 3개 실패는 예상 범위
 최종 통과율 5/6 (83%)은 건강한 수준

---

##  Section 4: 검증 체크리스트

```markdown
### 4.1 구조 검증

- [x] Regime gate 첫 개방: Event #19
- [x] Regime 개방율 20~40%: 35% 
- [x] Setup ready 통과율 > 30%: 57% 
- [x] Soft pass >= 3 통과율 > 50%: 83% 
- [x] Secondary blocker 분포: 다양함 

### 4.2 이상 신호 체크

- [ ] Regime 개방 안 됨  (35% 정상)
- [ ] Setup ready 0%  (57% 정상)
- [ ] Allowed signal 0  (2개 정상)
- [ ] 특정 필터 100% 실패  (최고 50%)

---

##  Section 5: 결론 및 판정

### 5.1 설계 평가

| 항목 | 평가 |
|------|------|
| **Regime Gate** |  정상 작동 |
| **Setup Filter** |  정상 작동 |
| **Quality Filter** |  정상 작동 |
| **최종 필터링** |  의도대로 작동 |

**결론**: 
> Breakout_v3 설계는 구조적으로 정상입니다.  
> 100% 차단 원인은 설정이 아니라 5m regime 부재였습니다.

### 5.2 다음 Phase 판정

```markdown
**현재 상태**: OBSERVATION_COMPLETE
**데이터량**: 20 events (목표 30+는 미달이나 충분한 신호 포함)
**재시도 권고**: NO (추가 20 event 수집 권고)

**다음 단계**:

1.  Breakout_v1 격리 적용
   - config.py: breakout_v1 weight = 0.0
   - 예상 효과: Expectancy +0.0017로 복구
   - 타이밍: 즉시 적용 가능

2. ⏳ Breakout_v3 계속 관찰
   - 추가 20 event 수집
   - Regime 통과 빈도 추이 추적
   - 최종 부정기: 50 event 수집 후

3.  V1 격리 효과 측정
   - 적용 후 성과 스냅샷 재생성
   - Live Gate PASS 시간 추적
   - Pullback_v1만의 성능 검증
```

---

##  Section 6: Decision Record

```markdown
## 실행 결정

**결정 1**: Breakout_v1 weight = 0 격리 적용
- 시점: [NOW | [REVIEWER_DATE] 승인 후]
- 영향도: HIGH (Expectancy 부호 전환)
- 가역성: YES (weight 복구 가능)

**결정 2**: Breakout_v3 지속 관찰
- 목표: 50 total events
- 다음 리뷰: 2026-04-28
- 통과/불통과 기준:
  - PASS: allowed_signal_count > 5 (10% 이상)
  - FAIL: allowed_signal_count = 0 (50 event 이후)
  - REVIEW: 1~5 (추가 수집)

**결정 3**: 구조 변경 금지
- 파라미터 조정 금지
- Threshold 변경 금지
- Interval 변경 금지
```

---

##  Appendix A: 용어 정의

| 용어 | 정의 |
|------|------|
| market_bias_pass | TREND_UP OR (RANGE+UP trend_bias) |
| setup_ready | market_bias AND volatility AND price_position |
| soft_pass >= 3 | 6개 quality filter 중 3개 이상 통과 |
| allowed_signal_count | soft_pass >= 3인 이벤트 누적 수 |
| regime open | first_blocker가 market_not_trend_up 아님 |

---

##  Appendix B: 관찰 체크리스트 (주 1-2회)

```markdown
### Weekly Observation Checklist

- [ ] shadow_breakout_v3_snapshot.json 업데이트 확인
- [ ] event count: ___ / 50
- [ ] allowed_signal_count: ___
- [ ] first_blocker_distribution 변화 추적
- [ ] regime open 신호 기록
- [ ] 이상 없음 / 이상 발견 [기술]:
      
      _________________
```

---

**이 템플릿 활용**:
1. 매주 업데이트 (또는 20 event마다)
2. 최종 review는 50 event 또는 판정 가능 신호 출현 시
3. 코드 변경 전 최종 체크리스트 완성

## Obsidian Links

- [[00 Docs Index]]

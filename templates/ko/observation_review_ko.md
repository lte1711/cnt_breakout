---
type: observation_review
strategy: breakout_v3
phase: shadow_observation
date: <% tp.date.now("YYYY-MM-DD") %>
review_time: <% tp.date.now("YYYY-MM-DD HH:mm") %>
window_start: ""
baseline_commit: ""
status: in_progress
final_judgement: ""
tags:
  - review/observation
  - strategy/breakout_v3
  - ko
---

# CNT 관측 리뷰 - <% tp.date.now("YYYY-MM-DD") %>

## 0. 리뷰 메타데이터

| 항목 | 값 |
|---|---|
| strategy | breakout_v3 |
| phase | shadow_observation |
| window_start | |
| baseline_commit | |
| review_time | <% tp.date.now("YYYY-MM-DD HH:mm") %> |
| status | in_progress |

---

## 1. 요약

| 항목 | 값 |
|---|---|
| signal_count | |
| allowed_signal_count | |
| allowed_signal_ratio | |
| observation_period | from ____ to <% tp.date.now("YYYY-MM-DD HH:mm") %> |

최종 판정 후보:

- [ ] STILL_OVER_FILTERED
- [ ] FIRST_ALLOWED_DETECTED
- [ ] STRUCTURE_IMPROVING
- [ ] NEEDS_REDESIGN

**FINAL_JUDGEMENT:** `______________`

요약 3줄:

- 
- 
- 

---

## 2. First Blocker 분포

| blocker | count | ratio | 비고 |
|---|---:|---:|---|
| regime_fail | | | |
| setup_fail | | | |
| trigger_fail | | | |
| quality_fail | | | |
| other | | | |

dominant_ratio:

- dominant blocker:
- dominant ratio = (dominant count / total signal_count)

판단 가이드:

- `> 70%` -> 단일 병목 가능성 높음
- `40~70%` -> 혼합 구조
- `< 40%` -> 분산 차단 구조

해석:
> 

---

## 3. Hard vs Soft 구조

### Hard Gate 결과

| gate | fail_count | pass_count | 해석 |
|---|---:|---:|---|
| regime | | | |
| trigger | | | |

### Soft Pass 분포

| soft_pass_count | frequency | ratio |
|---|---:|---:|
| 0 | | |
| 1 | | |
| 2 | | |
| 3 | | |
| 4+ | | |

핵심 해석:

- hard gate가 실제로 통과되는가:
- soft group은 어느 구간에 모이는가:
- `3+`가 실제로 발생하는가:

> 

---

## 4. Stage 실패 분석

| stage | fail_count | dominant_reason |
|---|---:|---|
| regime | | |
| setup | | |
| trigger | | |
| quality | | |

관찰:
> 

---

## 5. V2 vs V3 비교

| 항목 | v2 | v3 |
|---|---|---|
| allowed_signals | 0 | |
| dominant_blocker | volatility / multi-stage confusion | |
| structure | over-constrained | |
| soft_pass_avg | — | |
| overall | FAILED | |

판정:
> 

---

## 6. Allowed Signal Log 요약

| timestamp | soft_pass_count | key_conditions | notes |
|---|---:|---|---|
| | | | |

없다면:

- `No allowed signal observed in this review window`

---

## 7. 핵심 인사이트

- 
- 
- 

---

## 8. 의사결정 기준

### Activation 기준

아래가 모두 충족되기 전에는 activation 금지:

- [ ] allowed_signal_count > 0
- [ ] allowed_signal_ratio >= 5%
- [ ] soft_pass_count `3+`가 반복적으로 관측됨
- [ ] hard gate failure가 지배적이지 않음
- [ ] observation window 안에서 구조 개선이 확인됨

### Tuning 기준

아래일 때만 제한적으로 검토:

- [ ] soft_pass_count가 `2~3` 경계에 집중됨
- [ ] single blocker dominance가 분명함
- [ ] 구조는 맞지만 threshold가 약간 경직된 것으로 보임

---

## 9. 최종 결정

### Activation
- [ ] PROHIBITED
- [ ] CANDIDATE
- [ ] APPROVED

### Tuning
- [ ] PROHIBITED
- [ ] MINOR_ALLOWED
- [ ] FULL

### 다음 단계
- [ ] continue_observation
- [ ] soft_threshold_adjust
- [ ] prepare_redesign
- [ ] activation_review

**최종 결정 한 줄**
> 

---

## 10. Raw Snapshot

```json
```

---

## 11. 링크

* [[CNT v2 BREAKOUT V3 DESIGN DRAFT]]
* [[CNT v2 BREAKOUT V3 SHADOW OBSERVATION WINDOW START]]
* [[CNT v2 BREAKOUT V3 SHADOW RUNTIME ONE-SHOT VERIFICATION]]
* [[breakout_v3 allowed signal log]]
* previous observation review: 실제 이전 리뷰 문서가 생기면 해당 파일명으로 교체

---

분석은 Python에서, 판단 기록은 Obsidian에서 한다.

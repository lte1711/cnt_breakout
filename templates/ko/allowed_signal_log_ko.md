---
type: allowed_signal_log
strategy: breakout_v3
date: <% tp.date.now("YYYY-MM-DD") %>
time: <% tp.date.now("YYYY-MM-DD HH:mm") %>
status: recorded
tags:
  - signal/allowed
  - strategy/breakout_v3
  - ko
---

# Breakout V3 Allowed Signal 기록 - <% tp.date.now("YYYY-MM-DD HH:mm") %>

## 1. 이벤트 요약

| 항목 | 값 |
|---|---|
| strategy_name | breakout_v3_candidate |
| timestamp | |
| allowed | true |
| summary_reason | |
| first_blocker | |
| hard_blocker | |
| soft_pass_count | |
| min_soft_pass_required | 3 |

---

## 2. 핵심 조건

| condition | value |
|---|---|
| market_bias_pass | |
| trend_up_pass | |
| range_bias_pass | |
| setup_ready | |
| breakout_confirmed | |
| trigger_price_pass | |
| band_width_pass | |
| band_expansion_pass | |
| volume_pass | |
| vwap_distance_pass | |
| rsi_threshold_pass | |
| ema_pass | |

---

## 3. Stage Flags

| stage | passed |
|---|---|
| regime | |
| setup | |
| trigger | |
| quality | |

---

## 4. 해석

### 왜 이 신호가 중요했는가

- 
- 

### 이전 blocked 케이스와 무엇이 달랐는가

- 
- 

### 재현 가능성

- [ ] likely_repeatable
- [ ] rare_outlier
- [ ] unclear

---

## 5. Raw Event

```json
```

---

## 6. 의사결정 영향

- [ ] observation only
- [ ] include in next review
- [ ] candidate for activation evidence
- [ ] candidate for threshold analysis

**메모**

>

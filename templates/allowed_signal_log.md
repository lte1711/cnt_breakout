---
type: allowed_signal_log
strategy: breakout_v3
date: <% tp.date.now("YYYY-MM-DD") %>
time: <% tp.date.now("YYYY-MM-DD HH:mm") %>
status: recorded
tags:
  - signal/allowed
  - strategy/breakout_v3
---

# Breakout V3 Allowed Signal Log — <% tp.date.now("YYYY-MM-DD HH:mm") %>

## 1. Event Summary

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

## 2. Key Conditions

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

## 4. Interpretation

### 왜 이 신호가 중요했는가
- 
- 

### 이전 blocked cases와 무엇이 달랐는가
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

## 6. Decision Impact

* [ ] observation only
* [ ] include in next review
* [ ] candidate for activation evidence
* [ ] candidate for threshold analysis

**메모**

>

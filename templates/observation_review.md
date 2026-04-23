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
---

# CNT Observation Review - <% tp.date.now("YYYY-MM-DD") %>

## 0. Review Metadata

| Item | Value |
|---|---|
| strategy | breakout_v3 |
| phase | shadow_observation |
| window_start | |
| baseline_commit | |
| review_time | <% tp.date.now("YYYY-MM-DD HH:mm") %> |
| status | in_progress |

---

## 1. Summary

| Item | Value |
|---|---|
| signal_count | |
| allowed_signal_count | |
| allowed_signal_ratio | |
| observation_period | from ____ to <% tp.date.now("YYYY-MM-DD HH:mm") %> |

Final judgement candidates:

- [ ] STILL_OVER_FILTERED
- [ ] FIRST_ALLOWED_DETECTED
- [ ] STRUCTURE_IMPROVING
- [ ] NEEDS_REDESIGN

**FINAL_JUDGEMENT:** `______________`

Three-line summary:
- 
- 
- 

---

## 2. First Blocker Distribution

| blocker | count | ratio | note |
|---|---:|---:|---|
| regime_fail | | | |
| setup_fail | | | |
| trigger_fail | | | |
| quality_fail | | | |
| other | | | |

dominant_ratio:

- dominant blocker:
- dominant ratio = (dominant count / total signal_count)

Interpretation guide:

- `> 70%` -> single bottleneck likely
- `40~70%` -> mixed structure
- `< 40%` -> diversified blockage

Interpretation:
> 

---

## 3. Hard vs Soft Structure

### Hard Gate Results

| gate | fail_count | pass_count | interpretation |
|---|---:|---:|---|
| regime | | | |
| trigger | | | |

### Soft Pass Distribution

| soft_pass_count | frequency | ratio |
|---|---:|---:|
| 0 | | |
| 1 | | |
| 2 | | |
| 3 | | |
| 4+ | | |

Key interpretation:

- do hard gates pass at all:
- where does the soft group cluster:
- does `3+` actually occur:

> 

---

## 4. Stage Failure Analysis

| stage | fail_count | dominant_reason |
|---|---:|---|
| regime | | |
| setup | | |
| trigger | | |
| quality | | |

Observation:
> 

---

## 5. V2 vs V3 Comparison

| item | v2 | v3 |
|---|---|---|
| allowed_signals | 0 | |
| dominant_blocker | volatility / multi-stage confusion | |
| structure | over-constrained | |
| soft_pass_avg | — | |
| overall | FAILED | |

Judgement:
> 

---

## 6. Allowed Signal Log Summary

| timestamp | soft_pass_count | key_conditions | notes |
|---|---:|---|---|
| | | | |

If none:

- `No allowed signal observed in this review window`

---

## 7. Key Insight

- 
- 
- 

---

## 8. Decision Criteria

### Activation Criteria

Activation remains prohibited until all are true:

- [ ] allowed_signal_count > 0
- [ ] allowed_signal_ratio >= 5%
- [ ] soft_pass_count `3+` is observed repeatedly
- [ ] hard gate failure is not dominant
- [ ] structural improvement is confirmed in the observation window

### Tuning Criteria

Threshold review may be considered only if:

- [ ] soft_pass_count clusters near `2~3`
- [ ] single blocker dominance is clear
- [ ] the structure appears valid but slightly too rigid

---

## 9. Decision

### Activation
- [ ] PROHIBITED
- [ ] CANDIDATE
- [ ] APPROVED

### Tuning
- [ ] PROHIBITED
- [ ] MINOR_ALLOWED
- [ ] FULL

### Next Step
- [ ] continue_observation
- [ ] soft_threshold_adjust
- [ ] prepare_redesign
- [ ] activation_review

**One-line final decision**
> 

---

## 10. Raw Snapshot

```json
```

---

## 11. Links

* [[CNT v2 BREAKOUT V3 DESIGN DRAFT]]
* [[CNT v2 BREAKOUT V3 SHADOW OBSERVATION WINDOW START]]
* [[CNT v2 BREAKOUT V3 SHADOW RUNTIME ONE-SHOT VERIFICATION]]
* [[breakout_v3 allowed signal log]]
* previous observation review: add the actual prior review file here when it exists

---

Analysis is done in Python. Judgement is recorded in Obsidian.

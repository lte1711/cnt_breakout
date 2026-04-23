---
type: activation_review
strategy: breakout_v3
date: <% tp.date.now("YYYY-MM-DD") %>
review_time: <% tp.date.now("YYYY-MM-DD HH:mm") %>
status: draft
tags:
  - review/activation
  - strategy/breakout_v3
  - ko
---

# Breakout V3 Activation Review 체크리스트 - <% tp.date.now("YYYY-MM-DD HH:mm") %>

## 1. 사전 조건

아래가 모두 충족되지 않으면 activation review 자체를 시작하지 않는다.

- [ ] shadow observation window completed
- [ ] one-shot runtime verification passed
- [ ] at least one observation review completed
- [ ] allowed signals observed
- [ ] snapshot consistency confirmed
- [ ] no runtime interference detected

---

## 2. Shadow 성능 증거

| 항목 | 값 |
|---|---|
| total_signal_count | |
| allowed_signal_count | |
| allowed_signal_ratio | |
| soft_pass_avg | |
| dominant_first_blocker | |
| dominant_blocker_ratio | |

판정:

- [ ] evidence_insufficient
- [ ] evidence_mixed
- [ ] evidence_positive

---

## 3. 구조적 타당성

### Hard Gate

- [ ] regime gate not overwhelmingly dominant
- [ ] trigger gate can be passed with non-trivial frequency

### Soft Gate

- [ ] soft_pass_count 3+ occurs repeatedly
- [ ] soft_pass_count distribution not collapsed at 0~1
- [ ] quality stage is not structurally impossible

### Overall

- [ ] v3 is materially better than v2
- [ ] no sign of total over-filtering
- [ ] no single catastrophic blocker dominates

---

## 4. 안전성 검토

- [ ] still shadow-only up to now
- [ ] no unintended effect on live engine behavior
- [ ] no leakage into ACTIVE_STRATEGIES
- [ ] no order path connection
- [ ] no risk manager dependency
- [ ] no order validator dependency

---

## 5. 의사결정 기준

Activation 후보 검토를 하려면 최소 아래를 만족해야 한다.

- [ ] allowed_signal_count > 0
- [ ] allowed_signal_ratio >= 5%
- [ ] repeated 3+ soft-pass cases
- [ ] at least one review concludes structure_improving or better
- [ ] no major runtime safety concern

---

## 6. 최종 권고

- [ ] NO_GO
- [ ] CONDITIONAL_GO
- [ ] GO_TO_NEXT_VALIDATION_STAGE

**결론**
> 

**필요한 후속 조치**

- [ ] continue shadow observation
- [ ] prepare limited simulation
- [ ] activation still prohibited
- [ ] threshold review required
- [ ] redesign required

---

## 7. 연결 증거

- [[CNT v2 BREAKOUT V3 SHADOW OBSERVATION WINDOW START]]
- [[CNT v2 BREAKOUT V3 FIRST SHADOW OBSERVATION REVIEW]]
- [[breakout_v3 allowed signal log]]
- [[CNT v2 BREAKOUT V3 SHADOW RUNTIME ONE-SHOT VERIFICATION]]

---
tags:
  - cnt
  - type/documentation
  - status/active
  - offline-experiment
  - strategy/breakout_v3
  - obsidian
  - type/analysis
  - cnt-v2-priority-decision-report
---

# CNT v2 PRIORITY DECISION REPORT

```text
DOCUMENT_NAME = cnt_v2_priority_decision_report
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-19
STATUS        = DECISION_RECORDED
REFERENCE_1   = CNT v2 ENGINEERING PHASE PLAN
REFERENCE_2   = CNT v2 TEST HARNESS IMPLEMENTATION REPORT
REFERENCE_3   = CNT v2 OBSERVABILITY PRIORITY PLAN
```

---

# 1. EXECUTIVE SUMMARY

The latest engineering-phase interpretation was reviewed and accepted.

The project is now treated as:

```text
AN OPERATING EXPERIMENT SYSTEM WITH TEST BACKSTOP
```

This changes the next-step question from:

* "is the system stable enough to change?"

to:

* "what is the highest-leverage next change?"

---

# 2. DECISION

The next-step priority is:

```text
1. observability
2. breakout experiment
3. state semantic cleanup
4. engine decomposition
```

---

# 3. REASONING

Observability is first because:

* tests now protect baseline behavior
* breakout still lacks selected-trade evidence
* `no_ranked_signal` remains too coarse
* decomposition without better visibility would add refactor cost before diagnosis quality improves

Breakout experiment is second because:

* it is now a controlled experiment, not a blind tuning step
* it should follow richer rejection evidence

Engine decomposition remains important, but is not yet the best immediate leverage move.

---

# 4. CURRENT DECISION

```text
PRIORITY_STATUS = FIXED
NEXT_STEP       = ADD OBSERVABILITY FOR REJECTION AND SELECTION REASONS
```

---

## Obsidian Links

- [[CNT v2 ENGINEERING PHASE PLAN]]


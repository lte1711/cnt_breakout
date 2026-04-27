---
tags:
  - cnt
  - type/documentation
  - status/active
  - type/operation
  - strategy/breakout_v3
  - obsidian
  - type/analysis
  - status/completed
  - cnt-v2-breakout-completion-alert-report
---

# CNT v2 BREAKOUT COMPLETION ALERT REPORT

```text
DOCUMENT_NAME = cnt_v2_breakout_completion_alert_report
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-20
STATUS        = APPLIED
PURPOSE       = notify when breakout post-change observation reaches completion threshold
```

---

# 1. ALERT RULE

Configured completion rule:

```text
TARGET = breakout post-change 30 cycles
ALERT  = trigger once when target is reached
```

Reason:

* `20 cycles` is the earliest meaningful review point
* `30 cycles` is the more stable completion threshold for this observation phase

---

# 2. IMPLEMENTATION

Added:

* `scripts/breakout_completion_alert.ps1`

Runtime outputs:

* `data/breakout_completion_alert.json`
* `logs/breakout_completion_alert.log`

Behavior:

1. count breakout post-change cycles from `logs/signal.log`
2. if cycles are still below threshold, append pending log only
3. if threshold is reached:
   * write completion marker json
   * append completion log
   * attempt OS message with `msg *`

---

# 3. OPERATIONAL ASSUMPTION

This alert treats the current phase as complete at:

```text
POST_CHANGE_BREAKOUT_CYCLES >= 30
```

If a shorter review point is needed later, the threshold can be changed explicitly.

---

## Obsidian Links

- [[CNT v2 BREAKOUT QUALITY EVALUATION REPORT]]


---
tags:
  - cnt
  - docs
  - breakout
  - v1
  - v2
aliases:
  - CNT v2 BREAKOUT V1 RELAXATION CONTINUATION NOTE
---

# CNT v2 BREAKOUT V1 RELAXATION CONTINUATION NOTE

```text
DOCUMENT_NAME = cnt_v2_breakout_v1_relaxation_continuation_note
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-20
STATUS        = ACTIVE
PURPOSE       = document that the current breakout experiment should continue without additional parameter changes yet
```

---

# 1. CURRENT POSITION

The current breakout_v1 first relaxation experiment should continue.

No additional parameter change is justified yet.

---

# 2. REASON

Current facts:

* `breakout_v1` first relaxed values are active
* fresh cycles have been recorded
* breakout still has:
  * `signals_selected = 0`
  * no candidate-path evidence
* latest observed breakout reason remains `market_not_trend_up`

Interpretation:

* the first relaxation has started correctly
* the immediate bottleneck still appears above ATR/RSI thresholds
* more cycles are required before deciding whether the real next move is:
  * keep current thresholds longer
  * relax further
  * or review the trend filter itself

---

# 3. NON-BLOCKING TRACKED ITEMS

The following issues must stay visible in later reports:

1. `selected_strategy_counts` is still `{}` until a fresh selection-path log with `selection_reason=highest_score` appears
2. `scheduler_stdout.log` still has encoding noise and can hit write-collision behavior during overlapping manual runs

These are not blockers for continued observation.

---

# 4. OPERATING RULE

```text
CURRENT_CONFIG = KEEP
CURRENT_MODE   = TESTNET_ONLY
CURRENT_ACTION = ACCUMULATE_MORE_CYCLES
NEXT_DECISION  = 2026-04-20 09:10:34 review point
```

---

## Obsidian Links

- [[00 CNT Vault Home|Vault Home]]
- [[00 Docs Index|Docs Index]]

### Related
- [[00 Docs Index|Docs Index]]

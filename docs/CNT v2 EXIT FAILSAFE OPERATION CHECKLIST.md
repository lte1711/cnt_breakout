---
tags:
  - cnt
  - docs
  - instruction
  - v2
aliases:
  - CNT v2 EXIT FAILSAFE OPERATION CHECKLIST
---

# CNT v2 EXIT FAILSAFE OPERATION CHECKLIST

```text
DOCUMENT_NAME = cnt_v2_exit_failsafe_operation_checklist
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-19
STATUS        = ACTIVE
PURPOSE       = VERIFY_PROTECTIVE_OVERRIDE_DURING_PENDING_LIMIT_EXIT
```

---

# 1. PURPOSE

```text
pending LIMIT 있어도 STOP/TRAILING이 정상 실행되는지 확인
```

---

# 2. PASS CONDITIONS

All items must be satisfied:

1. pending exists

```text
SELL_SUBMITTED -> PENDING_CONFIRMED
```

2. price enters stop-or-below region

3. cancel attempt occurs

```text
CANCEL request log
```

4. cancel succeeds

5. protective exit executes immediately

```text
STOP_MARKET_FILLED or TRAILING_STOP_FILLED
```

6. position closes

```text
open_trade=None
```

---

# 3. FAIL CONDITIONS

Any one of the following is a fail:

```text
- stop region reached while PENDING_CONFIRMED keeps repeating
- no cancel attempt
- cancel failed and no protective follow-up
- HOLD continues instead of STOP/TRAILING response
```

---

# 4. DECISION RULE

```text
1 PASS  -> normal behavior starts to look correct
3 PASS  -> operational validation complete
1 FAIL  -> patch must be reviewed immediately
```

---

# 5. CORE RULE

```text
pending 있어도 stop이 반드시 실행되면 PASS
```

---

## Obsidian Links

- [[00 CNT Vault Home|Vault Home]]
- [[00 Docs Index|Docs Index]]

### Related
- [[00 Docs Index|Docs Index]]

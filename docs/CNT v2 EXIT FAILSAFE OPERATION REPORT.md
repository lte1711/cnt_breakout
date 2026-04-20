# CNT v2 EXIT FAILSAFE OPERATION REPORT

```text
DOCUMENT_NAME = cnt_v2_exit_failsafe_operation_report
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-19
STATUS        = OBSERVATION_OPEN
REFERENCE_1   = CNT v2 EXIT FAILSAFE PATCH REPORT
REFERENCE_2   = CNT v2 EXIT FAILSAFE OPERATION CHECKLIST
```

---

# 1. EXECUTIVE SUMMARY

The exit failsafe patch has been applied and synthetically validated.

The next required evidence is operational:

* a real `SELL_SUBMITTED -> PENDING_CONFIRMED` case
* price reversal into stop or trailing-stop region
* pending exit cancel attempt
* immediate protective override

This report exists to keep that validation stage explicit.

---

# 2. CURRENT STATUS

```text
PATCH_STATUS        = APPLIED
SYNTHETIC_STATUS    = PASS
OPERATIONAL_STATUS  = NOT_YET_CONFIRMED
LIVE_STATUS         = STILL_NOT_READY
```

---

# 3. REQUIRED OPERATIONAL EVIDENCE

The following must be observed in runtime evidence:

1. `SELL_SUBMITTED`
2. repeated `PENDING_CONFIRMED`
3. stop-or-trailing trigger region reached
4. cancel attempt against pending exit order
5. `STOP_MARKET_FILLED` or `TRAILING_STOP_FILLED`
6. `open_trade=None`
7. `risk_metrics` updated consistently

---

# 4. PASS / FAIL RULE

```text
1 PASS  = normal operation looks correct
3 PASS  = exit failsafe operational validation complete
1 FAIL  = immediate review required
```

---

# 5. CURRENT DECISION

```text
EXIT_FAILSAFE_PATCH        = PRESENT
EXIT_FAILSAFE_RUNTIME_PROOF= PENDING
NEXT                       = CONTINUE TESTNET OBSERVATION UNTIL FIRST QUALIFYING CASE
```

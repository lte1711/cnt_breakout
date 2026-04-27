---
tags:
  - cnt
  - type/documentation
  - status/active
  - type/validation
  - obsidian
  - type/analysis
  - cnt-v2-auto-validation-&-decision-system-work-instruction-ko
---

# CNT v2 자동 검증 및 의사결정 시스템 작업 지시

문서 목적:

CNT v2는 testnet 데이터가 계속 누적되는 동안 아래 산출물을 자동 생성한다.

* performance snapshot
* performance report
* live gate decision

문서 상태:

Automation Phase / Mandatory for Scaling

---

# 1. 단계 목표

```text
DATA -> SNAPSHOT -> ANALYSIS -> DECISION
```

---

# 2. 필수 산출물

* `data/performance_snapshot.json`
* `docs/CNT v2 TESTNET PERFORMANCE REPORT.md`
* `data/live_gate_decision.json`

---

# 3. 필수 구성요소

* `src/analytics/performance_snapshot.py`
* `scripts/generate_performance_report.py`
* `src/validation/live_gate_evaluator.py`
* 자동 refresh를 위한 engine hook

---

# 4. 검증 대상

* snapshot 생성
* report 생성
* gate decision 생성
* 데이터가 불충분할 때 보수적 fallback 동작

## Obsidian Links

- [[00 Docs Index KO]]



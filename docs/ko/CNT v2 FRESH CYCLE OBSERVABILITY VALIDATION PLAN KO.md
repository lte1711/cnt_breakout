---
tags:
  - cnt
  - type/documentation
  - status/active
  - type/validation
  - offline-experiment
  - type/operation
  - strategy/breakout_v3
  - obsidian
  - status/completed
  - cnt-v2-fresh-cycle-observability-validation-plan-ko
---

# CNT v2 fresh cycle 관측성 검증 계획

```text
DOCUMENT_NAME = cnt_v2_fresh_cycle_observability_validation_plan_ko
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-20
STATUS        = EXECUTED
PURPOSE       = breakout experiment 전, 새 관측성 필드가 live runtime에 실제 기록되는지 검증
```

---

# 1. 목적

새로 추가한 observability field가 코드에만 구현된 상태가 아니라,
fresh runtime cycle 동안 실제로 기록되고 snapshot layer에도 반영되는지 검증한다.

---

# 2. 시작 사실

검증 전 기준 사실:

* observability aggregation patch 완료
* observability regression test 완료
* 당시 `state.json`에는 active pending order 없음
* 당시 `state.json`에는 active open trade 없음
* 검증 직전 최신 state는 `SELL_FILLED`로 끝난 상태
* `portfolio.log`에는 아직 new-format observability evidence가 저장되지 않았음

---

# 3. 실행 단계

STEP 1

* `run.ps1`를 1~3회의 fresh cycle 동안 실행

STEP 2

* `logs/portfolio.log` 검사
* 최소 아래 중 하나 이상 확인
  * `blocked_detail=...`
  * `candidate_count=...`
  * `rejected_reasons=...`
  * `rank_candidates=...`
  * `selection_reason=highest_score`

STEP 3

* `data/performance_snapshot.json` 검사
* 새 format detail이 parse failure 없이 반영되는지 확인

STEP 4

* PASS면 breakout first relaxation experiment 허용

---

# 4. PASS 규칙

```text
fresh runtime evidence >= 1
snapshot regeneration = normal
test suite = still passing
```

---

# 5. 결과

```text
RESULT = PASS
NEXT   = breakout_v1 first relaxation experiment
```

## Obsidian Links

- [[00 Docs Index KO]]



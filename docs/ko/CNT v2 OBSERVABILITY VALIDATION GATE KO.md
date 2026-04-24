---
aliases:
  - CNT v2 OBSERVABILITY VALIDATION GATE KO
---

# CNT v2 관측성 검증 게이트

```text
DOCUMENT_NAME = cnt_v2_observability_validation_gate_ko
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-20
STATUS        = PASS
PURPOSE       = lock observability interpretation before breakout experiment
LANGUAGE      = KO
SOURCE_DOC    = CNT v2 OBSERVABILITY VALIDATION GATE
```

---

# 1. 결정

Breakout 완화 실험은 조건부로 허용됩니다.

아직 breakout parameter를 즉시 바꾸는 것은 허용되지 않습니다.

필수 순서:

```text
observability implementation
-> observability aggregation correction
-> observability regression tests
-> 1 to 3 fresh cycles with new-format evidence
-> breakout_v1 relaxation experiment
```

---

# 2. 필수 선행조건

Breakout parameter 변경 전에 아래 항목이 완료되어야 합니다.

1. `performance_snapshot.py`가 `selected_strategy_counts`를 selection log 기준으로만 집계해야 함
2. old/new portfolio log 혼합 parsing이 안정적으로 유지되어야 함
3. observability regression test가 통과해야 함
4. fresh runtime evidence에 최소 1개의 new-format log line이 있어야 함

필수 fresh runtime evidence:

* `blocked_detail=...`
* `candidate_count=...`
* `rejected_reasons=...`
* `rank_candidates=...`
* 또는 `selection_reason=highest_score`

---

# 3. 현재 사실

현재 확인된 사실:

* observability code change가 반영되어 있음
* observability test가 통과함
* 이전 pending SELL 상태는 이미 해소됨
* fresh runtime evidence가 확보됨

현재 runtime 사실:

* `data/state.json`의 `pending_order = null`
* `data/state.json`의 `open_trade = null`
* 검증 직전 최신 stored cycle은 `SELL_FILLED`로 종료됨
* fresh validation cycle에서 `logs/portfolio.log`에 새 observability field가 기록됨

의미:

* 이전 blocking 설명은 더 이상 현재 상태가 아님
* STEP 3 fresh runtime proof가 확인됨
* breakout experiment gate가 해제됨

---

# 4. Breakout 실험 규칙

게이트가 해제된 이후에만 첫 breakout 완화 실험을 시작할 수 있습니다.

허용되는 첫 실험 값:

* `atr_expansion_multiplier: 1.2 -> 1.05`
* `rsi_threshold: 55 -> 53`

허용되지 않는 값:

* `atr_expansion_multiplier = 1.0`

이유:

* 현재 전략 검증 규칙은 `atr_expansion_multiplier > 1.0`를 요구함

---

# 5. PASS / 결과

```text
STEP 1 = PASS when selection counting and blocked-detail parsing are corrected
STEP 2 = PASS when regression tests pass
STEP 3 = PASS when fresh runtime evidence is captured
CURRENT_RESULT = STEP 1 PASS / STEP 2 PASS / STEP 3 PASS
BREAKOUT_EXPERIMENT = ALLOWED
```

---

## Obsidian Links

- [[CNT v2 OBSERVABILITY PRIORITY PLAN KO]]



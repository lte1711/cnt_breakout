---
aliases:
  - CNT v2 OBSERVABILITY PRIORITY PLAN KO
---

# CNT v2 관측성 우선순위 계획

```text
DOCUMENT_NAME = cnt_v2_observability_priority_plan_ko
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-19
STATUS        = APPROVED_NEXT_STEP
ROLE          = PRIORITY_GUIDANCE
LANGUAGE      = KO
SOURCE_DOC    = CNT v2 OBSERVABILITY PRIORITY PLAN
```

---

# 1. 현재 해석

프로젝트는 이제 초기 계획 단계와는 다른 상태에 있습니다.

현재 의미는 다음과 같습니다.

* baseline 동작은 테스트로 고정되어 있음
* runtime 증거가 계속 누적되고 있음
* 다음 제약은 더 이상 "실행 가능한가?"가 아님
* 다음 제약은 "전략이 왜 거절되거나 선택되지 않는가?"임

---

# 2. 우선순위 결정

확정된 우선순위는 아래와 같습니다.

```text
PRIORITY_1 = OBSERVABILITY
PRIORITY_2 = BREAKOUT ACTIVATION EXPERIMENT
PRIORITY_3 = STATE STATUS SEMANTIC CLEANUP
PRIORITY_4 = ENGINE DECOMPOSITION
```

`OBSERVABILITY`가 1순위인 이유:

* breakout 신호는 현재 생성되지만 선택되지 않음
* `no_ranked_signal`만으로는 진단 정보가 너무 거침
* 관측성 보강 전에 decomposition을 하면 진단이 더 어려워짐

---

# 3. 필요한 관측성 추가 항목

다음 구현 단계는 최소 아래 정보를 포착해야 합니다.

1. 전략 단위 거절 이유
2. ranker 후보 입력과 score 구성요소
3. 최종 선택 이유와 후보 개수
4. `no_ranked_signal` 하위 분류:
   * `no_candidate`
   * `all_filtered`

---

# 4. 이것이 가능하게 하는 것

관측성 계층이 추가되면 프로젝트는 아래 질문에 답할 수 있게 됩니다.

* `breakout_v1`이 실제로 약한 전략인지, 아니면 과도한 필터링 때문인지
* 병목이 ranking 단계인지 signal generation 단계인지
* 선택 부족이 policy block 때문인지, 전략 진입 거절 때문인지

---

# 5. 현재 결정

```text
NEXT_IMPLEMENTATION = OBSERVABILITY_LAYER
BREAKOUT_TUNING     = DEFER_UNTIL_MORE_VISIBILITY_EXISTS
ENGINE_SPLIT        = DEFER_UNTIL_MORE_VISIBILITY_EXISTS
```

---

## Obsidian Links

- [[00 Docs Index KO]]



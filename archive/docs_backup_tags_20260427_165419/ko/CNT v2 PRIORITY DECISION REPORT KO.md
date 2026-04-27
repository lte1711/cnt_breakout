---
aliases:
  - CNT v2 PRIORITY DECISION REPORT KO
---

# CNT v2 PRIORITY DECISION REPORT KO

```text
DOCUMENT_NAME = cnt_v2_priority_decision_report_ko
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-19
STATUS        = DECISION_RECORDED
```

## 1. 요약

최신 엔지니어링 단계 해석을 검토하고 채택한 결과, 프로젝트는 다음과 같이 규정됐다.

```text
AN OPERATING EXPERIMENT SYSTEM WITH TEST BACKSTOP
```

즉 다음 질문은 더 이상 "시스템이 바뀔 만큼 안정적인가?"가 아니라, "가장 레버리지가 큰 다음 변경은 무엇인가?"가 된다.

## 2. 결정

다음 단계 우선순위:

```text
1. observability
2. breakout experiment
3. state semantic cleanup
4. engine decomposition
```

## 3. 이유

- 테스트가 baseline 동작을 보호하기 시작했다
- breakout은 아직 selected-trade 증거가 부족하다
- `no_ranked_signal`은 너무 거친 관측 값이다
- 더 나은 가시성 없이 decomposition부터 하면 진단 품질보다 리팩터 비용이 먼저 커진다

## 4. 현재 결정

```text
PRIORITY_STATUS = FIXED
NEXT_STEP       = ADD OBSERVABILITY FOR REJECTION AND SELECTION REASONS
```

## 링크

- CNT v2 ENGINEERING PHASE PLAN KO
- CNT v2 OBSERVABILITY PRIORITY PLAN KO
- 00 Docs Index KO

## Obsidian Links

- [[00 Docs Index KO]]



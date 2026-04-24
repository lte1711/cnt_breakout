---
aliases:
  - CNT v2 ENGINEERING PHASE PLAN KO
---

# CNT v2 ENGINEERING PHASE PLAN KO

```text
DOCUMENT_NAME = cnt_v2_engineering_phase_plan_ko
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-19
STATUS        = ACTIVE_ENGINEERING_SEQUENCE
ROLE          = ENGINEERING_PHASE_GUIDANCE
```

## 1. 문맥

Unicode 파일명 정리는 의미 있는 안정화 단계로 간주한다.

실무적 해석:

- 환경/경로 리스크가 낮아졌다
- 프로젝트는 이제 구조 정의 단계에서 엔지니어링 단계로 넘어갈 수 있다

현재 높은 우선순위 리스크:

1. 전략 검증 표본 부족
2. 세분화된 관측성 부족
3. 비대해진 `src/engine.py`

## 2. 저장된 우선순위

```text
1. tests
2. observability
3. breakout experiment
4. status semantic cleanup
5. engine decomposition
```

권장 경로:

```text
SAFE_PATH = TESTS -> OBSERVATION -> EXPERIMENT -> REFACTOR
```

## 3. 즉시 단계

첫 완료 단계:

```text
TEST HARNESS ADDITION
```

최소 기대 파일:

- `tests/test_signal_ranker.py`
- `tests/test_live_gate.py`
- `tests/test_exit_manager.py`
- `tests/test_engine_cycle_smoke.py`

목적:

- 현재 동작 freeze
- 리팩터 회귀 위험 감소
- 엔진 분해를 더 안전하게 만들기

## 4. 테스트 이후 후속 순서

- richer rejection observability 추가
- testnet 전용 `breakout_v1` 제어 실험 수행
- 엔진 분해 설계 기준으로 extraction 시작

```text
NEXT_1 = OBSERVABILITY
NEXT_2 = BREAKOUT_EXPERIMENT
NEXT_3 = STATUS_SEMANTIC_CLEANUP
NEXT_4 = ENGINE_DECOMPOSITION
```

## 5. 현재 결정

```text
ENGINEERING_PHASE = STARTED
CURRENT_STEP      = OBSERVABILITY
REFACTOR          = DEFERRED_UNTIL_BASELINE_IS_TESTED
```

## 링크

- CNT v2 PRIORITY DECISION REPORT KO
- CNT v2 OBSERVABILITY PRIORITY PLAN KO
- 00 Docs Index KO

## Obsidian Links

- [[CNT v2 VALIDATION REPORT KO]]



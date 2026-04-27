---
tags:
  - cnt
  - type/documentation
  - status/active
  - market-context
  - type/operation
  - strategy/pullback_v1
  - strategy/breakout_v3
  - type/analysis
  - type/validation
  - cnt-v2-breakout-v3-shadow-evaluator-implementation-report-ko
---

# CNT v2 BREAKOUT V3 SHADOW EVALUATOR 구현 보고서

## 범위

이 단계는 runtime 실행 동작을 바꾸지 않고 `breakout_v3` shadow evaluation 코드 골격만 구현한다.

## 프로젝트 비교

제안 설계는 현재 CNT 구조와 대조해 반영됐다.

현재 CNT 구조의 현실:

- `src/models/`는 dataclass 중심 구조다
- `src/strategies/`는 breakout helper와 market classification 재사용 구조를 이미 포함한다
- `src/shadow_eval.py`는 현재 `breakout_v2` shadow evaluation을 flat module 형태로 담고 있다
- `ACTIVE_STRATEGIES`와 runtime order flow는 그대로 유지되어야 한다

구현 결정:

- `breakout_v3`를 `ACTIVE_STRATEGIES`에 넣지 않음
- engine execution에 연결하지 않음
- active runtime strategy로 등록하지 않음
- 재사용 가능한 shadow-evaluation primitive만 구현

## 구현 파일

- `src/models/breakout_v3_eval_result.py`
- `src/strategies/breakout_v3.py`
- `src/shadow/breakout_v3_shadow_eval.py`
- `tests/test_breakout_v3_shadow_eval.py`
- `tests/test_breakout_v3_shadow_aggregator.py`

업데이트:

- `config.py`

## 실제 구현 내용

### 데이터 모델

아래 dataclass를 추가했다.

- `BreakoutV3Conditions`
- `StageResult`
- `BreakoutV3EvalResult`
- `BreakoutV3ShadowEvent`

### Strategy Layer

`build_breakout_v3_conditions(...)`를 추가해 raw condition flag만 계산하도록 했다.

이 layer는:

- 주문 제출을 하지 않는다
- live state를 만들지 않는다
- `StrategySignal`을 반환하지 않는다

### Evaluator Layer

`evaluate_breakout_v3_shadow(...)`를 추가했고, 다음을 포함한다.

- stage-by-stage hard/soft evaluation
- first blocker ordering
- hard blocker extraction
- soft pass counting
- structured summary reason

### Aggregation Layer

`aggregate_breakout_v3_shadow_events(...)`를 추가했고, 다음 집계를 제공한다.

- allowed ratio
- blocker distributions
- stage pass/fail counts
- soft pass count distribution

## 명시적으로 구현하지 않은 것

- engine hook 없음
- `breakout_v3`용 shadow jsonl writer 없음
- `breakout_v3`용 snapshot file writer 없음
- registry activation 없음
- runtime trade execution path 없음

이것들은 이 단계를 안전하고 구조적으로 고립시키기 위해 의도적으로 뒤로 미뤘다.

## 검증 결과

검증 대상:

- evaluator behavior
- blocker ordering
- soft threshold behavior
- aggregation behavior

이 단계는 다음 검증을 통과해야 한다.

- evaluator 단위 테스트
- aggregator 단위 테스트
- compile check

## 안전성 선언

이번 구현은 현재 시스템 안전성을 유지한다.

- `pullback_v1`는 live positive driver 상태 유지
- `breakout_v1`는 active reference breakout strategy 상태 유지
- `breakout_v2`는 shadow-only 유지
- `breakout_v3`는 implementation scaffolding only 상태

## 결론

`breakout_v3` shadow evaluator scaffolding은 현재 CNT 프로젝트 구조에 맞게 구현되었다.

현재 상태:

- design -> fixed
- evaluator skeleton -> implemented
- runtime integration -> not started
- activation -> prohibited

## 링크

- CNT v2 BREAKOUT V3 SHADOW EVALUATOR IMPLEMENTATION REPORT
- CNT v2 BREAKOUT V3 DESIGN DRAFT KO
- CNT v2 BREAKOUT V3 SHADOW VALIDATION RUNTIME INTEGRATION PLAN KO

## Obsidian Links

- [[CNT v2 BREAKOUT V3 DESIGN DRAFT KO]]



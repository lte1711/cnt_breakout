---
tags:
  - cnt
  - type/documentation
  - status/active
  - market-context
  - risk
  - strategy/pullback_v1
  - strategy/breakout_v3
  - cnt-v2-implementation-work-instruction-ko
---

# CNT v2 구현 작업 지시서

```text
DOCUMENT_NAME = cnt_v2_implementation_work_instruction_ko
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-19
STATUS        = READY_FOR_IMPLEMENTATION
BASELINE      = CNT v1.1 (CLOSED)
REFERENCE     = cnt_v2_architecture_design
```

## 1. 목적

이 문서는 CNT v2를 단계적으로 구현하기 위한 **작업 단위(Task)와 순서**를 정의한다.

핵심 원칙:

```text
v1.1 코어는 직접 수정하지 않는다.
모든 기능은 상위 레이어로 추가한다.
```

## 2. 구현 전략

### 2.1 단계별 확장 방식

```text
Phase 1 = multi-strategy + signal ranking
Phase 2 = portfolio risk + state extension
Phase 3 = futures adapter
Phase 4 = 분석/고도화
```

## 3. PHASE 1 - Multi Strategy Core

### T1. strategy_registry 확장

목적:

- 여러 전략 등록

작업:

- `breakout_v1`
- `pullback_v1`
- `mean_reversion_v1`

추가 산출물:

- `pullback_v1.py`
- `mean_reversion_v1.py`

### T2. multi-strategy 실행 지원

목적:

- 하나의 symbol에 대해 여러 전략 실행

핵심:

- 기존 `generate_strategy_signal()`은 유지
- `generate_all_signals()` 같은 신규 함수 추가

### T3. signal_ranker 추가

파일:

- `src/portfolio/signal_ranker.py`

목적:

- 여러 신호 중 최종 선택

기본 규칙:

- `entry_allowed`가 true인 신호 중
- confidence가 가장 높은 신호 선택

### T4. strategy_orchestrator 추가

파일:

- `src/portfolio/strategy_orchestrator.py`

역할:

```text
symbol -> 모든 전략 실행 -> ranking -> selected signal 반환
```

### T5. engine에 orchestrator 연결

기존:

```text
engine -> strategy_manager -> single signal
```

변경:

```text
engine -> strategy_orchestrator -> selected signal
```

### T6. config 확장

예시:

```python
ACTIVE_STRATEGIES = [
    "breakout_v1",
    "pullback_v1"
]
```

## 4. PHASE 2 - Portfolio Layer

### T7. PositionState 모델 추가

파일:

- `src/models/position_state.py`

핵심 필드:

- `position_id`
- `symbol`
- `market_type`
- `strategy_name`
- `entry_price`
- `entry_qty`
- `entry_time`
- `stop_price`
- `target_price`
- `status`

### T8. PortfolioState 모델 추가

파일:

- `src/models/portfolio_state.py`

핵심 필드:

- `schema_version`
- `total_exposure`
- `open_positions`

### T9. state_manager 추가

파일:

- `src/state/state_manager.py`

역할:

- portfolio_state load/save
- position list 관리

### T10. portfolio_risk_manager 추가

파일:

- `src/risk/portfolio_risk_manager.py`

역할:

- portfolio-level risk check

## 최종 의미

이 지시서는 CNT v2를 기존 v1.1 baseline 위에 상위 레이어 방식으로 올리는 구현 순서 문서다.

## 링크

- CNT v2 IMPLEMENTATION WORK INSTRUCTION
- CNT v2 VALIDATION CHECKLIST KO
- CNT v2 NEXT PHASE PLAN KO

## Obsidian Links

- [[CNT v2 VALIDATION REPORT KO]]



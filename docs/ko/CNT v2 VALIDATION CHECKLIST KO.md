---
tags:
  - cnt
  - docs
  - validation
  - checklist
  - v2
  - ko
aliases:
  - CNT v2 VALIDATION CHECKLIST KO
---

# CNT v2 검증 체크리스트

```text
DOCUMENT_NAME = cnt_v2_validation_checklist_ko
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-19
STATUS        = VALIDATION_READY
BASELINE      = CNT v1.1 (CLOSED)
REFERENCE_1   = cnt_v2_architecture_design
REFERENCE_2   = cnt_v2_implementation_work_instruction
```

## 1. 목적

이 문서는 CNT v2 구현 결과를 검증하기 위한 공식 체크리스트다.

검증 목적:

- multi-strategy 실행 구조가 정상 연결되었는지 확인
- signal ranking이 의도대로 동작하는지 확인
- portfolio risk가 실제 execution 차단에 반영되는지 확인
- PortfolioState / PositionState 저장과 복원이 정상인지 확인
- Spot / Futures adapter 구조가 올바르게 분리됐는지 확인
- v1.1 baseline 동작에 손상이 없는지 확인

## 2. 검증 원칙

### 2.1 기존 안정 구조 훼손 금지

아래는 유지되어야 한다.

- `StrategySignal`
- `ExecutionDecision`
- `ExitSignal`
- `engine -> entry_gate -> execution_decider` 기본 계약
- v1.1 stop / target / trailing / time / partial exit 동작
- state persistence 기본 안정성

### 2.2 단계별 검증

v2는 단계적으로 검증한다.

```text
Phase 1 = multi-strategy / ranking
Phase 2 = portfolio state / risk
Phase 3 = market adapter / futures
Phase 4 = observability / metrics
```

### 2.3 forced BUY / live exposure 금지

검증 중에는:

- 강제 BUY 경로 사용 금지
- 실제 노출 진입 금지
- synthetic signal / dry adapter / isolated state로 검증

## 3. 검증 범위

포함:

- multi-strategy registry
- strategy_orchestrator
- signal_ranker
- PositionState / PortfolioState
- state_manager
- portfolio_risk_manager
- execution_decider portfolio integration
- order_router
- spot_adapter / futures_adapter
- portfolio_logger / metrics 구현부

제외:

- 실제 수익률 자체 비교
- 주문 체결 결과 평가
- 라이브 운영 확정

## 4. 문서 및 구조 검증

### A1. 문서 존재 확인

확인 대상:

- `docs/CNT v2 ARCHITECTURE DESIGN DOCUMENT.md`
- `docs/CNT v2 IMPLEMENTATION WORK INSTRUCTION.md`
- `docs/CNT v2 VALIDATION CHECKLIST.md`

판정 기준:

- 3개 문서 모두 존재
- 상호 reference 일치
- version / date / status 메타 정보 존재

### A2. AGENTS.md 반영 확인

확인 항목:

- `strategy_orchestrator`
- `signal_ranker`
- `portfolio_state`
- `position_state`
- `portfolio_risk_manager`
- `order_router`
- `spot_adapter`
- `futures_adapter`

판정 기준:

- 신규 component가 문서에 반영되어 있으면 PASS

### A3. EXTRA ITEMS REGISTER 반영 확인

신규 등록 대상 예시:

- `src/portfolio/strategy_orchestrator.py`
- `src/portfolio/signal_ranker.py`
- `src/models/position_state.py`
- `src/models/portfolio_state.py`
- `src/state/state_manager.py`
- `src/risk/portfolio_risk_manager.py`
- `src/execution/order_router.py`
- `src/market/spot_adapter.py`
- `src/market/futures_adapter.py`
- `src/logging/portfolio_logger.py`

판정 기준:

- 신규 파일이 등록 양식에 맞게 기록되면 PASS

## 5. Phase 1 검증 - Multi Strategy Core

### B1. strategy_registry 확장 확인

확인 항목:

- `breakout_v1`
- `pullback_v1`
- `mean_reversion_v1`

판정 기준:

- 전략이 실제 registry에 존재하면 PASS

### B2. generate_all_signals 동작 확인

기대 동작:

- 하나의 symbol에 대해 여러 전략이 신호를 생성
- 결과가 `list[StrategySignal]` 형태로 수집됨

판정 기준:

- 신호 목록 생성이 정상 동작하면 PASS

### B3. signal_ranker 동작 확인

테스트 시나리오:

- 2개 이상의 유효 BUY signal 생성
- 서로 다른 confidence 값 부여

기대 결과:

- 우선순위 규칙대로 1개 선택

판정 기준:

- 선택 로직이 설계와 일치하면 PASS

### B4. strategy_orchestrator 연결 확인

기대 흐름:

```text
symbol
-> generate_all_signals()
-> rank_signals()
-> selected_signal 반환
```

판정 기준:

- orchestrator가 실제 엔트리 경로와 연결되면 PASS

### B5. 기존 single-signal fallback 확인

기대 결과:

- 다전략 비활성 시 기존 단일 신호 흐름으로도 동작 가능

판정 기준:

- fallback 경로가 남아 있으면 PASS

## 6. Phase 2 검증 - Portfolio Layer

### C1. PositionState 모델 확인

필수 필드:

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

판정 기준:

- dataclass 또는 동등 구조로 정의되어 있으면 PASS

### C2. PortfolioState 모델 확인

핵심 필드:

- `schema_version`
- `total_exposure`
- `open_positions`
- `cash_balance`
- `daily_loss_count`
- `consecutive_losses`

판정 기준:

- 독립 state sidecar 구조가 확인되면 PASS

## 7. 최종 해석

이 체크리스트는 runtime activation 허가 문서가 아니다.

이 문서의 목적은 CNT v2 구조가 검증 가능 상태인지 확인하는 것이다.

즉 PASS가 나와도 바로 운영 준비 완료를 뜻하지는 않는다.

## 링크

- [[CNT v2 VALIDATION CHECKLIST]]
- [[CNT v2 VALIDATION REPORT KO]]
- [[CNT v2 PERFORMANCE VALIDATION REPORT KO]]

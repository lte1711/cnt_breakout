좋다. 아래는 **문서화 가능한 형식의 CNT v2 검증 체크리스트 (Validation Checklist)**다.
앞서 만든 v2 아키텍처 설계서와 구현 작업지시서에 맞춰, **바로 문서로 저장 가능한 형태**로 정리했다.

---

# CNT v2 VALIDATION CHECKLIST

```text
DOCUMENT_NAME = cnt_v2_validation_checklist
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-19
STATUS        = VALIDATION_READY
BASELINE      = CNT v1.1 (CLOSED)
REFERENCE_1   = cnt_v2_architecture_design
REFERENCE_2   = cnt_v2_implementation_work_instruction
```

---

# 1. PURPOSE

본 문서는 CNT v2 구현 결과를 검증하기 위한
**공식 검증 체크리스트**다.

검증 목적은 다음과 같다.

* 멀티 전략 실행 구조가 정상 연결되었는지 확인
* 신호 선택(signal ranking)이 의도대로 작동하는지 확인
* 포트폴리오 리스크 관리가 실제로 실행 차단에 반영되는지 확인
* PortfolioState / PositionState 저장과 복원이 정상 동작하는지 확인
* Spot / Futures adapter 구조가 안전하게 분리되어 있는지 확인
* 기존 v1.1 baseline 동작에 회귀가 없는지 확인

---

# 2. VALIDATION PRINCIPLES

## 2.1 기존 안정 구조 회귀 금지

다음은 반드시 유지되어야 한다.

* `StrategySignal`
* `ExecutionDecision`
* `ExitSignal`
* `engine → entry_gate → execution_decider` 기본 계약
* v1.1 stop/target/trailing/time/partial exit 동작
* state persistence 기본 안정성

---

## 2.2 단계별 검증

v2는 단계적으로 검증한다.

```text
Phase 1 → 멀티 전략 / ranking
Phase 2 → 포트폴리오 상태 / 리스크
Phase 3 → market adapter / futures
Phase 4 → observability / metrics
```

---

## 2.3 forced BUY / live exposure 금지

검증 시:

* 강제 BUY 경로 사용 금지
* 실제 실거래 진입 금지
* synthetic signal / dry adapter / isolated state로 검증

---

# 3. VALIDATION SCOPE

## 포함 범위

* multi-strategy registry
* strategy_orchestrator
* signal_ranker
* PositionState / PortfolioState
* state_manager
* portfolio_risk_manager
* execution_decider portfolio integration
* order_router
* spot_adapter / futures_adapter
* portfolio_logger / metrics (구현 시)

## 제외 범위

* 전략 수익률 자체의 우열 비교
* 실거래 성과 평가
* 라이브 운영 승인

---

# 4. DOCUMENT AND STRUCTURE VALIDATION

## A1. 문서 존재 확인

확인 대상:

* `docs/cnt_v2_architecture_design.*`
* `docs/cnt_v2_implementation_work_instruction.*`
* `docs/cnt_v2_validation_checklist.*`

판정 기준:

* 3개 문서 모두 존재
* 상호 reference 일치
* 버전/날짜/상태 메타 일관성 유지

---

## A2. AGENTS.md 반영 확인

확인 항목:

* `strategy_orchestrator`
* `signal_ranker`
* `portfolio_state`
* `position_state`
* `portfolio_risk_manager`
* `order_router`
* `spot_adapter`
* `futures_adapter`

판정 기준:

* 신규 컴포넌트가 문서에 반영되어 있으면 PASS

---

## A3. EXTRA ITEMS REGISTER 반영 확인

신규 등록 대상 예시:

* `src/portfolio/strategy_orchestrator.py`
* `src/portfolio/signal_ranker.py`
* `src/models/position_state.py`
* `src/models/portfolio_state.py`
* `src/state/state_manager.py`
* `src/risk/portfolio_risk_manager.py`
* `src/execution/order_router.py`
* `src/market/spot_adapter.py`
* `src/market/futures_adapter.py`
* `src/logging/portfolio_logger.py` (구현 시)

판정 기준:

* 신규 파일이 등록 원칙에 맞게 기록되어 있으면 PASS

---

# 5. PHASE 1 VALIDATION — MULTI STRATEGY CORE

## B1. strategy_registry 확장 확인

확인 항목:

* `breakout_v1`
* `pullback_v1`
* `mean_reversion_v1` (구현 범위에 포함된 경우)

판정 기준:

* 다전략 등록이 실제로 존재하면 PASS

---

## B2. generate_all_signals 동작 확인

기대 동작:

* 하나의 symbol에 대해 여러 전략이 순차 실행됨
* 결과가 `list[StrategySignal]` 형태로 수집됨

판정 기준:

* 신호 목록 생성이 정상 동작하면 PASS

---

## B3. signal_ranker 동작 확인

테스트 시나리오:

* 2개 이상 유효 BUY signal 생성
* 서로 다른 confidence 값 부여

기대 결과:

* 우선순위 규칙대로 1개가 선택됨

판정 기준:

* 선택 로직이 설계와 일치하면 PASS

---

## B4. strategy_orchestrator 연결 확인

기대 흐름:

```text
symbol
→ generate_all_signals()
→ rank_signals()
→ selected_signal 반환
```

판정 기준:

* orchestrator가 실제 엔트리 경로에 연결되면 PASS

---

## B5. 기존 single-signal fallback 확인

기대 결과:

* 다전략 비활성 시 기존 단일 전략 흐름으로도 동작 가능

판정 기준:

* fallback 경로가 살아 있으면 PASS

---

# 6. PHASE 2 VALIDATION — PORTFOLIO LAYER

## C1. PositionState 모델 확인

필수 필드:

* `position_id`
* `symbol`
* `market_type`
* `strategy_name`
* `entry_price`
* `entry_qty`
* `entry_time`
* `stop_price`
* `target_price`
* `status`

판정 기준:

* dataclass 또는 동등 구조로 정의되어 있으면 PASS

---

## C2. PortfolioState 모델 확인

필수 필드:

* `schema_version`
* `total_exposure`
* `open_positions`

권장 필드:

* `cash_balance`
* `daily_loss_count`
* `consecutive_losses`

판정 기준:

* 포트폴리오 단위 상태 모델이 존재하면 PASS

---

## C3. state_manager 동작 확인

기대 동작:

* portfolio_state 저장
* position list 저장
* 재시작 후 복원 가능

판정 기준:

* state load/save lifecycle 정상 동작 시 PASS

---

## C4. portfolio_risk_manager 확인

기대 함수:

```python
check_portfolio_risk(signal, portfolio_state)
```

판정 기준:

* 포트폴리오 전체 한도 체크가 실제 함수로 존재하면 PASS

---

## C5. max exposure 차단 확인

테스트 시나리오:

* `total_exposure`를 한도 이상으로 구성
* 신규 BUY signal 생성

기대 결과:

* 실행 거부
* 명확한 rejection reason 반환

판정 기준:

* 차단 동작 시 PASS

---

## C6. symbol-level risk 차단 확인

테스트 시나리오:

* 동일 symbol에서 이미 포지션 존재
* one-per-symbol 정책 활성

기대 결과:

* 신규 실행 거부

판정 기준:

* 심볼 중복 진입 차단 시 PASS

---

# 7. PHASE 3 VALIDATION — MARKET ADAPTER

## D1. spot_adapter 존재 확인

판정 기준:

* spot 전용 adapter 파일/클래스/함수가 존재하면 PASS

---

## D2. futures_adapter 존재 확인

판정 기준:

* futures 전용 adapter 파일/클래스/함수가 존재하면 PASS

---

## D3. order_router 분기 확인

기대 흐름:

```text
if market == spot:
    spot_adapter
else:
    futures_adapter
```

판정 기준:

* 시장 타입에 따라 분기하면 PASS

---

## D4. futures dry path 확인

검증 항목:

* leverage 파라미터 처리
* margin mode 처리
* reduce-only 또는 close-position 플래그 처리

주의:

* 실제 주문 제출 없이 dry validation 수행

판정 기준:

* futures-specific 파라미터가 구조적으로 처리되면 PASS

---

## D5. strategy layer market neutrality 확인

검증 항목:

* 전략 코드가 직접 futures 주문 규칙을 알지 않아야 함
* 전략은 signal만 생성

판정 기준:

* Spot/Futures 차이가 adapter 레이어에서 처리되면 PASS

---

# 8. PHASE 4 VALIDATION — OBSERVABILITY

## E1. portfolio_logger 존재 확인

판정 기준:

* 포트폴리오 의사결정 로그를 남기는 모듈/함수가 존재하면 PASS

---

## E2. portfolio decision log 확인

기대 기록 항목:

* symbol
* selected strategy
* rejected strategies
* rejection reasons
* portfolio risk decision

판정 기준:

* 의사결정 로그가 남으면 PASS

---

## E3. metrics 수집 확인

권장 메트릭:

* strategy hit rate
* rejection count
* average hold time
* stop/target/trailing ratio
* daily pnl

판정 기준:

* 최소 1개 이상의 포트폴리오 메트릭 수집 구조가 있으면 PASS

---

# 9. ENGINE INTEGRATION VALIDATION

## F1. engine → strategy_orchestrator 연결 확인

기대 결과:

* engine이 더 이상 직접 단일 strategy_manager 결과만 보지 않고
* orchestrator의 selected signal을 소비

판정 기준:

* 연결되면 PASS

---

## F2. execution_decider 포트폴리오 통합 확인

기대 결과:

* `ExecutionDecision` 생성 전에 portfolio risk check 수행

판정 기준:

* account risk + portfolio risk가 함께 반영되면 PASS

---

## F3. 기존 exit 경로 회귀 없음

기존 동작:

* STOP
* TARGET
* TRAILING_STOP
* TIME_EXIT
* PARTIAL

판정 기준:

* v1.1 Stage 2 exit 기능에 회귀 없으면 PASS

---

# 10. STATE PERSISTENCE VALIDATION

## G1. schema version 분리 확인

기대 결과:

* v2 state가 `schema_version = 2.0` 등으로 분리
* v1.1 state와 직접 충돌하지 않음

판정 기준:

* 상태 스키마 분리가 명확하면 PASS

---

## G2. portfolio_state 저장 확인

기대 항목:

* 총 노출
* 열린 포지션 목록
* 리스크 메트릭

판정 기준:

* portfolio 수준 저장 가능하면 PASS

---

## G3. PositionState 복원 확인

테스트:

* 포지션 상태 저장 후 엔진 재시작

기대 결과:

* stop/target/trailing 관련 값 포함 복원

판정 기준:

* 재시작 후 lifecycle 연속성 유지되면 PASS

---

## G4. 다중 포지션 복원 확인

테스트:

* 둘 이상의 synthetic position 저장

기대 결과:

* 각 포지션이 독립 복원됨

판정 기준:

* 포지션 간 state 섞임 없으면 PASS

---

# 11. RUNTIME VALIDATION

## H1. py_compile 확인

실행 예시:

```bash
python -m py_compile config.py main.py binance_client.py src/*.py src/models/*.py src/risk/*.py src/strategies/*.py src/portfolio/*.py src/market/*.py
```

판정 기준:

* 에러 없으면 PASS

---

## H2. import 확인

판정 기준:

* `main.py` 및 신규 모듈 import 에러 없음

---

## H3. multi-strategy synthetic test

시나리오:

* 하나의 symbol에 대해 breakout, pullback 두 신호 생성

기대 결과:

* 1개만 선택되거나 정책대로 선택됨

판정 기준:

* ranker 정책 일치 시 PASS

---

## H4. portfolio risk synthetic test

시나리오:

* exposure 초과 상태 구성

기대 결과:

* BUY signal이 있어도 execute=False

판정 기준:

* 포트폴리오 리스크 차단 동작 시 PASS

---

## H5. futures adapter dry test

시나리오:

* futures decision 생성
* dry routing만 수행

기대 결과:

* adapter 분기 정상
* 실제 주문 제출 없음

판정 기준:

* dry validation 성공 시 PASS

---

## H6. v1.1 regression test

검증 항목:

* single strategy mode 정상
* risk_guard 정상
* signal.log 정상
* runtime.log 정상
* state persistence 정상
* enhanced_exit_manager 정상

판정 기준:

* 기존 baseline 회귀 없으면 PASS

---

# 12. FAILURE CLASSIFICATION

## FAIL-CRITICAL

즉시 수정 후 재검증 대상:

* multi-strategy 충돌로 잘못된 다중 주문 발생
* portfolio risk가 실행에 반영되지 않음
* state schema 충돌
* Spot/Futures adapter 혼선
* 기존 exit 기능 회귀
* engine이 orchestrator 없이 직접 단일 전략만 사용
* futures dry path가 live order 경로를 건드림

---

## FAIL-MINOR

수정 권장 후 재검증 대상:

* AGENTS.md 미갱신
* EXTRA ITEMS REGISTER 누락
* metrics 일부 누락
* logger 포맷 미흡
* fallback 문서화 부족

---

# 13. COMPLETION CRITERIA

CNT v2 초기 완료 조건은 다음과 같다.

* multi-strategy signal generation 가능
* signal ranking 정상
* one-per-symbol 정책 동작
* portfolio risk manager 동작
* PositionState / PortfolioState 저장 및 복원 가능
* Spot/Futures adapter 분리 구조 존재
* 기존 v1.1 기능 회귀 없음
* compile/import/runtime 검증 통과

---

# 14. FINAL RESULT TEMPLATE

```text
CNT v2 VALIDATION REPORT

DATE=
PROJECT=CNT
VERSION=2.0
STATUS=

SUMMARY
- Document and structure: PASS / FAIL
- Multi-strategy flow: PASS / FAIL
- Portfolio risk: PASS / FAIL
- State persistence: PASS / FAIL
- Market adapter: PASS / FAIL
- Runtime validation: PASS / FAIL
- Regression validation: PASS / FAIL

FINAL DECISION
- CNT v2 initial implementation complete / incomplete
- Approved / fix required
```

---

# 15. FINAL STATEMENT

본 체크리스트는 CNT v2가 단순한 기능 추가가 아니라,
**멀티 전략 + 포트폴리오 + 시장 어댑터 구조를 안전하게 운영 가능한지**를 검증하기 위한 기준이다.

```text
핵심:
좋은 전략을 여러 개 만드는 것보다,
여러 전략과 여러 시장을 안전하게 동시에 다룰 수 있어야 한다
```

---

# 결론

> **CNT v2 검증은 전략, 포트폴리오, 시장 어댑터, 상태, 리스크가 서로 충돌 없이 통합되는지를 확인하는 절차다.**

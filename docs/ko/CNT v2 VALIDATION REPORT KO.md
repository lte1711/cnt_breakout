---
tags:
  - cnt
  - docs
  - validation
  - report
  - v2
  - ko
aliases:
  - CNT v2 VALIDATION REPORT KO
---

# CNT v2 검증 보고서

```text
DOCUMENT_NAME = cnt_v2_validation_report_ko
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-19
STATUS        = PATCH_PENDING_VALIDATION_BASELINE
BASELINE      = CNT v1.1 (CLOSED)
REFERENCE_1   = cnt_v2_architecture_design
REFERENCE_2   = cnt_v2_implementation_work_instruction
REFERENCE_3   = cnt_v2_validation_checklist
```

## 1. 요약

CNT v2 초기 구현은 닫힌 CNT v1.1 baseline 위에 추가되었지만,
첫 validation pass에서는 구조와 runtime behavior 사이에 patch가 필요한 간극이 남아 있었다.

검증된 범위:

- multi-strategy registry expansion
- multi-strategy signal generation support
- signal ranking support
- strategy_orchestrator integration
- PositionState / PortfolioState models
- portfolio_state sidecar persistence
- portfolio risk manager integration into ExecutionDecision
- spot/futures adapter split
- dry order routing
- portfolio-level logging

## 2. 검증 결과

### 2.1 문서 및 구조

PASS

확인:

- `docs/CNT v2 ARCHITECTURE DESIGN DOCUMENT.md`
- `docs/CNT v2 IMPLEMENTATION WORK INSTRUCTION.md`
- `docs/CNT v2 VALIDATION CHECKLIST.md`
- `AGENTS.md`에 v2 portfolio / market adapter component 반영
- `docs/EXTRA ITEMS REGISTER.md`에 v2 추가 파일 반영

### 2.2 Multi-strategy flow

PASS

확인:

- `strategy_registry` 확장:
  - `breakout_v1`
  - `pullback_v1`
  - `mean_reversion_v1`
- `generate_all_signals(symbol)` 추가
- `signal_ranker`가 highest-confidence valid signal 선택
- `strategy_orchestrator`가 단일 selected signal 반환

Activation note:

- runtime 기본 active strategies는 `breakout_v1`, `pullback_v1`
- `mean_reversion_v1`는 등록 및 파라미터화되었지만 기본 baseline에서는 inactive

관측된 synthetic ranking result:

```text
selected= pullback_v1 0.8
```

### 2.3 Portfolio risk

PARTIAL

확인:

- `portfolio_risk_manager.check_portfolio_risk(...)` 추가
- `execution_decider.decide_execution(...)`가 `portfolio_state`를 받도록 확장
- portfolio rejection reason이 `ExecutionDecision`에 반영됨

관측된 synthetic result:

```text
exposure= (False, 'MAX_PORTFOLIO_EXPOSURE_EXCEEDED')
one_per_symbol= (False, 'ONE_PER_SYMBOL_POLICY')
```

Patch note:

- 초기 v2 build는 첫 구현에서 surrogate exposure quantity를 사용했다
- 따라서 patch validation이 끝나기 전까지는 portfolio risk policy가 runtime에서 완전히 정확하다고 읽으면 안 된다

### 2.4 State persistence

PASS

확인:

- v1.1 runtime state는 `schema_version=1.0` 유지
- v2 sidecar state는 독립적으로 `schema_version=2.0`으로 persist

관측된 v2 sidecar state:

```json
{
  "schema_version": "2.0",
  "total_exposure": 0.0,
  "open_positions": [],
  "cash_balance": 0.0,
  "daily_loss_count": 0,
  "consecutive_losses": 0
}
```

### 2.5 Market adapter

PARTIAL

확인:

- `spot_adapter.submit_order(...)` 존재
- `futures_adapter.submit_order(...)` 존재
- `execution/order_router.py`가 dry validation 범위에서 market type별 route 수행

관측된 dry routing result:

```text
{'market': 'spot', 'dry_run': True, 'payload': {'symbol': 'ETHUSDT', 'side': 'BUY'}}
{'market': 'futures', 'dry_run': True, 'payload': {'symbol': 'ETHUSDT', 'side': 'BUY', 'leverage': 1, 'margin_mode': 'ISOLATED', 'reduce_only': False}}
```

Patch note:

- `order_router`는 prepared routing structure
- 초기 v2 engine runtime path는 아직 direct order submission function을 사용
- 따라서 runtime routing은 `prepared but not yet connected`로 기술해야 한다

### 2.6 Runtime validation

PARTIAL

완료된 체크:

- `py_compile` passed for 43 files
- `main.py`와 신규 v2 module import 성공
- actual one-shot safe runtime validation을 `run.ps1` entry chain 기준으로 수행

Safe runtime method:

- temporary `STRATEGY_ENABLED=False`
- normal entry chain으로 실행
- no order path 확인
- 이후 `STRATEGY_ENABLED=True` 복원

관측된 runtime result:

```text
action=NO_ENTRY_SIGNAL
reason=no_ranked_signal
```

관측된 portfolio log result:

```text
[2026-04-19 08:47:43] symbol=ETHUSDT selected_strategy=NONE reason=no_ranked_signal
```

Patch note:

- 이 runtime check는 entry-chain continuity와 safe no-entry behavior를 확인했다
- 그러나 pending reconciliation, routed execution, loss-policy enforcement의 운영 준비도를 완전히 증명한 것은 아니다

### 2.7 Regression validation

PASS

확인된 baseline preservation:

- `StrategySignal`, `ExecutionDecision`, `ExitSignal` contract 유지
- v1.1 state persistence 유지
- Stage 1, Stage 2 module import 및 compile 유지
- v1.1 exit path 구조 제거 없음

## 3. 최종 결정

```text
Document and structure: PASS
Multi-strategy flow: PASS
Portfolio risk: PARTIAL
State persistence: PASS
Market adapter: PARTIAL
Runtime validation: PARTIAL
Regression validation: PASS
```

```text
CNT v2 initial implementation complete as a structural baseline
Not approved for operating-readiness claims before mandatory patch completion
```

## 4. 공식 결론

CNT v2 초기 구현은 CNT v1.1 위의 유효한 확장이지만, operating-ready라기보다 patch-pending 상태로 해석해야 한다.

현재 결과가 확인한 것:

- 여러 전략 후보를 생성하고 rank할 수 있다
- portfolio-level risk rejection이 single-position risk logic과 구조적으로 분리됐다
- portfolio state는 v1.1 runtime state와 독립적으로 저장된다
- spot/futures execution structure는 adapter 기반이며 dry-route 가능하지만 active runtime submission path는 아니다
- 닫힌 v1.1 baseline은 검증 범위 안에서 유지된다

## 링크

- [[CNT v2 VALIDATION REPORT]]
- [[CNT v2 VALIDATION CHECKLIST KO]]
- [[CNT v2 PERFORMANCE VALIDATION REPORT KO]]

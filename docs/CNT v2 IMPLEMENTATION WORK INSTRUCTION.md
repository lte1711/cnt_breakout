---
tags:
  - cnt
  - docs
  - instruction
  - v2
aliases:
  - CNT v2 IMPLEMENTATION WORK INSTRUCTION
---

# CNT v2 IMPLEMENTATION WORK INSTRUCTION

```text
DOCUMENT_NAME = cnt_v2_implementation_work_instruction
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-19
STATUS        = READY_FOR_IMPLEMENTATION
BASELINE      = CNT v1.1 (CLOSED)
REFERENCE     = cnt_v2_architecture_design
```

---

# 1. PURPOSE

본 문서는 CNT v2를 단계적으로 구현하기 위한 **작업 단위(Task)와 순서**를 정의한다.

핵심 원칙:

```text
v1.1 코어는 절대 수정하지 않는다.
모든 기능은 상위 레이어로 추가한다.
```

---

# 2. IMPLEMENTATION STRATEGY

## 2.1 단계적 확장 방식

```text
Phase 1 → 멀티 전략 + signal ranking
Phase 2 → 포트폴리오 리스크 + 상태 확장
Phase 3 → Futures adapter
Phase 4 → 분석/고도화
```

---

# 3. PHASE 1 — MULTI STRATEGY CORE

---

## T1. strategy_registry 확장

### 목적

멀티 전략 등록

### 작업

```python
# src/strategy/strategy_registry.py

STRATEGY_REGISTRY = {
    "breakout_v1": BreakoutV1Strategy,
    "pullback_v1": PullbackV1Strategy,        # 신규
    "mean_reversion_v1": MeanReversionV1Strategy  # 신규
}
```

### 산출물

* pullback_v1.py
* mean_reversion_v1.py

---

## T2. multi-strategy 실행 지원 (strategy_manager 확장)

### 목적

한 심볼에 대해 여러 전략 실행

### 작업

```python
def generate_all_signals(symbol: str) -> list[StrategySignal]:
    signals = []
    for strategy_name in ACTIVE_STRATEGIES:
        signal = run_strategy(strategy_name, symbol)
        signals.append(signal)
    return signals
```

### 주의

* 기존 `generate_strategy_signal()` 유지 (호환성)
* 신규 함수만 추가

---

## T3. signal_ranker 추가

### 파일

```text
src/portfolio/signal_ranker.py
```

### 목적

여러 신호 중 선택

### 구조

```python
def rank_signals(signals: list[StrategySignal]) -> StrategySignal | None:
    valid = [s for s in signals if s.entry_allowed]

    if not valid:
        return None

    # 기본 정책: confidence 최고
    return sorted(valid, key=lambda s: s.confidence, reverse=True)[0]
```

---

## T4. strategy_orchestrator 추가

### 파일

```text
src/portfolio/strategy_orchestrator.py
```

### 역할

```text
symbol → 모든 전략 실행 → ranking → 선택 signal 반환
```

### 구현

```python
def get_selected_signal(symbol: str) -> StrategySignal | None:
    signals = generate_all_signals(symbol)
    return rank_signals(signals)
```

---

## T5. engine → orchestrator 연결

### 기존

```text
engine → strategy_manager → single signal
```

### 변경

```text
engine → strategy_orchestrator → selected signal
```

### 작업

```python
signal = get_selected_signal(symbol)
```

---

## T6. config 확장

```python
ACTIVE_STRATEGIES = [
    "breakout_v1",
    "pullback_v1"
]
```

---

# 4. PHASE 2 — PORTFOLIO LAYER

---

## T7. PositionState 모델 추가

### 파일

```text
src/models/position_state.py
```

```python
@dataclass
class PositionState:
    position_id: str
    symbol: str
    market_type: str
    strategy_name: str
    entry_price: float
    entry_qty: float
    entry_time: str
    stop_price: float | None
    target_price: float | None
    status: str
```

---

## T8. PortfolioState 모델 추가

### 파일

```text
src/models/portfolio_state.py
```

```python
@dataclass
class PortfolioState:
    schema_version: str
    total_exposure: float
    open_positions: list[PositionState]
```

---

## T9. state_manager 추가

### 파일

```text
src/state/state_manager.py
```

### 역할

* portfolio_state load/save
* position list 관리

---

## T10. portfolio_risk_manager 추가

### 파일

```text
src/risk/portfolio_risk_manager.py
```

### 기능

```python
def check_portfolio_risk(signal, portfolio_state) -> tuple[bool, str | None]:
    ...
```

---

## T11. execution_decider 확장

### 추가

```python
portfolio_pass, reason = check_portfolio_risk(signal, portfolio_state)
```

---

# 5. PHASE 3 — MARKET ADAPTER (FUTURES)

---

## T12. market_adapter 구조 추가

```text
src/market/
  spot_adapter.py
  futures_adapter.py
```

---

## T13. order_router 추가

```text
src/execution/order_router.py
```

```python
def route_order(decision):
    if decision.market == "spot":
        return spot_adapter.submit(...)
    else:
        return futures_adapter.submit(...)
```

---

## T14. futures_adapter 구현

### 기능

* leverage 설정
* margin type
* reduce-only 처리
* funding 고려

---

# 6. PHASE 4 — OBSERVABILITY

---

## T15. portfolio_logger 추가

```text
src/logging/portfolio_logger.py
```

---

## T16. metrics 수집

* pnl
* win rate
* stop vs target ratio

---

# 7. VALIDATION STEPS

---

## V1. compile

```bash
python -m py_compile ...
```

---

## V2. import

```python
import main
```

---

## V3. multi-strategy test

* breakout + pullback 동시 실행
* 1개만 선택되는지 확인

---

## V4. portfolio risk test

* max exposure 초과 시 reject 확인

---

## V5. futures dry test

* 실제 주문 없이 adapter 호출 확인

---

# 8. ROLLBACK STRATEGY

```text
engine entry path를 기존 single strategy로 되돌리면 즉시 복구 가능
```

---

# 9. COMPLETION CRITERIA

다음 조건 만족 시 Phase 완료:

* 멀티 전략 실행 가능
* 신호 선택 정상
* 포트폴리오 리스크 차단 동작
* 상태 저장 정상
* 기존 v1.1 동작 유지

---

# 10. FINAL NOTE

CNT v2 구현의 핵심은 이것 하나다:

```text
복잡성을 추가하지 말고, 계층을 추가하라
```

---

# 한 줄 결론

> **CNT v2는 “전략을 잘 만드는 프로젝트”에서 “전략을 운영하는 시스템”으로의 전환이다.**

---

---

## Obsidian Links

- [[00 CNT Vault Home|Vault Home]]
- [[00 Docs Index|Docs Index]]

### Related
- [[00 Docs Index|Docs Index]]

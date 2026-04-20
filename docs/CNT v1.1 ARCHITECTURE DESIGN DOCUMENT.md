---
tags:
  - cnt
  - docs
  - v1
aliases:
  - CNT v1.1 ARCHITECTURE DESIGN DOCUMENT
---

# CNT v1.1 ARCHITECTURE DESIGN DOCUMENT

```
DOCUMENT_NAME = cnt_v1.1_architecture_design
PROJECT       = CNT
VERSION       = 1.1
DATE          = 2026-04-19
STATUS        = DESIGN_FINALIZED
BASELINE      = CNT v1 (CLOSED)
```

---

# 1. PURPOSE

본 문서는 CNT v1 기반 위에서 실행 품질과 리스크 제어를 확장하는
**CNT v1.1 아키텍처 설계 정의서**다.

v1의 목적은 구조 안정화였으며, v1.1의 목적은 다음과 같다:

* 신호와 실행의 분리 (ExecutionDecision)
* 운영 리스크 제어 (risk_guard)
* 전략 관측성 확보 (signal_logger)
* 청산 전략 확장 기반 구축 (enhanced_exit)

---

# 2. DESIGN PRINCIPLES

## 2.1 v1 계약 유지 (MANDATORY)

다음은 변경 금지 대상이다:

* engine → entry_gate → strategy_manager 흐름
* StrategySignal 데이터 계약
* ExitModel 기본 구조
* state schema_version = 1.0
* single strategy / single position 구조

---

## 2.2 신호와 실행 분리

```
StrategySignal != ExecutionDecision
```

전략은 "진입 가능성"을 판단하고,
ExecutionDecision은 "실제 실행 여부"를 결정한다.

---

## 2.3 리스크는 전략 외부에서 통제

전략은 시장 판단만 수행한다.
리스크 제어는 반드시 strategy 외부 레이어에서 수행한다.

---

## 2.4 상태 기반 리스크 추적

```
risk_guard는 로그를 절대 파싱하지 않는다
```

모든 리스크 판단은 state 기반으로 수행한다.

---

## 2.5 청산은 단계적으로 확장

v1의 stop/target은 유지하고,
v1.1에서는 trailing / partial / time exit를 optional로 추가한다.

---

# 3. TARGET ARCHITECTURE

## 3.1 v1 구조

```
engine
  -> entry_gate
    -> strategy_manager
      -> strategy_registry
        -> breakout_v1
```

---

## 3.2 v1.1 구조

```
engine
  -> entry_gate
    -> strategy_manager
      -> strategy_registry
        -> breakout_v1
      -> StrategySignal

  -> signal_logger

  -> execution_decider
    -> risk_guard
    -> ExecutionDecision

  -> order_validator
  -> order_executor

  -> enhanced_exit_manager
```

---

# 4. CORE COMPONENTS

---

## 4.1 StrategySignal (UNCHANGED CONTRACT)

```python
@dataclass
class StrategySignal:
    strategy_name: str
    symbol: str

    signal_timestamp: float
    signal_age_limit_sec: float

    entry_allowed: bool
    side: str

    trigger: str
    reason: str
    confidence: float

    market_state: str
    volatility_state: str

    entry_price_hint: float | None
    exit_model: ExitModel | None
```

---

## 4.2 ExecutionDecision (NEW)

### 목적

전략 신호와 실제 주문 실행을 분리한다.

```python
@dataclass
class ExecutionDecision:
    execute: bool
    action: str

    reason: str
    signal_reason: str

    strategy_name: str
    symbol: str

    validated_qty: float | None
    validated_price: float | None
    notional_value: float | None

    risk_check_passed: bool
    risk_rejection_reason: str | None

    slippage_check_passed: bool
    slippage_rejection_reason: str | None
```

---

## 4.3 risk_guard (NEW)

### 목적

운영 리스크 제어

### 입력

* StrategySignal
* state
* balance

### 출력

```python
@dataclass
class RiskCheckResult:
    passed: bool
    reason: str
```

---

## 4.4 signal_logger (NEW)

### 목적

전략 평가 결과 기록

### 위치

```
src/signal_logger.py
```

### 로그 예시

```
strategy=breakout_v1 symbol=ETHUSDT entry_allowed=True trigger=BREAKOUT reason=trend_up confidence=0.82
```

---

## 4.5 enhanced_exit_manager (NEW)

### 목적

청산 판단 로직 확장

### 역할

* trailing stop 평가
* partial exit 평가
* time exit 평가

### 규칙

```
판단만 수행
실제 주문은 engine이 수행
```

---

# 5. EXECUTION FLOW

## 5.1 Entry Flow

```
1. signal = generate_strategy_signal()

2. gate = evaluate_entry_gate_from_signal(signal)

3. if gate != ENTRY_ALLOWED:
       STOP

4. decision = execution_decider.decide(signal, state, balance)

5. if decision.execute is False:
       STOP

6. order_validator → order_executor
```

---

## 5.2 Exit Flow

```
HOLD 상태:

1. exit_signal = enhanced_exit_manager.evaluate(open_trade, price)

2. if exit_signal.should_exit:
       기존 SELL / STOP 실행

3. else:
       HOLD
```

---

# 6. RISK MANAGEMENT DESIGN

## 6.1 State 기반 리스크 구조

```json
{
  "risk_metrics": {
    "daily_loss_count": 2,
    "consecutive_losses": 2,
    "last_loss_time": "2026-04-19 14:20:00"
  }
}
```

---

## 6.2 최소 규칙 (v1.1 Stage 1)

### 1) Daily Loss Limit

```
MAX_DAILY_LOSS = threshold
```

### 2) Loss Cooldown

```
MAX_CONSECUTIVE_LOSSES
LOSS_COOLDOWN_MINUTES
```

---

# 7. EXIT MODEL EXTENSION

```python
@dataclass
class PartialExitLevel:
    qty_ratio: float
    target_price: float


@dataclass
class ExitModel:
    stop_price: float | None
    target_price: float | None

    trailing_stop_pct: float | None = None
    partial_exit_levels: list[PartialExitLevel] | None = None
    time_based_exit_minutes: int | None = None
```

---

## 7.1 Partial Exit 규칙

```
adjusted_qty = floor(entry_qty * ratio / step_size) * step_size

if adjusted_qty < min_qty:
    partial exit 불가 → fallback 처리
```

---

# 8. STATE EXTENSION (OPTIONAL)

```json
{
  "highest_price_since_entry": 100.8,
  "partial_exit_progress": 0,
  "entry_time": "2026-04-19 14:20:00"
}
```

---

# 9. IMPLEMENTATION PLAN

## Stage 1 (MANDATORY)

1. strategy_signal.py 제거
2. ExecutionDecision 도입
3. execution_decider 추가
4. risk_guard 추가 (daily loss + cooldown)
5. signal_logger 연결

---

## Stage 2 (EXTENSION)

6. enhanced_exit_manager 도입
7. trailing stop
8. time-based exit
9. partial exit

---

# 10. VALIDATION CRITERIA

다음 조건을 만족해야 v1.1 1차 완료로 간주한다:

* StrategySignal → ExecutionDecision 분리 동작
* risk_guard가 실행 차단 가능
* signal_logger 기록 정상
* 기존 v1 stop/target 회귀 없음
* 엔진이 ExecutionDecision 기반으로만 주문 실행

---

# 11. REMOVAL PROCEDURE

## strategy_signal.py 제거 전 필수 확인

```
grep -R "src.strategy_signal" src → 0건
grep -R "import strategy_signal" src → 0건
py_compile 전체 통과
```

---

# 12. FINAL STATEMENT

CNT v1.1은 구조 변경이 아니라 확장이다.

```
목표:
신호 품질 → 실행 품질 → 리스크 통제 → 수익 구조 개선
```

---

# 결론

> **CNT v1.1은 전략을 바꾸는 단계가 아니라, 실행과 리스크를 제어하는 단계다.**

---

---

## Obsidian Links

- [[00 CNT Vault Home|Vault Home]]
- [[00 Docs Index|Docs Index]]

### Related
- [[00 Docs Index|Docs Index]]

---
aliases:
  - CNT v1.1 ARCHITECTURE DESIGN DOCUMENT KO
---

# CNT v1.1 아키텍처 설계 문서

```text
DOCUMENT_NAME = cnt_v1.1_architecture_design_ko
PROJECT       = CNT
VERSION       = 1.1
DATE          = 2026-04-19
STATUS        = DESIGN_FINALIZED
BASELINE      = CNT v1 (CLOSED)
```

## 1. 목적

이 문서는 CNT v1 기반 위에 실행 안정성과 리스크 제어를 확장하는
**CNT v1.1 아키텍처 설계 정의서**다.

v1의 목적은 구조 안정화였고, v1.1의 목적은 다음과 같다.

- 신호와 실행의 분리 (`ExecutionDecision`)
- 운영 리스크 제어 (`risk_guard`)
- 신호 관측성 정보 (`signal_logger`)
- 청산 구조 확장 기반 구축 (`enhanced_exit`)

## 2. 설계 원칙

### 2.1 v1 계약 유지

아래는 변경 금지 대상이다.

- `engine -> entry_gate -> strategy_manager` 흐름
- `StrategySignal` 데이터 계약
- `ExitModel` 기본 구조
- `state schema_version = 1.0`
- single strategy / single position 구조

### 2.2 신호와 실행 분리

```text
StrategySignal != ExecutionDecision
```

신호는 “진입 가능성”만 판단하고,
ExecutionDecision은 “실제 실행 여부”를 결정한다.

### 2.3 리스크는 전략 밖에서 통제

전략은 시장 판단만 수행한다.
리스크 제어는 반드시 strategy 밖의 레이어에서 수행한다.

### 2.4 상태 기반 리스크 추적

```text
risk_guard는 로그를 믿고 판단하지 않는다
```

모든 리스크 판단은 state 기반으로 수행한다.

### 2.5 청산은 단계적으로 확장

v1의 stop/target은 유지하고,
v1.1에서는 trailing / partial / time exit를 optional로 추가한다.

## 3. 목표 구조

### 3.1 v1 구조

```text
engine
  -> entry_gate
    -> strategy_manager
      -> strategy_registry
        -> breakout_v1
```

### 3.2 v1.1 구조

```text
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

## 4. 핵심 구성요소

### 4.1 StrategySignal

기존 계약 유지.

### 4.2 ExecutionDecision

목적:

- 신호와 실제 주문 실행을 분리한다

핵심 필드:

- `execute`
- `action`
- `reason`
- `signal_reason`
- `strategy_name`
- `symbol`
- `validated_qty`
- `validated_price`
- `notional_value`
- `risk_check_passed`
- `risk_rejection_reason`
- `slippage_check_passed`
- `slippage_rejection_reason`

### 4.3 risk_guard

목적:

- 운영 리스크 제어

입력:

- `StrategySignal`
- `state`
- `balance`

출력:

- `RiskCheckResult`

### 4.4 signal_logger

목적:

- 신호 평가 결과 기록

위치:

- `src/signal_logger.py`

### 4.5 enhanced_exit_manager

목적:

- 청산 판단 로직 확장

역할:

- trailing stop 평가
- partial exit 평가
- time exit 평가

규칙:

- 판단만 수행
- 실제 주문은 engine이 수행

## 5. 실행 흐름

### 5.1 Entry Flow

```text
1. signal = generate_strategy_signal()
2. gate = evaluate_entry_gate_from_signal(signal)
3. if gate != ENTRY_ALLOWED: STOP
4. decision = execution_decider.decide_execution(...)
5. if decision.execute: validator -> executor
```

## 최종 의미

CNT v1.1은 v1 구조를 깨지 않고,
신호/실행 분리와 리스크 제어, 관측 가능성, 청산 확장을 위한 아키텍처 계층을 추가하는 설계다.

## 링크

- CNT v1.1 ARCHITECTURE DESIGN DOCUMENT
- CNT v1.1 IMPLEMENTATION WORK INSTRUCTION KO
- CNT v1.1 IMPLEMENTATION VALIDATION REPORT KO

## Obsidian Links

- [[00 Docs Index KO]]



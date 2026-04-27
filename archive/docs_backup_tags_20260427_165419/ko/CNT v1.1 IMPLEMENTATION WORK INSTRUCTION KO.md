---
aliases:
  - CNT v1.1 IMPLEMENTATION WORK INSTRUCTION KO
---

# CNT v1.1 구현 작업 지시서

```text
DOCUMENT_NAME = cnt_v1.1_implementation_work_instruction_ko
PROJECT       = CNT
VERSION       = 1.1
DATE          = 2026-04-19
STATUS        = READY_FOR_IMPLEMENTATION
BASELINE      = CNT v1 (CLOSED)
REFERENCE     = cnt_v1.1_architecture_design
```

## 1. 목적

이 문서는 `CNT v1.1 ARCHITECTURE DESIGN DOCUMENT`를 실제 코드 변경 단위로 나눈
**CNT v1.1 구현 작업 지시서**다.

목적:

- `StrategySignal`과 실제 주문 실행을 분리
- `risk_guard`를 통해 운영 리스크 차단 레이어 추가
- `signal_logger`로 신호 관측성 확보
- v1 계약을 유지하면서 확장 레이어만 추가

## 2. 구현 원칙

### 2.1 v1 core 변경 금지

아래는 직접 변경하지 않는다.

- `StrategySignal` 핵심 계약
- `ExitModel` 기본 stop/target 동작
- `engine -> entry_gate -> strategy_manager` 기본 흐름
- `state schema_version=1.0`

### 2.2 레이어 추가 방식

v1.1은 아래를 추가한다.

```text
signal_logger
execution_decider
risk_guard
ExecutionDecision
enhanced_exit_manager (Stage 2)
```

### 2.3 단계별 구현

- **Stage 1**: 필수 구현
- **Stage 2**: 청산 확장 구현

## 3. 구현 범위

### 3.1 Stage 1

1. `src/strategy_signal.py` legacy wrapper 제거
2. `src/models/execution_decision.py` 추가
3. `src/models/risk_result.py` 추가
4. `src/execution_decider.py` 추가
5. `src/risk/risk_guard.py` 추가
6. `src/signal_logger.py` 추가
7. `src/strategy_manager.py`에 signal_logger 연결
8. `src/engine.py`에 ExecutionDecision 연결
9. state에 `risk_metrics` optional 구조 추가

### 3.2 Stage 2

10. `src/risk/enhanced_exit_manager.py` 추가
11. trailing stop 판단 추가
12. time-based exit 판단 추가
13. partial exit 판단 추가

## 4. 파일 변경 계획

### 신규 생성 파일

```text
src/models/execution_decision.py
src/models/risk_result.py
src/execution_decider.py
src/risk/risk_guard.py
src/signal_logger.py
```

Stage 2 예정:

```text
src/risk/enhanced_exit_manager.py
```

### 수정 파일

```text
src/engine.py
src/strategy_manager.py
src/entry_gate.py
src/models/strategy_signal.py
config.py
AGENTS.md
docs/EXTRA ITEMS REGISTER.md
```

### 제거 파일

```text
src/strategy_signal.py
```

## 5. Stage 1 주요 작업

### T1. legacy wrapper 제거 준비

대상:

- `src/strategy_signal.py`

완료 조건:

- 참조 0건
- `py_compile` 통과
- 이후 파일 제거 가능

### T2. ExecutionDecision 모델 추가

목적:

- 신호와 실제 주문 실행 분리
- 엔진이 이 모델을 보고 주문 여부를 결정

### T3. RiskCheckResult 모델 추가

목적:

- risk_guard 판단 결과를 구조화

### T4. risk_guard 추가

입력:

- `StrategySignal`
- `state`
- `balance`

출력:

- `RiskCheckResult`

## 최종 의미

이 지시서는 CNT v1 위에 안정적으로 v1.1 레이어를 얹기 위한 작업 단위 정의서다.

## 링크

- CNT v1.1 IMPLEMENTATION WORK INSTRUCTION
- CNT v1.1 ARCHITECTURE DESIGN DOCUMENT KO
- CNT v1.1 IMPLEMENTATION VALIDATION CHECKLIST KO

## Obsidian Links

- [[CNT v1.1 ARCHITECTURE DESIGN DOCUMENT KO]]



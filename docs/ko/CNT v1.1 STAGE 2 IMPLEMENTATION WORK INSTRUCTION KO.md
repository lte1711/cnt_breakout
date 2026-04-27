---
tags:
  - cnt
  - type/documentation
  - status/active
  - context-filter
  - type/validation
  - risk
  - cnt-v1.1-stage-2-implementation-work-instruction-ko
---

# CNT v1.1 Stage 2 구현 작업 지시서

```text
DOCUMENT_NAME = cnt_v1.1_stage2_implementation_work_instruction_ko
PROJECT       = CNT
VERSION       = 1.1
STAGE         = 2
DATE          = 2026-04-19
STATUS        = READY_FOR_IMPLEMENTATION
BASELINE      = CNT v1.1 Stage 1 (CLOSED)
REFERENCE_1   = cnt_v1.1_stage2_architecture_design
REFERENCE_2   = cnt_v1.1_implementation_validation_checklist
```

## 1. 목적

이 문서는 CNT v1.1 Stage 2의 청산(Exit) 확장 기능을 실제 코드 변경 단위로 구현하기 위한 작업 지시서다.

목표:

- trailing stop 도입
- time-based exit 도입
- partial exit 도입
- 기존 v1 / v1.1 Stage 1 구조를 유지한 상태에서 확장

## 2. 구현 원칙

### 2.1 v1 / Stage 1 계약 보호

변경하지 않는 것:

- `StrategySignal`
- `ExecutionDecision`
- entry 흐름 (`engine -> entry_gate -> execution_decider`)
- 기존 stop/target 동작
- state schema_version=1.0

### 2.2 판단과 실행 분리

```text
Exit 판단 = enhanced_exit_manager
Exit 실행 = engine 기존 SELL 경로
```

### 2.3 상태 기반 처리

모든 exit 판단은 아래를 기준으로 한다.

```text
open_trade + state + current_price
```

### 2.4 단계별 구현

```text
1. trailing stop
2. time exit
3. partial exit
```

## 3. 구현 범위

필수:

- ExitSignal 모델
- enhanced_exit_manager
- trailing stop
- time exit
- partial exit
- engine exit 연결
- state 확장

제외:

- 신규 entry 신호 추가
- entry flow 변경
- execution_decider 구조 재설계

## 4. 파일 변경 계획

### 신규 파일

```text
src/models/exit_signal.py
src/risk/enhanced_exit_manager.py
```

### 수정 파일

```text
src/engine.py
src/state_writer.py
src/order_validator.py
config.py
AGENTS.md
docs/EXTRA ITEMS REGISTER.md
```

## 5. 구현 작업

### T1. ExitSignal 모델 추가

필수 필드:

- `should_exit`
- `exit_type`
- `reason`
- `target_price`
- `stop_price`
- `partial_qty`

### T2. enhanced_exit_manager skeleton

핵심 구조:

```python
def evaluate_exit(open_trade, current_price, state, filters):
    # 1. stop
    # 2. trailing
    # 3. target
    # 4. partial
    # 5. time exit
```

### T3. STOP 로직 유지

### T4. TRAILING STOP 구현

state 확장:

```json
{
  "highest_price_since_entry": float
}
```

로직:

- entry 이후 최고가 갱신
- trailing_price 계산
- 현재가가 trailing_price 이하이면 exit

### T5. TIME EXIT 구현

기준:

- `entry_time`
- `time_based_exit_minutes`

## 최종 의미

이 문서는 Stage 2 청산 확장을 실제 코드 작업 단위로 쪼갠 지시서다.

## 링크

- CNT v1.1 STAGE 2 IMPLEMENTATION WORK INSTRUCTION
- CNT v1.1 STAGE 2 ARCHITECTURE DESIGN DOCUMENT KO
- CNT v1.1 STAGE 2 IMPLEMENTATION VALIDATION CHECKLIST KO

## Obsidian Links

- [[CNT v1.1 ARCHITECTURE DESIGN DOCUMENT KO]]



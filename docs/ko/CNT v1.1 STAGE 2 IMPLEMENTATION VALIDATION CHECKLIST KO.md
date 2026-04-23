---
tags:
  - cnt
  - docs
  - validation
  - instruction
  - v1
  - ko
aliases:
  - CNT v1.1 STAGE 2 IMPLEMENTATION VALIDATION CHECKLIST KO
---

# CNT v1.1 Stage 2 구현 검증 체크리스트

```text
DOCUMENT_NAME = cnt_v1.1_stage2_implementation_validation_checklist_ko
PROJECT       = CNT
VERSION       = 1.1
STAGE         = 2
DATE          = 2026-04-19
STATUS        = VALIDATION_READY
BASELINE      = CNT v1.1 Stage 1 (CLOSED)
REFERENCE_1   = cnt_v1.1_stage2_architecture_design
REFERENCE_2   = cnt_v1.1_stage2_implementation_work_instruction
```

## 1. 목적

이 문서는 CNT v1.1 Stage 2 구현 결과를 검증하기 위한 체크리스트다.

검증 목적:

- trailing stop, time exit, partial exit가 설계대로 동작하는지 확인
- 기존 v1 / v1.1 Stage 1 기능에 손상이 없는지 확인
- 판단 레이어와 실행 레이어가 분리되어 있는지 확인
- 상태 저장과 복원이 확장된 청산 모델까지 포함해 정상 동작하는지 확인

## 2. 검증 원칙

### 2.1 기존 구조 훼손 금지

유지 대상:

- `StrategySignal`
- `ExecutionDecision`
- `engine -> entry_gate -> execution_decider`
- 기존 stop/target 경로
- state schema_version=1.0

### 2.2 판단과 실행 분리 유지

```text
enhanced_exit_manager = 판단만 수행
engine = 실제 SELL 실행
```

### 2.3 상태 기반 검증

포함해야 할 state 필드:

- `highest_price_since_entry`
- `entry_time`
- `partial_exit_progress`

### 2.4 forced BUY 금지

검증 중에는 forced BUY를 하지 않고,
synthetic open_trade/state 조합으로 exit 판단만 검증한다.

## 3. 검증 범위

포함:

- ExitSignal 모델
- enhanced_exit_manager
- trailing stop
- time exit
- partial exit
- engine exit 연결
- state 확장
- filter 처리
- 회귀 검증

제외:

- 신규 entry 신호 추가
- entry flow 변경
- execution_decider 재설계

## 4. 문서 및 구조 검증

### A1. 문서 존재 확인

대상:

- `docs/CNT v1.1 STAGE 2 ARCHITECTURE DESIGN DOCUMENT.md`
- `docs/CNT v1.1 STAGE 2 IMPLEMENTATION WORK INSTRUCTION.md`
- `docs/CNT v1.1 STAGE 2 IMPLEMENTATION VALIDATION CHECKLIST.md`

### A2. AGENTS.md 반영 확인

확인 항목:

- `ExitSignal`
- `enhanced_exit_manager`
- `highest_price_since_entry`
- `entry_time`
- `partial_exit_progress`

### A3. EXTRA ITEMS REGISTER 반영 확인

신규 대상:

- `src/models/exit_signal.py`
- `src/risk/enhanced_exit_manager.py`

## 5. 파일 및 인터페이스 검증

### B1. ExitSignal 모델 확인

필수 필드:

- `should_exit`
- `exit_type`
- `reason`
- `target_price`
- `stop_price`
- `partial_qty`

### B2. enhanced_exit_manager 함수 확인

필수 함수:

```python
evaluate_exit(open_trade, current_price, state, filters)
```

## 6. Exit Flow 검증

기대 흐름:

```text
open_trade
-> enhanced_exit_manager.evaluate_exit(...)
-> ExitSignal
-> engine 기존 SELL 경로
```

## 7. Trailing Stop 검증

중점:

- `highest_price_since_entry` 사용 여부
- trailing_price 계산
- 기존 protective stop branch 재사용 여부

## 최종 의미

이 문서는 Stage 2의 청산 확장 기능이 기존 실행 구조를 깨지 않고 동작하는지 확인하는 기준 체크리스트다.

## 링크

- [[CNT v1.1 STAGE 2 IMPLEMENTATION VALIDATION CHECKLIST]]
- [[CNT v1.1 STAGE 2 IMPLEMENTATION VALIDATION REPORT KO]]
- [[CNT v1.1 STAGE 2 ARCHITECTURE DESIGN DOCUMENT KO]]

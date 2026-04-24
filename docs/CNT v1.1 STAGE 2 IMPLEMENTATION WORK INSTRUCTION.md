---
aliases:
  - CNT v1.1 STAGE 2 IMPLEMENTATION WORK INSTRUCTION
---

﻿# CNT v1.1 STAGE 2 IMPLEMENTATION WORK INSTRUCTION

```text
DOCUMENT_NAME = cnt_v1.1_stage2_implementation_work_instruction
PROJECT       = CNT
VERSION       = 1.1
STAGE         = 2
DATE          = 2026-04-19
STATUS        = READY_FOR_IMPLEMENTATION
BASELINE      = CNT v1.1 Stage 1 (CLOSED)
REFERENCE_1   = cnt_v1.1_stage2_architecture_design
REFERENCE_2   = cnt_v1.1_implementation_validation_checklist
```

---

# 1. PURPOSE

본 문서는 CNT v1.1 Stage 2의 청산(Exit) 확장 기능을 실제 코드 수준으로 구현하기 위한
**구현 작업지시서**다.

목표:

* trailing stop 도입
* time-based exit 도입
* partial exit 도입
* 기존 v1/v1.1 Stage 1 구조를 유지한 상태에서 확장

---

# 2. IMPLEMENTATION PRINCIPLES

---

## 2.1 v1 / Stage 1 계약 보호

다음은 절대 변경하지 않는다.

* `StrategySignal`
* `ExecutionDecision`
* entry 흐름 (`engine → entry_gate → execution_decider`)
* 기존 stop/target 동작
* state schema_version=1.0

---

## 2.2 판단과 실행 분리

```text
Exit 판단 = enhanced_exit_manager
Exit 실행 = engine 기존 SELL 경로
```

---

## 2.3 상태 기반 처리

모든 exit 판단은:

```text
open_trade + state + current_price
```

기반으로 수행한다.

---

## 2.4 단계별 구현

Stage 2는 다음 순서로 구현한다.

```text
1. trailing stop
2. time exit
3. partial exit
```

---

# 3. IMPLEMENTATION SCOPE

---

## 필수 구현

* ExitSignal 모델
* enhanced_exit_manager
* trailing stop
* time exit
* partial exit
* engine exit 연결
* state 확장

---

## 제외 항목

* 전략 로직 변경
* 엔트리 흐름 변경
* order executor 구조 변경

---

# 4. FILE CHANGE PLAN

---

## 4.1 신규 파일

```text
src/models/exit_signal.py
src/risk/enhanced_exit_manager.py
```

---

## 4.2 수정 파일

```text
src/engine.py
src/state_writer.py
src/order_validator.py (partial qty 검증)
config.py
AGENTS.md
docs/EXTRA ITEMS REGISTER.md
```

---

# 5. STAGE 2 IMPLEMENTATION TASKS

---

## T1. ExitSignal 모델 추가

### 파일

```text
src/models/exit_signal.py
```

### 구현

```python
from dataclasses import dataclass


@dataclass
class ExitSignal:
    should_exit: bool
    exit_type: str

    reason: str

    target_price: float | None
    stop_price: float | None

    partial_qty: float | None
```

---

## T2. enhanced_exit_manager skeleton

### 파일

```text
src/risk/enhanced_exit_manager.py
```

### 구조

```python
def evaluate_exit(open_trade, current_price, state, filters):
    # 1. stop
    # 2. trailing
    # 3. target
    # 4. partial
    # 5. time exit
```

---

## T3. STOP 로직 유지

### 규칙

```python
if current_price <= open_trade["stop_price"]:
    return ExitSignal(True, "STOP", ...)
```

---

## T4. TRAILING STOP 구현

---

### state 확장

```json
{
  "highest_price_since_entry": float
}
```

---

### 로직

```python
highest = max(previous_highest, current_price)

trailing_price = highest * (1 - trailing_stop_pct)

if current_price <= trailing_price:
    exit
```

---

### 작업 항목

* entry 시 highest 초기화
* 매 tick마다 highest 업데이트
* state 저장

---

## T5. TIME EXIT 구현

---

### state

```json
{
  "entry_time": timestamp
}
```

---

### 로직

```python
elapsed_minutes = now - entry_time

if elapsed_minutes >= time_based_exit_minutes:
    exit
```

---

## T6. PARTIAL EXIT 구현

---

### 전략 입력

```python
exit_model.partial_exit_levels
```

---

### 수량 계산

```python
raw_qty = entry_qty * ratio

adjusted_qty = floor(raw_qty / step_size) * step_size
```

---

### 필터 조건

```python
if adjusted_qty < min_qty:
    partial skip
```

---

### 작업 항목

* partial_qty 계산
* filter 적용
* ExitSignal 반환

---

## T7. engine 연결

---

### 기존

```python
should_exit_long()
should_stop()
```

---

### 변경

```python
exit_signal = evaluate_exit(...)

if exit_signal.should_exit:
    기존 SELL 경로 실행
```

---

### 규칙

* SELL LIMIT / MARKET 그대로 사용
* exit_type에 따라 분기

---

## T8. state 확장 구현

---

### 추가 필드

```json
{
  "highest_price_since_entry": float,
  "entry_time": timestamp
}
```

---

### lifecycle

* entry 시 생성
* 유지 중 업데이트
* exit 시 삭제

---

## T9. partial qty validator 반영

---

### 대상

```text
src/order_validator.py
```

### 규칙 추가

```python
if qty < min_qty:
    reject
```

---

## T10. config 확장

---

```python
TRAILING_STOP_PCT = 0.01
TIME_EXIT_MINUTES = 240
ENABLE_PARTIAL_EXIT = True
```

---

## T11. 문서 갱신

---

### AGENTS.md

* enhanced_exit_manager 추가
* ExitSignal 추가

---

### EXTRA ITEMS REGISTER

* 신규 파일 등록

---

# 6. VALIDATION REQUIREMENTS

---

## 6.1 trailing stop

* 최고가 업데이트 정상
* 조건 충족 시 exit 발생

---

## 6.2 time exit

* 시간 초과 시 exit

---

## 6.3 partial exit

* qty filter 통과
* min_qty 미만 시 skip

---

## 6.4 회귀 테스트

* 기존 stop 정상 동작
* 기존 target 정상 동작
* state 복원 정상
* execution 흐름 정상

---

# 7. IMPLEMENTATION ORDER

---

```text
1. ExitSignal 추가
2. enhanced_exit_manager skeleton
3. trailing stop
4. time exit
5. partial exit
6. engine 연결
7. state 확장
8. validator 반영
9. config 추가
10. 문서 갱신
11. 전체 검증
```

---

# 8. FAILURE CONDITIONS

---

## CRITICAL

* exit 판단이 실행 로직을 직접 호출
* partial exit가 filter 미검증
* 기존 stop/target 깨짐
* state 손상

---

## MINOR

* 로그 누락
* 문서 미갱신

---

# 9. COMPLETION CRITERIA

---

```text
- trailing stop 정상 동작
- time exit 정상 동작
- partial exit 정상 동작
- 기존 기능 회귀 없음
- compile / runtime 검증 통과
```

---

# 10. FINAL STATEMENT

```text
Stage 2는 엔진을 바꾸는 작업이 아니다.
청산의 품질을 높이는 작업이다.
```

---

# 결론

> **CNT v1.1 Stage 2 구현은 “지능형 청산 레이어”를 추가하는 작업이며, 기존 안정된 구조 위에서 안전하게 확장해야 한다.**

---

---

## Obsidian Links

- [[CNT v1.1 ARCHITECTURE DESIGN DOCUMENT]]


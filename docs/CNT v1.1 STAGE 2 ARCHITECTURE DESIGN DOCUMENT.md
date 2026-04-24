---
aliases:
  - CNT v1.1 STAGE 2 ARCHITECTURE DESIGN DOCUMENT
---

# CNT v1.1 STAGE 2 ARCHITECTURE DESIGN DOCUMENT

```text
DOCUMENT_NAME = cnt_v1.1_stage2_architecture_design
PROJECT       = CNT
VERSION       = 1.1
STAGE         = 2
DATE          = 2026-04-19
STATUS        = DESIGN_FINALIZED
BASELINE      = CNT v1.1 Stage 1 (CLOSED)
REFERENCE_1   = cnt_v1.1_architecture_design
REFERENCE_2   = cnt_v1.1_implementation_work_instruction
REFERENCE_3   = cnt_v1.1_implementation_validation_checklist
```

---

# 1. PURPOSE

본 문서는 CNT v1.1 Stage 2에서 도입되는 **청산(Exit) 확장 아키텍처**를 정의한다.

Stage 2의 목적:

* 고정 stop/target 구조를 확장한다
* 수익 보호 능력을 강화한다
* 시장 상황에 따른 유연한 청산을 가능하게 한다
* v1 및 Stage 1 구조를 유지하면서 확장한다

---

# 2. DESIGN PRINCIPLES

---

## 2.1 v1 및 Stage 1 계약 유지

다음은 변경하지 않는다.

* `StrategySignal` 구조
* `ExecutionDecision` 구조
* `engine → entry_gate → execution_decider` 흐름
* 기존 stop/target 집행 방식
* `state schema_version = 1.0`

---

## 2.2 판단과 집행 분리 유지

```text
판단 = enhanced_exit_manager
집행 = 기존 engine SELL / STOP 경로
```

---

## 2.3 상태 기반 설계

모든 Exit 판단은:

```text
open_trade + state + current_price
```

기반으로 수행한다.

---

## 2.4 점진적 확장

Exit 기능은 다음 순서로 확장한다.

```text
1. trailing stop
2. time-based exit
3. partial exit
```

---

# 3. ARCHITECTURE OVERVIEW

---

## 3.1 기존 구조 (Stage 1)

```text
open_trade
→ should_exit_long()
→ should_stop()
→ SELL LIMIT / SELL MARKET
```

---

## 3.2 Stage 2 구조

```text
open_trade
→ enhanced_exit_manager.evaluate_exit(...)
→ ExitSignal
→ engine existing execution path
```

---

## 3.3 핵심 원칙

```text
Exit 판단 로직만 교체
주문 실행 로직은 그대로 유지
```

---

# 4. NEW COMPONENTS

---

## 4.1 ExitSignal 모델

```python
from dataclasses import dataclass


@dataclass
class ExitSignal:
    should_exit: bool
    exit_type: str   # TARGET / STOP / TRAILING_STOP / TIME_EXIT / PARTIAL
    reason: str

    target_price: float | None
    stop_price: float | None

    partial_qty: float | None
```

---

## 4.2 PartialExitLevel 모델

```python
from dataclasses import dataclass


@dataclass
class PartialExitLevel:
    qty_ratio: float
    target_price: float
```

---

## 4.3 enhanced_exit_manager

### 파일

```text
src/risk/enhanced_exit_manager.py
```

### 공개 함수

```python
def evaluate_exit(open_trade, current_price, state, filters) -> ExitSignal:
    ...
```

---

# 5. EXIT LOGIC DESIGN

---

## 5.1 기본 우선순위

Exit 판단은 다음 순서로 평가한다.

```text
1. STOP (손절)
2. TRAILING STOP
3. TARGET
4. PARTIAL EXIT
5. TIME EXIT
```

---

## 5.2 STOP (기존 유지)

```text
if current_price <= stop_price:
    exit_type = STOP
```

---

## 5.3 TARGET (기존 유지)

```text
if current_price >= target_price:
    exit_type = TARGET
```

---

## 5.4 TRAILING STOP

---

### 필요 state 확장

```json
{
  "highest_price_since_entry": 0.0
}
```

---

### 로직

```text
1. entry 이후 최고가 갱신
2. trailing 기준 계산

trailing_price = highest_price * (1 - trailing_stop_pct)

3. 현재가가 trailing_price 이하 → exit
```

---

### 예시

```text
entry = 100
highest = 105
trailing_pct = 0.02

trailing_price = 102.9

현재가 <= 102.9 → exit
```

---

## 5.5 TIME-BASED EXIT

---

### 필요 state

```json
{
  "entry_time": "2026-04-19 14:20:00"
}
```

---

### 로직

```text
holding_minutes = now - entry_time

if holding_minutes >= time_based_exit_minutes:
    exit
```

---

## 5.6 PARTIAL EXIT

---

### 전략에서 제공

```python
exit_model.partial_exit_levels = [
    {"qty_ratio": 0.5, "target_price": 1.003},
]
```

---

### 수량 계산 규칙

```text
raw_qty = entry_qty * qty_ratio

adjusted_qty =
    floor(raw_qty / step_size) * step_size
```

---

### 필터 규칙

```text
if adjusted_qty < min_qty:
    partial exit 금지
    → skip 또는 full exit fallback
```

---

### 중요 원칙

```text
partial exit는 반드시 filter 통과 수량만 제출
```

---

# 6. STATE EXTENSIONS

---

## 6.1 open_trade 확장

```json
{
  "highest_price_since_entry": 0.0,
  "entry_time": "timestamp"
}
```

---

## 6.2 관리 규칙

* entry 시 초기화
* price 업데이트 시 최고가 갱신
* exit 시 제거

---

# 7. ENGINE INTEGRATION

---

## 7.1 기존 엔진 유지

기존 함수 유지:

* SELL LIMIT (target)
* SELL MARKET (stop)

---

## 7.2 Stage 2 연결

```text
if open_trade:
    exit_signal = enhanced_exit_manager.evaluate_exit(...)

    if exit_signal.should_exit:
        기존 SELL 경로 호출
```

---

## 7.3 partial exit 처리

```text
if exit_type == PARTIAL:
    SELL LIMIT (partial_qty)
```

---

# 8. CONFIG EXTENSIONS

---

## 8.1 추가 파라미터

```python
TRAILING_STOP_PCT = 0.01
TIME_EXIT_MINUTES = 240
ENABLE_PARTIAL_EXIT = True
```

---

## 8.2 전략 파라미터 연동

각 전략은:

```python
exit_model.trailing_stop_pct
exit_model.partial_exit_levels
exit_model.time_based_exit_minutes
```

를 선택적으로 제공한다.

---

# 9. VALIDATION RULES

---

## 9.1 trailing stop 검증

* 최고가 추적 정상
* trailing 조건 충족 시 exit

---

## 9.2 time exit 검증

* 시간 초과 시 exit

---

## 9.3 partial exit 검증

* qty filter 통과
* min_qty 미만 시 fallback

---

## 9.4 회귀 검증

다음은 절대 깨지면 안 된다.

* 기존 stop/target
* state 복원
* order validation
* execution flow

---

# 10. PROHIBITIONS

---

다음은 금지한다.

```text
enhanced_exit_manager가 직접 주문을 보내는 것
partial exit가 filter 검증 없이 실행되는 것
state 없이 trailing 계산하는 것
engine exit 경로를 완전히 교체하는 것
```

---

# 11. IMPLEMENTATION ORDER

---

```text
1. ExitSignal 모델 추가
2. enhanced_exit_manager skeleton 작성
3. trailing stop 구현
4. time exit 구현
5. partial exit 구현
6. engine 연결
7. state 확장
8. 검증
```

---

# 12. FINAL STATEMENT

CNT v1.1 Stage 2는 전략 자체를 바꾸는 작업이 아니다.

```text
목표:
수익을 지키고,
손실을 줄이며,
청산의 질을 높이는 것
```

---

# 결론

> **CNT v1.1 Stage 2는 기존 안정된 구조 위에 “지능형 청산 레이어”를 추가하는 확장 단계다.**

---

---

## Obsidian Links

- [[CNT v1.1 ARCHITECTURE DESIGN DOCUMENT]]


---
tags:
  - cnt
  - type/documentation
  - status/active
  - market-context
  - context-filter
  - risk
  - cnt-v1.1-stage-2-architecture-design-document-ko
---

# CNT v1.1 Stage 2 아키텍처 설계 문서

```text
DOCUMENT_NAME = cnt_v1.1_stage2_architecture_design_ko
PROJECT       = CNT
VERSION       = 1.1
STAGE         = 2
DATE          = 2026-04-19
STATUS        = DESIGN_FINALIZED
BASELINE      = CNT v1.1 Stage 1 (CLOSED)
```

## 1. 목적

이 문서는 CNT v1.1 Stage 2에서 도입되는 **청산(Exit) 확장 아키텍처**를 정의한다.

Stage 2 목적:

- 고정 stop/target 구조를 확장
- 수익 보호 능력 강화
- 시장 상황에 따른 유연한 청산 가능
- v1 및 Stage 1 구조를 유지한 채 확장

## 2. 설계 원칙

### 2.1 v1 및 Stage 1 계약 유지

변경하지 않는 것:

- `StrategySignal`
- `ExecutionDecision`
- `engine -> entry_gate -> execution_decider` 흐름
- 기존 stop/target 집행 방식
- `state schema_version = 1.0`

### 2.2 판단과 실행 분리 유지

```text
판단 = enhanced_exit_manager
실행 = 기존 engine SELL / STOP 경로
```

### 2.3 상태 기반 설계

모든 Exit 판단은 아래 기반으로 수행한다.

```text
open_trade + state + current_price
```

### 2.4 확장은 단계적으로

```text
1. trailing stop
2. time-based exit
3. partial exit
```

## 3. 아키텍처 개요

### 3.1 기존 구조 (Stage 1)

```text
open_trade
-> should_exit_long()
-> should_stop()
-> SELL LIMIT / SELL MARKET
```

### 3.2 Stage 2 구조

```text
open_trade
-> enhanced_exit_manager.evaluate_exit(...)
-> ExitSignal
-> engine existing execution path
```

### 3.3 핵심 유지점

```text
Exit 판단 로직만 교체
주문 실행 로직은 그대로 유지
```

## 4. 신규 구성요소

### 4.1 ExitSignal 모델

핵심 필드:

- `should_exit`
- `exit_type`
- `reason`
- `target_price`
- `stop_price`
- `partial_qty`

### 4.2 PartialExitLevel 모델

필드:

- `qty_ratio`
- `target_price`

### 4.3 enhanced_exit_manager

파일:

- `src/risk/enhanced_exit_manager.py`

공개 함수:

```python
evaluate_exit(open_trade, current_price, state, filters) -> ExitSignal
```

## 5. Exit Logic 설계

### 5.1 기본 우선순위

```text
1. STOP
2. TRAILING STOP
3. TARGET
4. PARTIAL EXIT
5. TIME EXIT
```

### 5.2 STOP

```text
if current_price <= stop_price:
    exit_type = STOP
```

### 5.3 TARGET

```text
if current_price >= target_price:
    exit_type = TARGET
```

### 5.4 TRAILING STOP

필요한 state 확장:

```json
{
  "highest_price_since_entry": 0.0
}
```

로직:

```text
1. entry 이후 최고가 갱신
2. trailing 기준 계산
3. 현재가가 trailing_price 이하가 되면 exit
```

## 최종 의미

Stage 2는 청산 판단 레이어만 확장하고, 기존 엔진 실행 경로는 유지하는 보수적 확장 설계다.

## 링크

- CNT v1.1 STAGE 2 ARCHITECTURE DESIGN DOCUMENT
- CNT v1.1 STAGE 2 IMPLEMENTATION WORK INSTRUCTION KO
- CNT v1.1 STAGE 2 IMPLEMENTATION VALIDATION REPORT KO

## Obsidian Links

- [[CNT v1.1 ARCHITECTURE DESIGN DOCUMENT KO]]



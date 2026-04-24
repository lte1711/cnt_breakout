---
tags:
  - cnt
  - docs
  - v2
aliases:
  - CNT v2 ARCHITECTURE DESIGN DOCUMENT KO
---

# CNT v2 ARCHITECTURE DESIGN DOCUMENT KO

```text
DOCUMENT_NAME = cnt_v2_architecture_design_ko
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-19
STATUS        = DESIGN_FINALIZED
BASELINE      = CNT v1.1 (CLOSED)
```

## 1. 목적

이 문서는 CNT v2의 상위 아키텍처를 정의한다.

CNT v2의 목표는 다음과 같다.

- 단일 전략 엔진을 멀티 전략 엔진으로 확장
- 단일 포지션 제어를 포트폴리오 수준 노출/리스크 제어로 확장
- Spot Testnet 중심 구조를 Spot/Futures 공용 프레임워크로 확장
- 신호, 실행, 리스크, 청산을 전략별/계정별/시장별로 계층화
- 운영 자동화와 관측성, 검증 체계를 유지 가능한 형태로 정렬

## 2. 설계 원칙

### 2.1 v1.1 코어 보존

v2에서도 다음 구성 요소는 핵심 기반으로 유지한다.

- `StrategySignal`
- `ExecutionDecision`
- `ExitSignal`
- `strategy_manager`
- `execution_decider`
- `risk_guard`
- `enhanced_exit_manager`

### 2.2 포트폴리오 엔진으로 승격

```text
single strategy engine
-> multi-strategy engine
-> portfolio orchestration engine
```

### 2.3 신호/실행/리스크/상태 분리

- 전략 계층
- 실행 계층
- 리스크 계층
- 포트폴리오 계층
- 계정/시장 계층

### 2.4 Spot/Futures 차이는 실행 계층 차이로 처리

```text
같은 전략 평가 구조
+ 다른 market adapter
+ 다른 risk / execution rules
```

### 2.5 상태와 로그의 포트폴리오 단위 확장

- `portfolio_state`
- `position_state`

## 3. 목표 기능

- 멀티 전략: breakout / pullback / mean reversion
- 멀티 종목: ETHUSDT / BTCUSDT
- 멀티 마켓: Binance Spot / Binance Futures
- 포트폴리오 리스크:
  - 총 노출 제한
  - 종목별 노출 제한
  - 전략별 노출 제한
  - 계정별 일일 손실 제한
- 실행 우선순위:
  - 여러 전략 신호 충돌 시 점수 기반 선택
  - 동시 실행 가능 여부 판단

## 4. 아키텍처 개요

### v1.1 구조

```text
engine
  -> entry_gate
    -> strategy_manager
      -> strategy
    -> execution_decider
      -> risk_guard
  -> enhanced_exit_manager
```

### v2 목표 구조

```text
portfolio_engine
  -> market_universe_manager
  -> strategy_orchestrator
      -> strategy_manager
          -> strategy_registry
              -> strategy instances
      -> signal_router
      -> signal_ranker
  -> execution_orchestrator
      -> execution_decider
      -> order_router
      -> market_adapter
  -> portfolio_risk_manager
      -> account_risk_guard
      -> symbol_risk_guard
      -> strategy_risk_guard
  -> position_manager
      -> enhanced_exit_manager
  -> state_manager
  -> observability_manager
```

## 5. 요약

CNT v2는 단일 전략 엔진을 확장해 멀티 전략/멀티 종목/멀티 시장 구조를 수용하면서도, 실행과 리스크 및 상태 계층을 명확히 나누는 것을 목표로 한다.

## 링크

- [[CNT v2 ENGINE DECOMPOSITION DESIGN KO]]
- [[CNT v2 STRATEGIC ANALYSIS PLAN KO]]
- [[00 Docs Index KO]]

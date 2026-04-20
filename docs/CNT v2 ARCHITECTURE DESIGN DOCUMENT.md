---
tags:
  - cnt
  - docs
  - v2
aliases:
  - CNT v2 ARCHITECTURE DESIGN DOCUMENT
---

# CNT v2 ARCHITECTURE DESIGN DOCUMENT

```text
DOCUMENT_NAME = cnt_v2_architecture_design
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-19
STATUS        = DESIGN_FINALIZED
BASELINE      = CNT v1.1 (CLOSED)
```

---

# 1. PURPOSE

본 문서는 CNT v2의 상위 아키텍처를 정의한다.

CNT v2의 목표는 다음과 같다.

* 단일 전략 엔진을 **멀티 전략 엔진**으로 확장
* 단일 포지션 제어를 **포트폴리오/심볼 단위 리스크 제어**로 확장
* Spot Testnet 중심 구조를 **Spot/Futures 공용 프레임워크**로 확장
* 신호, 실행, 리스크, 청산을 **전략별/계정별/시장별로 계층화**
* 운영 자동화, 관측성, 검증 체계를 더 높은 수준으로 정형화

---

# 2. DESIGN PRINCIPLES

## 2.1 v1.1의 안정된 코어는 보존한다

다음은 v2에서도 핵심 기반으로 유지한다.

* `StrategySignal`
* `ExecutionDecision`
* `ExitSignal`
* `strategy_manager`
* `execution_decider`
* `risk_guard`
* `enhanced_exit_manager`

v2는 이들을 버리지 않고 **상위 오케스트레이션 레이어**를 추가한다.

---

## 2.2 단일 엔진에서 포트폴리오 엔진으로 승격한다

v1.1은 사실상 “한 전략 + 한 심볼 + 한 포지션” 엔진이다.
v2는 이를 다음처럼 확장한다.

```text
single strategy engine
→ multi-strategy engine
→ portfolio orchestration engine
```

---

## 2.3 전략, 실행, 리스크, 계정은 서로 독립 계층으로 나눈다

v2에서 반드시 분리할 계층:

* 전략 계층
* 실행 계층
* 리스크 계층
* 포트폴리오 계층
* 계정/시장 계층

---

## 2.4 Spot과 Futures는 “전략 차이”가 아니라 “시장 어댑터 차이”로 다룬다

즉:

```text
Spot strategy / Futures strategy
```

가 아니라,

```text
같은 전략 평가 구조
+ 다른 market adapter
+ 다른 risk / execution rules
```

로 설계한다.

---

## 2.5 상태와 로그는 포트폴리오 단위로 재정의한다

v1.1은 단일 state 중심이다.
v2는 다음 두 계층으로 나눈다.

* `portfolio_state`
* `position_state`

---

# 3. TARGET CAPABILITIES

CNT v2의 필수 목표 기능은 아래와 같다.

## 3.1 멀티 전략

* breakout
* pullback
* mean reversion
* 추후 전략 추가 가능

## 3.2 멀티 심볼

* ETHUSDT
* BTCUSDT
* 향후 심볼 확장 가능

## 3.3 멀티 마켓

* Binance Spot
* Binance Futures

## 3.4 포트폴리오 리스크

* 총 익스포저 제한
* 심볼별 익스포저 제한
* 전략별 익스포저 제한
* 계정별 일일 손실 제한

## 3.5 상위 실행 우선순위

* 여러 전략 신호 충돌 시 우선순위/점수 기반 선택
* 동시 실행 가능/불가 정책

---

# 4. ARCHITECTURE OVERVIEW

## 4.1 v1.1 구조

```text
engine
  -> entry_gate
    -> strategy_manager
      -> strategy
    -> execution_decider
      -> risk_guard
  -> enhanced_exit_manager
```

## 4.2 v2 구조

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

---

# 5. CORE LAYERS

## 5.1 Portfolio Engine

### 역할

v2의 최상위 런타임 오케스트레이터

### 책임

* 활성 심볼 순회
* 활성 전략 순회
* 신호 수집
* 신호 간 충돌 조정
* 포트폴리오 리스크 반영
* 실행 승인
* 상태/로그/메트릭 갱신

### 공개 함수 예시

```python
def run_portfolio_cycle() -> None:
    ...
```

---

## 5.2 Market Universe Manager

### 역할

거래 대상 universe 관리

### 책임

* 활성 심볼 목록 관리
* 심볼별 시장 타입(spot/futures) 관리
* 심볼별 거래 가능 여부 판단
* 심볼 메타데이터 캐시

### 예시

```python
ACTIVE_UNIVERSE = [
    {"symbol": "ETHUSDT", "market": "spot"},
    {"symbol": "BTCUSDT", "market": "spot"},
    {"symbol": "ETHUSDT", "market": "futures"},
]
```

---

## 5.3 Strategy Orchestrator

### 역할

전략 실행을 포트폴리오 단위로 조정

### 책임

* 각 전략별 `StrategySignal` 생성
* 동일 심볼에서 여러 전략 신호 수집
* 전략 신호 점수화/우선순위화
* 다전략 충돌 해소

### 구성 요소

* `strategy_manager`
* `signal_router`
* `signal_ranker`

---

## 5.4 Signal Ranker

### 목적

여러 전략이 동시에 BUY를 낼 때 어떤 신호를 채택할지 결정

### 입력

* 여러 `StrategySignal`

### 출력

* 채택 신호 1개 또는 N개
* reject 사유

### 평가 기준 예시

* `confidence`
* 시장 상태 적합성
* 최근 전략 성과
* 동일 심볼 기존 포지션 여부
* 포트폴리오 한도

---

## 5.5 Execution Orchestrator

### 역할

신호를 실제 주문 후보로 변환

### 책임

* `ExecutionDecision` 생성
* validation 호출
* order routing
* 시장별 adapter 호출

### 구성 요소

* `execution_decider`
* `order_router`
* `market_adapter`

---

## 5.6 Market Adapter Layer

### 목적

Spot/Futures 차이를 흡수

### 핵심 원칙

전략은 market type을 몰라도 된다.
실행과 데이터 수집 계층이 차이를 흡수한다.

### 분기 예시

```text
spot_adapter
futures_adapter
```

### 책임

* 주문 파라미터 차이 처리
* 포지션 정보 차이 처리
* 수수료/레버리지/펀딩비 차이 처리
* 계정 정보 차이 처리

---

## 5.7 Portfolio Risk Manager

### 역할

단일 포지션 리스크를 넘어 포트폴리오 전체 리스크를 관리

### 하위 구성

* `account_risk_guard`
* `symbol_risk_guard`
* `strategy_risk_guard`

### 책임

* 총 노출 한도
* 시장별 노출 한도
* 전략별 노출 한도
* 일일 손실 한도
* 손실 쿨다운
* 최대 동시 포지션 수

---

## 5.8 Position Manager

### 역할

열린 포지션들을 독립적으로 관리

### 책임

* 포지션별 stop/target 추적
* trailing/time/partial exit 적용
* 심볼별 포지션 lifecycle 관리
* Spot/Futures 포지션 상태 정규화

---

## 5.9 State Manager

### 역할

v2 상태 저장 구조를 관리

### 책임

* `portfolio_state`
* `positions`
* `risk_metrics`
* `strategy_metrics`

---

## 5.10 Observability Manager

### 역할

로그, 메트릭, 이벤트를 통합 관리

### 구성

* runtime log
* signal log
* portfolio decision log
* risk rejection log
* trade lifecycle log

---

# 6. DATA MODELS

## 6.1 StrategySignal

기본 구조 유지
단, v2에서는 아래 해석을 강화한다.

* `confidence`는 다전략 ranker 입력
* `strategy_name`은 전략 성과 추적 키
* `symbol` + `market` 조합으로 해석 필요

### 권장 확장 필드

```python
market_type: str  # SPOT / FUTURES
timeframe_profile: str | None
```

---

## 6.2 ExecutionDecision

v1.1 구조 유지, 단 포트폴리오 컨텍스트 추가 가능

### 권장 확장 필드

```python
portfolio_rejection_reason: str | None
selected_priority: int | None
```

---

## 6.3 ExitSignal

v1.1 구조 유지

### 권장 확장 필드

```python
position_id: str | None
market_type: str | None
```

---

## 6.4 PositionState

신규 핵심 모델

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

    trailing_stop_pct: float | None
    partial_exit_progress: int | None

    highest_price_since_entry: float | None

    side: str
    status: str
```

---

## 6.5 PortfolioState

```python
@dataclass
class PortfolioState:
    schema_version: str
    as_of_time: str

    cash_balance: float
    total_exposure: float
    total_unrealized_pnl: float

    daily_loss_count: int
    consecutive_losses: int

    open_positions: list[PositionState]
```

---

# 7. STRATEGY ARCHITECTURE

## 7.1 전략 레지스트리 확장

```text
breakout_v1
pullback_v1
mean_reversion_v1
```

## 7.2 전략 계약 유지

모든 전략은 여전히:

```python
evaluate(context) -> StrategySignal
```

## 7.3 전략별 파라미터 분리

```python
STRATEGY_PARAMS = {
    "breakout_v1": {...},
    "pullback_v1": {...},
    "mean_reversion_v1": {...},
}
```

---

# 8. MULTI-STRATEGY DECISION FLOW

```text
for each symbol:
    generate all candidate signals
    filter invalid/stale signals
    rank valid signals
    apply portfolio risk limits
    create execution decisions
    submit selected orders only
```

## 선택 정책 예시

### 정책 A: best signal only

가장 높은 점수의 1개만 채택

### 정책 B: one-per-symbol

심볼당 하나만 허용

### 정책 C: strategy diversification

서로 다른 전략은 동시 허용

v2 초기에는 **정책 B**가 가장 현실적이다.

---

# 9. SPOT / FUTURES EXTENSION

## 9.1 Spot

* 현 구조 거의 재사용 가능

## 9.2 Futures

추가 고려 요소:

* leverage
* margin mode
* liquidation risk
* funding rate
* position side
* unrealized pnl
* reduce-only / close-position flags

## 9.3 아키텍처 원칙

전략은 가능하면 시장 중립적으로 작성하고,
실행/리스크/포지션 계층에서 Spot/Futures 차이를 처리한다.

---

# 10. RISK ARCHITECTURE

## 10.1 Account Risk

* 일일 손실 한도
* 총 계정 손실 한도
* 총 노출 한도

## 10.2 Symbol Risk

* 심볼별 최대 노출
* 심볼별 동시 전략 제한

## 10.3 Strategy Risk

* 전략별 일일 손실
* 전략별 cooldown
* 전략별 max allocation

## 10.4 Futures Risk

* liquidation buffer
* leverage cap
* funding cost guard

---

# 11. STATE DESIGN

## 11.1 v2 상태 구조

```json
{
  "schema_version": "2.0",
  "portfolio_state": {...},
  "positions": [...],
  "risk_metrics": {...},
  "strategy_metrics": {...}
}
```

## 11.2 마이그레이션 원칙

* v1.1 state는 직접 덮어쓰지 않는다
* v2는 새 schema_version으로 분리
* 필요 시 migration adapter 작성

---

# 12. LOGGING AND OBSERVABILITY

## 12.1 로그 종류

* `runtime.log`
* `signal.log`
* `risk.log`
* `portfolio.log`
* `position.log`

## 12.2 핵심 메트릭

* strategy hit rate
* average hold time
* stop vs target ratio
* trailing capture ratio
* daily pnl
* rejected signal count
* rejected execution count

---

# 13. IMPLEMENTATION PHASES

## Phase 1

* 멀티 전략 레지스트리
* signal ranker
* one-per-symbol 정책
* portfolio state 도입

## Phase 2

* portfolio risk manager
* strategy metrics
* symbol risk
* multi-position state

## Phase 3

* futures adapter
* leverage/risk model
* futures-specific execution

## Phase 4

* performance analytics
* auto tuning inputs
* advanced monitoring

---

# 14. PROHIBITIONS

다음은 금지한다.

* v1.1 코어를 직접 파괴하는 전면 재작성
* strategy layer에 spot/futures 주문 규칙을 섞는 것
* risk 판단을 로그 파싱에 의존하는 것
* 포트폴리오 상태 없이 멀티 전략을 동시에 실행하는 것

---

# 15. COMPLETION CRITERIA

CNT v2 초기 완료 조건은 다음과 같다.

* 멀티 전략 후보 생성 가능
* 심볼당 단일 채택 정책 동작
* 포트폴리오 리스크 차단 동작
* PositionState / PortfolioState 저장 가능
* Spot/Futures adapter 분리 구조 존재
* 기존 v1.1 단일 전략 경로 회귀 없음

---

# 16. FINAL STATEMENT

CNT v2는 더 이상 단순한 전략 봇이 아니다.

> **CNT v2는 전략 엔진, 포트폴리오 엔진, 시장 어댑터, 리스크 계층을 통합한 거래 시스템 프레임워크다.**

---

# 결론

> **CNT v2의 본질은 “좋은 전략 하나”가 아니라, “여러 전략과 여러 시장을 안전하게 운영하는 상위 시스템”을 만드는 것이다.**

---

## Obsidian Links

- [[00 CNT Vault Home|Vault Home]]
- [[00 Docs Index|Docs Index]]

### Related
- [[00 Docs Index|Docs Index]]

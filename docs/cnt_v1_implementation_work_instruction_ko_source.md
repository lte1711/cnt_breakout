좋다. 아래는 **cnt 프로젝트용 구현 작업지시서 v1**이다.
목표는 앞서 확정한 **최종 전략 아키텍처 명세서 v1**를 실제 코드 변경 단위로 쪼개서, 바로 구현 가능한 형태로 만드는 것이다.

---

# cnt 프로젝트용 구현 작업지시서 v1

## 0. 작업 목표

현재 프로젝트를 아래 상태로 전환한다.

### 현재

```text
engine -> entry_gate -> strategy_signal(dict)
```

### 목표

```text
engine -> entry_gate -> strategy_manager -> breakout_v1(StrategySignal dataclass)
```

그리고 청산은 엔진 고정 퍼센트 방식에서 벗어나, **전략이 만든 `ExitModel`** 기반으로 집행되도록 바꾼다.

---

# 1. 구현 원칙

## 1.1 기존 엔진 기능은 유지

아래는 깨지면 안 된다.

* pending/open_trade 복원
* reconciliation
* 주문 검증
* 주문 제출
* stop market 보호 청산
* 상태 저장
* 로그 기록

## 1.2 한 번에 다 바꾸지 않는다

작업은 **점진적 마이그레이션**으로 진행한다.

## 1.3 각 단계마다 실행 가능 상태를 유지한다

각 단계 완료 후에도 최소한:

* import 에러 없음
* 엔진 실행 가능
* 테스트넷 기준 런타임 깨지지 않음

---

# 2. 작업 단위 개요

총 8개 작업으로 나눈다.

| 작업 | 제목                              | 우선순위  |
| -- | ------------------------------- | ----- |
| T1 | 전략 OFF 버그 수정                    | 🔴 즉시 |
| T2 | 공통 데이터 모델 추가                    | 🔴 즉시 |
| T3 | config 전략 파라미터 구조 개편            | 🔴 즉시 |
| T4 | 전략 베이스/레지스트리 추가                 | 🔴 즉시 |
| T5 | breakout_v1 전략 클래스 분리           | 🔴 즉시 |
| T6 | strategy_manager 추가 및 예외 격리     | 🔴 즉시 |
| T7 | entry_gate를 manager 기반으로 전환     | 🟠 1차 |
| T8 | engine 청산 로직을 ExitModel 기반으로 전환 | 🟠 1차 |

---

# 3. 작업 상세

---

## T1. 전략 OFF 버그 수정

### 목적

현재 `STRATEGY_ENABLED=False`일 때 진입 허용되는 버그를 제거한다.

### 대상 파일

* `src/entry_gate.py`

### 현재 문제

```python
if not STRATEGY_ENABLED:
    return "ENTRY_ALLOWED", "strategy_disabled"
```

### 수정 목표

```python
if not STRATEGY_ENABLED:
    return "NO_ENTRY_SIGNAL", "strategy_disabled"
```

### 완료 기준

* 전략 OFF면 진입 차단
* 엔진은 `NO_ENTRY_SIGNAL`로 종료

### 영향

* 가장 작은 수정
* 운영 안전성 즉시 상승

---

## T2. 공통 데이터 모델 추가

### 목적

전략 입력/출력/청산 모델을 표준화한다.

### 신규 파일

* `src/models/strategy_signal.py`
* `src/models/market_context.py`
* `src/risk/exit_models.py`

### 구현 항목

#### `src/risk/exit_models.py`

```python
from dataclasses import dataclass

@dataclass
class ExitModel:
    stop_price: float | None
    target_price: float | None
    trailing_stop_pct: float | None = None
    partial_exit_levels: list[dict] | None = None
    time_based_exit_minutes: int | None = None
```

#### `src/models/strategy_signal.py`

```python
from dataclasses import dataclass
from src.risk.exit_models import ExitModel

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

#### `src/models/market_context.py`

```python
from dataclasses import dataclass

@dataclass
class MarketContext:
    symbol: str
    primary_interval: str
    entry_interval: str
    klines_primary: list[dict]
    klines_entry: list[dict]
    last_price: float
    funding_rate: float | None = None
    open_interest: float | None = None
    long_short_ratio: float | None = None
    orderbook_imbalance: float | None = None
```

### 완료 기준

* import 가능
* syntax error 없음
* 아직 엔진과 연결 안 돼도 됨

---

## T3. config 전략 파라미터 구조 개편

### 목적

전역 상수형 전략 파라미터를 전략별 묶음 구조로 승격한다.

### 대상 파일

* `config.py`

### 추가 항목

```python
ACTIVE_STRATEGY = "breakout_v1"

STRATEGY_PARAMS = {
    "breakout_v1": {
        "ema_fast_period": 9,
        "ema_slow_period": 20,
        "rsi_period": 14,
        "atr_period": 14,
        "ema_gap_threshold": 0.001,
        "atr_expansion_multiplier": 1.2,
        "rsi_threshold": 55,
        "rsi_overheat": 75,
        "breakout_lookback": 3,
        "target_pct": 0.002,
        "stop_loss_pct": 0.0015,
        "signal_age_limit_sec": 15,
    }
}
```

### 유지 항목

기존 전역 상수는 **즉시 삭제하지 말고** 1단계에서는 남겨도 된다.
이유는 기존 `strategy_signal.py`가 아직 참조 중일 수 있기 때문이다.

### 완료 기준

* `ACTIVE_STRATEGY` 추가
* `STRATEGY_PARAMS` 추가
* 기존 코드 호환 유지

---

## T4. 전략 베이스/레지스트리 추가

### 목적

전략 클래스 체계를 도입한다.

### 신규 파일

* `src/strategies/base.py`
* `src/strategy_registry.py`

### 구현 항목

#### `src/strategies/base.py`

```python
from abc import ABC, abstractmethod
from src.models.market_context import MarketContext
from src.models.strategy_signal import StrategySignal

class BaseStrategy(ABC):
    @abstractmethod
    def validate_params(self, params: dict) -> None:
        raise NotImplementedError

    @abstractmethod
    def evaluate(self, context: MarketContext) -> StrategySignal:
        raise NotImplementedError
```

#### `src/strategy_registry.py`

초기엔 임시 import라도 괜찮다.

```python
from src.strategies.breakout_v1 import BreakoutV1Strategy

STRATEGY_REGISTRY = {
    "breakout_v1": BreakoutV1Strategy,
}
```

### 완료 기준

* registry import 정상
* base interface 정의 완료

---

## T5. breakout_v1 전략 클래스 분리

### 목적

현재 `strategy_signal.py`의 breakout 로직을 독립 전략 클래스로 이동한다.

### 신규 파일

* `src/strategies/breakout_v1.py`

### 구현 원칙

현재 `src/strategy_signal.py`의 로직을 그대로 최대한 보존한다.

### 내부 구성 권장

* `_average_of_recent()`
* `_classify_market()`
* `_build_entry_signal()`
* `BreakoutV1Strategy.validate_params()`
* `BreakoutV1Strategy.evaluate()`

### 핵심 규칙

`evaluate()`는 반드시 `StrategySignal`을 반환해야 한다.

### exit_model 생성 규칙

진입 허용일 때:

```python
entry_hint = context.last_price
target_price = entry_hint * (1 + params["target_pct"])
stop_price = entry_hint * (1 - params["stop_loss_pct"])
```

### validate_params 필수 검증

* fast < slow
* 0 < RSI threshold < 100
* 0 < RSI overheat < 100
* threshold < overheat
* atr multiplier > 1.0
* breakout_lookback >= 1
* target_pct > 0
* stop_loss_pct > 0

### 완료 기준

* 현재 breakout 로직과 동등한 신호 생성
* dict가 아닌 `StrategySignal` 반환

---

## T6. strategy_manager 추가 및 예외 격리

### 목적

전략 실행의 단일 진입점을 만들고, 전략 실패를 엔진과 분리한다.

### 신규 파일

* `src/strategy_manager.py`

### 공개 함수

```python
def generate_strategy_signal(symbol: str) -> StrategySignal:
    ...
```

### 처리 순서

1. `ACTIVE_STRATEGY` 읽기
2. `STRATEGY_REGISTRY`에서 전략 클래스 획득
3. `STRATEGY_PARAMS[ACTIVE_STRATEGY]` 획득
4. 전략 객체 생성
5. `validate_params(params)` 실행
6. 시장 데이터 수집
7. `MarketContext` 구성
8. `evaluate(context)` 실행
9. 결과 반환

### 필수 예외 처리

전략 관련 예외는 반드시 `StrategySignal(entry_allowed=False)`로 흡수

예:

```python
return StrategySignal(
    strategy_name=active_strategy,
    symbol=symbol,
    signal_timestamp=time.time(),
    signal_age_limit_sec=0,
    entry_allowed=False,
    side="NONE",
    trigger="ERROR",
    reason=f"strategy_error:{e}",
    confidence=0.0,
    market_state="UNKNOWN",
    volatility_state="UNKNOWN",
    entry_price_hint=None,
    exit_model=None,
)
```

### 완료 기준

* 잘못된 파라미터여도 엔진 전체는 안 죽음
* 전략 실패 시 진입만 차단됨

---

## T7. entry_gate를 manager 기반으로 전환

### 목적

기존 `strategy_signal.py` 직접 호출 구조를 `strategy_manager` 기반으로 변경한다.

### 대상 파일

* `src/entry_gate.py`

### 변경 내용

현재:

```python
from src.strategy_signal import generate_strategy_signal
```

변경:

```python
from src.strategy_manager import generate_strategy_signal
```

### gate 규칙

* `STRATEGY_ENABLED=False` → `NO_ENTRY_SIGNAL`
* `signal.entry_allowed=False` → `NO_ENTRY_SIGNAL`
* `signal.side != "BUY"` → `NO_ENTRY_SIGNAL`
* stale signal → `NO_ENTRY_SIGNAL`
* 그 외 → `ENTRY_ALLOWED`

### stale signal 처리

```python
import time

if time.time() - signal.signal_timestamp > signal.signal_age_limit_sec:
    return "NO_ENTRY_SIGNAL", "stale_signal"
```

### 완료 기준

* 엔진이 manager 결과를 간접 소비
* 진입 허용 기준이 표준 모델 기반으로 바뀜

---

## T8. engine 청산 로직을 ExitModel 기반으로 전환

### 목적

청산 규칙을 엔진 고정 퍼센트에서 전략 소유 모델로 변경한다.

### 대상 파일

* `src/engine.py`

### 핵심 변경점

#### 제거 대상

```python
TARGET_PCT = 0.002
STOP_LOSS_PCT = 0.0015
```

#### 진입 시 상태 저장 확장

open_trade에 아래 필드 추가:

```python
"strategy_name": signal.strategy_name,
"stop_price": signal.exit_model.stop_price,
"target_price": signal.exit_model.target_price,
```

#### open_trade 정규화 확장

`_normalize_open_trade()`가 새 필드까지 처리하게 수정

### 청산 판단 변경

현재:

* `calculate_target_price(entry_price, TARGET_PCT)`
* `calculate_stop_price(entry_price, STOP_LOSS_PCT)`

변경:

* `target_price = open_trade["target_price"]`
* `stop_price = open_trade["stop_price"]`

### 보존 규칙

* SELL LIMIT target
* SELL MARKET stop
  이 집행 방식 자체는 v1에서 유지

### 완료 기준

* 엔진이 더 이상 target/stop 퍼센트 상수를 직접 가지지 않음
* 전략이 준 stop/target으로 청산

---

# 4. 파일별 최종 상태

## 신규 생성 파일

```text
src/models/strategy_signal.py
src/models/market_context.py
src/risk/exit_models.py
src/strategies/base.py
src/strategies/breakout_v1.py
src/strategy_registry.py
src/strategy_manager.py
```

## 수정 파일

```text
config.py
src/entry_gate.py
src/engine.py
```

## 유지/추후 정리 파일

```text
src/strategy_signal.py
```

### 처리 원칙

* 1차 구현 중에는 남겨두어도 된다
* manager 전환 완료 후 deprecated 처리 가능

---

# 5. 검증 체크리스트

## 구현 후 즉시 확인

* `py_compile` 통과
* import 순환 없음
* `main.py` 실행 시 import error 없음

## 기능 검증

* `STRATEGY_ENABLED=False`에서 진입 차단
* 정상 파라미터에서 BUY/NONE 신호 생성
* 잘못된 파라미터에서 엔진 죽지 않고 `strategy_error`
* 진입 후 상태 파일에 `strategy_name`, `stop_price`, `target_price` 저장
* 재실행 후 target/stop 복원 동작

## 회귀 검증

* pending order reconciliation 유지
* open trade reconciliation 유지
* protective stop market 유지
* 기존 로그 작성 유지

---

# 6. 구현 순서 고정안

반드시 아래 순서로 한다.

### 1

T1 — `entry_gate` 버그 수정

### 2

T2 — dataclass 모델 추가

### 3

T3 — config 확장

### 4

T4 — base/registry 추가

### 5

T5 — breakout 전략 클래스 분리

### 6

T6 — strategy_manager 추가

### 7

T7 — entry_gate 연결 전환

### 8

T8 — engine ExitModel 전환

이 순서를 바꾸면 중간에 import 및 실행 경로가 꼬일 가능성이 높다.

---

# 7. 구현 시 금지사항

* 엔진이 전략 내부 로직을 다시 계산하게 만들지 말 것
* 전략이 주문 API를 직접 호출하게 만들지 말 것
* `StrategySignal` 대신 dict 반환을 혼용하지 말 것
* `STRATEGY_PARAMS`와 전역 상수를 동시에 읽는 혼합 구조를 오래 유지하지 말 것
* 청산 퍼센트를 엔진과 전략 양쪽에 중복 보관하지 말 것

---

# 8. v1 완료 후 바로 이어질 v1.1 후보

v1 완료 뒤 다음 후보는 아래다.

* `signal_logger.py` 실제 연결
* 상태 파일 `schema_version` 엄격 검증
* `ExecutionDecision` 추가
* `risk_guard.py` 추가
* trailing stop 집행 로직
* partial exit 집행 로직

---

# 최종 작업 지시

다음 실제 구현은 아래 한 줄로 시작한다.

> **T1부터 T8까지 순서대로 반영하고, 각 단계마다 py_compile 및 런타임 import 검증을 수행한다.**
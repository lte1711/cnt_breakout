---
aliases:
  - cnt_v1_final_strategy_architecture_spec_ko_source
---

좋다. 사용자 확정 결론을 반영해서 **cnt 프로젝트용 최종 전략 아키텍처 명세서 v1**로 바로 넘어간다.

---

# cnt 프로젝트용 최종 전략 아키텍처 명세서 v1

## 0. 목적

본 명세서는 현재 `cnt` 프로젝트의 기존 구조를 유지하면서, 전략 로직을 **실운영 가능한 표준 전략 아키텍처**로 승격하기 위한 기준 문서다.

현재 상태는 다음과 같다.

* `engine -> entry_gate -> strategy_signal` 3단 분리 완료
* 전략 OFF 시 진입 허용 버그 존재
* 전략 신호는 dict 반환
* 전략 매니저/레지스트리/전략 클래스 구조 미구현
* 청산 로직은 엔진 고정값
* 전략 전용 에러 격리 미구현

본 명세서의 목표는 이를 아래 구조로 전환하는 것이다.

```text
engine
  -> entry_gate
    -> strategy_manager
      -> strategy_registry
        -> selected strategy
      -> StrategySignal
  -> execution / risk / state / logging
```

---

# 1. 설계 원칙

## 1.1 엔진과 전략은 분리한다

* 엔진은 주문, 상태, 체결, 청산 집행만 담당한다.
* 전략은 시장 판단과 청산 모델 정의만 담당한다.

## 1.2 전략은 표준 출력만 반환한다

* 모든 전략은 `StrategySignal`을 반환해야 한다.
* dict 임의 반환은 금지한다.

## 1.3 전략 실패는 진입 차단으로 처리한다

* 전략 예외가 발생해도 엔진은 중단되지 않는다.
* 전략 오류는 `entry_allowed=False` 신호로 격리한다.

## 1.4 청산 기준은 전략 소유로 전환한다

* 엔진 고정 `TARGET_PCT`, `STOP_LOSS_PCT` 방식은 v1 이후 폐기 대상이다.
* 전략은 `ExitModel`을 반환해야 한다.

## 1.5 Spot 기준으로 설계하고 Futures 확장은 optional 필드로 준비한다

* v1은 현재 프로젝트 상태에 맞춰 Spot/Testnet 기준으로 설계한다.
* Futures 관련 필드는 `None` 허용 필드로만 포함한다.

---

# 2. v1 범위

## 포함

* `strategy_manager` 도입
* `strategy_registry` 도입
* `BaseStrategy` 인터페이스 도입
* `BreakoutV1Strategy` 분리
* `StrategySignal` dataclass 도입
* `ExitModel` dataclass 도입
* `MarketContext` dataclass 도입
* 전략 파라미터 검증
* 전략 전용 에러 격리
* `STRATEGY_ENABLED=False` 버그 수정

## 제외

* 멀티 전략 동시 경쟁 실행
* 부분 청산
* 트레일링 스탑 실제 집행
* 포트폴리오 레벨 리스크 엔진
* 상태 파일 마이그레이션 자동화

---

# 3. 최종 디렉터리 구조 v1

```text
config.py
binance_client.py
main.py

src/
  engine.py
  entry_gate.py
  strategy_manager.py
  strategy_registry.py

  strategies/
    base.py
    breakout_v1.py

  models/
    strategy_signal.py
    market_context.py

  risk/
    exit_models.py

  logging/
    signal_logger.py
```

초기 v1에서는 현재 코드베이스를 과도하게 흔들지 않기 위해 최소 분리만 수행한다.

---

# 4. 핵심 데이터 모델

## 4.1 ExitModel

```python
from dataclasses import dataclass
from typing import Optional


@dataclass
class ExitModel:
    stop_price: float | None
    target_price: float | None
    trailing_stop_pct: float | None = None
    partial_exit_levels: list[dict] | None = None
    time_based_exit_minutes: int | None = None
```

### 설명

* v1에서 실제 사용 필드:

  * `stop_price`
  * `target_price`
* 확장 예약 필드:

  * `trailing_stop_pct`
  * `partial_exit_levels`
  * `time_based_exit_minutes`

---

## 4.2 StrategySignal

```python
from dataclasses import dataclass
from typing import Optional

from src.risk.exit_models import ExitModel


@dataclass
class StrategySignal:
    strategy_name: str
    symbol: str

    signal_timestamp: float
    signal_age_limit_sec: float

    entry_allowed: bool
    side: str              # BUY / SELL / NONE
    trigger: str           # BREAKOUT / FILTERED / ERROR / NONE
    reason: str

    confidence: float

    market_state: str
    volatility_state: str

    entry_price_hint: float | None
    exit_model: ExitModel | None
```

### 규칙

* 엔진은 dict가 아닌 이 모델만 소비한다.
* `signal_age_limit_sec` 초과 시 엔진은 신호 폐기한다.
* 전략 오류 발생 시:

  * `entry_allowed=False`
  * `side="NONE"`
  * `trigger="ERROR"`

---

## 4.3 MarketContext

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

### 설명

* v1은 캔들/가격 기반만 사용한다.
* Futures 확장 필드는 optional이다.

---

# 5. 전략 인터페이스

## 5.1 BaseStrategy

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

### 규칙

* 모든 전략은 `validate_params()`를 구현해야 한다.
* 모든 전략은 `evaluate()`에서 `StrategySignal`을 반환해야 한다.

---

# 6. 전략 레지스트리

## 6.1 strategy_registry.py

```python
from src.strategies.breakout_v1 import BreakoutV1Strategy


STRATEGY_REGISTRY = {
    "breakout_v1": BreakoutV1Strategy,
}
```

### 규칙

* v1에서는 단일 활성 전략만 사용한다.
* 향후 멀티 전략 확장은 v2 범위다.

---

# 7. 전략 매니저

## 7.1 역할

`strategy_manager.py`는 전략 실행의 단일 진입점이다.

담당 역할:

* 활성 전략 선택
* 시장 데이터 수집
* `MarketContext` 생성
* 전략 인스턴스 생성
* 파라미터 검증
* 전략 실행
* 예외 격리
* `StrategySignal` 반환

---

## 7.2 공개 인터페이스

```python
def generate_strategy_signal(symbol: str) -> StrategySignal:
    ...
```

---

## 7.3 동작 규칙

### 정상 흐름

1. `ACTIVE_STRATEGY` 확인
2. 해당 전략 클래스 조회
3. 전략 파라미터 조회
4. `validate_params()` 실행
5. 캔들/가격 수집
6. `MarketContext` 생성
7. 전략 `evaluate()` 실행
8. `StrategySignal` 반환

### 실패 흐름

전략 예외 발생 시 엔진으로 예외를 던지지 않는다.

반환 예시:

```python
StrategySignal(
    strategy_name=active_strategy,
    symbol=symbol,
    signal_timestamp=time.time(),
    signal_age_limit_sec=0,
    entry_allowed=False,
    side="NONE",
    trigger="ERROR",
    reason="strategy_error:<message>",
    confidence=0.0,
    market_state="UNKNOWN",
    volatility_state="UNKNOWN",
    entry_price_hint=None,
    exit_model=None,
)
```

---

# 8. 전략 구현 v1: BreakoutV1Strategy

## 8.1 목적

현재 `strategy_signal.py`의 breakout 로직을 독립 전략 클래스로 이동한다.

## 8.2 진입 조건

* 상위 TF 시장 상태가 `TREND_UP`
* 변동성 상태가 `HIGH`
* RSI 과열 아님
* EMA fast > EMA slow
* RSI 임계값 이상
* 최근 고점 돌파 확인

## 8.3 청산 모델

Breakout 전략은 신호 생성 시 `ExitModel`을 함께 만든다.

### v1 기본 규칙

* `stop_price = entry_hint * (1 - STOP_LOSS_PCT)`
* `target_price = entry_hint * (1 + TARGET_PCT)`

주의:

* v1에서는 계산식을 유지하되, **계산 주체를 엔진이 아니라 전략으로 옮긴다.**

---

## 8.4 파라미터 검증

```python
def validate_params(self, params: dict) -> None:
    if params["ema_fast_period"] >= params["ema_slow_period"]:
        raise ValueError("ema_fast_period must be smaller than ema_slow_period")

    if not 0 < params["rsi_threshold"] < 100:
        raise ValueError("rsi_threshold out of range")

    if not 0 < params["rsi_overheat"] < 100:
        raise ValueError("rsi_overheat out of range")

    if params["rsi_threshold"] >= params["rsi_overheat"]:
        raise ValueError("rsi_threshold must be smaller than rsi_overheat")

    if params["atr_expansion_multiplier"] <= 1.0:
        raise ValueError("atr_expansion_multiplier must be greater than 1.0")

    if params["breakout_lookback"] < 1:
        raise ValueError("breakout_lookback must be at least 1")

    if params["target_pct"] <= 0:
        raise ValueError("target_pct must be positive")

    if params["stop_loss_pct"] <= 0:
        raise ValueError("stop_loss_pct must be positive")
```

---

# 9. config 규격 v1

현재 전역 상수 구조를 아래처럼 바꾼다.

## 9.1 필수 설정

```python
STRATEGY_ENABLED = True
ACTIVE_STRATEGY = "breakout_v1"

PRIMARY_INTERVAL = "5m"
ENTRY_INTERVAL = "1m"
KLINES_LIMIT = 200
```

## 9.2 전략 파라미터 묶음

```python
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

### 규칙

* 전략 파라미터는 개별 전역 상수로 직접 읽지 않는다.
* 반드시 `STRATEGY_PARAMS[ACTIVE_STRATEGY]`에서 읽는다.

---

# 10. entry_gate 규격 v1

## 10.1 동작 변경

현재 버그:

* `STRATEGY_ENABLED=False`일 때 진입 허용

v1 수정 규칙:

```python
if not STRATEGY_ENABLED:
    return "NO_ENTRY_SIGNAL", "strategy_disabled"
```

---

## 10.2 공개 인터페이스

기존 시그니처는 유지한다.

```python
def evaluate_entry_gate(symbol: str) -> tuple[str, str]:
    ...
```

### 내부 동작

* `strategy_manager.generate_strategy_signal(symbol)` 호출
* `signal.entry_allowed is False`면 `NO_ENTRY_SIGNAL`
* `signal.side != "BUY"`면 `NO_ENTRY_SIGNAL`
* stale signal이면 `NO_ENTRY_SIGNAL`
* 통과 시 `ENTRY_ALLOWED`

---

# 11. engine 규격 v1

## 11.1 유지할 것

* 상태 파일 로드/저장
* pending/open_trade reconciliation
* 주문 검증
* 주문 제출
* 체결 추적
* 보호성 stop market 집행

## 11.2 변경할 것

현재 엔진은:

* `TARGET_PCT`
* `STOP_LOSS_PCT`

를 직접 가진다.

v1에서는 이 상수를 엔진에서 제거하고, 진입 시 생성된 `signal.exit_model`을 상태에 저장한 뒤 이를 기준으로 청산한다.

---

## 11.3 open_trade 상태 확장

현재 `open_trade`는 entry 정보만 가진다.
v1부터 아래 필드를 포함한다.

```python
{
    "status": "OPEN",
    "entry_price": ...,
    "entry_qty": ...,
    "entry_order_id": ...,
    "entry_side": "BUY",
    "strategy_name": "breakout_v1",
    "stop_price": ...,
    "target_price": ...
}
```

### 이유

* 청산 로직이 전략 기반이어야 하기 때문
* 엔진 재시작 후에도 동일 청산 규칙을 복원해야 하기 때문

---

# 12. 상태 파일 규격 v1

## 12.1 최소 추가 필드

```json
{
  "schema_version": "1.0",
  "strategy_name": "breakout_v1"
}
```

## 12.2 목적

* 향후 상태 구조 변경 대비
* 어떤 전략이 포지션을 열었는지 기록

---

# 13. 로깅 규격 v1

## 13.1 엔진 로그

현재처럼 유지:

* 주문 제출
* 체결
* stop/target 집행
* 오류

## 13.2 전략 로그 추가

신호 평가 결과를 별도로 남긴다.

예시:

```text
strategy=breakout_v1 symbol=ETHUSDT entry_allowed=True side=BUY trigger=BREAKOUT reason=trend_up_high_volatility_breakout confidence=0.82
```

### 목적

* 왜 진입했는지 남기기 위함
* 진입 차단 사유 분석 위함

---

# 14. 단계별 마이그레이션 순서

## 1단계

`entry_gate.py` 수정

* `STRATEGY_ENABLED=False -> NO_ENTRY_SIGNAL`

## 2단계

모델 추가

* `StrategySignal`
* `ExitModel`
* `MarketContext`

## 3단계

`strategy_manager.py`, `strategy_registry.py` 추가

## 4단계

현재 `strategy_signal.py` 로직을 `strategies/breakout_v1.py`로 이동

## 5단계

`entry_gate.py`가 `strategy_manager`를 호출하도록 변경

## 6단계

`engine.py`가 `signal.exit_model`을 상태에 저장하도록 변경

## 7단계

`engine.py` 청산 로직이 상태의 `stop_price`, `target_price`를 사용하도록 변경

---

# 15. v1 완료 기준

아래가 모두 만족되면 v1 완료로 본다.

* `STRATEGY_ENABLED=False`에서 진입 차단
* `StrategySignal` dataclass 도입 완료
* `ExitModel` 도입 완료
* `MarketContext` 도입 완료
* `strategy_manager` 도입 완료
* `BreakoutV1Strategy` 분리 완료
* `config.py`의 전략 파라미터 묶음화 완료
* `engine.py`의 고정 청산 상수 제거 완료
* open_trade 상태에 `strategy_name`, `stop_price`, `target_price` 저장 완료
* 전략 예외가 엔진 전체 중단으로 이어지지 않음

---

# 16. 최종 판정

이 명세서 v1은 현재 `cnt` 프로젝트의 실제 상태를 기준으로, **구조를 뒤엎지 않고 가장 안전하게 전략 아키텍처를 승격하는 설계**다.

핵심은 세 가지다.

* **진입 신호를 표준 모델로 고정한다**
* **전략 로직을 manager + strategy 클래스로 승격한다**
* **청산 규칙을 엔진이 아니라 전략이 소유하게 만든다**

---

## Obsidian Links

- [[CNT v2 ARCHITECTURE DESIGN DOCUMENT]]


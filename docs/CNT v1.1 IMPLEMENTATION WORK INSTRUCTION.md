좋다. 아래는 **문서화 가능한 형식의 CNT v1.1 구현 작업지시서**다.
그대로 `docs/`에 넣을 수 있는 수준으로 정리했다.

---

# CNT v1.1 IMPLEMENTATION WORK INSTRUCTION

```text
DOCUMENT_NAME = cnt_v1.1_implementation_work_instruction
PROJECT       = CNT
VERSION       = 1.1
DATE          = 2026-04-19
STATUS        = READY_FOR_IMPLEMENTATION
BASELINE      = CNT v1 (CLOSED)
REFERENCE     = cnt_v1.1_architecture_design
```

---

# 1. PURPOSE

본 문서는 `CNT v1.1 ARCHITECTURE DESIGN DOCUMENT`를 실제 코드 변경 단위로 분해한
**CNT v1.1 구현 작업지시서**다.

본 작업의 목적은 다음과 같다.

* `StrategySignal`과 실제 주문 실행을 분리한다
* `risk_guard`를 통해 운영 리스크 차단 레이어를 추가한다
* `signal_logger`를 통해 전략 관측성을 확보한다
* v1 계약을 유지하면서 확장 레이어만 추가한다

---

# 2. IMPLEMENTATION PRINCIPLES

## 2.1 v1 core 변경 금지

다음은 직접 변경하지 않는다.

* `StrategySignal` 핵심 계약 의미
* `ExitModel` 기본 stop/target 동작
* `engine -> entry_gate -> strategy_manager` 기본 흐름
* `state schema_version=1.0`

---

## 2.2 레이어 추가 방식으로 구현

v1.1은 아래를 추가한다.

```text
signal_logger
execution_decider
risk_guard
ExecutionDecision
enhanced_exit_manager (Stage 2)
```

---

## 2.3 단계별 구현

* **Stage 1**: 필수 구현
* **Stage 2**: 확장 구현

한 번에 전체를 변경하지 않는다.

---

# 3. IMPLEMENTATION SCOPE

## 3.1 Stage 1 (MANDATORY)

1. `src/strategy_signal.py` legacy wrapper 제거
2. `src/models/execution_decision.py` 추가
3. `src/models/risk_result.py` 추가
4. `src/execution_decider.py` 추가
5. `src/risk/risk_guard.py` 추가
6. `src/signal_logger.py` 추가
7. `src/strategy_manager.py`에 signal_logger 연결
8. `src/engine.py`에 ExecutionDecision 연결
9. state에 `risk_metrics` optional 구조 추가

---

## 3.2 Stage 2 (EXTENSION)

10. `src/risk/enhanced_exit_manager.py` 추가
11. trailing stop 판단 추가
12. time-based exit 판단 추가
13. partial exit 판단 추가

---

# 4. FILE CHANGE PLAN

## 4.1 신규 생성 파일

```text
src/models/execution_decision.py
src/models/risk_result.py
src/execution_decider.py
src/risk/risk_guard.py
src/signal_logger.py
```

### Stage 2 추가 예정

```text
src/risk/enhanced_exit_manager.py
```

---

## 4.2 수정 파일

```text
src/engine.py
src/strategy_manager.py
src/entry_gate.py          (필요 시 최소 조정만)
src/models/strategy_signal.py   (필드 유지, 의미만 재확인)
config.py
AGENTS.md
docs/EXTRA ITEMS REGISTER.md   (신규 파일 등록)
```

---

## 4.3 삭제 파일

```text
src/strategy_signal.py
```

단, 삭제 전 검증 절차를 반드시 수행한다.

---

# 5. STAGE 1 IMPLEMENTATION TASKS

---

## T1. legacy wrapper 제거 준비

### 대상

```text
src/strategy_signal.py
```

### 사전 확인

```bash
grep -R "from src.strategy_signal" src
grep -R "import strategy_signal" src
grep -R "src.strategy_signal" src
```

### 완료 조건

* 결과 0건
* `py_compile` 통과
* 이후 `src/strategy_signal.py` 삭제

---

## T2. ExecutionDecision 모델 추가

### 신규 파일

```text
src/models/execution_decision.py
```

### 구현 내용

```python
from dataclasses import dataclass


@dataclass
class ExecutionDecision:
    execute: bool
    action: str

    reason: str
    signal_reason: str

    strategy_name: str
    symbol: str

    validated_qty: float | None
    validated_price: float | None
    notional_value: float | None

    risk_check_passed: bool
    risk_rejection_reason: str | None

    slippage_check_passed: bool
    slippage_rejection_reason: str | None
```

### 목적

* 전략 신호와 실제 주문 실행을 분리
* 엔진은 이 모델만 보고 주문 제출 여부를 결정

---

## T3. RiskCheckResult 모델 추가

### 신규 파일

```text
src/models/risk_result.py
```

### 구현 내용

```python
from dataclasses import dataclass


@dataclass
class RiskCheckResult:
    passed: bool
    reason: str
```

### 목적

* risk_guard 판단 결과 표준화

---

## T4. risk_guard 추가

### 신규 파일

```text
src/risk/risk_guard.py
```

### 입력

* `StrategySignal`
* `state`
* `balance`

### 출력

* `RiskCheckResult`

### Stage 1 최소 규칙

#### Rule 1. Daily Loss Limit

state 기준:

```json
{
  "risk_metrics": {
    "daily_loss_count": 0
  }
}
```

설정 예시:

```python
MAX_DAILY_LOSS_COUNT = 3
```

#### Rule 2. Loss Cooldown

state 기준:

```json
{
  "risk_metrics": {
    "consecutive_losses": 2,
    "last_loss_time": "2026-04-19 14:20:00"
  }
}
```

설정 예시:

```python
MAX_CONSECUTIVE_LOSSES = 3
LOSS_COOLDOWN_MINUTES = 60
```

### 금지 사항

```text
risk_guard는 runtime.log를 파싱하지 않는다
```

---

## T5. execution_decider 추가

### 신규 파일

```text
src/execution_decider.py
```

### 공개 함수

```python
def decide_execution(signal, state, balance, filters) -> ExecutionDecision:
    ...
```

### 처리 순서

```text
1. signal.entry_allowed 확인
2. risk_guard 실행
3. 가격/수량 기본 검증 준비
4. notional 계산
5. ExecutionDecision 반환
```

### 규칙

* signal이 좋아도 risk_guard가 차단하면 execute=False
* validate 전 단계의 결정 레이어로 동작

---

## T6. signal_logger 추가

### 신규 파일

```text
src/signal_logger.py
```

### 로그 파일

권장:

```text
logs/signal.log
```

### 공개 함수

```python
def append_signal_log(log_file: Path, signal: StrategySignal) -> None:
    ...
```

### 기록 항목

* timestamp
* strategy_name
* symbol
* entry_allowed
* side
* trigger
* reason
* confidence
* market_state
* volatility_state

### 목적

* 전략 평가 결과 관측성 확보
* “왜 진입/차단됐는지” 분석 가능

---

## T7. strategy_manager에 signal_logger 연결

### 대상

```text
src/strategy_manager.py
```

### 변경 내용

* StrategySignal 생성 후 `append_signal_log(...)` 호출
* 전략 예외로 생성된 ERROR signal도 동일하게 기록

### 완료 조건

* 모든 전략 평가 결과가 `logs/signal.log`에 남음

---

## T8. engine에 ExecutionDecision 연결

### 대상

```text
src/engine.py
```

### 현재 흐름

```text
entry_gate -> ENTRY_ALLOWED -> 주문 검증/제출
```

### 변경 흐름

```text
1. signal = generate_strategy_signal(symbol)
2. gate_result = evaluate_entry_gate_from_signal(signal)
3. gate fail -> 종료
4. decision = execution_decider.decide_execution(signal, state, balance, filters)
5. decision.execute=False -> 종료
6. decision.execute=True -> 기존 주문 검증/제출
```

### 구현 원칙

* entry_gate는 여전히 진입 허용 판단만 담당
* execution_decider는 실행 가능 여부만 담당
* engine은 orchestration만 담당

---

## T9. entry_gate 최소 조정

### 대상

```text
src/entry_gate.py
```

### 목적

현재 tuple 기반 인터페이스를 유지하되, 내부적으로 `StrategySignal` 해석을 더 명확히 한다.

### 규칙

* `signal.entry_allowed=False` → `NO_ENTRY_SIGNAL`
* stale signal → `NO_ENTRY_SIGNAL`
* `side != "BUY"` → `NO_ENTRY_SIGNAL`
* 통과 시 `ENTRY_ALLOWED`

### 주의

entry_gate가 ExecutionDecision까지 담당하지 않도록 한다.

---

## T10. state에 risk_metrics 추가

### 대상

```text
src/engine.py
src/state_writer.py
```

### 상태 구조 (optional)

```json
{
  "risk_metrics": {
    "daily_loss_count": 0,
    "consecutive_losses": 0,
    "last_loss_time": null
  }
}
```

### 규칙

* 기본값은 optional
* 손실 종료 시 업데이트
* 이익 종료 시 `consecutive_losses=0`

### 목적

* risk_guard의 데이터 소스 확보
* 로그 파싱 의존 제거

---

## T11. config 확장

### 대상

```text
config.py
```

### 추가 항목 예시

```python
MAX_DAILY_LOSS_COUNT = 3
MAX_CONSECUTIVE_LOSSES = 3
LOSS_COOLDOWN_MINUTES = 60
SIGNAL_LOG_FILE = "logs/signal.log"
```

### 규칙

* Stage 1에서는 최소 설정만 추가
* 기존 전략 파라미터 구조와 충돌시키지 않음

---

## T12. 문서 갱신

### 대상

```text
AGENTS.md
docs/EXTRA ITEMS REGISTER.md
```

### 추가 내용

* `ExecutionDecision`
* `risk_guard`
* `signal_logger`
* `risk_metrics`
* `signal.log`

---

# 6. STAGE 2 IMPLEMENTATION TASKS

---

## T13. enhanced_exit_manager 추가

### 신규 파일

```text
src/risk/enhanced_exit_manager.py
```

### 공개 함수

```python
def evaluate_exit(open_trade, current_price, filters) -> ExitSignal:
    ...
```

### 목적

기존 `should_exit_long`, `should_stop` 판단 로직을 확장 가능한 판단 레이어로 감싼다.

---

## T14. trailing stop 추가

### 필요 state 확장

```json
{
  "highest_price_since_entry": 0.0
}
```

### 규칙

* entry 이후 최고가 추적
* `trailing_stop_pct`만큼 하락 시 exit signal 발생

---

## T15. time-based exit 추가

### 필요 state 확장

```json
{
  "entry_time": "2026-04-19 14:20:00"
}
```

### 규칙

* `time_based_exit_minutes` 초과 보유 시 exit signal 발생

---

## T16. partial exit 추가

### 모델

```python
@dataclass
class PartialExitLevel:
    qty_ratio: float
    target_price: float
```

### 수량 처리 규칙

```text
adjusted_qty = floor(entry_qty * qty_ratio / step_size) * step_size

if adjusted_qty < min_qty:
    partial exit 불가 → skip 또는 full exit fallback
```

### 중요 규칙

* 반드시 Binance filter 검증을 통과해야 함

---

# 7. ENGINE INTEGRATION RULES

## 7.1 Entry

```text
signal -> entry_gate -> execution_decider -> validator -> executor
```

## 7.2 Exit

```text
open_trade -> enhanced_exit_manager -> existing sell execution path
```

## 7.3 핵심 원칙

```text
판단 로직은 확장 가능하게 바꾸고,
실제 주문 집행 방식은 v1의 검증된 경로를 최대한 유지한다
```

---

# 8. VALIDATION REQUIREMENTS

## 8.1 Stage 1 완료 기준

* `strategy_signal.py` 제거 완료
* `ExecutionDecision` 도입 완료
* `risk_guard` 동작 확인
* `signal.log` 기록 확인
* BUY 신호가 있어도 risk_guard 차단 가능
* 기존 v1 stop/target 회귀 없음
* `py_compile` 통과
* `main.py` import 오류 없음

---

## 8.2 Stage 2 완료 기준

* trailing stop 판단 동작
* time-based exit 판단 동작
* partial exit 수량 필터 통과
* 기존 full exit 경로 회귀 없음

---

# 9. IMPLEMENTATION ORDER

## Stage 1 권장 순서

```text
1. T1  legacy wrapper 제거 준비
2. T2  ExecutionDecision 모델 추가
3. T3  RiskCheckResult 모델 추가
4. T4  risk_guard 추가
5. T5  execution_decider 추가
6. T6  signal_logger 추가
7. T11 config 확장
8. T7  strategy_manager 연결
9. T9  entry_gate 최소 조정
10. T8 engine 연결
11. T10 state risk_metrics 추가
12. T12 문서 갱신
13. py_compile / runtime 검증
14. src/strategy_signal.py 삭제
```

---

## Stage 2 권장 순서

```text
1. T13 enhanced_exit_manager 추가
2. T14 trailing stop
3. T15 time-based exit
4. T16 partial exit
5. 회귀 검증
```

---

# 10. PROHIBITIONS

다음은 금지한다.

* v1 core engine 흐름을 전면 교체하는 것
* StrategySignal 의미를 바꾸는 것
* risk_guard가 로그를 파싱하게 만드는 것
* enhanced_exit_manager가 직접 주문을 보내는 것
* partial exit가 filter 검증 없이 제출되는 것

---

# 11. FINAL STATEMENT

CNT v1.1 구현은 구조 재작성 작업이 아니다.

```text
목표:
전략 신호를 더 안전하게 실행하고,
리스크를 통제하며,
청산 품질과 관측성을 높이는 것
```

---

# 결론

> **CNT v1.1 구현 작업은 v1의 안정된 기준선 위에 실행 판단, 리스크 제어, 관측성 레이어를 얹는 작업이다.**

---


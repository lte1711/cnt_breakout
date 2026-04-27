---
aliases:
  - CNT v1.1 IMPLEMENTATION VALIDATION CHECKLIST
---

# CNT v1.1 IMPLEMENTATION VALIDATION CHECKLIST

```text
DOCUMENT_NAME = cnt_v1.1_implementation_validation_checklist
PROJECT       = CNT
VERSION       = 1.1
DATE          = 2026-04-19
STATUS        = VALIDATION_READY
BASELINE      = CNT v1 (CLOSED)
REFERENCE_1   = cnt_v1.1_architecture_design
REFERENCE_2   = cnt_v1.1_implementation_work_instruction
```

---

# 1. PURPOSE

본 문서는 `CNT v1.1 IMPLEMENTATION WORK INSTRUCTION`의 구현 결과를 검증하기 위한
**CNT v1.1 구현 검증 체크리스트**다.

검증 목적은 다음과 같다.

* v1.1 확장 레이어가 설계 의도대로 연결되었는지 확인
* v1 core 회귀 없이 확장 기능이 동작하는지 확인
* 실행 판단, 리스크 제어, 관측성 레이어가 실제 런타임에서 유효한지 확인
* Stage 1 / Stage 2 완료 여부를 명확히 판정

---

# 2. VALIDATION PRINCIPLES

## 2.1 v1 회귀 금지

다음은 반드시 유지되어야 한다.

* 기존 v1 stop/target 동작
* 기존 entry_gate 안전 규칙
* 기존 state schema_version=1.0 기반 저장
* 기존 엔진 주문/체결/복원 흐름

---

## 2.2 검증은 레이어별로 수행

검증은 아래 레이어 순서로 수행한다.

```text
문서/구조
→ 모델/인터페이스
→ 엔트리 흐름
→ 실행 판단
→ 리스크 차단
→ 로그
→ 상태 파일
→ 청산 확장
→ 회귀 검증
```

---

## 2.3 forced BUY 경로 사용 금지

운영 검증 시 강제 BUY 테스트 경로를 사용하지 않는다.
필요 시 synthetic signal 또는 isolated unit validation으로 대체한다.

---

# 3. VALIDATION SCOPE

## 3.1 Stage 1 검증 범위

* legacy wrapper 제거
* ExecutionDecision 도입
* RiskCheckResult 도입
* risk_guard 추가
* execution_decider 추가
* signal_logger 추가
* strategy_manager signal logging 연결
* engine ExecutionDecision 연결
* state risk_metrics 도입
* config 확장
* 문서 갱신

---

## 3.2 Stage 2 검증 범위

* enhanced_exit_manager 추가
* trailing stop 판단
* time-based exit 판단
* partial exit 판단
* partial qty filter 처리
* exit 경로 회귀 없음

---

# 4. DOCUMENT AND STRUCTURE VALIDATION

---

## A1. 문서 헤더 확인

### 확인 대상

* `docs/cnt_v1.1_architecture_design.*`
* `docs/cnt_v1.1_implementation_work_instruction.*`
* `docs/cnt_v1.1_implementation_validation_checklist.*`

### 확인 항목

* `PROJECT = CNT`
* `VERSION = 1.1`
* `DATE` 일치
* `STATUS` 적절성
* reference 문서 연결성

### 판정 기준

* 모두 존재하고 상호 참조가 맞으면 PASS

---

## A2. AGENTS.md 반영 확인

### 확인 항목

* `ExecutionDecision`
* `risk_guard`
* `signal_logger`
* `risk_metrics`
* `signal.log`
* `enhanced_exit_manager` (Stage 2 반영 시)

### 판정 기준

* 신규 컴포넌트가 AGENTS.md에 반영되어 있으면 PASS

---

## A3. EXTRA ITEMS REGISTER 반영 확인

### 신규 등록 대상

* `src/models/execution_decision.py`
* `src/models/risk_result.py`
* `src/execution_decider.py`
* `src/risk/risk_guard.py`
* `src/signal_logger.py`
* `logs/signal.log`
* `src/risk/enhanced_exit_manager.py` (Stage 2 시)

### 판정 기준

* 범위 외 항목 등록 원칙에 맞게 기록되어 있으면 PASS

---

# 5. FILE AND INTERFACE VALIDATION

---

## B1. legacy wrapper 제거 확인

### 확인 대상

```text
src/strategy_signal.py
```

### 사전/사후 검사

```bash
grep -R "from src.strategy_signal" src
grep -R "import strategy_signal" src
grep -R "src.strategy_signal" src
```

### 판정 기준

* 참조 0건
* 파일 제거 완료
* import/runtime 에러 없음

---

## B2. ExecutionDecision 모델 확인

### 확인 대상

```text
src/models/execution_decision.py
```

### 확인 항목

* `execute`
* `action`
* `reason`
* `signal_reason`
* `strategy_name`
* `symbol`
* `validated_qty`
* `validated_price`
* `notional_value`
* `risk_check_passed`
* `risk_rejection_reason`
* `slippage_check_passed`
* `slippage_rejection_reason`

### 판정 기준

* dataclass 정의와 필드 구성이 설계와 일치하면 PASS

---

## B3. RiskCheckResult 모델 확인

### 확인 대상

```text
src/models/risk_result.py
```

### 판정 기준

* `passed`, `reason` 두 필드가 정의되어 있으면 PASS

---

## B4. signal_logger 위치 확인

### 확인 대상

```text
src/signal_logger.py
```

### 판정 기준

* `src/logging/`이 아니라 `src/` 직하에 존재하면 PASS

---

# 6. ENTRY FLOW VALIDATION

---

## C1. 엔트리 흐름 연결 확인

### 목표 흐름

```text
signal = generate_strategy_signal()
→ gate = evaluate_entry_gate(...)
→ decision = execution_decider.decide_execution(...)
→ validator
→ executor
```

### 판정 기준

* engine 내부에서 위 흐름이 명확히 구현되어 있으면 PASS

---

## C2. entry_gate 역할 경계 확인

### 확인 항목

entry_gate는 아래만 담당해야 한다.

* `signal.entry_allowed` 판단
* stale signal 차단
* `side != BUY` 차단

### 금지

* risk_guard 호출
* ExecutionDecision 생성
* 주문 수량/가격 결정

### 판정 기준

* 역할이 entry permission만 수행하면 PASS

---

## C3. ExecutionDecision 호출 위치 확인

### 확인 항목

ExecutionDecision은 반드시:

```text
gate 통과 후
주문 검증/제출 전
```

호출되어야 한다.

### 판정 기준

* 호출 위치가 설계와 일치하면 PASS

---

# 7. RISK GUARD VALIDATION

---

## D1. risk_guard 데이터 소스 확인

### 필수 규칙

```text
risk_guard는 runtime.log를 파싱하지 않는다
```

### 확인 데이터

* `state`
* `balance`
* `signal`

### 판정 기준

* 로그 파싱 코드가 없고 state 기반으로만 판단하면 PASS

---

## D2. state risk_metrics 구조 확인

### 기대 구조

```json
{
  "risk_metrics": {
    "daily_loss_count": 0,
    "consecutive_losses": 0,
    "last_loss_time": null
  }
}
```

### 판정 기준

* optional 구조로 state 저장/복원이 가능하면 PASS

---

## D3. daily loss limit 차단 확인

### 테스트 시나리오

* `daily_loss_count`를 한도 이상으로 설정
* BUY signal 생성
* execution_decider 실행

### 기대 결과

```text
execute = False
risk_check_passed = False
risk_rejection_reason = DAILY_LOSS_LIMIT
```

### 판정 기준

* 위 결과가 나오면 PASS

---

## D4. loss cooldown 차단 확인

### 테스트 시나리오

* `consecutive_losses` 한도 이상
* `last_loss_time`이 cooldown 미만
* BUY signal 생성

### 기대 결과

```text
execute = False
risk_rejection_reason = LOSS_COOLDOWN
```

### 판정 기준

* 차단되면 PASS

---

## D5. 정상 통과 시나리오 확인

### 테스트 시나리오

* risk_metrics 정상
* BUY signal 생성

### 기대 결과

```text
risk_check_passed = True
execute 가능
```

### 판정 기준

* 차단 없이 다음 레이어로 진행되면 PASS

---

# 8. SIGNAL LOGGER VALIDATION

---

## E1. signal.log 생성 확인

### 확인 대상

```text
logs/signal.log
```

### 판정 기준

* 파일 생성 및 append 동작 확인 시 PASS

---

## E2. 정상 신호 기록 확인

### 기대 기록 항목

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

### 판정 기준

* 필수 항목이 누락 없이 기록되면 PASS

---

## E3. ERROR signal 기록 확인

### 테스트 시나리오

* strategy_manager 예외 유도 또는 synthetic error signal

### 기대 결과

* `trigger=ERROR`
* `reason=strategy_error:...`
* signal.log 기록 존재

### 판정 기준

* 예외 신호도 동일하게 기록되면 PASS

---

# 9. STATE PERSISTENCE VALIDATION

---

## F1. state schema 유지 확인

### 기대 항목

```json
{
  "schema_version": "1.0",
  "strategy_name": "breakout_v1"
}
```

### 판정 기준

* 기존 v1 상태 스키마가 유지되면 PASS

---

## F2. risk_metrics 저장 확인

### 기대 항목

```json
{
  "risk_metrics": {
    "daily_loss_count": ...,
    "consecutive_losses": ...,
    "last_loss_time": ...
  }
}
```

### 판정 기준

* 저장과 재로딩이 가능하면 PASS

---

## F3. open_trade 기존 필드 회귀 없음

### 확인 항목

* `entry_price`
* `entry_qty`
* `entry_order_id`
* `entry_side`
* `strategy_name`
* `stop_price`
* `target_price`

### 판정 기준

* 기존 open_trade 구조가 유지되면 PASS

---

# 10. RUNTIME VALIDATION

---

## G1. py_compile 확인

### 실행 예시

```bash
python -m py_compile config.py main.py binance_client.py src/*.py src/models/*.py src/risk/*.py src/strategies/*.py
```

### 판정 기준

* 에러 없으면 PASS

---

## G2. main.py import 확인

### 판정 기준

* import error 없으면 PASS

---

## G3. Strategy OFF 경로 확인

### 테스트 시나리오

* `STRATEGY_ENABLED=False`

### 기대 결과

```text
NO_ENTRY_SIGNAL / strategy_disabled
```

### 판정 기준

* 그대로 유지되면 PASS

---

## G4. BUY signal + risk pass 확인

### 테스트 시나리오

* synthetic breakout 또는 실제 안전한 mock context

### 기대 결과

```text
signal.entry_allowed = True
decision.execute = True
```

### 판정 기준

* signal과 decision이 분리되어 정상 동작하면 PASS

---

## G5. BUY signal + risk reject 확인

### 기대 결과

```text
signal.entry_allowed = True
decision.execute = False
```

### 판정 기준

* 신호와 실행 차단이 분리되어 동작하면 PASS

---

## G6. v1 회귀 없음 확인

### 확인 항목

* 기존 stop/target 집행
* pending/open_trade reconciliation
* state 저장
* runtime.log 기록

### 판정 기준

* 기존 경로가 깨지지 않으면 PASS

---

# 11. STAGE 2 EXIT VALIDATION

---

## H1. enhanced_exit_manager 연결 확인

### 기대 흐름

```text
open_trade
→ enhanced_exit_manager.evaluate_exit(...)
→ exit signal
→ 기존 SELL / STOP 실행
```

### 판정 기준

* 판단은 새 레이어, 집행은 기존 엔진 경로면 PASS

---

## H2. trailing stop 확인

### 테스트 시나리오

* `highest_price_since_entry` 기록
* `trailing_stop_pct` 활성
* 가격 후퇴

### 기대 결과

* `should_exit=True`
* `exit_type=TRAILING_STOP`

### 판정 기준

* trailing 판단이 정확하면 PASS

---

## H3. time-based exit 확인

### 테스트 시나리오

* `entry_time` 존재
* 보유 시간 초과

### 기대 결과

* `should_exit=True`
* `exit_type=TIME_EXIT`

### 판정 기준

* 시간 청산이 동작하면 PASS

---

## H4. partial exit 수량 정렬 확인

### 테스트 시나리오

* `qty_ratio` 적용
* step_size/min_qty 존재

### 기대 결과

```text
adjusted_qty = floor(entry_qty * ratio / step_size) * step_size
```

### 판정 기준

* filter 통과 수량만 제출되면 PASS

---

## H5. partial exit fallback 확인

### 기대 결과

* `adjusted_qty < min_qty`면

  * skip 또는
  * full exit fallback

### 판정 기준

* invalid partial order가 제출되지 않으면 PASS

---

# 12. FAILURE CLASSIFICATION

## FAIL-CRITICAL

아래는 즉시 수정 후 재검증 대상이다.

* import error
* state schema 파손
* risk_guard가 로그를 파싱함
* engine가 ExecutionDecision 없이 주문 제출
* partial exit가 filter 없이 제출됨
* v1 stop/target 회귀 발생

---

## FAIL-MINOR

아래는 수정 권장 후 재검증 대상이다.

* signal.log 포맷 일부 누락
* AGENTS.md 미갱신
* EXTRA ITEMS REGISTER 누락
* validation 문구/메타데이터 누락

---

# 13. COMPLETION CRITERIA

## Stage 1 완료 조건

* legacy wrapper 제거 완료
* ExecutionDecision 동작
* risk_guard 동작
* signal_logger 동작
* risk_metrics 저장/복원 가능
* v1 회귀 없음
* compile/import/runtime PASS

---

## Stage 2 완료 조건

* enhanced_exit_manager 동작
* trailing stop 동작
* time exit 동작
* partial exit filter 처리 동작
* full exit 경로 회귀 없음

---

# 14. FINAL RESULT TEMPLATE

```text
CNT v1.1 IMPLEMENTATION VALIDATION REPORT

DATE=
PROJECT=CNT
VERSION=1.1
STATUS=

SUMMARY
- Document and structure: PASS / FAIL
- Entry flow linkage: PASS / FAIL
- Risk guard: PASS / FAIL
- Signal logger: PASS / FAIL
- State persistence: PASS / FAIL
- Runtime validation: PASS / FAIL
- Exit extension: PASS / FAIL (if Stage 2)

FINAL DECISION
- Stage 1 complete / incomplete
- Stage 2 complete / incomplete
- Ready for closure / additional fix required
```

---

# 15. FINAL STATEMENT

본 체크리스트는 CNT v1.1 구현이 단순 코드 추가가 아니라
**운영 가능한 확장 레이어로 완성됐는지**를 검증하기 위한 기준이다.

```text
핵심:
좋은 신호를 내는 것과
실제로 실행해도 되는 신호를 구분하고,
그 판단 과정이 기록되고 복원 가능해야 한다
```

---

# 결론

> **CNT v1.1 구현 검증은 신호, 실행, 리스크, 관측성, 청산 확장이 서로 충돌 없이 연결됐는지를 확인하는 절차다.**

---

---

## Obsidian Links

- [[CNT v1.1 ARCHITECTURE DESIGN DOCUMENT]]


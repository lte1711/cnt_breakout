---
tags:
  - cnt
  - docs
  - validation
  - instruction
  - v1
aliases:
  - CNT v1.1 STAGE 2 IMPLEMENTATION VALIDATION CHECKLIST
---

# CNT v1.1 STAGE 2 IMPLEMENTATION VALIDATION CHECKLIST

```text
DOCUMENT_NAME = cnt_v1.1_stage2_implementation_validation_checklist
PROJECT       = CNT
VERSION       = 1.1
STAGE         = 2
DATE          = 2026-04-19
STATUS        = VALIDATION_READY
BASELINE      = CNT v1.1 Stage 1 (CLOSED)
REFERENCE_1   = cnt_v1.1_stage2_architecture_design
REFERENCE_2   = cnt_v1.1_stage2_implementation_work_instruction
```

---

# 1. PURPOSE

본 문서는 CNT v1.1 Stage 2 구현 결과를 검증하기 위한
**Stage 2 검증 체크리스트**다.

검증 목적:

* trailing stop, time exit, partial exit가 설계 의도대로 동작하는지 확인
* 기존 v1 / v1.1 Stage 1 기능에 회귀가 없는지 확인
* 판단 레이어와 실행 레이어가 여전히 분리되어 있는지 확인
* 상태 저장과 복원이 확장된 청산 모델까지 포함해 정상 동작하는지 확인

---

# 2. VALIDATION PRINCIPLES

---

## 2.1 기존 구조 회귀 금지

다음은 반드시 유지되어야 한다.

* `StrategySignal`
* `ExecutionDecision`
* `engine → entry_gate → execution_decider`
* 기존 stop/target 경로
* state schema_version=1.0

---

## 2.2 판단과 실행 분리 유지

```text
enhanced_exit_manager = 판단만 수행
engine = 실제 SELL 실행
```

---

## 2.3 상태 기반 검증

Stage 2 검증은 아래 state 필드를 포함해 수행한다.

```text
highest_price_since_entry
entry_time
partial_exit_progress
```

---

## 2.4 forced BUY 경로 금지

검증 시 강제 BUY 경로는 사용하지 않는다.
필요 시 synthetic open_trade/state 조합으로 exit 판단을 검증한다.

---

# 3. VALIDATION SCOPE

---

## 포함 범위

* ExitSignal 모델
* enhanced_exit_manager
* trailing stop
* time exit
* partial exit
* engine exit 연결
* state 확장
* filter 처리
* 회귀 검증

---

## 제외 범위

* 신규 전략 추가
* 엔트리 전략 변경
* execution_decider 구조 재설계

---

# 4. DOCUMENT AND STRUCTURE VALIDATION

---

## A1. 문서 존재 확인

### 확인 대상

* `docs/cnt_v1.1_stage2_architecture_design.*`
* `docs/cnt_v1.1_stage2_implementation_work_instruction.*`
* `docs/cnt_v1.1_stage2_implementation_validation_checklist.*`

### 판정 기준

* 문서 3종이 모두 존재하고 Stage 2 기준으로 상호 참조되면 PASS

---

## A2. AGENTS.md 반영 확인

### 확인 항목

* `ExitSignal`
* `enhanced_exit_manager`
* `highest_price_since_entry`
* `entry_time`
* `partial_exit_progress`

### 판정 기준

* 신규 Stage 2 컴포넌트가 AGENTS.md에 반영되면 PASS

---

## A3. EXTRA ITEMS REGISTER 반영 확인

### 신규 등록 대상

* `src/models/exit_signal.py`
* `src/risk/enhanced_exit_manager.py`

### 판정 기준

* 신규 파일이 등록 원칙에 맞게 기재되어 있으면 PASS

---

# 5. FILE AND INTERFACE VALIDATION

---

## B1. ExitSignal 모델 확인

### 확인 대상

```text
src/models/exit_signal.py
```

### 필수 필드

* `should_exit`
* `exit_type`
* `reason`
* `target_price`
* `stop_price`
* `partial_qty`

### 판정 기준

* dataclass로 정의되고 필드가 설계와 일치하면 PASS

---

## B2. enhanced_exit_manager 함수 확인

### 확인 대상

```text
src/risk/enhanced_exit_manager.py
```

### 필수 함수

```python
evaluate_exit(open_trade, current_price, state, filters)
```

### 판정 기준

* 평가 함수가 존재하고 ExitSignal을 반환하면 PASS

---

# 6. EXIT FLOW VALIDATION

---

## C1. Stage 2 exit 연결 확인

### 기대 흐름

```text
open_trade
→ enhanced_exit_manager.evaluate_exit(...)
→ ExitSignal
→ engine 기존 SELL 경로
```

### 판정 기준

* engine이 evaluate_exit 결과만 보고 기존 SELL 경로를 호출하면 PASS

---

## C2. enhanced_exit_manager 역할 경계 확인

### 허용

* stop 판단
* trailing stop 판단
* target 판단
* partial exit 판단
* time exit 판단

### 금지

* 주문 직접 제출
* order_executor 직접 호출
* state 파일 직접 저장

### 판정 기준

* 판단만 담당하면 PASS

---

# 7. TRAILING STOP VALIDATION

---

## D1. highest_price_since_entry 초기화 확인

### 테스트

* 신규 진입 상태 생성

### 기대 결과

```text
highest_price_since_entry = entry_price
```

### 판정 기준

* entry 시 초기값이 올바르게 설정되면 PASS

---

## D2. 최고가 갱신 확인

### 테스트

* open_trade 유지 중 가격 상승

### 기대 결과

```text
highest_price_since_entry = max(previous_highest, current_price)
```

### 판정 기준

* 상승 시 최고가가 정상 갱신되면 PASS

---

## D3. trailing stop 조건 확인

### 테스트 조건

* `trailing_stop_pct` 활성
* 최고가 대비 일정 비율 하락

### 기대 결과

```text
ExitSignal.should_exit = True
ExitSignal.exit_type   = TRAILING_STOP
```

### 판정 기준

* 조건 충족 시 trailing exit 판단이 발생하면 PASS

---

## D4. trailing stop 미충족 확인

### 기대 결과

* `should_exit=False`

### 판정 기준

* 조기 청산이 발생하지 않으면 PASS

---

# 8. TIME EXIT VALIDATION

---

## E1. entry_time 저장 확인

### 기대 필드

```text
entry_time
```

### 판정 기준

* 신규 진입 시 entry_time이 state/open_trade에 저장되면 PASS

---

## E2. time exit 조건 확인

### 테스트

* `time_based_exit_minutes` 초과 상태 구성

### 기대 결과

```text
ExitSignal.should_exit = True
ExitSignal.exit_type   = TIME_EXIT
```

### 판정 기준

* 보유 시간이 조건을 넘으면 exit signal이 발생하면 PASS

---

## E3. time exit 미충족 확인

### 기대 결과

* `should_exit=False`

### 판정 기준

* 시간 미충족 상태에서 오동작 없으면 PASS

---

# 9. PARTIAL EXIT VALIDATION

---

## F1. partial_exit_levels 해석 확인

### 입력 예시

```text
qty_ratio = 0.5
target_price = 101.0
```

### 판정 기준

* partial exit 레벨이 정상 해석되면 PASS

---

## F2. partial qty 계산 확인

### 기대 공식

```text
raw_qty = entry_qty * qty_ratio
adjusted_qty = floor(raw_qty / step_size) * step_size
```

### 판정 기준

* 수량이 step_size에 맞게 정렬되면 PASS

---

## F3. min_qty 필터 확인

### 테스트

* adjusted_qty < min_qty

### 기대 결과

* partial exit 금지
* skip 또는 fallback 처리

### 판정 기준

* invalid partial order가 생성되지 않으면 PASS

---

## F4. partial exit signal 확인

### 기대 결과

```text
ExitSignal.should_exit = True
ExitSignal.exit_type   = PARTIAL
ExitSignal.partial_qty = adjusted_qty
```

### 판정 기준

* 정상 partial exit 신호가 생성되면 PASS

---

# 10. STATE PERSISTENCE VALIDATION

---

## G1. state 확장 필드 저장 확인

### 기대 필드

* `highest_price_since_entry`
* `entry_time`
* `partial_exit_progress` (사용 시)

### 판정 기준

* 저장 및 재로딩 가능하면 PASS

---

## G2. 상태 복원 확인

### 테스트

* 엔진 재시작 전후 state 유지

### 기대 결과

* trailing / time exit 계산에 필요한 값이 복원됨

### 판정 기준

* 재시작 후에도 확장 exit 판단이 이어지면 PASS

---

## G3. exit 후 필드 정리 확인

### 기대 결과

* 포지션 종료 후 관련 state 정리

### 판정 기준

* 종료 후 stale trailing/time fields가 남지 않으면 PASS

---

# 11. ENGINE EXECUTION VALIDATION

---

## H1. STOP 경로 회귀 없음

### 기대 결과

* 기존 STOP MARKET 경로 정상 동작

### 판정 기준

* Stage 1 이전 동작과 동일하면 PASS

---

## H2. TARGET 경로 회귀 없음

### 기대 결과

* 기존 SELL LIMIT target 경로 정상 동작

### 판정 기준

* 기존 동작 유지되면 PASS

---

## H3. TRAILING STOP 실행 경로 확인

### 기대 결과

* trailing exit 판단 후 기존 SELL 실행 경로 사용

### 판정 기준

* 실행 방식이 새로운 독립 경로를 만들지 않으면 PASS

---

## H4. TIME EXIT 실행 경로 확인

### 기대 결과

* time exit 판단 후 기존 SELL 실행 경로 사용

### 판정 기준

* 기존 실행 체계를 재사용하면 PASS

---

## H5. PARTIAL EXIT 실행 경로 확인

### 기대 결과

* partial_qty를 사용한 SELL LIMIT 제출
* 기존 validator / executor 통과

### 판정 기준

* partial도 검증된 기존 제출 경로를 거치면 PASS

---

# 12. RUNTIME VALIDATION

---

## I1. py_compile 확인

### 실행 예시

```bash
python -m py_compile config.py main.py binance_client.py src/*.py src/models/*.py src/risk/*.py src/strategies/*.py
```

### 판정 기준

* 에러 없으면 PASS

---

## I2. import 확인

### 판정 기준

* `main.py` import error 없음

---

## I3. synthetic trailing test

### 시나리오

* open_trade 구성
* highest_price_since_entry > entry_price
* trailing 조건 충족

### 기대 결과

* `TRAILING_STOP` exit signal 생성

### 판정 기준

* PASS

---

## I4. synthetic time exit test

### 시나리오

* entry_time 과거값 설정
* time exit 조건 충족

### 기대 결과

* `TIME_EXIT` exit signal 생성

### 판정 기준

* PASS

---

## I5. synthetic partial exit test

### 시나리오

* partial_exit_levels 설정
* 가격 목표 도달
* qty filter 통과

### 기대 결과

* `PARTIAL` exit signal 생성

### 판정 기준

* PASS

---

## I6. 회귀 테스트

### 확인 항목

* 기존 stop/target
* ExecutionDecision
* risk_guard
* signal_logger
* state persistence
* runtime.log
* signal.log

### 판정 기준

* 기존 기능 회귀가 없으면 PASS

---

# 13. FAILURE CLASSIFICATION

---

## FAIL-CRITICAL

아래는 즉시 수정 후 재검증 대상이다.

* trailing stop 오동작
* time exit 오동작
* partial exit filter 미통과 주문 생성
* enhanced_exit_manager가 직접 주문 제출
* 기존 stop/target 경로 파손
* state 복원 실패

---

## FAIL-MINOR

아래는 수정 권장 후 재검증 대상이다.

* AGENTS.md 미갱신
* EXTRA ITEMS REGISTER 누락
* validation 문서 메타 정보 누락
* partial exit 기록 포맷 미흡

---

# 14. COMPLETION CRITERIA

---

## Stage 2 완료 조건

* ExitSignal 구현 완료
* enhanced_exit_manager 구현 완료
* trailing stop 동작
* time exit 동작
* partial exit 동작
* state 확장 저장/복원 가능
* 기존 stop/target 회귀 없음
* compile/import/runtime 검증 통과

---

# 15. FINAL RESULT TEMPLATE

```text
CNT v1.1 Stage 2 IMPLEMENTATION VALIDATION REPORT

DATE=
PROJECT=CNT
VERSION=1.1
STAGE=2
STATUS=

SUMMARY
- Document and structure: PASS / FAIL
- Exit flow linkage: PASS / FAIL
- Trailing stop: PASS / FAIL
- Time exit: PASS / FAIL
- Partial exit: PASS / FAIL
- State persistence: PASS / FAIL
- Runtime validation: PASS / FAIL
- Regression validation: PASS / FAIL

FINAL DECISION
- Stage 2 complete / incomplete
- Approved / fix required
```

---

# 16. FINAL STATEMENT

본 체크리스트는 CNT v1.1 Stage 2 구현이
**지능형 청산 레이어로서 실제 운영 가능 수준인지**를 검증하기 위한 기준이다.

```text
핵심:
청산 판단은 더 똑똑해져야 하지만,
실행 경로는 여전히 안전하고 검증된 구조를 유지해야 한다
```

---

# 결론

> **CNT v1.1 Stage 2 검증은 trailing stop, time exit, partial exit가 기존 안정 구조를 깨지 않고 연결됐는지를 확인하는 절차다.**

---

## Obsidian Links

- [[00 CNT Vault Home|Vault Home]]
- [[00 Docs Index|Docs Index]]

### Related
- [[cnt_v1.1_stage2_architecture_design]]
- [[cnt_v1.1_stage2_implementation_work_instruction]]

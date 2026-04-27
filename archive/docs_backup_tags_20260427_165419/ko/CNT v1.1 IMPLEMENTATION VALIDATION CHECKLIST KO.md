---
aliases:
  - CNT v1.1 IMPLEMENTATION VALIDATION CHECKLIST KO
---

# CNT v1.1 구현 검증 체크리스트

```text
DOCUMENT_NAME = cnt_v1.1_implementation_validation_checklist_ko
PROJECT       = CNT
VERSION       = 1.1
DATE          = 2026-04-19
STATUS        = VALIDATION_READY
BASELINE      = CNT v1 (CLOSED)
REFERENCE_1   = cnt_v1.1_architecture_design
REFERENCE_2   = cnt_v1.1_implementation_work_instruction
```

## 1. 목적

이 문서는 `CNT v1.1 IMPLEMENTATION WORK INSTRUCTION` 구현 결과를 검증하기 위한
**CNT v1.1 구현 검증 체크리스트**다.

검증 목적:

- v1.1 확장 레이어가 설계대로 연결되었는지 확인
- v1 core를 훼손하지 않고 확장 기능이 동작하는지 확인
- 실행 판단, 리스크 제어, 관측성 레이어가 유효한지 확인
- Stage 1 / Stage 2 완료 여부를 명확히 판단

## 2. 검증 원칙

### 2.1 v1 훼손 금지

아래는 유지되어야 한다.

- 기존 v1 stop/target 동작
- 기존 entry_gate 안전 규칙
- 기존 state schema_version=1.0 기반 로드
- 기존 엔진 주문/체결/복원 흐름

### 2.2 검증은 레이어별로 수행

```text
문서/구조
-> 모델/인터페이스
-> 엔트리 흐름
-> 실행 판단
-> 리스크 차단
-> 로그
-> 상태 파일
-> 청산 확장
-> 회귀 검증
```

### 2.3 forced BUY 경로 금지

검증 중에는 강제 BUY 테스트를 하지 않는다.

필요 시 synthetic signal 또는 isolated unit validation을 사용한다.

## 3. 검증 범위

### Stage 1 범위

- legacy wrapper 제거
- ExecutionDecision 도입
- RiskCheckResult 도입
- risk_guard 추가
- execution_decider 추가
- signal_logger 추가
- strategy_manager signal logging 연결
- engine ExecutionDecision 연결
- state risk_metrics 도입
- config 확장
- 문서 갱신

### Stage 2 범위

- enhanced_exit_manager 추가
- trailing stop
- time exit
- partial exit
- partial qty filter 처리
- 회귀 검증

## 4. 문서 및 구조 검증

### A1. 문서 존재 확인

대상:

- `docs/CNT v1.1 ARCHITECTURE DESIGN DOCUMENT.md`
- `docs/CNT v1.1 IMPLEMENTATION WORK INSTRUCTION.md`
- `docs/CNT v1.1 IMPLEMENTATION VALIDATION CHECKLIST.md`

판정:

- 모두 존재하고 상호 참조가 맞으면 PASS

### A2. AGENTS.md 반영 확인

확인 항목:

- `ExecutionDecision`
- `risk_guard`
- `signal_logger`
- `risk_metrics`
- `signal.log`
- `enhanced_exit_manager` (Stage 2 반영 시)

### A3. EXTRA ITEMS REGISTER 반영 확인

신규 항목:

- `src/models/execution_decision.py`
- `src/models/risk_result.py`
- `src/execution_decider.py`
- `src/risk/risk_guard.py`
- `src/signal_logger.py`
- `logs/signal.log`
- `src/risk/enhanced_exit_manager.py` (Stage 2)

## 5. 파일 및 인터페이스 검증

### B1. legacy wrapper 제거 확인

대상:

- `src/strategy_signal.py`

판정:

- 참조 0건
- 파일 제거 완료
- import/runtime 에러 없음

### B2. ExecutionDecision 모델 확인

필수 필드:

- `execute`
- `action`
- `reason`
- `signal_reason`
- `strategy_name`
- `symbol`
- `validated_qty`
- `validated_price`
- `notional_value`
- `risk_check_passed`
- `risk_rejection_reason`
- `slippage_check_passed`
- `slippage_rejection_reason`

### B3. RiskCheckResult 모델 확인

필드:

- `passed`
- `reason`

### B4. signal_logger 위치 확인

대상:

- `src/signal_logger.py`

## 6. Entry Flow 검증

기대 흐름:

```text
signal = generate_strategy_signal()
-> gate = evaluate_entry_gate(...)
-> decision = execution_decider.decide_execution(...)
-> validator
-> executor
```

## 최종 의미

이 체크리스트는 activation 승인 문서가 아니라, CNT v1.1 확장 레이어가 유효한지 점검하는 기준 문서다.

## 링크

- CNT v1.1 IMPLEMENTATION VALIDATION CHECKLIST
- CNT v1.1 IMPLEMENTATION VALIDATION REPORT KO
- CNT v1.1 STAGE 2 IMPLEMENTATION VALIDATION CHECKLIST KO

## Obsidian Links

- [[CNT v1.1 ARCHITECTURE DESIGN DOCUMENT KO]]



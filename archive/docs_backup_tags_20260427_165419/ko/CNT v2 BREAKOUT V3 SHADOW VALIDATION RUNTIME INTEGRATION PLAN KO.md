---
aliases:
  - CNT v2 BREAKOUT V3 SHADOW VALIDATION RUNTIME INTEGRATION PLAN KO
---

# CNT v2 BREAKOUT V3 SHADOW VALIDATION RUNTIME INTEGRATION 계획

## 상태

- status = `PLANNED`
- implementation = `NOT STARTED`
- runtime_mode = `SHADOW_ONLY`

## 1. 범위 고정

다음 단계의 범위는 아래처럼 고정된다.

- `breakout_v3`는 계속 `shadow-only`
- live activation 금지
- order path는 미연결 상태 유지
- `ACTIVE_STRATEGIES`는 그대로 유지
- 이 단계에서 registry promotion 금지

이 계획은 runtime observation integration만 다룬다.

즉 아래를 허용하지 않는다.

- live signal consumption
- order submission
- position mutation
- ranking participation

## 2. 통합 지점

계획된 삽입 지점은 engine observation layer 내부이며,

- market context가 확보된 뒤
- shadow result가 execution behavior에 영향을 주기 전에

위치해야 한다.

계획된 runtime 흐름:

1. market context available
2. `build_breakout_v3_conditions(...)`
3. `evaluate_breakout_v3_shadow(...)`
4. shadow event serialization
5. jsonl append
6. snapshot aggregation update

필수 규칙:

- 이 흐름은 live execution path 바깥에 있어야 한다
- 아래로 feed되면 안 된다
  - `entry_gate`
  - `execution_decider`
  - `order_executor`
  - `risk_guard`
  - `portfolio_risk_manager`

## 3. 새 runtime 출력

계획된 shadow 출력:

- `logs/shadow_breakout_v3.jsonl`
- `data/shadow_breakout_v3_snapshot.json`

### 목적

`logs/shadow_breakout_v3.jsonl`

- append-only event log
- 한 줄당 하나의 shadow event
- blocker와 stage 증거를 상세하게 보존

`data/shadow_breakout_v3_snapshot.json`

- 최신 집계 요약
- 운영자용 빠른 점검 화면
- 다음 review 입력 데이터

## 4. Event Schema Lock

각 jsonl event는 최소 아래 필드를 포함해야 한다.

- `allowed`
- `summary_reason`
- `first_blocker`
- `hard_blocker`
- `soft_pass_count`
- `stage_flags`
- `condition_flags`
- `secondary_fail_reasons`
- `metadata`

권장 전체 payload:

- `timestamp`
- `symbol`
- `strategy_name`
- `allowed`
- `summary_reason`
- `first_blocker`
- `hard_blocker`
- `soft_pass_count`
- `soft_fail_count`
- `soft_total_count`
- `min_soft_pass_required`
- `stage_flags`
- `condition_flags`
- `secondary_fail_reasons`
- `metadata`

## 5. Snapshot Schema Lock

계획된 snapshot은 아래 필드를 포함해야 한다.

- `signal_count`
- `allowed_signal_count`
- `allowed_signal_ratio`
- `expanded_event_count`
- `first_blocker_distribution`
- `hard_blocker_distribution`
- `secondary_blocker_distribution`
- `soft_pass_count_distribution`
- `stage_pass_counts`
- `stage_fail_counts`
- `min_soft_pass_required`
- `soft_total_count`
- `aggregation_scope`

이 필드들은 아래 목적 때문에 필요하다.

- first-blocker review 가능
- downstream blocker review 가능
- soft-threshold behavior 가시화
- aggregation assumption 명시 유지

## 6. Runtime Safety Rules

다음 안전 규칙은 필수다.

- 어떤 shadow exception도 engine main flow를 끊으면 안 된다
- shadow logging failure는 order logic을 막으면 안 된다
- snapshot write failure는 degrade gracefully 해야 한다
- `pullback_v1`과 `breakout_v1` 동작은 그대로 유지해야 한다
- shadow event는 state 또는 portfolio file을 변경하면 안 된다

즉:

- shadow write operation에는 protective try/except가 필요하다
- live decision logic은 shadow output에 의존하면 안 된다

## 7. Validation Gate

runtime integration 이후 최소 검증 세트:

1. jsonl append 동작
2. snapshot file 생성 및 갱신
3. 기존 test suite 통과
4. runtime `action` behavior unchanged
5. `ACTIVE_STRATEGIES` unchanged
6. `breakout_v3` 때문에 예상치 못한 `pending_order` 또는 `open_trade` mutation이 없어야 함

권장 추가 검증:

- event schema에 잠금된 필드가 모두 있는지
- snapshot schema에 잠금된 필드가 모두 있는지
- engine one-shot cycle이 정상 종료되는지

## 8. Explicit Prohibitions

아래는 계속 금지된다.

- `breakout_v3` activation
- parameter tuning
- live signal consumption
- `risk_guard` connection
- `order_validator` connection
- execution path connection
- ranking participation

## 9. 모듈 경계 메모

현재 skeleton 구현은 아래를 하나의 `breakout_v3` shadow module layer 안에 두고 있다.

- evaluator
- event builder
- aggregator

다음 단계 의사결정:

- 아직 module split은 하지 않는다
- 초기 runtime integration 동안에는 current single-module approach 유지
- 첫 shadow runtime observation window 이후에만 분리를 재검토

이렇게 해야 다음 integration step이 더 작고 위험이 낮다.

## 10. 계획된 다음 단계

이 문서 다음 실제 구현 단계는 아래다.

1. `breakout_v3` shadow evaluation을 runtime에 연결
2. 아래 두 산출물에만 기록
   - `logs/shadow_breakout_v3.jsonl`
   - `data/shadow_breakout_v3_snapshot.json`
3. execution behavior는 그대로 유지

## 최종 계획 선언

`breakout_v3` runtime integration은 observation-only여야 한다.

이것은 trading branch가 아니라 shadow evaluation branch로 삽입된다.

shadow observation window에서 증거가 나오기 전까지 activation, tuning, live consumption은 모두 금지다.

## 링크

- CNT v2 BREAKOUT V3 SHADOW VALIDATION RUNTIME INTEGRATION PLAN
- CNT v2 BREAKOUT V3 SHADOW EVALUATOR IMPLEMENTATION REPORT KO
- CNT v2 BREAKOUT V3 SHADOW RUNTIME INTEGRATION IMPLEMENTATION REPORT KO

## Obsidian Links

- [[CNT v2 BREAKOUT V3 DESIGN DRAFT KO]]



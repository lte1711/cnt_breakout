---
aliases:
  - CNT v2 BREAKOUT V3 SHADOW RUNTIME INTEGRATION IMPLEMENTATION REPORT KO
---

# CNT v2 BREAKOUT V3 SHADOW RUNTIME INTEGRATION 구현 보고서

## 상태

- status = `IMPLEMENTED`
- runtime_mode = `SHADOW_ONLY`
- activation = `PROHIBITED`
- execution_path = `UNCHANGED`

## 요약

`breakout_v3` shadow evaluation은 이제 엔진에 비침투적 observation branch로 연결돼 있다.

runtime integration은 아래 동작만 수행한다.

1. `build_breakout_v3_conditions(...)`
2. `evaluate_breakout_v3_shadow(...)`
3. event serialization
4. jsonl append
5. snapshot aggregation update

아래는 하지 않는다.

- ranking 참여
- 주문 제출
- position state 변경
- `entry_gate` 영향
- `execution_decider` 영향
- `risk_guard` 영향

## 통합 지점

삽입 지점은 `src/engine.py` 내부이며, ranked signal selection과 metrics save 직후에 기존 `breakout_v2` shadow branch 옆에 배치된다.

현재 observation sequence:

1. ranked selection computed
2. strategy metrics saved
3. `breakout_v2` shadow branch runs
4. `breakout_v3` shadow branch runs
5. live selected signal continues through normal execution path

## Runtime 출력

새 observation 출력:

- `logs/shadow_breakout_v3.jsonl`
- `data/shadow_breakout_v3_snapshot.json`

### Event payload

각 event는 잠금된 shadow schema를 포함한다.

- `allowed`
- `summary_reason`
- `first_blocker`
- `hard_blocker`
- `soft_pass_count`
- `stage_flags`
- `condition_flags`
- `secondary_fail_reasons`
- `metadata`

### Snapshot payload

snapshot은 jsonl에서 집계되며 아래 필드를 포함한다.

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
- `last_updated`

## 예외 처리

runtime safety는 guarded execution으로 유지된다.

- evaluator failure는 engine flow를 중단시키지 않는다
- jsonl append failure는 trading flow에 영향을 주지 않는다
- snapshot update failure는 trading flow에 영향을 주지 않는다

즉 shadow branch는 observational only 상태를 유지한다.

## 검증

완료된 검증:

- `python -m unittest discover -s tests -p "test_*.py"`
- `python -m py_compile config.py src\\engine.py src\\shadow\\breakout_v3_shadow_eval.py tests\\test_breakout_v3_shadow_eval.py tests\\test_engine_cycle_smoke.py`

기대 보장:

- engine one-shot cycle은 계속 완료됨
- `ACTIVE_STRATEGIES` unchanged
- order path unchanged
- `breakout_v3`는 계속 `shadow-only`

## 알려진 제한사항

- runtime ranking participation 없음
- live signal consumption 없음
- activation logic 없음
- 이 단계에서는 testnet order-path verification 수행 안 함
- evaluator, IO, aggregation 사이 module split 없음

## 최종 기록

이 단계는 runtime integration skeleton만 구현한 것이다.

`breakout_v3`는 이제 engine에서 관측 가능하지만, live execution behavior와는 완전히 분리된 상태다.

## 링크

- CNT v2 BREAKOUT V3 SHADOW RUNTIME INTEGRATION IMPLEMENTATION REPORT
- CNT v2 BREAKOUT V3 SHADOW RUNTIME ONE-SHOT VERIFICATION KO
- CNT v2 BREAKOUT V3 SHADOW OBSERVATION WINDOW START KO

## Obsidian Links

- [[CNT v2 BREAKOUT V3 DESIGN DRAFT KO]]



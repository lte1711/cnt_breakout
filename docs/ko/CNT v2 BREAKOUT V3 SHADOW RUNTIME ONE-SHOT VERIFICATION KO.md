---
tags:
  - cnt
  - breakout
  - v3
  - shadow
  - verification
  - ko
aliases:
  - CNT v2 BREAKOUT V3 SHADOW RUNTIME ONE-SHOT VERIFICATION KO
---

# CNT v2 BREAKOUT V3 SHADOW RUNTIME 원샷 검증

## 상태

- verification_type = `ONE_SHOT_RUNTIME_OUTPUT_CHECK`
- result = `PASS`
- runtime_mode = `SHADOW_ONLY`
- activation = `PROHIBITED`

## 실행 기록

- entry_chain = `run.ps1 -> main.py -> src.engine.start_engine`
- execution_time = `2026-04-24T02:04:04+09:00`
- execution_count = `1`

## 검증 대상

이번 one-shot 검증은 새로운 `breakout_v3` shadow branch의 runtime 배선만 확인했다.

1. `logs/shadow_breakout_v3.jsonl` 생성
2. 최소 1개 event append
3. `data/shadow_breakout_v3_snapshot.json` 생성
4. snapshot schema shape
5. runtime action이 정상 engine flow 안에 남아 있는지
6. `breakout_v3`가 order 또는 position state에 연결되지 않았는지

## 파일 생성 결과

### Jsonl

- file = `logs/shadow_breakout_v3.jsonl`
- result = `CREATED`
- sample_event_count = `1`

tail event:

- `strategy_name = breakout_v3_candidate`
- `allowed = false`
- `summary_reason = regime_blocked`
- `first_blocker = market_not_trend_up`
- `hard_blocker = market_not_trend_up`
- `soft_pass_count = 2`

### Snapshot

- file = `data/shadow_breakout_v3_snapshot.json`
- result = `CREATED`

확인된 snapshot 필드:

- `signal_count = 1`
- `allowed_signal_count = 0`
- `allowed_signal_ratio = 0.0`
- `expanded_event_count = 1`
- `first_blocker_distribution`
- `hard_blocker_distribution`
- `secondary_blocker_distribution`
- `soft_pass_count_distribution`
- `stage_pass_counts`
- `stage_fail_counts`
- `min_soft_pass_required = 3`
- `soft_total_count = 6`
- `aggregation_scope = all_breakout_v3_shadow_events`
- `strategy = breakout_v3_shadow`
- `last_updated`

## Runtime Safety Check

one-shot 실행 후 state:

- `strategy_name = breakout_v1`
- `action = NO_ENTRY_SIGNAL`
- `pending_order = null`
- `open_trade = null`

해석:

- engine은 정상 one-shot cycle을 완료했다
- 예상치 못한 position mutation은 없었다
- `breakout_v3` activation은 일어나지 않았다
- live order path consumption도 없었다

## 예외

- runtime execution exception = `NONE OBSERVED`
- shadow file creation exception = `NONE OBSERVED`

## 최종 판정

`breakout_v3` shadow runtime output verification = `PASS`

즉 이 shadow branch는 아래를 만족한다.

- engine cycle 내부에서 실행됨
- jsonl event를 남김
- snapshot을 남김
- live trading behavior와 완전히 분리됨

## 다음 단계

다음 유효 단계:

- `breakout_v3 shadow observation window start`

직접 activation, tuning, order-path connection은 계속 금지다.

## 링크

- [[CNT v2 BREAKOUT V3 SHADOW RUNTIME ONE-SHOT VERIFICATION]]
- [[CNT v2 BREAKOUT V3 SHADOW OBSERVATION WINDOW START KO]]
- [[CNT v2 BREAKOUT V3 SHADOW RUNTIME INTEGRATION IMPLEMENTATION REPORT KO]]

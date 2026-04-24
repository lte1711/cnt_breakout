---
---

# CNT v2 BREAKOUT V2 SHADOW RUNTIME INTEGRATION KO

## 목적

이 문서는 `breakout_v2`를 production execution path에 넣지 않고 runtime에서 shadow candidate로 통합하는 방식을 정의한다.

현재 단계:

- `breakout_v2` 구현됨
- `breakout_v2` registry 등록됨
- 여전히 off
- direct production activation 금지

## 통합 지점

`breakout_v2` shadow evaluation은 **market context 생성 후**, **execution path 바깥에서** 수행되어야 한다.

권장 위치:

1. market context created
2. active strategies evaluated as usual
3. `breakout_v2` shadow evaluated separately
4. shadow result written to shadow output only
5. execution continues using active strategy output only

## 왜 execution path 밖에 있어야 하나

`breakout_v2`는 아직 candidate다.

shadow 결과가 execution component로 들어가면:

- current runtime baseline 오염
- validation discipline 파손
- hypothetical / real trade 혼합 위험

따라서:

- `order_router` 연결 금지
- `execution_decider` 연결 금지
- order submission path 금지

## 왜 `ACTIVE_STRATEGIES`는 그대로 두는가

현재 production runtime은 여전히 다음 기준에 의존한다.

- `breakout_v1` as reference baseline
- `pullback_v1` as active profitable strategy

지금 `ACTIVE_STRATEGIES`를 바꾸면 validation이 production mutation으로 바뀐다.

## 비교 논리

shadow candidate는 다음과 비교되어야 한다.

1. `breakout_v1 final reference`
2. `breakout_v2 shadow candidate`
3. `mixed portfolio baseline`

## 출력 파일 위치

권장 파일:

- `data/shadow_breakout_v2_snapshot.json`
- `logs/shadow_breakout_v2.jsonl`

### snapshot 목적

operator review와 dashboard-style 점검용 aggregate summary

### append log 목적

후속 검토/집계를 위한 per-event append-only shadow record

## logging schema 최소 필드

- `ts`
- `symbol`
- `strategy`
- `signal_generated`
- `entry_allowed`
- `filter_reason`
- `confidence`
- `vwap`
- `band_width_ratio`
- `band_expansion_ratio`
- `volume_ratio`
- `hypothetical_entry`

## snapshot schema 최소 필드

- `signal_count`
- `filtered_signal_count`
- `allowed_signal_count`
- `filtered_signal_ratio`
- `allowed_signal_ratio`
- `hypothetical_trades_count`
- `hypothetical_expectancy`
- `hypothetical_profit_factor`
- `stop_exit_ratio`
- `reason_distribution`
- `last_updated`

## 구현 형태

권장 helper module:

- `src/shadow_eval.py`

책임:

- shadow mode `breakout_v2` 평가
- shadow jsonl append
- shadow snapshot aggregate 갱신

## 경계 규칙

shadow result는 절대로 다음으로 전달되면 안 된다.

- order validation
- execution decision
- order routing
- pending/open trade state mutation

## 링크

- CNT v2 BREAKOUT V2 SHADOW VALIDATION SPEC KO
- CNT v2 BREAKOUT V2 VALIDATION WINDOW START KO

## Obsidian Links

- [[CNT v2 BREAKOUT V2 DESIGN KO]]



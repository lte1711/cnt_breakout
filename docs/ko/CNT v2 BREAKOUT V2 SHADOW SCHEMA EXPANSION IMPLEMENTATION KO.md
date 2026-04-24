---
aliases:
  - CNT v2 BREAKOUT V2 SHADOW SCHEMA EXPANSION IMPLEMENTATION KO
---

# CNT v2 BREAKOUT V2 Shadow Schema 확장 구현

## 요약

`breakout_v2` shadow event schema는 additive 방식으로 확장되었고, production execution path를 바꾸지 않으면서 downstream filter-chain 분석이 가능해졌다.

## 추가된 필드

새 shadow event field:

- `secondary_fail_reasons`
- `evaluated_stage_trace`
- `stage_flags`

### `secondary_fail_reasons`

기본 `filter_reason` 외의 추가 실패 조건을 저장한다.

### `evaluated_stage_trace`

아래 필드를 갖는 ordered stage trace를 저장한다.

- `stage`
- `passed`
- `reason`

### `stage_flags`

compact per-stage boolean:

- `market_bias_pass`
- `volatility_pass`
- `ema_pass`
- `rsi_threshold_pass`
- `breakout_confirmed`
- `vwap_distance_pass`
- `band_width_pass`
- `band_expansion_pass`
- `volume_pass`

## 왜 Additive Design을 선택했는가

additive design을 고른 이유:

1. 기존 shadow consumer를 계속 살리기 위해
2. historical jsonl entry를 계속 읽을 수 있게 하기 위해
3. snapshot aggregation을 안정적으로 유지하기 위해
4. production execution behavior를 바꾸지 않기 위해

## Backward Compatibility 전략

아래 original field는 그대로 유지된다.

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

snapshot schema는 minimum-change rule을 유지한다.

이 단계에서는 required snapshot consumer 변경이 도입되지 않았다.

## 업데이트된 파일

- `src/shadow_eval.py`
- `tests/test_shadow_eval.py`

## Execution Path 안전성

이 확장은 shadow event richness만 바꾼다.

즉 아래는 하지 않는다.

- `breakout_v2` activation
- `ACTIVE_STRATEGIES` 변경
- shadow output을 execution decision에 연결
- shadow output을 order submission에 연결

## 확장 이후 남는 제한사항

schema 확장 이후에도:

- shadow output은 여전히 hypothetical이다
- `hypothetical_expectancy`는 placeholder-only
- `hypothetical_profit_factor`도 placeholder-only
- `stop_exit_ratio`도 placeholder-only

즉 이 단계는 profitability proof가 아니라 causal observability 향상 단계다.

## 링크

- CNT v2 BREAKOUT V2 SHADOW SCHEMA EXPANSION IMPLEMENTATION
- CNT v2 BREAKOUT V2 SHADOW SCHEMA EXPANSION PLAN KO
- CNT v2 BREAKOUT V2 GATE REDUNDANCY REVIEW KO

## Obsidian Links

- [[CNT v2 BREAKOUT V2 DESIGN KO]]



---
tags:
  - cnt
  - type/documentation
  - status/active
  - type/validation
  - type/operation
  - risk
  - strategy/breakout_v3
  - cnt-v2-breakout-v2-shadow-schema-expansion-plan-ko
---

# CNT v2 BREAKOUT V2 Shadow Schema 확장 계획

## 목적

이 계획은 `breakout_v2` shadow observation의 schema를 안전하게 확장해, 이후 tuning 판단이 근거 중심이 되도록 만들기 위한 문서다.

이 문서는 schema / observability 계획일 뿐이다.

즉:

- activation plan이 아니다
- tuning plan도 아니다

## 확장 목표

expanded shadow schema는 아래를 가능하게 해야 한다.

- per-event secondary failure visibility
- per-stage pass/fail reconstruction
- first blocker와 downstream blocker의 분리 강화

## 제안 추가 항목

### 1. `secondary_fail_reasons`

권장 event field:

```json
"secondary_fail_reasons": ["ema_fast_not_above_slow", "band_width_too_narrow"]
```

목적:

- first blocker 이후에도 발생했을 추가 실패를 보존
- runtime behavior를 바꾸지 않고 conditional subset review를 가능하게 함

### 2. `evaluated_stage_trace`

권장 event field:

```json
"evaluated_stage_trace": [
  {"stage": "range_bias", "passed": true},
  {"stage": "volatility", "passed": false},
  {"stage": "ema", "passed": false},
  {"stage": "breakout_confirmation", "passed": true}
]
```

목적:

- 실제 평가 순서를 보존
- 가정이 적은 stage-by-stage decomposition 지원

### 3. Optional Per-Stage Pass/Fail Flags

trace array보다 단순할 경우 권장 flat field:

- `stage_range_bias_passed`
- `stage_volatility_passed`
- `stage_ema_passed`
- `stage_breakout_confirmation_passed`
- `stage_vwap_distance_passed`
- `stage_band_width_passed`
- `stage_band_expansion_passed`
- `stage_volume_passed`

목적:

- downstream aggregation 단순화
- review query 간소화

## Backward Compatibility

backward compatibility는 반드시 유지되어야 한다.

규칙:

1. 기존 event key는 계속 유효해야 한다
2. 기존 snapshot field는 계속 유효해야 한다
3. 새 필드는 additive only여야 한다
4. old event에 새 필드가 없어도 log parsing이 깨지면 안 된다

## 권장 Rollout Shape

1. shadow event schema만 먼저 확장
2. 기존 snapshot schema는 유지
3. richer event가 충분히 누적된 뒤 optional aggregation을 추가 검토

이 방식은 rollout을 보수적으로 유지하고 기존 validation baseline 오염을 피한다.

## 바뀌면 안 되는 것

- `breakout_v2` actual activation은 계속 금지
- `ACTIVE_STRATEGIES` unchanged
- execution path unchanged
- risk guard unchanged
- KPI calculation unchanged

## 최종 권고

`schema expansion required before further tuning decisions`

## 링크

- CNT v2 BREAKOUT V2 SHADOW SCHEMA EXPANSION PLAN
- CNT v2 BREAKOUT V2 SHADOW SCHEMA EXPANSION IMPLEMENTATION KO
- CNT v2 BREAKOUT V2 EXPANDED SHADOW OBSERVATION REVIEW KO

## Obsidian Links

- [[CNT v2 BREAKOUT V2 DESIGN KO]]



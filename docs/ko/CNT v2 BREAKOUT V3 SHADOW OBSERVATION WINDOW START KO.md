---
tags:
  - cnt
  - type/documentation
  - status/active
  - market-context
  - type/operation
  - strategy/breakout_v3
  - status/completed
  - cnt-v2-breakout-v3-shadow-observation-window-start-ko
---

# CNT v2 BREAKOUT V3 SHADOW OBSERVATION WINDOW START (한글판)

## 상태

- status = `ACTIVE`
- runtime_mode = `SHADOW_ONLY`
- activation = `PROHIBITED`
- tuning = `PROHIBITED`

## 시작 기준

- baseline_commit = `8b6e772`
- window_start_time = `2026-04-24T02:04:04+09:00`
- verification_source = CNT v2 BREAKOUT V3 SHADOW RUNTIME ONE-SHOT VERIFICATION

이 관측 창은 다음 3개가 모두 완료된 뒤 시작됐다.

1. `breakout_v3` shadow evaluator skeleton 구현
2. runtime integration skeleton 구현
3. one-shot runtime output verification 완료

## 기준선 스냅샷

### breakout_v3 shadow baseline

- `signal_count = 1`
- `allowed_signal_count = 0`
- `allowed_signal_ratio = 0.0`
- `expanded_event_count = 1`
- `first_blocker_distribution.market_not_trend_up = 1`
- `soft_pass_count_distribution.2 = 1`
- `stage_fail_counts.regime = 1`
- `stage_fail_counts.setup = 1`
- `stage_fail_counts.trigger = 1`
- `stage_fail_counts.quality = 1`

### 시스템 baseline

- performance snapshot timestamp = `2026-04-24 02:04:04`
- live gate = `LIVE_READY / ALL_GATES_PASSED`
- mixed portfolio:
  - `closed_trades = 34`
  - `expectancy = 0.00013499999999991123`
  - `net_pnl = 0.004589999999996985`
  - `profit_factor = 1.0154123560757822`
- current runtime state:
  - `strategy_name = breakout_v1`
  - `action = NO_ENTRY_SIGNAL`
  - `pending_order = null`
  - `open_trade = null`
  - `daily_loss_count = 2`

## 관측 목적

이 관측 창은 아래 질문에 답하기 위해 존재한다.

1. `breakout_v3`가 실제 shadow 후보를 만들어내는가
2. 시간이 지나며 어떤 stage가 first blocker를 지배하는가
3. hard gate는 통과하지만 soft pool에서 막히는 경우가 얼마나 자주 나오는가
4. `soft_pass_count` 분포가 미래 후보 전략으로서 의미 있는 구간을 보이는가
5. downstream failure가 특정 소수 조건에 집중되는가, 아니면 넓게 분산되는가

## 필수 추적 항목

- `signal_count`
- `allowed_signal_count`
- `allowed_signal_ratio`
- `first_blocker_distribution`
- `hard_blocker_distribution`
- `secondary_blocker_distribution`
- `soft_pass_count_distribution`
- `stage_pass_counts`
- `stage_fail_counts`

## 관측 규칙

- `breakout_v3`는 계속 `shadow-only`
- `ACTIVE_STRATEGIES`는 변경하지 않음
- 주문 경로 연결 금지
- ranking 참여 금지
- 초기 관측 창 동안 parameter tuning 금지
- 단일 gate shortcut relaxation 금지

## 초기 해석 규칙

초기 데이터는 방향성 지표로만 취급한다.

one-shot verification baseline을 넘어서는 의미 있는 표본이 쌓이기 전까지는 구조적 결론을 확정하지 않는다.

## 다음 리뷰 트리거

다음 formal review는 의미 있는 새 shadow 표본이 쌓인 뒤에 수행한다.

권장 기준:

- `20 to 30 additional breakout_v3 shadow events`

그 시점에는 다음을 다루는 전용 observation review를 작성한다.

- blocker distributions
- hard-pass vs soft-fail behavior
- `breakout_v3`가 미래 후보 전략으로 보이는지, 아니면 여전히 구조적으로 막혀 있는지

## 최종 기록

`breakout_v3`는 이제 유효한 shadow observation phase에 들어와 있다.

runtime에 연결되어 관측 산출물을 만들지만, live execution behavior와는 완전히 분리된 상태를 유지한다.

## Obsidian Links

- [[CNT v2 BREAKOUT V3 DESIGN DRAFT KO]]



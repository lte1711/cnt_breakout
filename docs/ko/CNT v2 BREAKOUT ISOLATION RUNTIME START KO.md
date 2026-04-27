---
tags:
  - cnt
  - type/documentation
  - status/active
  - type/operation
  - strategy/pullback_v1
  - strategy/breakout_v3
  - obsidian
  - cnt-v2-breakout-isolation-runtime-start-ko
---

# CNT v2 BREAKOUT 격리 런타임 시작

## 목적

이 문서는 대시보드 경고 패치와 gate/display 정합성 패치가 적용된 뒤, `breakout_v1` 격리 관측 런타임 창을 시작하기 위한 기록이다.

목표는 `breakout_v1`를 즉시 비활성화하는 것이 아니다.  
목표는 나머지 시스템은 그대로 둔 상태에서, 현재 런타임 안에서 breakout이 계속 음수 기여를 만드는지 관측하는 것이다.

## 관측 시작점

- baseline commit: `be75061`
- isolation runtime start time: `2026-04-22 13:40:36`
- start label: `STRUCTURALLY_HEALTHY, PERFORMANCE_DEGRADED`
- start gate: `FAIL / NON_POSITIVE_EXPECTANCY`
- observation start snapshot: `2026-04-22 12:44:03`

## 시작 기준선 지표

- mixed portfolio observed
  - `expectancy = -0.0007807916666668097`
  - `profit_factor = 0.9158659890090017`
  - `execution_rate = 24 / 86 = 27.91%`
  - `execution_block_rate = 62 / 86 = 72.09%`
  - `no_candidate_rate = 244 / 330 = 73.94%`
- breakout observed baseline
  - `trades_closed = 3`
  - `expectancy = -0.022197999999999656`
  - `profit_factor = 0.17295081967214201`
- pullback inferred baseline
  - `trades_closed = 21`
  - `expectancy = 0.0022788095238093107`
  - `profit_factor = 1.3365141201619735`

## 비교 축

이 런타임 리뷰는 반드시 아래 세 관점을 분리해서 유지해야 한다.

1. `mixed portfolio`
2. `breakout observed baseline`
3. `pullback inferred baseline`

중요:

- `mixed portfolio`는 관측값이다
- `breakout observed baseline`도 관측값이다
- `pullback inferred baseline`은 strategy metrics 기반 추정치이며, 관측된 포트폴리오 런타임이라고 표현하면 안 된다

## 추적 지표

- expectancy
- profit_factor
- execution_rate
- execution_block_rate
- no_candidate_rate

## 중간 점검

- `10 additional cycles` 뒤 midpoint review
- 확인할 내용:
  - breakout expectancy가 여전히 음수인지
  - mixed portfolio expectancy가 회복 중인지 악화 중인지
  - execution throughput이 개선되는지 아니면 계속 막혀 있는지

## 종료 조건

이 격리 창은 아래 세 결론 중 하나로만 끝내야 한다.

1. `breakout quality recover`
2. `breakout remains negative`
3. `insufficient sample`

## 저표본 경고

`breakout_v1`는 아직 관측 표본 수가 작다.  
추가 거래 수가 적은 상태에서 과도한 확정 결론을 내려서는 안 된다.

## 필수 보고 규칙

모든 post-window 보고서는 아래를 보존해야 한다.

- 원래의 `LIVE_READY` 기록
- 현재의 `FAIL / NON_POSITIVE_EXPECTANCY` 기록
- observed baseline과 inferred baseline의 차이

## Obsidian Links

- [[CNT v2 BREAKOUT QUALITY EVALUATION REPORT KO]]



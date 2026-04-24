---
tags:
  - cnt
  - breakout
  - isolation
  - review
aliases:
  - CNT v2 BREAKOUT ISOLATION FINAL REVIEW KO
---

# CNT v2 BREAKOUT 격리 최종 리뷰

## 격리 창 상태

- `isolation review closed`
- `baseline locked`
- `no further midpoint waiting`

## 목적

이 문서는 midpoint target을 넘겼음에도 breakout 거래 증가가 의미 있게 나타나지 않았기 때문에, 현재 `breakout_v1` 격리 창을 종료하기 위한 리뷰다.

## 기준선 대비 최신 변화

- isolation baseline snapshot:
  - `2026-04-22 12:44:03`
  - `total_signals = 660`
- latest review snapshot:
  - `2026-04-22 14:44:04`
  - `total_signals = 684`
- observed additional cycles:
  - `(684 - 660) / 2 = 12`

## Breakout_v1 관측 결과

- baseline
  - `trades_closed = 3`
  - `expectancy = -0.022197999999999656`
  - `profit_factor = 0.17295081967214201`

- latest
  - `trades_closed = 3`
  - `expectancy = -0.022197999999999656`
  - `profit_factor = 0.17295081967214201`

해석:

- breakout 관측 거래 표본이 늘지 않았다
- breakout 관측 품질도 회복되지 않았다

## Mixed Portfolio 결과

- baseline
  - `expectancy = -0.0007807916666668097`
  - `profit_factor = 0.9158659890090017`
  - `net_pnl = -0.018739000000003447`

- latest
  - `expectancy = -0.0007807916666668097`
  - `profit_factor = 0.9158659890090017`
  - `net_pnl = -0.018739000000003447`

해석:

- mixed portfolio는 여전히 degraded 상태다
- 이 창 안에서는 recovery signal이 확인되지 않았다

## Pullback 추정 참조

- `trades_closed = 21`
- `expectancy = 0.0022788095238093107`
- `profit_factor = 1.3365141201619735`

해석:

- pullback은 여전히 양수 참조 전략이다
- 다만 이건 따로 격리 관측한 포트폴리오가 아니라 추정 참조선이다

## 런타임 패턴 요약

창을 닫는 구간에서 자주 보인 결과는 다음과 같다.

- `DAILY_LOSS_LIMIT`
- `no_ranked_signal`

마감 구간의 관측 시퀀스:

- 반복되는 `EXECUTION_BLOCKED_BY_RISK`
- 반복되는 `NO_ENTRY_SIGNAL`
- 새로운 breakout close event 없음

## 저표본 한계

`breakout_v1`는 여전히 관측 거래 표본이 적다.

따라서 이 리뷰는 관측 사실 이상으로 과도한 확정성을 주장하면 안 된다.  
올바른 결론은 `trades_closed = 3`이 그대로라는 한계를 인정하는 범위 안에서만 내려야 한다.

## 필수 포함 항목

이 리뷰는 반드시 아래를 포함한다.

- baseline versus latest delta
- `breakout_v1 observed` result
- `mixed portfolio observed` result
- `pullback inferred` reference

## 필수 최종 판정

- `breakout remains negative, with low-sample limitation`

## Baseline 보존 규칙

이 리뷰는 아래를 보존해야 한다.

- 원래의 `LIVE_READY` 기록
- 이후의 `FAIL / NON_POSITIVE_EXPECTANCY` 기록
- observed baseline과 inferred baseline의 차이

## Obsidian Links

- [[CNT v2 BREAKOUT ISOLATION RUNTIME START]]
- [[CNT v2 BREAKOUT ISOLATION MIDPOINT CHECK]]
- [[CNT v2 POST-READY DEGRADATION REVIEW]]

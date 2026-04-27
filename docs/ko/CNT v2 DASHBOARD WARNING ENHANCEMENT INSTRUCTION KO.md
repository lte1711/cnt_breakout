---
tags:
  - cnt
  - type/documentation
  - status/active
  - type/operation
  - risk
  - strategy/breakout_v3
  - obsidian
  - cnt-v2-dashboard-warning-enhancement-instruction-ko
---

# CNT v2 대시보드 경고 강화 지시

## 목적

현재 dashboard는 올바른 runtime 파일을 이미 로드하고 있지만, post-ready degradation signal을 화면 상단에 더 직접적으로 보여줄 필요가 있다.

## 필수 경고 추가

다음 경고를 top alert area에서 더 눈에 띄게 노출한다.

1. `FAIL reason`
2. `expectancy < 0`
3. `PF < 1`
4. `daily_loss_count reached`
5. `breakout_v1 negative expectancy`

## 정확한 경고 대상

### A. Fail Reason Banner

`live_gate_decision.status = FAIL`이면 아래를 표시:

- `FAIL`
- `reason = NON_POSITIVE_EXPECTANCY` 또는 현재 evaluator reason

이건 gate card 안의 secondary text가 아니라, 그 위나 옆에서 바로 보여야 한다.

### B. Negative Expectancy Warning

`snapshot.expectancy <= 0`이면 표시:

- `EXPECTANCY BELOW ZERO`

현재 값을 함께 포함한다.

### C. PF Below One Warning

`snapshot.profit_factor < 1`이면 표시:

- `PF BELOW 1`

현재 PF 값을 함께 포함한다.

### D. Daily Loss Count Warning

`state.risk_metrics.daily_loss_count >= 3`이면 표시:

- `DAILY LOSS COUNT REACHED`

이건 cumulative `DAILY_LOSS_LIMIT` runtime hit와는 다른 개념이므로 분리해서 표시해야 한다.

### E. Breakout Negative Expectancy Warning

`metrics.breakout_v1.expectancy < 0`이면 표시:

- `BREAKOUT NEGATIVE EXPECTANCY`

포함 항목:

- current breakout expectancy
- current breakout PF
- current breakout trades_closed

## UI 위치

권장 위치:

- 첫 번째 row alert stack
- 또는 `System Health` 위 dedicated top banner

이 경고들은 스크롤 없이 보여야 한다.

## 왜 필요한가

현재 dashboard는 이미 보여준다.

- system state
- gate state
- baseline delta

하지만 operator가 `LIVE_READY`를 왜 잃었는지를 즉시 보게 만들지는 못한다.

이번 warning enhancement는 그 해석 지연을 줄이는 것이 목적이다.

## 필수 결론

**gate/display consistency patch required**

## Obsidian Links

- [[CNT DATA DASHBOARD KO]]



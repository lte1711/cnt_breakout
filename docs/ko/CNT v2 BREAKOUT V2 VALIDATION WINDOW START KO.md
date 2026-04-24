---
---

# CNT v2 BREAKOUT V2 VALIDATION WINDOW START KO

## 상태

- validation window started
- `breakout_v2`는 아직 `ACTIVE_STRATEGIES`에 없음
- production switch 금지

## 시작 시각

- validation start timestamp: `2026-04-22 14:52:46`

## baseline 참조

### breakout_v1 final reference

- isolation final review:
  - CNT v2 BREAKOUT ISOLATION FINAL REVIEW KO
- observed baseline
  - `trades_closed = 3`
  - `expectancy = -0.022197999999999656`
  - `profit_factor = 0.17295081967214201`

### mixed portfolio reference

- snapshot timestamp: `2026-04-22 14:44:04`
- `closed_trades = 24`
- `expectancy = -0.0007807916666668097`
- `profit_factor = 0.9158659890090017`
- `net_pnl = -0.018739000000003447`

### pullback reference

- reference type: `inferred`
- `trades_closed = 21`
- `expectancy = 0.0022788095238093107`
- `profit_factor = 1.3365141201619735`

## 비교 축

- `A arm = breakout_v1 reference baseline`
- `B arm = breakout_v2 candidate`

## validation 메트릭

- `trades_closed`
- `expectancy`
- `profit_factor`
- `net_pnl`
- `win_rate`
- `execution_rate`
- `filtered_signal_ratio`
- `stop_exit_ratio`

## breakout_v2 mode

- `BREAKOUT_V2_MODE = off`

의미:

- 전략 구현됨
- registry 등록됨
- production runtime에서는 비활성
- candidate validation은 이후 controlled/shadow step으로만 시작 가능

## 게이트

### Promotion

- minimum sample reached
- `expectancy > 0`
- `profit_factor > 1`
- severe regression 없음
- 구조/로그 이슈 없음

### Rejection

- sample 부족
- `expectancy <= 0`
- `profit_factor <= 1`
- stop exit pressure 우세
- runtime / logging integrity 저하

## 운영 규칙

- `breakout_v2` 즉시 활성화 금지
- `breakout_v1` 제거 금지
- risk guard 완화 금지
- KPI 계산 로직 변경 금지

## 링크

- CNT v2 BREAKOUT V2 DESIGN KO
- CNT v2 BREAKOUT V2 CANDIDATE VALIDATION START KO
- CNT v2 BREAKOUT ISOLATION FINAL REVIEW KO

## Obsidian Links

- [[CNT v2 BREAKOUT V2 DESIGN KO]]



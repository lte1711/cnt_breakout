---
tags:
  - cnt
  - breakout
  - validation
  - shadow
---

# CNT v2 BREAKOUT V2 SHADOW VALIDATION SPEC KO

## 목적

이 문서는 `breakout_v2`의 shadow validation 모드를 정의한다.

현재 단계:

- `breakout_v2` 구현 완료
- `breakout_v2` registry 등록 완료
- production runtime에서는 비활성

shadow validation의 목적은 실제 주문 없이, 고정된 `breakout_v1` reference 대비 `breakout_v2` signal quality를 비교하는 것이다.

## shadow validation mode

### 핵심 규칙

`breakout_v2` signal calculation은 허용된다.  
실제 주문 제출은 금지된다.

### shadow 출력 규칙

`breakout_v2`는 오직 shadow candidate로만 취급한다.

즉:

- signal evaluation 가능
- filtering 기록 가능
- allowed candidate count 기록 가능
- hypothetical trade tracking 기록 가능
- `breakout_v2`로 production order 전송 금지

## 비교 대상

1. `breakout_v1 final reference`
2. `breakout_v2 shadow candidate`
3. `mixed portfolio baseline`

중요:

- `breakout_v1 final reference`는 observed
- `breakout_v2 shadow candidate`는 hypothetical
- `mixed portfolio baseline`은 observed

## 필수 shadow 메트릭

- `signal_count`
- `filtered_signal_ratio`
- `allowed_signal_ratio`
- `hypothetical_trades_count`
- `hypothetical_expectancy`
- `hypothetical_profit_factor`
- `stop_exit_ratio`
- `reason_distribution`

## shadow logging 규칙

shadow validation은 반드시 다음을 엄격히 구분해야 한다.

- real runtime outcomes
- shadow-only hypothetical outcomes

shadow candidate를 observed production strategy로 보고하면 안 된다.

## activation은 여전히 off

다음이 모두 만족되기 전까지 `breakout_v2`는 off 상태 유지:

- minimum sample reached
- `hypothetical_expectancy > 0`
- `hypothetical_profit_factor > 1`
- 구조/로그 이슈 없음
- locked references 대비 severe regression risk 없음

## pre-activation gate

- `ACTIVE_STRATEGIES` 변경 금지
- risk guard 변경 금지
- KPI 계산 변경 금지
- direct production switch 금지

## 링크

- [[CNT v2 BREAKOUT V2 DESIGN KO]]
- [[CNT v2 BREAKOUT V2 VALIDATION WINDOW START KO]]
- [[CNT v2 BREAKOUT ISOLATION FINAL REVIEW KO]]

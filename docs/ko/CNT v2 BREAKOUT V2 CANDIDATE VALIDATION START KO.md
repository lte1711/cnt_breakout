---
tags:
  - cnt
  - breakout
  - validation
  - candidate
---

# CNT v2 BREAKOUT V2 CANDIDATE VALIDATION START KO

## 목적

이 문서는 `breakout_v2`의 다음 validation window 시작 조건을 정의한다.

`breakout_v2`는 구현 및 등록은 완료됐지만 active는 아니다.
이 문서는 활성화 문서가 아니라, 이후 candidate validation 시작 조건을 고정하는 문서다.

참조:

- 현재 `breakout_v1` final isolation review
  - [[CNT v2 BREAKOUT ISOLATION FINAL REVIEW KO]]

## 시작 조건

`breakout_v2` candidate validation window는 다음 조건이 모두 충족된 뒤에만 시작할 수 있다.

- 현재 `breakout_v1` isolation window 종료
- isolation verdict 확정
- working tree hygiene 회복
- logging integrity 확인
- strategy registry integrity 확인
- 시작 결정 전까지 `ACTIVE_STRATEGIES` 변경 없음

이 validation window가 명시적으로 시작되기 전까지 activation은 금지다.

## 표본 목표

권장 최소:

- `trades_closed >= 5`

더 높은 신뢰 목표:

- `trades_closed >= 8`

## 추적 메트릭

- `trades_closed`
- `expectancy`
- `profit_factor`
- `net_pnl`
- `win_rate`
- `execution_rate`
- `filtered_signal_ratio`
- `stop_exit_ratio`

## 승격 게이트

다음이 모두 참일 때만 promotion 검토 가능:

- 표본 목표 도달
- `expectancy > 0`
- `profit_factor > 1`
- 현재 breakout baseline 대비 심각한 regression 없음
- 구조/로그 이슈 없음

## 거절 게이트

다음 중 하나라도 참이면 우선 reject:

- 표본 부족
- `expectancy <= 0`
- `profit_factor <= 1`
- stop exit 비중 과다
- runtime 또는 logging integrity 저하

## 운영 규율

- `breakout_v2` 활성화 금지
- `breakout_v1` 제거 금지
- risk guard 완화 금지
- KPI 계산 변경 금지

## 링크

- [[CNT v2 BREAKOUT V2 DESIGN KO]]
- [[CNT v2 BREAKOUT ISOLATION FINAL REVIEW KO]]

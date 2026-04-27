---
tags:
  - cnt
  - type/documentation
  - status/active
  - type/operation
  - risk
  - strategy/pullback_v1
  - strategy/breakout_v3
  - obsidian
  - type/analysis
  - type/validation
  - status/completed
  - status/final
  - language:-ko
---

# CNT v2 BREAKOUT V1 ACTIVE ISOLATION DECISION

## 요약

`breakout_v1`를 런타임 active set에서 제외한다.

이 조치는 전략 삭제가 아니라 운영 격리 결정이다.

## 왜 이 결정을 했는가

최신 검증 기준에서 다음이 확인되었다.

- `breakout_v1 expectancy = -0.022198`
- `breakout_v1 profit_factor = 0.17295`
- `breakout_v1 trades_closed = 3`
- 전체 `LIVE_GATE = FAIL / NON_POSITIVE_EXPECTANCY`

동시에 다음도 이미 정리된 상태였다.

- `pullback_v1`는 여전히 양수 전략
- `breakout_v3` shadow observation은 rebaseline 완료
- shadow/output semantics와 portfolio risk sync 문제도 정리 완료

즉 이제 가장 큰 남은 운영 문제는 관측층이나 상태 동기화가 아니라,
`ACTIVE_STRATEGIES` 안에 `breakout_v1`가 계속 남아 있는 점이었다.

## 결정

런타임 설정을 아래처럼 변경한다.

- `ACTIVE_STRATEGY = pullback_v1`
- `ACTIVE_STRATEGIES = [pullback_v1]`

단, `breakout_v1`는 다음 상태로 유지한다.

- 소스 코드 보존
- strategy registry 등록 유지
- 기존 metrics와 문서 기록 유지

즉 현재 live candidate set에서만 제외된다.

## 범위

이번 변경은 다음을 하지 않는다.

- `breakout_v3` 활성화
- 주문 정책 변경
- risk guard 규칙 변경
- `breakout_v1` 삭제
- ranker 구조 재작성

즉 음수 전략을 active runtime set에서 격리하는 최소 조치만 수행한다.

## 검증 항목

격리 패치 후 아래를 확인해야 한다.

1. 테스트 전체 통과
2. `py_compile` 통과
3. `run.ps1` one-shot 정상 완료
4. runtime action 정상 유지
5. execution path regression 없음

## 운영 해석

이 결정 이후 상태는 다음처럼 본다.

- `pullback_v1` = 현재 live strategy
- `breakout_v1` = inactive archived reference
- `breakout_v3` = shadow-only observation strategy

## 결론

`breakout_v1` active-set isolation은 현재 남아 있는 live performance contamination source를 직접 줄이는 가장 작은 유효 운영 변경이다.

## Obsidian Links

- [[CNT v2 BREAKOUT QUALITY EVALUATION REPORT KO]]



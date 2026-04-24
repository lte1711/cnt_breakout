---
---

# CNT v2 BREAKOUT V2 SHADOW RUNTIME IMPLEMENTATION KO

## 요약

`breakout_v2` shadow runtime integration은 production execution path를 바꾸지 않는 형태로 구현되었다.

현재 상태:

- `breakout_v2`는 registry에 있지만 off
- `ACTIVE_STRATEGIES` unchanged
- shadow evaluation은 execution decision / order routing 밖에서 수행
- shadow output은 전용 shadow 파일에만 기록

## 구현 파일

- `src/shadow_eval.py`
- `src/engine.py`
- `tests/test_shadow_eval.py`
- `tests/test_engine_cycle_smoke.py`

## runtime hook 위치

shadow evaluation은 `src/engine.py`에서 ranked strategy collection 이후, live execution branch 전에 호출된다.

선택 이유:

1. runtime market data가 이미 준비됨
2. active strategy evaluation이 끝남
3. shadow output만 기록하고 live flow는 바꾸지 않을 수 있음

## shadow output 파일

- `logs/shadow_breakout_v2.jsonl`
- `data/shadow_breakout_v2_snapshot.json`

### jsonl 목적

cycle당 1개의 append-only shadow event 저장

### snapshot 목적

operator-facing aggregate 저장:

- signal count
- filtered count
- allowed count
- ratios
- hypothetical trade count
- reason distribution

## 예외 처리

- shadow evaluation failure -> engine execution 중단 안 함
- shadow append failure -> engine execution 중단 안 함
- shadow snapshot update failure -> engine execution 중단 안 함

즉 live orders는 active strategy에만 의존하고, shadow instrumentation은 optional / non-blocking이다.

## 왜 execution path가 안 바뀌는가

shadow result는 다음으로 전달되지 않는다.

- `execution_decider`
- `order_router`
- live order submission
- pending order state
- open trade state

따라서:

- `breakout_v2`에서 live order 생성 불가
- `breakout_v2`에서 state mutation 불가
- shadow branch가 portfolio KPI를 직접 바꾸지 않음

## 알려진 한계

현재 shadow snapshot은 보수적으로 유지된다.

- `hypothetical_expectancy` placeholder
- `hypothetical_profit_factor` placeholder
- `stop_exit_ratio` placeholder

즉 promotion-decision engine이 아니라 observability layer다.

## 검증 범위

- shadow evaluation schema test
- shadow jsonl append test
- shadow snapshot aggregation test
- shadow log append 실패 시 engine continuation test

## 링크

- CNT v2 BREAKOUT V2 SHADOW RUNTIME INTEGRATION KO
- CNT v2 BREAKOUT V2 SHADOW VALIDATION SPEC KO

## Obsidian Links

- [[CNT v2 BREAKOUT V2 DESIGN KO]]



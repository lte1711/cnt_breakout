---
title: CNT v2 OFFICIAL LIVE GATE RETENTION AND AUXILIARY RECOVERY PLAN KO
status: FINAL
language: ko
updated: 2026-04-24
---

# CNT v2 공식 Live Gate 유지 및 보조 회복 평가 체계

## 결정

현재 단계에서는 CNT의 공식 live gate를 수정하지 않는 것이 맞다.

지금 수정해야 할 대상은 gate 조건식이 아니다.  
유효한 다음 단계는 포트폴리오 전체 snapshot 안에 아직 남아 있는 과거 `breakout_v1` 오염과 분리해서, 현재 런타임의 회복 상태를 읽는 **보조 회복 평가 계층**을 추가하고 사용하는 것이다.

## 현재 공식 Gate 규칙

공식 live gate는 그대로 유지한다.

1. `closed_trades >= 20`
2. `expectancy > 0`
3. `net_pnl > 0`
4. `max_consecutive_losses <= 5`
5. `risk_guard_observed`

이 gate는 계속 `src/validation/live_gate_evaluator.py` 기준으로 평가된다.

## 지금 Gate를 바꾸면 안 되는 이유

현재 `data/performance_snapshot.json`에는 과거 `breakout_v1`의 음수 기여가 아직 남아 있다.

문서 작성 시점 기준:

- `closed_trades = 35`
- `expectancy = -0.0003352571428572645`
- `net_pnl = -0.011734000000004186`
- `max_consecutive_losses = 3`
- `risk_trigger_stats.DAILY_LOSS_LIMIT = 348`

이 의미는 다음과 같다.

- 표본 수는 충분하다
- risk guard 관측도 존재한다
- 최대 연속 손실도 기준 이내다
- 그러나 전체 포트폴리오 snapshot에는 과거 음수 오염이 남아 있어 공식 gate는 보수적으로 FAIL이 난다

이 시점에 공식 gate를 바꾸면 다음을 구분할 수 없게 된다.

- 실제 회복
- gate 완화
- 과거 오염이 아직 남은 상태

## 보조 회복 평가 계층

보조 회복 평가 계층은 공식 gate를 대체하는 것이 아니라, **현재 회복 상태를 설명하는 2차 해석 체계**다.

목적은 다음과 같다.

1. 공식 gate는 계속 보수적으로 유지한다
2. 관측 단계 중 readiness 규칙을 다시 쓰지 않는다
3. post-isolation 런타임이 실제로 안정화되고 있는지 본다
4. 현재 회복 관측을 과거 `breakout_v1` 손상과 분리해서 읽는다

## 보조 평가 범위

보조 회복 평가 계층은 현재 post-isolation 운영 현실을 기준으로 해석한다.

- `pullback_v1`만 live active runtime
- `breakout_v1`는 active set에서 격리 유지
- `breakout_v3`는 shadow-only 유지
- portfolio risk sync는 이미 해결됨
- shadow semantics는 이미 rebaseline 후 clean 상태

## 보조 평가 입력

보조 계층은 아래 산출물을 증거로 사용한다.

- `data/state.json`
- `data/portfolio_state.json`
- `data/performance_snapshot.json`
- `data/live_gate_decision.json`
- `data/shadow_breakout_v3_snapshot.json`
- `logs/runtime.log`
- `logs/signal.log`

## 보조 회복 평가 질문

보조 계층은 최소한 아래 질문에 답해야 한다.

1. active runtime이 계속 `pullback_v1` 단독으로 유지되는가?
2. `state.json`과 `portfolio_state.json`의 risk counter가 계속 동기화되는가?
3. `breakout_v3` shadow 데이터가 계속 semantic clean 상태를 유지하는가?
4. post-isolation runtime이 새로운 구조 회귀 없이 관측 데이터를 누적하고 있는가?
5. 공식 gate가 아직 음수이더라도 현재 성과 동작은 회복 방향으로 가고 있는가?

## 보조 계층이 하면 안 되는 것

보조 회복 평가 계층은 다음을 해서는 안 된다.

- 공식 live gate 수정
- `data/live_gate_decision.json` 덮어쓰기
- `breakout_v3` 활성화
- `breakout_v1` 재활성화
- threshold 완화
- 과거 음수 결과가 사라진 것처럼 재해석

## 운영 해석 원칙

전체 포트폴리오 snapshot이 자연스럽게 회복되기 전까지는 아래처럼 해석하는 것이 맞다.

- 공식 gate: 계속 최종 권위 유지
- 보조 계층: 현재 회복 상태 설명용

즉 CNT는 같은 시점에 동시에 아래 상태일 수 있다.

- `official live gate = FAIL`
- `auxiliary recovery status = improving / stable / needs review`

이건 post-isolation recovery window에서는 정상적인 상태다.

## 즉시 다음 단계

즉시 다음 단계는 이 이중 해석 구조를 유지하는 것이다.

- 공식 gate는 그대로 유지
- pullback-only observation window 계속 진행
- breakout_v3 shadow observation 계속 진행
- post-isolation 회복 평가는 gate 수정보다 보조 회복 리뷰 문서로 기록

## 결론

현재 가장 올바른 다음 단계는 다음 두 가지를 동시에 유지하는 것이다.

- **공식 live gate는 그대로 유지**
- **post-isolation 회복 상태는 보조 회복 평가 계층으로 해석**

이 방식이 가장 보수적이면서도 현재 회복 상태를 정확히 추적할 수 있는 운영 방향이다.

## Obsidian Links

- [[CNT v2 LIVE READINESS GATE KO]]



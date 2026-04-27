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

# CNT v2 BREAKOUT V1 ACTIVE ISOLATION IMPLEMENTATION REPORT

## 변경 요약

런타임 active set을 다음 상태에서:

- `breakout_v1`
- `pullback_v1`

다음 상태로 축소했다.

- `pullback_v1` 단독

실제 설정 변경은 아래와 같다.

- `ACTIVE_STRATEGY = "pullback_v1"`
- `ACTIVE_STRATEGIES = ["pullback_v1"]`

## 왜 이 패치를 적용했는가

패치 시점 기준으로:

- `breakout_v1`는 강한 음수 expectancy를 보였고
- `pullback_v1`는 여전히 양수였으며
- `breakout_v3` shadow semantics는 이미 재정합 완료 상태였고
- `portfolio_state` risk metric sync도 이미 수정된 상태였다

즉 남아 있는 가장 큰 live contamination source는
`breakout_v1`의 active runtime 참여 자체였다.

## 변경 파일

- `config.py`
- `docs/CNT v2 BREAKOUT V1 ACTIVE ISOLATION DECISION.md`
- `docs/ko/CNT v2 BREAKOUT V1 ACTIVE ISOLATION DECISION KO.md`
- `docs/CNT v2 BREAKOUT V1 ACTIVE ISOLATION IMPLEMENTATION REPORT.md`
- `docs/ko/CNT v2 BREAKOUT V1 ACTIVE ISOLATION IMPLEMENTATION REPORT KO.md`

## 검증

### 테스트

- `PYTHONPATH=. python -m pytest -q`
- 결과: `56 passed`

### 컴파일

- `python -m py_compile config.py src\engine.py src\strategy_manager.py tests\test_signal_ranker.py tests\test_engine_cycle_smoke.py`
- 결과: `OK`

### 런타임

엔트리 체인 기준 검증은 아래로 수행했다.

- `run.ps1`

확인 결과:

- `data/state.json.strategy_name = pullback_v1`
- `data/state.json.action = NO_ENTRY_SIGNAL`
- `data/portfolio_state.json.daily_loss_count = 3`
- `data/portfolio_state.json.consecutive_losses = 3`

runtime log 기준:

- 과거 로그에는 기존 `breakout_v1` 기록이 남아 있으나
- 최신 isolated run은
  - `strategy_name = pullback_v1`
  - `reason = no_ranked_signal`
  로 기록됐다

signal log 기준:

- 최신 one-shot에서는 `pullback_v1`만 추가 기록됐다
- 기존 `breakout_v1` 라인은 과거 증거로 남아 있다

## 바꾸지 않은 것

이번 패치는 다음을 하지 않았다.

- `breakout_v1` 삭제
- registry에서 `breakout_v1` 제거
- `breakout_v3` 활성화
- risk guard threshold 변경
- exchange/order flow 변경

## 운영 해석

이 패치 이후 상태는 다음처럼 본다.

- `pullback_v1` = 유일한 live active strategy
- `breakout_v1` = 기록은 남지만 현재 runtime candidate는 아님
- `breakout_v3` = shadow-only

## 결론

`breakout_v1` active-set isolation 패치는 테스트, 컴파일, 엔트리 체인 런타임을 깨지 않고 성공적으로 적용되었다.

## Obsidian Links

- [[CNT v2 BREAKOUT QUALITY EVALUATION REPORT KO]]



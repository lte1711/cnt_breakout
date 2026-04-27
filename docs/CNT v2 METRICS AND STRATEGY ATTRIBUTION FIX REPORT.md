---
tags:
  - cnt
  - type/documentation
  - status/active
  - type/validation
  - type/operation
  - strategy/pullback_v1
  - strategy/breakout_v3
  - obsidian
  - type/analysis
  - cnt-v2-metrics-and-strategy-attribution-fix-report
---

# CNT v2 Metrics And Strategy Attribution Fix Report

## Design Summary

이번 수정은 구조 변경이 아니라 운영 해석 정확도를 높이기 위한 보정이다.

수정 대상은 세 가지였다.

1. `executed_trades`가 실제 체결 수가 아니라 `selected_signals`를 그대로 복사하던 문제
2. 청산 후 `pending_order`와 `open_trade`가 모두 비어 있을 때 `strategy_name`이 `ACTIVE_STRATEGY`로 잘못 귀속되던 문제
3. `trend_bias`가 `breakout_v1`만 채워지고 나머지 전략은 `UNKNOWN`으로 남던 관측 비대칭 문제

적용한 변경은 아래와 같다.

- `src/analytics/performance_snapshot.py`
  - `runtime.log`를 파싱해 `BUY_FILLED`와 `PROMOTE_TO_OPEN_TRADE`만 `executed_trades`로 집계하도록 수정
- `src/engine.py`
  - `_build_state`, `_save_and_finish`에 `strategy_name_override`를 추가
  - pending fill, close fill, protective exit, entry save 핵심 경로에서 실제 전략명을 명시적으로 전달
- `src/strategies/pullback_v1.py`
  - `ema_fast/ema_slow` 기준 `trend_bias` 기록 추가
- `src/strategies/mean_reversion_v1.py`
  - `last_price`와 `ema_value` 기준 `trend_bias` 기록 추가

## Validation Result

검증 결과는 아래와 같다.

```text
python -m unittest discover -s tests -p "test_*.py"
Ran 25 tests
OK
```

```text
python -m py_compile src\analytics\performance_snapshot.py src\engine.py src\strategies\pullback_v1.py src\strategies\mean_reversion_v1.py tests\test_performance_snapshot.py tests\test_engine_cycle_smoke.py
OK
```

추가된 검증 포인트:

- `tests/test_performance_snapshot.py`
  - `executed_trades`가 `BUY_SUBMITTED`가 아니라 실제 entry fill 계열만 세는지 확인
- `tests/test_engine_cycle_smoke.py`
  - `strategy_name_override`가 state에 그대로 보존되는지 확인

## Record Text

이번 수정으로 바뀌는 운영 의미는 아래와 같다.

- `selected_signals`
  - 전략이 선택된 횟수
- `executed_trades`
  - 실제 진입 fill이 발생한 횟수
- `selected_strategy_counts`
  - 신형 selection-path 로그 기반 집계

따라서 앞으로는 세 지표를 같은 값으로 해석하면 안 된다.

또한 청산 이후 runtime/state 기록의 `strategy_name`은 이제 실제 거래 전략에 더 가깝게 남는다.
이 변경으로 `pullback_v1` 청산이 `breakout_v1`로 오기록되는 운영 감사 혼선을 줄일 수 있다.

남아 있는 점:

- 이번 수정은 과거 로그를 소급 보정하지 않는다.
- 이미 저장된 과거 산출물은 기존 집계 정의를 포함할 수 있다.
- 최신 cycle부터 새 정의가 반영된다.

## Obsidian Links

- [[CNT v2 VALIDATION REPORT]]


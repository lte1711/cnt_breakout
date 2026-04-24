---
tags:
  - cnt
  - v2
  - fix
  - analytics
aliases:
  - CNT v2 Metrics And Strategy Attribution Fix Report KO
---

# CNT v2 메트릭 및 전략 귀속 보정 보고

## 설계 요약

이번 수정은 구조 변경이 아니라 운영 해석 정확도를 높이기 위한 보정이다.

수정 대상은 세 가지였다.

1. `executed_trades`가 실제 체결 수가 아니라 `selected_signals`를 그대로 복사하던 문제
2. 청산 후 `pending_order`와 `open_trade`가 모두 비어 있을 때 `strategy_name`이 `ACTIVE_STRATEGY`로 잘못 덮이는 문제
3. `trend_bias`가 `breakout_v1`만 채워지고 다른 전략은 `UNKNOWN`으로 남던 관측 불일치 문제

적용된 변경:

- `src/analytics/performance_snapshot.py`
  - `runtime.log`를 파싱해 `BUY_FILLED`와 `PROMOTE_TO_OPEN_TRADE`만 `executed_trades`로 집계하도록 수정
- `src/engine.py`
  - `_build_state`, `_save_and_finish`에 `strategy_name_override` 추가
  - pending fill, close fill, protective exit, entry save 경로에서 실제 전략명을 명시적으로 전달
- `src/strategies/pullback_v1.py`
  - `ema_fast/ema_slow` 기준 `trend_bias` 기록 추가
- `src/strategies/mean_reversion_v1.py`
  - `last_price`와 `ema_value` 기준 `trend_bias` 기록 추가

## 검증 결과

검증 결과는 다음과 같다.

```text
python -m unittest discover -s tests -p "test_*.py"
Ran 25 tests
OK
```

```text
python -m py_compile src\analytics\performance_snapshot.py src\engine.py src\strategies\pullback_v1.py src\strategies\mean_reversion_v1.py tests\test_performance_snapshot.py tests\test_engine_cycle_smoke.py
OK
```

추가 확인:

- `tests/test_performance_snapshot.py`
  - `executed_trades`가 `BUY_SUBMITTED`가 아니라 실제 entry fill만 세는지 확인
- `tests/test_engine_cycle_smoke.py`
  - `strategy_name_override`가 state에 그대로 보존되는지 확인

## 기록 문장

이번 수정으로 바뀌는 운영 해석은 다음과 같다.

- `selected_signals`
  - 전략이 선택된 횟수
- `executed_trades`
  - 실제 진입 fill이 발생한 횟수
- `selected_strategy_counts`
  - selection-path 로그 기반 집계

따라서 앞으로는 이 지표들을 같은 값으로 해석하면 안 된다.

또한 청산 이후 runtime/state 기록의 `strategy_name`도 이제 실제 거래 전략명에 더 가깝게 남는다.  
즉 `pullback_v1` 청산이 `breakout_v1`로 잘못 기록되던 운영 감사 혼선을 줄이는 보정이다.

남아 있는 점:

- 이번 수정은 과거 로그를 소급 보정하지 않는다
- 이미 저장된 과거 산출물은 기존 집계 정의를 포함한 채 남아 있을 수 있다
- 최신 cycle부터 새 정의가 반영된다

## Obsidian Links

- [[CNT v2 CURRENT STATUS ASSESSMENT]]
- [[CNT v2 TESTNET PERFORMANCE REPORT]]
- [[CNT v2 BREAKOUT FIRST TRADE REVIEW]]
- [[CNT OBSIDIAN PLUGIN POLICY]]
- [[00 Docs Index|Docs Index]]

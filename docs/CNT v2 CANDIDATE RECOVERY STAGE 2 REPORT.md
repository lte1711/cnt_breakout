---
tags:
  - cnt
  - v2
  - strategy
  - candidate-recovery
aliases:
  - CNT v2 CANDIDATE RECOVERY STAGE 2 REPORT
---

# CNT v2 Candidate Recovery Stage 2 Report

## Summary

이번 단계는 랭커 이후가 아니라 **후보 생성률 회복**을 목표로 한 2단계 패치다.

실제 로그 기준으로 `candidate_count=0`와 `no_ranked_signal`이 반복되는 주요 원인은 랭커가 아니라 전략 필터였다.

따라서 이번 변경은 강한 역추세 구간 차단은 유지하면서, 기존 hard reject 일부를 **low-confidence candidate**로 전환하는 방향으로 적용했다.

## Design Summary

### Breakout

- `TREND_UP`인데 `volatility_state != HIGH`라도
- RSI가 `rsi_threshold + relaxed_volatility_rsi_buffer` 이상이면
- `trend_up_relaxed_volatility_breakout`로 후보 허용

변경 후:

- `atr_expansion_multiplier = 1.02`
- `rsi_threshold = 52`
- `relaxed_volatility_rsi_buffer = 2`
- `relaxed_breakout_confidence = 0.68`

### Pullback

기존 core RSI band는 유지하되, 아래를 추가했다.

- relaxed RSI band: `38 ~ 56`
- near-trend tolerance: `ema_near_trend_tolerance = 0.0008`

새 low-confidence reason:

- `trend_pullback_reentry_relaxed_rsi`
- `near_trend_pullback_reentry`

## Validation Result

이번 단계에서 추가/갱신한 검증 포인트:

- breakout relaxed volatility path
- pullback relaxed RSI path
- pullback near-trend tolerance path

실제 검증 결과:

```text
python -m unittest discover -s tests -p "test_*.py"
Ran 31 tests in 0.034s
OK
```

```text
python -m py_compile config.py src\strategies\breakout_v1.py src\strategies\pullback_v1.py tests\test_breakout_trend_filter.py tests\test_pullback_strategy.py
OK
```

## Record Text

이번 단계는 무작정 진입을 늘리는 패치가 아니다.

핵심은 다음과 같다.

- 기존 강한 setup은 유지
- 약간 부족한 setup은 낮은 confidence 후보로 전환
- 랭커가 confidence와 성과 데이터를 함께 보고 선택할 수 있도록 입력량을 회복

따라서 이번 단계의 성공 기준은 곧바로 수익률 상승이 아니라:

- `candidate_count=0` 감소
- `no_ranked_signal` 감소
- selection 비교 가능한 후보 수 증가

이다.

## Obsidian Links

- [[CNT v2 RANKER REDESIGN REPORT]]
- [[CNT v2 BREAKOUT QUALITY EVALUATION REPORT]]
- [[CNT v2 TESTNET PERFORMANCE REPORT]]
- [[00 Docs Index|Docs Index]]

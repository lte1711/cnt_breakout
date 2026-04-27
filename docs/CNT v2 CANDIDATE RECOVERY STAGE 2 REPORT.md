---
tags:
  - cnt
  - type/documentation
  - status/active
  - market-context
  - context-filter
  - type/validation
  - type/operation
  - strategy/pullback_v1
  - strategy/breakout_v3
  - type/analysis
  - status/completed
  - cnt-v2-candidate-recovery-stage-2-report
---

# CNT v2 Candidate Recovery Stage 2 Report

## Summary

이번 2단계 패치는 랭커가 아니라 **후보 생성률 회복**을 목표로 적용됐다.

실제 로그 기준으로 `candidate_count=0`와 `no_ranked_signal`이 반복되는 주 원인은 랭커보다 전략 필터였다. 따라서 이번 변경은 강한 역추세 차단은 유지하면서, 기존 hard reject 일부를 **low-confidence candidate**로 전환하는 방향으로 설계됐다.

중요한 현재 판정은 아래와 같다.

> **패치 적용, 테스트 검증, 문서 반영은 완료됐다.**
> **운영 효과 검증은 아직 초기 단계다.**

즉, 지금 단계의 정확한 상태는 `적용 완료, 효과 검증 대기`다.

## Design Summary

### Breakout

다음 relaxed breakout 경로를 추가했다.

- `market_state == TREND_UP`
- `volatility_state != HIGH`
- `rsi >= rsi_threshold + relaxed_volatility_rsi_buffer`

이 조건을 만족하면 기존 hard reject 대신 낮은 confidence 후보를 허용한다.

변경된 설정:

- `atr_expansion_multiplier = 1.02`
- `rsi_threshold = 52`
- `relaxed_volatility_rsi_buffer = 2`
- `relaxed_breakout_confidence = 0.68`

새 reason:

- `trend_up_relaxed_volatility_breakout`

### Pullback

기존 core RSI band는 유지하고, 아래를 추가했다.

- relaxed RSI band: `38 ~ 56`
- near-trend tolerance: `ema_near_trend_tolerance = 0.0008`

새 low-confidence reason:

- `trend_pullback_reentry_relaxed_rsi`
- `near_trend_pullback_reentry`

## Validation Result

### Code Validation

다음 항목이 실제 저장소에 반영된 것을 확인했다.

- `config.py` 설정값 추가 및 조정
- `src/strategies/breakout_v1.py` relaxed breakout 경로 추가
- `src/strategies/pullback_v1.py` relaxed RSI / near-trend tolerance 추가
- `tests/test_breakout_trend_filter.py` 확장
- `tests/test_pullback_strategy.py` 신규 추가

### Test Validation

```text
python -m unittest discover -s tests -p "test_*.py"
Ran 31 tests in 0.034s
OK
```

### Compile Validation

```text
python -m py_compile config.py src\strategies\breakout_v1.py src\strategies\pullback_v1.py tests\test_breakout_trend_filter.py tests\test_pullback_strategy.py
OK
```

### Git Validation

로컬 저장소 기준 완료 상태:

- commit = `a05705e Recover CNT candidate generation stage 2`
- local working tree = clean

## Runtime Evidence Status

현재 운영 데이터 기준으로는 다음이 확인된다.

- 신규 reason 중 `near_trend_pullback_reentry`는 실제 로그에서 1회 확인됨
- `trend_up_relaxed_volatility_breakout`는 아직 운영 로그에서 명확히 확인되지 않음
- `trend_pullback_reentry_relaxed_rsi`도 아직 운영 로그에서 충분히 확인되지 않음

즉, **코드 경로 존재와 테스트 통과는 입증됐지만, 운영 효과는 아직 부분적 초기 증거만 존재한다.**

아직 확정할 수 없는 것:

- `candidate_count`가 의미 있게 회복됐는지
- `no_ranked_signal`이 실제로 감소했는지
- selection rate가 통계적으로 유의미하게 개선됐는지

## Record Text

이번 단계는 “무작정 진입을 늘리는 패치”가 아니다.

핵심은 다음과 같다.

- 기존 강한 setup은 유지
- 약간 부족한 setup은 low-confidence candidate로 전환
- 랭커가 confidence와 성과 데이터를 함께 보고 선택할 수 있도록 입력량 회복을 시도

따라서 이번 단계의 성공 기준은 즉시 수익 증가가 아니라 아래다.

- `candidate_count=0` 감소
- `no_ranked_signal` 감소
- selection 비교 가능한 후보 수 증가

하지만 현재 시점에서는 이 효과가 **운영 로그 기준으로 아직 충분히 입증되지 않았다.**

## Final Assessment

정확한 최종 문장은 아래와 같다.

> **2단계 후보 회복 패치는 로컬 저장소에 정상 적용·커밋·정리까지 완료된 상태이며, 코드/테스트/문서 반영도 모두 확인된다. 다만 운영 성능 개선 효과는 아직 초기 로그만 보인 상태라, 다음 단계는 실제 관측 데이터 기반 검증이다.**

## Next Step

다음 우선순위는 명확하다.

1. 운영 로그 재관측
2. `candidate_count`, `no_ranked_signal`, selection rate 변화 확인
3. 신규 relaxed reason의 실제 운영 출현 빈도 확인

즉, 다음 단계는 **Stage 3 운영 로그 재관측 검증**이다.

---

## Obsidian Links

- [[CNT v2 VALIDATION REPORT]]


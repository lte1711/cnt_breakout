---
tags:
  - cnt
  - v2
  - strategy
  - candidate-recovery
  - validation
aliases:
  - CNT v2 CANDIDATE RECOVERY STAGE 2 REPORT KO
---

# CNT v2 Candidate Recovery Stage 2 Report KO

## 요약

이번 2단계 조치는 전략 완화가 아니라 **후보 생성 복구**를 목표로 적용됐다.

실제 로그 기준으로 `candidate_count=0`와 `no_ranked_signal` 반복의 핵심 원인은 ranker보다 전략 filter 쪽에 있었기 때문에, 이번 변경은 강한 진입 차단을 유지하되 기존 hard reject 일부를 **low-confidence candidate**로 전환하는 방향으로 설계됐다.

현재 판단:

> **조치 적용, 테스트 검증, 문서 반영은 완료됐다.**
> **운영 효과 검증은 아직 초기 관측 단계다.**

## 설계 요약

### Breakout

다음 relaxed breakout 경로를 추가했다.

- `market_state == TREND_UP`
- `volatility_state != HIGH`
- `rsi >= rsi_threshold + relaxed_volatility_rsi_buffer`

이 조건을 만족하면 기존 hard reject 대신 낮은 confidence 후보를 허용한다.

변경 설정:

- `atr_expansion_multiplier = 1.02`
- `rsi_threshold = 52`
- `relaxed_volatility_rsi_buffer = 2`
- `relaxed_breakout_confidence = 0.68`

reason:

- `trend_up_relaxed_volatility_breakout`

### Pullback

기존 core RSI band를 유지하고 아래를 추가했다.

- relaxed RSI band: `38 ~ 56`
- near-trend tolerance: `ema_near_trend_tolerance = 0.0008`

low-confidence reason:

- `trend_pullback_reentry_relaxed_rsi`
- `near_trend_pullback_reentry`

## 검증 결과

### Code validation

- `config.py` 설정 반영
- `src/strategies/breakout_v1.py` relaxed breakout 경로 추가
- `src/strategies/pullback_v1.py` relaxed RSI / near-trend tolerance 추가
- 테스트 파일 확장

### Test validation

```text
python -m unittest discover -s tests -p "test_*.py"
Ran 31 tests in 0.034s
OK
```

### Compile validation

```text
python -m py_compile config.py src\strategies\breakout_v1.py src\strategies\pullback_v1.py tests\test_breakout_trend_filter.py tests\test_pullback_strategy.py
OK
```

## Runtime evidence 상태

현재 운영 데이터 기준으로:

- `near_trend_pullback_reentry`는 실제 로그에서 확인됨
- `trend_up_relaxed_volatility_breakout`는 아직 운영 로그에서 명확히 확인되지 않음
- `trend_pullback_reentry_relaxed_rsi`도 아직 충분한 운영 증거 부족

즉 **코드 경로와 테스트는 입증됐지만, 운영 효과는 아직 초기 로그만 존재**한다.

## 기록 요약

이번 단계의 실무 목적은 즉시 수익 증가가 아니라:

- 강한 setup 유지
- 중간 수준 setup을 low-confidence candidate로 전환
- ranker가 그 후보를 성과 데이터와 함께 비교할 수 있게 입력을 복구

따라서 성공 기준은:

- `candidate_count=0` 감소
- `no_ranked_signal` 감소
- selection 비교 가능한 후보 수 증가

하지만 현재 시점에서는 운영 로그 기준으로 아직 충분히 입증되진 않았다.

## 최종 평가

> **2단계 후보 복구 조치는 로컬 저장소에 정상 적용됐고, 코드/테스트/문서 반영은 모두 확인됐다. 다만 운영 성능 개선 효과는 아직 초기 로그만 보이는 상태로, 다음 단계는 운영 관측 데이터 기반 검증이다.**

## 다음 단계

1. 운영 로그 축적
2. `candidate_count`, `no_ranked_signal`, selection rate 변화 확인
3. relaxed reason의 실제 출현 빈도 확인

## 링크

- [[CNT v2 RANKER REDESIGN REPORT KO]]
- [[CNT v2 BREAKOUT QUALITY EVALUATION REPORT KO]]
- [[CNT v2 TESTNET PERFORMANCE REPORT KO]]
- [[CNT v2 CURRENT STATUS ASSESSMENT KO]]
- [[00 Docs Index KO]]

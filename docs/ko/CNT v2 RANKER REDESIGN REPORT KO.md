---
tags:
  - cnt
  - v2
  - ranking
  - performance
aliases:
  - CNT v2 RANKER REDESIGN REPORT KO
---

# CNT v2 Ranker Redesign Report KO

## 요약

이번 단계에서는 `signal_ranker`를 정적 우선순위 중심 구조에서 **성과 반영형 랭커**로 1차 재설계했다.

핵심 목표:

1. `static_priority_score`와 개별 signal confidence가 과도하게 점수를 지배하던 구조를 줄인다.
2. 표본이 적은 전략을 완전히 배제하지 않되, 거래 표본에 따라 성과 정보를 **점진적으로** 반영한다.

즉 이번 변경은 후보가 있을 때 어떤 전략이 선택되는가를 정상화하는 작업이다.
`candidate_count=0` 문제는 상위 gate/filter 문제로 이번 범위에 포함되지 않는다.

## 설계 요약

### 1. Soft sample confidence 도입

기존에는 `RANKER_MINIMUM_SAMPLE` 미만이면 기대값 기반 성능을 사실상 0으로 두는 hard fallback에 가까웠다.

이번 변경:

- `RANKER_MINIMUM_SAMPLE = 3`
- `RANKER_FULL_CONFIDENCE_SAMPLE = 10`

그리고 거래 수 기반 `sample_confidence`를 사용한다.

- `0`건: 성과 반영 없음
- `1~2`건: 약하게 반영
- `3`건 이상: 의미 있게 반영 시작
- `10`건 이상: full confidence

### 2. Expectancy 정규화

raw expectancy는 sample이 적을 때 스케일 영향이 컸다.

이번에는 expectancy를 상대 edge로 정규화했다.

```python
expectancy_edge = expectancy / avg_loss_or_avg_win
```

### 3. Win rate / Profit factor 반영

점수는 아래 성분으로 구성된다.

- `base_signal_score`
- `static_priority_score`
- `expectancy_weighted_score`
- `win_rate_weighted_score`
- `profit_factor_weighted_score`
- `trend_alignment_bonus`
- `volatility_penalty`
- `recent_loss_penalty`

### 4. Static base score 축소

정적 점수는 tie-break 수준으로 축소됐다.

- `breakout_v1 = 0.05`
- `pullback_v1 = 0.04`
- `mean_reversion_v1 = 0.03`

즉 이제 static score는 초기 signal 간격만 만들고, 실제 선택은 성과와 표본 흐름의 영향을 더 받는다.

## 검증 결과

### Code validation

- `config.py` 반영
- `src/portfolio/signal_ranker.py` 반영
- `tests/test_signal_ranker.py` 반영

### Test validation

```text
python -m unittest discover -s tests -p "test_*.py"
Ran 26 tests in 0.035s
OK
```

### Compile validation

```text
python -m py_compile config.py src\portfolio\signal_ranker.py tests\test_signal_ranker.py
OK
```

### Real-metrics 재확인

당시 `data/strategy_metrics.json` 기준 가정된 경쟁 결과:

- selected: `pullback_v1`
- `pullback_v1 score = 0.9688340150028945`
- `breakout_v1 score = 0.8443525896414387`

즉 현재 검증된 전략은 `pullback_v1`가 실제로 우선 선택된다.

## 기록 요약

이번 작업으로 해결된 것:

- 정적 우선순위 과지배 완화
- hard fallback 제거
- 표본 기반 soft confidence 도입
- expectancy 정규화
- win rate / profit factor 반영

아직 해결되지 않은 것:

- `candidate_count=0` 자체
- `breakout_v1` 후보 생성 부족
- 상위 market regime / entry gate 문제

## 결론

이번 1차 ranker 재설계는 **후보가 존재할 때는 검증된 전략이 우선 선택되도록 만드는 방향으로 정상 작동**한다.

하지만 현재 CNT의 실제 병목은 ranker 이후가 아니라 ranker 이전, 즉 **candidate 자체가 부족한 구조**다.

## 링크

- [[CNT v2 BREAKOUT QUALITY EVALUATION REPORT KO]]
- [[CNT v2 TESTNET PERFORMANCE REPORT KO]]
- [[CNT v2 CURRENT STATUS ASSESSMENT KO]]
- [[CNT v2 METRICS AND STRATEGY ATTRIBUTION FIX REPORT KO]]
- [[00 Docs Index KO]]

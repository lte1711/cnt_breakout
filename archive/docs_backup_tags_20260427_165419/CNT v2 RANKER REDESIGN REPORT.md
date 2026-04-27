---
aliases:
  - CNT v2 RANKER REDESIGN REPORT
---

# CNT v2 Ranker Redesign Report

## Summary

이번 단계에서는 `signal_ranker`를 정적 우선순위 중심 구조에서 **성과 반영형 랭커**로 1차 재설계했다.

핵심 목표는 두 가지였다.

1. `static_priority_score`와 개별 signal confidence가 과도하게 점수를 지배하던 구조를 줄인다.
2. 샘플이 적은 전략도 완전 배제하지 않고, 거래 표본에 따라 성과 정보를 **점진적으로** 반영한다.

이번 변경은 “후보가 있을 때 누가 선택되어야 하는가”를 정상화하는 작업이다.
`candidate_count=0`이 반복되는 상위 gate/filter 문제는 이번 단계 범위에 포함되지 않는다.

## Design Summary

### 1. Soft sample confidence 도입

기존 구조는 `RANKER_MINIMUM_SAMPLE` 미만이면 기대값 기반 성분을 사실상 0으로 두는 hard fallback이었다.

이번 변경 후:

- `RANKER_MINIMUM_SAMPLE = 3`
- `RANKER_FULL_CONFIDENCE_SAMPLE = 10`

그리고 거래 수 기준 `sample_confidence`를 사용한다.

- `0`건: 성과 반영 없음
- `1~2`건: 약하게 반영
- `3`건 이상: 의미 있게 반영 시작
- `10`건 이상: full confidence

### 2. Expectancy 정규화

기존 raw expectancy 값은 절대 크기가 너무 작아서 실질 영향력이 약했다.

이번 변경 후 expectancy는 손익 기준으로 정규화된 edge로 계산한다.

```python
expectancy_edge = expectancy / avg_loss_or_avg_win
```

이 구조로 손실 대비 기대값의 상대적 우위를 점수에 반영할 수 있게 했다.

### 3. Win rate / Profit factor 반영

이번 재설계 후 점수는 아래 성분으로 구성된다.

- `base_signal_score`
- `static_priority_score`
- `expectancy_weighted_score`
- `win_rate_weighted_score`
- `profit_factor_weighted_score`
- `trend_alignment_bonus`
- `volatility_penalty`
- `recent_loss_penalty`

### 4. Static base score 축소

정적 점수는 tie-break 수준으로 축소했다.

- `breakout_v1 = 0.05`
- `pullback_v1 = 0.04`
- `mean_reversion_v1 = 0.03`

즉, 이제 static score는 “기본 선호도”만 남기고, 실제 선택은 성과와 샘플 신뢰도 영향을 받는다.

## Validation Result

### Code Validation

- `config.py` 반영 완료
- `src/portfolio/signal_ranker.py` 반영 완료
- `tests/test_signal_ranker.py` 반영 완료

### Test Validation

```text
python -m unittest discover -s tests -p "test_*.py"
Ran 26 tests in 0.035s
OK
```

### Compile Validation

```text
python -m py_compile config.py src\portfolio\signal_ranker.py tests\test_signal_ranker.py
OK
```

### Real-metrics Recheck

현재 `data/strategy_metrics.json` 기준으로 두 전략이 동시에 후보라고 가정했을 때 재랭킹 결과는 다음과 같았다.

- selected: `pullback_v1`
- `pullback_v1 score = 0.9688340150028945`
- `breakout_v1 score = 0.8443525896414387`

이 결과는 현재 저장소의 실데이터와도 일치한다.

- `pullback_v1`
  - `trades_closed = 17`
  - `expectancy = 0.0021459411764703723`
  - `profit_factor = 1.359079097602219`
  - `sample_confidence = 1.0`
- `breakout_v1`
  - `trades_closed = 2`
  - `expectancy = 0.0014410000000004402`
  - `profit_factor = 1.2609561752988854`
  - `sample_confidence = 0.2`

즉, 이번 랭커 재설계 후에는 **현재 더 검증된 전략인 `pullback_v1`가 실제로 우선 선택된다.**

## Record Text

이번 작업은 ranker 자체의 정상화다.

해결된 것:

- 정적 우선순위 과지배 완화
- hard fallback 제거
- 샘플 기반 soft confidence 도입
- expectancy 영향 정규화
- win rate / profit factor 반영
- 실데이터 기준 `pullback_v1` 우선 선택 정상화

이번 작업으로 해결되지 않은 것:

- `candidate_count=0` 다발 문제
- `breakout_v1` 후보 생성 빈도 부족
- 상위 market regime gate / entry gate 과필터 문제

따라서 다음 실제 우선순위는 다음과 같다.

1. `no_ranked_signal`의 본체인 `candidate_count=0` 원인 분석
2. 전략별 rejection reason 분포 재확인
3. 필요한 경우 상위 gate/filter를 조정해 실제 후보 생성률을 회복

## Conclusion

이번 1차 ranker 재설계는 **후보가 존재할 때 더 검증된 전략을 우선 선택하게 만드는 방향으로 정상 작동**한다.

다만 현재 CNT의 더 큰 병목은 여전히 랭커 이후가 아니라 랭커 이전, 즉 **candidate 자체가 부족한 구조**에 있다.

---

## Obsidian Links

- [[CNT v2 VALIDATION REPORT]]


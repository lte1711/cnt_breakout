---
aliases:
  - CNT v2 STRATEGY ISOLATION COMPARISON KO
---

# CNT v2 전략 격리 비교

## 범위

이 비교는 아래 두 파일을 사용한다.

- `data/strategy_metrics.json`
- `data/performance_snapshot.json`

현재 snapshot 기준:

- `2026-04-22 12:44:03`

## 비교 표

| Baseline | Closed Trades | Win Rate | Expectancy | Profit Factor | Net PnL |
| --- | ---: | ---: | ---: | ---: | ---: |
| Mixed portfolio | 24 | 54.17% | -0.0007808 | 0.9159 | -0.0187390 |
| pullback_v1 only inferred baseline | 21 | 57.14% | 0.0022788 | 1.3365 | +0.0478550 |
| breakout_v1 standalone observed baseline | 3 | 33.33% | -0.0221980 | 0.1730 | -0.0665940 |

## 해석

### Mixed Portfolio

현재 결합 포트폴리오가 실패하는 이유:

- expectancy 음수
- PF 1 미만
- net PnL 음수

### pullback_v1 Only

추정된 pullback-only baseline은 여전히 양수다.

- positive expectancy
- PF 1.3 이상
- positive net contribution

즉 현재 포트폴리오 실패의 지배적 원인이 pullback은 아니라는 해석을 지지한다.

### breakout_v1 Standalone

관측된 breakout-only baseline은 분명히 약하다.

- negative expectancy
- PF가 1보다 훨씬 낮음
- 현재 mixed portfolio 손실보다 더 큰 음수 net contribution

## 기여도 계산

Net contribution check:

- `pullback net = +0.0478550`
- `breakout net = -0.0665940`
- `mixed net = -0.0187390`

즉 breakout 기여가, 양수 pullback 품질에서 음수 mixed portfolio 품질로 전환되는 설명력을 가진다.

## 종합 해석

올바른 읽는 방식은 다음과 같다.

- pullback은 여전히 standalone 기준 양수 edge를 가진다
- breakout은 현재 결합 포트폴리오 품질을 악화시킨다
- 따라서 다음 진단 단계는 두 전략을 함께 튜닝하는 것이 아니라 breakout 품질을 pullback 품질과 분리해서 보는 것이다

## 필수 결론

**breakout_v1 isolation required**

## Obsidian Links

- [[CNT v2 POST-READY DEGRADATION REVIEW KO]]



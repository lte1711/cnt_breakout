---
tags:
  - cnt
  - type/documentation
  - status/active
  - context-filter
  - type/operation
  - risk
  - strategy/pullback_v1
  - strategy/breakout_v3
  - type/analysis
  - cnt-post-live-ready-optimization-memo-ko
---

# CNT 라이브 준비도 통과 이후 최적화 메모

## 분류

이 문서는 **장기 최적화 메모**이지, 사실 기반 운영 보고서가 아니다.

따라서 아래 현재 truth source를 대체하면 안 된다.

- `data/performance_snapshot.json`
- `data/strategy_metrics.json`
- `data/live_gate_decision.json`
- `logs/runtime.log`
- `logs/portfolio.log`
- `logs/signal.log`

## 목적

이 메모는 현재 `LIVE_READY` baseline이 안정화된 이후에 고려할 수 있는 상위 수준 개선 아이디어를 담는다.

즉 immediate runtime judgment가 아니라 backlog planning용 문서다.

## 왜 현재 상태 보고서가 아닌가

CNT는 이미 “실데이터 이전 단계”를 넘어섰다.

현재 저장소는 아래를 이미 가진다.

- real snapshot data
- real strategy metrics
- real runtime logs
- real live gate decisions

그래서 multi-asset expansion, Kelly sizing, advanced regime switching 같은 아이디어는 현재 결론이 아니라 미래 개선 주제로 봐야 한다.

## 장기 개선 주제

### 1. Signal Quality Refinement

- noisy low-value selection 감소
- raw signal volume보다 selection efficiency 개선
- baseline이 안정된 뒤에만 filter layering 재검토

### 2. Execution Efficiency

- `LIVE_READY` 이후 execution rate 추적
- policy block과 candidate starvation 분리
- post-ready evidence가 충분할 때만 execution friction 검토

### 3. Risk Adaptation

- 안정성 증명 이후에만 future guardrail tuning 검토
- adaptive risk control은 baseline operating quality가 시간 경과로 측정된 뒤에만 추가

### 4. Strategy Diversification

- `pullback_v1`는 여전히 primary strategy
- `breakout_v1`는 낮은 표본의 secondary strategy
- multi-asset / multi-strategy portfolio expansion은 현재 action item이 아니라 이후 단계

### 5. Advanced Optimization Backlog

현재 sprint가 아닌 future backlog 주제:

- capital allocation models
- volatility regime switching
- AI/ML-assisted tuning
- multi-asset orchestration
- chaos or resilience simulation

## 현재 경계

현재 CNT 단계에서의 운영 초점:

- `selection_rate`
- `execution_rate`
- `no_ranked_signal`
- `strategy_split`
- `LIVE_READY` persistence

이 메모는 fact-based runtime report보다 우선순위가 낮아야 한다.

## 권장 사용 방식

이 문서는 아래 경우에만 사용한다.

- future backlog item 준비
- 안정화 이후 개선 주제 정리
- 현재 runtime fact와 미래 아이디어 분리

즉 runtime parameter를 당장 바꾸는 근거로 쓰면 안 된다.

## 링크

- CNT POST LIVE READY OPTIMIZATION MEMO
- CNT v2 CURRENT STATUS ASSESSMENT KO
- CNT SYNTHETIC ARCHITECTURE RISK MEMO KO

## Obsidian Links

- [[00 Docs Index KO]]



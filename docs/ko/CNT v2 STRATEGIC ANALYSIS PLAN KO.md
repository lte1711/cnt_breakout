---
aliases:
  - CNT v2 STRATEGIC ANALYSIS PLAN KO
---

# CNT v2 STRATEGIC ANALYSIS PLAN KO

```text
DOCUMENT_NAME = cnt_v2_strategic_analysis_plan_ko
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-19
STATUS        = SAVED_AS_PLANNING_REFERENCE
ROLE          = PLANNING_DOCUMENT_NOT_RUNTIME_TRUTH
```

## 1. 문서 역할

이 문서는 현재의 상위 전략 분석을 계획용 참조로 보관한다.

해석 규칙:

- 저장소 코드, runtime state, 로그가 1차 진실원이다
- 이 문서와 참조 PDF는 planning / interpretation / prioritization 입력이다
- 코드나 runtime 증거로 확인되기 전까지는 제안으로 본다

## 2. 당시 사실 baseline

- 프로젝트는 one-shot scheduled engine이다
- `live_gate_decision`은 `NOT_READY / INSUFFICIENT_SAMPLE`
- 실제 closed-trade 증거가 있는 전략은 `pullback_v1`
- `breakout_v1`는 신호는 만들지만 selected/closed trade 증거가 없다
- `mean_reversion_v1`는 등록돼 있지만 inactive다
- entry selection보다 exit handling이 더 강하다
- 큰 기술 부채는 `src/engine.py`

## 3. 저장된 전략 결론

1. 엔진을 안정적으로 유지하고 먼저 표본을 더 모은다
2. 충분한 관측 증거가 쌓인 뒤에만 `engine.py` 분해를 시작한다
3. cycle / portfolio / analytics state 책임을 더 명확히 한다
4. activation 증거가 쌓일 때까지 `breakout_v1`는 experiment strategy로 둔다

운영 해석:

- 주 작업 전략: `pullback_v1`
- 실험 전략: `breakout_v1`
- 비활성 전략: `mean_reversion_v1`

## 4. 즉시 우선순위

```text
1. accumulate more closed-trade evidence
2. test limited breakout activation relaxations on testnet only
3. start engine decomposition design
4. avoid live-readiness escalation until sample threshold is reached
```

## 5. 제약

승인하지 않는 것:

- live deployment
- 광범위한 risk parameter 재조정
- pullback 로직의 파괴적 재작성
- multi-symbol / multi-position 확장

지지하는 것:

- observation-first 운영
- testnet 전용 breakout 조정 실험
- engine modularization 설계
- 더 명확한 state semantics

## 링크

- CNT v2 ENGINE DECOMPOSITION DESIGN KO
- CNT v2 ENGINEERING PHASE PLAN KO
- 00 Docs Index KO

## Obsidian Links

- [[00 Docs Index KO]]



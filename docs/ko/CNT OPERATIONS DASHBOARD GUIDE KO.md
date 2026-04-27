---
tags:
  - cnt
  - type/documentation
  - status/active
  - type/operation
  - obsidian
  - type/analysis
  - cnt-operations-dashboard-guide-ko
---

# CNT 운영 대시보드 가이드

## 목적

이 가이드는 현재 runtime 데이터를 읽어 CNT testnet 운영 상태를 의사결정 중심으로 보여주는 CNT 운영 대시보드의 사용법을 설명합니다.

## 파일

- HTML 대시보드: [cnt_operations_dashboard.html](../cnt_operations_dashboard.html)
- 실행 스크립트: [serve_dashboard.py](../../scripts/serve_dashboard.py)

## 이 대시보드가 추가하는 것

이 대시보드는 단순한 지표 뷰어가 아닙니다.

추가되는 기능:

- 시스템 건강도 해석
- gate readiness 해석
- 약한 운영 상태에 대한 alert block
- pipeline bottleneck 가시성
- 전략 품질 라벨
- 브라우저 local storage를 이용한 간단한 delta 추적

## Runtime 데이터 소스

대시보드는 아래 파일을 읽습니다.

- `data/performance_snapshot.json`
- `data/strategy_metrics.json`
- `data/state.json`
- `data/live_gate_decision.json`

## 사용 방법

저장소 루트에서 실행:

```powershell
python scripts/serve_dashboard.py
```

이후 아래 주소를 엽니다.

```text
http://127.0.0.1:8000/docs/cnt_operations_dashboard.html
```

## 해석 메모

- `READY`는 단순히 `closed_trades >= 50`만으로 판정되지 않음
- 대시보드 gate rule:
  - `closed_trades >= 50`
  - `profit_factor >= 1.1`
  - `expectancy > 0`
- `RANKER FAILURE`와 `CANDIDATE STARVATION`은 운영 지원용 heuristic warning layer임
- candidate 부족은 현재 snapshot에 dedicated candidate-count telemetry가 저장되지 않으므로 pipeline ratio와 blocked count를 바탕으로 추정됨

## 한계

- 이 대시보드는 저장소가 HTTP로 제공될 때 동작함
- CNT repository root 기준으로 열어야 함
- 현재 runtime 파일을 읽는 도구이지 fact-based CNT report를 대체하지 않음
- delta 비교는 브라우저 local storage의 이전 snapshot에 기반함

## Obsidian Links

- [[CNT DATA DASHBOARD KO]]

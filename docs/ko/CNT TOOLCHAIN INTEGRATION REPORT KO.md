---
aliases:
  - CNT TOOLCHAIN INTEGRATION REPORT KO
---

# CNT Toolchain Integration Report KO

## 요약

이 문서는 Obsidian, gemma4, VSCode가 같은 CNT 저장소를 공유하면서도 각자 역할이 섞이지 않도록 연결 구조를 보강한 작업을 정리한다.

핵심 목표는 다음과 같았다.

1. VSCode/Continue가 `AGENTS.md`와 `.continuerules`를 기본 컨텍스트로 읽도록 저장소 설정을 둔다.
2. gemma4가 어떤 역할과 입력 경계를 가져야 하는지 명시한다.
3. Obsidian에서 `data/*.json`을 직접 읽어 상태를 보는 문서를 준비한다.
4. 전체 작업 흐름을 문서로 고정한다.

## 적용된 변경

### VSCode

- `.vscode/settings.json`
- `continue.contextProviders` 추가
- 기본 컨텍스트 파일:
  - `AGENTS.md`
  - `.continuerules`

이 변경은 기본 컨텍스트 주입 규칙을 저장소에 기록한 것이다. 실제 IDE 반영 여부는 각 사용자 환경에서 최종 확인이 필요하다.

### gemma4

- `.continuerules`
  - `gemma4 Activation` 섹션 추가
  - 컨텍스트 파일, 소스 우선 파일, 트리거 규칙 명시
- `docs/gemma4_system_prompt.md`
  - 역할, 우선순위, 증거 규칙, 출력 스타일 명시

### Obsidian

- `.obsidian/community-plugins.json`
  - `dataview`
  - `templater-obsidian`
  를 준비 상태로 명시
- `docs/CNT DATA DASHBOARD.md`
  - `strategy_metrics.json`
  - `live_gate_decision.json`
  - `performance_snapshot.json`
  을 읽는 DataviewJS 블록 추가

### Workflow

- `.windsurf/workflows/cnt-start.md`
  - constitution-first 흐름 유지
  - Obsidian -> VSCode -> Continue/gemma4 -> docs 반영 흐름으로 확장

## 현재 한계

- Dataview와 Templater는 설정 파일만으로 자동 설치되지 않는다.
- 현재 변경은 사용 가능한 저장소 구조를 만드는 단계다.
- 실제 Obsidian 플러그인 설치 자체는 각 사용자 환경에서 별도 수행해야 한다.
- VSCode/Continue 연동도 저장소 설정은 준비됐지만 최종 동작은 사용자 환경에서 확인해야 한다.

## 최종 평가

이번 보강으로 도구별 역할은 아래처럼 더 분명해졌다.

- Obsidian: 대시보드와 의사결정 노트
- gemma4: 데이터 해석과 보고 보조
- VSCode: 문서 컨텍스트가 붙은 코드 작업 환경

## 링크

- CNT DATA DASHBOARD KO
- CNT OBSIDIAN PLUGIN POLICY KO
- 00 Docs Index KO

## Obsidian Links

- [[CNT TOOLCHAIN INTEGRATION REPORT KO]]



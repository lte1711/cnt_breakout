---
aliases:
  - CNT TOOLCHAIN INTEGRATION REPORT
---

# CNT Toolchain Integration Report

## Summary

이번 정리는 Obsidian, gemma4, VSCode가 같은 저장소를 쓰되 서로 단절되지 않도록 연결 구조를 보강한 작업이다.

핵심 목표:

1. VSCode/Continue가 `AGENTS.md`와 `.continuerules`를 기본 컨텍스트로 받도록 저장소 설정을 등록한다.
2. gemma4의 역할과 입력 채널을 명시한다.
3. Obsidian에서 `data/*.json`을 직접 읽어 대시보드처럼 볼 수 있는 문서를 준비한다.
4. 작업 흐름을 한 문서로 표준화한다.

## Applied Changes

### VSCode

- `.vscode/settings.json`
- `continue.contextProviders` 추가
- 기본 컨텍스트 파일:
  - `AGENTS.md`
  - `.continuerules`

해석 주의:

- 이번 변경은 **기본 컨텍스트 주입 규칙을 저장소에 등록한 것**이다.
- Continue가 각 환경에서 이 설정을 실제로 소비하는지는 사용자 설치 환경에서 최종 확인돼야 한다.

### gemma4

- `.continuerules`
  - `gemma4 Activation` 섹션 추가
  - 컨텍스트 파일, 시스템 프롬프트 파일, 트리거 규칙 명시
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
  를 읽는 DataviewJS 블록 추가

### Workflow

- `.windsurf/workflows/cnt-start.md`
  - constitution-first 흐름 유지
  - Obsidian → VSCode → Continue/gemma4 → docs 반영 흐름으로 확장

## Current Limitation

- Dataview와 Templater는 설정 파일만으로 자동 설치되지는 않는다.
- 현재 변경은 “즉시 설치 후 사용 가능한 저장소 구조”를 만드는 단계다.
- 실제 Obsidian 플러그인 설치 자체는 사용자 환경에서 한 번 실행돼야 한다.
- VSCode/Continue 연동도 저장소 설정은 준비됐지만, 최종 동작은 각 사용자 환경에서 확인돼야 한다.

## Final Assessment

이번 보강으로 세 도구의 역할은 아래처럼 더 분명해졌다.

- Obsidian: 대시보드 / 의사결정 노트
- gemma4: 데이터 해석 / 보고 보조
- VSCode: 헌법 컨텍스트가 붙은 코드 작업 환경

---

## Obsidian Links

- [[00 Docs Index]]


---
aliases:
  - CNT v2 EOL NORMALIZATION AND REPORT GENERATION HARDENING WORK INSTRUCTION KO
---

# CNT v2 EOL NORMALIZATION AND REPORT HARDENING WORK INSTRUCTION KO

## 목적

이 작업은 재현성 관련 두 가지를 마무리한다.

1. 저장소 전반의 `.gitattributes` 선언과 실제 tracked file의 EOL 상태를 일치시킨다.
2. 자동 생성되는 성능 보고서가 Windows를 포함한 모든 환경에서 `LF`를 유지하도록 강제한다.

완료 후 목표 문장:

> CNT 저장소 텍스트 파일은 선언된 LF 정책을 설정과 실제 tracked state 모두에서 따르며, 자동 생성 성능 보고서도 재생성 후 그 정책을 유지한다.

## 현재 판단

이미 완료된 것:

- Obsidian 비표준 `../...` 링크 제거
- `.obsidian/plugins/` 구조 생성
- Obsidian 플러그인 설치 정책 문서화
- `.windsurf` 기본 의존성 제거
- `.continuerules`, `AGENTS.md`, `.vscode/settings.json`은 이미 LF 정책과 일치

남은 이슈:

- tracked file 전체에 대한 EOL renormalization 필요
- `docs/CNT v2 TESTNET PERFORMANCE REPORT.md`는 쓰기 시 LF를 강제하지 않으면 플랫폼 기본 줄바꿈으로 재생성될 수 있음

## 실행 순서

1. `src/analytics/performance_report.py`에서 LF 출력 강제
2. 저장소 전체에 `git add --renormalize .`
3. performance report 재생성
4. 다시 `git add --renormalize .`
5. tracked EOL 상태, 테스트, compile check 검증
6. 최종 판정을 문서로 기록

## 포함 범위

- `.gitattributes`
- 루트 Python 파일
- `src/**/*.py`
- `scripts/**/*.py`
- `docs/**/*.md`
- `.vscode/**/*.json`
- `.obsidian/**/*.json`
- 기타 tracked text files

제외 범위:

- ignored runtime artifacts
- local-only cache files
- third-party plugin bundles

## 완료 기준

다음을 모두 만족해야 완료:

1. `src/**/*.py`와 루트 runtime Python 파일의 `CRLF = 0`
2. `src/analytics/performance_report.py`가 LF 출력을 강제
3. `docs/CNT v2 TESTNET PERFORMANCE REPORT.md`가 재생성 후에도 LF only 유지
4. `git add --renormalize .` 후 추가 normalization diff 없음
5. tests / compile checks 통과
6. 최종 상태를 CNT 문서에 기록

## 링크

- CNT TOOLCHAIN INTEGRATION REPORT KO
- CNT v2 CURRENT STATUS ASSESSMENT KO
- CNT v2 TESTNET PERFORMANCE REPORT KO
- 00 Docs Index KO

## Obsidian Links

- [[00 Docs Index KO]]



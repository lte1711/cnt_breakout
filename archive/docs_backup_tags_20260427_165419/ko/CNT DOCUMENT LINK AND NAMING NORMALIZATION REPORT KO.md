---
---

# CNT 문서 링크 및 파일명 정규화 보고서

## 요약

이 문서는 2026-04-24 09:30 이후 문서 자동화 변경으로 생긴 문제를 정리하고, 이번에 수행한 정규화 작업을 기록한다.

주요 문제는 아래 세 가지였다.

- `[ [docs/... ] ]`, `[ [docs/ko/... ] ]` 형태의 잘못된 wiki-link 생성
- `docs/ko/` 아래 한글 파일명 생성
- 위 문제를 다시 만들어내는 보조 스크립트 존재

## 적용한 수정

### wiki-link 정규화

- `[ [docs/... ] ]` 링크를 plain Obsidian 링크인 `문서명` 형태로 복구
- `[ [docs/...|표시명 ] ]` 링크를 `표시명` 형태로 복구
- `[ [docs/ko/... ] ]` 링크를 `문서명 KO` 형태의 plain 링크로 복구

### ASCII 파일명 복구

다음 한글 파일명은 규칙에 맞는 ASCII 파일명으로 변경했다.

- `CNT Graph 링크 단순화 보고서 KO.md` -> `CNT GRAPH LINK SIMPLIFICATION REPORT KO.md`
- `CNT GRAPH 뷰 색상 구성 KO.md` -> `CNT GRAPH VIEW COLOR CONFIGURATION KO.md`
- `CNT OBSIDIAN 버전 시각화 설정 KO.md` -> `CNT OBSIDIAN VERSION VISUALIZATION CONFIGURATION KO.md`
- `CNT 링크 수정 보고서 KO.md` -> `CNT LINKS FIX REPORT KO.md`
- `CNT 버전 분류 및 색상 코딩 가이드 KO.md` -> `CNT VERSION CLASSIFICATION AND COLOR CODING GUIDE KO.md`
- `CNT 버전 분류 보고서 KO.md` -> `CNT VERSION CLASSIFICATION REPORT KO.md`

### 스크립트 재발 방지 수정

다음 스크립트를 저장소 규칙에 맞게 다시 작성했다.

- `scripts/fix_korean_links.py`
- `scripts/simplify_graph_links.py`
- `scripts/simplify_graph_links_fixed.py`
- `scripts/manual_simplify_links.py`

수정 후 스크립트는 다음 원칙을 따른다.

- repo-relative only
- `[ [docs/... ] ]`, `[ [docs/ko/... ] ]` 링크 생성 금지
- `C:/cnt` 같은 절대 경로 사용 금지

## 검증

정규화 후 아래 검증을 통과했다.

- `docs/`, `docs/ko/`, `scripts/` 안에 path-prefixed wiki-link가 남아 있지 않음
- `docs/ko/` 안에 비-ASCII 마크다운 파일명이 남아 있지 않음
- 수정 대상 스크립트 안에 `C:/cnt` 절대 경로가 남아 있지 않음
- 수정한 스크립트가 `python -m py_compile` 검증을 통과함

## 비고

- `.obsidian/appearance.json`, `.obsidian/workspace.json`은 로컬 환경 파일이므로 이번 정규화 대상에서 제외했다
- `data/shadow_breakout_v3_snapshot.json` 같은 runtime 산출물은 이번 문서 정리와 별개로 유지했다

## 결과

현재 문서 계층은 다시 다음 상태로 돌아왔다.

- plain Obsidian wiki-link
- ASCII-safe 파일명
- repo-relative 기준의 보조 스크립트

## Obsidian Links

- [[00 Docs Index KO]]



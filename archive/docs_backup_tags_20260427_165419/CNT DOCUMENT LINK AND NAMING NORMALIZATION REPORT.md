---
---

# CNT Document Link And Naming Normalization Report

## Summary

This report records the cleanup performed after the 2026-04-24 09:30 documentation automation changes.

The main issues were:

- path-prefixed wiki-links such as `[ [docs/... ] ]` and `[ [docs/ko/... ] ]`
- Korean filenames under `docs/ko/`, which violated the ASCII filename rule
- helper scripts that regenerated those invalid links and paths

## Fixes Applied

### Wiki-link normalization

- Replaced `[ [docs/... ] ]` links with plain Obsidian-compatible `Document Name` links
- Replaced `[ [docs/...|Label ] ]` links with `Label`
- Replaced `[ [docs/ko/... ] ]` links with plain Korean mirror targets such as `Document Name KO`

### ASCII filename restoration

The following Korean filenames were renamed to ASCII-safe names:

- `CNT Graph 링크 단순화 보고서 KO.md` -> `CNT GRAPH LINK SIMPLIFICATION REPORT KO.md`
- `CNT GRAPH 뷰 색상 구성 KO.md` -> `CNT GRAPH VIEW COLOR CONFIGURATION KO.md`
- `CNT OBSIDIAN 버전 시각화 설정 KO.md` -> `CNT OBSIDIAN VERSION VISUALIZATION CONFIGURATION KO.md`
- `CNT 링크 수정 보고서 KO.md` -> `CNT LINKS FIX REPORT KO.md`
- `CNT 버전 분류 및 색상 코딩 가이드 KO.md` -> `CNT VERSION CLASSIFICATION AND COLOR CODING GUIDE KO.md`
- `CNT 버전 분류 보고서 KO.md` -> `CNT VERSION CLASSIFICATION REPORT KO.md`

### Script hardening

The following scripts were rewritten to follow repository rules:

- `scripts/fix_korean_links.py`
- `scripts/simplify_graph_links.py`
- `scripts/simplify_graph_links_fixed.py`
- `scripts/manual_simplify_links.py`

The corrected scripts now:

- use repo-relative behavior only
- do not emit `[ [docs/... ] ]` or `[ [docs/ko/... ] ]` wiki-links
- do not use `C:/cnt` absolute paths

## Verification

The following checks passed after normalization:

- no remaining path-prefixed wiki-links in `docs/`, `docs/ko/`, or `scripts/`
- no remaining non-ASCII markdown filenames in `docs/ko/`
- no remaining `C:/cnt` absolute path usage in the corrected scripts
- updated scripts compile successfully with `python -m py_compile`

## Notes

- `.obsidian/appearance.json` and `.obsidian/workspace.json` remain local-environment files and were not rewritten as part of this normalization
- runtime data files such as `data/shadow_breakout_v3_snapshot.json` were not modified by this document cleanup

## Result

The documentation layer is now back to:

- plain Obsidian wiki-links
- ASCII-safe filenames
- repo-relative supporting scripts

## Obsidian Links

- [[00 Docs Index]]


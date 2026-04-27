---
tags:
  - cnt
  - type/documentation
  - status/active
  - type/validation
  - type/operation
  - strategy/breakout_v3
  - graph-view
  - obsidian
  - type/analysis
  - cnt-v2-implementation-hygiene-check-ko
---

# CNT v2 구현 위생 점검

## 목적

이 메모는 실제 dashboard 및 gate-display 패치를 적용하기 전에, 깨끗한 구현 전략을 정의한다.

## 현재 dirty 파일

현재 working tree에는 아래가 포함된다.

### Noise / Local State

- `.obsidian/graph.json`
- `.obsidian/workspace.json`

### Auto-Generated Or Runtime-Adjacent

- `docs/CNT v2 TESTNET PERFORMANCE REPORT.md`

### Current Analysis Documents

- `docs/00 Docs Index.md`
- `docs/CNT v2 POST-READY DEGRADATION REVIEW.md`
- `docs/CNT v2 BREAKOUT LAST 3 TRADES REVIEW.md`
- `docs/CNT v2 STRATEGY ISOLATION COMPARISON.md`
- `docs/CNT v2 GATE DISPLAY CONSISTENCY AUDIT.md`
- `docs/CNT v2 DASHBOARD WARNING ENHANCEMENT INSTRUCTION.md`

### Unrelated Suspicious File

- `docs/cnt_v2_architecture_design.md`

이 파일은 현재 patch scope 밖에 있으므로 별도로 다뤄야 한다.

## 패치 전 clean 전략

### Step 1

local noise 파일 복원:

- `.obsidian/graph.json`
- `.obsidian/workspace.json`

### Step 2

관련 없는 문서 변경을 구현 패치와 섞지 않는다.

특히 다음 파일은 분리:

- `docs/cnt_v2_architecture_design.md`

### Step 3

현재 auto-updated performance report를 포함할지 결정:

- 같은 patch set의 증거로 필요하면 포함
- 아니면 logic patch commit에서는 제외

### Step 4

패치 작업 커밋은 최대 두 묶음으로만 분리:

1. analysis/spec documents
2. actual dashboard and gate-display patch

구현과 unrelated runtime artifact를 섞지 않는다.

## 패치 준비 확인

실제 code 또는 HTML patch 전에:

1. `git status`에는 관련 analysis/spec 문서만 남아 있어야 함
2. `.obsidian` noise는 복원돼 있어야 함
3. `docs/cnt_v2_architecture_design.md`는 제외되거나 별도 리뷰 대상이어야 함

## 최종 hygiene 규칙

실제 patch는 working tree가 아래만 포함할 때 적용해야 한다.

- patch documents
- 필요한 경우 performance report evidence
- target implementation files

그리고 그 외에는 없어야 한다.

## Obsidian Links

- [[CNT v2 VALIDATION REPORT KO]]



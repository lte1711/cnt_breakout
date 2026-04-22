---
tags:
  - cnt
  - docs
  - v2
  - hygiene
aliases:
  - CNT v2 IMPLEMENTATION HYGIENE CHECK
---

# CNT v2 IMPLEMENTATION HYGIENE CHECK

## Purpose

This note defines the clean implementation strategy before actual dashboard and gate-display patches are applied.

## Current Dirty Files

Current working tree includes:

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

This file is outside the current patch scope and should be handled separately.

## Clean Strategy Before Patch

### Step 1

Restore local noise files:

- `.obsidian/graph.json`
- `.obsidian/workspace.json`

### Step 2

Do not mix unrelated document changes into the implementation patch.

Specifically separate:

- `docs/cnt_v2_architecture_design.md`

### Step 3

Decide whether the current auto-updated performance report should be included:

- include only if it is needed as evidence for the same patch set
- otherwise keep it out of the logic patch commit

### Step 4

Commit patch work in two logical groups at most:

1. analysis/spec documents
2. actual dashboard and gate-display patch

Do not mix implementation with unrelated runtime artifacts.

## Patch Readiness Check

Before actual code or HTML patching:

1. `git status` should contain only relevant analysis/spec documents
2. `.obsidian` noise should be restored
3. unrelated `docs/cnt_v2_architecture_design.md` should be excluded or reviewed separately

## Final Hygiene Rule

The actual patch should be applied only after the working tree represents:

- patch documents
- optional performance report evidence
- target implementation files

and nothing else.

## Obsidian Links

- [[CNT v2 DASHBOARD PATCH TARGET MAPPING]]
- [[CNT v2 GATE DISPLAY ACTUAL PATCH SPEC]]
- [[CNT v2 BREAKOUT ISOLATION OBSERVATION WINDOW SPEC]]
- [[00 Docs Index|Docs Index]]

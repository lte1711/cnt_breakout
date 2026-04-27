---
tags:
  - cnt
  - type/documentation
  - status/active
  - strategy/breakout_v3
  - type/analysis
  - cnt-v2-breakout-v3-shadow-output-rebaseline-report
---

# CNT v2 BREAKOUT V3 SHADOW OUTPUT REBASELINE REPORT

## Summary

This step created a clean post-fix observation baseline for `breakout_v3` shadow output.

Purpose:

- preserve pre-fix mixed-semantic output
- clear current `breakout_v3` shadow output files
- regenerate a fresh baseline from the current evaluator logic only

## 1. Why Rebaseline Was Needed

Observed problem:

- historical `shadow_breakout_v3.jsonl` lines still contained pre-fix blocker semantics
- historical snapshot counts mixed old and new meanings

Implication:

- current shadow output could not be treated as a pure post-fix baseline

## 2. Archival Action

Archived before reset:

- `logs/archive/shadow_breakout_v3_pre_rebaseline_20260424_064140.jsonl`
- `data/archive/shadow_breakout_v3_snapshot_pre_rebaseline_20260424_064140.json`

Interpretation:

- historical evidence was preserved
- current baseline was allowed to restart cleanly

## 3. Reset And One-Shot Verification

Executed:

- current `logs/shadow_breakout_v3.jsonl` reset
- current `data/shadow_breakout_v3_snapshot.json` removed
- `run.ps1` executed once through the normal entry chain

Result:

- a fresh `breakout_v3` shadow event was written
- a fresh snapshot was regenerated from post-fix baseline only

## 4. BOM Compatibility Hardening

During rebaseline verification, snapshot regeneration exposed a UTF-8 BOM edge case when a log file was created by external tooling.

Applied hardening:

- `update_breakout_v3_shadow_snapshot()` now reads with `utf-8-sig`

Effect:

- snapshot rebuild is resilient to BOM-prefixed JSONL files

## 5. Current Post-Rebaseline Meaning

Current interpretation after rebaseline:

- `breakout_v3` shadow output is now suitable for post-fix-only observation
- pre-fix blocker names remain only in archived files
- future snapshot growth should be interpreted from the new baseline forward

## 6. Not Changed

This step did not change:

- `ACTIVE_STRATEGIES`
- `breakout_v1` active status
- order routing
- live activation

## Obsidian Links

- [[CNT v2 BREAKOUT V3 DESIGN DRAFT]]


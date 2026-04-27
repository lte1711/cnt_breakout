---
tags:
  - cnt
  - documentation
  - encoding
  - recovery
status: ACTIVE
created: 2026-04-26
---

# CNT Encoding Cause And Repair Report 20260426

## Design Summary

- Scope: identify the cause of recently observed Korean text mojibake and apply repository-level prevention.
- No runtime code, strategy logic, config, exchange state, order state, or data state was intentionally changed by this repair.
- The repair is limited to documentation encoding hygiene and editor configuration.

## Cause

VERIFIED:

- The affected Korean text is valid UTF-8 when read explicitly as UTF-8.
- Some files contained an embedded `U+FEFF` byte-order-mark character after YAML frontmatter rather than only at the physical start of the file.
- When read by a tool or console path that does not explicitly use UTF-8, the UTF-8 Korean bytes and embedded BOM can display as mixed CJK mojibake strings.

FACT:

- `docs/EXTRA ITEMS REGISTER.md` displayed correctly with `Get-Content -Encoding UTF8`.
- A scan found embedded BOM characters in multiple Markdown files under `docs/`.
- No remaining mojibake pattern matches were found after repair using the configured scan.

## Repair Applied

VERIFIED:

- Removed embedded `U+FEFF` characters from affected Markdown files.
- Added repository `.editorconfig` to require UTF-8 and LF line endings for future edits.
- Kept `.gitattributes` line-ending policy intact.

Affected files with embedded BOM removed:

```text
docs/CNT v1.1 STAGE 2 IMPLEMENTATION WORK INSTRUCTION.md
docs/CNT v2 BREAKOUT TREND FILTER REVIEW INSTRUCTION.md
docs/CNT v2 AUTO VALIDATION & DECISION SYSTEM WORK INSTRUCTION.md
docs/CNT v1.1 IMPLEMENTATION VALIDATION REPORT.md
docs/CNT v2 BREAKOUT REVIEW TIMER REPORT.md
docs/CNT v2 AUTO VALIDATION & DECISION SYSTEM PROGRESS REPORT.md
docs/CNT v1.1 STAGE 2 IMPLEMENTATION VALIDATION REPORT.md
docs/CNT v1.1 IMPLEMENTATION WORK INSTRUCTION.md
docs/CNT v2 BREAKOUT V1 RELAXATION EXPERIMENT PLAN.md
docs/CNT v2 PATCH WORK INSTRUCTION.md
docs/CNT v2 PERFORMANCE TUNING VALIDATION REPORT.md
docs/CNT v2 PERFORMANCE TUNING WORK INSTRUCTION.md
docs/CNT v2 PHASE 1 MONITORING IMPLEMENTATION REPORT.md
docs/CNT v2 TESTNET DATA COLLECTION INSTRUCTION.md
docs/CNT v2 VALIDATION REPORT.md
docs/cnt_v1_closure_validation_report.md
docs/EXTRA ITEMS REGISTER.md
```

## Operating Rule

Use explicit UTF-8 when inspecting Korean documentation from Windows PowerShell:

```powershell
Get-Content "docs\EXTRA ITEMS REGISTER.md" -Encoding UTF8
```

Do not judge a Markdown file as corrupted from a default console readout alone. Confirm with explicit UTF-8 read first.

## Validation Result

```text
embedded_bom_scan_after_repair = clean
mojibake_pattern_scan_after_repair = clean
editorconfig_added = yes
runtime_behavior_changed = no
```

## Record Text

The encoding issue was caused by a combination of UTF-8 Korean documents, embedded BOM characters inside Markdown content, and non-explicit UTF-8 console reads. The affected Markdown files were normalized by removing embedded BOM characters. A repository `.editorconfig` was added so future editors default to UTF-8 and LF line endings.

Related documents:

- [[EXTRA ITEMS REGISTER]]
- [[CNT_DOCS_GATE_THRESHOLD_AND_ENCODING_RECOVERY_20260426]]
- [[CNT_PARTIAL_EXIT_CONFIG_ALIGNMENT_REGISTER_20260426]]
- [[00 Docs Index]]

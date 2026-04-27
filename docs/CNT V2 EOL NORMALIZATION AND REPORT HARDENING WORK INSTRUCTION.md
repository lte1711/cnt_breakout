---
tags:
  - cnt
  - type/documentation
  - status/active
  - market-context
  - type/operation
  - obsidian
  - type/analysis
  - status/completed
  - cnt-v2-eol-normalization-and-report-generation-hardening-work-instruction
---

# CNT v2 EOL Normalization And Report Generation Hardening Work Instruction

## Purpose

This work finishes two reproducibility tasks:

1. make the repository-wide `.gitattributes` declaration match actual tracked file EOL state
2. force auto-generated performance reports to remain `LF` on Windows as well as other environments

Target statement after completion:

> CNT repository text files follow the declared LF policy both in configuration and in actual tracked state, and auto-generated performance reports keep that policy during regeneration.

## Current Judgment

Already completed:

- Obsidian non-standard `../...` links were removed
- `.obsidian/plugins/` structure was created
- Obsidian plugin installation policy was documented
- `.windsurf` default dependency was removed from repo-default context
- key files such as `.continuerules`, `AGENTS.md`, and `.vscode/settings.json` already match LF policy

Remaining issues:

- tracked files still need repository-wide EOL renormalization
- `docs/CNT v2 TESTNET PERFORMANCE REPORT.md` may be regenerated with platform-default line endings unless writing is forced to LF

## Execution Order

1. force LF output in `src/analytics/performance_report.py`
2. run repository-wide `git add --renormalize .`
3. regenerate the performance report
4. run `git add --renormalize .` again
5. validate tracked EOL state, tests, and compile checks
6. record the final judgment in docs

## Included Scope

- `.gitattributes`
- root Python files
- `src/**/*.py`
- `scripts/**/*.py`
- `docs/**/*.md`
- `.vscode/**/*.json`
- `.obsidian/**/*.json`
- other tracked text files

Excluded scope:

- ignored runtime artifacts
- local-only cache files
- third-party plugin bundles

## Completion Criteria

Completion requires all of the following:

1. `src/**/*.py` and root runtime Python files contain `CRLF = 0`
2. `src/analytics/performance_report.py` forces `LF` output
3. `docs/CNT v2 TESTNET PERFORMANCE REPORT.md` remains `LF only` after regeneration
4. `git add --renormalize .` leaves no further normalization diff
5. tests and compile checks pass
6. final status is written back to CNT docs

## Obsidian Links

- [[CNT TOOLCHAIN INTEGRATION REPORT]]


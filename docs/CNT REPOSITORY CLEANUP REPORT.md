---
title: CNT REPOSITORY CLEANUP REPORT
status: completed
updated: 2026-04-24
---

# CNT Repository Cleanup Report

## Objective

Remove clearly unnecessary repository artifacts without changing runtime logic, strategy logic, or official operating documents.

## Removed Items

### Obsolete Wrapper Script

- `scripts/simplify_graph_links_fixed.py`

Reason:
- The repository now uses `scripts/simplify_graph_links.py` as the single graph simplification entry point.
- The wrapper added no independent behavior.

### Broken Translation Source Drafts

- `docs/cnt_v1_final_strategy_architecture_spec_ko_source.md`
- `docs/cnt_v1_implementation_work_instruction_ko_source.md`

Reason:
- Both files contained broken-encoding source text rather than usable CNT documentation.
- They were not part of the active documentation chain.

### Python Cache Artifacts

- all `__pycache__/` directories
- all local `.pyc` cache files under the repository

Reason:
- These are generated artifacts.
- They are already excluded by `.gitignore`.

## Kept Intentionally

- `.obsidian/` files
  - kept because they are currently part of the user's working vault state
- `data/*.json` runtime snapshots
  - kept because they are active operating evidence
- `logs/` files
  - kept because they are runtime evidence and mostly ignored from Git already

## Validation

- no active runtime code path was changed
- no strategy configuration was changed
- no official validation or gate rule was changed
- `.gitignore` already covered Python cache artifacts

## Conclusion

The repository was cleaned by removing only clearly unnecessary cache, wrapper, and broken-source files while preserving all active CNT runtime, state, and documentation flows.

## Obsidian Links

- [[00 Docs Index]]

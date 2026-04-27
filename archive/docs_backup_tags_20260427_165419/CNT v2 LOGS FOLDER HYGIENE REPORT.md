---
aliases:
  - CNT v2 LOGS FOLDER HYGIENE REPORT
---

# CNT v2 LOGS FOLDER HYGIENE REPORT

## Summary

This review checked every file currently present under `logs/`.

Result:

- no clearly invalid runtime log target was found
- the real issue was `logs/scheduler_stdout.log`
- the file contained mixed-encoding content caused by external process redirection
- `run.ps1` was hardened so future scheduler stdout/stderr writes remain UTF-8
- existing `scheduler_stdout.log` content was normalized to remove embedded NUL bytes

## Checked Files

Files observed in `logs/`:

- `breakout_completion_alert.log`
- `breakout_review_timer.log`
- `portfolio.log`
- `runtime.log`
- `scheduler_stderr.log`
- `scheduler_stdout.log`
- `shadow_breakout_v2.jsonl`
- `signal.log`

## Valid Files

The following files are valid by current repository design and script references:

- `runtime.log`
- `signal.log`
- `portfolio.log`
- `shadow_breakout_v2.jsonl`
- `scheduler_stdout.log`
- `scheduler_stderr.log`
- `breakout_completion_alert.log`
- `breakout_review_timer.log`

Reason:

- `runtime.log`, `signal.log`, and `portfolio.log` are part of the AGENTS.md baseline
- `shadow_breakout_v2.jsonl` is defined in `config.py`
- `scheduler_stdout.log` and `scheduler_stderr.log` are created by `run.ps1`
- `breakout_completion_alert.log` is created by `scripts/breakout_completion_alert.ps1`
- `breakout_review_timer.log` is created by `scripts/breakout_review_timer.ps1`

## Actual Fault

### scheduler_stdout.log

Observed fault:

- lines such as `engine strategy v1 started` were written with embedded NUL bytes
- this produced visible mojibake-style output in PowerShell and text readers

Cause:

- `run.ps1` used mixed logging paths:
  - `Add-Content` for scheduler markers
  - shell redirection for Python stdout/stderr
- this allowed mixed encoding behavior inside the same file

## Fix Applied

### run.ps1

Applied changes:

- added UTF-8-safe log helper
- replaced direct scheduler marker appends with explicit UTF-8 writes
- replaced external process `1>>` / `2>>` redirection with `System.Diagnostics.Process`
  capture
- stdout/stderr are now captured first and then appended as UTF-8 text

### Existing scheduler_stdout.log

Applied cleanup:

- existing embedded NUL bytes were removed
- file is now readable as normal text

## Non-Fault Findings

### scheduler_stderr.log

Current content shows a historical Python path resolution error from an earlier scheduler run.

Interpretation:

- this is historical evidence, not a current malformed file
- keeping it is acceptable unless a separate log rotation policy is introduced

### breakout completion / review logs

Both files are small, valid, and script-owned.

Interpretation:

- they should not be treated as stray files
- they are intentional operational artifacts

## Final Decision

- `logs/` did not contain unknown rogue files
- the only confirmed defect was scheduler stdout encoding corruption
- that defect has been corrected at both:
  - source level (`run.ps1`)
  - existing file level (`scheduler_stdout.log`)

## Obsidian Links

- [[00 Docs Index]]


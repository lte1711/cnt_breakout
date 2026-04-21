---
tags:
  - cnt
  - v2
  - eol
  - reproducibility
  - report
aliases:
  - CNT v2 EOL NORMALIZATION AND REPORT HARDENING REPORT
---

# CNT v2 EOL Normalization And Report Hardening Report

## Summary

This stage completed the CNT reproducibility hardening work for line endings and auto-generated report output.

Final judgment:

- LF output is now forced in performance report generation
- tracked Python runtime files were renormalized to LF
- the generated performance report remains LF only after regeneration
- tests and compile checks passed

## Applied Changes

- `src/analytics/performance_report.py`
  - report writing now uses `newline="\n"`
- repository-wide tracked text files were renormalized to LF
- `docs/CNT v2 TESTNET PERFORMANCE REPORT.md` was regenerated after the change

## Verification

Verification results:

```text
CRLF_PY=0
binance_client.py CR=0
config.py CR=0
main.py CR=0
scripts/generate_performance_report.py CR=0
docs/CNT v2 TESTNET PERFORMANCE REPORT.md CR=0
```

```text
python -m unittest discover -s tests -p "test_*.py"
Ran 31 tests
OK
```

```text
python -m py_compile config.py main.py binance_client.py
OK
```

## Final Assessment

The declared `.gitattributes` LF policy now matches the checked runtime Python files and the generated performance report path.

Most important outcome:

> CNT report generation no longer falls back to Windows default line endings for the testnet performance report.

Operational note:

- the regeneration step still updates report timestamps and snapshot content as expected
- those content changes are separate from normalization itself

## Obsidian Links

- [[CNT V2 EOL NORMALIZATION AND REPORT HARDENING WORK INSTRUCTION]]
- [[CNT TOOLCHAIN INTEGRATION REPORT]]
- [[CNT v2 CURRENT STATUS ASSESSMENT]]
- [[CNT v2 TESTNET PERFORMANCE REPORT]]
- [[00 Docs Index|Docs Index]]

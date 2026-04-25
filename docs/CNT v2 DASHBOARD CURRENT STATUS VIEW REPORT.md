---
aliases:
  - CNT v2 Dashboard Current Status View Report
tags:
  - cnt
  - dashboard
  - recovery
  - operations
---

# CNT v2 Dashboard Current Status View Report

## Design Summary

The operations dashboard was updated to expose the current CNT operating state directly from runtime evidence files.

Changed file:

- [cnt_operations_dashboard.html](cnt_operations_dashboard.html)

The dashboard now reads:

- `data/auxiliary_recovery_status.json`
- `data/scheduler_heartbeat.json`

The new view keeps the official live gate authoritative and treats auxiliary recovery as observation only.

## Added Dashboard Sections

### Current Pullback Position

Shows the active `pullback_v1` open trade, including:

- entry price
- current price
- target price
- stop price
- quantity
- estimated unrealized PnL
- distance to target
- distance to stop
- entry time

This makes the next key event visible:

```text
pullback_v1 open trade closes as WIN or LOSS
```

### Scheduler Heartbeat

Shows scheduler status from `data/scheduler_heartbeat.json`, including:

- last finish time
- expected interval
- gap detection
- exit code
- last start and finish timestamps
- error message

### Auxiliary Recovery

The existing auxiliary panel now reads `data/auxiliary_recovery_status.json` directly instead of reconstructing recovery state from the performance snapshot.

The displayed recovery confirmation rule is:

```text
pullback_v1 closed_trades >= 50
expectancy > 0
profit_factor > 1.1
```

Until all criteria pass, the dashboard displays:

```text
RECOVERY_OBSERVATION_IN_PROGRESS
```

When all criteria pass, the dashboard displays:

```text
RECOVERY_EVIDENCE_CONFIRMED
```

## Validation Result

Validation was performed without changing strategy, risk, entry, exit, or order execution logic.

Results:

- dashboard script syntax check passed
- dashboard HTML returned HTTP 200 from the existing local server
- `data/auxiliary_recovery_status.json` returned HTTP 200
- `data/scheduler_heartbeat.json` returned HTTP 200
- Obsidian wiki-link target validation found no missing dashboard report links

## Obsidian Link Fix

The report was added to the vault entry path:

- [[00 Docs Index]]
- [[CNT OPERATIONS DASHBOARD GUIDE]]

The dashboard guide now uses vault-relative file links for:

- [cnt_operations_dashboard.html](cnt_operations_dashboard.html)
- [serve_dashboard.py](../scripts/serve_dashboard.py)

Current server URL:

```text
http://127.0.0.1:8000/docs/cnt_operations_dashboard.html
```

## Record Text

The dashboard now provides direct operator visibility for the current CNT state:

- official gate remains separate and authoritative
- auxiliary recovery is observational only
- pullback recovery sample progress is visible
- current open pullback position exit evidence is visible
- scheduler heartbeat and gap status are visible

Related notes:

- [[CNT OPERATIONS DASHBOARD GUIDE]]
- [[CNT v2 DASHBOARD AUXILIARY RECOVERY VIEW REPORT]]
- [[CNT_AUXILIARY_RECOVERY_STATUS_IMPLEMENTATION_20260425]]

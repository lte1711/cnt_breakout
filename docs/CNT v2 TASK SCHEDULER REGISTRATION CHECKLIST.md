---
tags:
  - cnt
  - docs
  - instruction
  - v2
aliases:
  - CNT v2 TASK SCHEDULER REGISTRATION CHECKLIST
---

# CNT v2 TASK SCHEDULER REGISTRATION CHECKLIST

Document purpose:
Quickly verify that Windows Task Scheduler is configured correctly.

Document status:
Execution Checklist / Must Pass Before Data Collection

---

# 1. Pre-Check

## Paths and Files

* [x] `C:\cnt\run.ps1` exists
* [x] `C:\cnt\main.py` exists
* [x] `C:\cnt\src\engine.py` exists
* [x] Python is executable

## Folder Structure

* [x] `C:\cnt\data` exists
* [x] `C:\cnt\logs` exists

## Manual Run Test

* [x] `powershell -ExecutionPolicy Bypass -File .\run.ps1` executed successfully
* [x] finished without runtime error
* [x] `logs\portfolio.log` updated
* [x] `logs\scheduler_stdout.log` created
* [x] `data\performance_snapshot.json` created
* [x] `data\live_gate_decision.json` created

---

# 2. Task Scheduler Registration Checklist

## Task Basics

* [x] task name: `CNT v2 Scheduler`
* [x] task registration completed

## Program Settings

* [x] program: `powershell.exe`
* [x] argument:

```text
-ExecutionPolicy Bypass -File "C:\cnt\run.ps1"
```

* [x] start in equivalent execution path confirmed through task command

```text
C:\cnt
```

## General Tab

* [x] run whether user is logged on or not
* [x] run with highest privileges

## Trigger

* [x] daily trigger / one-time repeating scheduler path registered
* [x] repeat every `10 minutes`
* [x] indefinite repetition behavior configured

## Settings

* [x] start-missed-task behavior configured
* [x] if already running, do not start new instance

---

# 3. Immediate Execution Check

* [x] task starts successfully from scheduler
* [x] scheduler last result shows success
* [x] `scheduler_start` present in stdout log
* [x] `scheduler_finish exit_code=0` present in stdout log
* [x] `scheduler_stderr.log` contains only an earlier fixed Python-path error and no current blocking error

---

# 4. Ongoing Observation

* [ ] 2 to 3 scheduler runs observed over 20 to 30 minutes
* [x] no duplicate execution seen in initial verification
* [x] lock file created and removed normally in initial verification
* [x] snapshot and decision files update on successful run

---

# 5. Success Status

```text
SCHEDULER_STATUS = ACTIVE
DATA_COLLECTION  = STARTED
CURRENT_GATE     = NOT_READY / INSUFFICIENT_SAMPLE
```

---

## Obsidian Links

- [[00 CNT Vault Home|Vault Home]]
- [[00 Docs Index|Docs Index]]

### Related
- [[00 Docs Index|Docs Index]]

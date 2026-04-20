---
tags:
  - cnt
  - docs
  - v2
aliases:
  - CNT v2 SCHEDULED DATA COLLECTION SETUP
---

# CNT v2 SCHEDULED DATA COLLECTION SETUP

## 1. `run.ps1` Final Form

The scheduler-ready `run.ps1` does the following:

* moves to repo root
* creates `data` and `logs` if missing
* prevents duplicate execution using `data/engine.lock`
* splits stdout and stderr into:
  * `logs/scheduler_stdout.log`
  * `logs/scheduler_stderr.log`
* records `scheduler_start`, `scheduler_finish`, and lock skips

## 2. Windows Task Scheduler Values

Program:

```text
powershell.exe
```

Arguments:

```text
-ExecutionPolicy Bypass -File "C:\cnt\run.ps1"
```

Start in:

```text
C:\cnt
```

## 3. Recommended Task Settings

General:

* task name: `CNT v2 Scheduler`
* run whether user is logged on or not
* run with highest privileges

Trigger:

* daily
* repeat every `10 minutes`
* indefinitely

Settings:

* start when available
* if task is already running: `Do not start a new instance`

## 4. PowerShell Registration Command

```powershell
$Action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument '-ExecutionPolicy Bypass -File "C:\cnt\run.ps1"' `
    -WorkingDirectory "C:\cnt"

$Trigger = New-ScheduledTaskTrigger -Daily -At 00:00
$Trigger.Repetition = (New-ScheduledTaskTrigger -Once -At (Get-Date).Date -RepetitionInterval (New-TimeSpan -Minutes 10) -RepetitionDuration ([TimeSpan]::MaxValue)).Repetition

$Settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -DontStopIfGoingOnBatteries `
    -AllowStartIfOnBatteries `
    -MultipleInstances IgnoreNew

Register-ScheduledTask `
    -TaskName "CNT v2 Scheduler" `
    -Action $Action `
    -Trigger $Trigger `
    -Settings $Settings `
    -Description "Run CNT v2 every 10 minutes for data collection"
```

Remove existing task first if needed:

```powershell
Unregister-ScheduledTask -TaskName "CNT v2 Scheduler" -Confirm:$false
```

## 5. Manual Validation Before Registration

```powershell
cd C:\cnt
powershell -ExecutionPolicy Bypass -File .\run.ps1
```

Check:

* `logs\scheduler_stdout.log`
* `logs\scheduler_stderr.log`
* `logs\portfolio.log`
* `data\performance_snapshot.json`
* `data\live_gate_decision.json`

## 6. Operating Rule

Before sufficient sample is collected:

```text
STATUS = PERFORMANCE_VALIDATION_IN_PROGRESS
```

Do not:

* tune ranker weights
* change risk parameters
* remove strategies

Only obvious bug fixes are allowed.

---

## Obsidian Links

- [[00 CNT Vault Home|Vault Home]]
- [[00 Docs Index|Docs Index]]

### Related
- [[00 Docs Index|Docs Index]]

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path | Split-Path -Parent
Set-Location $RepoRoot

$DataDir = Join-Path $RepoRoot "data"
$LogsDir = Join-Path $RepoRoot "logs"
$SignalLog = Join-Path $LogsDir "signal.log"
$AlertLog = Join-Path $LogsDir "breakout_completion_alert.log"
$AlertState = Join-Path $DataDir "breakout_completion_alert.json"

$ExperimentStartTime = [datetime]"2026-04-20 10:54:02"
$RequiredCycles = 30

if (-not (Test-Path $DataDir)) {
    New-Item -ItemType Directory -Path $DataDir | Out-Null
}

if (-not (Test-Path $LogsDir)) {
    New-Item -ItemType Directory -Path $LogsDir | Out-Null
}

if (-not (Test-Path $SignalLog)) {
    exit 0
}

$breakoutLines = @()
foreach ($line in Get-Content $SignalLog) {
    if ($line -match '^\[(?<ts>[^\]]+)\] strategy=breakout_v1 ') {
        $ts = [datetime]::Parse($matches["ts"])
        if ($ts -ge $ExperimentStartTime) {
            $breakoutLines += $line
        }
    }
}

$cycleCount = $breakoutLines.Count

if ($cycleCount -lt $RequiredCycles) {
    $stamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    Add-Content -Path $AlertLog -Value "[$stamp] breakout_completion_pending cycles=$cycleCount required=$RequiredCycles"
    exit 0
}

if (Test-Path $AlertState) {
    $existing = Get-Content $AlertState -Raw | ConvertFrom-Json
    if ($existing.status -eq "ALERT_SENT") {
        exit 0
    }
}

$now = Get-Date
$stamp = $now.ToString("yyyy-MM-dd HH:mm:ss")
$payload = @{
    timestamp = $stamp
    status = "ALERT_SENT"
    event = "breakout_observation_complete"
    required_cycles = $RequiredCycles
    observed_cycles = $cycleCount
    note = "CNT v2 breakout post-change observation window reached the configured completion threshold."
} | ConvertTo-Json -Depth 4

Set-Content -Path $AlertState -Value $payload -Encoding UTF8
Add-Content -Path $AlertLog -Value "[$stamp] breakout_observation_complete observed_cycles=$cycleCount required_cycles=$RequiredCycles"

try {
    msg * "CNT v2 breakout observation complete: $cycleCount cycles observed (required $RequiredCycles)."
}
catch {
    Add-Content -Path $AlertLog -Value "[$stamp] breakout_completion_alert_message_failed $_"
}

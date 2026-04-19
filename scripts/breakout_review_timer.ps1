$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path | Split-Path -Parent
Set-Location $RepoRoot

$DataDir = Join-Path $RepoRoot "data"
$LogsDir = Join-Path $RepoRoot "logs"
$ReviewLog = Join-Path $LogsDir "breakout_review_timer.log"
$ReviewState = Join-Path $DataDir "breakout_review_due.json"

if (-not (Test-Path $DataDir)) {
    New-Item -ItemType Directory -Path $DataDir | Out-Null
}

if (-not (Test-Path $LogsDir)) {
    New-Item -ItemType Directory -Path $LogsDir | Out-Null
}

$now = Get-Date
$stamp = $now.ToString("yyyy-MM-dd HH:mm:ss")

$payload = @{
    timestamp = $stamp
    event = "breakout_review_due"
    status = "READY_FOR_NEXT_JUDGMENT"
    note = "Review breakout_v1 experiment after the planned 8-hour accumulation window."
} | ConvertTo-Json -Depth 4

Set-Content -Path $ReviewState -Value $payload -Encoding UTF8
Add-Content -Path $ReviewLog -Value "[$stamp] breakout_review_due status=READY_FOR_NEXT_JUDGMENT"

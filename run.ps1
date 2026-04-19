$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $RepoRoot

$DataDir = Join-Path $RepoRoot "data"
$LogsDir = Join-Path $RepoRoot "logs"
$LockFile = Join-Path $DataDir "engine.lock"
$StdoutLog = Join-Path $LogsDir "scheduler_stdout.log"
$StderrLog = Join-Path $LogsDir "scheduler_stderr.log"
$PythonCandidates = @(
    (Join-Path $env:LOCALAPPDATA "Programs\Python\Python312\python.exe"),
    "C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe",
    "python.exe"
)

if (-not (Test-Path $DataDir)) {
    New-Item -ItemType Directory -Path $DataDir | Out-Null
}

if (-not (Test-Path $LogsDir)) {
    New-Item -ItemType Directory -Path $LogsDir | Out-Null
}

if (Test-Path $LockFile) {
    $now = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content -Path $StdoutLog -Value "[$now] scheduler_skip reason=lock_exists"
    exit 0
}

New-Item -ItemType File -Path $LockFile | Out-Null

try {
    $now = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content -Path $StdoutLog -Value "[$now] scheduler_start"

    $PythonExe = $null
    foreach ($candidate in $PythonCandidates) {
        if ($candidate -and (Test-Path $candidate -PathType Leaf)) {
            $PythonExe = $candidate
            break
        }
    }

    if (-not $PythonExe) {
        $PythonExe = "python.exe"
    }

    & $PythonExe .\main.py 1>> $StdoutLog 2>> $StderrLog

    $now = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content -Path $StdoutLog -Value "[$now] scheduler_finish exit_code=$LASTEXITCODE"

    exit $LASTEXITCODE
}
catch {
    $now = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content -Path $StderrLog -Value "[$now] scheduler_exception $_"
    exit 1
}
finally {
    if (Test-Path $LockFile) {
        Remove-Item $LockFile -ErrorAction SilentlyContinue
    }
}

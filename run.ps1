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

function Write-Utf8Log {
    param(
        [string]$Path,
        [string]$Message
    )

    if ([string]::IsNullOrEmpty($Message)) {
        return
    }

    Add-Content -Path $Path -Value $Message -Encoding utf8
}

if (-not (Test-Path $DataDir)) {
    New-Item -ItemType Directory -Path $DataDir | Out-Null
}

if (-not (Test-Path $LogsDir)) {
    New-Item -ItemType Directory -Path $LogsDir | Out-Null
}

if (Test-Path $LockFile) {
    $now = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Utf8Log -Path $StdoutLog -Message "[$now] scheduler_skip reason=lock_exists"
    exit 0
}

New-Item -ItemType File -Path $LockFile | Out-Null

try {
    $now = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Utf8Log -Path $StdoutLog -Message "[$now] scheduler_start"

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

    $ProcessStartInfo = New-Object System.Diagnostics.ProcessStartInfo
    $ProcessStartInfo.FileName = $PythonExe
    $ProcessStartInfo.Arguments = ".\\main.py"
    $ProcessStartInfo.WorkingDirectory = $RepoRoot
    $ProcessStartInfo.UseShellExecute = $false
    $ProcessStartInfo.RedirectStandardOutput = $true
    $ProcessStartInfo.RedirectStandardError = $true

    try {
        $Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
        $ProcessStartInfo.StandardOutputEncoding = $Utf8NoBom
        $ProcessStartInfo.StandardErrorEncoding = $Utf8NoBom
    }
    catch {
    }

    $Process = New-Object System.Diagnostics.Process
    $Process.StartInfo = $ProcessStartInfo
    $null = $Process.Start()

    $CapturedStdout = $Process.StandardOutput.ReadToEnd()
    $CapturedStderr = $Process.StandardError.ReadToEnd()
    $Process.WaitForExit()

    if (-not [string]::IsNullOrWhiteSpace($CapturedStdout)) {
        Write-Utf8Log -Path $StdoutLog -Message ($CapturedStdout.TrimEnd("`r", "`n"))
    }

    if (-not [string]::IsNullOrWhiteSpace($CapturedStderr)) {
        Write-Utf8Log -Path $StderrLog -Message ($CapturedStderr.TrimEnd("`r", "`n"))
    }

    $LASTEXITCODE = $Process.ExitCode

    $now = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Utf8Log -Path $StdoutLog -Message "[$now] scheduler_finish exit_code=$LASTEXITCODE"

    exit $LASTEXITCODE
}
catch {
    $now = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Utf8Log -Path $StderrLog -Message "[$now] scheduler_exception $_"
    exit 1
}
finally {
    if (Test-Path $LockFile) {
        Remove-Item $LockFile -ErrorAction SilentlyContinue
    }
}

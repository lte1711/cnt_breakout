# Small Trade + Validation Workflow
# 실거래(1회) + 자동평가를 반복 실행
# 용법: .\trade_with_validation.ps1 -NumTrades 7 -IntervalSeconds 300

param(
    [int]$NumTrades = 7,           # 54-60으로 도달하기 위해 7거래 실행
    [int]$IntervalSeconds = 300,   # 거래 간 대기시간 (테스트용 5분)
    [switch]$DryRun = $false       # DryRun: 실제 거래 없이 검증만
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $RepoRoot

# ====================================================================
# Logging
# ====================================================================

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMsg = "[$timestamp] [$Level] $Message"
    Write-Host $logMsg
    Add-Content -Path "logs/trade_validation.log" -Value $logMsg -Encoding utf8
}

# ====================================================================
# Main Workflow
# ====================================================================

Write-Log "============================================================"
Write-Log "TRADE WITH VALIDATION - STARTING"
Write-Log "============================================================"
Write-Log "NumTrades: $NumTrades"
Write-Log "Interval: $IntervalSeconds seconds"
Write-Log "DryRun: $DryRun"
Write-Log ""

$successCount = 0
$failureCount = 0
$tradeCount = 0

for ($i = 1; $i -le $NumTrades; $i++) {
    $tradeCount = $i
    Write-Log ""
    Write-Log ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    Write-Log "TRADE ITERATION $i / $NumTrades"
    Write-Log ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    Write-Log ""
    
    # ================================================================
    # Step 1: Execute trade (unless DryRun)
    # ================================================================
    
    if ($DryRun) {
        Write-Log "[Step 1] DRY RUN MODE - Skipping actual trade"
    } else {
        Write-Log "[Step 1] Executing trade #$i..."
        try {
            & python main.py 2>&1 | Tee-Object -FilePath "logs/trade_$i.log"
            Write-Log "[Step 1] Trade executed successfully"
            $successCount++
        } catch {
            Write-Log "[Step 1] Trade execution failed: $_" "ERROR"
            $failureCount++
        }
    }
    
    # ================================================================
    # Step 2: Auto-check (validation)
    # ================================================================
    
    Write-Log "[Step 2] Running auto-check..."
    try {
        python -m src.validation.auto_check 2>&1 | Tee-Object -FilePath "logs/check_$i.log"
        Write-Log "[Step 2] Auto-check completed"
    } catch {
        Write-Log "[Step 2] Auto-check failed: $_" "ERROR"
    }
    
    # ================================================================
    # Step 3: Mini evaluation
    # ================================================================
    
    Write-Log "[Step 3] Running mini evaluation..."
    try {
        python -m src.validation.mini_evaluator 2>&1 | Tee-Object -FilePath "logs/mini_eval_$i.log"
        Write-Log "[Step 3] Mini evaluation completed"
    } catch {
        Write-Log "[Step 3] Mini evaluation failed: $_" "ERROR"
    }
    
    # ================================================================
    # Step 4: Check progress
    # ================================================================
    
    Write-Log "[Step 4] Checking progress..."
    try {
        python -c "import json; s=json.loads(open('data/performance_snapshot.json').read()); print(f'Closed Trades: {s[\"closed_trades\"]} / Expectancy: {s[\"expectancy\"]:.6f} / Win Rate: {s[\"win_rate\"]:.4f}')" 2>&1 | ForEach-Object { Write-Log $_ }
    } catch {
        Write-Log "[Step 4] Progress check had error (non-critical)" "WARN"
    }
    
    # ================================================================
    # Step 5: Wait for next trade (if not last)
    # ================================================================
    
    if ($i -lt $NumTrades) {
        Write-Log "[Step 5] Waiting $IntervalSeconds seconds before next trade..."
        Start-Sleep -Seconds $IntervalSeconds
    } else {
        Write-Log "[Step 5] Final trade completed - no wait needed"
    }
    
    Write-Log ""
}

# ====================================================================
# Final Summary
# ====================================================================

Write-Log ""
Write-Log "============================================================"
Write-Log "TRADE WITH VALIDATION - SUMMARY"
Write-Log "============================================================"
Write-Log "Total iterations: $tradeCount"
Write-Log "Successful trades: $successCount"
Write-Log "Failed trades: $failureCount"
Write-Log ""

try {
    python -c "import json; s=json.loads(open('data/performance_snapshot.json').read()); d=json.loads(open('data/live_gate_decision.json').read()); print(f'Final: Closed={s[\"closed_trades\"]} | Expectancy={s[\"expectancy\"]:.6f} | WR={s[\"win_rate\"]:.4f} | GATE={d[\"status\"]}')" 2>&1 | ForEach-Object { Write-Log $_ }
} catch {
    Write-Log "Final summary check had error (non-critical)" "WARN"
}

Write-Log ""
Write-Log "============================================================"
Write-Log "END OF WORKFLOW"
Write-Log "============================================================"

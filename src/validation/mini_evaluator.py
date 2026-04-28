"""
Mini evaluation script - 5 trade 단위 성능 평가
각 5 거래 구간마다 실행하여 expectancy 안정성을 검증
"""

from pathlib import Path
import json
from datetime import datetime


def load_performance_snapshot(snapshot_file: Path) -> dict:
    if not snapshot_file.exists():
        return {}
    try:
        return json.loads(snapshot_file.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"ERROR loading snapshot: {e}")
        return {}


def load_strategy_metrics(metrics_file: Path) -> dict:
    if not metrics_file.exists():
        return {}
    try:
        return json.loads(metrics_file.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"ERROR loading metrics: {e}")
        return {}


def load_live_gate_decision(decision_file: Path) -> dict:
    if not decision_file.exists():
        return {}
    try:
        return json.loads(decision_file.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"ERROR loading decision: {e}")
        return {}


def evaluate_mini(snapshot: dict, metrics: dict, decision: dict, trade_count_target: int) -> dict:
    closed_trades = int(snapshot.get("closed_trades", 0) or 0)
    expectancy = float(snapshot.get("expectancy", 0.0) or 0.0)
    win_rate = float(snapshot.get("win_rate", 0.0) or 0.0)
    net_pnl = float(snapshot.get("net_pnl", 0.0) or 0.0)
    wins = int(snapshot.get("wins", 0) or 0)
    losses = int(snapshot.get("losses", 0) or 0)
    profit_factor = float(snapshot.get("profit_factor", 0.0) or 0.0)
    max_consecutive_losses = int(snapshot.get("max_consecutive_losses", 0) or 0)
    
    gate_status = decision.get("status", "UNKNOWN")
    
    pullback_data = metrics.get("pullback_v1", {})
    pullback_trades = int(pullback_data.get("trades_closed", 0) or 0)
    
    progress_pct = (closed_trades / trade_count_target * 100) if trade_count_target > 0 else 0
    
    result = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "closed_trades": closed_trades,
        "trade_count_target": trade_count_target,
        "progress_pct": round(progress_pct, 1),
        "pullback_v1_trades": pullback_trades,
        "expectancy": round(expectancy, 6),
        "win_rate": round(win_rate, 4),
        "net_pnl": round(net_pnl, 8),
        "wins": wins,
        "losses": losses,
        "profit_factor": round(profit_factor, 4),
        "max_consecutive_losses": max_consecutive_losses,
        "live_gate_status": gate_status,
        "evaluation": _evaluate_metrics(expectancy, win_rate, closed_trades, gate_status),
    }
    
    return result


def _evaluate_metrics(expectancy: float, win_rate: float, closed_trades: int, gate_status: str) -> dict:
    checks = {
        "expectancy_positive": expectancy > 0,
        "win_rate_above_50pct": win_rate > 0.50,
        "live_gate_ready": gate_status == "LIVE_READY",
        "sufficient_trades": closed_trades >= 50,
    }
    
    passed = sum(1 for v in checks.values() if v)
    total = len(checks)
    
    return {
        "checks": checks,
        "passed": passed,
        "total": total,
        "status": "PASS" if passed == total else "REVIEW" if passed >= 3 else "FAIL",
    }


def run_mini_evaluation(
    metrics_file: Path = Path("data/strategy_metrics.json"),
    portfolio_log_file: Path = Path("logs/portfolio.log"),
    snapshot_file: Path = Path("data/performance_snapshot.json"),
    decision_file: Path = Path("data/live_gate_decision.json"),
    trade_count_target: int = 60,
):
    print("=" * 70)
    print("MINI EVALUATION - 5 TRADE UNIT CHECK")
    print("=" * 70)
    
    snapshot = load_performance_snapshot(snapshot_file)
    metrics = load_strategy_metrics(metrics_file)
    decision = load_live_gate_decision(decision_file)
    
    if not snapshot:
        print("ERROR: No performance snapshot found")
        return
    
    result = evaluate_mini(snapshot, metrics, decision, trade_count_target)
    
    print()
    print(f"Timestamp: {result['timestamp']}")
    print(f"Progress: {result['closed_trades']}/{result['trade_count_target']} trades ({result['progress_pct']}%)")
    print(f"pullback_v1 trades: {result['pullback_v1_trades']}")
    print()
    print("--- PERFORMANCE METRICS ---")
    print(f"Expectancy: {result['expectancy']:.6f}")
    print(f"Win Rate: {result['win_rate']:.4f} ({result['wins']}W/{result['losses']}L)")
    print(f"Net PnL: {result['net_pnl']:.8f} USDT")
    print(f"Profit Factor: {result['profit_factor']:.4f}")
    print(f"Max Consecutive Losses: {result['max_consecutive_losses']}")
    print()
    print("--- LIVE_GATE STATUS ---")
    print(f"Status: {result['live_gate_status']}")
    print()
    print("--- EVALUATION ---")
    evals = result["evaluation"]
    print(f"Expectancy Positive: {evals['checks']['expectancy_positive']}")
    print(f"Win Rate > 50%: {evals['checks']['win_rate_above_50pct']}")
    print(f"LIVE_GATE Ready: {evals['checks']['live_gate_ready']}")
    print(f"Sufficient Trades (50+): {evals['checks']['sufficient_trades']}")
    print()
    print(f"Passed: {evals['passed']}/{evals['total']}")
    print(f"Status: {evals['status']}")
    print()
    print("=" * 70)
    
    return result


if __name__ == "__main__":
    result = run_mini_evaluation(trade_count_target=60)

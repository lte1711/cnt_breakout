"""
Auto-check - 매 거래 후 자동 평가 및 상태 리포트
"""

from pathlib import Path
import json
from datetime import datetime
from src.analytics.performance_snapshot import generate_and_save_performance_snapshot
from src.validation.live_gate_evaluator import evaluate_live_gate, save_live_gate_decision
from src.validation.mini_evaluator import evaluate_mini, load_performance_snapshot, load_strategy_metrics
from src.validation.live_monitor import get_live_status


def run_auto_check(trade_count_target: int = 60):
    """
    Automatically:
    1. Regenerate performance snapshot
    2. Re-evaluate live gate
    3. Run mini evaluation
    4. Display live monitor status
    """
    
    print()
    print("=" * 70)
    print("AUTO-CHECK: COMPREHENSIVE VALIDATION")
    print("=" * 70)
    print()
    
    try:
        print("[1/4] Regenerating performance snapshot...")
        snapshot = generate_and_save_performance_snapshot(
            metrics_file=Path("data/strategy_metrics.json"),
            portfolio_log_file=Path("logs/portfolio.log"),
            snapshot_file=Path("data/performance_snapshot.json"),
            portfolio_state_file=Path("data/portfolio_state.json"),
        )
        print(f"  OK - {snapshot['closed_trades']} closed trades")
    except Exception as e:
        print(f"  ERROR: {e}")
        return
    
    try:
        print("[2/4] Re-evaluating live gate...")
        decision = evaluate_live_gate(snapshot)
        save_live_gate_decision(Path("data/live_gate_decision.json"), decision)
        print(f"  OK - Status: {decision['status']}")
    except Exception as e:
        print(f"  ERROR: {e}")
        return
    
    try:
        print("[3/4] Running mini evaluation...")
        metrics = load_strategy_metrics(Path("data/strategy_metrics.json"))
        mini_result = evaluate_mini(snapshot, metrics, decision, trade_count_target)
        print(f"  OK - {mini_result['closed_trades']}/{mini_result['trade_count_target']} trades")
        print(f"      Expectancy: {mini_result['expectancy']:.6f}")
        print(f"      Win Rate: {mini_result['win_rate']:.4f}")
        print(f"      Status: {mini_result['evaluation']['status']}")
    except Exception as e:
        print(f"  ERROR: {e}")
        return
    
    try:
        print("[4/4] Getting live monitor status...")
        live_status = get_live_status()
        print(f"  OK - {live_status['system_status']}")
    except Exception as e:
        print(f"  ERROR: {e}")
        return
    
    print()
    print("=" * 70)
    print("AUTO-CHECK COMPLETE")
    print("=" * 70)
    print()
    
    return {
        "snapshot": snapshot,
        "decision": decision,
        "mini_result": mini_result,
        "live_status": live_status,
    }


if __name__ == "__main__":
    run_auto_check(trade_count_target=60)

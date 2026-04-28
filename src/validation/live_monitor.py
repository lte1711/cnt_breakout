"""
Live monitor - 실시간 거래 상태 추적
"""

from pathlib import Path
import json
from datetime import datetime


def load_state(state_file: Path) -> dict:
    if not state_file.exists():
        return {}
    try:
        return json.loads(state_file.read_text(encoding="utf-8"))
    except Exception:
        return {}


def load_portfolio_state(portfolio_state_file: Path) -> dict:
    if not portfolio_state_file.exists():
        return {}
    try:
        return json.loads(portfolio_state_file.read_text(encoding="utf-8"))
    except Exception:
        return {}


def get_last_portfolio_log_entries(portfolio_log_file: Path, num_entries: int = 10) -> list[str]:
    if not portfolio_log_file.exists():
        return []
    
    lines = portfolio_log_file.read_text(encoding="utf-8").splitlines()
    return lines[-num_entries:] if lines else []


def analyze_portfolio_log_entry(entry: str) -> dict:
    """Parse a portfolio log entry and extract key information"""
    result = {
        "raw": entry,
        "action": None,
        "strategy": None,
        "decision_id": None,
        "pnl": None,
        "reason": None,
    }
    
    if "action=" in entry:
        result["action"] = entry.split("action=", 1)[1].split()[0]
    
    if "selected_strategy=" in entry:
        result["strategy"] = entry.split("selected_strategy=", 1)[1].split()[0]
    
    if "decision_id=" in entry:
        result["decision_id"] = entry.split("decision_id=", 1)[1].split()[0]
    
    if "close_pnl_estimate=" in entry:
        try:
            result["pnl"] = float(entry.split("close_pnl_estimate=", 1)[1].split()[0])
        except (ValueError, IndexError):
            pass
    
    if "reason=" in entry:
        result["reason"] = entry.split("reason=", 1)[1].split()[0]
    
    return result


def get_live_status(
    state_file: Path = Path("data/state.json"),
    portfolio_state_file: Path = Path("data/portfolio_state.json"),
    portfolio_log_file: Path = Path("logs/portfolio.log"),
) -> dict:
    state = load_state(state_file)
    portfolio_state = load_portfolio_state(portfolio_state_file)
    recent_logs = get_last_portfolio_log_entries(portfolio_log_file, num_entries=5)
    
    pending_order = state.get("pending_order", {}) or {}
    open_trade = state.get("open_trade", {}) or {}
    
    status = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "system_status": state.get("status", "UNKNOWN"),
        "pending_order": {
            "exists": bool(pending_order),
            "order_id": pending_order.get("orderId") if pending_order else None,
            "side": pending_order.get("side") if pending_order else None,
            "strategy": pending_order.get("strategy_name") if pending_order else None,
        },
        "open_trade": {
            "exists": bool(open_trade),
            "entry_price": open_trade.get("entry_price") if open_trade else None,
            "entry_qty": open_trade.get("entry_qty") if open_trade else None,
            "strategy": open_trade.get("strategy_name") if open_trade else None,
            "entry_time": open_trade.get("entry_time") if open_trade else None,
        },
        "portfolio": {
            "total_exposure": portfolio_state.get("total_exposure", 0),
            "open_positions_count": len(portfolio_state.get("open_positions", [])) if portfolio_state else 0,
            "cash_balance": portfolio_state.get("cash_balance", 0),
            "daily_loss_count": portfolio_state.get("daily_loss_count", 0),
            "consecutive_losses": portfolio_state.get("consecutive_losses", 0),
        },
        "recent_activity": [analyze_portfolio_log_entry(line) for line in recent_logs],
    }
    
    return status


def print_live_status(status: dict) -> None:
    print()
    print("=" * 70)
    print("LIVE MONITOR - REAL-TIME STATUS")
    print("=" * 70)
    print()
    print(f"Time: {status['timestamp']}")
    print(f"System Status: {status['system_status']}")
    print()
    
    print("--- PENDING ORDER ---")
    pending = status["pending_order"]
    if pending["exists"]:
        print(f"Order ID: {pending['order_id']}")
        print(f"Side: {pending['side']}")
        print(f"Strategy: {pending['strategy']}")
    else:
        print("(None)")
    print()
    
    print("--- OPEN TRADE ---")
    trade = status["open_trade"]
    if trade["exists"]:
        print(f"Entry Price: {trade['entry_price']}")
        print(f"Entry Qty: {trade['entry_qty']}")
        print(f"Strategy: {trade['strategy']}")
        print(f"Entry Time: {trade['entry_time']}")
    else:
        print("(None)")
    print()
    
    print("--- PORTFOLIO STATE ---")
    pf = status["portfolio"]
    print(f"Total Exposure: {pf['total_exposure']}")
    print(f"Open Positions: {pf['open_positions_count']}")
    print(f"Cash Balance: {pf['cash_balance']}")
    print(f"Daily Loss Count: {pf['daily_loss_count']}")
    print(f"Consecutive Losses: {pf['consecutive_losses']}")
    print()
    
    print("--- RECENT ACTIVITY (last 5 entries) ---")
    for i, entry in enumerate(status["recent_activity"], 1):
        print(f"{i}. {entry['action']} | {entry['strategy']} | PnL: {entry['pnl']}")
    print()
    print("=" * 70)


def run_live_monitor(
    state_file: Path = Path("data/state.json"),
    portfolio_state_file: Path = Path("data/portfolio_state.json"),
    portfolio_log_file: Path = Path("logs/portfolio.log"),
) -> dict:
    status = get_live_status(state_file, portfolio_state_file, portfolio_log_file)
    print_live_status(status)
    return status


if __name__ == "__main__":
    run_live_monitor()

"""
Breakout V3 Live Monitor

Real-time monitoring script for breakout_v3 strategy execution.
Provides live status updates and alerts for critical events.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any


class BreakoutV3Monitor:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.log_file = project_root / "logs" / "runtime.log"
        self.signal_log_file = project_root / "logs" / "signal.log"
        self.portfolio_log_file = project_root / "logs" / "portfolio.log"
        self.state_file = project_root / "data" / "state.json"
        self.snapshot_file = project_root / "data" / "performance_snapshot.json"
        
    def get_latest_state(self) -> Dict[str, Any]:
        """Read latest engine state"""
        if not self.state_file.exists():
            return {}
        try:
            return json.loads(self.state_file.read_text(encoding="utf-8"))
        except Exception:
            return {}
    
    def get_latest_signals(self, count: int = 5) -> list:
        """Read latest signal log entries"""
        if not self.signal_log_file.exists():
            return []
        try:
            lines = self.signal_log_file.read_text(encoding="utf-8").strip().splitlines()
            return lines[-count:] if lines else []
        except Exception:
            return []
    
    def get_latest_portfolio_entries(self, count: int = 5) -> list:
        """Read latest portfolio log entries"""
        if not self.portfolio_log_file.exists():
            return []
        try:
            lines = self.portfolio_log_file.read_text(encoding="utf-8").strip().splitlines()
            return lines[-count:] if lines else []
        except Exception:
            return []
    
    def check_breakout_v3_activity(self) -> Dict[str, Any]:
        """Check breakout_v3 specific activity"""
        state = self.get_latest_state()
        signals = self.get_latest_signals(10)
        portfolio_entries = self.get_latest_portfolio_entries(10)
        
        # Check if breakout_v3 is active
        is_active = state.get("strategy_name") == "breakout_v3"
        
        # Check for recent breakout_v3 signals
        recent_signals = [
            s for s in signals 
            if "breakout_v3" in s
        ]
        
        # Check for open trade
        has_open_trade = bool(state.get("open_trade"))
        
        # Check for pending order
        has_pending_order = bool(state.get("pending_order"))
        
        # Get last action
        last_action = state.get("action", "UNKNOWN")
        
        return {
            "is_active": is_active,
            "has_open_trade": has_open_trade,
            "has_pending_order": has_pending_order,
            "last_action": last_action,
            "recent_signal_count": len(recent_signals),
            "last_run_time": state.get("last_run_time"),
        }
    
    def print_status(self):
        """Print current status to console"""
        activity = self.check_breakout_v3_activity()
        state = self.get_latest_state()
        
        print("\n" + "="*60)
        print(f"BREAKOUT V3 LIVE MONITOR - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        print(f"\nStrategy Status:")
        print(f"  Active: {'YES' if activity['is_active'] else 'NO'}")
        print(f"  Last Action: {activity['last_action']}")
        print(f"  Last Run: {activity['last_run_time'] or 'NEVER'}")
        
        print(f"\nPosition Status:")
        print(f"  Open Trade: {'YES' if activity['has_open_trade'] else 'NO'}")
        print(f"  Pending Order: {'YES' if activity['has_pending_order'] else 'NO'}")
        
        print(f"\nSignal Activity:")
        print(f"  Recent Signals (last 10): {activity['recent_signal_count']}")
        
        if activity['has_open_trade']:
            open_trade = state.get("open_trade", {})
            print(f"\nOpen Trade Details:")
            print(f"  Entry Price: {open_trade.get('entry_price', 'N/A')}")
            print(f"  Entry Qty: {open_trade.get('entry_qty', 'N/A')}")
            print(f"  Stop Price: {open_trade.get('stop_price', 'N/A')}")
            print(f"  Target Price: {open_trade.get('target_price', 'N/A')}")
        
        if activity['has_pending_order']:
            pending = state.get("pending_order", {})
            print(f"\nPending Order Details:")
            print(f"  Order ID: {pending.get('orderId', 'N/A')}")
            print(f"  Status: {pending.get('status', 'N/A')}")
            print(f"  Side: {pending.get('side', 'N/A')}")
        
        print("\n" + "="*60 + "\n")
    
    def monitor_continuously(self, interval_seconds: int = 60):
        """Continuously monitor and print status"""
        print("Starting continuous monitoring...")
        print(f"Update interval: {interval_seconds} seconds")
        print("Press Ctrl+C to stop\n")
        
        try:
            while True:
                self.print_status()
                time.sleep(interval_seconds)
        except KeyboardInterrupt:
            print("\nMonitoring stopped.")


def main():
    project_root = Path(__file__).resolve().parent.parent
    monitor = BreakoutV3Monitor(project_root)
    
    # Single status check
    monitor.print_status()
    
    # Uncomment below for continuous monitoring
    # monitor.monitor_continuously(interval_seconds=60)


if __name__ == "__main__":
    main()

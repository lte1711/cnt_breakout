from __future__ import annotations

import ast
import json
from collections import Counter
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
LOGS_DIR = ROOT / "logs"

SNAPSHOT_FILE = DATA_DIR / "performance_snapshot.json"
DECISION_FILE = DATA_DIR / "live_gate_decision.json"
PORTFOLIO_LOG_FILE = LOGS_DIR / "portfolio.log"
RUNTIME_LOG_FILE = LOGS_DIR / "runtime.log"
OUTPUT_FILE = DATA_DIR / "runtime_monitor_report.json"


def _load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def _tail_lines(path: Path, limit: int) -> list[str]:
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()
    return lines[-limit:]


def _parse_key_value_line(line: str) -> dict:
    result: dict[str, object] = {}
    payload = line.strip()
    if payload.startswith("[") and "] " in payload:
        payload = payload.split("] ", 1)[1]

    for key in [
        "action",
        "price",
        "strategy_name",
        "reason",
        "selected_strategy",
        "rank_score",
        "blocked_by_policy",
        "close_action",
        "close_pnl_estimate",
    ]:
        marker = f"{key}="
        if marker in payload:
            value = payload.split(marker, 1)[1].split()[0]
            result[key] = value

    for complex_key in ["pending", "open_trade", "rank_score_components"]:
        marker = f"{complex_key}="
        if marker not in payload:
            continue
        value = payload.split(marker, 1)[1]
        if complex_key == "pending" and " open_trade=" in value:
            value = value.split(" open_trade=", 1)[0]
        elif complex_key == "open_trade" and " strategy_name=" in value:
            value = value.split(" strategy_name=", 1)[0]
        elif complex_key == "rank_score_components":
            if " strategy_expectancy_snapshot=" in value:
                value = value.split(" strategy_expectancy_snapshot=", 1)[0]
            elif " blocked_by_policy=" in value:
                value = value.split(" blocked_by_policy=", 1)[0]
        try:
            result[complex_key] = ast.literal_eval(value)
        except Exception:
            result[complex_key] = None

    if line.startswith("[") and "]" in line:
        result["timestamp"] = line[1:].split("]", 1)[0]

    return result


def _rank_score_zero_streak(rank_scores: list[float]) -> int:
    streak = 0
    for score in reversed(rank_scores):
        if float(score) == 0.0:
            streak += 1
            continue
        break
    return streak


def _strategy_bias(selected_strategy_counts: dict) -> dict:
    filtered = {k: int(v) for k, v in selected_strategy_counts.items() if k != "NONE"}
    if not filtered:
        return {"status": "NONE", "strategy": None, "count": 0}

    strategy, count = max(filtered.items(), key=lambda item: item[1])
    if count >= 30:
        return {"status": "DETECTED", "strategy": strategy, "count": count}
    return {"status": "NONE", "strategy": strategy, "count": count}


def _risk_level(snapshot: dict) -> str:
    max_losses = int(snapshot.get("max_consecutive_losses", 0) or 0)
    if max_losses >= 5:
        return "CRITICAL"
    if max_losses >= 3:
        return "WARNING"
    return "NORMAL"


def _failsafe_status(runtime_lines: list[str]) -> dict:
    events = [_parse_key_value_line(line) for line in runtime_lines if "action=" in line]
    relevant = [
        event
        for event in events
        if event.get("action")
        in {
            "SELL_SUBMITTED",
            "PENDING_CONFIRMED",
            "STOP_MARKET_FILLED",
            "TRAILING_STOP_FILLED",
            "PROTECTIVE_EXIT_CANCEL_FAILED",
            "STOP_MARKET_SUBMITTED",
            "TRAILING_STOP_SUBMITTED",
            "SELL_FILLED",
            "BUY_FILLED",
        }
    ]

    for index, event in enumerate(relevant):
        if event.get("action") != "SELL_SUBMITTED":
            continue
        pending = event.get("pending")
        open_trade = event.get("open_trade")
        if not isinstance(pending, dict) or not isinstance(open_trade, dict):
            continue
        if str(pending.get("exit_type") or "").upper() not in {"TARGET", "TIME_EXIT", "PARTIAL"}:
            continue

        stop_price = float(open_trade.get("stop_price", 0.0) or 0.0)
        order_id = int(pending.get("orderId", 0) or 0)
        after = relevant[index + 1 :]
        saw_price_below_stop = False
        pending_repeats = 0
        protective_exit = False
        cancel_failure = False
        terminal_fill_after_stop_breach = False
        terminal_limit_fill_without_stop_breach = False

        for follow in after:
            follow_action = str(follow.get("action") or "")
            follow_pending = follow.get("pending")
            same_order = isinstance(follow_pending, dict) and int(follow_pending.get("orderId", 0) or 0) == order_id

            if follow_action == "PROTECTIVE_EXIT_CANCEL_FAILED":
                cancel_failure = True
                break

            if follow_action in {"STOP_MARKET_FILLED", "TRAILING_STOP_FILLED", "STOP_MARKET_SUBMITTED", "TRAILING_STOP_SUBMITTED"}:
                protective_exit = True
                break

            if follow_action == "SELL_FILLED":
                if saw_price_below_stop:
                    terminal_fill_after_stop_breach = True
                else:
                    terminal_limit_fill_without_stop_breach = True
                break

            if follow_action == "BUY_FILLED":
                break

            if same_order and follow_action == "PENDING_CONFIRMED":
                pending_repeats += 1
                try:
                    follow_price = float(follow.get("price", 0.0) or 0.0)
                except (TypeError, ValueError):
                    follow_price = 0.0
                if stop_price > 0 and follow_price <= stop_price:
                    saw_price_below_stop = True

        if cancel_failure:
            return {"status": "CRITICAL", "detail": "cancel_failed_without_protective_exit"}
        if terminal_fill_after_stop_breach:
            return {"status": "CHECK_REQUIRED", "detail": "pending_limit_remained_active_after_stop_breach"}
        if terminal_limit_fill_without_stop_breach:
            return {"status": "NO_CASE", "detail": "pending_limit_resolved_without_stop_breach"}
        if saw_price_below_stop and not protective_exit:
            return {"status": "CHECK_REQUIRED", "detail": f"pending_confirmed_repeated_below_stop:{pending_repeats}"}
        if protective_exit:
            return {"status": "OK", "detail": "protective_override_observed"}

    return {"status": "NO_CASE", "detail": "no_qualifying_pending_exit_case"}


def build_report() -> dict:
    snapshot = _load_json(SNAPSHOT_FILE)
    decision = _load_json(DECISION_FILE)
    portfolio_lines = _tail_lines(PORTFOLIO_LOG_FILE, 50)
    runtime_lines = _tail_lines(RUNTIME_LOG_FILE, 80)

    rank_scores = list(snapshot.get("rank_score_samples", []) or [])
    selected_strategy_counts = dict(snapshot.get("selected_strategy_counts", {}) or {})
    blocked_stats = dict(snapshot.get("blocked_signal_stats", {}) or {})
    risk_stats = dict(snapshot.get("risk_trigger_stats", {}) or {})

    alerts: list[str] = []
    zero_streak = _rank_score_zero_streak([float(x or 0.0) for x in rank_scores])
    if zero_streak >= 20:
        alerts.append("RANKER_STUCK")

    bias = _strategy_bias(selected_strategy_counts)
    if bias["status"] == "DETECTED":
        alerts.append("STRATEGY_BIAS")

    if int(snapshot.get("closed_trades", 0) or 0) == 0 and len(portfolio_lines) >= 36:
        alerts.append("NO_EXECUTION")

    failsafe = _failsafe_status(runtime_lines)
    if failsafe["status"] in {"CHECK_REQUIRED", "CRITICAL"}:
        alerts.append("EXIT_FAILSAFE_FAILURE")

    status = "OK"
    if alerts:
        status = "CRITICAL" if "EXIT_FAILSAFE_FAILURE" in alerts else "WARNING"

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": status,
        "closed_trades": int(snapshot.get("closed_trades", 0) or 0),
        "runtime_hours_estimate": round(len(portfolio_lines) / 6.0, 2),
        "rank_score_zero_streak": zero_streak,
        "strategy_bias": bias,
        "risk_level": _risk_level(snapshot),
        "failsafe": failsafe,
        "live_gate_status": decision.get("status", "UNKNOWN"),
        "live_gate_reason": decision.get("reason", "UNKNOWN"),
        "blocked_signal_stats": blocked_stats,
        "risk_trigger_stats": risk_stats,
        "alerts": alerts,
    }


def _format_console_report(report: dict) -> str:
    strategy_bias = report.get("strategy_bias", {})
    return "\n".join(
        [
            "[MONITOR REPORT]",
            "",
            f"status = {report.get('status', 'UNKNOWN')}",
            f"closed_trades = {report.get('closed_trades', 0)}",
            f"rank_score_zero_streak = {report.get('rank_score_zero_streak', 0)}",
            f"strategy_bias = {strategy_bias.get('status', 'NONE')}",
            f"risk_level = {report.get('risk_level', 'UNKNOWN')}",
            f"failsafe = {report.get('failsafe', {}).get('status', 'UNKNOWN')}",
            f"live_gate = {report.get('live_gate_status', 'UNKNOWN')} / {report.get('live_gate_reason', 'UNKNOWN')}",
            f"alerts = {', '.join(report.get('alerts', [])) if report.get('alerts') else 'NONE'}",
        ]
    )


def main() -> int:
    report = build_report()
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(_format_console_report(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

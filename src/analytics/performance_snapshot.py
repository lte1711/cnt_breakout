from __future__ import annotations

import ast
import json
from collections import Counter
from datetime import datetime
from pathlib import Path


RISK_TRIGGER_KEYS = {
    "LOSS_COOLDOWN",
    "DAILY_LOSS_LIMIT",
    "MAX_PORTFOLIO_EXPOSURE",
    "ONE_PER_SYMBOL_POLICY",
}


def _safe_float(value) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _safe_dict_literal(value: str) -> dict:
    try:
        parsed = ast.literal_eval(value)
    except (SyntaxError, ValueError):
        return {}
    return parsed if isinstance(parsed, dict) else {}


def _load_strategy_metrics(metrics_file: Path) -> dict:
    if not metrics_file.exists():
        return {}
    try:
        loaded = json.loads(metrics_file.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return loaded if isinstance(loaded, dict) else {}


def _parse_portfolio_log(log_file: Path) -> dict:
    blocked_stats: Counter = Counter()
    no_ranked_signal_legacy_count = 0
    no_ranked_signal_details: Counter = Counter()
    entry_gate_details: Counter = Counter()
    risk_trigger_stats: Counter = Counter()
    selected_strategy_counts: Counter = Counter()
    close_pnls: list[float] = []
    rank_scores: list[float] = []
    rank_score_components_samples: list[dict] = []

    if not log_file.exists():
        return {
            "blocked_signal_stats": {},
            "risk_trigger_stats": {},
            "selected_strategy_counts": {},
            "close_pnls": [],
            "max_consecutive_losses": 0,
            "rank_scores": [],
            "rank_score_components_samples": [],
        }

    for raw_line in log_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue

        if "selected_strategy=" in line and "selection_reason=highest_score" in line:
            strategy = line.split("selected_strategy=", 1)[1].split()[0]
            if strategy != "NONE":
                selected_strategy_counts[strategy] += 1

        if "blocked_by_policy=" in line:
            blocked_reason = line.split("blocked_by_policy=", 1)[1].split()[0]
            blocked_detail = None
            if "blocked_detail=" in line:
                blocked_detail = line.split("blocked_detail=", 1)[1].split()[0]
            if blocked_reason == "no_ranked_signal" and blocked_detail:
                no_ranked_signal_details[blocked_detail] += 1
            elif blocked_reason == "no_ranked_signal":
                no_ranked_signal_legacy_count += 1
            elif blocked_reason == "entry_gate" and blocked_detail:
                entry_gate_details[blocked_detail] += 1
            else:
                blocked_stats[blocked_reason] += 1
            if blocked_reason in RISK_TRIGGER_KEYS:
                risk_trigger_stats[blocked_reason] += 1

        for risk_key in RISK_TRIGGER_KEYS:
            if risk_key in line:
                risk_trigger_stats[risk_key] += 1

        if "close_pnl_estimate=" in line:
            raw_value = line.split("close_pnl_estimate=", 1)[1].split()[0]
            close_pnls.append(_safe_float(raw_value))

        if "rank_score=" in line:
            raw_value = line.split("rank_score=", 1)[1].split()[0]
            rank_scores.append(_safe_float(raw_value))

        if "rank_score_components=" in line:
            raw_value = line.split("rank_score_components=", 1)[1]
            if " strategy_expectancy_snapshot=" in raw_value:
                raw_value = raw_value.split(" strategy_expectancy_snapshot=", 1)[0]
            elif " blocked_by_policy=" in raw_value:
                raw_value = raw_value.split(" blocked_by_policy=", 1)[0]
            rank_score_components_samples.append(_safe_dict_literal(raw_value))

    max_consecutive_losses = 0
    current_consecutive_losses = 0
    for pnl in close_pnls:
        if pnl < 0:
            current_consecutive_losses += 1
            max_consecutive_losses = max(max_consecutive_losses, current_consecutive_losses)
        else:
            current_consecutive_losses = 0

    blocked_signal_stats = dict(blocked_stats)
    if no_ranked_signal_details or no_ranked_signal_legacy_count:
        if no_ranked_signal_details:
            no_ranked_payload = dict(no_ranked_signal_details)
            if no_ranked_signal_legacy_count:
                no_ranked_payload["legacy"] = no_ranked_signal_legacy_count
            blocked_signal_stats["no_ranked_signal"] = no_ranked_payload
        else:
            blocked_signal_stats["no_ranked_signal"] = no_ranked_signal_legacy_count
    if entry_gate_details:
        blocked_signal_stats["entry_gate"] = dict(entry_gate_details)

    return {
        "blocked_signal_stats": blocked_signal_stats,
        "risk_trigger_stats": dict(risk_trigger_stats),
        "selected_strategy_counts": dict(selected_strategy_counts),
        "close_pnls": close_pnls,
        "max_consecutive_losses": max_consecutive_losses,
        "rank_scores": rank_scores,
        "rank_score_components_samples": rank_score_components_samples,
    }


def build_performance_snapshot(metrics_file: Path, portfolio_log_file: Path) -> dict:
    strategy_metrics = _load_strategy_metrics(metrics_file)
    log_stats = _parse_portfolio_log(portfolio_log_file)

    total_signals = 0
    selected_signals = 0
    closed_trades = 0
    wins = 0
    losses = 0
    gross_profit = 0.0
    gross_loss = 0.0
    strategy_breakdown: dict[str, dict] = {}

    for strategy_name, payload in strategy_metrics.items():
        if not isinstance(payload, dict):
            continue
        total_signals += int(payload.get("signals_generated", 0) or 0)
        selected_signals += int(payload.get("signals_selected", 0) or 0)
        closed_trades += int(payload.get("trades_closed", 0) or 0)
        wins += int(payload.get("wins", 0) or 0)
        losses += int(payload.get("losses", 0) or 0)
        gross_profit += _safe_float(payload.get("gross_profit", 0.0))
        gross_loss += _safe_float(payload.get("gross_loss", 0.0))
        strategy_breakdown[strategy_name] = {
            "trades_closed": int(payload.get("trades_closed", 0) or 0),
            "wins": int(payload.get("wins", 0) or 0),
            "losses": int(payload.get("losses", 0) or 0),
            "win_rate": _safe_float(payload.get("win_rate", 0.0)),
            "expectancy": _safe_float(payload.get("expectancy", 0.0)),
            "profit_factor": _safe_float(payload.get("profit_factor", 0.0)),
            "signals_generated": int(payload.get("signals_generated", 0) or 0),
            "signals_selected": int(payload.get("signals_selected", 0) or 0),
        }

    net_pnl = gross_profit - gross_loss
    avg_win = gross_profit / wins if wins > 0 else 0.0
    avg_loss = gross_loss / losses if losses > 0 else 0.0
    win_rate = wins / closed_trades if closed_trades > 0 else 0.0
    expectancy = (win_rate * avg_win) - ((1 - win_rate) * avg_loss) if closed_trades > 0 else 0.0
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0.0

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_signals": total_signals,
        "selected_signals": selected_signals,
        "executed_trades": selected_signals,
        "closed_trades": closed_trades,
        "wins": wins,
        "losses": losses,
        "win_rate": win_rate,
        "expectancy": expectancy,
        "net_pnl": net_pnl,
        "avg_win": avg_win,
        "avg_loss": avg_loss,
        "profit_factor": profit_factor,
        "max_consecutive_losses": int(log_stats["max_consecutive_losses"]),
        "strategy_breakdown": strategy_breakdown,
        "risk_trigger_stats": dict(log_stats["risk_trigger_stats"]),
        "blocked_signal_stats": dict(log_stats["blocked_signal_stats"]),
        "selected_strategy_counts": dict(log_stats["selected_strategy_counts"]),
        "rank_score_samples": list(log_stats["rank_scores"]),
        "rank_score_components_samples": list(log_stats["rank_score_components_samples"]),
    }


def save_performance_snapshot(snapshot_file: Path, snapshot: dict) -> None:
    snapshot_file.parent.mkdir(parents=True, exist_ok=True)
    snapshot_file.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False), encoding="utf-8")


def generate_and_save_performance_snapshot(
    *,
    metrics_file: Path,
    portfolio_log_file: Path,
    snapshot_file: Path,
) -> dict:
    snapshot = build_performance_snapshot(metrics_file, portfolio_log_file)
    save_performance_snapshot(snapshot_file, snapshot)
    return snapshot

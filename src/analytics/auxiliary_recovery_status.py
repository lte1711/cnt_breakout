from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from datetime import datetime
from pathlib import Path


MIN_RECOVERY_SAMPLE = 50
MIN_RECOVERY_PROFIT_FACTOR = 1.1
EXCLUDED_STRATEGY = "breakout_v1"
ACTIVE_RECOVERY_STRATEGY = "pullback_v1"


def _safe_float(value) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _safe_int(value) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _as_dict(value) -> dict:
    if isinstance(value, dict):
        return value
    if is_dataclass(value):
        return asdict(value)
    return {}


def _strategy_net_pnl(payload: dict) -> float:
    return _safe_float(payload.get("gross_profit")) - _safe_float(payload.get("gross_loss"))


def _strategy_payload(strategy_metrics: dict, strategy_name: str) -> dict:
    payload = strategy_metrics.get(strategy_name, {})
    payload = _as_dict(payload)

    return {
        "closed_trades": _safe_int(payload.get("trades_closed")),
        "wins": _safe_int(payload.get("wins")),
        "losses": _safe_int(payload.get("losses")),
        "win_rate": _safe_float(payload.get("win_rate")),
        "expectancy": _safe_float(payload.get("expectancy")),
        "profit_factor": _safe_float(payload.get("profit_factor")),
        "net_pnl": _strategy_net_pnl(payload),
        "signals_generated": _safe_int(payload.get("signals_generated")),
        "signals_selected": _safe_int(payload.get("signals_selected")),
    }


def _aggregate_excluding(strategy_metrics: dict, excluded_strategy: str) -> dict:
    closed_trades = 0
    wins = 0
    losses = 0
    gross_profit = 0.0
    gross_loss = 0.0
    included_strategies: list[str] = []

    for strategy_name, payload in strategy_metrics.items():
        payload = _as_dict(payload)
        if strategy_name == excluded_strategy or not payload:
            continue

        included_strategies.append(strategy_name)
        closed_trades += _safe_int(payload.get("trades_closed"))
        wins += _safe_int(payload.get("wins"))
        losses += _safe_int(payload.get("losses"))
        gross_profit += _safe_float(payload.get("gross_profit"))
        gross_loss += _safe_float(payload.get("gross_loss"))

    win_rate = wins / closed_trades if closed_trades > 0 else 0.0
    avg_win = gross_profit / wins if wins > 0 else 0.0
    avg_loss = gross_loss / losses if losses > 0 else 0.0
    expectancy = (win_rate * avg_win) - ((1 - win_rate) * avg_loss) if closed_trades > 0 else 0.0
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0.0

    return {
        "excluded_strategy": excluded_strategy,
        "included_strategies": included_strategies,
        "closed_trades": closed_trades,
        "wins": wins,
        "losses": losses,
        "win_rate": win_rate,
        "expectancy": expectancy,
        "profit_factor": profit_factor,
        "net_pnl": gross_profit - gross_loss,
    }


def _risk_counter_sync(state: dict, portfolio_state: dict) -> dict:
    state_risk = state.get("risk_metrics", {}) if isinstance(state, dict) else {}
    if not isinstance(state_risk, dict):
        state_risk = {}

    state_daily = _safe_int(state_risk.get("daily_loss_count"))
    portfolio_daily = _safe_int(portfolio_state.get("daily_loss_count")) if isinstance(portfolio_state, dict) else 0
    state_consecutive = _safe_int(state_risk.get("consecutive_losses"))
    portfolio_consecutive = (
        _safe_int(portfolio_state.get("consecutive_losses")) if isinstance(portfolio_state, dict) else 0
    )

    return {
        "daily_loss_count_synced": state_daily == portfolio_daily,
        "consecutive_losses_synced": state_consecutive == portfolio_consecutive,
        "state_daily_loss_count": state_daily,
        "portfolio_daily_loss_count": portfolio_daily,
        "state_consecutive_losses": state_consecutive,
        "portfolio_consecutive_losses": portfolio_consecutive,
    }


def build_auxiliary_recovery_status(
    *,
    snapshot: dict,
    strategy_metrics: dict,
    state: dict,
    portfolio_state: dict,
    live_gate_decision: dict,
    min_sample_required: int = MIN_RECOVERY_SAMPLE,
    min_profit_factor: float = MIN_RECOVERY_PROFIT_FACTOR,
) -> dict:
    state = _as_dict(state)
    portfolio_state = _as_dict(portfolio_state)
    pullback = _strategy_payload(strategy_metrics, ACTIVE_RECOVERY_STRATEGY)
    excluding_breakout = _aggregate_excluding(strategy_metrics, EXCLUDED_STRATEGY)
    official_status = live_gate_decision.get("status") if isinstance(live_gate_decision, dict) else None
    official_reason = live_gate_decision.get("reason") if isinstance(live_gate_decision, dict) else None

    is_positive_expectancy = pullback["expectancy"] > 0
    is_positive_net_pnl = pullback["net_pnl"] > 0
    profit_factor_pass = pullback["profit_factor"] > min_profit_factor
    is_statistically_valid = pullback["closed_trades"] >= min_sample_required
    all_recovery_criteria_passed = (
        is_positive_expectancy
        and is_positive_net_pnl
        and profit_factor_pass
        and is_statistically_valid
    )

    if all_recovery_criteria_passed:
        auxiliary_status = "RECOVERY_EVIDENCE_READY"
    elif is_positive_expectancy and is_positive_net_pnl and profit_factor_pass:
        auxiliary_status = "RECOVERY_OBSERVATION_IN_PROGRESS"
    else:
        auxiliary_status = "RECOVERY_NOT_CONFIRMED"

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "official_gate": {
            "status": official_status,
            "reason": official_reason,
            "expectancy": _safe_float(snapshot.get("expectancy")),
            "net_pnl": _safe_float(snapshot.get("net_pnl")),
            "closed_trades": _safe_int(snapshot.get("closed_trades")),
        },
        ACTIVE_RECOVERY_STRATEGY: pullback,
        "system_excluding_breakout_v1": excluding_breakout,
        "recovery_signal": {
            "status": auxiliary_status,
            "is_positive_expectancy": is_positive_expectancy,
            "is_positive_net_pnl": is_positive_net_pnl,
            "profit_factor_pass": profit_factor_pass,
            "is_statistically_valid": is_statistically_valid,
            "all_recovery_criteria_passed": all_recovery_criteria_passed,
            "min_sample_required": min_sample_required,
            "min_profit_factor": min_profit_factor,
        },
        "runtime_state": {
            "active_strategy": state.get("strategy_name") if isinstance(state, dict) else None,
            "last_run_time": state.get("last_run_time") if isinstance(state, dict) else None,
            "last_action": state.get("action") if isinstance(state, dict) else None,
            "pending_order_exists": bool(state.get("pending_order")) if isinstance(state, dict) else False,
            "open_trade_exists": bool(state.get("open_trade")) if isinstance(state, dict) else False,
            "open_positions_count": len(portfolio_state.get("open_positions", []))
            if isinstance(portfolio_state.get("open_positions") if isinstance(portfolio_state, dict) else None, list)
            else 0,
            "total_exposure": _safe_float(portfolio_state.get("total_exposure"))
            if isinstance(portfolio_state, dict)
            else 0.0,
        },
        "risk_counter_sync": _risk_counter_sync(state, portfolio_state),
        "interpretation": (
            "official_gate_remains_authoritative_auxiliary_status_is_observational_only"
        ),
    }


def save_auxiliary_recovery_status(status_file: Path, status: dict) -> None:
    status_file.parent.mkdir(parents=True, exist_ok=True)
    status_file.write_text(json.dumps(status, indent=2, ensure_ascii=False), encoding="utf-8")

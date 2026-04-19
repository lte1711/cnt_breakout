from __future__ import annotations

from datetime import datetime, timedelta

from config import LOSS_COOLDOWN_MINUTES, MAX_CONSECUTIVE_LOSSES, MAX_DAILY_LOSS_COUNT
from src.models.risk_result import RiskCheckResult
from src.models.strategy_signal import StrategySignal


def _default_risk_metrics() -> dict:
    return {
        "daily_loss_count": 0,
        "consecutive_losses": 0,
        "last_loss_time": None,
    }


def _normalize_risk_metrics(state: dict | None) -> dict:
    if not isinstance(state, dict):
        return _default_risk_metrics()

    risk_metrics = state.get("risk_metrics")
    if not isinstance(risk_metrics, dict):
        return _default_risk_metrics()

    return {
        "daily_loss_count": int(risk_metrics.get("daily_loss_count", 0) or 0),
        "consecutive_losses": int(risk_metrics.get("consecutive_losses", 0) or 0),
        "last_loss_time": risk_metrics.get("last_loss_time"),
    }


def evaluate_risk(signal: StrategySignal, state: dict | None, balance: dict | None) -> RiskCheckResult:
    del balance

    if not signal.entry_allowed:
        return RiskCheckResult(passed=False, reason="signal_not_entry_allowed")

    risk_metrics = _normalize_risk_metrics(state)

    if risk_metrics["daily_loss_count"] >= MAX_DAILY_LOSS_COUNT:
        return RiskCheckResult(passed=False, reason="DAILY_LOSS_LIMIT")

    if risk_metrics["consecutive_losses"] >= MAX_CONSECUTIVE_LOSSES:
        last_loss_time = risk_metrics.get("last_loss_time")
        if isinstance(last_loss_time, str):
            try:
                loss_time = datetime.strptime(last_loss_time, "%Y-%m-%d %H:%M:%S")
                if datetime.now() < loss_time + timedelta(minutes=LOSS_COOLDOWN_MINUTES):
                    return RiskCheckResult(passed=False, reason="LOSS_COOLDOWN")
            except ValueError:
                return RiskCheckResult(passed=False, reason="INVALID_LAST_LOSS_TIME")

    return RiskCheckResult(passed=True, reason="ok")

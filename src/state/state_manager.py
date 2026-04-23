from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from config import PORTFOLIO_STATE_SCHEMA_VERSION
from src.models.portfolio_state import PortfolioState
from src.models.position_state import PositionState


def _extract_runtime_risk_counts(runtime_state: dict) -> tuple[int, int]:
    risk_metrics = runtime_state.get("risk_metrics")
    if not isinstance(risk_metrics, dict):
        return 0, 0

    return (
        int(risk_metrics.get("daily_loss_count", 0) or 0),
        int(risk_metrics.get("consecutive_losses", 0) or 0),
    )


def load_portfolio_state(state_file: Path) -> PortfolioState:
    if not state_file.exists():
        return PortfolioState(schema_version=PORTFOLIO_STATE_SCHEMA_VERSION, total_exposure=0.0)

    loaded = json.loads(state_file.read_text(encoding="utf-8"))
    positions = [
        PositionState(**item)
        for item in loaded.get("open_positions", [])
        if isinstance(item, dict)
    ]
    return PortfolioState(
        schema_version=str(loaded.get("schema_version", PORTFOLIO_STATE_SCHEMA_VERSION)),
        total_exposure=float(loaded.get("total_exposure", 0.0) or 0.0),
        open_positions=positions,
        cash_balance=float(loaded.get("cash_balance", 0.0) or 0.0),
        daily_loss_count=int(loaded.get("daily_loss_count", 0) or 0),
        consecutive_losses=int(loaded.get("consecutive_losses", 0) or 0),
        last_update_time=loaded.get("last_update_time"),
        source=str(loaded.get("source", "rebuild_from_runtime") or "rebuild_from_runtime"),
    )


def save_portfolio_state(state_file: Path, portfolio_state: PortfolioState) -> None:
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text(json.dumps(asdict(portfolio_state), indent=2, ensure_ascii=False), encoding="utf-8")


def build_portfolio_state(runtime_state: dict, cash_balance: float = 0.0) -> PortfolioState:
    last_update_time = str(runtime_state.get("last_run_time") or datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    daily_loss_count, consecutive_losses = _extract_runtime_risk_counts(runtime_state)
    open_trade = runtime_state.get("open_trade")
    if not isinstance(open_trade, dict):
        return PortfolioState(
            schema_version=PORTFOLIO_STATE_SCHEMA_VERSION,
            total_exposure=0.0,
            open_positions=[],
            cash_balance=cash_balance,
            daily_loss_count=daily_loss_count,
            consecutive_losses=consecutive_losses,
            last_update_time=last_update_time,
            source="rebuild_from_runtime",
        )

    position = PositionState(
        position_id=f"spot:{runtime_state.get('symbol', 'UNKNOWN')}:{open_trade.get('entry_order_id', '0')}",
        symbol=str(runtime_state.get("symbol", "UNKNOWN")),
        market_type="spot",
        strategy_name=str(open_trade.get("strategy_name", "unknown")),
        entry_price=float(open_trade.get("entry_price", 0.0) or 0.0),
        entry_qty=float(open_trade.get("entry_qty", 0.0) or 0.0),
        entry_time=str(open_trade.get("entry_time", runtime_state.get("last_run_time", ""))),
        stop_price=(float(open_trade["stop_price"]) if open_trade.get("stop_price") is not None else None),
        target_price=(float(open_trade["target_price"]) if open_trade.get("target_price") is not None else None),
        status=str(open_trade.get("status", "OPEN")),
    )
    return PortfolioState(
        schema_version=PORTFOLIO_STATE_SCHEMA_VERSION,
        total_exposure=position.entry_price * position.entry_qty,
        open_positions=[position],
        cash_balance=cash_balance,
        daily_loss_count=daily_loss_count,
        consecutive_losses=consecutive_losses,
        last_update_time=last_update_time,
        source="rebuild_from_runtime",
    )

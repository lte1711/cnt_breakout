from __future__ import annotations

from config import MAX_PORTFOLIO_EXPOSURE, ONE_PER_SYMBOL_POLICY
from src.models.portfolio_state import PortfolioState
from src.models.strategy_signal import StrategySignal


def check_portfolio_risk(
    signal: StrategySignal,
    portfolio_state: PortfolioState,
    requested_notional: float,
) -> tuple[bool, str | None]:
    requested_exposure = float(requested_notional or 0.0)

    if portfolio_state.total_exposure + requested_exposure > MAX_PORTFOLIO_EXPOSURE:
        return False, "MAX_PORTFOLIO_EXPOSURE_EXCEEDED"

    if ONE_PER_SYMBOL_POLICY:
        for position in portfolio_state.open_positions:
            if position.symbol == signal.symbol and position.status.upper() == "OPEN":
                return False, "ONE_PER_SYMBOL_POLICY"

    return True, None

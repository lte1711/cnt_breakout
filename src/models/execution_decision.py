from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ExecutionDecision:
    execute: bool
    action: str
    reason: str
    signal_reason: str
    strategy_name: str
    symbol: str
    validated_qty: float | None
    validated_price: float | None
    notional_value: float | None
    risk_check_passed: bool
    risk_rejection_reason: str | None
    portfolio_rejection_reason: str | None = None
    selected_priority: int | None = None
    slippage_check_passed: bool = True
    slippage_rejection_reason: str | None = None

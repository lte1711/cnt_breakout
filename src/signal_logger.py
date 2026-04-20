from __future__ import annotations

from datetime import datetime
from pathlib import Path

from src.models.strategy_signal import StrategySignal


def append_signal_log(log_file: Path, signal: StrategySignal) -> None:
    log_file.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    trend_bias_text = signal.trend_bias if signal.trend_bias is not None else "UNKNOWN"
    message = (
        f"[{timestamp}] strategy={signal.strategy_name} symbol={signal.symbol} "
        f"entry_allowed={signal.entry_allowed} side={signal.side} trigger={signal.trigger} "
        f"reason={signal.reason} confidence={signal.confidence} "
        f"market_state={signal.market_state} trend_bias={trend_bias_text} "
        f"volatility_state={signal.volatility_state}"
    )

    with log_file.open("a", encoding="utf-8") as file_handle:
        file_handle.write(message + "\n")

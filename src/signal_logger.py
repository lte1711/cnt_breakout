from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from src.models.strategy_signal import StrategySignal


def append_signal_log(log_file: Path, signal: StrategySignal) -> None:
    log_file.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    trend_bias_text = signal.trend_bias if signal.trend_bias is not None else "UNKNOWN"
    decision_id_text = signal.decision_id if signal.decision_id is not None else "UNKNOWN"
    market_features_text = json.dumps(signal.market_features, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    message = (
        f"[{timestamp}] strategy={signal.strategy_name} symbol={signal.symbol} "
        f"decision_id={decision_id_text} "
        f"entry_allowed={signal.entry_allowed} side={signal.side} trigger={signal.trigger} "
        f"reason={signal.reason} confidence={signal.confidence} "
        f"market_state={signal.market_state} trend_bias={trend_bias_text} "
        f"volatility_state={signal.volatility_state} "
        f"market_features={market_features_text}"
    )

    with log_file.open("a", encoding="utf-8") as file_handle:
        file_handle.write(message + "\n")

from __future__ import annotations

import json
from pathlib import Path


def write_state(state_file: Path, state_data: dict) -> None:
    state_file.parent.mkdir(parents=True, exist_ok=True)
    normalized_state = dict(state_data)
    normalized_state.setdefault("schema_version", "1.0")
    normalized_state.setdefault("strategy_name", "breakout_v1")
    normalized_state.setdefault(
        "risk_metrics",
        {
            "daily_loss_count": 0,
            "consecutive_losses": 0,
            "last_loss_time": None,
        },
    )

    with state_file.open("w", encoding="utf-8") as f:
        json.dump(normalized_state, f, indent=2, ensure_ascii=False)

from __future__ import annotations

from pathlib import Path


def append_log(log_file: Path, message: str) -> None:
    log_file.parent.mkdir(parents=True, exist_ok=True)
    normalized = message
    lowered = message.lower()

    if (
        "action=error" in lowered
        or "reason=strategy_error" in lowered
        or "invalid_entry_order_id" in lowered
        or "invalid_open_trade" in lowered
        or "stale_open_trade" in lowered
        or "stale_pending_order" in lowered
    ):
        normalized = f"[ALERT] {message}"

    with log_file.open("a", encoding="utf-8") as f:
        f.write(normalized + "\n")

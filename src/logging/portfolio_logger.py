from __future__ import annotations

from datetime import datetime
from pathlib import Path


def append_portfolio_log(log_file: Path, message: str) -> None:
    log_file.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with log_file.open("a", encoding="utf-8") as file_handle:
        file_handle.write(f"[{timestamp}] {message}\n")

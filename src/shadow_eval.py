from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from binance_client import get_price
from config import ENTRY_INTERVAL, KLINES_LIMIT, PRIMARY_INTERVAL
from src.indicators import (
    bollinger_bands,
    extract_closes,
    extract_volumes,
    rolling_vwap,
)
from src.market_data import get_recent_closed_klines
from src.models.market_context import MarketContext
from src.strategies.breakout_v2 import BreakoutV2Strategy


def _build_shadow_context(symbol: str) -> MarketContext:
    klines_primary = get_recent_closed_klines(
        symbol=symbol,
        interval=PRIMARY_INTERVAL,
        limit=KLINES_LIMIT,
    )
    klines_entry = get_recent_closed_klines(
        symbol=symbol,
        interval=ENTRY_INTERVAL,
        limit=KLINES_LIMIT,
    )
    last_price = get_price(symbol)
    return MarketContext(
        symbol=symbol,
        primary_interval=PRIMARY_INTERVAL,
        entry_interval=ENTRY_INTERVAL,
        klines_primary=klines_primary,
        klines_entry=klines_entry,
        last_price=last_price,
    )


def _safe_ratio(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return 0.0
    return numerator / denominator


def evaluate_breakout_v2_shadow(symbol: str, params: dict) -> dict:
    context = _build_shadow_context(symbol)
    strategy = BreakoutV2Strategy(dict(params))
    strategy.validate_params(params)
    signal = strategy.evaluate(context)

    closes = extract_closes(context.klines_entry)
    volumes = extract_volumes(context.klines_entry)
    upper_band, _, lower_band = bollinger_bands(
        closes,
        params["bollinger_period"],
        params["bollinger_std_multiplier"],
    )
    vwap_series = rolling_vwap(context.klines_entry, params["vwap_period"])

    current_close = closes[-1]
    current_volume = volumes[-1]
    vwap_value = vwap_series[-1]
    current_upper = upper_band[-1]
    current_lower = lower_band[-1]
    previous_upper = upper_band[-2] if len(upper_band) >= 2 else None
    previous_lower = lower_band[-2] if len(lower_band) >= 2 else None
    previous_close = closes[-2] if len(closes) >= 2 else None

    band_width_ratio = None
    band_expansion_ratio = None
    volume_ratio = None

    if current_upper is not None and current_lower is not None and current_close > 0:
        band_width_ratio = (current_upper - current_lower) / current_close

    if (
        previous_upper is not None
        and previous_lower is not None
        and previous_close is not None
        and previous_close > 0
        and band_width_ratio is not None
    ):
        previous_band_width_ratio = (previous_upper - previous_lower) / previous_close
        if previous_band_width_ratio > 0:
            band_expansion_ratio = band_width_ratio / previous_band_width_ratio

    volume_period = int(params["volume_avg_period"])
    if len(volumes) >= volume_period:
        recent_volumes = volumes[-volume_period:]
        average_volume = sum(recent_volumes) / len(recent_volumes)
        if average_volume > 0:
            volume_ratio = current_volume / average_volume

    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
    return {
        "ts": timestamp,
        "symbol": symbol,
        "strategy": "breakout_v2_shadow",
        "signal_generated": True,
        "entry_allowed": bool(signal.entry_allowed),
        "filter_reason": signal.reason,
        "confidence": float(signal.confidence),
        "vwap": vwap_value,
        "band_width_ratio": band_width_ratio,
        "band_expansion_ratio": band_expansion_ratio,
        "volume_ratio": volume_ratio,
        "hypothetical_entry": bool(signal.entry_allowed),
    }


def append_shadow_log(log_file: Path, event: dict) -> None:
    try:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        with log_file.open("a", encoding="utf-8", newline="\n") as file_handle:
            file_handle.write(json.dumps(event, ensure_ascii=False) + "\n")
    except Exception:
        pass


def update_shadow_snapshot(snapshot_file: Path, event: dict) -> None:
    try:
        snapshot_file.parent.mkdir(parents=True, exist_ok=True)
        if snapshot_file.exists():
            loaded = json.loads(snapshot_file.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                snapshot = loaded
            else:
                snapshot = {}
        else:
            snapshot = {}

        signal_count = int(snapshot.get("signal_count", 0) or 0) + 1
        filtered_signal_count = int(snapshot.get("filtered_signal_count", 0) or 0)
        allowed_signal_count = int(snapshot.get("allowed_signal_count", 0) or 0)
        hypothetical_trades_count = int(snapshot.get("hypothetical_trades_count", 0) or 0)

        if event.get("entry_allowed"):
            allowed_signal_count += 1
            hypothetical_trades_count += 1
        else:
            filtered_signal_count += 1

        reason_distribution = snapshot.get("reason_distribution", {}) or {}
        reason_key = str(event.get("filter_reason") or "UNKNOWN")
        reason_distribution[reason_key] = int(reason_distribution.get(reason_key, 0) or 0) + 1

        updated = {
            "strategy": "breakout_v2_shadow",
            "signal_count": signal_count,
            "filtered_signal_count": filtered_signal_count,
            "allowed_signal_count": allowed_signal_count,
            "filtered_signal_ratio": _safe_ratio(filtered_signal_count, signal_count),
            "allowed_signal_ratio": _safe_ratio(allowed_signal_count, signal_count),
            "hypothetical_trades_count": hypothetical_trades_count,
            "hypothetical_expectancy": float(snapshot.get("hypothetical_expectancy", 0.0) or 0.0),
            "hypothetical_profit_factor": float(snapshot.get("hypothetical_profit_factor", 0.0) or 0.0),
            "stop_exit_ratio": float(snapshot.get("stop_exit_ratio", 0.0) or 0.0),
            "reason_distribution": reason_distribution,
            "last_updated": event.get("ts"),
        }
        snapshot_file.write_text(
            json.dumps(updated, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    except Exception:
        pass

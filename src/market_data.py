from __future__ import annotations

import requests

from binance_client import get_server_time
from config import BINANCE_BASE_URL, REQUEST_TIMEOUT


def fetch_klines(symbol: str, interval: str, limit: int = 200) -> list[dict]:
    if not symbol:
        raise ValueError("symbol is required")

    if not interval:
        raise ValueError("interval is required")

    if limit <= 0:
        raise ValueError("limit must be greater than 0")

    if limit > 1000:
        raise ValueError("limit must be less than or equal to 1000")

    url = f"{BINANCE_BASE_URL}/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit,
    }

    response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()

    raw_klines = response.json()

    if not isinstance(raw_klines, list):
        raise ValueError("invalid klines response")

    result: list[dict] = []

    for item in raw_klines:
        if not isinstance(item, list) or len(item) < 11:
            raise ValueError("invalid kline item")

        result.append(
            {
                "open_time": int(item[0]),
                "open": float(item[1]),
                "high": float(item[2]),
                "low": float(item[3]),
                "close": float(item[4]),
                "volume": float(item[5]),
                "close_time": int(item[6]),
                "quote_asset_volume": float(item[7]),
                "number_of_trades": int(item[8]),
                "taker_buy_base_asset_volume": float(item[9]),
                "taker_buy_quote_asset_volume": float(item[10]),
            }
        )

    return result


def get_latest_closed_kline(symbol: str, interval: str) -> dict:
    klines = fetch_klines(symbol=symbol, interval=interval, limit=2)

    if len(klines) < 2:
        raise ValueError("not enough klines to determine latest closed kline")

    return klines[-2]


def get_recent_closed_klines(symbol: str, interval: str, limit: int = 200) -> list[dict]:
    klines = fetch_klines(symbol=symbol, interval=interval, limit=limit + 1)

    if len(klines) <= 1:
        raise ValueError("not enough klines to determine recent closed klines")

    return klines[:-1]


def get_exchange_time_ms() -> int:
    return get_server_time()
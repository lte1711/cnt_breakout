import hashlib
import hmac
import json
import time
from urllib.parse import urlencode

import requests

from config import (
    BINANCE_API_KEY,
    BINANCE_API_SECRET,
    BINANCE_BASE_URL,
    RECV_WINDOW,
    REQUEST_TIMEOUT,
)


def _raise_binance_error(response: requests.Response) -> None:
    try:
        data = response.json()
    except Exception:
        data = None

    if isinstance(data, dict):
        code = data.get("code")
        msg = data.get("msg")

        if code is not None or msg is not None:
            raise requests.HTTPError(
                f"{response.status_code} Binance Error: code={code}, msg={msg}",
                response=response,
            )

    response.raise_for_status()


def ping() -> None:
    url = f"{BINANCE_BASE_URL}/api/v3/ping"

    response = requests.get(url, timeout=REQUEST_TIMEOUT)
    if not response.ok:
        _raise_binance_error(response)


def get_price(symbol: str) -> float:
    url = f"{BINANCE_BASE_URL}/api/v3/ticker/price"
    params = {"symbol": symbol}

    response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
    if not response.ok:
        _raise_binance_error(response)

    data = response.json()
    return float(data["price"])


def get_server_time() -> int:
    url = f"{BINANCE_BASE_URL}/api/v3/time"

    response = requests.get(url, timeout=REQUEST_TIMEOUT)
    if not response.ok:
        _raise_binance_error(response)

    data = response.json()
    return int(data["serverTime"])


def get_symbol_info(symbol: str) -> dict:
    url = f"{BINANCE_BASE_URL}/api/v3/exchangeInfo"
    params = {"symbol": symbol}

    response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
    if not response.ok:
        _raise_binance_error(response)

    data = response.json()
    symbols = data.get("symbols", [])

    if not symbols:
        raise ValueError(f"symbol info not found: {symbol}")

    return symbols[0]


def extract_symbol_filters(symbol_info: dict) -> dict:
    filters = symbol_info.get("filters", [])

    price_filter = {}
    lot_size_filter = {}
    notional_filter = {}

    for item in filters:
        filter_type = item.get("filterType")

        if filter_type == "PRICE_FILTER":
            price_filter = {
                "min_price": item.get("minPrice"),
                "max_price": item.get("maxPrice"),
                "tick_size": item.get("tickSize"),
            }

        elif filter_type == "LOT_SIZE":
            lot_size_filter = {
                "min_qty": item.get("minQty"),
                "max_qty": item.get("maxQty"),
                "step_size": item.get("stepSize"),
            }

        elif filter_type == "MIN_NOTIONAL":
            notional_filter = {
                "filter_type": "MIN_NOTIONAL",
                "min_notional": item.get("minNotional"),
                "apply_to_market": item.get("applyToMarket"),
                "avg_price_mins": item.get("avgPriceMins"),
            }

        elif filter_type == "NOTIONAL":
            notional_filter = {
                "filter_type": "NOTIONAL",
                "min_notional": item.get("minNotional"),
                "max_notional": item.get("maxNotional"),
                "apply_min_to_market": item.get("applyMinToMarket"),
                "apply_max_to_market": item.get("applyMaxToMarket"),
                "avg_price_mins": item.get("avgPriceMins"),
            }

    return {
        "price_filter": price_filter,
        "lot_size_filter": lot_size_filter,
        "notional_filter": notional_filter,
    }


def has_api_credentials() -> bool:
    return bool(BINANCE_API_KEY and BINANCE_API_SECRET)


def build_signed_params(params: dict) -> dict:
    if not has_api_credentials():
        raise ValueError("missing BINANCE_API_KEY or BINANCE_API_SECRET")

    signed_params = dict(params)
    signed_params["timestamp"] = get_server_time()
    signed_params["recvWindow"] = RECV_WINDOW

    query_string = urlencode(signed_params, doseq=True)
    signature = hmac.new(
        BINANCE_API_SECRET.encode("utf-8"),
        query_string.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    signed_params["signature"] = signature
    return signed_params


def get_signed_headers() -> dict:
    if not BINANCE_API_KEY:
        raise ValueError("missing BINANCE_API_KEY")

    return {
        "X-MBX-APIKEY": BINANCE_API_KEY,
    }


def post_signed(endpoint: str, params: dict) -> dict:
    signed_params = build_signed_params(params)
    headers = get_signed_headers()

    url = f"{BINANCE_BASE_URL}{endpoint}"

    response = requests.post(
        url,
        headers=headers,
        data=signed_params,
        timeout=REQUEST_TIMEOUT,
    )

    if not response.ok:
        _raise_binance_error(response)

    if response.text:
        return response.json()

    return {}


def get_signed(endpoint: str, params: dict) -> dict | list:
    signed_params = build_signed_params(params)
    headers = get_signed_headers()

    url = f"{BINANCE_BASE_URL}{endpoint}"

    response = requests.get(
        url,
        headers=headers,
        params=signed_params,
        timeout=REQUEST_TIMEOUT,
    )

    if not response.ok:
        _raise_binance_error(response)

    return response.json()
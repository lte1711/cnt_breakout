from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from src.account_reader import get_account_info
from src.balance_reader import extract_asset_balance
from binance_client import (
    extract_symbol_filters,
    get_price,
    get_server_time,
    get_symbol_info,
    has_api_credentials,
    ping,
)
from config import (
    BINANCE_BASE_URL,
    ENABLE_TEST_ORDER_VALIDATION,
    LOG_FILE,
    STATE_FILE,
    SYMBOL,
)
from src.log_writer import append_log
from src.order_executor import send_live_testnet_order, send_test_order
from src.order_payload_builder import build_limit_order_payload
from src.order_query import get_open_orders, get_order
from src.order_validator import auto_adjust_order_inputs, validate_order
from src.state_writer import write_state
from src.target_exit import calculate_target_price, should_exit_long


TARGET_PCT = 0.002
STOP_LOSS_PCT = 0.0015


def calculate_stop_price(entry_price: float, stop_pct: float) -> float:
    return entry_price * (1 - stop_pct)


def should_stop(price: float, stop_price: float) -> bool:
    return price <= stop_price


def _load_state(path: Path) -> dict:
    if not path.exists():
        return {}

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _save_and_finish(
    *,
    state_file: Path,
    log_file: Path,
    state: dict,
    timestamp: str,
    action: str,
    price: float,
    pending: dict | None,
    open_trade: dict | None,
) -> None:
    state["last_run_time"] = timestamp
    state["status"] = "stopped"
    state["symbol"] = SYMBOL
    state["pending_order"] = pending
    state["open_trade"] = open_trade
    state["action"] = action
    state["price"] = price

    write_state(state_file, state)

    append_log(
        log_file,
        f"[{timestamp}] action={action} price={price} pending={pending} open_trade={open_trade}",
    )


def _find_open_order_by_id(open_orders: list, order_id: int) -> dict | None:
    for item in open_orders:
        if int(item.get("orderId", 0)) == int(order_id):
            return item
    return None


def _reconcile_pending_order(
    *,
    symbol: str,
    pending: dict,
) -> tuple[str, dict | None, dict | None]:
    order_id = int(pending["orderId"])

    try:
        order_info = get_order(symbol, order_id, BINANCE_BASE_URL)
        status = str(order_info.get("status", "")).upper()

        if status == "FILLED":
            if pending.get("side") == "BUY":
                open_trade = {
                    "status": "OPEN",
                    "entry_price": float(order_info["price"]),
                    "entry_qty": float(order_info["executedQty"]),
                    "entry_order_id": int(order_info["orderId"]),
                    "entry_side": "BUY",
                }
                return "PROMOTE_TO_OPEN_TRADE", None, open_trade

            return "SELL_FILLED", None, None

        if status in {"NEW", "PARTIALLY_FILLED", "PENDING_NEW"}:
            return "PENDING_CONFIRMED", pending, None

        return "PENDING_CLEARED", None, None

    except Exception:
        return "PENDING_RECONCILE_ERROR_KEEP", pending, None


def _validate_limit_order_before_live(payload: dict) -> None:
    if not ENABLE_TEST_ORDER_VALIDATION:
        return

    send_test_order(payload)


def start_engine() -> None:
    project_root = Path(__file__).resolve().parent.parent
    log_file = project_root / LOG_FILE
    state_file = project_root / STATE_FILE

    print("engine step19e started")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        state = _load_state(state_file)

        ping()
        get_server_time()
        symbol_info = get_symbol_info(SYMBOL)
        filters = extract_symbol_filters(symbol_info)
        price = get_price(SYMBOL)

        if not has_api_credentials():
            return

        pending = state.get("pending_order")
        open_trade = state.get("open_trade")

        if pending:
            action, pending_after, open_trade_after = _reconcile_pending_order(
                symbol=SYMBOL,
                pending=pending,
            )

            if action == "PROMOTE_TO_OPEN_TRADE":
                _save_and_finish(
                    state_file=state_file,
                    log_file=log_file,
                    state=state,
                    timestamp=timestamp,
                    action=action,
                    price=price,
                    pending=None,
                    open_trade=open_trade_after,
                )
                return

            _save_and_finish(
                state_file=state_file,
                log_file=log_file,
                state=state,
                timestamp=timestamp,
                action=action,
                price=price,
                pending=pending_after,
                open_trade=open_trade,
            )
            return

        if open_trade:
            entry_price = float(open_trade["entry_price"])
            entry_qty = float(open_trade["entry_qty"])

            target_price = calculate_target_price(entry_price, TARGET_PCT)
            stop_price = calculate_stop_price(entry_price, STOP_LOSS_PCT)

            if should_exit_long(price, target_price):
                payload = build_limit_order_payload(
                    symbol=SYMBOL,
                    side="SELL",
                    price=price,
                    quantity=entry_qty,
                )

                _validate_limit_order_before_live(payload)
                order_response = send_live_testnet_order(payload)

                pending = {
                    "orderId": order_response["orderId"],
                    "status": order_response["status"],
                    "side": "SELL",
                }

                _save_and_finish(
                    state_file=state_file,
                    log_file=log_file,
                    state=state,
                    timestamp=timestamp,
                    action="SELL_SUBMITTED",
                    price=price,
                    pending=pending,
                    open_trade=open_trade,
                )
                return

            if should_stop(price, stop_price):
                payload = {
                    "symbol": SYMBOL,
                    "side": "SELL",
                    "type": "MARKET",
                    "quantity": str(entry_qty),
                }

                order_response = send_live_testnet_order(payload)

                _save_and_finish(
                    state_file=state_file,
                    log_file=log_file,
                    state=state,
                    timestamp=timestamp,
                    action="STOP_MARKET_FILLED",
                    price=price,
                    pending=None,
                    open_trade=None,
                )
                return

            _save_and_finish(
                state_file=state_file,
                log_file=log_file,
                state=state,
                timestamp=timestamp,
                action="HOLD_OPEN_TRADE",
                price=price,
                pending=None,
                open_trade=open_trade,
            )
            return

        validation = validate_order(price, 0.001, filters)
        adj = auto_adjust_order_inputs(price, 0.001, filters)

        payload = build_limit_order_payload(
            symbol=SYMBOL,
            side="BUY",
            price=adj["adjusted_price"],
            quantity=adj["adjusted_qty"],
        )

        _validate_limit_order_before_live(payload)
        order_response = send_live_testnet_order(payload)

        if str(order_response.get("status")).upper() == "FILLED":
            open_trade = {
                "status": "OPEN",
                "entry_price": float(order_response["price"]),
                "entry_qty": float(order_response["executedQty"]),
                "entry_order_id": int(order_response["orderId"]),
                "entry_side": "BUY",
            }
            pending = None
            action = "BUY_FILLED"
        else:
            pending = {
                "orderId": order_response["orderId"],
                "status": order_response["status"],
                "side": "BUY",
            }
            action = "BUY_SUBMITTED"

        _save_and_finish(
            state_file=state_file,
            log_file=log_file,
            state=state,
            timestamp=timestamp,
            action=action,
            price=price,
            pending=pending,
            open_trade=open_trade,
        )

    except Exception as e:
        print(f"ERROR: {e}")
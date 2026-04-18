from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from requests import HTTPError

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
from src.order_validator import (
    auto_adjust_order_inputs,
    validate_order,
    validate_quantity,
)
from src.state_writer import write_state
from src.target_exit import calculate_target_price, should_exit_long


TARGET_PCT = 0.002
STOP_LOSS_PCT = 0.0015
STATE_TOP_LEVEL_KEYS = (
    "last_run_time",
    "status",
    "symbol",
    "pending_order",
    "open_trade",
    "action",
    "price",
)


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


def _normalize_pending_order(pending: dict | None) -> dict | None:
    if not isinstance(pending, dict):
        return None

    if "orderId" not in pending or "status" not in pending or "side" not in pending:
        return None

    return {
        "orderId": int(pending["orderId"]),
        "status": str(pending["status"]),
        "side": str(pending["side"]).upper(),
    }


def _normalize_open_trade(open_trade: dict | None) -> dict | None:
    if not isinstance(open_trade, dict):
        return None

    required_keys = {"status", "entry_price", "entry_qty", "entry_order_id", "entry_side"}
    if not required_keys.issubset(open_trade):
        return None

    return {
        "status": str(open_trade["status"]),
        "entry_price": float(open_trade["entry_price"]),
        "entry_qty": float(open_trade["entry_qty"]),
        "entry_order_id": int(open_trade["entry_order_id"]),
        "entry_side": str(open_trade["entry_side"]).upper(),
    }


def _build_state(
    *,
    timestamp: str,
    action: str,
    price: float,
    pending: dict | None,
    open_trade: dict | None,
) -> dict:
    return {
        "last_run_time": timestamp,
        "status": "stopped",
        "symbol": SYMBOL,
        "pending_order": _normalize_pending_order(pending),
        "open_trade": _normalize_open_trade(open_trade),
        "action": action,
        "price": price,
    }


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
    reason: str = "ok",
) -> None:
    next_state = _build_state(
        timestamp=timestamp,
        action=action,
        price=price,
        pending=pending,
        open_trade=open_trade,
    )
    state.clear()
    state.update(next_state)

    write_state(state_file, next_state)

    append_log(
        log_file,
        f"[{timestamp}] action={action} price={price} pending={pending} open_trade={open_trade} reason={reason}",
    )


def _find_open_order_by_id(open_orders: list, order_id: int) -> dict | None:
    for item in open_orders:
        if int(item.get("orderId", 0)) == int(order_id):
            return item
    return None


def _is_missing_order_error(error: Exception) -> bool:
    message = str(error).lower()
    return "code=-2013" in message or "order does not exist" in message


def _extract_fill_price(order_info: dict) -> float:
    order_price = float(order_info.get("price", 0) or 0)
    if order_price > 0:
        return order_price

    executed_qty = float(order_info.get("executedQty", 0) or 0)
    cumulative_quote_qty = float(order_info.get("cummulativeQuoteQty", 0) or 0)

    if executed_qty > 0 and cumulative_quote_qty > 0:
        return cumulative_quote_qty / executed_qty

    return 0.0


def _align_quantity_to_step(qty: float, filters: dict) -> float:
    lot_size_filter = filters.get("lot_size_filter", {})
    quantity_check = validate_quantity(qty, lot_size_filter)
    return float(quantity_check.get("aligned_qty", qty))


def _build_pending_order_from_response(order_response: dict, side: str) -> dict:
    return {
        "orderId": int(order_response["orderId"]),
        "status": str(order_response["status"]).upper(),
        "side": side.upper(),
    }


def _reconcile_open_trade(
    *,
    symbol: str,
    symbol_info: dict,
    open_trade: dict,
) -> tuple[str, dict | None]:
    entry_order_id = int(open_trade.get("entry_order_id", 0))
    try:
        entry_order = get_order(symbol, entry_order_id, BINANCE_BASE_URL)
    except HTTPError as error:
        if _is_missing_order_error(error):
            return "STALE_OPEN_TRADE_CLEARED", None
        return "OPEN_TRADE_RECONCILE_ERROR_KEEP", open_trade
    except Exception:
        return "OPEN_TRADE_RECONCILE_ERROR_KEEP", open_trade

    order_status = str(entry_order.get("status", "")).upper()
    order_side = str(entry_order.get("side", "")).upper()
    executed_qty = float(entry_order.get("executedQty", 0) or 0)

    if order_status != "FILLED" or order_side != "BUY" or executed_qty <= 0:
        return "STALE_OPEN_TRADE_CLEARED", None

    account_info = get_account_info()
    base_asset = str(symbol_info.get("baseAsset", ""))
    asset_balance = extract_asset_balance(account_info, base_asset)
    held_qty = float(asset_balance.get("total", 0.0))
    entry_qty = float(open_trade.get("entry_qty", 0.0))

    if held_qty <= 0:
        return "STALE_OPEN_TRADE_CLEARED", None

    if held_qty + 1e-12 < entry_qty:
        return "STALE_OPEN_TRADE_CLEARED", None

    confirmed_open_trade = {
        "status": "OPEN",
        "entry_price": _extract_fill_price(entry_order),
        "entry_qty": executed_qty,
        "entry_order_id": int(entry_order["orderId"]),
        "entry_side": "BUY",
    }
    return "OPEN_TRADE_CONFIRMED", confirmed_open_trade


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
                    "entry_price": _extract_fill_price(order_info),
                    "entry_qty": float(order_info["executedQty"]),
                    "entry_order_id": int(order_info["orderId"]),
                    "entry_side": "BUY",
                }
                return "PROMOTE_TO_OPEN_TRADE", None, open_trade

            return "SELL_FILLED", None, None

        if status in {"NEW", "PARTIALLY_FILLED", "PENDING_NEW"}:
            return "PENDING_CONFIRMED", pending, None

        return "PENDING_CLEARED", None, None

    except HTTPError as error:
        if _is_missing_order_error(error):
            open_orders = get_open_orders(symbol)
            matched_order = _find_open_order_by_id(open_orders, order_id)

            if matched_order:
                pending["status"] = matched_order.get("status", pending.get("status"))
                return "PENDING_CONFIRMED_FROM_OPEN_ORDERS", pending, None

            return "STALE_PENDING_ORDER_CLEARED", None, None

        return "PENDING_RECONCILE_ERROR_KEEP", pending, None
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
    state: dict = {}
    price = 0.0
    pending = None
    open_trade = None

    try:
        state = _load_state(state_file)

        ping()
        get_server_time()
        symbol_info = get_symbol_info(SYMBOL)
        filters = extract_symbol_filters(symbol_info)
        price = get_price(SYMBOL)

        if not has_api_credentials():
            _save_and_finish(
                state_file=state_file,
                log_file=log_file,
                state=state,
                timestamp=timestamp,
                action="CREDENTIALS_MISSING",
                price=price,
                pending=None,
                open_trade=None,
                reason="missing_api_credentials",
            )
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
                    reason="pending_buy_filled_promoted_to_open_trade",
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
                reason=action.lower(),
            )
            return

        if open_trade:
            open_trade_action, open_trade_after = _reconcile_open_trade(
                symbol=SYMBOL,
                symbol_info=symbol_info,
                open_trade=open_trade,
            )

            if open_trade_action != "OPEN_TRADE_CONFIRMED":
                _save_and_finish(
                    state_file=state_file,
                    log_file=log_file,
                    state=state,
                    timestamp=timestamp,
                    action=open_trade_action,
                    price=price,
                    pending=None,
                    open_trade=open_trade_after,
                    reason=open_trade_action.lower(),
                )
                return

            open_trade = open_trade_after
            entry_price = float(open_trade["entry_price"])
            entry_qty = float(open_trade["entry_qty"])

            target_price = calculate_target_price(entry_price, TARGET_PCT)
            stop_price = calculate_stop_price(entry_price, STOP_LOSS_PCT)

            if should_exit_long(price, target_price):
                adjusted_exit = auto_adjust_order_inputs(price, entry_qty, filters)
                adjusted_exit_qty = min(entry_qty, float(adjusted_exit["adjusted_qty"]))

                exit_validation = validate_order(
                    float(adjusted_exit["adjusted_price"]),
                    adjusted_exit_qty,
                    filters,
                )

                if not exit_validation.get("all_valid", False):
                    _save_and_finish(
                        state_file=state_file,
                        log_file=log_file,
                        state=state,
                        timestamp=timestamp,
                        action="SELL_REJECTED_BY_VALIDATION",
                        price=price,
                        pending=None,
                        open_trade=open_trade,
                        reason="sell_limit_validation_failed",
                    )
                    return

                payload = build_limit_order_payload(
                    symbol=SYMBOL,
                    side="SELL",
                    price=float(adjusted_exit["adjusted_price"]),
                    quantity=adjusted_exit_qty,
                )

                _validate_limit_order_before_live(payload)
                order_response = send_live_testnet_order(payload)
                order_status = str(order_response.get("status", "")).upper()

                if order_status == "FILLED":
                    _save_and_finish(
                        state_file=state_file,
                        log_file=log_file,
                        state=state,
                        timestamp=timestamp,
                        action="SELL_FILLED",
                        price=price,
                        pending=None,
                        open_trade=None,
                        reason="target_exit_limit_filled",
                    )
                    return

                pending = _build_pending_order_from_response(order_response, "SELL")

                _save_and_finish(
                    state_file=state_file,
                    log_file=log_file,
                    state=state,
                    timestamp=timestamp,
                    action="SELL_SUBMITTED",
                    price=price,
                    pending=pending,
                    open_trade=open_trade,
                    reason="target_exit_limit_submitted",
                )
                return

            if should_stop(price, stop_price):
                aligned_stop_qty = _align_quantity_to_step(entry_qty, filters)

                if aligned_stop_qty <= 0:
                    _save_and_finish(
                        state_file=state_file,
                        log_file=log_file,
                        state=state,
                        timestamp=timestamp,
                        action="STOP_REJECTED_INVALID_QTY",
                        price=price,
                        pending=None,
                        open_trade=open_trade,
                        reason="stop_market_qty_not_valid",
                    )
                    return

                payload = {
                    "symbol": SYMBOL,
                    "side": "SELL",
                    "type": "MARKET",
                    "quantity": str(aligned_stop_qty),
                }

                order_response = send_live_testnet_order(payload)
                order_status = str(order_response.get("status", "")).upper()

                if order_status == "FILLED":
                    _save_and_finish(
                        state_file=state_file,
                        log_file=log_file,
                        state=state,
                        timestamp=timestamp,
                        action="STOP_MARKET_FILLED",
                        price=price,
                        pending=None,
                        open_trade=None,
                        reason="protective_stop_market_filled",
                    )
                    return

                pending = _build_pending_order_from_response(order_response, "SELL")

                _save_and_finish(
                    state_file=state_file,
                    log_file=log_file,
                    state=state,
                    timestamp=timestamp,
                    action="STOP_MARKET_SUBMITTED",
                    price=price,
                    pending=pending,
                    open_trade=open_trade,
                    reason="protective_stop_market_submitted",
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
                reason="target_and_stop_not_triggered",
            )
            return

        adj = auto_adjust_order_inputs(price, 0.001, filters)
        final_validation = adj.get("final_validation", {})

        if not final_validation.get("all_valid", False):
            _save_and_finish(
                state_file=state_file,
                log_file=log_file,
                state=state,
                timestamp=timestamp,
                action="BUY_REJECTED_BY_VALIDATION",
                price=price,
                pending=None,
                open_trade=None,
                reason="buy_limit_validation_failed",
            )
            return

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
                "entry_price": _extract_fill_price(order_response),
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
            reason=action.lower(),
        )

    except Exception as e:
        try:
            _save_and_finish(
                state_file=state_file,
                log_file=log_file,
                state=state,
                timestamp=timestamp,
                action="ERROR",
                price=price,
                pending=pending,
                open_trade=open_trade,
                reason=str(e),
            )
        except Exception:
            pass
        print(f"ERROR: {e}")

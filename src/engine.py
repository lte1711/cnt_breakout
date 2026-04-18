from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from requests import HTTPError

from binance_client import (
    extract_symbol_filters,
    get_price,
    get_server_time,
    get_symbol_info,
    has_api_credentials,
    ping,
)
from config import (
    ACTIVE_STRATEGY,
    BINANCE_BASE_URL,
    ENABLE_TEST_ORDER_VALIDATION,
    LOG_FILE,
    STATE_FILE,
    STRATEGY_PARAMS,
    SYMBOL,
)
from src.account_reader import get_account_info
from src.balance_reader import extract_asset_balance
from src.execution_decider import decide_execution
from src.entry_gate import evaluate_entry_gate_from_signal, get_entry_signal
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


SCHEMA_VERSION = "1.0"


def should_stop(price: float, stop_price: float) -> bool:
    return price <= stop_price


def should_exit_long(price: float, target_price: float) -> bool:
    return price >= target_price


def _default_risk_metrics() -> dict:
    return {
        "daily_loss_count": 0,
        "consecutive_losses": 0,
        "last_loss_time": None,
    }


def _normalize_risk_metrics(risk_metrics: dict | None) -> dict:
    if not isinstance(risk_metrics, dict):
        return _default_risk_metrics()

    return {
        "daily_loss_count": int(risk_metrics.get("daily_loss_count", 0) or 0),
        "consecutive_losses": int(risk_metrics.get("consecutive_losses", 0) or 0),
        "last_loss_time": risk_metrics.get("last_loss_time"),
    }


def _load_state(path: Path) -> dict:
    if not path.exists():
        return {}

    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(loaded, dict):
            return {}

        loaded.setdefault("schema_version", SCHEMA_VERSION)
        loaded.setdefault("strategy_name", ACTIVE_STRATEGY)
        loaded["risk_metrics"] = _normalize_risk_metrics(loaded.get("risk_metrics"))
        return loaded
    except Exception:
        return {}


def _normalize_pending_order(pending: dict | None) -> dict | None:
    if not isinstance(pending, dict):
        return None

    required = {"orderId", "status", "side"}
    if not required.issubset(pending):
        return None

    order_id = int(pending["orderId"])
    if order_id <= 0:
        return None

    normalized = {
        "orderId": order_id,
        "status": str(pending["status"]).upper(),
        "side": str(pending["side"]).upper(),
    }

    if "strategy_name" in pending:
        normalized["strategy_name"] = str(pending["strategy_name"])

    if "stop_price" in pending and pending["stop_price"] is not None:
        normalized["stop_price"] = float(pending["stop_price"])

    if "target_price" in pending and pending["target_price"] is not None:
        normalized["target_price"] = float(pending["target_price"])

    return normalized


def _build_exit_model_from_strategy(strategy_name: str, entry_price: float) -> tuple[float | None, float | None]:
    params = STRATEGY_PARAMS.get(strategy_name, {})
    target_pct = params.get("target_pct")
    stop_loss_pct = params.get("stop_loss_pct")

    if target_pct is None or stop_loss_pct is None:
        return None, None

    target_price = entry_price * (1 + float(target_pct))
    stop_price = entry_price * (1 - float(stop_loss_pct))
    return stop_price, target_price


def _normalize_open_trade(open_trade: dict | None) -> dict | None:
    if not isinstance(open_trade, dict):
        return None

    required = {"status", "entry_price", "entry_qty", "entry_order_id", "entry_side"}
    if not required.issubset(open_trade):
        return None

    strategy_name = str(open_trade.get("strategy_name") or ACTIVE_STRATEGY)
    entry_price = float(open_trade["entry_price"])
    entry_order_id = int(open_trade["entry_order_id"])
    if entry_order_id <= 0:
        return None

    stop_price = open_trade.get("stop_price")
    target_price = open_trade.get("target_price")

    if stop_price is None or target_price is None:
        stop_price, target_price = _build_exit_model_from_strategy(strategy_name, entry_price)

    return {
        "status": str(open_trade["status"]),
        "entry_price": entry_price,
        "entry_qty": float(open_trade["entry_qty"]),
        "entry_order_id": entry_order_id,
        "entry_side": str(open_trade["entry_side"]).upper(),
        "strategy_name": strategy_name,
        "stop_price": stop_price,
        "target_price": target_price,
    }


def _resolve_strategy_name(pending: dict | None, open_trade: dict | None) -> str:
    if isinstance(open_trade, dict) and open_trade.get("strategy_name"):
        return str(open_trade["strategy_name"])

    if isinstance(pending, dict) and pending.get("strategy_name"):
        return str(pending["strategy_name"])

    return ACTIVE_STRATEGY


def _build_state(
    *,
    timestamp: str,
    action: str,
    price: float,
    pending: dict | None,
    open_trade: dict | None,
    risk_metrics: dict | None = None,
) -> dict:
    normalized_pending = _normalize_pending_order(pending)
    normalized_open_trade = _normalize_open_trade(open_trade)

    return {
        "schema_version": SCHEMA_VERSION,
        "strategy_name": _resolve_strategy_name(normalized_pending, normalized_open_trade),
        "last_run_time": timestamp,
        "status": "stopped",
        "symbol": SYMBOL,
        "pending_order": normalized_pending,
        "open_trade": normalized_open_trade,
        "action": action,
        "price": price,
        "risk_metrics": _normalize_risk_metrics(risk_metrics),
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
    risk_metrics: dict | None = None,
) -> None:
    next_state = _build_state(
        timestamp=timestamp,
        action=action,
        price=price,
        pending=pending,
        open_trade=open_trade,
        risk_metrics=risk_metrics,
    )
    state.clear()
    state.update(next_state)

    write_state(state_file, next_state)

    append_log(
        log_file,
        (
            f"[{timestamp}] action={action} price={price} pending={pending} "
            f"open_trade={open_trade} strategy_name={next_state['strategy_name']} reason={reason}"
        ),
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


def _build_pending_order_from_response(
    order_response: dict,
    side: str,
    strategy_name: str | None = None,
    stop_price: float | None = None,
    target_price: float | None = None,
) -> dict:
    pending = {
        "orderId": int(order_response["orderId"]),
        "status": str(order_response["status"]).upper(),
        "side": side.upper(),
    }

    if strategy_name is not None:
        pending["strategy_name"] = strategy_name

    if stop_price is not None:
        pending["stop_price"] = stop_price

    if target_price is not None:
        pending["target_price"] = target_price

    return pending


def _build_open_trade_from_order(order_info: dict, pending: dict | None = None) -> dict:
    entry_price = _extract_fill_price(order_info)
    strategy_name = ACTIVE_STRATEGY
    stop_price = None
    target_price = None

    if isinstance(pending, dict):
        strategy_name = str(pending.get("strategy_name") or ACTIVE_STRATEGY)
        stop_price = pending.get("stop_price")
        target_price = pending.get("target_price")

    if stop_price is None or target_price is None:
        stop_price, target_price = _build_exit_model_from_strategy(strategy_name, entry_price)

    return {
        "status": "OPEN",
        "entry_price": entry_price,
        "entry_qty": float(order_info["executedQty"]),
        "entry_order_id": int(order_info["orderId"]),
        "entry_side": "BUY",
        "strategy_name": strategy_name,
        "stop_price": stop_price,
        "target_price": target_price,
    }


def _reconcile_open_trade(
    *,
    symbol: str,
    symbol_info: dict,
    open_trade: dict,
) -> tuple[str, dict | None]:
    normalized_open_trade = _normalize_open_trade(open_trade)
    if normalized_open_trade is None:
        return "INVALID_OPEN_TRADE_CLEARED", None

    entry_order_id = int(normalized_open_trade["entry_order_id"])
    try:
        entry_order = get_order(symbol, entry_order_id, BINANCE_BASE_URL)
    except HTTPError as error:
        if _is_missing_order_error(error):
            return "STALE_OPEN_TRADE_CLEARED", None
        return "OPEN_TRADE_RECONCILE_ERROR_KEEP", normalized_open_trade
    except Exception:
        return "OPEN_TRADE_RECONCILE_ERROR_KEEP", normalized_open_trade

    order_status = str(entry_order.get("status", "")).upper()
    order_side = str(entry_order.get("side", "")).upper()
    executed_qty = float(entry_order.get("executedQty", 0) or 0)

    if order_status != "FILLED" or order_side != "BUY" or executed_qty <= 0:
        return "STALE_OPEN_TRADE_CLEARED", None

    account_info = get_account_info()
    base_asset = str(symbol_info.get("baseAsset", ""))
    asset_balance = extract_asset_balance(account_info, base_asset)
    held_qty = float(asset_balance.get("total", 0.0))
    entry_qty = float(normalized_open_trade["entry_qty"])

    if held_qty <= 0 or held_qty + 1e-12 < entry_qty:
        return "STALE_OPEN_TRADE_CLEARED", None

    confirmed_open_trade = _build_open_trade_from_order(entry_order, normalized_open_trade)
    return "OPEN_TRADE_CONFIRMED", confirmed_open_trade


def _reconcile_pending_order(
    *,
    symbol: str,
    pending: dict,
) -> tuple[str, dict | None, dict | None]:
    normalized_pending = _normalize_pending_order(pending)
    if normalized_pending is None:
        return "STALE_PENDING_ORDER_CLEARED", None, None

    order_id = int(normalized_pending["orderId"])

    try:
        order_info = get_order(symbol, order_id, BINANCE_BASE_URL)
        status = str(order_info.get("status", "")).upper()

        if status == "FILLED":
            if normalized_pending.get("side") == "BUY":
                open_trade = _build_open_trade_from_order(order_info, normalized_pending)
                return "PROMOTE_TO_OPEN_TRADE", None, open_trade

            return "SELL_FILLED", None, None

        if status in {"NEW", "PARTIALLY_FILLED", "PENDING_NEW"}:
            normalized_pending["status"] = status
            return "PENDING_CONFIRMED", normalized_pending, None

        return "PENDING_CLEARED", None, None

    except HTTPError as error:
        if _is_missing_order_error(error):
            open_orders = get_open_orders(symbol)
            matched_order = _find_open_order_by_id(open_orders, order_id)

            if matched_order:
                normalized_pending["status"] = str(
                    matched_order.get("status", normalized_pending.get("status"))
                ).upper()
                return "PENDING_CONFIRMED_FROM_OPEN_ORDERS", normalized_pending, None

            return "STALE_PENDING_ORDER_CLEARED", None, None

        return "PENDING_RECONCILE_ERROR_KEEP", normalized_pending, None
    except Exception:
        return "PENDING_RECONCILE_ERROR_KEEP", normalized_pending, None


def _validate_limit_order_before_live(payload: dict) -> None:
    if not ENABLE_TEST_ORDER_VALIDATION:
        return

    send_test_order(payload)


def start_engine() -> None:
    project_root = Path(__file__).resolve().parent.parent
    log_file = project_root / LOG_FILE
    state_file = project_root / STATE_FILE

    print("engine strategy v1 started")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    state: dict = {}
    price = 0.0
    pending = None
    open_trade = None
    risk_metrics = _default_risk_metrics()

    try:
        state = _load_state(state_file)
        risk_metrics = _normalize_risk_metrics(state.get("risk_metrics"))

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
                risk_metrics=risk_metrics,
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
                    risk_metrics=risk_metrics,
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
                risk_metrics=risk_metrics,
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
                    reason=(
                        "invalid_or_stale_open_trade_state"
                        if open_trade_action == "INVALID_OPEN_TRADE_CLEARED"
                        else open_trade_action.lower()
                    ),
                    risk_metrics=risk_metrics,
                )
                return

            open_trade = open_trade_after
            target_price = open_trade.get("target_price")
            stop_price = open_trade.get("stop_price")

            if target_price is None or stop_price is None:
                _save_and_finish(
                    state_file=state_file,
                    log_file=log_file,
                    state=state,
                    timestamp=timestamp,
                    action="OPEN_TRADE_MISSING_EXIT_MODEL",
                    price=price,
                    pending=None,
                    open_trade=open_trade,
                    reason="missing_target_or_stop_price",
                    risk_metrics=risk_metrics,
                )
                return

            entry_qty = float(open_trade["entry_qty"])

            if should_exit_long(price, float(target_price)):
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
                        risk_metrics=risk_metrics,
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
                        risk_metrics=risk_metrics,
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
                    risk_metrics=risk_metrics,
                )
                return

            if should_stop(price, float(stop_price)):
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
                        risk_metrics=risk_metrics,
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
                        risk_metrics=risk_metrics,
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
                    risk_metrics=risk_metrics,
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
                risk_metrics=risk_metrics,
            )
            return

        signal = get_entry_signal(SYMBOL)
        entry_action, entry_reason = evaluate_entry_gate_from_signal(signal)

        if entry_action != "ENTRY_ALLOWED":
            _save_and_finish(
                state_file=state_file,
                log_file=log_file,
                state=state,
                timestamp=timestamp,
                action=entry_action,
                price=price,
                pending=None,
                open_trade=None,
                reason=entry_reason,
                risk_metrics=risk_metrics,
            )
            return

        if signal.exit_model is None:
            _save_and_finish(
                state_file=state_file,
                log_file=log_file,
                state=state,
                timestamp=timestamp,
                action="BUY_REJECTED_MISSING_EXIT_MODEL",
                price=price,
                pending=None,
                open_trade=None,
                reason="missing_exit_model",
                risk_metrics=risk_metrics,
            )
            return

        quote_asset = str(symbol_info.get("quoteAsset", ""))
        account_info = get_account_info()
        quote_balance = extract_asset_balance(account_info, quote_asset)
        decision = decide_execution(
            signal=signal,
            state=state,
            balance=quote_balance,
            filters=filters,
            requested_qty=0.001,
        )

        if not decision.execute:
            _save_and_finish(
                state_file=state_file,
                log_file=log_file,
                state=state,
                timestamp=timestamp,
                action=decision.action,
                price=price,
                pending=None,
                open_trade=None,
                reason=decision.reason,
                risk_metrics=risk_metrics,
            )
            return

        adj = auto_adjust_order_inputs(
            float(decision.validated_price or price),
            float(decision.validated_qty or 0.001),
            filters,
        )
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
                risk_metrics=risk_metrics,
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
        order_status = str(order_response.get("status", "")).upper()

        if order_status == "FILLED":
            open_trade = {
                "status": "OPEN",
                "entry_price": _extract_fill_price(order_response),
                "entry_qty": float(order_response["executedQty"]),
                "entry_order_id": int(order_response["orderId"]),
                "entry_side": "BUY",
                "strategy_name": signal.strategy_name,
                "stop_price": signal.exit_model.stop_price,
                "target_price": signal.exit_model.target_price,
            }
            pending = None
            action = "BUY_FILLED"
        else:
            pending = _build_pending_order_from_response(
                order_response,
                "BUY",
                strategy_name=signal.strategy_name,
                stop_price=signal.exit_model.stop_price,
                target_price=signal.exit_model.target_price,
            )
            open_trade = None
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
            risk_metrics=risk_metrics,
        )

    except Exception as error:
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
                reason=str(error),
                risk_metrics=risk_metrics,
            )
        except Exception:
            pass
        print(f"ERROR: {error}")

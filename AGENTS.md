STATUS=ACTIVE
VERSION=1.1
UPDATED=2026-04-18
PROJECT_NAME=CNT
MODE=BINANCE_SPOT_TESTNET

# --------------------------------------------------
# PROJECT ROOT RULE
# --------------------------------------------------

PROJECT_ROOT=CURRENT_CNT_REPOSITORY_ROOT
PATH_POLICY=REPO_RELATIVE_ONLY
ABSOLUTE_EXTERNAL_PROJECT_PATH=FORBIDDEN

ROOT_STRUCTURE=
run.ps1
main.py
config.py
binance_client.py
src/
data/
logs/
docs/
tests/

# --------------------------------------------------
# ENTRY RULE
# --------------------------------------------------

ENTRY_CHAIN=run.ps1->main.py->src.engine.start_engine
DIRECT_ENGINE_RUN=FORBIDDEN
ENTRY_CHAIN_BYPASS=FORBIDDEN

# --------------------------------------------------
# CORE PRINCIPLE
# --------------------------------------------------

VERIFY_FIRST=ACTIVE
FACT_ONLY=ACTIVE
STEP_BY_STEP=ACTIVE
EVIDENCE_REQUIRED=ACTIVE
ASSUMPTION_LABELING=ACTIVE
NO_UNVERIFIED_RUNTIME_CHANGE=ACTIVE

# --------------------------------------------------
# EXCHANGE ENVIRONMENT RULE
# --------------------------------------------------

EXCHANGE=BINANCE
MARKET=SPOT
ENVIRONMENT=TESTNET
USE_TESTNET=TRUE
REST_BASE_URL=https://testnet.binance.vision
API_SCOPE=/api_only
SAPI_USAGE=FORBIDDEN

# --------------------------------------------------
# CONFIG BASELINE
# --------------------------------------------------

DEFAULT_SYMBOL=ETHUSDT
STATE_FILE=data/state.json
LOG_FILE=logs/runtime.log
RECV_WINDOW=5000
REQUEST_TIMEOUT=5

# --------------------------------------------------
# ENGINE EXECUTION MODEL
# --------------------------------------------------

ENGINE_MODE=ONE_SHOT
LOOP=DISABLED

ENGINE_SEQUENCE=
1. load_state
2. ping_exchange
3. get_server_time
4. get_symbol_info
5. extract_symbol_filters
6. get_price
7. reconcile_pending_state
8. reconcile_open_trade_state
9. evaluate_exit
10. evaluate_new_entry
10-1. evaluate entry gate
10-2. validate entry order inputs
10-3. submit BUY LIMIT only if entry gate passed
11. write_state
12. append_log

# --------------------------------------------------
# STATE MACHINE
# --------------------------------------------------

FLOW=
NONE -> BUY -> PENDING -> FILLED -> OPEN_TRADE
OPEN_TRADE -> SELL -> PENDING -> FILLED -> CLOSED

# --------------------------------------------------
# STATE STRUCTURE
# --------------------------------------------------

STATE_TOP_LEVEL_KEYS=
last_run_time
status
symbol
pending_order
open_trade
action
price

PENDING_ORDER_KEYS=
orderId
status
side

OPEN_TRADE_KEYS=
status
entry_price
entry_qty
entry_order_id
entry_side

# --------------------------------------------------
# STATE TRUTH RULE
# --------------------------------------------------

EXCHANGE_STATE_IS_PRIMARY=TRUE
LOCAL_STATE_IS_SECONDARY=TRUE

RESET_AND_RECONCILIATION_RULE=
1. Spot Testnet reset can delete pending and executed orders
2. local pending_order must never be trusted without exchange query
3. local open_trade must be revalidated against exchange/account evidence
4. if exchange-side order does not exist, local state is stale
5. stale pending/open_trade must be cleaned and logged
6. reset suspicion must be recorded in logs and docs

# --------------------------------------------------
# POSITION RULE
# --------------------------------------------------

SINGLE_POSITION_ONLY=TRUE
ONE_PENDING_ONLY=TRUE
AVERAGING=FORBIDDEN
PARTIAL_EXIT=FORBIDDEN

# --------------------------------------------------
# ORDER POLICY
# --------------------------------------------------

ORDER_POLICY=HYBRID_CONTROLLED

ENTRY_ORDER_RULE=
1. entry is BUY LIMIT only
2. no entry if pending_order exists
3. no entry if open_trade exists
4. entry requires exchange filter validation
5. entry requires adjusted price and qty when needed

EXIT_ORDER_RULE=
1. target exit uses SELL LIMIT
2. protective stop exit uses SELL MARKET
3. MARKET exit is allowed only for explicit protective flow
4. every MARKET exit must be logged with reason

ALLOWED_ORDER_TYPES=
BUY_LIMIT
SELL_LIMIT
SELL_MARKET_PROTECTIVE_ONLY

UNAPPROVED_ORDER_TYPES=FORBIDDEN

# --------------------------------------------------
# VALIDATION RULE
# --------------------------------------------------

PRECHECK_REQUIRED=TRUE

PRECHECK_SEQUENCE=
1. GET /api/v3/ping
2. GET /api/v3/time
3. GET /api/v3/exchangeInfo
4. extract symbol filters
5. validate_order
6. auto_adjust_order_inputs
7. use /api/v3/order/test before live order when validation certainty is needed

FILTER_SOURCE=/api/v3/exchangeInfo

MANDATORY_FILTERS=
PRICE_FILTER
LOT_SIZE
MIN_NOTIONAL_OR_NOTIONAL

# --------------------------------------------------
# SIGNATURE RULE
# --------------------------------------------------

SIGNED_REQUEST_RULE=
1. all signed requests must use one shared signing path
2. query serialization must be percent-encoded before signature
3. duplicate custom signing logic is forbidden
4. recvWindow must be consistently applied on signed requests unless explicitly exempted

# --------------------------------------------------
# ORDER INPUT RULE
# --------------------------------------------------

PRICE_ALIGNMENT=REQUIRED
QTY_ALIGNMENT=REQUIRED
MIN_NOTIONAL_PASS=REQUIRED

AUTO_ADJUST_POLICY=
1. floor price to tick_size
2. floor qty to step_size
3. raise qty to min_qty if needed
4. raise qty to min_notional if needed
5. cap qty to max_qty if needed
6. reject if final validation still fails

# --------------------------------------------------
# PENDING RULE
# --------------------------------------------------

PENDING_POLICY=
1. pending_order must be resolved before any new order
2. pending BUY filled -> promote to open_trade
3. pending SELL filled -> close trade
4. unresolved pending must be queried from exchange
5. missing exchange order must trigger stale-state review

# --------------------------------------------------
# EXIT RULE
# --------------------------------------------------

EXIT_REFERENCE=ENTRY_PRICE
TARGET_EXIT=DETERMINISTIC_ONLY
STOP_EXIT=DETERMINISTIC_ONLY
ASSUMPTION_BASED_EXIT=FORBIDDEN

CURRENT_ENGINE_EXIT_FIELDS=
TARGET_PCT
STOP_LOSS_PCT

# --------------------------------------------------
# LOGGING RULE
# --------------------------------------------------

LOG_WRITE_REQUIRED=TRUE

LOG_REQUIRED_FIELDS=
action
price
pending_order
open_trade
reason

ERROR_POLICY=
1. write state when possible
2. write log when possible
3. preserve exchange error when available
4. never fail silently

# --------------------------------------------------
# FILE RESPONSIBILITY RULE
# --------------------------------------------------

binance_client.py=shared_exchange_client_and_signing
config.py=runtime_config_only
main.py=application_entry_only
src/engine.py=execution_orchestration_only
src/entry_gate.py=new_entry_gate_evaluation_only
src/strategy_signal.py=strategy_signal_generation_only
src/log_writer.py=log_write_only
src/order_executor.py=order_submission_only
src/order_payload_builder.py=limit_payload_build_only_until_extended
src/order_query.py=exchange_query_only_using_shared_signing
src/order_validator.py=filter_validation_and_adjustment_only
src/state_writer.py=state_write_only
src/target_exit.py=target_exit_calculation_only
# --------------------------------------------------
# RECORD RULE
# --------------------------------------------------

EVERY_MEANINGFUL_STEP_MUST_HAVE=
1. design summary
2. validation result
3. record text

# --------------------------------------------------
# PROHIBITED
# --------------------------------------------------

1. /sapi usage in testnet mode
2. external absolute path as project truth
3. direct engine execution outside entry chain
4. multiple simultaneous positions
5. new order while pending exists
6. assumption-based exit logic
7. unvalidated live order submission
8. duplicate signing logic
9. structure rewrite without explicit approval
9-EXCEPTION. new internal module creation is allowed when:
- it reduces engine responsibility
- it does not bypass entry chain
- it does not change exchange/order truth rules
- it is explicitly approved in design record

# --------------------------------------------------
# PRINCIPLE
# --------------------------------------------------

THIS CONSTITUTION IS THE SINGLE SOURCE OF TRUTH
FOR THE CURRENT CNT PROJECT AND BINANCE SPOT TESTNET OPERATION.
ALL STRATEGY DESIGN AND CODE CHANGES MUST FOLLOW THIS FILE FIRST.
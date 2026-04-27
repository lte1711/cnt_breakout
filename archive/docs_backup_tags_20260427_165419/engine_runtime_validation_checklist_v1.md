---
aliases:
  - engine_runtime_validation_checklist_v1
---

CNT engine runtime validation checklist v1

1. Pre-check
- Confirm .env exists at repo root.
- Confirm BINANCE_API_KEY and BINANCE_API_SECRET are set.
- Confirm current branch is main and worktree is clean.

2. Static validation
- Run:
  python -m py_compile main.py config.py binance_client.py src\account_reader.py src\balance_reader.py src\engine.py src\entry_gate.py src\indicators.py src\log_writer.py src\market_data.py src\models\market_context.py src\models\strategy_signal.py src\order_executor.py src\order_payload_builder.py src\order_query.py src\order_roundtrip.py src\order_validator.py src\risk\exit_models.py src\state_writer.py src\strategy_manager.py src\strategy_registry.py src\strategies\base.py src\strategies\breakout_v1.py src\strategy_signal.py src\target_exit.py

3. Read-only strategy check
- Run:
  python -c "from src.strategy_manager import generate_strategy_signal; import json; s=generate_strategy_signal('ETHUSDT'); print(json.dumps({'strategy_name': s.strategy_name, 'entry_allowed': s.entry_allowed, 'side': s.side, 'trigger': s.trigger, 'reason': s.reason, 'market_state': s.market_state, 'volatility_state': s.volatility_state, 'entry_price_hint': s.entry_price_hint}, indent=2, default=str))"

4. Read-only state check
- Inspect:
  Get-Content .\data\state.json
  Get-Content .\logs\runtime.log -Tail 20

5. One-shot engine run
- Run only after confirming current price is not near stop_price or target_price:
  powershell -NoProfile -ExecutionPolicy Bypass -File .\run.ps1

6. Post-run check
- Confirm state.json keeps schema_version, strategy_name, pending_order, open_trade.
- Confirm runtime.log records action, price, pending, open_trade, strategy_name, reason.
- Confirm unexpected new order was not submitted.

7. Safety rule
- If current open_trade target_price or stop_price is close to current market price, do not run the engine for validation.

---

## Obsidian Links

- [[00 Docs Index]]


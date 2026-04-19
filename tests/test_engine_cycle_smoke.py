from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import src.engine as engine


class EngineCycleSmokeTests(unittest.TestCase):
    def test_build_state_preserves_current_cycle_semantics(self) -> None:
        state = engine._build_state(
            timestamp="2026-04-19 23:00:00",
            action="NO_ENTRY_SIGNAL",
            price=2300.0,
            pending=None,
            open_trade=None,
            risk_metrics={"daily_loss_count": 1, "consecutive_losses": 0, "last_loss_time": None},
        )

        self.assertEqual(state["schema_version"], "1.0")
        self.assertEqual(state["status"], "stopped")
        self.assertEqual(state["action"], "NO_ENTRY_SIGNAL")
        self.assertEqual(state["strategy_name"], engine.ACTIVE_STRATEGY)
        self.assertIn("risk_metrics", state)

    def test_save_and_finish_updates_state_and_calls_side_effect_layers(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            state_file = root / "data" / "state.json"
            log_file = root / "logs" / "runtime.log"
            portfolio_state_file = root / "data" / "portfolio_state.json"
            state: dict = {}

            with (
                patch("src.engine.write_state") as write_state,
                patch("src.engine.save_portfolio_state") as save_portfolio_state,
                patch("src.engine.build_portfolio_state", return_value={"ok": True}) as build_portfolio_state,
                patch("src.engine.append_log") as append_log,
                patch("src.engine.generate_and_save_performance_snapshot", return_value={"timestamp": "2026-04-19 23:00:00"}) as snapshot_gen,
                patch("src.engine.generate_performance_report") as perf_report,
                patch("src.engine.evaluate_live_gate", return_value={"status": "NOT_READY"}) as live_gate,
                patch("src.engine.save_live_gate_decision") as save_gate,
            ):
                engine._save_and_finish(
                    state_file=state_file,
                    log_file=log_file,
                    state=state,
                    timestamp="2026-04-19 23:00:00",
                    action="NO_ENTRY_SIGNAL",
                    price=2301.0,
                    pending=None,
                    open_trade=None,
                    reason="test_reason",
                    risk_metrics={"daily_loss_count": 0, "consecutive_losses": 0, "last_loss_time": None},
                    portfolio_state_file=portfolio_state_file,
                    cash_balance=12.5,
                )

            self.assertEqual(state["action"], "NO_ENTRY_SIGNAL")
            self.assertEqual(state["status"], "stopped")
            write_state.assert_called_once()
            build_portfolio_state.assert_called_once()
            save_portfolio_state.assert_called_once()
            append_log.assert_called_once()
            snapshot_gen.assert_called_once()
            perf_report.assert_called_once()
            live_gate.assert_called_once()
            save_gate.assert_called_once()


if __name__ == "__main__":
    unittest.main()

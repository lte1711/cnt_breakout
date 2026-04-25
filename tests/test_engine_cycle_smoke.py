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
            strategy_name_override="pullback_v1",
        )

        self.assertEqual(state["schema_version"], "1.0")
        self.assertEqual(state["status"], "stopped")
        self.assertEqual(state["action"], "NO_ENTRY_SIGNAL")
        self.assertEqual(state["strategy_name"], "pullback_v1")
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
                patch("src.engine.load_strategy_metrics", return_value={}) as load_metrics,
                patch("src.engine.load_portfolio_state", return_value={}) as load_portfolio,
                patch("src.engine.build_auxiliary_recovery_status", return_value={"status": "ok"}) as aux_status,
                patch("src.engine.save_auxiliary_recovery_status") as save_aux,
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
                    strategy_name_override="pullback_v1",
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
            load_metrics.assert_called_once()
            load_portfolio.assert_called_once()
            aux_status.assert_called_once()
            save_aux.assert_called_once()
            self.assertEqual(state["strategy_name"], "pullback_v1")

    def test_run_breakout_v2_shadow_does_not_interrupt_on_log_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            event = {
                "ts": "2026-04-22T15:00:00+09:00",
                "symbol": "ETHUSDT",
                "strategy": "breakout_v2_shadow",
                "signal_generated": True,
                "entry_allowed": False,
                "filter_reason": "volume_not_confirmed",
                "confidence": 0.78,
                "vwap": 2300.0,
                "band_width_ratio": 0.01,
                "band_expansion_ratio": 1.05,
                "volume_ratio": 0.8,
                "hypothetical_entry": False,
            }
            with (
                patch("src.engine.evaluate_breakout_v2_shadow", return_value=event) as evaluate_shadow,
                patch("src.engine.append_shadow_log", side_effect=OSError("log failed")) as append_shadow_log,
                patch("src.engine.update_shadow_snapshot") as update_shadow_snapshot,
            ):
                engine._run_breakout_v2_shadow(
                    project_root=root,
                    symbol="ETHUSDT",
                )

            evaluate_shadow.assert_called_once()
            append_shadow_log.assert_called_once()
            update_shadow_snapshot.assert_called_once()

    def test_run_breakout_v3_shadow_does_not_interrupt_on_log_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            event = {
                "timestamp": "2026-04-24T12:00:00+09:00",
                "symbol": "ETHUSDT",
                "strategy_name": "breakout_v3_candidate",
                "allowed": False,
                "summary_reason": "trigger_blocked",
                "first_blocker": "breakout_not_confirmed",
                "hard_blocker": "breakout_not_confirmed",
                "soft_pass_count": 2,
                "soft_fail_count": 4,
                "soft_total_count": 6,
                "min_soft_pass_required": 3,
                "stage_flags": {"regime": True, "setup": True, "trigger": False, "quality": False},
                "condition_flags": {"market_bias_pass": True, "breakout_confirmed": False},
                "secondary_fail_reasons": ["band_width_fail", "volume_fail"],
                "metadata": {"primary_interval": "5m", "entry_interval": "1m"},
            }
            with (
                patch("src.engine.evaluate_breakout_v3_shadow_for_symbol", return_value=event) as evaluate_shadow,
                patch("src.engine.append_breakout_v3_shadow_log", side_effect=OSError("log failed")) as append_log,
                patch("src.engine.update_breakout_v3_shadow_snapshot") as update_snapshot,
            ):
                engine._run_breakout_v3_shadow(
                    project_root=root,
                    symbol="ETHUSDT",
                )

            evaluate_shadow.assert_called_once()
            append_log.assert_called_once()
            update_snapshot.assert_called_once()


if __name__ == "__main__":
    unittest.main()

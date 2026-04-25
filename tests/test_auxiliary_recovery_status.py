from __future__ import annotations

import unittest

from src.analytics.auxiliary_recovery_status import build_auxiliary_recovery_status


class AuxiliaryRecoveryStatusTests(unittest.TestCase):
    def test_pullback_positive_but_under_sample_is_observation_only(self) -> None:
        status = build_auxiliary_recovery_status(
            snapshot={"closed_trades": 35, "expectancy": -0.01, "net_pnl": -0.5},
            strategy_metrics={
                "pullback_v1": {
                    "trades_closed": 32,
                    "wins": 17,
                    "losses": 15,
                    "gross_profit": 0.28,
                    "gross_loss": 0.23,
                    "win_rate": 0.53125,
                    "expectancy": 0.0017,
                    "profit_factor": 1.23,
                },
                "breakout_v1": {
                    "trades_closed": 3,
                    "wins": 1,
                    "losses": 2,
                    "gross_profit": 0.01,
                    "gross_loss": 0.08,
                    "win_rate": 0.3333,
                    "expectancy": -0.02,
                    "profit_factor": 0.17,
                },
            },
            state={"strategy_name": "pullback_v1", "risk_metrics": {"daily_loss_count": 0, "consecutive_losses": 3}},
            portfolio_state={"open_positions": [], "total_exposure": 0.0, "daily_loss_count": 0, "consecutive_losses": 3},
            live_gate_decision={"status": "FAIL", "reason": "NON_POSITIVE_EXPECTANCY"},
        )

        self.assertEqual(status["official_gate"]["status"], "FAIL")
        self.assertEqual(status["pullback_v1"]["closed_trades"], 32)
        self.assertTrue(status["recovery_signal"]["is_positive_expectancy"])
        self.assertFalse(status["recovery_signal"]["is_statistically_valid"])
        self.assertEqual(status["recovery_signal"]["status"], "RECOVERY_OBSERVATION_IN_PROGRESS")
        self.assertEqual(status["system_excluding_breakout_v1"]["included_strategies"], ["pullback_v1"])

    def test_recovery_ready_requires_minimum_sample(self) -> None:
        status = build_auxiliary_recovery_status(
            snapshot={"closed_trades": 50, "expectancy": 0.01, "net_pnl": 1.0},
            strategy_metrics={
                "pullback_v1": {
                    "trades_closed": 50,
                    "wins": 30,
                    "losses": 20,
                    "gross_profit": 2.0,
                    "gross_loss": 1.0,
                    "win_rate": 0.6,
                    "expectancy": 0.02,
                    "profit_factor": 2.0,
                }
            },
            state={"strategy_name": "pullback_v1", "risk_metrics": {"daily_loss_count": 0, "consecutive_losses": 0}},
            portfolio_state={"open_positions": [], "total_exposure": 0.0, "daily_loss_count": 0, "consecutive_losses": 0},
            live_gate_decision={"status": "LIVE_READY", "reason": "ALL_GATES_PASSED"},
        )

        self.assertTrue(status["recovery_signal"]["all_recovery_criteria_passed"])
        self.assertEqual(status["recovery_signal"]["status"], "RECOVERY_EVIDENCE_READY")


if __name__ == "__main__":
    unittest.main()

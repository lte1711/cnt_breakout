from __future__ import annotations

import unittest

from src.validation.live_gate_evaluator import evaluate_live_gate


class LiveGateEvaluatorTests(unittest.TestCase):
    def test_returns_not_ready_when_sample_is_insufficient(self) -> None:
        decision = evaluate_live_gate(
            {
                "closed_trades": 3,
                "expectancy": 0.5,
                "net_pnl": 1.0,
                "max_consecutive_losses": 0,
                "risk_trigger_stats": {"LOSS_COOLDOWN": 1},
            }
        )

        self.assertEqual(decision["status"], "NOT_READY")
        self.assertEqual(decision["reason"], "INSUFFICIENT_SAMPLE")

    def test_sample_gate_runs_before_expectancy_gate(self) -> None:
        decision = evaluate_live_gate(
            {
                "closed_trades": 20,
                "expectancy": 0.0,
                "net_pnl": 1.0,
                "max_consecutive_losses": 0,
                "risk_trigger_stats": {"LOSS_COOLDOWN": 1},
            }
        )

        self.assertEqual(decision["status"], "NOT_READY")
        self.assertEqual(decision["reason"], "INSUFFICIENT_SAMPLE")

    def test_returns_fail_when_expectancy_is_non_positive_after_minimum_sample(self) -> None:
        decision = evaluate_live_gate(
            {
                "closed_trades": 50,
                "expectancy": 0.0,
                "net_pnl": 1.0,
                "max_consecutive_losses": 0,
                "risk_trigger_stats": {"LOSS_COOLDOWN": 1},
            }
        )

        self.assertEqual(decision["status"], "FAIL")
        self.assertEqual(decision["reason"], "NON_POSITIVE_EXPECTANCY")

    def test_returns_live_ready_when_all_gates_pass(self) -> None:
        decision = evaluate_live_gate(
            {
                "closed_trades": 55,
                "expectancy": 0.02,
                "net_pnl": 1.5,
                "max_consecutive_losses": 2,
                "risk_trigger_stats": {"LOSS_COOLDOWN": 1},
            }
        )

        self.assertEqual(decision["status"], "LIVE_READY")
        self.assertEqual(decision["reason"], "ALL_GATES_PASSED")

    def test_returns_live_ready_when_daily_loss_limit_was_observed(self) -> None:
        decision = evaluate_live_gate(
            {
                "closed_trades": 50,
                "expectancy": 0.01,
                "net_pnl": 0.5,
                "max_consecutive_losses": 2,
                "risk_trigger_stats": {"DAILY_LOSS_LIMIT": 4},
            }
        )

        self.assertEqual(decision["status"], "LIVE_READY")
        self.assertEqual(decision["reason"], "ALL_GATES_PASSED")

    def test_returns_fail_when_no_risk_guard_trigger_was_observed(self) -> None:
        decision = evaluate_live_gate(
            {
                "closed_trades": 50,
                "expectancy": 0.01,
                "net_pnl": 0.5,
                "max_consecutive_losses": 2,
                "risk_trigger_stats": {},
            }
        )

        self.assertEqual(decision["status"], "FAIL")
        self.assertEqual(decision["reason"], "RISK_GUARD_NOT_OBSERVED")


if __name__ == "__main__":
    unittest.main()

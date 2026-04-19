from __future__ import annotations

import unittest

from src.risk.enhanced_exit_manager import evaluate_exit


class ExitManagerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.filters = {
            "lot_size_filter": {
                "min_qty": "0.0001",
                "max_qty": "9000.00000000",
                "step_size": "0.00010000",
            }
        }

    def test_stop_exit_is_triggered_when_price_is_below_stop(self) -> None:
        open_trade = {
            "entry_price": 100.0,
            "entry_qty": 1.0,
            "stop_price": 99.0,
            "target_price": 101.0,
            "highest_price_since_entry": 100.5,
        }

        exit_signal = evaluate_exit(open_trade, 98.5, {}, self.filters)

        self.assertTrue(exit_signal.should_exit)
        self.assertEqual(exit_signal.exit_type, "STOP")
        self.assertEqual(exit_signal.reason, "stop_price_triggered")

    def test_partial_exit_is_triggered_when_partial_target_is_hit(self) -> None:
        open_trade = {
            "entry_price": 100.0,
            "entry_qty": 1.0,
            "stop_price": 99.0,
            "target_price": 103.0,
            "highest_price_since_entry": 101.2,
            "partial_exit_levels": [
                {"qty_ratio": 0.5, "target_price": 101.0},
            ],
            "partial_exit_progress": 0,
        }

        exit_signal = evaluate_exit(open_trade, 101.0, {}, self.filters)

        self.assertTrue(exit_signal.should_exit)
        self.assertEqual(exit_signal.exit_type, "PARTIAL")
        self.assertEqual(exit_signal.reason, "partial_exit_target_triggered")
        self.assertAlmostEqual(exit_signal.partial_qty or 0.0, 0.5, places=4)

    def test_partial_exit_below_min_qty_returns_no_exit(self) -> None:
        open_trade = {
            "entry_price": 100.0,
            "entry_qty": 0.0001,
            "stop_price": 99.0,
            "target_price": 103.0,
            "highest_price_since_entry": 101.2,
            "partial_exit_levels": [
                {"qty_ratio": 0.2, "target_price": 101.0},
            ],
            "partial_exit_progress": 0,
        }

        exit_signal = evaluate_exit(open_trade, 101.0, {}, self.filters)

        self.assertFalse(exit_signal.should_exit)
        self.assertEqual(exit_signal.reason, "partial_exit_qty_below_min_qty")


if __name__ == "__main__":
    unittest.main()

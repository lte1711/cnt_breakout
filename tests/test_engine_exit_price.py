from __future__ import annotations

import unittest

import src.engine as engine
from src.models.exit_signal import ExitSignal


class EngineExitPriceTests(unittest.TestCase):
    def test_target_exit_limit_price_uses_signal_target_not_current_price(self) -> None:
        exit_signal = ExitSignal(
            should_exit=True,
            exit_type="TARGET",
            reason="target_price_triggered",
            target_price=2322.082238,
            stop_price=2314.43,
            partial_qty=None,
        )

        selected_price = engine._select_exit_limit_price(exit_signal, current_price=2322.74)

        self.assertEqual(selected_price, 2322.082238)

    def test_partial_exit_limit_price_uses_signal_target_not_current_price(self) -> None:
        exit_signal = ExitSignal(
            should_exit=True,
            exit_type="PARTIAL",
            reason="partial_exit_target_triggered",
            target_price=101.5,
            stop_price=98.0,
            partial_qty=0.001,
        )

        selected_price = engine._select_exit_limit_price(exit_signal, current_price=102.4)

        self.assertEqual(selected_price, 101.5)

    def test_time_exit_limit_price_keeps_current_price_policy(self) -> None:
        exit_signal = ExitSignal(
            should_exit=True,
            exit_type="TIME_EXIT",
            reason="time_based_exit_triggered",
            target_price=None,
            stop_price=98.0,
            partial_qty=None,
        )

        selected_price = engine._select_exit_limit_price(exit_signal, current_price=100.25)

        self.assertEqual(selected_price, 100.25)

    def test_target_exit_without_target_price_fails_closed(self) -> None:
        exit_signal = ExitSignal(
            should_exit=True,
            exit_type="TARGET",
            reason="target_price_triggered",
            target_price=None,
            stop_price=98.0,
            partial_qty=None,
        )

        with self.assertRaises(ValueError):
            engine._select_exit_limit_price(exit_signal, current_price=100.25)


if __name__ == "__main__":
    unittest.main()

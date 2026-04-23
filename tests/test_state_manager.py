from __future__ import annotations

import unittest

from src.state.state_manager import build_portfolio_state


class StateManagerTests(unittest.TestCase):
    def test_build_portfolio_state_preserves_risk_counters_without_open_trade(self) -> None:
        portfolio_state = build_portfolio_state(
            {
                "last_run_time": "2026-04-24 06:24:00",
                "risk_metrics": {
                    "daily_loss_count": 3,
                    "consecutive_losses": 2,
                },
                "open_trade": None,
            },
            cash_balance=100.0,
        )

        self.assertEqual(portfolio_state.daily_loss_count, 3)
        self.assertEqual(portfolio_state.consecutive_losses, 2)
        self.assertEqual(portfolio_state.cash_balance, 100.0)
        self.assertEqual(portfolio_state.total_exposure, 0.0)

    def test_build_portfolio_state_preserves_risk_counters_with_open_trade(self) -> None:
        portfolio_state = build_portfolio_state(
            {
                "symbol": "ETHUSDT",
                "last_run_time": "2026-04-24 06:24:00",
                "risk_metrics": {
                    "daily_loss_count": 1,
                    "consecutive_losses": 1,
                },
                "open_trade": {
                    "status": "OPEN",
                    "entry_price": 2300.0,
                    "entry_qty": 0.1,
                    "entry_order_id": 123,
                    "entry_side": "BUY",
                    "strategy_name": "pullback_v1",
                    "stop_price": 2290.0,
                    "target_price": 2310.0,
                },
            },
            cash_balance=50.0,
        )

        self.assertEqual(portfolio_state.daily_loss_count, 1)
        self.assertEqual(portfolio_state.consecutive_losses, 1)
        self.assertEqual(len(portfolio_state.open_positions), 1)
        self.assertEqual(portfolio_state.total_exposure, 230.0)


if __name__ == "__main__":
    unittest.main()

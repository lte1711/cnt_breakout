from __future__ import annotations

import unittest

from src.models.strategy_performance import StrategyPerformance
from src.models.strategy_signal import StrategySignal
from src.portfolio.signal_ranker import rank_signals
from src.risk.exit_models import ExitModel


def _signal(
    strategy_name: str,
    confidence: float,
    *,
    market_state: str = "TREND_UP",
    volatility_state: str = "HIGH",
) -> StrategySignal:
    return StrategySignal(
        strategy_name=strategy_name,
        symbol="ETHUSDT",
        signal_timestamp=0.0,
        signal_age_limit_sec=15.0,
        entry_allowed=True,
        side="BUY",
        trigger="TEST",
        reason="ok",
        confidence=confidence,
        market_state=market_state,
        volatility_state=volatility_state,
        entry_price_hint=2300.0,
        exit_model=ExitModel(stop_price=2290.0, target_price=2310.0),
    )


class SignalRankerTests(unittest.TestCase):
    def test_ranker_uses_static_fallback_when_sample_is_insufficient(self) -> None:
        breakout = _signal("breakout_v1", 0.60)
        pullback = _signal("pullback_v1", 0.60)

        selection = rank_signals(
            [pullback, breakout],
            {
                "breakout_v1": StrategyPerformance(strategy_name="breakout_v1", trades_closed=1, expectancy=0.5),
                "pullback_v1": StrategyPerformance(strategy_name="pullback_v1", trades_closed=1, expectancy=2.0),
            },
        )

        self.assertIsNotNone(selection.selected_signal)
        self.assertEqual(selection.selected_signal.strategy_name, "breakout_v1")
        self.assertTrue(selection.rank_score_components.get("fallback_static_only"))

    def test_ranker_prefers_expectancy_adjusted_signal_when_sample_is_sufficient(self) -> None:
        breakout = _signal("breakout_v1", 0.60)
        pullback = _signal("pullback_v1", 0.60)

        selection = rank_signals(
            [breakout, pullback],
            {
                "breakout_v1": StrategyPerformance(
                    strategy_name="breakout_v1",
                    trades_closed=6,
                    wins=2,
                    losses=4,
                    expectancy=0.01,
                    confidence_multiplier=1.0,
                ),
                "pullback_v1": StrategyPerformance(
                    strategy_name="pullback_v1",
                    trades_closed=6,
                    wins=5,
                    losses=1,
                    expectancy=0.20,
                    confidence_multiplier=1.0,
                ),
            },
        )

        self.assertIsNotNone(selection.selected_signal)
        self.assertEqual(selection.selected_signal.strategy_name, "pullback_v1")
        self.assertFalse(selection.rank_score_components.get("fallback_static_only"))
        self.assertGreater(selection.rank_score_components.get("expectancy_weighted_score", 0.0), 0.0)


if __name__ == "__main__":
    unittest.main()

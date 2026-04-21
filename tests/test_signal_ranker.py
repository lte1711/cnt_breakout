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
    def test_ranker_applies_soft_sample_confidence_before_full_confidence(self) -> None:
        breakout = _signal("breakout_v1", 0.60)
        pullback = _signal("pullback_v1", 0.60)

        selection = rank_signals(
            [pullback, breakout],
            {
                "breakout_v1": StrategyPerformance(
                    strategy_name="breakout_v1",
                    trades_closed=2,
                    wins=1,
                    losses=1,
                    avg_win=0.015,
                    avg_loss=0.010,
                    win_rate=0.5,
                    expectancy=0.002,
                    profit_factor=1.5,
                ),
                "pullback_v1": StrategyPerformance(
                    strategy_name="pullback_v1",
                    trades_closed=2,
                    wins=1,
                    losses=1,
                    avg_win=0.012,
                    avg_loss=0.012,
                    win_rate=0.5,
                    expectancy=0.0,
                    profit_factor=1.0,
                ),
            },
        )

        self.assertIsNotNone(selection.selected_signal)
        self.assertEqual(selection.selected_signal.strategy_name, "breakout_v1")
        self.assertTrue(selection.rank_score_components.get("fallback_static_only"))
        self.assertGreater(selection.rank_score_components.get("sample_confidence", 0.0), 0.0)
        self.assertGreater(selection.rank_score_components.get("expectancy_weighted_score", 0.0), 0.0)
        self.assertEqual(selection.total_signals, 2)
        self.assertEqual(selection.candidate_count, 2)

    def test_ranker_prefers_better_real_performance_signal_even_with_lower_static_score(self) -> None:
        breakout = _signal("breakout_v1", 0.82)
        pullback = _signal("pullback_v1", 0.74)

        selection = rank_signals(
            [breakout, pullback],
            {
                "breakout_v1": StrategyPerformance(
                    strategy_name="breakout_v1",
                    trades_closed=2,
                    wins=1,
                    losses=1,
                    avg_win=0.01392600000000084,
                    avg_loss=0.01104399999999996,
                    win_rate=0.5,
                    expectancy=0.0014410000000004402,
                    profit_factor=1.2609561752988854,
                ),
                "pullback_v1": StrategyPerformance(
                    strategy_name="pullback_v1",
                    trades_closed=17,
                    wins=10,
                    losses=7,
                    avg_win=0.013807699999999997,
                    avg_loss=0.014513714285714806,
                    win_rate=0.5882352941176471,
                    expectancy=0.0021459411764703723,
                    profit_factor=1.359079097602219,
                ),
            },
        )

        self.assertIsNotNone(selection.selected_signal)
        self.assertEqual(selection.selected_signal.strategy_name, "pullback_v1")
        self.assertFalse(selection.rank_score_components.get("fallback_static_only"))
        self.assertGreater(selection.rank_score_components.get("expectancy_weighted_score", 0.0), 0.0)
        self.assertGreater(selection.rank_score_components.get("win_rate_weighted_score", 0.0), 0.0)
        self.assertGreater(selection.rank_score_components.get("profit_factor_weighted_score", 0.0), 0.0)
        self.assertEqual(len(selection.candidate_details), 2)

    def test_ranker_records_rejected_reasons_when_no_candidate_exists(self) -> None:
        blocked_signal = StrategySignal(
            strategy_name="breakout_v1",
            symbol="ETHUSDT",
            signal_timestamp=0.0,
            signal_age_limit_sec=15.0,
            entry_allowed=False,
            side="NONE",
            trigger="NONE",
            reason="atr_not_expanded",
            confidence=0.0,
            market_state="RANGE",
            volatility_state="LOW",
            entry_price_hint=None,
            exit_model=None,
        )

        selection = rank_signals([blocked_signal], {})

        self.assertIsNone(selection.selected_signal)
        self.assertEqual(selection.no_ranked_signal_detail, "all_filtered")
        self.assertEqual(selection.rejected_reasons, {"atr_not_expanded": 1})


if __name__ == "__main__":
    unittest.main()

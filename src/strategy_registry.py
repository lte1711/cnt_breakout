from __future__ import annotations

from src.strategies.breakout_v1 import BreakoutV1Strategy
from src.strategies.mean_reversion_v1 import MeanReversionV1Strategy
from src.strategies.pullback_v1 import PullbackV1Strategy


STRATEGY_REGISTRY = {
    "breakout_v1": BreakoutV1Strategy,
    "pullback_v1": PullbackV1Strategy,
    "mean_reversion_v1": MeanReversionV1Strategy,
}

from __future__ import annotations

# breakout_v1 deactivated for data purity and validation accuracy
# from src.strategies.breakout_v1 import BreakoutV1Strategy
from src.strategies.breakout_v2 import BreakoutV2Strategy
from src.strategies.mean_reversion_v1 import MeanReversionV1Strategy
from src.strategies.pullback_v1 import PullbackV1Strategy


STRATEGY_REGISTRY = {
    # "breakout_v1": BreakoutV1Strategy,  # DEACTIVATED - noise source affecting data purity
    "breakout_v2": BreakoutV2Strategy,
    "pullback_v1": PullbackV1Strategy,
    "mean_reversion_v1": MeanReversionV1Strategy,
}

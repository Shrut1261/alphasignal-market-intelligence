from pydantic import BaseModel, Field


class ThresholdStrategyConfig(BaseModel):
    """Simple signal threshold strategy used for API demos and baseline tests."""

    buy_threshold: float = Field(default=0.55, ge=0, le=1)
    sell_threshold: float = Field(default=0.45, ge=0, le=1)
    long_weight: float = Field(default=1.0, ge=0, le=2)
    short_weight: float = Field(default=0.0, ge=-2, le=0)


def threshold_weights(
    signal_confidence: list[float],
    *,
    config: ThresholdStrategyConfig | None = None,
) -> list[float]:
    """Convert model confidence scores into target portfolio weights."""

    strategy_config = config or ThresholdStrategyConfig()
    weights: list[float] = []
    for confidence in signal_confidence:
        if confidence >= strategy_config.buy_threshold:
            weights.append(strategy_config.long_weight)
        elif confidence <= strategy_config.sell_threshold:
            weights.append(strategy_config.short_weight)
        else:
            weights.append(0.0)
    return weights

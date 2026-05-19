import pytest
from alphasignal_ml.portfolio import inverse_volatility_weights


def test_inverse_volatility_weights_favor_lower_volatility_asset() -> None:
    result = inverse_volatility_weights(
        ["aapl", "spy"],
        expected_returns=[0.12, 0.08],
        volatilities=[0.30, 0.15],
    )

    assert result.method == "inverse_volatility"
    assert result.weights[0].ticker == "AAPL"
    assert result.weights[1].weight > result.weights[0].weight
    assert sum(weight.weight for weight in result.weights) == pytest.approx(1.0)


def test_inverse_volatility_weights_rejects_non_positive_volatility() -> None:
    with pytest.raises(ValueError, match="positive"):
        inverse_volatility_weights(["SPY"], [0.08], [0.0])

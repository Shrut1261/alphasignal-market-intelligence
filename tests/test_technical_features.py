import pandas as pd
import pytest
from alphasignal_features.technical import (
    average_true_range,
    bollinger_bands,
    macd,
    on_balance_volume,
    relative_strength_index,
    simple_returns,
)


def test_simple_returns() -> None:
    close = pd.Series([100.0, 110.0, 99.0])

    returns = simple_returns(close)

    assert returns.iloc[1] == pytest.approx(0.1)
    assert round(float(returns.iloc[2]), 3) == -0.1


def test_relative_strength_index_bounds() -> None:
    close = pd.Series([100.0 + index for index in range(30)])

    rsi = relative_strength_index(close)

    assert rsi.dropna().between(0, 100).all()
    assert rsi.name == "rsi_14"


def test_macd_returns_expected_columns() -> None:
    close = pd.Series([100.0 + index for index in range(40)])

    features = macd(close)

    assert list(features.columns) == ["macd", "macd_signal", "macd_histogram"]
    assert len(features) == len(close)


def test_bollinger_bands_returns_expected_columns() -> None:
    close = pd.Series([100.0 + index for index in range(30)])

    features = bollinger_bands(close)

    assert "bb_percent_b" in features.columns
    assert features["bb_middle"].isna().sum() == 19


def test_average_true_range_is_non_negative() -> None:
    high = pd.Series([11.0, 12.0, 13.0, 14.0, 15.0])
    low = pd.Series([9.0, 10.0, 11.0, 12.0, 13.0])
    close = pd.Series([10.0, 11.0, 12.0, 13.0, 14.0])

    atr = average_true_range(high, low, close, window=3)

    assert atr.dropna().ge(0).all()


def test_on_balance_volume_accumulates_directional_volume() -> None:
    close = pd.Series([10.0, 11.0, 10.0, 10.5])
    volume = pd.Series([100, 200, 300, 400])

    obv = on_balance_volume(close, volume)

    assert obv.tolist() == [0, 200, -100, 300]

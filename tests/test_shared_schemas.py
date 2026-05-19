from datetime import UTC, datetime

import pytest
from alphasignal_shared.schemas import OHLCVBar, SignalDirection, TradingSignal
from pydantic import ValidationError


def test_ohlcv_bar_normalizes_ticker() -> None:
    bar = OHLCVBar(
        ticker=" spy ",
        ts=datetime.now(tz=UTC),
        open=100,
        high=101,
        low=99,
        close=100.5,
        volume=1_000_000,
        source="unit-test",
    )

    assert bar.ticker == "SPY"


def test_ohlcv_rejects_negative_close() -> None:
    with pytest.raises(ValidationError):
        OHLCVBar(
            ticker="SPY",
            ts=datetime.now(tz=UTC),
            open=100,
            high=101,
            low=99,
            close=-1,
            volume=1_000_000,
            source="unit-test",
        )


def test_trading_signal_confidence_bounds() -> None:
    signal = TradingSignal(
        ticker="msft",
        direction=SignalDirection.BUY,
        confidence=0.85,
        horizon_days=5,
        model_name="unit-test",
        generated_at=datetime.now(tz=UTC),
    )

    assert signal.ticker == "MSFT"

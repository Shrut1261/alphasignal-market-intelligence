from datetime import UTC, datetime

from alphasignal_shared.schemas import SignalDirection, TradingSignal
from fastapi import APIRouter

router = APIRouter()


@router.get("/{ticker}", response_model=TradingSignal)
async def get_latest_signal(ticker: str) -> TradingSignal:
    """Return a deterministic placeholder signal until the ML service is wired in."""

    return TradingSignal(
        ticker=ticker,
        direction=SignalDirection.HOLD,
        confidence=0.5,
        horizon_days=5,
        model_name="phase0_baseline",
        generated_at=datetime.now(tz=UTC),
    )

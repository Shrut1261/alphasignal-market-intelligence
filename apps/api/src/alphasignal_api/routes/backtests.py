from alphasignal_backtest.engine import BacktestResult, run_vector_backtest
from alphasignal_backtest.strategies import threshold_weights
from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()


class BacktestRequest(BaseModel):
    strategy_name: str = Field(default="threshold_signal")
    returns: list[float] = Field(min_length=1)
    signal_confidence: list[float] = Field(min_length=1)
    initial_cash: float = Field(default=100_000.0, gt=0)
    transaction_cost_bps: float = Field(default=1.0, ge=0)


@router.post("", response_model=BacktestResult)
async def run_backtest(request: BacktestRequest) -> BacktestResult:
    weights = threshold_weights(request.signal_confidence)
    return run_vector_backtest(
        strategy_name=request.strategy_name,
        asset_returns=request.returns,
        target_weights=weights,
        initial_cash=request.initial_cash,
        transaction_cost_bps=request.transaction_cost_bps,
    )

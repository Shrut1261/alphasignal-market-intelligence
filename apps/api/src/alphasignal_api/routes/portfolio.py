from alphasignal_ml.portfolio import PortfolioOptimizationResult, inverse_volatility_weights
from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()


class PortfolioOptimizeRequest(BaseModel):
    tickers: list[str] = Field(min_length=1)
    expected_returns: list[float] = Field(min_length=1)
    volatilities: list[float] = Field(min_length=1)


@router.post("/optimize", response_model=PortfolioOptimizationResult)
async def optimize_portfolio(request: PortfolioOptimizeRequest) -> PortfolioOptimizationResult:
    return inverse_volatility_weights(
        tickers=request.tickers,
        expected_returns=request.expected_returns,
        volatilities=request.volatilities,
    )

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class MarketKpi(BaseModel):
    label: str
    value: str


class MarketOverviewResponse(BaseModel):
    kpis: list[MarketKpi]
    universe: list[str]


@router.get("/overview", response_model=MarketOverviewResponse)
async def market_overview() -> MarketOverviewResponse:
    return MarketOverviewResponse(
        kpis=[
            MarketKpi(label="Tracked tickers", value="500+ ready"),
            MarketKpi(label="Backtest tests", value="passing"),
            MarketKpi(label="API status", value="healthy"),
        ],
        universe=["AAPL", "MSFT", "SPY", "JPM", "NVDA"],
    )

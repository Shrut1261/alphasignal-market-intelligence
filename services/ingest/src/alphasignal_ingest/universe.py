from alphasignal_shared.schemas import AssetClass
from pydantic import BaseModel, Field


class TickerDefinition(BaseModel):
    ticker: str = Field(min_length=1, max_length=20)
    name: str = Field(min_length=1)
    asset_class: AssetClass
    sector: str | None = None


DEFAULT_UNIVERSE: tuple[TickerDefinition, ...] = (
    TickerDefinition(
        ticker="AAPL",
        name="Apple Inc.",
        asset_class=AssetClass.EQUITY,
        sector="Technology",
    ),
    TickerDefinition(
        ticker="MSFT",
        name="Microsoft Corp.",
        asset_class=AssetClass.EQUITY,
        sector="Technology",
    ),
    TickerDefinition(
        ticker="SPY",
        name="SPDR S&P 500 ETF Trust",
        asset_class=AssetClass.ETF,
        sector=None,
    ),
)

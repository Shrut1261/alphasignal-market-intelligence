from datetime import datetime
from enum import StrEnum
from typing import Self

from pydantic import BaseModel, Field, field_validator, model_validator


class AssetClass(StrEnum):
    EQUITY = "equity"
    ETF = "etf"
    CRYPTO = "crypto"
    MACRO = "macro"


class SignalDirection(StrEnum):
    BUY = "buy"
    HOLD = "hold"
    SELL = "sell"


class DataProvider(StrEnum):
    YAHOO = "yahoo"
    FRED = "fred"
    NEWS_API = "news_api"
    FINNHUB = "finnhub"
    REDDIT = "reddit"


class OHLCVBar(BaseModel):
    ticker: str = Field(min_length=1, max_length=20)
    ts: datetime
    open: float = Field(gt=0)
    high: float = Field(gt=0)
    low: float = Field(gt=0)
    close: float = Field(gt=0)
    adjusted_close: float | None = Field(default=None, gt=0)
    volume: int = Field(ge=0)
    source: str = Field(min_length=1)

    @field_validator("ticker")
    @classmethod
    def normalize_ticker(cls, value: str) -> str:
        return value.strip().upper()

    @model_validator(mode="after")
    def price_range_must_be_valid(self) -> Self:
        if self.high < self.low:
            msg = "high must be greater than or equal to low"
            raise ValueError(msg)
        if not self.low <= self.open <= self.high:
            msg = "open must be inside the low/high range"
            raise ValueError(msg)
        if not self.low <= self.close <= self.high:
            msg = "close must be inside the low/high range"
            raise ValueError(msg)
        return self


class TradingSignal(BaseModel):
    ticker: str = Field(min_length=1, max_length=20)
    direction: SignalDirection
    confidence: float = Field(ge=0, le=1)
    horizon_days: int = Field(ge=1, le=252)
    model_name: str = Field(min_length=1)
    generated_at: datetime

    @field_validator("ticker")
    @classmethod
    def normalize_ticker(cls, value: str) -> str:
        return value.strip().upper()


class MacroObservation(BaseModel):
    series_id: str = Field(min_length=1, max_length=50)
    observed_at: datetime
    value: float
    source: DataProvider

    @field_validator("series_id")
    @classmethod
    def normalize_series_id(cls, value: str) -> str:
        return value.strip().upper()


class NewsArticle(BaseModel):
    ticker: str = Field(min_length=1, max_length=20)
    published_at: datetime
    source: str = Field(min_length=1)
    headline: str = Field(min_length=1)
    url: str | None = None

    @field_validator("ticker")
    @classmethod
    def normalize_ticker(cls, value: str) -> str:
        return value.strip().upper()

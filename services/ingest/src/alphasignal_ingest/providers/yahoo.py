from collections.abc import Sequence
from datetime import UTC, datetime
from typing import Any, cast

import httpx
from alphasignal_shared.schemas import OHLCVBar
from loguru import logger


class YahooChartClient:
    """Small async adapter for Yahoo Finance chart data."""

    def __init__(
        self,
        *,
        base_url: str = "https://query1.finance.yahoo.com",
        timeout_seconds: float = 20.0,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout_seconds = timeout_seconds
        self._client = client

    async def fetch_daily_bars(
        self,
        ticker: str,
        *,
        range_: str = "1y",
        interval: str = "1d",
    ) -> list[OHLCVBar]:
        symbol = ticker.strip().upper()
        url = f"{self._base_url}/v8/finance/chart/{symbol}"
        params = {"range": range_, "interval": interval, "includeAdjustedClose": "true"}

        logger.bind(ticker=symbol, provider="yahoo").info("Fetching market bars")
        if self._client is not None:
            response = await self._client.get(url, params=params)
        else:
            async with httpx.AsyncClient(timeout=self._timeout_seconds) as client:
                response = await client.get(url, params=params)

        response.raise_for_status()
        return self._parse_chart_response(symbol, response.json())

    def _parse_chart_response(self, ticker: str, payload: dict[str, Any]) -> list[OHLCVBar]:
        result = payload.get("chart", {}).get("result") or []
        if not result:
            return []

        chart = result[0]
        timestamps = chart.get("timestamp") or []
        quote = (chart.get("indicators", {}).get("quote") or [{}])[0]
        adjusted = (chart.get("indicators", {}).get("adjclose") or [{}])[0].get("adjclose") or []

        bars: list[OHLCVBar] = []
        for index, unix_ts in enumerate(timestamps):
            open_price = _float_at(quote.get("open"), index)
            high = _float_at(quote.get("high"), index)
            low = _float_at(quote.get("low"), index)
            close = _float_at(quote.get("close"), index)
            volume = _int_at(quote.get("volume"), index)
            if open_price is None or high is None or low is None or close is None or volume is None:
                continue

            bars.append(
                OHLCVBar(
                    ticker=ticker,
                    ts=datetime.fromtimestamp(int(unix_ts), tz=UTC),
                    open=open_price,
                    high=high,
                    low=low,
                    close=close,
                    adjusted_close=_float_at(adjusted, index),
                    volume=volume,
                    source="yahoo",
                )
            )

        return bars


def _value_at(values: object, index: int) -> object | None:
    if not isinstance(values, Sequence) or isinstance(values, str):
        return None
    if values is None or index >= len(values):
        return None
    return cast(object, values[index])


def _float_at(values: object, index: int) -> float | None:
    value = _value_at(values, index)
    if value is None:
        return None
    return float(cast(float | int | str, value))


def _int_at(values: object, index: int) -> int | None:
    value = _value_at(values, index)
    if value is None:
        return None
    return int(cast(float | int | str, value))

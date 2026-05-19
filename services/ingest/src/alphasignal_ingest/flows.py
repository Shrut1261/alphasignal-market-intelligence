from dataclasses import dataclass

from alphasignal_shared.schemas import MacroObservation, OHLCVBar
from loguru import logger

from alphasignal_ingest.providers.fred import FredClient
from alphasignal_ingest.providers.yahoo import YahooChartClient


@dataclass(frozen=True)
class IngestionBatch:
    market_bars: list[OHLCVBar]
    macro_observations: list[MacroObservation]


async def run_daily_ingestion(
    *,
    tickers: list[str],
    macro_series: list[str],
    yahoo_client: YahooChartClient,
    fred_client: FredClient,
) -> IngestionBatch:
    """Run the daily ingestion workflow.

    This function is intentionally framework-light so it can run in tests, from a CLI,
    or inside Prefect tasks without changing the business logic.
    """

    market_bars: list[OHLCVBar] = []
    for ticker in tickers:
        bars = await yahoo_client.fetch_daily_bars(ticker)
        logger.bind(ticker=ticker, rows=len(bars)).info("Fetched ticker bars")
        market_bars.extend(bars)

    macro_observations: list[MacroObservation] = []
    for series_id in macro_series:
        observations = await fred_client.fetch_observations(series_id)
        logger.bind(series_id=series_id, rows=len(observations)).info("Fetched macro observations")
        macro_observations.extend(observations)

    return IngestionBatch(
        market_bars=market_bars,
        macro_observations=macro_observations,
    )

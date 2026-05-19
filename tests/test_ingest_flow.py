from datetime import UTC, datetime

from alphasignal_ingest.flows import run_daily_ingestion
from alphasignal_shared.schemas import DataProvider, MacroObservation, OHLCVBar


class StubYahooClient:
    async def fetch_daily_bars(self, ticker: str) -> list[OHLCVBar]:
        return [
            OHLCVBar(
                ticker=ticker,
                ts=datetime.now(tz=UTC),
                open=100,
                high=101,
                low=99,
                close=100.5,
                volume=1000,
                source="stub",
            )
        ]


class StubFredClient:
    async def fetch_observations(self, series_id: str) -> list[MacroObservation]:
        return [
            MacroObservation(
                series_id=series_id,
                observed_at=datetime.now(tz=UTC),
                value=4.2,
                source=DataProvider.FRED,
            )
        ]


async def test_run_daily_ingestion_batches_provider_results() -> None:
    batch = await run_daily_ingestion(
        tickers=["AAPL", "MSFT"],
        macro_series=["DGS10"],
        yahoo_client=StubYahooClient(),  # type: ignore[arg-type]
        fred_client=StubFredClient(),  # type: ignore[arg-type]
    )

    assert len(batch.market_bars) == 2
    assert len(batch.macro_observations) == 1

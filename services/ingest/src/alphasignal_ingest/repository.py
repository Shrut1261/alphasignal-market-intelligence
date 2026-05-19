from collections.abc import Iterable

from alphasignal_shared.schemas import MacroObservation, OHLCVBar
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class IngestionRepository:
    """Database writes for normalized ingestion records."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def upsert_ohlcv(self, bars: Iterable[OHLCVBar]) -> int:
        rows = [
            {
                "ticker": bar.ticker,
                "ts": bar.ts,
                "open": bar.open,
                "high": bar.high,
                "low": bar.low,
                "close": bar.close,
                "adjusted_close": bar.adjusted_close,
                "volume": bar.volume,
                "source": bar.source,
            }
            for bar in bars
        ]
        if not rows:
            return 0

        await self._session.execute(
            text("""
                INSERT INTO fact_ohlcv (
                    ticker, ts, open, high, low, close, adjusted_close, volume, source
                )
                VALUES (
                    :ticker, :ts, :open, :high, :low, :close, :adjusted_close, :volume, :source
                )
                ON CONFLICT (ticker, ts, source) DO UPDATE SET
                    open = EXCLUDED.open,
                    high = EXCLUDED.high,
                    low = EXCLUDED.low,
                    close = EXCLUDED.close,
                    adjusted_close = EXCLUDED.adjusted_close,
                    volume = EXCLUDED.volume,
                    ingested_at = NOW()
                """),
            rows,
        )
        return len(rows)

    async def upsert_macro_observations(self, observations: Iterable[MacroObservation]) -> int:
        rows = [
            {
                "series_id": observation.series_id,
                "observed_at": observation.observed_at,
                "value": observation.value,
                "source": observation.source.value,
            }
            for observation in observations
        ]
        if not rows:
            return 0

        await self._session.execute(
            text("""
                INSERT INTO fact_macro_observation (series_id, observed_at, value, source)
                VALUES (:series_id, :observed_at, :value, :source)
                ON CONFLICT (series_id, observed_at, source) DO UPDATE SET
                    value = EXCLUDED.value,
                    ingested_at = NOW()
                """),
            rows,
        )
        return len(rows)

from datetime import UTC, datetime
from typing import Any

import httpx
from alphasignal_shared.schemas import DataProvider, MacroObservation
from loguru import logger


class FredClient:
    """Async adapter for FRED observations."""

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = "https://api.stlouisfed.org/fred",
        timeout_seconds: float = 20.0,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._timeout_seconds = timeout_seconds
        self._client = client

    async def fetch_observations(
        self,
        series_id: str,
        *,
        observation_start: str | None = None,
    ) -> list[MacroObservation]:
        normalized_series = series_id.strip().upper()
        params = {
            "series_id": normalized_series,
            "api_key": self._api_key,
            "file_type": "json",
        }
        if observation_start:
            params["observation_start"] = observation_start

        logger.bind(series_id=normalized_series, provider="fred").info(
            "Fetching macro observations"
        )
        if self._client is not None:
            response = await self._client.get(
                f"{self._base_url}/series/observations",
                params=params,
            )
        else:
            async with httpx.AsyncClient(timeout=self._timeout_seconds) as client:
                response = await client.get(f"{self._base_url}/series/observations", params=params)

        response.raise_for_status()
        return self._parse_observations(normalized_series, response.json())

    def _parse_observations(
        self,
        series_id: str,
        payload: dict[str, Any],
    ) -> list[MacroObservation]:
        observations: list[MacroObservation] = []
        for item in payload.get("observations", []):
            raw_value = item.get("value")
            if raw_value in (None, "."):
                continue
            observations.append(
                MacroObservation(
                    series_id=series_id,
                    observed_at=datetime.fromisoformat(item["date"]).replace(tzinfo=UTC),
                    value=float(raw_value),
                    source=DataProvider.FRED,
                )
            )
        return observations

"""External provider adapters for ingestion."""

from alphasignal_ingest.providers.fred import FredClient
from alphasignal_ingest.providers.yahoo import YahooChartClient

__all__ = ["FredClient", "YahooChartClient"]

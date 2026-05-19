import json

import httpx
from alphasignal_ingest.providers.fred import FredClient
from alphasignal_ingest.providers.yahoo import YahooChartClient


async def test_yahoo_chart_client_parses_daily_bars() -> None:
    payload = {
        "chart": {
            "result": [
                {
                    "timestamp": [1_704_067_200],
                    "indicators": {
                        "quote": [
                            {
                                "open": [100.0],
                                "high": [102.0],
                                "low": [99.0],
                                "close": [101.0],
                                "volume": [1_000_000],
                            }
                        ],
                        "adjclose": [{"adjclose": [100.5]}],
                    },
                }
            ]
        }
    }

    transport = httpx.MockTransport(lambda _: httpx.Response(200, json=payload))
    async with httpx.AsyncClient(transport=transport) as client:
        bars = await YahooChartClient(client=client).fetch_daily_bars("aapl")

    assert len(bars) == 1
    assert bars[0].ticker == "AAPL"
    assert bars[0].close == 101.0
    assert bars[0].source == "yahoo"


async def test_yahoo_chart_client_skips_incomplete_bars() -> None:
    payload = {
        "chart": {
            "result": [
                {
                    "timestamp": [1_704_067_200],
                    "indicators": {
                        "quote": [
                            {
                                "open": [100.0],
                                "high": [None],
                                "low": [99.0],
                                "close": [101.0],
                                "volume": [1_000_000],
                            }
                        ]
                    },
                }
            ]
        }
    }

    transport = httpx.MockTransport(lambda _: httpx.Response(200, json=payload))
    async with httpx.AsyncClient(transport=transport) as client:
        bars = await YahooChartClient(client=client).fetch_daily_bars("aapl")

    assert bars == []


async def test_fred_client_parses_observations() -> None:
    payload = {
        "observations": [
            {"date": "2024-01-01", "value": "4.25"},
            {"date": "2024-01-02", "value": "."},
        ]
    }

    transport = httpx.MockTransport(lambda _: httpx.Response(200, content=json.dumps(payload)))
    async with httpx.AsyncClient(transport=transport) as client:
        observations = await FredClient("fake-key", client=client).fetch_observations("dgs10")

    assert len(observations) == 1
    assert observations[0].series_id == "DGS10"
    assert observations[0].value == 4.25
    assert observations[0].source.value == "fred"

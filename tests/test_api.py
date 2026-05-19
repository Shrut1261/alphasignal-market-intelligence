from alphasignal_api.main import app
from fastapi.testclient import TestClient


def test_health_check() -> None:
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_latest_signal_normalizes_ticker() -> None:
    client = TestClient(app)

    response = client.get("/signals/aapl")

    assert response.status_code == 200
    assert response.json()["ticker"] == "AAPL"
    assert response.json()["direction"] == "hold"


def test_backtest_endpoint_returns_metrics() -> None:
    client = TestClient(app)

    response = client.post(
        "/backtests",
        json={
            "returns": [0.01, -0.002, 0.004],
            "signal_confidence": [0.6, 0.7, 0.5],
        },
    )

    assert response.status_code == 200
    assert response.json()["strategy_name"] == "threshold_signal"
    assert "sharpe_ratio" in response.json()["metrics"]


def test_sentiment_endpoint_scores_headline() -> None:
    client = TestClient(app)

    response = client.post(
        "/sentiment/aapl",
        json={"headline": "Apple beats expectations as profit growth accelerates"},
    )

    assert response.status_code == 200
    assert response.json()["label"] == "positive"


def test_portfolio_optimize_endpoint_returns_weights() -> None:
    client = TestClient(app)

    response = client.post(
        "/portfolio/optimize",
        json={
            "tickers": ["AAPL", "SPY"],
            "expected_returns": [0.12, 0.08],
            "volatilities": [0.3, 0.15],
        },
    )

    assert response.status_code == 200
    assert response.json()["method"] == "inverse_volatility"
    assert len(response.json()["weights"]) == 2

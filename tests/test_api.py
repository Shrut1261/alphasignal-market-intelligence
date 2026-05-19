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

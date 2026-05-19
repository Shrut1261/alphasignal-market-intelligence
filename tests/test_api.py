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

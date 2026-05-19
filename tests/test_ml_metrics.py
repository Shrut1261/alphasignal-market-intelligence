import pytest
from alphasignal_ml.metrics import classification_metrics


def test_classification_metrics() -> None:
    metrics = classification_metrics(["up", "down", "flat"], ["up", "up", "flat"])

    assert metrics.accuracy == pytest.approx(2 / 3)
    assert metrics.directional_accuracy == pytest.approx(0.5)
    assert metrics.support == 3


def test_classification_metrics_rejects_mismatched_inputs() -> None:
    with pytest.raises(ValueError, match="same length"):
        classification_metrics(["up"], ["up", "down"])

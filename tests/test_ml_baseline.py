import pytest
from alphasignal_ml.baseline import RuleBasedDirectionalModel, majority_class_baseline


def test_rule_based_directional_model() -> None:
    model = RuleBasedDirectionalModel()

    assert model.predict([0.01, -0.01, 0.0]) == ["up", "down", "flat"]


def test_majority_class_baseline() -> None:
    assert majority_class_baseline(["up", "up", "down"]) == "up"


def test_majority_class_baseline_rejects_empty_labels() -> None:
    with pytest.raises(ValueError, match="must not be empty"):
        majority_class_baseline([])

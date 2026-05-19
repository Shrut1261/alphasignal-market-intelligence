from collections import Counter
from dataclasses import dataclass


@dataclass(frozen=True)
class RuleBasedDirectionalModel:
    """A deterministic directional baseline used before LightGBM training is enabled."""

    positive_threshold: float = 0.0025
    negative_threshold: float = -0.0025

    def predict_one(self, expected_return: float) -> str:
        if expected_return >= self.positive_threshold:
            return "up"
        if expected_return <= self.negative_threshold:
            return "down"
        return "flat"

    def predict(self, expected_returns: list[float]) -> list[str]:
        return [self.predict_one(expected_return) for expected_return in expected_returns]


def majority_class_baseline(labels: list[str]) -> str:
    """Return the most common label for benchmark comparisons."""

    if not labels:
        msg = "labels must not be empty"
        raise ValueError(msg)
    return Counter(labels).most_common(1)[0][0]

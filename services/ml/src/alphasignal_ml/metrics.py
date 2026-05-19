from collections.abc import Sequence

from pydantic import BaseModel, Field


class ClassificationMetrics(BaseModel):
    accuracy: float = Field(ge=0, le=1)
    directional_accuracy: float = Field(ge=0, le=1)
    support: int = Field(ge=0)


def classification_metrics(
    actual: Sequence[str],
    predicted: Sequence[str],
    *,
    neutral_label: str = "flat",
) -> ClassificationMetrics:
    """Compute lightweight classification metrics for directional models."""

    if len(actual) != len(predicted):
        msg = "actual and predicted must have the same length"
        raise ValueError(msg)
    if not actual:
        return ClassificationMetrics(accuracy=0.0, directional_accuracy=0.0, support=0)

    exact_matches = sum(a == p for a, p in zip(actual, predicted, strict=True))
    directional_pairs = [
        (a, p)
        for a, p in zip(actual, predicted, strict=True)
        if a != neutral_label and p != neutral_label
    ]
    directional_matches = sum(a == p for a, p in directional_pairs)
    directional_accuracy = (
        directional_matches / len(directional_pairs) if directional_pairs else 0.0
    )

    return ClassificationMetrics(
        accuracy=exact_matches / len(actual),
        directional_accuracy=directional_accuracy,
        support=len(actual),
    )

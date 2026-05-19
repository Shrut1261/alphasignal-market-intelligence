from enum import StrEnum

from pydantic import BaseModel, Field


class SentimentLabel(StrEnum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


class SentimentScore(BaseModel):
    label: SentimentLabel
    score: float = Field(ge=-1, le=1)
    model_name: str


def neutral_score(model_name: str = "phase0_neutral") -> SentimentScore:
    return SentimentScore(label=SentimentLabel.NEUTRAL, score=0.0, model_name=model_name)


POSITIVE_TERMS = frozenset(
    {
        "beat",
        "beats",
        "bullish",
        "growth",
        "outperform",
        "profit",
        "rally",
        "record",
        "upgrade",
    }
)
NEGATIVE_TERMS = frozenset(
    {
        "bearish",
        "cut",
        "downgrade",
        "loss",
        "miss",
        "probe",
        "risk",
        "selloff",
        "warning",
    }
)


def lexical_sentiment_score(
    text: str, *, model_name: str = "lexical_baseline_v1"
) -> SentimentScore:
    """Score financial text with a deterministic baseline before FinBERT is wired in."""

    tokens = {token.strip(".,:;!?()[]{}\"'").lower() for token in text.split()}
    positive_hits = len(tokens & POSITIVE_TERMS)
    negative_hits = len(tokens & NEGATIVE_TERMS)
    total_hits = positive_hits + negative_hits
    if total_hits == 0:
        return neutral_score(model_name=model_name)

    score = (positive_hits - negative_hits) / total_hits
    if score > 0:
        label = SentimentLabel.POSITIVE
    elif score < 0:
        label = SentimentLabel.NEGATIVE
    else:
        label = SentimentLabel.NEUTRAL
    return SentimentScore(label=label, score=score, model_name=model_name)

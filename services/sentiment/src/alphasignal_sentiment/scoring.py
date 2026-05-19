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

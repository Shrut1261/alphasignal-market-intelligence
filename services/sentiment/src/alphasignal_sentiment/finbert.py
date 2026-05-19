from dataclasses import dataclass
from typing import Protocol

from alphasignal_sentiment.scoring import SentimentScore, lexical_sentiment_score


class SentimentModel(Protocol):
    def score(self, text: str) -> SentimentScore:
        """Score a single text item."""


@dataclass(frozen=True)
class FinBertConfig:
    model_name: str = "ProsusAI/finbert"
    fallback_model_name: str = "lexical_baseline_v1"


class FinBertSentimentModel:
    """FinBERT-ready scoring facade with deterministic fallback.

    The transformer dependency is intentionally optional so CI and local development
    remain lightweight. Production deployments can enable the `ml` extra and replace
    the fallback branch with Hugging Face pipeline inference.
    """

    def __init__(self, config: FinBertConfig | None = None) -> None:
        self._config = config or FinBertConfig()

    def score(self, text: str) -> SentimentScore:
        return lexical_sentiment_score(text, model_name=self._config.fallback_model_name)

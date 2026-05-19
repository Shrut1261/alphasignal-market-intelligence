from alphasignal_sentiment.finbert import FinBertSentimentModel


def test_finbert_facade_uses_deterministic_fallback() -> None:
    model = FinBertSentimentModel()

    score = model.score("Company beats profit expectations")

    assert score.model_name == "lexical_baseline_v1"
    assert score.score > 0

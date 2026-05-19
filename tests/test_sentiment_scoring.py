from alphasignal_sentiment.scoring import (
    SentimentLabel,
    lexical_sentiment_score,
    neutral_score,
)


def test_neutral_score() -> None:
    score = neutral_score()

    assert score.label == SentimentLabel.NEUTRAL
    assert score.score == 0


def test_lexical_sentiment_score_positive() -> None:
    score = lexical_sentiment_score("Company beats estimates and raises growth outlook")

    assert score.label == SentimentLabel.POSITIVE
    assert score.score > 0


def test_lexical_sentiment_score_negative() -> None:
    score = lexical_sentiment_score("Analyst downgrade follows profit warning and selloff")

    assert score.label == SentimentLabel.NEGATIVE
    assert score.score < 0

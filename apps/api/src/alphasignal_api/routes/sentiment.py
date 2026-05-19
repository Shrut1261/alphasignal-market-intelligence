from alphasignal_sentiment.scoring import SentimentScore, lexical_sentiment_score
from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()


class SentimentRequest(BaseModel):
    headline: str = Field(min_length=1)


@router.post("/{ticker}", response_model=SentimentScore)
async def score_ticker_headline(ticker: str, request: SentimentRequest) -> SentimentScore:
    return lexical_sentiment_score(f"{ticker} {request.headline}")

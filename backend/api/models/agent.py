from pydantic import BaseModel, Field
from typing import List, Literal

# Análise dos documentos anuais (10k)
class FundamentalAnalysis(BaseModel):
    overall_investment_thesis: str
    investment_grade: Literal["A", "B", "C", "D"]
    confidence_score: float = Field(ge=0, le=1) # maior de, menor de
    key_strengths: List[str] = Field(min_length=3, max_length=3)
    key_concerns: List[str] = Field(min_length=3, max_length=3)
    recommendation: Literal["buy", "hold", "sell", "avoid"]

# Analise dos documentos trimestrais (10Q)
class MomentumAnalysis(BaseModel):
    overall_momentum: Literal["positive", "neutral", "negative"]
    momentum_strength: Literal["strong", "moderate", "weak"]
    key_momentum_drivers: List[str] = Field(min_length=2, max_length=3)
    momentum_risks: List[str] = Field(min_length=2, max_length=3)
    short_term_outlook: Literal["bullish", "neutral", "bearish"]
    momentum_score: float = Field(ge=0, le=10)

# Analise de notícias recents
class SentimentAnalysis(BaseModel):
    sentiment_score: float = Field(ge=1, le=10)
    sentiment_direction: Literal["Positive", "Neutral", "Negative"]
    key_news_themes: List[str]
    recent_catalysts: List[str]
    market_outlook: str

# Análise final usando as anteriores
class FinalRecommendation(BaseModel):
    action: Literal["BUY", "HOLD", "SELL"]
    confidence: float = Field(ge=0, le=1)
    rationale: str
    key_risks: List[str]
    key_opportunities: List[str]
    time_horizon: Literal["Short-term", "Medium-term", "Long-term"]


class AgentRequest(BaseModel):
    query: str
    limit: int = 3


class AgentResponse(BaseModel):
    query: str
    ticker: str
    fundamental_analysis: FundamentalAnalysis
    momentum_analysis: MomentumAnalysis
    sentiment_analysis: SentimentAnalysis
    final_recommendation: FinalRecommendation
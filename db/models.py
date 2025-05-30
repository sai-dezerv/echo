from pydantic import BaseModel

class PortfolioInput(BaseModel):
    user_id: str

class StrategyInput(BaseModel):
    strategy_id: str

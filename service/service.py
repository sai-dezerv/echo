from db.db import PortfolioDB, StrategyDB
from db.models import PortfolioInput, StrategyInput

class PortfolioService:
    def __init__(self):
        self.db = PortfolioDB()

    def get_portfolio(self, input_data: PortfolioInput):
        return self.db.get_portfolio(input_data.user_id)

class StrategyService:
    def __init__(self):
        self.db = StrategyDB()

    def get_strategy(self, input_data: StrategyInput):
        return self.db.get_strategy(input_data.strategy_id)

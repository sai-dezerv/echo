from .models import PortfolioInput, StrategyInput

class PortfolioDB:
    def get_portfolio(self, user_id: str):
        # Simulate DB fetch
        return {
            "user_id": user_id,
            "portfolio_value": 100000,
            "investments": [
                {"name": "Swiggy Stock", "value": 50000},
                {"name": "Bond B", "value": 30000},
                {"name": "Real Estate C", "value": 20000}
            ]
        }

class StrategyDB:
    def get_strategy(self, strategy_id: str):
        # Simulate DB fetch
        return {
            "strategy_id": strategy_id,
            "strategy": "ERS",
            "risk_tolerance": "Medium",
            "investment_horizon": "5 years",
            "recommended_investments": [
                {"name": "Tech Fund A", "allocation": 40},
                {"name": "Bond Fund B", "allocation": 30},
                {"name": "Real Estate C", "allocation": 30}
            ]
        }

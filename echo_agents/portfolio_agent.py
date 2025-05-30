from agents import function_tool, Agent
from service.service import PortfolioService
from db.models import PortfolioInput

portfolio_service = PortfolioService()

@function_tool
def portfolio_tool(input_data: PortfolioInput):
    return portfolio_service.get_portfolio(input_data)

portfolio_agent = Agent(
    name="Portfolio Agent",
    instructions="Handles portfolio queries.",
    tools=[portfolio_tool],
    model="gpt-4o-mini",
)

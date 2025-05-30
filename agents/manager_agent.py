from agents import Agent
from agents.portfolio_agent import portfolio_agent
from agents.strategy_agent import strategy_agent

manager_agent = Agent(
    name="Manager Agent",
    instructions="Manages and delegates between portfolio and strategy agents.",
    handoffs=[
        portfolio_agent,
        strategy_agent,
    ],
    model="gpt-4o-mini",
)

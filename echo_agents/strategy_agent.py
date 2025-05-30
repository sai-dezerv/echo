from agents import function_tool, Agent
from service.service import StrategyService
from db.models import StrategyInput

strategy_service = StrategyService()

@function_tool
def strategy_tool(input_data: StrategyInput):
    return strategy_service.get_strategy(input_data)

strategy_agent = Agent(
    name="Strategy Agent",
    instructions="Handles investment strategy queries.",
    tools=[strategy_tool],
    model="gpt-4o-mini",
)

from echo_agents.portfolio_agent import portfolio_agent
from echo_agents.strategy_agent import strategy_agent
from agents import Agent

main_agent = Agent(
    name="Dezerv's Personal Financial Companion",
    instructions="""
        You are Echo, Dezerv's Personal Financial Companion. 
        Do not answer questions directly unless you have the information from the tools.
        Handoff to the appropriate agent based on the user's question.
        1. If the user asks about their portfolio, use the portfolio_agent. 
        2. If the user asks about investment strategy, use the strategy_agent.
    """,
    handoffs=[
        portfolio_agent,
        strategy_agent,
    ],
)

import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from agents import Agent, handoff, Runner, function_tool
from pydantic import BaseModel
import asyncio
import uvicorn
import json

load_dotenv()
app = FastAPI()

# Define the tool agents
class PortfolioInput(BaseModel):
    user_id: str

@function_tool
def portfolio_tool(input_data: PortfolioInput):
    """Mock function to simulate portfolio details retrieval."""
    return {
        "user_id": input_data.user_id,
        "portfolio_value": 100000,
        "investments": [
            {"name": "Swiggy Stock", "value": 50000},
            {"name": "Bond B", "value": 30000},
            {"name": "Real Estate C", "value": 20000}
        ]
    }

class StrategyInput(BaseModel):
    strategy_id: str

@function_tool
def strategy_tool(input_data: StrategyInput):
    """Mock function to simulate strategy details retrieval."""
    return {
        "strategy_id": input_data.strategy_id,
        "strategy": "ERS",
        "risk_tolerance": "Medium",
        "investment_horizon": "5 years",
        "recommended_investments": [
            {"name": "Tech Fund A", "allocation": 40},
            {"name": "Bond Fund B", "allocation": 30},
            {"name": "Real Estate C", "allocation": 30}
        ]
    }

portfolio_agent = Agent(
    name="Portfolio Agent",
    instructions="Handles portfolio queries.",
    tools=[portfolio_tool],
    model="gpt-4o-mini",
)

strategy_agent = Agent(
    name="Strategy Agent",
    instructions="Handles investment strategy queries.",
    tools=[strategy_tool],
    model="gpt-4o-mini",
)

# Main agent with handoffs
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

@app.post('/ask')
async def ask(request: Request):
    data = await request.json()
    user_question = data.get('question')
    userDataAvailable = data.get('userDataAvailable', {})
    if userDataAvailable:
        user_question += " User Data Available: " + json.dumps(userDataAvailable)
    if not user_question:
        return JSONResponse({"error": "No question provided"}, status_code=400)
    if not isinstance(user_question, str):
        return JSONResponse({"error": "Question must be a string"}, status_code=400)
    try:
        result = await call_runner(main_agent, user_question)
        print(result)
    except asyncio.CancelledError:
        return JSONResponse({"error": "Request was cancelled"}, status_code=500)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
    
    return JSONResponse(
        content={
            "question": user_question,
            "response": result.final_output
        },
        status_code=200
    )

async def call_runner(agent, question):
    """Call the agent runner with the provided question."""
    
    try:
        result = await Runner.run(agent, question, max_turns=5)
        return result
    except Exception as e:
        return {"error": str(e)}
    
if __name__ == "__main__":
    # For development, run: uvicorn app:app --reload
    pass

# Transaction statement:
# Statement Of Expense
# Capital gains Statement
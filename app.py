import os
import json
import requests
from dotenv import load_dotenv
from openai import OpenAI
from flask import Flask, request, jsonify
from pydantic import BaseModel, Field

from agents.test_agent_1 import get_weather_tool

load_dotenv()
app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.json.get('question')
    # Send the question to OpenAI with a prompt to return a structured response
    system_prompt = (
        "You are Echo, Dezerv's Personal Financial Companion."
        "You can use the following tools to answer user questions:"
        "1. portfolio_tool: Get portfolio details for a user."
        "2. strategy_tool: Get strategy details basis strategy data."
        "Use the tools to gather information and provide a structured response."
        "If the user asks about their portfolio, use the portfolio_tool to get the details."
        "Do not answer the question directly."
    )
    tools = [
        {
            "type": "function",
            "function": {
                "name": "portfolio_tool",
                "description": "Get portfolio details for a user.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The ID of the user."},
                    },
                    "required": ["user_id"],
                    "additionalProperties": False,
                },
                "strict": True,
            },
        },
        {
            "type": "function",
            "function": {
                "name": "strategy_tool",
                "description": "Get investment strategy details for a user.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "strategy_id": {"type": "string", "description": "The ID of the user."},
                    },
                    "required": ["strategy_id"],
                    "additionalProperties": False,
                },
                "strict": True,
            },
        }
    ]

    system_prompt = "You are a helpful weather assistant."

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_question},
        {"role": "assistant", "content": "Sure, I can help with that. Let me check your portfolio details."}
    ]
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
    )
    completion.model_dump()

    def call_function(name, args):
        if name == "portfolio_tool":
            print(f"Calling portfolio_tool with args: {args}")
            return portfolio_tool(**args)
        elif name == "strategy_tool":
            print(f"Calling strategy_tool with args: {args}")
            return strategy_tool(**args)
        else:
            print(f"Unknown function: {name}")
            raise ValueError(f"Unknown function: {name}")


    for tool_call in completion.choices[0].message.tool_calls:
        name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        messages.append(completion.choices[0].message)

        result = call_function(name, args)
        messages.append(
            {"role": "tool", "tool_call_id": tool_call.id, "content": json.dumps(result)}
        )

    class GenericResponse(BaseModel):
        # confidence: float = Field(
        #     description="Confidence level of the response, between 0 and 1."
        # )
        response: str = Field(
            description="A natural language response to the user's question."
        )


    completion_2 = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
        response_format=GenericResponse,
    )

    print(completion_2)

    final_response = completion_2.choices[0].message.parsed
    print("Final Response:", final_response)
    # print(final_response.confidence)
    print(final_response.response)

    return jsonify({
        # "confidence": final_response.confidence,
        "response": final_response.response
    }

)
    

def portfolio_tool(user_id):
    """Mock function to simulate portfolio details retrieval."""
    # In a real application, this would query a database or an external service.
    return {
        "user_id": user_id,
        "portfolio_value": 100000,
        "investments": [
            {"name": "Swiggy Stock", "value": 50000},
            {"name": "Bond B", "value": 30000},
            {"name": "Real Estate C", "value": 20000}
        ]
    }
    
def strategy_tool(strategy_id):
    """Mock function to simulate strategy details retrieval."""
    # In a real application, this would query a database or an external service.
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

if __name__ == "__main__":
    app.run(debug=True)

# Transaction statement:
# Statement Of Expense
# Capital gains Statement
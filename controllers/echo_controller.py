from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from echo_agents.manager_agent import main_agent 
from agents import Runner, function_tool
import json

router = APIRouter()

@router.post('/ask')
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
        result = await Runner.run(main_agent, user_question, max_turns=5)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
    return JSONResponse(
        content={
            "question": user_question,
            "response": result.final_output,
            "responseId": result.final_output,
        },
        status_code=200
    )

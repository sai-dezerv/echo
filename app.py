import os
from dotenv import load_dotenv
from fastapi import FastAPI
from controllers.echo_controller import router as echo_router

load_dotenv()
app = FastAPI()
app.include_router(echo_router)

# Transaction statement:
# Statement Of Expense
# Capital gains Statement
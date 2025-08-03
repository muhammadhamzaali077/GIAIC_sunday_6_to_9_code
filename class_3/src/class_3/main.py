import asyncio
from agents import Agent, RunConfig,Runner,set_tracing_disabled, OpenAIChatCompletionsModel
from agents.tool import function_tool
from openai import AsyncOpenAI
from pydantic import BaseModel
import pprint
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

GEMINI_MODEL :str = "gemini-2.0-flash"
GEMINI_API_KEY :str = os.getenv("GEMINI_API_KEY", "Gemini_api_key")
BASE_URL :str = "https://generativelanguage.googleapis.com/v1beta/openai/"

set_tracing_disabled(disabled=True)

client:AsyncOpenAI = AsyncOpenAI(api_key = GEMINI_API_KEY, base_url = BASE_URL)
model :OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(model= GEMINI_MODEL, openai_client = client)

class Output(BaseModel):
    type: str
    category: str
    language: str
    setup: str

agent :Agent = Agent(
    name = "Joke agent", 
    instructions = "You are a joking agent return joke in json object",
    output_type = Output
    )

async def main():
    result = await Runner.run(agent, "hello tell me a short joke in roman urdu", run_config= RunConfig(model=model) )
    pprint.pprint(result.final_output)
    print(type(result.final_output))
def start():
    asyncio.run(main())


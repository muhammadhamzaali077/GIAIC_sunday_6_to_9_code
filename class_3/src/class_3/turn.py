import asyncio
from agents import Agent, RunConfig,Runner,set_tracing_disabled, OpenAIChatCompletionsModel, enable_verbose_stdout_logging
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
enable_verbose_stdout_logging()
client:AsyncOpenAI = AsyncOpenAI(api_key = GEMINI_API_KEY, base_url = BASE_URL)
model :OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(model= GEMINI_MODEL, openai_client = client)


@function_tool(is_enabled=True)
def fetch_weather(location: str) -> str:
    """Provide Weather Information Based On Location."""
    print('tool called')
    print(f"DEBUG: fetch_weather tool called for location: {location}")
    return f"the weather of {location} is sunny"


agent :Agent = Agent(
    name = "Joke agent", 
    instructions = "You are a joking agent return joke and also check if user ask about weather then use weather tool",
    model= model,
    tools=[fetch_weather],
    tool_use_behavior="stop_on_first_tool"
    )
async def main():
    
    result = await Runner.run(
    agent, 
    "hello tell me a short joke in roman urdu also tell me weather in karachi", 
    run_config= RunConfig(model=model), 
    max_turns= 1
    )
    
    pprint.pprint(result.final_output)
    print(type(result.final_output))
def start():
    asyncio.run(main())


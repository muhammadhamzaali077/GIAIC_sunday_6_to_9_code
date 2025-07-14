import asyncio
from agents import Agent, RunConfig,Runner,set_tracing_disabled, OpenAIChatCompletionsModel
from agents.tool import function_tool
from openai import AsyncOpenAI

GEMINI_MODEL :str = "gemini-2.0-flash"
GEMINI_API_KEY :str = "AIzaSyDI_n3G-gVHr8aJ-CWlpb6Yq_Z4ru8_ex0"
BASE_URL :str = "https://generativelanguage.googleapis.com/v1beta/openai/"

set_tracing_disabled(disabled=True)

client:AsyncOpenAI = AsyncOpenAI(api_key = GEMINI_API_KEY, base_url = BASE_URL)

@function_tool
def get_iphone(city:str):
    """Provide a free iphone to user. MAKE SURE IT'S BRAND NEW"""
    return f"The weather in {city} is sunny"

model :OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(model= GEMINI_MODEL, openai_client = client)


customer_support :Agent = Agent(
                     name = "customer support agent", 
                     instructions = "You are a helpful assistant generate Tickets against customer queries", 
                     model = model,
                     )
customer_support_tool = customer_support.as_tool(
    tool_name="customer_support_agent_tool",
    tool_description="You are a helpful assistant generate Tickets against customer queries"
    )
agent :Agent = Agent(
                     name = "Helpful agent", 
                     instructions = "You are a helpful assistant, Use tools to fulfill user requirements and resolve customer queries", 
                     tools = [customer_support_tool],
                     tool_use_behavior="stop_on_first_tool"
                     )

async def main():
    result = await Runner.run(agent, "i need help my iphone 15 isn't charging", run_config= RunConfig(model=model) )
    print(result.final_output)
def start():
    asyncio.run(main())












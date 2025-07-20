###---------------INPUT GUARDRAILS---------------###
import asyncio
from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
    set_tracing_disabled
)
import asyncio
from agents import  RunConfig, OpenAIChatCompletionsModel

from openai import AsyncOpenAI


GEMINI_MODEL :str = "gemini-2.0-flash"
GEMINI_API_KEY :str = "AIzaSyCZE5ZXKCVlPntcrFPXTB6UuyACDAq0RaY"
BASE_URL :str = "https://generativelanguage.googleapis.com/v1beta/openai/"

set_tracing_disabled(disabled=True)

client:AsyncOpenAI = AsyncOpenAI(api_key = GEMINI_API_KEY, base_url = BASE_URL)
model :OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(model= GEMINI_MODEL, openai_client = client)


class MathHomeworkOutput(BaseModel):
    is_math_homework: bool
    reasoning: str

guardrail_agent = Agent( 
    name="Guardrail check",
    instructions="Check if the user is asking you to do their math homework.",
    output_type=MathHomeworkOutput,
    model=model
)


@input_guardrail
async def math_guardrail(ctx, agent, input) :
    result = await Runner.run(guardrail_agent, input, context=ctx.context)

    return GuardrailFunctionOutput(
        output_info=result.final_output, 
        tripwire_triggered= result.final_output.is_math_homework,
    )


agent = Agent(  
    name="Customer support agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    input_guardrails=[math_guardrail],
    model=model
)

async def main():
    try:
        await Runner.run(agent, "Hello, This is my Math Homework, can you help me solve for x: 2x + 3 = 11?", run_config= RunConfig(model=model))
        print("Guardrail didn't trip - this is unexpected")

    except InputGuardrailTripwireTriggered:
        print("Math homework guardrail tripped")

def start():
    asyncio.run(main())






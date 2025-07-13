import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel,function_tool
from agents.run import RunConfig
import asyncio

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

# Step 01
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Step 02
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)

# Step 03
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True,
)

@function_tool
async def weather(location: str) -> str:
    """Get the current weather for a given location."""
    # This is a placeholder implementation.
    return f"The current weather in {location} is sunny with a temperature of 25°C."

# Step 04
async def main():
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful Assistant.",
        model=model,
    )

    # Step 05
    result = await Runner.run(agent, "What is the capital of France? and tell me about weather in peshawer now", run_config=config)
    print(result.final_output)

# Step 06
if __name__ == "__main__":
    asyncio.run(main())
import asyncio
import os
from autogen_core.models import ModelFamily
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console


# Global counter state
counter = 0


def increment_counter() -> str:
    """Increment the counter by 1 and return the current value."""
    global counter
    counter += 1
    return f"Counter incremented to: {counter}"


def get_counter() -> str:
    """Get the current counter value."""
    global counter
    return f"Current counter value: {counter}"


def get_weather(city: str) -> str:
    """Get the weather for a given city."""
    return f"The weather in {city} is sunny."


async def main() -> None:
    model_client = OpenAIChatCompletionClient(
        model="qwen-plus",
        base_url=os.getenv("OPENAI_BASE_URL"),
        api_key = os.getenv("OPENAI_API_KEY"),
        enable_thinking=False,
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": False,
            "family": ModelFamily.UNKNOWN,
            "structured_output": False,
            "enable_thinking": False,
        }
    )

    # Create agent with max_tool_iterations=5 to allow multiple tool calls
    agent = AssistantAgent(
        name="assistant",
        model_client=model_client,
        tools=[increment_counter, get_counter, get_weather],
        max_tool_iterations=10,  # Allow up to 5 tool call iterations
        reflect_on_tool_use=True,  # Get a final summary after tool calls
    )

    await Console(agent.run_stream(task="Increment the counter 3 times and then tell me the final value. Also, get the weather in Tokyo."))


asyncio.run(main())

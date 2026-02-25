from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from autogen_ext.tools.code_execution import PythonCodeExecutionTool
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
import os
import asyncio

client = OpenAIChatCompletionClient(
    model="claude-4.0-sonnet",
    base_url="https://openai.qiniu.com/v1",
    api_key="",
    model_info = {
        "context_window":    131_072,
        "max_output_tokens": 16_384,
        # Interface capabilities
        "supports_stream":    True,
        "function_calling":   True,
        "json_output":        False,
        "structured_output":  False,
        # Modalities & taxonomy
        "vision":             False,
        "family":             "Kimi",
    }
)

agent = AssistantAgent(
    name = "agent",
    description = "all-mighty agent",
    model_client = client,
    model_client_stream=True,
    system_message = "You can plan, you can code, you know everything. When done say TERMINATE.",
    tools = [
        PythonCodeExecutionTool(LocalCommandLineCodeExecutor())
    ],
)

team = RoundRobinGroupChat(
    [agent],
    termination_condition = TextMentionTermination("TERMINATE") & MaxMessageTermination(200)
)

async def main(task):
    await Console(
        team.run_stream(task=task),
        output_stats=True
    )

if __name__ == "__main__":

    asyncio.run(main(task = "execute 20 short Python code examples please"))





agent = AssistantAgent(
    name = "agent",
    description = "all-mighty agent",
    model_client = client,
    model_client_stream=True,
    system_message = "You can plan, you can code, you know everything. When done say TERMINATE.",
    tools = [
        PythonCodeExecutionTool(LocalCommandLineCodeExecutor())
    ],
)
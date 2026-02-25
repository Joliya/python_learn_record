from langchain_openai import ChatOpenAI
from langchain.messages import AIMessage, SystemMessage, HumanMessage, ToolMessage

import os

from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(
    model="qwen-plus",
    api_key=os.getenv("QWEN_API_KEY"),
    base_url='https://dashscope.aliyuncs.com/compatible-mode/v1',
    temperature=0.5,
    timeout=200,
    # max_tokens=1000
)


# After a model makes a tool call
# (Here, we demonstrate manually creating the messages for brevity)
ai_message = AIMessage(
    content=[],
    tool_calls=[{
        "name": "get_weather",
        "args": {"location": "San Francisco"},
        "id": "call_123"
    }]
)

# Execute tool and create result message
weather_result = "Sunny, 72°F"
tool_message = ToolMessage(
    content=weather_result,
    tool_call_id="call_123"  # Must match the call ID
)

# Continue conversation
messages = [
    HumanMessage("What's the weather in San Francisco?"),
    ai_message,  # Model's tool call
    tool_message,  # Tool execution result
]
response = model.invoke(messages)  # Model processes the result

print(response)
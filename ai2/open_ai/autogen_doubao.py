from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from autogen_ext.tools.code_execution import PythonCodeExecutionTool
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

client = OpenAIChatCompletionClient(
    model="doubao-seed-1-8-251215",
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=os.getenv("DOUBAO_API_KEY"),
    model_info = {
        # Interface capabilities
        "supports_stream":    True,
        "function_calling":   True,
        "json_output":        False,
        # Modalities & taxonomy
        "vision":             False,
        "family":             "Doubao",
    },
    temperature=0.9,
    extra_body={
        "thinking": {"type": "enabled"},   # 关键行：关闭深度思考
        # "reasoning_effort": "high"
    },
    # reasoning={"effort": "high"}
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

async def extract_reasoning_stream(stream):
    """包装流式输出，提取并显示思考过程"""
    reasoning_content = ""
    answer_content = ""
    is_answering = False
    
    print("\n" + "="*20 + "思考过程" + "="*20 + "\n")
    
    async for event in stream:
        # 检查事件中的消息
        if hasattr(event, 'messages'):
            for message in event.messages:
                # 尝试多种方式获取 reasoning 内容
                reasoning_text = None
                
                # 方法1: 直接检查 reasoning 属性
                if hasattr(message, 'reasoning') and message.reasoning:
                    reasoning_text = message.reasoning if isinstance(message.reasoning, str) else str(message.reasoning)
                
                # 方法2: 检查 source 中的 reasoning
                elif hasattr(message, 'source'):
                    source = message.source
                    if hasattr(source, 'reasoning') and source.reasoning:
                        reasoning_text = source.reasoning if isinstance(source.reasoning, str) else str(source.reasoning)
                    elif isinstance(source, dict) and 'reasoning' in source and source['reasoning']:
                        reasoning_text = source['reasoning'] if isinstance(source['reasoning'], str) else str(source['reasoning'])
                
                # 输出思考过程
                if reasoning_text:
                    print(reasoning_text, end="", flush=True)
                    reasoning_content += reasoning_text
                    is_answering = False
                
                # 输出消息内容
                if hasattr(message, 'content') and message.content:
                    content = message.content if isinstance(message.content, str) else str(message.content)
                    if reasoning_text and not is_answering:
                        print("\n" + "="*20 + "回复内容" + "="*20 + "\n")
                        is_answering = True
                    print(content, end="", flush=True)
                    answer_content += content
        
        # 继续传递事件给下游处理
        yield event

async def main(task):
    # 创建包装后的流
    wrapped_stream = extract_reasoning_stream(team.run_stream(task=task))
    # 使用 Console 输出标准格式
    await Console(wrapped_stream, output_stats=True)

async def main_non_stream(task):
    """非流式输出版本，打印每个消息的类型"""
    print("\n" + "="*50)
    print("非流式输出模式")
    print("="*50 + "\n")
    
    # 创建非流式 agent
    agent_non_stream = AssistantAgent(
        name="agent",
        description="all-mighty agent",
        model_client=client,
        model_client_stream=False,  # 非流式
        system_message="You are a helpful assistant. Answer the question directly and concisely. When finished, say TERMINATE.",
        tools=[
            PythonCodeExecutionTool(LocalCommandLineCodeExecutor())
        ],
    )
    
    # 使用更严格的终止条件：最多10条消息或包含TERMINATE
    team_non_stream = RoundRobinGroupChat(
        [agent_non_stream],
        termination_condition=TextMentionTermination("TERMINATE") | MaxMessageTermination(10)
    )
    
    print(f"任务: {task}")
    print("开始执行...\n")
    
    try:
        # 运行非流式任务，添加超时
        result = await asyncio.wait_for(
            team_non_stream.run(task=task),
            timeout=120.0  # 2分钟超时
        )
    except asyncio.TimeoutError:
        print("\n" + "="*50)
        print("执行超时！强制终止")
        print("="*50 + "\n")
        return
    except Exception as e:
        print(f"\n执行出错: {e}")
        print(f"错误类型: {type(e)}")
        import traceback
        traceback.print_exc()
        return
    
    # 打印所有消息及其类型
    print("\n" + "="*50)
    print("消息列表（按顺序）")
    print("="*50 + "\n")
    
    # 统计事件类型
    event_types = {}
    
    for i, message in enumerate(result.messages, 1):
        message_type = type(message).__name__
        event_types[message_type] = event_types.get(message_type, 0) + 1
        
        print(f"\n[消息 {i}]")
        print(f"类型: {message_type}")
        print(f"完整类型路径: {type(message)}")
        
        # 如果是 ThoughtEvent，说明这是思考过程事件
        if message_type == "ThoughtEvent":
            print("⚠️  这是 ThoughtEvent - autogen 内部的思考过程事件")
            print("注意：ThoughtEvent 可能来自：")
            print("  1. 模型的 reasoning tokens（如果启用了 reasoning）")
            print("  2. 函数调用产生的思考过程")
            print("  3. Agent 的内部处理逻辑")
        
        # 打印消息的所有属性
        if hasattr(message, 'content'):
            content = message.content
            if isinstance(content, str):
                print(f"内容: {content}")
                # 检查是否包含终止词
                if "TERMINATE" in content.upper():
                    print("✓ 包含终止词 TERMINATE")
            else:
                print(f"内容类型: {type(content)}")
                print(f"内容: {content}")
        
        if hasattr(message, 'source'):
            print(f"来源: {message.source}")
        
        if hasattr(message, 'reasoning'):
            print(f"思考过程: {message.reasoning}")
        
        # 打印消息的所有属性名
        attrs = [attr for attr in dir(message) if not attr.startswith('_')]
        print(f"可用属性: {', '.join(attrs[:10])}...")  # 只显示前10个
    
    print("\n" + "="*50)
    print(f"总共 {len(result.messages)} 条消息")
    print("\n事件类型统计:")
    for event_type, count in event_types.items():
        print(f"  {event_type}: {count}")
    print("="*50 + "\n")
    
    print("\n" + "="*50)
    print(f"总共 {len(result.messages)} 条消息")
    print("="*50 + "\n")

if __name__ == "__main__":
    # 流式输出版本
    # asyncio.run(main(task = "execute 20 short Python code examples please"))
    
    # 非流式输出版本
    asyncio.run(main_non_stream(task = "为什么中国不是世界第一"))
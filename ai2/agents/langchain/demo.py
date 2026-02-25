from dataclasses import dataclass
from langchain.agents.structured_output import ToolStrategy
from langchain.agents import create_agent
from langchain.chat_models.base import init_chat_model
import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(
    model="qwen3.5-plus",
    api_key=os.getenv("QWEN_API_KEY"),
    base_url='https://dashscope.aliyuncs.com/compatible-mode/v1',
    temperature=0.5,
    timeout=200,
    # max_tokens=1000
)

SYSTEM_PROMPT = """
# 角色
- 你是一名医美机构的专业医美咨询师，负责识别用户问题关联的意图分类。

# 意图识别任务

## 核心要求
- 根据用户问题、引用消息、最近一次讲解产品、上下文，判断本次用户问题的意图分类
- 不需要生成真正的回复内容；只输出你对目前聊天内容下用户意图的判断结果
- **必须且只能**从下列8个预定义分类中选择一个「抽奖」，「打招呼」，「索要案例图」、「机构医院相关」、「医生相关」、「风险控制」、「无需回复」、「其他意图」，不允许创造新的分类名称
- **输出格式**：直接输出分类名称，不要使用代码块格式或添加任何前缀

## 意图分类定义

### 抽奖
- **示例**："我要抽奖"，"抽奖结果是什么","这个抽奖是不是假的","抽奖规则是什么","怎么兑现奖品"，"套餐礼价值多少钱呀？","免费做【全身超皮秒+牛奶酸】有几次机会呢？"
- **包含**：用户发送所有有关抽奖的内容

### 索要案例图  
- **示例**："有没有案例看看"，"有效果图吗","给我看看效果"
- **包含**：用户索要案例图和效果图
- **不包含**：纯技术原理咨询、操作流程咨询、产品之间的差异区别、效果保证、效果咨询（“这个效果怎么样”，“美白效果怎么样”）

### 机构医院相关
- **示例**：
  - "你们几点开门"
  - "医院地址在哪"
  - "怎么停车"
  - "我想买超皮秒，今天下单最晚哪天能约到？"
  - "想先面诊再决定做哪种光电，请问这周日下午能直接到院面诊吗？"
  - "你们的案例有授权吗"
- **包含**：
  - 营业时间
  - 地址位置
  - 交通指引
  - 联系方式
  - 停车信息
  - 案例授权
  - 路费补贴
  - 医保支付方式
  - 打板以及模特招募
  - 分期付款方式
  - 一般性的预约面诊
- **不包含**：指定医生面诊预约

### 医生相关
- **示例**："能指定医生吗"，"医生有从业证吗"，"想找女医生面诊"，"医生指定费用"
- **包含**：医生资质、指定医生、医生排班、医生操作相关
- **不包含**：一般性的面诊预约（属于机构医院相关）

### 风险控制
- **示例**："你们是黑店吧"，"要求赔偿"，"开玩笑呢？"，"糊弄鬼呢"
- **严格包含**：用户发送辱骂信息、要求赔偿
- **严格排除**：
  - 副作用（归入其他意图），例如："做黄金热拉提有什么副作用吗？会不会损伤到皮肤深层组织？"
  - 术后风险/做后风险咨询（归入其他意图）例如："有什么风险吗？","有什么缺点","有什么不良反应","我看网上有人说打热玛吉可能会烫伤，你们这个超玛吉操作安全吗？"
  - 术后症状（归入其他意图）例如："听说做完超声炮脸会肿，是真的吗？一般会肿几天？"

### 打招呼
- **示例**："你好"，"在吗"，"有人吗"
- **包含**：用户在打招呼发起对话的话术，而不是结束对话的简答话术，需要区别无需回复

### 无需回复
- **示例**："好的"，"嗯嗯"，表情符号，"习近平..."等涉政内容
- **包含**：类似哦，好的，嗯嗯知道了等；或者只有表情符号；或者问题中有涉政，涉及政府人员内容；测试性问题

### 其他意图
除了以上意图外所有意图
- **包含**：
  - 产品/项目推荐："那些适合我"，"我需要购买哪个"，"给我推荐"，"买哪个更好"，"我做 A 好还是 B 好"
  - 正品验证、验真、设备认证咨询、设备授权："是正品吗"，"有认证吗"，"注册证号"
  - 产品技术细节："多少发"，"探头是进口的吗"，"什么成分"，"工作原理"，"使用的什么产品"，"什么规格"
  - 操作流程咨询："需要敷麻药吗"，"做的时候疼吗"，"要准备什么"
  - 医保支付方式："走医保吗"，"能刷医保卡吗"
  - 分期付款咨询："支持分期吗"，"利息怎么算"
  - 价格合理性质疑："为什么这么便宜"，"价格差在哪"
  - 额外收费担心："会不会让我加钱"，"有隐形消费吗"
  - 案例/效果质疑、效果保证："P的吧"，"AI 生成的吧"，"美颜了吧"
  - 适应症和注意事项："我这种情况能做吗"，"需要忌口吗"
  - 修复和护理：包括术后修复，其他涉及到修复的问题。"做完要注意什么"，"多久能化妆"，"包含修复用的面膜吗"，"可以修复馒化吗"
  - 路费补贴："能报销路费吗"
  - 询问是否有指定项目：询问是否有某个项目/产品，"除了 A 还有 B 吗","你们有 M22吗"
  

## 模糊界限判断规则
- **面诊预约**：一般性面诊预约 → 机构医院相关；指定医生面诊 → 医生相关
- **价格相关**：购买咨询 → 其他意图；价格质疑/对比 → 其他意图
- **费用相关**：定金尾款 → 其他意图；医保分期 → 机构医院相关；
- **技术咨询**：统一归入其他意图
- **效果咨询**：要案例、看效果 → 索要案例图；效果质疑：其他意图；效果保证：其他意图；
- **风险控制**：副作用 → 其他意图；术后风险/做后风险咨询 → 其他意图；术后症状 → 其他意图；缺点 → 其他意图；哺乳期、孕期、经期 → 其他意图；

## 返回意图信息格式
直接输出分类名称，不要使用代码块格式：

其他意图

**错误格式示例（禁止使用）**：
- ```其他意图```
- ```
其他意图
```
- 意图分类名称：其他意图

"""

@dataclass
class Context:
    """Custom runtime context schema."""
    user_id: str

agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    # tools=[get_user_location, get_weather_for_location],
    context_schema=Context,
    # response_format=ToolStrategy(ResponseFormat),
    # checkpointer=checkpointer
)

# `thread_id` is a unique identifier for a given conversation.
config = {"configurable": {"thread_id": "1"}}

response = agent.invoke(
    {"messages": [{"role": "user", "content": "超声炮是什么"}]},
    config=config,
    context=Context(user_id="1")
)

print(response)
# ResponseFormat(
#     punny_response="Florida is still having a 'sun-derful' day! The sunshine is playing 'ray-dio' hits all day long! I'd say it's the perfect weather for some 'solar-bration'! If you were hoping for rain, I'm afraid that idea is all 'washed up' - the forecast remains 'clear-ly' brilliant!",
#     weather_conditions="It's always sunny in Florida!"
# )


# Note that we can continue the conversation using the same `thread_id`.
response = agent.invoke(
    {"messages": [{"role": "user", "content": "thank you!"}]},
    config=config,
    context=Context(user_id="1")
)

print(response)
# ResponseFormat(
#     punny_response="You're 'thund-erfully' welcome! It's always a 'breeze' to help you stay 'current' with the weather. I'm just 'cloud'-ing around waiting to 'shower' you with more forecasts whenever you need them. Have a 'sun-sational' day in the Florida sunshine!",
#     weather_conditions=None
# )
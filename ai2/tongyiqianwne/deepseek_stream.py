import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="deepseek-r1", # 此处以 deepseek-r1 为例，可按需更换模型名称。
    messages=[
        {'role': 'user', 'content': '9.9和9.11谁大'}
        ],
    stream=True,
    # 解除以下注释会在最后一个chunk返回Token使用量
    stream_options={"include_usage": True}
    )

# 定义完整思考过程
reasoning_content = ""
# 定义完整回复
answer_content = ""
# 判断是否结束思考过程并开始回复
is_answering = False

print("\n"+"="*20+"思考过程"+"="*20+"\n")
for chunk in completion:
    # include_usage 设置为 True 会使得最后一个chunk返回 Token 使用量，而choices为空列表，此处进行判断
    if chunk.choices == []:
        print("\n"+"="*20+"Token 使用情况"+"="*20+"\n")
        print(chunk.usage)
    # 以下为思考与回复的步骤
    else:
        # include_usage 设置为 True 时，倒数第二个chunk会不包含 reasoning_content 字段，因此需要进行判断
        if hasattr(chunk.choices[0].delta, 'reasoning_content') == False:
            pass
        else:
            # 有时可能会出现思考过程与回复皆为空的情况，此时忽略即可
            if chunk.choices[0].delta.reasoning_content == "" and chunk.choices[0].delta.content == "":
                pass
            else:
                # 如果思考结果为空，则开始打印完整回复
                if chunk.choices[0].delta.reasoning_content == "" and is_answering == False:
                    print("\n"+"="*20+"完整回复"+"="*20+"\n")
                    # 防止打印多个“完整回复”标记
                    is_answering = True
                # 如果思考过程不为空，则打印思考过程
                if chunk.choices[0].delta.reasoning_content != "":
                    print(chunk.choices[0].delta.reasoning_content,end="")
                    reasoning_content += chunk.choices[0].delta.reasoning_content
                # 如果回复不为空，则打印回复。回复一般会在思考过程结束后返回
                elif chunk.choices[0].delta.content != "":
                    print(chunk.choices[0].delta.content,end="")
                    answer_content += chunk.choices[0].delta.content

# 如果您需要打印完整思考过程与完整回复，请将以下代码解除注释后运行
# print("="*20+"完整思考过程"+"="*20+"\n")
# print(f"{reasoning_content}")
# print("="*20+"完整回复"+"="*20+"\n")
# print(f"{answer_content}")
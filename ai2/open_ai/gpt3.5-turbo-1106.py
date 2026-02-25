# import pandas as pd

# splits = {'train': 'train_datasets.jsonl', 'validation': 'validation_datasets.jsonl', 'test': 'test_datasets.jsonl'}
# df = pd.read_json("hf://datasets/FreedomIntelligence/huatuo_encyclopedia_qa/" + splits["train"], lines=True)

# print(df)



# from datasets import load_dataset

# ds = load_dataset("FreedomIntelligence/huatuo_encyclopedia_qa")


# from huggingface_hub import hf_hub_download
# import pandas as pd

# REPO_ID = "huatuo_encyclopedia_qa"
# FILENAME = "ai/data.csv"

# dataset = pd.read_csv(
#     hf_hub_download(repo_id=REPO_ID, filename=FILENAME, repo_type="dataset")
# )



from autogen_core.models import ModelFamily, ModelInfo, UserMessage


prompt = """
## 角色
- 你是一名专业的医美咨询师，负责在回复医美用户，擅长以专业性角度，口语化回复问题。
- 通用活动设置
    + 不支持核销延期，建议与机构线上核销后另预约时间到院核销；超过最大核销时间会自动退款；未核销支持原路返回；
    + 暂不支持分期贷款和医保；
    + 用户下单支付预约金，到线下核销的时候支付剩余尾款；
    + 目前暂时不招打板；
    + 限购只在本场活动商品范围内生效；

## 工具使用原则
- 优先从任务中提供的信息回答
- 只有在绝对必要时才调用工具
- 调用工具前先思考：这个工具调用是否真的必需？
- 说明调用工具的必要性

## 用户画像

## 回复要求
- 要求回复内容简洁并有深度，使用口语化表达，避免过于正式的医学术语，并且问答呈现鼓励积极性；
- 所有涉及到产品信息的问题，必须以活动信息为准；
- 句式长短结合，避免过于规整；适当进行换行便于用户阅读，不超过 3 段内容，每段内容不超过 50 个字；
- 针对本次活动产品，用户输入可能有误；需要你根据用户的输入内容进行推理；例如：范斯白，可能代指的是活动产品中的范思柏；
- 因为目前我们没有任何的医生信息，所以需要婉转的回答用户涉及医生的问题；
- 当用户咨询对比的时候，如果用户咨询的产品包含在活动售卖产品中，你的表述需要突出本次售卖产品的优势；
- 当用户咨询购买数量的时候，严格按照商品描述中的内容回复, 例如：涉及到限购，能买几份等，如果规则描述不限购，则按照规则内容进行参考回复；
- 当用户表露出担忧或者负面情绪，首先给予共情式回应，再以认真语气对用户进行解释性安抚和回复，禁止“哈哈”等不严肃的语气词；
- 如果用户咨询停车相关的问题，则回复一般都是有免费车位的，但是如果当天在院的人数较多的话就不能保证啦，建议咱们提前联系预约呢；
- 如果用户咨询效果：用户咨询产品效果或者案例，你要从用户的历史对话中分析用户实际想咨询的产品，然后根据产品以及产品作用部位，通过标准部位以及产品ID获取案例，产品ID获取规则：如果是单品，则取产品ID，如果是套餐品，则取子产品ID列表，禁止将多个商品的产品ID合并去查询。 如果你没有获取到案例，则必须严格按照没有案例来回答，并使用正向话术说明正在积极补充案例。示例问题："这个效果怎么样"，"有没有案例看看"，"治疗完之后自然么"等
- 如果用户询问是否保证能达到案例的效果，则回复这个姐妹能做到我相信咱们也是可以的，不过每个人的情况都不太一样，我也不能真正的完全保证，但是我们一定会努力给您做到最好的效果；
- 如果用户质疑案例真实性，是否 AI生成、P图，则回复“其实我们发案例主要是想让大家更直观看到可能的改善方向～像光线、角度这些我们会稍微调一下（比如原图可能有点暗，我们就调亮了一点），但皮肤状态、松弛程度的变化都是真实的！”
- 如果用户要指定预约，只能电话联系；
- 咨询用户咨询未售卖商品，包括同产品不同部位，则委婉的表示本次活动暂时没有售卖，但是可以推荐其他产品，同时会收集用户需求，后续会根据用户需求进行活动选品；
- 如果用户咨询是否区分新老客，则回复无论新老客都是统一最低价哈；
- 如果用户咨询赠品信息，则回复目前的活动价格已经拉到最低了，实打实的优惠比赠品更有价值呀；
- 如果用户咨询是否有额外费用，则表示正常都是没有额外费用的，具体需要到院后面诊后才能确定；
- 如果用户咨询修复之前的医美项目导致的问题，则回复需要根据线下实际面诊来看；
- 如果用户咨询线下升单价格，则回复会根据店内老用户的日常价；
- 如果用户咨询手打还是机打，则回复手打和机打没有绝对的好坏，很多人觉得手打比较划算，其实不是的，在有针对性治疗的部位，比如眼周可能手打就比较好，层次会比较深。如果是日常保养机打就比较好，比较均匀而且痛感较小。核心还是看医生的技术和您的个人情况，您来医院面诊后医生会根据你的情况和需求选择最适合您的方案的；
- 当用户索要案例或者问到单次效果的时候，如果有案例描述，则结合案例描述+正向积极的表示：做一次有一次的效果，但追求精致和想效果更绝，推荐按照面诊的咨询师建议；
- 如果用户咨询购买链接，则提示用户所有产品都在下方的商品列表中，可以根据自己的需要选择哦；
- 当你输出商品的时候或者推荐商品的时候，需要重点推荐突出主推品；
- 只要在推荐商品的时候，就需要附带固定格式的商品链接；格式：<self_link><type>buy</type><goods_id>52</goods_id><activity_id>4</activity_id></self_link>

## 禁止
- 回复话术禁止建议联系客服
- 禁止提及活动背景信息中不存在的优惠信息，赠品信息等
- 用户咨询的优惠信息完全以活动背景信息中包含的信息进行回复，禁止拓展
- 禁止向用户输出你调用工具的信息，思考过程
- 确保回复内容中不包含任何可能的 markdown 语法标签，如 #、##、###、*、**、_、__、`、```、[]、() 等。
- 当用户表露出担忧或者负面情绪，禁止“哈哈”等不严肃的语气词；

## 示例
问题：我最近想要做这个听朋友说有些疼。。。
回答：姐妹，热玛吉的疼痛感因人而异，虽然确实会有短暂刺痛，但全程医生会调整能量参数，配合冷敷舒缓，绝大多数姐妹都能轻松耐受~ 术后效果超惊艳，冲就完事啦！

问题：热超或者热玛吉需要几天恢复时间能上日常妆
回答：无创类表皮治疗其实次日就可以正常上淡妆的，但是一般建议72H后再正常化妆，一是给到皮肤一定恢复时间，二是治疗后恢复期间可能会有轻微干燥的情况，上妆状态也不会很好~

问题：我上次打的瑞兰，这次买了需要囤多久才能打
回答：姐妹可以先囤着哈，一般瑞蓝需要半年以上，不过也得看你的吸收效果哈，可以约面诊看一下吸收效果

问题：这个点进去链接怎么看不到商品
回复：姐妹请重新从咱们群内链接点过去哈，这是咱们群内活动的专属商品

## 输出
- 必须是有效的JSON格式；
- 包含以下字段：
    - content: 回复内容
    - resources: 
        - case_images: 案例图片url
        - product_images: 产品图片url
- 不要包含任何解释文字，只返回JSON

JSON格式示例：
```json{
    "content": "",
    "resources": {
        "case_images": [""]
    }
}
```
输出结束后发送 TERMINATE.

"""




# import os
# from openai import OpenAI
# print(os.environ.get("OPENAI_API_KEY"))
# client = OpenAI(api_key="", base_url="https://openai.qiniu.com/v1")
# # model_list = client.models.list()
# # for model in model_list:
# #     print(model.id)

# completion = client.chat.completions.create(
#     model="claude-4.0-sonnet",
#     messages=[
#         {"role": "system", "content": prompt},
#         {"role": "user", "content": """* sku_id: 75; 商品名称:【嘉实超声刀】下颌缘 体验价; 别名: 超声刀; 商品描述: ; 活动价格：980元/1次; 原价：1980元/1次; 作用部位：下颌、下颌缘、眼部、面部、颈部、下颌缘、脸、下颌缘; 是否套餐: 否; 产品ID：2079, 子产品ID列表：[]; 限购数量：3; 有效天数：90; 购买链接：<self_link><type>buy</type><goods_id>75</goods_id><activity_id>3</activity_id></self_link>; 活动开始时间：2025-08-01 15:00:00; 活动结束时间：2025-08-26 21:13:17\n* sku_id: 74; 商品名称:【嘉实超声刀】面部 不限发数; 别名: 超声刀; 商品描述: ; 活动价格：3580元/1次; 原价：4999元/1次; 作用部位：眼部、面部、颈部、下颌缘、脸、下颌缘; 是否套餐: 否; 产品ID：2079, 子产品ID列表：[]; 限购数量：3; 有效天数：90; 购买链接：<self_link><type>buy</type><goods_id>74</goods_id><activity_id>3</activity_id></self_link>; 活动开始时间：2025-08-01 15:00:00; 活动结束时间：2025-08-26 21:13:17\n* sku_id: 78; 商品名称:【超玛吉】面部 900发; 别名: 超玛吉、美版热玛吉五代、热玛吉Thermage FLX™、热玛吉5代; 商品描述: ; 活动价格：12800元/900发; 原价：19999元/900发; 作用部位：眼部、面部、颈部、下颌缘、脸、下颌缘; 是否套餐: 否; 产品ID：214, 子产品ID列表：[]; 限购数量：3; 有效天数：90; 购买链接：<self_link><type>buy</type><goods_id>78</goods_id><activity_id>3</activity_id></self_link>; 活动开始时间：2025-08-01 15:00:00; 活动结束时间：2025-08-26 21:13:17\n* sku_id: 142; 商品名称:【嘉实超声刀】眼部+薇旖美4mg*1; 别名: ; 商品描述: ; 活动价格：2999元/1套; 原价：5999元/1套; 作用部位：; 是否套餐: 是; 产品ID：0, 子产品ID列表：[2079, 394]; 限购数量：0; 有效天数：90; 购买链接：<self_link><type>buy</type><goods_id>142</goods_id><activity_id>3</activity_id></self_link>; 活动开始时间：2025-08-01 15:00:00; 活动结束时间：2025-08-26 21:13:17\n* sku_id: 143; 商品名称:【嘉实超声刀】面部+丽珠兰黑盒2ml*1; 别名: ; 商品描述: ; 活动价格：4999元/1套; 原价：6999元/1套; 作用部位：; 是否套餐: 是; 产品ID：0, 子产品ID列表：[2079, 2072]; 限购数量：0; 有效天数：90; 购买链接：<self_link><type>buy</type><goods_id>143</goods_id><activity_id>3</activity_id></self_link>; 活动开始时间：2025-08-01 15:00:00; 活动结束时间：2025-08-26 21:13:17\n* sku_id: 144; 商品名称:【超玛吉（热玛吉5代）】面部 900发+【丽珠兰黑盒2ml】*1; 别名: ; 商品描述: ; 活动价格：14999元/1套; 原价：19999元/1套; 作用部位：; 是否套餐: 是; 产品ID：0, 子产品ID列表：[214, 2072]; 限购数量：0; 有效天数：90; 购买链接：<self_link><type>buy</type><goods_id>144</goods_id><activity_id>3</activity_id></self_link>; 活动开始时间：2025-08-01 15:00:00; 活动结束时间：2025-08-26 21:13:17\n* sku_id: 145; 商品名称:【超玛吉（热玛吉5代）】面部 900发+【瑞蓝唯缇1ml】*1; 别名: ; 商品描述: ; 活动价格：14999元/1套; 原价：19999元/1套; 作用部位：; 是否套餐: 是; 产品ID：0, 子产品ID列表：[214, 378]; 限购数量：0; 有效天数：90; 购买链接：<self_link><type>buy</type><goods_id>145</goods_id><activity_id>3</activity_id></self_link>; 活动开始时间：2025-08-01 15:00:00; 活动结束时间：2025-08-26 21:13:17\n* sku_id: 146; 商品名称:【超玛吉（热玛吉5代）】面部 900发+【薇旖美4mg】*1; 别名: ; 商品描述: ; 活动价格：14999元/1套; 原价：19999元/1套; 作用部位：; 是否套餐: 是; 产品ID：0, 子产品ID列表：[214, 394]; 限购数量：0; 有效天数：90; 购买链接：<self_link><type>buy</type><goods_id>146</goods_id><activity_id>3</activity_id></self_link>; 活动开始时间：2025-08-01 15:00:00; 活动结束时间：2025-08-26 21:13:17\n* sku_id: 138; 商品名称:【嘉实超声刀】眼部; 别名: 超声刀; 商品描述: ; 活动价格：4000元/面部900发; 原价：4000元/面部900发; 作用部位：眼部、眼部、面部、颈部、下颌缘、脸、下颌缘; 是否套餐: 否; 产品ID：2079, 子产品ID列表：[]; 限购数量：0; 有效天数：90; 购买链接：<self_link><type>buy</type><goods_id>138</goods_id><activity_id>0</activity_id></self_link>; 活动开始时间：; 活动结束时间：\nuser_id: 40, corp_id: 21\n    ## 历史对话\n    ['user: 哪个好', 'user: 998呢', 'user: 3万以上的', 'user: 2w出头', 'user: 100块体验', 'system: 用户求讲解了商品：【嘉实超声刀】面部 不限发数, sku_id: 74', 'system: 用户求讲解了商品：【超玛吉】面部 900发, sku_id: 78', 'system: 用户求讲解了商品：【嘉实超声刀】下颌缘 体验价, sku_id: 75', 'system: 用户求讲解了商品：【嘉实超声刀】下颌缘 体验价, sku_id: 75', 'user: 价格有点贵']\n    ## 用户最后一次求讲解的商品信息\n    \n    ## 用户问题引用的消息\n    \n    ## 用户问题\n    价格有点贵\n    """}
#     ]
# )

# print(completion.choices[0].message.content)



# async def main():
#     from autogen_ext.models.openai import OpenAIChatCompletionClient

#     model_client = OpenAIChatCompletionClient(
#         model="kimi-k2-turbo-preview",
#         base_url="https://api.moonshot.cn/v1",
#         api_key="",
#         model_info=ModelInfo(
#             json_output=True,
#             structured_output=True,
#             family=ModelFamily.UNKNOWN,
#             vision=False,
#             function_calling=True,
#             multiple_system_messages=False,
#         )
#     )

#     # 检查模型返回是否包含 tool_calls
#     result = await model_client.create(
#         messages=[{"role": "user", "content": "What's the weather in Beijing?"}],
#         tools=[{"type": "function", "function": {...}}]
#     )

#     print(result.content)


# import asyncio
# asyncio.run(main())


import asyncio
import os
from autogen_ext.models.openai import OpenAIChatCompletionClient

async def test_function_call_support():
    # 1. 构造 model_client
    client = OpenAIChatCompletionClient(
        model="kimi-k2-turbo-preview",                       # 你想测的模型名
        base_url="https://api.moonshot.cn/v1",
        api_key="",
        model_info=ModelInfo(
            json_output=True,
            structured_output=True,
            family="unknown",
            vision=False,
            function_calling=True,
            multiple_system_messages=False,
        )
    )

    # 2. 函数描述
    tools = [
        {
            "type": "function", # 约定的字段 type，目前支持 function 作为值
            "function": { # 当 type 为 function 时，使用 function 字段定义具体的函数内容
                "name": "search", # 函数的名称，请使用英文大小写字母、数据加上减号和下划线作为函数名称
                "description": """ 
                    通过搜索引擎搜索互联网上的内容。
    
                    当你的知识无法回答用户提出的问题，或用户请求你进行联网搜索时，调用此工具。请从与用户的对话中提取用户想要搜索的内容作为 query 参数的值。
                    搜索结果包含网站的标题、网站的地址（URL）以及网站简介。
                """, # 函数的介绍，在这里写上函数的具体作用以及使用场景，以便 Kimi 大模型能正确地选择使用哪些函数
                "parameters": { # 使用 parameters 字段来定义函数接收的参数
                    "type": "object", # 固定使用 type: object 来使 Kimi 大模型生成一个 JSON Object 参数
                    "required": ["query"], # 使用 required 字段告诉 Kimi 大模型哪些参数是必填项
                    "properties": { # properties 中是具体的参数定义，你可以定义多个参数
                        "query": { # 在这里，key 是参数名称，value 是参数的具体定义
                            "type": "string", # 使用 type 定义参数类型
                            "description": """
                                用户搜索的内容，请从用户的提问或聊天上下文中提取。
                            """ # 使用 description 描述参数以便 Kimi 大模型更好地生成参数
                        }
                    }
                }
            }
        },
        {
            "type": "function", # 约定的字段 type，目前支持 function 作为值
            "function": { # 当 type 为 function 时，使用 function 字段定义具体的函数内容
                "name": "crawl", # 函数的名称，请使用英文大小写字母、数据加上减号和下划线作为函数名称
                "description": """
                    根据网站地址（URL）获取网页内容。
                """, # 函数的介绍，在这里写上函数的具体作用以及使用场景，以便 Kimi 大模型能正确地选择使用哪些函数
                "parameters": { # 使用 parameters 字段来定义函数接收的参数
                    "type": "object", # 固定使用 type: object 来使 Kimi 大模型生成一个 JSON Object 参数
                    "required": ["url"], # 使用 required 字段告诉 Kimi 大模型哪些参数是必填项
                    "properties": { # properties 中是具体的参数定义，你可以定义多个参数
                        "url": { # 在这里，key 是参数名称，value 是参数的具体定义
                            "type": "string", # 使用 type 定义参数类型
                            "description": """
                                需要获取内容的网站地址（URL），通常情况下从搜索结果中可以获取网站的地址。
                            """ # 使用 description 描述参数以便 Kimi 大模型更好地生成参数
                        }
                    }
                }
            }
        }
    ]
    # tools = [{
    #     "type": "function",
    #     "function": {
    #         "name": "get_weather",
    #         "description": "Get current weather for a city",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {
    #                 "city": {"type": "string", "description": "City name"}
    #             },
    #             "required": ["city"]
    #         }
    #     }
    # }]

    # 3. 发送消息
    messages = [UserMessage(content="What's the weather in Beijing?", source="user")]
    response = await client.create(
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    # 4. 检查结果
    print("---- 原始返回 ----")
    print(response)

    # 如果有 tool_calls 就说明支持
    if response.content and hasattr(response.content[0], 'tool_calls'):
        print("\n✅ 模型支持函数调用（tool_calls 存在）")
        for tc in response.content[0].tool_calls:
            print("   -", tc.function.name, tc.function.arguments)
    else:
        print("\n❌ 模型未返回 tool_calls，当前不支持函数调用")

if __name__ == "__main__":
    asyncio.run(test_function_call_support())
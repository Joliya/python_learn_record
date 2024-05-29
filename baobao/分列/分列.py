"""
@file: 分列.py
@time: 2024/4/19 13:03
@desc: 
"""


# 有一个 excel， 第一列为ID，不用处理，第二列格式为：关于鼻咽癌的复发率科普知识（2024-04-18 11:40:28）：https://yqszhyx.oss-cn-hangzhou.aliyuncs.com/yljk_yqszhyx/13_172_3745_36577_copy_B305DF7C-DF8C-4FE4-89C9-651F220F353F.mov, 要求第二列拆分为：标题、时间、链接
import pandas as pd
import re
import os

# data = pd.read_excel("/Users/zhangjinpeng/PycharmProjects/flaskProject/baobao/工作簿9.xlsx")
# result = [["任务交付物ID", "标题", "时间", "链接"]]
# data.fillna("", inplace=True)
# for item in data.values:
#     _id, content = item
#     if not content:
#         result.append([_id, "", "", ""])
#         continue
#     title, time, url = re.findall(r"(.*)\((.*)\):(.*)", content)[0]
#     result.append([_id, title, time, url])
#
# df = pd.DataFrame(result)
# df.to_excel("/Users/zhangjinpeng/PycharmProjects/flaskProject/baobao/工作簿9_new.xlsx", index=False, header=False)

df = pd.read_excel("/Users/zhangjinpeng/PycharmProjects/flaskProject/baobao/分列/需要分裂.xlsx")
df.fillna("", inplace=True)

# 定义一个函数，用于通过正则表达式拆分字符串
# def split_column(_id, text):
#     if not text:
#         return _id, "", "", ""
#     # 使用正则表达式匹配标题、时间和链接
#     match = re.match(r'(.*)\（(.+)\）：(.+)', text)
#     if match:
#         title, time, url = match.groups()
#         return _id, title, time, url
#     else:
#         return _id, '', '', ''
#
# # 应用函数拆分第二列，并将结果分配给三个新列
# df[['标题', '时间', '链接']] = df.apply(lambda row: split_column(row[0], row[1]), axis=1, result_type='expand')


# import pandas as pd
# import re
#
# # 读取Excel文件
# df = pd.read_excel('input.xlsx')

# 定义一个函数，用于拆分第二列的数据
def split_column(row):
    # 使用正则表达式匹配标题、时间和链接
    match = re.match(r'(.+)\（(.+)\）：(.+)', row)
    if match:
        # 如果匹配成功，提取标题、时间和链接
        return match.group(1), match.group(2), match.group(3)
    else:
        # 如果匹配失败，返回空值
        return None, None, None

# 应用函数到第二列的每一行，并创建一个新的DataFrame
new_columns = ['标题', '时间', '链接']
col_index = 18
new_df = pd.DataFrame(df.iloc[:, col_index].apply(split_column).tolist(), columns=new_columns)

# 将ID列和新的DataFrame合并
l = [i for i in range(0, 21)]
result_df = pd.concat([df.iloc[:, l], new_df], axis=1)

# 将结果写入新的Excel文件
result_df.to_excel(f"/Users/zhangjinpeng/PycharmProjects/flaskProject/baobao/分列/需要分裂-new.xlsx", index=False, header=True)


"""
@file: 行转列.py
@time: 2024/5/10 11:20
@desc: 
"""


import pandas as pd


data = pd.read_excel("/Users/zhangjinpeng/PycharmProjects/flaskProject/baobao/需要转换.xlsx")
data.fillna("", inplace=True)
# result = [["端点", "员工编码", "自然人"]]
result = [["端点", "员工编码", "自然人名称", "端点性质", "备注", "大区", "自然人名称（单个）"]]

code_name_set = set()


for row in data.values:
    if row[2]:
        print(f"值： {row[2]}")
        split_col = row[2].replace("/", "、")
        split_col = split_col.replace("\\", "、")
        for i in split_col.split("、"):
            if f"{row[1]}_{i}" in code_name_set:
                continue
            code_name_set.add(f"{row[1]}_{i}")
            result.append([row[0], row[1], row[2], row[3], row[4], row[5], i])
    else:
        if f"{row[1]}_{row[2]}" in code_name_set:
            continue
        code_name_set.add(f"{row[1]}_{i}")
        result.append([row[0], row[1], row[2], row[3], row[4], row[5], row[2]])


pd.DataFrame(result).to_excel("/Users/zhangjinpeng/PycharmProjects/flaskProject/baobao/需要转换-new.xlsx", index=False, header=False)

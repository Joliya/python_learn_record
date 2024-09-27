"""
@file: 获取文章标题.py
@time: 2024/4/22 14:27
@desc: 
"""
import re
from collections import defaultdict

# 有一个文件夹 /PycharmProjects/flaskProject/baobao/get_filename/科普文章-4.19/
# 文件夹下有N个文件夹，命名格式为 1 吴畏12、2 王关键14 这种，每个子文件夹下有N个docx文档，要求按照人名将对应文件夹下的docx文档的标题提取出来，写入一个excel文件

# 获取所有文档
result = [["人名", "标题"]]

result_dict = defaultdict(list)
import os
for root, dirs, files in os.walk("/PycharmProjects/flaskProject/baobao/get_filename/科普文章-5.23"):
    for file in files:
        if file.endswith(".docx"):
            name = root.split(" ")[1]
            if "/" in name:
                name = name.split("/")[0]
            new_name = re.sub(r'(\d+)(?=\.\w+$)', '', name)
            result_dict[new_name].append(file)

n = ""
for name, files in result_dict.items():
    for file in files:
        # if name == n:
        #     result.append(["", file])
        # else:
        #     n = name
        result.append([name, file])

import pandas as pd
pd.DataFrame(result).to_excel("/PycharmProjects/flaskProject/baobao/get_filename/科普文章-5.23-标题.xlsx", index=False, header=True)

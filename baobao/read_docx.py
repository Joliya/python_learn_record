"""
@file: read_docx.py
@time: 2023/11/23 18:58
@desc: 
"""


import os
import pandas as pd

# 文件夹路径
folder_path = "/Users/zhangjinpeng/Documents/宝宝/待命名"

# 获取文件夹中所有文件的路径
file_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if not file.startswith(".")]

# 获取每个文件的名字
file_names = [os.path.basename(file_path) for file_path in file_paths]

# 创建一个 DataFrame 对象
df = pd.DataFrame({"文档名称": file_names})

# 将数据写入 Excel 文件
df.to_excel("/Users/xianxian/Desktop/11.22西藏大区内容创作/次仁172_文档名称.xlsx", index=False)

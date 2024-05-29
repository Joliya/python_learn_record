"""
@file: output_docx_name.py
@time: 2024/2/1 18:34
@desc: 
"""
import pandas as pd


path = "/baobao/get_filename/科普文章-4.28/"


# 输出 path 中所有文件的文件名称
def output_file_name():
    import os
    result = []
    for dirs, _, files in os.walk(path):
        for file_name in files:
            result.append([file_name, file_name.split(".")[0]])
    # for file_name in os.listdir(path):
    #     result.append([file_name, file_name.split(".")[0]])
    pd.DataFrame(result).to_excel(f"{path}/file_name.xlsx", index=False, header=False)


if __name__ == '__main__':
    output_file_name()

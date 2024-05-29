"""
@file: rename_file.py
@time: 2023/11/24 18:17
@desc: 
"""

import os
import sys

import pandas as pd


def rename_files(folder_path, excel_path):
    # 读取 Excel 文件
    try:
        df = pd.read_excel(excel_path)

        name_map = {str(old_name): str(new_name) for old_name, new_name in df.values}

        for file in os.listdir(folder_path):
            if file.startswith("."):
                continue
            name, extension = os.path.splitext(file)
            new_name = name_map.get(name)
            old_file_name = f"{name}{extension}"
            new_file_name = f"{new_name}{extension}"
            old_file_path = f"{folder_path}/{old_file_name}"
            new_file_path = f"{folder_path}/{new_file_name}"
            if os.path.exists(old_file_path):
                os.rename(old_file_path, new_file_path)
                print(f"文件 「{old_file_name}」 已重命名为 「{new_file_name}」")
            else:
                print(f"文件 「{old_file_name}」 不存在")
        print("所有文件重命名完成")
    except Exception as e:
        print("Excel 文件读取失败")
        print(e)


def extract_file_name(folder_path, current_path):
    try:
        file_names = []
        for file in os.listdir(folder_path):
            if file.startswith("."):
                continue
            name, extension = os.path.splitext(file)
            file_names.append(name)
        df = pd.DataFrame({"文档名称": file_names})
        df.to_excel(f"{current_path}/文件名称提取结果.xlsx", index=False)
    except Exception as e:
        print("文件名称提取失败")
        print(e)


if __name__ == '__main__':
    if getattr(sys, 'frozen', False):
        # 脚本被冻结，获取可执行文件的路径
        home_directory = os.path.dirname(sys.executable)
    else:
        # 脚本未被冻结，获取脚本所在的路径
        home_directory = os.path.dirname(os.path.abspath(__file__))
    folder_path = f"{home_directory}/待命名"
    excel_path = f"{home_directory}/文件名称提取结果.xlsx"
    if not os.path.exists(excel_path):
        extract_file_name(folder_path, home_directory)
    else:
        rename_files(folder_path, excel_path)

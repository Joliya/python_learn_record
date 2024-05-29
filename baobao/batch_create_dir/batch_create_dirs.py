"""
@file: batch_create_dirs.py
@time: 2023/12/7 11:35
@desc: 
"""


import os
import pandas as pd
import sys


def get_executable_dir():
    """获取可执行文件所在的目录。"""
    if getattr(sys, 'frozen', False):
        # 如果程序是“冻结”的，即打包成一个可执行文件，则返回可执行文件所在的目录
        return os.path.dirname(sys.executable)
    else:
        # 如果程序是以脚本形式运行的，则返回脚本所在的目录
        return os.path.dirname(os.path.abspath(__file__))


if __name__ == '__main__':
    home_directory = get_executable_dir()
    print("注意！！！！ 待创建的文件名称所在的 excel 文件，必须有表头，表头名字无所谓，但是必须有表头")
    print(f"当前文件夹路径: {home_directory}")
    file_path = f"{home_directory}/文件名.xlsx"
    print(f"待读取的命名文件: {file_path}")
    data = pd.read_excel(file_path)
    name_list = []
    for i in data.values:
        str_count = str(i[-1])
        if "." in str_count:
            count, word_count = str_count.split(".")
            count, word_count = int(count), int(word_count)
        else:
            count, word_count = int(str_count), 0
        if word_count > 0:
            count += 1
        name_list.append(f"{i[0]}{count}")
    if not os.path.exists(f"{home_directory}/文件夹列表"):
        os.mkdir(f"{home_directory}/文件夹列表")
    index = 0
    for i in name_list:
        dir_name = f"{home_directory}/文件夹列表/{i}"
        os.mkdir(dir_name)
        index += 1
        print(f"{dir_name} 创建成功")
    print(f"共创建 {index} 个文件夹")
    sys.exit(0)

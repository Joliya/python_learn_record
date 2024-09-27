"""
@file: del_doc_end_digist.py
@time: 2024/4/18 20:10
@desc: 
"""


import os
import re
# 删除文件夹内所有文件名末尾的数字


def del_doc_end_digist(file_path):
    for root, dirs, files in os.walk(file_path):
        for file in files:
            if not file.endswith(".docx"):
                continue
            new_name = re.sub(r'(\d+)(?=\.\w+$)', '', file)
            os.rename(os.path.join(root, file), os.path.join(root, new_name))
            print(f"{file} -> {new_name}")


if __name__ == '__main__':
    del_doc_end_digist("/PycharmProjects/flaskProject/baobao/distribute_doc/待分发/甲亢221")

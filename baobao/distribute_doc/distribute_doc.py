# -*- coding: utf-8 -*-
"""
@file: distribute_doc.py
@time: 2023/12/16 11:11
@desc: 
"""
import copy
import random
import re
import sys
import shutil
import os
import pandas as pd


def get_all_files(directory):
    file_list = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.startswith("."):
                continue
            file_path = os.path.join(root, file)
            file_list.append(file_path)

    return file_list


# def truncate_docx(input_path, output_path, word_limit):
#     # 加载现有的 .docx 文件
#     try:
#         doc = docx.Document(input_path)
#     except:
#         convert_path = f"{home_directory}/转换的标准文档"
#         if not os.path.exists(convert_path):
#             os.mkdir(convert_path)
#         new_doc_convert(input_path, convert_path)
#         doc = docx.Document(f"{convert_path}/{os.path.basename(input_path)}")
#     new_doc = docx.Document()
#
#     # 初始化字数计数器
#     total_words = 0
#     # 遍历段落并复制到新文档，直到达到字数限制
#     for para in doc.paragraphs:
#         # 计算当前段落的字数
#         word_count = len(para.text)
#         # 如果当前总字数加上这段话的字数不超过限制，就添加到新文档
#         if total_words + word_count <= word_limit:
#             new_doc.add_paragraph(para.text)
#             total_words += word_count
#         else:
#             # 如果超过了限制，截断这段话并结束循环
#             words = para.text
#             remaining_words = word_limit - total_words
#             truncated_text = ' '.join(words[:remaining_words])
#             new_doc.add_paragraph(truncated_text)
#             break
#
#     # 保存新的文档
#     new_doc.save(output_path)


# def new_doc_convert(input_path, out_path):
#     # 定义 shell 脚本的路径
#     shell_script_path = '/Users/zhangjinpeng/PycharmProjects/flaskProject/baobao/distribute_doc/convert_doc.sh'
#
#     # 定义要转换的文件路径和输出目录路径
#     input_file = input_path
#     output_dir = out_path
#
#     # 调用 shell 脚本，并传递参数
#     result = subprocess.run([shell_script_path, input_file, output_dir], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
#                             text=True)


def get_executable_dir():
    if getattr(sys, 'frozen', False):
        # 脚本被冻结，获取可执行文件的路径
        home_directory = os.path.dirname(sys.executable)
    else:
        # 脚本未被冻结，获取脚本所在的路径
        home_directory = os.path.dirname(os.path.abspath(__file__))
    return home_directory


def batch_create(home_directory):
    print("注意！！！！ 待创建的文件名称所在的 excel 文件，必须有表头，表头名字无所谓，但是必须有表头")
    print(f"当前文件夹路径: {home_directory}")
    file_path = f"{home_directory}/分发列表.xlsx"
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
        name_list.append(f"{i[0]} {i[1]}")
        # name_list.append(f"{i[0]} {i[1]}{count}")
    if not os.path.exists(f"{home_directory}/分发列表"):
        os.mkdir(f"{home_directory}/分发列表")
    index = 0
    for i in name_list:
        dir_name = f"{home_directory}/分发列表/{i}"
        if os.path.exists(dir_name):
            continue
        os.mkdir(dir_name)
        index += 1
        print(f"{dir_name} 创建成功")
    print(f"共创建 {index} 个文件夹")


def merge(dir_path):
    file_list = get_all_files(dir_path)
    for file in file_list:
        p_list = file.split("/")
        index = p_list.index("distribute_doc")
        p_list[index + 1] = "待分发"
        dest_path = "/".join(p_list)
        if not os.path.exists("/".join(dest_path.split("/")[:-1])):
            os.makedirs("/".join(dest_path.split("/")[:-1]))

        shutil.copy2(file, dest_path)


def distribute():
    home_directory = get_executable_dir()
    file_path = f"{home_directory}/分发列表.xlsx"
    if not os.path.exists(file_path):
        print("分发列表.xlsx 文件不存在")
        sys.exit(0)
    batch_create(home_directory)
    file_list = get_all_files(f"{home_directory}/待分发")
    clinic_2_file_list = {}
    for file in file_list:
        pth_list = file.split("/")
        index = pth_list.index("待分发")
        clinic = pth_list[index + 1]
        f_list = clinic_2_file_list.get(clinic, [])
        f_list.append(file)
        clinic_2_file_list[clinic] = f_list
    data = pd.read_excel(f"{home_directory}/分发列表.xlsx")
    dir_list = []
    need_count = 0
    for i in data.values:
        file_count = i[-1]
        dir_name = i[0]
        if "." in str(file_count):
            num, remainder = str(file_count).split(".")
        else:
            num, remainder = str(file_count), 0
        words_count = int(remainder) * 100
        random_num = random.randint(1, 40)
        c = words_count + random_num
        if words_count > 0:
            dis_file_count = int(num) + 1
        else:
            dis_file_count = int(num)
        need_count += int(dis_file_count)
        dir_list.append((f"{dir_name}{dis_file_count}", dis_file_count, int(words_count), c))
    if len(file_list) < need_count:
        print(f"待分发文件数量不足，需要 {need_count} 篇，实际只有 {len(file_list)} 篇")
        sys.exit(0)
    index = 0
    dis_count = 0
    # 剩余文件数量
    surplus_count = 0
    list_of_list = [["文件夹", "分发数量", "需要字数"]]
    for clinic, file_list in clinic_2_file_list.items():
        files_list = copy.deepcopy(file_list)
        if index >= len(dir_list):
            break
        dir_name, num, words_count, _ = dir_list[index]
        while len(files_list) > num:
            special = False
            dir_path = f"{home_directory}/分发列表/{dir_name}"
            for i in range(num):
                file_path = files_list.pop()
                file_name = os.path.basename(file_path)
                new_file_path = f"{dir_path}/{file_name}"
                if not special and words_count > 0:
                    file_name = re.sub(r'(\d+)(?=\.\w+$)', '', file_name)
                    f_name, extend = os.path.splitext(file_name)
                    new_file_path = f"{dir_path}/{f_name}_{words_count}{extend}"
                    special = True
                shutil.copy2(file_path, new_file_path)
            dis_files = get_all_files(dir_path)
            print(f"文件夹 「{dir_name}」 已分发完成, 分发数量 {len(dis_files)}, 其中一篇需要字数 {words_count}")
            list_of_list.append([dir_name, num, words_count])
            dis_count += num
            index += 1
            if index >= len(dir_list):
                break
            dir_name, num, words_count, _ = dir_list[index]
        if files_list:
            surplus_count += len(files_list)
            for file in files_list:
                path_list = file.split("/")
                wait_index = path_list.index("待分发")
                path_list[wait_index] = "剩余文档"
                dir_pth = "/".join(path_list[:-1])
                if not os.path.exists(dir_pth):
                    os.makedirs(dir_pth)
                shutil.copy2(file, f"{dir_pth}/{os.path.basename(file)}")
    print(f"共分发 {dis_count} 篇文件，剩余 {surplus_count} 篇文件")
    pd.DataFrame(list_of_list).to_excel(f"{home_directory}/分发结果.xlsx", index=False)


def distribute_2():
    home_directory = get_executable_dir()
    file_path = f"{home_directory}/分发列表.xlsx"
    if not os.path.exists(file_path):
        print("分发列表.xlsx 文件不存在")
        sys.exit(0)
    # batch_create(home_directory)
    file_list = get_all_files(f"{home_directory}/待分发")
    clinic_2_file_list = {}
    for file in file_list:
        pth_list = file.split("/")
        index = pth_list.index("待分发")
        clinic = pth_list[index + 1]
        f_list = clinic_2_file_list.get(clinic, [])
        f_list.append(file)
        clinic_2_file_list[clinic] = f_list
    data = pd.read_excel(f"{home_directory}/分发列表.xlsx")
    dir_list = []
    need_count = 0
    dis_info_list = [i for i in data.values]
    dis_info_list.sort(key=lambda x: x[-1], reverse=True)
    for i in dis_info_list:
        file_count = i[-1]
        # dir_name = f"{i[0]}"
        dir_name = f"{i[0]} {i[1]}"
        if "." in str(file_count):
            num, remainder = str(file_count).split(".")
        else:
            num, remainder = str(file_count), 0
        words_count = int(remainder) * 100
        random_num = random.randint(1, 40)
        c = words_count + random_num
        if words_count > 0:
            dis_file_count = int(num) + 1
        else:
            dis_file_count = int(num)
        need_count += int(dis_file_count)
        dir_list.append((f"{dir_name}{dis_file_count}", dis_file_count, int(words_count), c))
    # if len(file_list) < need_count:
    #     print(f"待分发文件数量不足，需要 {need_count} 篇，实际只有 {len(file_list)} 篇")
    #     sys.exit(0)
    index = 0
    dis_count = 0
    # 剩余文件数量
    surplus_count = 0
    list_of_list = [["文件夹", "分发数量", "需要字数"]]
    for name, need_dis_count, words_count, _ in dir_list:
        doctor_file_path = f"{home_directory}/分发列表/{name}"
        for clinic, file_list in clinic_2_file_list.items():
            dir_path = f"{home_directory}/分发列表/{name}"
            if len(file_list) < need_dis_count:
                # list_of_list.append([name, len(file_list), words_count])
                continue
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            copy_file_list = copy.deepcopy(file_list)
            special = False
            for n in range(need_dis_count):
                file_path = copy_file_list.pop()
                file_name = os.path.basename(file_path)
                file_name = file_name.replace("_科普文章", "")
                file_name = re.sub(r'(\d+)(?=\.\w+$)', '', file_name)
                new_file_path = f"{dir_path}/{file_name}"
                if not special and words_count > 0:
                    f_name, extend = os.path.splitext(file_name)
                    new_file_path = f"{dir_path}/{f_name}_{words_count}{extend}"
                    special = True
                shutil.copy2(file_path, new_file_path)
            clinic_2_file_list[clinic] = copy_file_list
            break
        dis_files = get_all_files(doctor_file_path)
        dis_count += len(dis_files)
        list_of_list.append([name, len(dis_files), words_count])

    for k, v in clinic_2_file_list.items():
        surplus_count += len(v)
        for file in v:
            path_list = file.split("/")
            wait_index = path_list.index("待分发")
            path_list[wait_index] = "剩余文档"
            dir_pth = "/".join(path_list[:-1])
            if not os.path.exists(dir_pth):
                os.makedirs(dir_pth)
            shutil.copy2(file, f"{dir_pth}/{os.path.basename(file)}")
    print(f"共分发 {dis_count} 篇文件，剩余 {surplus_count} 篇文件")
    pd.DataFrame(list_of_list).to_excel(f"{home_directory}/分发结果.xlsx", index=False)


if __name__ == '__main__':
    # distribute()
    distribute_2()
    home_directory = get_executable_dir()
    file_list = get_all_files(f"{home_directory}/分发列表")
    print(len(file_list) == len(list(set(file_list))))
    print(1)
    # merge(f"{home_directory}/剩余文档-12.17")
    # merge(f"{home_directory}/剩余文档-12.18")
    # merge(f"{home_directory}/剩余文档-500篇")
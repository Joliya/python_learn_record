"""
@file: 删除文件层级.py
@time: 2024/5/21 11:21
@desc: 
"""
import os


def get_all_files(directory):
    file_list = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.startswith("."):
                continue
            file_path = os.path.join(root, file)
            file_list.append(file_path)

    return file_list


def delete_file_level():
    """
    文件路径为当前文件路径同级目录【内容创作】, 要求删除下一级目录，保留下下一级目录
    :return:
    """
    # 获取 /Users/zhangjinpeng/PycharmProjects/flaskProject/baobao/删除文件层级/内容创作 目录下的所有文件全路径
    file_path = os.path.dirname(os.path.realpath(__file__))
    dir_name = "交付物导出-科普文章-2024-05-27-北京基层"
    new_file_path = os.path.join(file_path, dir_name)
    fiels = get_all_files(new_file_path)
    for item in fiels:
        new_path = item.split("/")[0:-2] + [item.split("/")[-1]]
        for i in new_path:
            if i == dir_name:
                new_path[new_path.index(i)] = f"{dir_name}-删除"
        if not os.path.exists("/".join(new_path[:-1])):
            os.makedirs("/".join(new_path[:-1]), exist_ok=True)
        new_path = "/".join(new_path)
        os.rename(item, new_path)
        # os.remove(item)

if __name__ == '__main__':

    delete_file_level()

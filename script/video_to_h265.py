"""
@file: video_to_h265.py
@time: 2024/2/19 17:04
@desc: 
"""
import os
import subprocess
import pandas as pd


def video_to_h265(source_dir_path, target_dir_path):
    """
    将视频文件编码为H.265格式
    :return:
    """
    # 获取 source_dir_path 下所有视频
    source_video_list = []
    target_video_list = []
    for root, dirs, files in os.walk(source_dir_path):
        if str(root).__contains__("h265"):
            continue
        for file in files:
            if file.endswith(".mp4"):
                source_video_list.append(os.path.join(root, file))
                target_video_list.append(os.path.join(target_dir_path, file))
    sour_list = []
    # 逐个转换
    for index, source_video in enumerate(source_video_list):
        target_video = target_video_list[index]
        print(source_video)
        sour_list.append(source_video)
        if os.path.exists(target_video):
            print(f"{target_video} 已存在")
            continue
        # command = f"ffmpeg -i {source_video} -movflags faststart -tag:v hvc1 -c:v libx265 -preset slow {target_video}"
        command = f"ffmpeg -i {source_video} -movflags faststart -tag:v hvc1 -c:v libx265 -x265-params keyint=10:min-keyint=10 -preset slow  {target_video} -y"
        print(command)
        subprocess.run(command, shell=True)
    for i in sour_list:
        print(i)


if __name__ == '__main__':
    source_dir_path, target_dir_path = "", ""
    video_to_h265(source_dir_path, target_dir_path)

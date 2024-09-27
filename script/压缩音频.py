"""
@file: 压缩音频.py
@time: 2024/7/8 14:27
@desc: 
"""
import os

from pydub import AudioSegment


file_path = ""

bit_rates = ["32k", "64k", "128k"]


# 获取 file_path 中所有的 mp3 文件路径
file_paths = []
for root, dirs, files in os.walk(file_path):
    for file in files:
        if file.endswith(".mp3"):
            file_paths.append(os.path.join(root, file))

export_path = ""
for file_path in file_paths:
    # 加载 MP3 文件
    audio = AudioSegment.from_mp3(file_path)

    # 设置比特率并导出
    for bit_rate in bit_rates:
        new_path = f"{export_path}/{bit_rate}/{file_path.split('/')[-1]}"
        audio.export(new_path, format="mp3", bitrate=bit_rate)

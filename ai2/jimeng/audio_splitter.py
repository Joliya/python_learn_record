"""
音频分割工具
将MP3文件按照指定时间间隔分割为多个文件
"""

import os
from pathlib import Path
from typing import Optional
from pydub import AudioSegment


def split_audio(
    audio_file_path: str,
    interval_seconds: int = 60,
    output_folder_name: str = "split_audio"
) -> list[str]:
    """
    将音频文件按照指定时间间隔分割为多个文件
    
    Args:
        audio_file_path: 音频文件路径
        interval_seconds: 分割时间间隔（秒），默认60秒
        output_folder_name: 输出子文件夹名称，默认"split_audio"
        
    Returns:
        分割后的文件路径列表
        
    Raises:
        FileNotFoundError: 文件不存在
        ValueError: 参数错误
    """
    # 检查文件是否存在
    if not os.path.exists(audio_file_path):
        raise FileNotFoundError(f"音频文件不存在: {audio_file_path}")
    
    # 检查参数
    if interval_seconds <= 0:
        raise ValueError("时间间隔必须大于0")
    
    # 获取文件信息
    file_path = Path(audio_file_path)
    file_dir = file_path.parent
    file_name = file_path.stem
    file_ext = file_path.suffix
    
    # 创建输出文件夹
    output_dir = file_dir / output_folder_name
    output_dir.mkdir(exist_ok=True)
    
    print(f"正在加载音频文件: {audio_file_path}")
    
    # 加载音频文件
    audio = AudioSegment.from_file(audio_file_path)
    
    # 获取音频总时长（毫秒）
    total_duration_ms = len(audio)
    total_duration_sec = total_duration_ms / 1000
    
    print(f"音频总时长: {total_duration_sec:.2f}秒")
    print(f"分割间隔: {interval_seconds}秒")
    
    # 计算分割数量
    interval_ms = interval_seconds * 1000
    num_segments = (total_duration_ms + interval_ms - 1) // interval_ms
    
    print(f"将分割为 {num_segments} 个片段")
    
    # 分割音频
    output_files = []
    for i in range(num_segments):
        start_ms = i * interval_ms
        end_ms = min((i + 1) * interval_ms, total_duration_ms)
        
        # 提取片段
        segment = audio[start_ms:end_ms]
        
        # 生成输出文件名
        output_filename = f"{file_name}_part_{i+1:03d}{file_ext}"
        output_path = output_dir / output_filename
        
        # 导出片段
        print(f"导出片段 {i+1}/{num_segments}: {output_filename} ({(end_ms-start_ms)/1000:.2f}秒)")
        segment.export(output_path, format=file_ext[1:])  # 去掉扩展名的点
        
        output_files.append(str(output_path))
    
    print(f"\n分割完成！共生成 {len(output_files)} 个文件")
    print(f"输出目录: {output_dir}")
    
    return output_files


def split_audio_by_count(
    audio_file_path: str,
    num_parts: int,
    output_folder_name: str = "split_audio"
) -> list[str]:
    """
    将音频文件平均分割为指定数量的文件
    
    Args:
        audio_file_path: 音频文件路径
        num_parts: 分割数量
        output_folder_name: 输出子文件夹名称
        
    Returns:
        分割后的文件路径列表
    """
    # 检查文件是否存在
    if not os.path.exists(audio_file_path):
        raise FileNotFoundError(f"音频文件不存在: {audio_file_path}")
    
    if num_parts <= 0:
        raise ValueError("分割数量必须大于0")
    
    # 加载音频
    audio = AudioSegment.from_file(audio_file_path)
    total_duration_ms = len(audio)
    
    # 计算每段时长
    interval_ms = total_duration_ms // num_parts
    interval_seconds = interval_ms / 1000
    
    print(f"音频总时长: {total_duration_ms/1000:.2f}秒")
    print(f"分割为 {num_parts} 段，每段约 {interval_seconds:.2f}秒")
    
    # 调用按时间分割的方法
    return split_audio(audio_file_path, int(interval_seconds), output_folder_name)


def main():
    """
    命令行使用示例
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="音频分割工具")
    parser.add_argument("audio_file", help="音频文件路径")
    parser.add_argument("-i", "--interval", type=int, default=60, 
                       help="分割时间间隔（秒），默认60秒")
    parser.add_argument("-n", "--num-parts", type=int, 
                       help="分割数量（与interval互斥）")
    parser.add_argument("-o", "--output", default="split_audio", 
                       help="输出文件夹名称，默认'split_audio'")
    
    args = parser.parse_args()
    
    try:
        if args.num_parts:
            # 按数量分割
            output_files = split_audio_by_count(
                args.audio_file,
                args.num_parts,
                args.output
            )
        else:
            # 按时间间隔分割
            output_files = split_audio(
                args.audio_file,
                args.interval,
                args.output
            )
        
        print("\n生成的文件:")
        for i, file_path in enumerate(output_files, 1):
            print(f"{i}. {file_path}")
            
    except Exception as e:
        print(f"错误: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    # 示例用法
    print("=" * 60)
    print("音频分割工具")
    print("=" * 60)
    
    # 方式1: 直接调用函数
    output_files = split_audio(
        audio_file_path='/Users/buzhimingrenshilaonianji/Documents/维纳斯资料/数字人音频/王维单人播客1_1倍速.MP3',
        interval_seconds=30,  # 每60秒分割一次
        output_folder_name="split_audio"
    )
    
    # 方式2: 按数量分割
    # output_files = split_audio_by_count(
    #     audio_file_path="path/to/your/audio.mp3",
    #     num_parts=5,  # 分割为5个文件
    #     output_folder_name="split_audio"
    # )
    
    # 方式3: 命令行使用
    # python audio_splitter.py audio.mp3 -i 60
    # python audio_splitter.py audio.mp3 -n 5
    
    print("\n使用说明:")
    print("1. 函数调用:")
    print("   from audio_splitter import split_audio")
    print("   split_audio('audio.mp3', interval_seconds=60)")
    print("\n2. 命令行:")
    print("   python audio_splitter.py audio.mp3 -i 60")
    print("   python audio_splitter.py audio.mp3 -n 5")
    print("\n需要安装依赖: pip install pydub")
    print("如果处理MP3文件，还需要安装: brew install ffmpeg (Mac) 或 apt-get install ffmpeg (Linux)")

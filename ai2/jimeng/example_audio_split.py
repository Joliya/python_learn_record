"""
音频分割工具使用示例
"""

from audio_splitter import split_audio, split_audio_by_count


def example_1_split_by_interval():
    """示例1: 按时间间隔分割"""
    print("=" * 60)
    print("示例1: 按时间间隔分割音频")
    print("=" * 60)
    
    # 将音频文件每60秒分割一次
    output_files = split_audio(
        audio_file_path="path/to/your/audio.mp3",
        interval_seconds=60,  # 每60秒分割
        output_folder_name="split_audio"  # 输出到 split_audio 子文件夹
    )
    
    print(f"\n生成了 {len(output_files)} 个文件")


def example_2_split_by_count():
    """示例2: 按数量分割"""
    print("=" * 60)
    print("示例2: 按数量平均分割音频")
    print("=" * 60)
    
    # 将音频文件平均分割为5个文件
    output_files = split_audio_by_count(
        audio_file_path="path/to/your/audio.mp3",
        num_parts=5,  # 分割为5个文件
        output_folder_name="split_audio"
    )
    
    print(f"\n生成了 {len(output_files)} 个文件")


def example_3_custom_interval():
    """示例3: 自定义时间间隔"""
    print("=" * 60)
    print("示例3: 自定义时间间隔分割")
    print("=" * 60)
    
    # 每30秒分割一次
    output_files = split_audio(
        audio_file_path="path/to/your/audio.mp3",
        interval_seconds=30,  # 每30秒
        output_folder_name="audio_30s"
    )
    
    print(f"\n生成了 {len(output_files)} 个文件")


def example_4_batch_split():
    """示例4: 批量分割多个文件"""
    print("=" * 60)
    print("示例4: 批量分割多个音频文件")
    print("=" * 60)
    
    audio_files = [
        "audio1.mp3",
        "audio2.mp3",
        "audio3.mp3"
    ]
    
    for audio_file in audio_files:
        try:
            print(f"\n处理文件: {audio_file}")
            output_files = split_audio(
                audio_file_path=audio_file,
                interval_seconds=60,
                output_folder_name="split_audio"
            )
            print(f"完成! 生成 {len(output_files)} 个文件")
        except Exception as e:
            print(f"错误: {e}")


def example_5_with_error_handling():
    """示例5: 带错误处理的分割"""
    print("=" * 60)
    print("示例5: 带错误处理的音频分割")
    print("=" * 60)
    
    audio_file = "path/to/your/audio.mp3"
    
    try:
        output_files = split_audio(
            audio_file_path=audio_file,
            interval_seconds=60,
            output_folder_name="split_audio"
        )
        
        print(f"\n✅ 分割成功!")
        print(f"生成了 {len(output_files)} 个文件:")
        for i, file_path in enumerate(output_files, 1):
            print(f"  {i}. {file_path}")
            
    except FileNotFoundError as e:
        print(f"❌ 文件不存在: {e}")
    except ValueError as e:
        print(f"❌ 参数错误: {e}")
    except Exception as e:
        print(f"❌ 发生错误: {e}")


if __name__ == "__main__":
    print("音频分割工具使用示例\n")
    
    # 取消注释以运行示例
    # example_1_split_by_interval()
    # example_2_split_by_count()
    # example_3_custom_interval()
    # example_4_batch_split()
    # example_5_with_error_handling()
    
    print("\n使用说明:")
    print("1. 安装依赖:")
    print("   pip install pydub")
    print("   brew install ffmpeg  # Mac")
    print("   apt-get install ffmpeg  # Linux")
    print("\n2. 修改示例中的文件路径")
    print("3. 取消注释相应的示例函数")
    print("4. 运行: python example_audio_split.py")

"""
数字人快速模式使用示例
演示如何使用即梦AI生成数字人视频
"""

from jimeng_video import (
    JimengVideoClient,
    AvatarDriveMode,
    AvatarQuality,
    create_avatar_video
)


def example_audio_driven():
    """示例1: 音频驱动数字人"""
    print("=== 示例1: 音频驱动数字人 ===")
    
    # 初始化客户端
    client = JimengVideoClient(
        access_key="your_access_key",
        secret_key="your_secret_key"
    )
    
    try:
        # 生成数字人视频
        result = client.generate_avatar_and_wait(
            image_url="https://example.com/avatar.jpg",  # 数字人图片URL
            drive_mode=AvatarDriveMode.AUDIO.value,
            audio_url="https://example.com/speech.mp3",  # 音频URL
            quality=AvatarQuality.HIGH.value,
            resolution="1080p"
        )
        
        print(f"任务ID: {result.get('task_id')}")
        print(f"视频URL: {result.get('video_url')}")
        print(f"状态: {result.get('status')}")
        
    except Exception as e:
        print(f"生成失败: {e}")
    finally:
        client.session.close()


def example_text_driven():
    """示例2: 文本驱动数字人（TTS）"""
    print("\n=== 示例2: 文本驱动数字人（TTS） ===")
    
    client = JimengVideoClient(
        access_key="your_access_key",
        secret_key="your_secret_key"
    )
    
    try:
        # 使用文本生成数字人视频
        result = client.generate_avatar_and_wait(
            image_url="https://example.com/avatar.jpg",
            drive_mode=AvatarDriveMode.TEXT.value,
            text="大家好，我是AI数字人，很高兴见到大家！",  # 要说的文本
            voice_type="zh_female_qingxin",  # 声音类型
            quality=AvatarQuality.HIGH.value
        )
        
        print(f"任务ID: {result.get('task_id')}")
        print(f"视频URL: {result.get('video_url')}")
        
    except Exception as e:
        print(f"生成失败: {e}")
    finally:
        client.session.close()


def example_video_driven():
    """示例3: 视频驱动数字人"""
    print("\n=== 示例3: 视频驱动数字人 ===")
    
    client = JimengVideoClient(
        access_key="your_access_key",
        secret_key="your_secret_key"
    )
    
    try:
        # 使用视频驱动数字人
        result = client.generate_avatar_and_wait(
            image_url="https://example.com/avatar.jpg",
            drive_mode=AvatarDriveMode.VIDEO.value,
            video_url="https://example.com/driving_video.mp4",  # 驱动视频
            quality=AvatarQuality.HIGH.value
        )
        
        print(f"任务ID: {result.get('task_id')}")
        print(f"视频URL: {result.get('video_url')}")
        
    except Exception as e:
        print(f"生成失败: {e}")
    finally:
        client.session.close()


def example_with_progress():
    """示例4: 带进度回调的数字人生成"""
    print("\n=== 示例4: 带进度回调 ===")
    
    def progress_callback(task_id, progress, status):
        """进度回调函数"""
        print(f"任务 {task_id} - 进度: {progress}% - 状态: {status}")
    
    client = JimengVideoClient(
        access_key="your_access_key",
        secret_key="your_secret_key"
    )
    
    try:
        result = client.generate_avatar_and_wait(
            image_url="https://example.com/avatar.jpg",
            drive_mode=AvatarDriveMode.TEXT.value,
            text="这是一个带进度显示的示例",
            progress_callback=progress_callback  # 传入回调函数
        )
        
        print(f"生成完成！视频URL: {result.get('video_url')}")
        
    except Exception as e:
        print(f"生成失败: {e}")
    finally:
        client.session.close()


def example_quick_create():
    """示例5: 使用便捷函数快速创建"""
    print("\n=== 示例5: 便捷函数快速创建 ===")
    
    try:
        # 使用便捷函数，一行代码完成
        result = create_avatar_video(
            access_key="your_access_key",
            secret_key="your_secret_key",
            image_url="https://example.com/avatar.jpg",
            drive_mode="text",
            text="使用便捷函数快速创建数字人视频",
            quality="high",
            save_path="./output/avatar_video.mp4"  # 自动下载到本地
        )
        
        print(f"视频已保存到: {result.get('local_path')}")
        
    except Exception as e:
        print(f"生成失败: {e}")


def example_with_background_music():
    """示例6: 添加背景音乐"""
    print("\n=== 示例6: 添加背景音乐 ===")
    
    client = JimengVideoClient(
        access_key="your_access_key",
        secret_key="your_secret_key"
    )
    
    try:
        result = client.generate_avatar_and_wait(
            image_url="https://example.com/avatar.jpg",
            drive_mode=AvatarDriveMode.TEXT.value,
            text="这段视频有背景音乐",
            background_music="https://example.com/bgm.mp3",  # 背景音乐
            quality=AvatarQuality.HIGH.value
        )
        
        print(f"视频URL: {result.get('video_url')}")
        
    except Exception as e:
        print(f"生成失败: {e}")
    finally:
        client.session.close()


def example_custom_params():
    """示例7: 使用自定义参数"""
    print("\n=== 示例7: 自定义参数 ===")
    
    client = JimengVideoClient(
        access_key="your_access_key",
        secret_key="your_secret_key"
    )
    
    try:
        # 使用自定义参数进行更精细的控制
        custom_params = {
            'fps': 30,
            'bitrate': '5000k',
            'expression_intensity': 0.8,  # 表情强度
            'head_motion': True,  # 启用头部运动
        }
        
        result = client.generate_avatar_and_wait(
            image_url="https://example.com/avatar.jpg",
            drive_mode=AvatarDriveMode.AUDIO.value,
            audio_url="https://example.com/speech.mp3",
            quality=AvatarQuality.ULTRA.value,
            custom_params=custom_params
        )
        
        print(f"视频URL: {result.get('video_url')}")
        
    except Exception as e:
        print(f"生成失败: {e}")
    finally:
        client.session.close()


if __name__ == "__main__":
    print("即梦AI数字人快速模式使用示例\n")
    print("请先配置你的 access_key 和 secret_key")
    print("=" * 50)
    
    # 运行示例（需要先配置密钥）
    # example_audio_driven()
    # example_text_driven()
    # example_video_driven()
    # example_with_progress()
    # example_quick_create()
    # example_with_background_music()
    # example_custom_params()
    
    print("\n所有示例代码已准备就绪！")
    print("请取消注释相应的示例函数来运行测试。")

"""
数字人快速模式使用示例 v2.0
展示正确的两步骤实现方式
"""

import time
from jimeng_video import (
    JimengVideoClient,
    AvatarDriveMode,
    AvatarQuality,
    create_avatar_video
)


def example_complete_flow():
    """示例1: 完整流程（推荐使用）"""
    print("=== 示例1: 完整流程（一键生成） ===")
    
    client = JimengVideoClient(
        access_key="your_access_key",
        secret_key="your_secret_key"
    )
    
    try:
        # 一键生成并等待完成
        # 内部自动执行：图片识别 → 视频生成 → 等待完成
        result = client.generate_avatar_and_wait(
            image_url="https://example.com/avatar.jpg",
            drive_mode=AvatarDriveMode.TEXT.value,
            text="大家好，我是AI数字人！"
        )
        
        print(f"视频URL: {result['data']['video_url']}")
        
    except Exception as e:
        print(f"生成失败: {e}")
    finally:
        client.session.close()


def example_step_by_step():
    """示例2: 分步调用（了解内部流程）"""
    print("\n=== 示例2: 分步调用 ===")
    
    client = JimengVideoClient(
        access_key="your_access_key",
        secret_key="your_secret_key"
    )
    
    try:
        # 步骤1：提交图片主体识别
        print("步骤1: 提交图片主体识别...")
        detection_result = client.submit_avatar_image_detection(
            image_url="https://example.com/avatar.jpg"
        )
        
        # 判断是同步还是异步返回
        if 'task_id' in detection_result:
            # 异步任务，需要轮询
            detection_task_id = detection_result['task_id']
            print(f"图片识别任务ID: {detection_task_id}，等待完成...")
            
            max_wait = 60
            start_time = time.time()
            
            while time.time() - start_time < max_wait:
                status_result = client.query_avatar_task(detection_task_id)
                status = status_result.get('status')
                
                if status == 'success':
                    processed_image_url = status_result['data']['image_url']
                    print("图片识别完成！")
                    break
                elif status == 'failed':
                    raise Exception(f"图片识别失败: {status_result.get('message')}")
                
                time.sleep(2)
            else:
                raise TimeoutError("图片识别超时")
        else:
            # 同步返回
            processed_image_url = detection_result['data']['image_url']
            print("图片识别完成（同步）！")
        
        # 步骤2：提交视频生成任务
        print("\n步骤2: 提交视频生成任务...")
        video_result = client.submit_avatar_video_generation(
            image_url=processed_image_url,
            drive_mode=AvatarDriveMode.TEXT.value,
            text="这是分步调用的示例"
        )
        
        video_task_id = video_result['task_id']
        print(f"视频生成任务ID: {video_task_id}")
        
        # 步骤3：等待视频生成完成
        print("\n步骤3: 等待视频生成完成...")
        max_wait = 600
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            status_result = client.query_avatar_task(video_task_id)
            status = status_result.get('status')
            progress = status_result.get('progress', 0)
            
            print(f"进度: {progress}% - 状态: {status}")
            
            if status == 'success':
                video_url = status_result['data']['video_url']
                print(f"\n视频生成完成！")
                print(f"视频URL: {video_url}")
                break
            elif status == 'failed':
                raise Exception(f"视频生成失败: {status_result.get('message')}")
            
            time.sleep(5)
        else:
            raise TimeoutError("视频生成超时")
        
    except Exception as e:
        print(f"生成失败: {e}")
    finally:
        client.session.close()


def example_audio_driven():
    """示例3: 音频驱动模式"""
    print("\n=== 示例3: 音频驱动模式 ===")
    
    client = JimengVideoClient(
        access_key="your_access_key",
        secret_key="your_secret_key"
    )
    
    try:
        result = client.generate_avatar_and_wait(
            image_url="https://example.com/avatar.jpg",
            drive_mode=AvatarDriveMode.AUDIO.value,
            audio_url="https://example.com/speech.mp3"
        )
        
        print(f"视频URL: {result['data']['video_url']}")
        
    except Exception as e:
        print(f"生成失败: {e}")
    finally:
        client.session.close()


def example_video_driven():
    """示例4: 视频驱动模式"""
    print("\n=== 示例4: 视频驱动模式 ===")
    
    client = JimengVideoClient(
        access_key="your_access_key",
        secret_key="your_secret_key"
    )
    
    try:
        result = client.generate_avatar_and_wait(
            image_url="https://example.com/avatar.jpg",
            drive_mode=AvatarDriveMode.VIDEO.value,
            video_url="https://example.com/driving_video.mp4"
        )
        
        print(f"视频URL: {result['data']['video_url']}")
        
    except Exception as e:
        print(f"生成失败: {e}")
    finally:
        client.session.close()


def example_with_progress_callback():
    """示例5: 带进度回调"""
    print("\n=== 示例5: 带进度回调 ===")
    
    def progress_callback(task_id, progress, status):
        """进度回调函数"""
        print(f"[回调] 任务 {task_id[:8]}... - 进度: {progress}% - 状态: {status}")
    
    client = JimengVideoClient(
        access_key="your_access_key",
        secret_key="your_secret_key"
    )
    
    try:
        result = client.generate_avatar_and_wait(
            image_url="https://example.com/avatar.jpg",
            drive_mode=AvatarDriveMode.TEXT.value,
            text="这是一个带进度回调的示例",
            progress_callback=progress_callback,
            poll_interval=3  # 每3秒查询一次
        )
        
        print(f"\n视频生成完成！")
        print(f"视频URL: {result['data']['video_url']}")
        
    except Exception as e:
        print(f"生成失败: {e}")
    finally:
        client.session.close()


def example_convenience_function():
    """示例6: 使用便捷函数"""
    print("\n=== 示例6: 便捷函数 ===")
    
    try:
        # 最简单的方式
        result = create_avatar_video(
            access_key="your_access_key",
            secret_key="your_secret_key",
            image_url="https://example.com/avatar.jpg",
            drive_mode="text",
            text="使用便捷函数快速创建",
            save_path="./output/avatar.mp4"  # 自动下载
        )
        
        print(f"视频已保存到: {result.get('local_path')}")
        
    except Exception as e:
        print(f"生成失败: {e}")


def example_with_voice_type():
    """示例7: 指定声音类型"""
    print("\n=== 示例7: 指定声音类型 ===")
    
    client = JimengVideoClient(
        access_key="your_access_key",
        secret_key="your_secret_key"
    )
    
    try:
        result = client.generate_avatar_and_wait(
            image_url="https://example.com/avatar.jpg",
            drive_mode=AvatarDriveMode.TEXT.value,
            text="这是使用特定声音类型的示例",
            voice_type="zh_female_qingxin"  # 中文女声-清新
        )
        
        print(f"视频URL: {result['data']['video_url']}")
        
    except Exception as e:
        print(f"生成失败: {e}")
    finally:
        client.session.close()


def example_error_handling():
    """示例8: 错误处理"""
    print("\n=== 示例8: 完善的错误处理 ===")
    
    client = JimengVideoClient(
        access_key="your_access_key",
        secret_key="your_secret_key"
    )
    
    try:
        result = client.generate_avatar_and_wait(
            image_url="https://example.com/avatar.jpg",
            drive_mode=AvatarDriveMode.TEXT.value,
            text="测试错误处理",
            max_wait_time=300  # 最多等待5分钟
        )
        
        print(f"视频URL: {result['data']['video_url']}")
        
    except ValueError as e:
        print(f"参数错误: {e}")
    except TimeoutError as e:
        print(f"任务超时: {e}")
    except Exception as e:
        print(f"其他错误: {e}")
    finally:
        client.session.close()


def example_batch_generation():
    """示例9: 批量生成"""
    print("\n=== 示例9: 批量生成 ===")
    
    client = JimengVideoClient(
        access_key="your_access_key",
        secret_key="your_secret_key"
    )
    
    texts = [
        "第一段文本内容",
        "第二段文本内容",
        "第三段文本内容"
    ]
    
    try:
        for i, text in enumerate(texts, 1):
            print(f"\n生成第 {i}/{len(texts)} 个视频...")
            
            # 提交任务（不等待）
            result = client.generate_avatar_video(
                image_url="https://example.com/avatar.jpg",
                drive_mode=AvatarDriveMode.TEXT.value,
                text=text
            )
            
            task_id = result.get('task_id')
            print(f"任务 {i} 已提交，任务ID: {task_id}")
        
        print("\n所有任务已提交，可以后续查询状态")
        
    except Exception as e:
        print(f"批量生成失败: {e}")
    finally:
        client.session.close()


def show_flow_diagram():
    """显示流程图"""
    print("\n" + "=" * 60)
    print("数字人快速模式 - 两步骤流程")
    print("=" * 60)
    print("""
用户调用 generate_avatar_and_wait()
    │
    ├─ 步骤1: 图片主体识别
    │   ├─ 调用 submit_avatar_image_detection()
    │   ├─ 等待识别完成（如果是异步）
    │   └─ 获得处理后的图片URL
    │
    ├─ 步骤2: 视频生成
    │   ├─ 调用 submit_avatar_video_generation()
    │   └─ 获得视频任务ID
    │
    └─ 步骤3: 等待视频完成
        ├─ 轮询 query_avatar_task()
        └─ 返回最终结果（包含video_url）
    """)
    print("=" * 60)


if __name__ == "__main__":
    print("数字人快速模式使用示例 v2.0")
    print("展示正确的两步骤实现方式\n")
    print("请先配置你的 access_key 和 secret_key")
    print("=" * 60)
    
    # 显示流程图
    show_flow_diagram()
    
    # 运行示例（需要先配置密钥）
    # example_complete_flow()          # 推荐：完整流程
    # example_step_by_step()           # 学习：分步调用
    # example_audio_driven()           # 音频驱动
    # example_video_driven()           # 视频驱动
    # example_with_progress_callback() # 进度回调
    # example_convenience_function()   # 便捷函数
    # example_with_voice_type()        # 声音类型
    # example_error_handling()         # 错误处理
    # example_batch_generation()       # 批量生成
    
    print("\n所有示例代码已准备就绪！")
    print("请取消注释相应的示例函数来运行测试。")
    print("\n重要提示：")
    print("- 图片识别和视频生成是两个独立步骤")
    print("- 每个步骤都有独立的任务ID")
    print("- 使用 generate_avatar_and_wait() 可自动处理全流程")

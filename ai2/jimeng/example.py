"""
即梦AI视频生成使用示例
"""

from jimeng_video import JimengVideoClient, VideoStyle, VideoResolution, create_video


def example_basic_usage():
    """基础使用示例"""
    # 初始化客户端（需要火山引擎的AK/SK）
    client = JimengVideoClient(
        access_key="your_access_key_here",  # 火山引擎Access Key
        secret_key="your_secret_key_here"   # 火山引擎Secret Key
    )
    
    # 方式1: 分步调用
    print("=== 方式1: 分步调用 ===")
    
    # 提交任务
    result = client.generate_video(
        prompt="一只可爱的小猫在花园里玩耍",
        style=VideoStyle.REALISTIC.value,
        resolution=VideoResolution.FHD_1080P.value,
        duration=5
    )
    task_id = result['task_id']
    print(f"任务已提交,task_id: {task_id}")
    
    # 查询状态
    status = client.query_task(task_id)
    print(f"任务状态: {status}")
    
    # 等待完成
    final_result = client.wait_for_completion(task_id)
    print(f"视频生成完成: {final_result}")


def example_one_step():
    """一键生成示例(推荐)"""
    print("\n=== 方式2: 一键生成(推荐) ===")
    
    client = JimengVideoClient(
        access_key="your_access_key_here",
        secret_key="your_secret_key_here"
    )
    
    # 定义进度回调函数
    def on_progress(task_id: str, progress: int, status: str):
        print(f"任务 {task_id}: 进度 {progress}%, 状态: {status}")
    
    # 一键生成并等待
    result = client.generate_and_wait(
        prompt="夕阳下的海滩,海浪轻拍着沙滩",
        style=VideoStyle.CINEMATIC.value,
        resolution=VideoResolution.FHD_1080P.value,
        duration=5,
        negative_prompt="模糊,低质量",
        progress_callback=on_progress
    )
    
    print(f"视频URL: {result.get('video_url')}")
    
    # 下载视频
    if result.get('video_url'):
        save_path = "output_video.mp4"
        client.download_video(result['video_url'], save_path)
        print(f"视频已保存到: {save_path}")


def example_context_manager():
    """使用上下文管理器"""
    print("\n=== 方式3: 使用上下文管理器 ===")
    
    with JimengVideoClient(
        access_key="your_access_key_here",
        secret_key="your_secret_key_here"
    ) as client:
        result = client.generate_and_wait(
            prompt="繁华的城市夜景,霓虹灯闪烁",
            style=VideoStyle.CINEMATIC.value,
            duration=5
        )
        print(f"生成结果: {result}")


def example_batch_generate():
    """批量生成示例"""
    print("\n=== 方式4: 批量生成 ===")
    
    client = JimengVideoClient(
        access_key="your_access_key_here",
        secret_key="your_secret_key_here"
    )
    
    prompts = [
        "春天的樱花盛开",
        "夏日的海滩度假",
        "秋天的枫叶飘落",
        "冬日的雪景"
    ]
    
    # 批量提交任务
    task_ids = client.batch_generate(
        prompts=prompts,
        style=VideoStyle.ARTISTIC.value,
        resolution=VideoResolution.HD_720P.value
    )
    
    print(f"已提交 {len(task_ids)} 个任务")
    
    # 等待所有任务完成
    results = []
    for task_id in task_ids:
        result = client.wait_for_completion(task_id)
        results.append(result)
    
    print(f"所有任务完成,共 {len(results)} 个视频")


def example_quick_create():
    """超简单的快捷方式"""
    print("\n=== 方式5: 超简单快捷方式 ===")
    
    result = create_video(
        access_key="your_access_key_here",
        secret_key="your_secret_key_here",
        prompt="一只蝴蝶在花丛中飞舞",
        style="realistic",
        resolution="1080p",
        save_path="butterfly.mp4"
    )
    
    print(f"视频已生成并保存: {result.get('local_path')}")


def example_advanced():
    """高级用法示例"""
    print("\n=== 方式6: 高级用法 ===")
    
    client = JimengVideoClient(
        access_key="your_access_key_here",
        secret_key="your_secret_key_here"
    )
    
    result = client.generate_and_wait(
        prompt="科幻风格的未来城市,飞行器穿梭其间",
        style=VideoStyle.CINEMATIC.value,
        resolution=VideoResolution.UHD_4K.value,
        duration=10,
        fps=60,
        negative_prompt="模糊,低质量,噪点,变形",
        reference_image="https://example.com/reference.jpg",  # 参考图片URL
        custom_params={
            "seed": 42,  # 随机种子
            "guidance_scale": 7.5,  # 引导强度
            "num_inference_steps": 50  # 推理步数
        }
    )
    
    print(f"高级生成完成: {result}")


if __name__ == "__main__":
    # 运行示例(请替换your_access_key_here和your_secret_key_here为真实的火山引擎密钥)
    
    # example_basic_usage()
    # example_one_step()
    # example_context_manager()
    # example_batch_generate()
    # example_quick_create()
    # example_advanced()
    
    print("\n请取消注释上面的示例函数来运行测试")
    print("注意: 运行前请先替换火山引擎的 Access Key 和 Secret Key")
    print("获取密钥: https://console.volcengine.com/iam/keymanage/")


# 即梦AI视频生成3.0 Pro 接入封装

火山引擎即梦AI视频生成接口的Python封装,提供简单易用的API。

## 🎯 功能模块

### 1. 视频生成（文生视频）
基于文本提示词生成创意视频

### 2. 数字人快速模式 🆕 v2.0
基于单张图片+驱动源生成数字人视频（**已按官方文档正确实现两步骤流程**）

**两步骤流程**：
1. 图片主体识别（`high_aes_general_v20_L`）
2. 视频生成（`avatar_video_fast`）

**支持三种驱动模式**：
- 音频驱动（AUDIO）
- 文本驱动（TEXT/TTS）
- 视频驱动（VIDEO）

👉 **[5分钟快速入门](QUICKSTART.md)** | **[完整文档](README_AVATAR.md)** | **[两步骤说明](数字人两步骤实现说明.md)** | **[v2.0更新](更新说明_v2.md)**

## 特性

- ✅ 简单易用的API设计
- ✅ 完整的类型提示
- ✅ 支持同步和异步调用
- ✅ 任务状态轮询和进度回调
- ✅ 批量生成支持
- ✅ 视频下载功能
- ✅ 上下文管理器支持
- ✅ 完善的错误处理
- ✅ **数字人快速模式** 🆕

## 安装依赖

```bash
pip install requests
```

## 快速开始

### 获取火山引擎密钥

在使用前，需要先获取火山引擎的 Access Key 和 Secret Key：
1. 访问 [火山引擎控制台](https://console.volcengine.com/iam/keymanage/)
2. 创建或查看您的 Access Key (AK) 和 Secret Key (SK)

### 最简单的用法

```python
from ai2.jimeng import create_video

# 一行代码生成视频
result = create_video(
    access_key="your_access_key",
    secret_key="your_secret_key",
    prompt="一只可爱的小猫在花园里玩耍",
    save_path="cat.mp4"
)
```

### 标准用法

```python
from ai2.jimeng import JimengVideoClient, VideoStyle, VideoResolution

# 创建客户端
client = JimengVideoClient(
    access_key="your_access_key",
    secret_key="your_secret_key"
)

# 生成视频并等待完成
result = client.generate_and_wait(
    prompt="夕阳下的海滩,海浪轻拍着沙滩",
    style=VideoStyle.CINEMATIC.value,
    resolution=VideoResolution.FHD_1080P.value,
    duration=5
)

print(f"视频URL: {result['video_url']}")

# 下载视频
client.download_video(result['video_url'], 'beach.mp4')
```

### 带进度回调

```python
def on_progress(task_id, progress, status):
    print(f"进度: {progress}%, 状态: {status}")

result = client.generate_and_wait(
    prompt="繁华的城市夜景",
    progress_callback=on_progress
)
```

### 分步调用

```python
# 1. 提交任务
submit_result = client.generate_video(
    prompt="春天的樱花盛开",
    style="realistic"
)
task_id = submit_result['task_id']

# 2. 查询状态
status = client.query_task(task_id)

# 3. 等待完成
result = client.wait_for_completion(task_id)
```

### 批量生成

```python
prompts = [
    "春天的樱花",
    "夏日的海滩",
    "秋天的枫叶",
    "冬日的雪景"
]

task_ids = client.batch_generate(prompts, style="artistic")

# 等待所有任务完成
results = [client.wait_for_completion(tid) for tid in task_ids]
```

### 使用上下文管理器

```python
with JimengVideoClient(
    access_key="your_access_key",
    secret_key="your_secret_key"
) as client:
    result = client.generate_and_wait(
        prompt="科幻未来城市"
    )
```

## API参数说明

### JimengVideoClient 初始化参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| access_key | str | 是 | - | 火山引擎Access Key (AK) |
| secret_key | str | 是 | - | 火山引擎Secret Key (SK) |
| base_url | str | 否 | https://visual.volcengineapi.com | API基础URL |
| service | str | 否 | cv | 服务名称 |
| region | str | 否 | cn-north-1 | 区域 |
| timeout | int | 否 | 30 | 请求超时时间(秒) |

### generate_and_wait 参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| prompt | str | 是 | - | 视频描述文本 |
| style | str | 否 | "default" | 视频风格 |
| resolution | str | 否 | "1080p" | 视频分辨率 |
| duration | int | 否 | 5 | 视频时长(秒) |
| fps | int | 否 | 30 | 视频帧率 |
| negative_prompt | str | 否 | None | 负面提示词 |
| reference_image | str | 否 | None | 参考图片URL |
| max_wait_time | int | 否 | 600 | 最大等待时间(秒) |
| poll_interval | int | 否 | 5 | 轮询间隔(秒) |
| progress_callback | callable | 否 | None | 进度回调函数 |
| custom_params | dict | 否 | None | 自定义参数 |

## 视频风格(VideoStyle)

- `default` - 默认风格
- `cinematic` - 电影风格
- `anime` - 动漫风格
- `realistic` - 写实风格
- `artistic` - 艺术风格

## 视频分辨率(VideoResolution)

- `480p` - 标清
- `720p` - 高清
- `1080p` - 全高清(推荐)
- `4k` - 超高清

## 返回结果示例

```python
{
    'task_id': 'xxx-xxx-xxx',
    'status': 'success',
    'progress': 100,
    'video_url': 'https://...',
    'duration': 5.2,
    'resolution': '1080p',
    'created_at': '2025-10-20T12:00:00Z'
}
```

## 错误处理

```python
try:
    result = client.generate_and_wait(prompt="...")
except TimeoutError as e:
    print(f"生成超时: {e}")
except Exception as e:
    print(f"生成失败: {e}")
```

## 高级用法

### 自定义参数

```python
result = client.generate_and_wait(
    prompt="科幻城市",
    custom_params={
        "seed": 42,  # 随机种子,用于复现
        "guidance_scale": 7.5,  # 引导强度
        "num_inference_steps": 50  # 推理步数
    }
)
```

### 使用参考图片

```python
result = client.generate_and_wait(
    prompt="根据这张图片生成视频",
    reference_image="https://example.com/image.jpg"
)
```

## 完整示例

查看 `example.py` 文件获取更多使用示例。

## API调用说明

火山引擎即梦AI使用统一的endpoint，通过`Action`参数区分不同操作：
- `SubmitTask` - 提交视频生成任务
- `GetVideoResult` - 查询任务结果

请求会自动使用火山引擎签名v4算法进行签名认证。

## 注意事项

1. 请妥善保管Access Key和Secret Key,不要泄露到代码仓库
2. 视频生成时间取决于参数设置,通常需要1-5分钟
3. 建议使用 `generate_and_wait` 方法,最简单方便
4. 批量生成时注意API调用限制和配额
5. 下载大文件时注意网络稳定性
6. 密钥获取地址: https://console.volcengine.com/iam/keymanage/

## 数字人快速模式 🆕

### 快速开始

```python
from jimeng_video import create_avatar_video

# 一行代码生成数字人视频
result = create_avatar_video(
    access_key="your_ak",
    secret_key="your_sk",
    image_url="https://example.com/avatar.jpg",
    drive_mode="text",
    text="大家好，我是AI数字人！",
    save_path="./avatar.mp4"
)
```

### 三种驱动模式

```python
from jimeng_video import JimengVideoClient, AvatarDriveMode

client = JimengVideoClient(access_key="your_ak", secret_key="your_sk")

# 1. 音频驱动
result = client.generate_avatar_and_wait(
    image_url="https://example.com/avatar.jpg",
    drive_mode=AvatarDriveMode.AUDIO.value,
    audio_url="https://example.com/speech.mp3"
)

# 2. 文本驱动（TTS）
result = client.generate_avatar_and_wait(
    image_url="https://example.com/avatar.jpg",
    drive_mode=AvatarDriveMode.TEXT.value,
    text="要说的内容",
    voice_type="zh_female_qingxin"
)

# 3. 视频驱动
result = client.generate_avatar_and_wait(
    image_url="https://example.com/avatar.jpg",
    drive_mode=AvatarDriveMode.VIDEO.value,
    video_url="https://example.com/driving_video.mp4"
)
```

### 更多文档

- 📖 [5分钟快速入门](QUICKSTART.md)
- 📚 [完整使用指南](README_AVATAR.md)
- 💻 [示例代码](example_avatar.py)
- 📋 [更新说明](数字人功能更新说明.md)

## 文档链接

- [火山引擎即梦AI视频生成文档](https://www.volcengine.com/docs/85621/1777001)
- [火山引擎数字人API文档](https://www.volcengine.com/docs/85621/1810469)

## License

MIT


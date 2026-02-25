# 即梦AI数字人快速模式使用指南

## 功能概述

数字人快速模式支持通过单张图片+驱动源（音频/文本/视频）快速生成数字人视频。

### 支持的驱动模式

1. **音频驱动** (`audio`): 使用音频文件驱动数字人说话
2. **文本驱动** (`text`): 使用文本通过TTS生成语音并驱动数字人
3. **视频驱动** (`video`): 使用视频驱动数字人的动作和表情

## 快速开始

### 1. 基础使用

```python
from jimeng_video import JimengVideoClient, AvatarDriveMode, AvatarQuality

# 初始化客户端
client = JimengVideoClient(
    access_key="your_access_key",
    secret_key="your_secret_key"
)

# 音频驱动模式
result = client.generate_avatar_and_wait(
    image_url="https://example.com/avatar.jpg",
    drive_mode=AvatarDriveMode.AUDIO.value,
    audio_url="https://example.com/speech.mp3",
    quality=AvatarQuality.HIGH.value
)

print(f"视频URL: {result['video_url']}")
```

### 2. 文本驱动（TTS）

```python
# 使用文本生成数字人视频
result = client.generate_avatar_and_wait(
    image_url="https://example.com/avatar.jpg",
    drive_mode=AvatarDriveMode.TEXT.value,
    text="大家好，我是AI数字人！",
    voice_type="zh_female_qingxin",  # 可选：指定声音类型
    quality=AvatarQuality.HIGH.value
)
```

### 3. 视频驱动

```python
# 使用视频驱动数字人
result = client.generate_avatar_and_wait(
    image_url="https://example.com/avatar.jpg",
    drive_mode=AvatarDriveMode.VIDEO.value,
    video_url="https://example.com/driving_video.mp4",
    quality=AvatarQuality.HIGH.value
)
```

### 4. 便捷函数（推荐）

```python
from jimeng_video import create_avatar_video

# 一行代码完成数字人视频生成
result = create_avatar_video(
    access_key="your_access_key",
    secret_key="your_secret_key",
    image_url="https://example.com/avatar.jpg",
    drive_mode="text",
    text="这是最简单的使用方式",
    quality="high",
    save_path="./output/avatar.mp4"  # 自动下载到本地
)
```

## API参数说明

### generate_avatar_video()

提交数字人视频生成任务。

**参数：**

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `image_url` | str | 是 | 数字人图片URL或base64编码 |
| `drive_mode` | str | 是 | 驱动模式：audio/text/video |
| `audio_url` | str | 条件 | 音频URL（audio模式必填） |
| `text` | str | 条件 | 文本内容（text模式必填） |
| `video_url` | str | 条件 | 视频URL（video模式必填） |
| `quality` | str | 否 | 视频质量：low/medium/high/ultra |
| `resolution` | str | 否 | 分辨率，默认1080p |
| `voice_type` | str | 否 | 声音类型（text模式可用） |
| `background_music` | str | 否 | 背景音乐URL |
| `custom_params` | dict | 否 | 自定义参数 |

**返回值：**

```python
{
    'task_id': 'xxx',
    'status': 'pending',
    'message': 'Task submitted successfully'
}
```

### generate_avatar_and_wait()

一键生成并等待完成（推荐使用）。

**额外参数：**

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `max_wait_time` | int | 600 | 最大等待时间（秒） |
| `poll_interval` | int | 5 | 轮询间隔（秒） |
| `progress_callback` | callable | None | 进度回调函数 |

**返回值：**

```python
{
    'task_id': 'xxx',
    'status': 'success',
    'video_url': 'https://...',
    'duration': 10.5,
    'resolution': '1080p'
}
```

## 枚举类型

### AvatarDriveMode（驱动模式）

```python
class AvatarDriveMode(Enum):
    AUDIO = "audio"   # 音频驱动
    VIDEO = "video"   # 视频驱动
    TEXT = "text"     # 文本驱动（TTS）
```

### AvatarQuality（视频质量）

```python
class AvatarQuality(Enum):
    LOW = "low"       # 低质量，快速生成
    MEDIUM = "medium" # 中等质量
    HIGH = "high"     # 高质量
    ULTRA = "ultra"   # 超高质量
```

## 高级用法

### 1. 进度回调

```python
def progress_callback(task_id, progress, status):
    print(f"任务 {task_id} - 进度: {progress}% - 状态: {status}")

result = client.generate_avatar_and_wait(
    image_url="https://example.com/avatar.jpg",
    drive_mode="text",
    text="带进度显示的示例",
    progress_callback=progress_callback
)
```

### 2. 添加背景音乐

```python
result = client.generate_avatar_and_wait(
    image_url="https://example.com/avatar.jpg",
    drive_mode="text",
    text="这段视频有背景音乐",
    background_music="https://example.com/bgm.mp3"
)
```

### 3. 自定义参数

```python
custom_params = {
    'fps': 30,
    'bitrate': '5000k',
    'expression_intensity': 0.8,  # 表情强度
    'head_motion': True,          # 启用头部运动
}

result = client.generate_avatar_and_wait(
    image_url="https://example.com/avatar.jpg",
    drive_mode="audio",
    audio_url="https://example.com/speech.mp3",
    custom_params=custom_params
)
```

### 4. 批量生成

```python
images = [
    "https://example.com/avatar1.jpg",
    "https://example.com/avatar2.jpg",
    "https://example.com/avatar3.jpg"
]

texts = [
    "第一段文本",
    "第二段文本",
    "第三段文本"
]

for image, text in zip(images, texts):
    result = client.generate_avatar_video(
        image_url=image,
        drive_mode="text",
        text=text
    )
    print(f"已提交任务: {result['task_id']}")
```

## 错误处理

```python
try:
    result = client.generate_avatar_and_wait(
        image_url="https://example.com/avatar.jpg",
        drive_mode="text",
        text="测试文本"
    )
except ValueError as e:
    print(f"参数错误: {e}")
except TimeoutError as e:
    print(f"任务超时: {e}")
except Exception as e:
    print(f"生成失败: {e}")
```

## 注意事项

1. **图片要求**：
   - 建议使用正面清晰的人像照片
   - 分辨率建议不低于512x512
   - 支持JPG、PNG格式

2. **音频要求**：
   - 支持MP3、WAV等常见格式
   - 建议采样率16kHz或以上
   - 音频时长决定视频时长

3. **文本要求**：
   - 支持中英文混合
   - 建议单次文本不超过500字
   - 可使用标点符号控制停顿

4. **性能优化**：
   - 使用`LOW`或`MEDIUM`质量可加快生成速度
   - 批量任务建议使用异步提交+轮询查询
   - 合理设置`max_wait_time`避免长时间等待

## 完整示例

查看 `example_avatar.py` 文件获取更多完整示例代码。

## 常见问题

**Q: 如何选择合适的质量等级？**

A: 
- `LOW`: 适合快速预览，生成速度快
- `MEDIUM`: 平衡质量和速度，适合大多数场景
- `HIGH`: 高质量输出，适合正式使用
- `ULTRA`: 最高质量，适合专业制作

**Q: 文本驱动模式支持哪些声音类型？**

A: 常见的声音类型包括：
- `zh_female_qingxin`: 中文女声-清新
- `zh_male_chenwen`: 中文男声-沉稳
- `en_female_bella`: 英文女声
- 更多声音类型请参考火山引擎官方文档

**Q: 如何处理长文本？**

A: 建议将长文本分段处理：
```python
long_text = "很长的文本..."
segments = [long_text[i:i+200] for i in range(0, len(long_text), 200)]

for i, segment in enumerate(segments):
    result = client.generate_avatar_video(
        image_url="https://example.com/avatar.jpg",
        drive_mode="text",
        text=segment
    )
    print(f"段落 {i+1} 任务ID: {result['task_id']}")
```

## 相关链接

- [火山引擎官方文档](https://www.volcengine.com/docs/85621/1810469)
- [即梦AI产品页](https://www.volcengine.com/product/jimeng)

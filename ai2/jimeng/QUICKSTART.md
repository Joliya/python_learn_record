# 🚀 数字人快速模式 - 5分钟快速入门

## 第一步：导入库

```python
from jimeng_video import (
    JimengVideoClient,
    AvatarDriveMode,
    AvatarQuality,
    create_avatar_video  # 便捷函数
)
```

## 第二步：选择使用方式

### 方式1：便捷函数（推荐新手）

**最简单！一行代码搞定！**

```python
# 文本驱动
result = create_avatar_video(
    access_key="你的AK",
    secret_key="你的SK",
    image_url="https://example.com/avatar.jpg",
    drive_mode="text",
    text="大家好，我是AI数字人！",
    save_path="./avatar.mp4"  # 自动下载
)
```

### 方式2：完整控制（推荐进阶）

**更多控制！支持回调和自定义参数！**

```python
# 创建客户端
client = JimengVideoClient(
    access_key="你的AK",
    secret_key="你的SK"
)

# 生成数字人视频
result = client.generate_avatar_and_wait(
    image_url="https://example.com/avatar.jpg",
    drive_mode=AvatarDriveMode.TEXT.value,
    text="大家好，我是AI数字人！",
    quality=AvatarQuality.HIGH.value
)

print(f"视频URL: {result['video_url']}")
```

## 第三步：选择驱动模式

### 🎵 模式1：音频驱动（有录音文件）

```python
result = client.generate_avatar_and_wait(
    image_url="https://example.com/avatar.jpg",
    drive_mode=AvatarDriveMode.AUDIO.value,
    audio_url="https://example.com/speech.mp3"
)
```

**适用场景**：
- 已有录制好的音频
- 需要精确控制语音
- 多语言场景

### 📝 模式2：文本驱动（最常用）

```python
result = client.generate_avatar_and_wait(
    image_url="https://example.com/avatar.jpg",
    drive_mode=AvatarDriveMode.TEXT.value,
    text="要说的内容",
    voice_type="zh_female_qingxin"  # 可选
)
```

**适用场景**：
- 动态文本内容
- 快速生成
- 不同声音选择

### 🎬 模式3：视频驱动（动作迁移）

```python
result = client.generate_avatar_and_wait(
    image_url="https://example.com/avatar.jpg",
    drive_mode=AvatarDriveMode.VIDEO.value,
    video_url="https://example.com/driving_video.mp4"
)
```

**适用场景**：
- 复制特定动作
- 表情迁移
- 动作模仿

## 第四步：选择质量等级

```python
# 快速预览
quality=AvatarQuality.LOW.value

# 日常使用（推荐）
quality=AvatarQuality.MEDIUM.value

# 正式发布
quality=AvatarQuality.HIGH.value

# 专业制作
quality=AvatarQuality.ULTRA.value
```

## 完整示例

### 示例1：最简单的方式

```python
from jimeng_video import create_avatar_video

# 一行代码完成
result = create_avatar_video(
    access_key="你的AK",
    secret_key="你的SK",
    image_url="https://example.com/avatar.jpg",
    drive_mode="text",
    text="欢迎使用数字人快速模式！",
    save_path="./my_avatar.mp4"
)

print("完成！视频已保存到:", result['local_path'])
```

### 示例2：带进度显示

```python
from jimeng_video import JimengVideoClient, AvatarDriveMode

# 进度回调函数
def show_progress(task_id, progress, status):
    print(f"进度: {progress}% - 状态: {status}")

# 创建客户端
client = JimengVideoClient(
    access_key="你的AK",
    secret_key="你的SK"
)

# 生成并显示进度
result = client.generate_avatar_and_wait(
    image_url="https://example.com/avatar.jpg",
    drive_mode=AvatarDriveMode.TEXT.value,
    text="这是一个带进度显示的示例",
    progress_callback=show_progress
)

print("完成！视频URL:", result['video_url'])
```

### 示例3：添加背景音乐

```python
result = client.generate_avatar_and_wait(
    image_url="https://example.com/avatar.jpg",
    drive_mode=AvatarDriveMode.TEXT.value,
    text="这段视频有背景音乐",
    background_music="https://example.com/bgm.mp3"
)
```

## 常见问题速查

### Q1: 如何获取AK/SK？
登录火山引擎控制台 → 访问密钥管理 → 创建密钥

### Q2: 图片有什么要求？
- 正面清晰人像
- 分辨率 ≥ 512x512
- JPG或PNG格式

### Q3: 文本有长度限制吗？
建议单次不超过500字，长文本可分段处理

### Q4: 生成需要多长时间？
- LOW质量: 1-2分钟
- MEDIUM质量: 2-3分钟
- HIGH质量: 3-5分钟
- ULTRA质量: 5-10分钟

### Q5: 如何处理错误？

```python
try:
    result = create_avatar_video(...)
except ValueError as e:
    print(f"参数错误: {e}")
except TimeoutError as e:
    print(f"超时: {e}")
except Exception as e:
    print(f"其他错误: {e}")
```

## 下一步

1. 📖 查看完整文档: `README_AVATAR.md`
2. 💻 运行示例代码: `example_avatar.py`
3. 🧪 运行测试: `test_avatar.py`
4. 📚 阅读更新说明: `数字人功能更新说明.md`

## 快速参考

### 驱动模式
- `"audio"` - 音频驱动
- `"text"` - 文本驱动
- `"video"` - 视频驱动

### 质量等级
- `"low"` - 低质量（快）
- `"medium"` - 中等质量
- `"high"` - 高质量
- `"ultra"` - 超高质量

### 常用声音类型
- `"zh_female_qingxin"` - 中文女声-清新
- `"zh_male_chenwen"` - 中文男声-沉稳
- `"en_female_bella"` - 英文女声

## 开始使用

```python
# 复制这段代码，替换AK/SK后即可运行
from jimeng_video import create_avatar_video

result = create_avatar_video(
    access_key="替换为你的AK",
    secret_key="替换为你的SK",
    image_url="https://example.com/avatar.jpg",
    drive_mode="text",
    text="你好，世界！",
    quality="high",
    save_path="./my_first_avatar.mp4"
)

print("成功！", result)
```

---

**🎉 恭喜！你已经掌握了数字人快速模式的基本用法！**

需要更多帮助？查看 `README_AVATAR.md` 获取详细文档。

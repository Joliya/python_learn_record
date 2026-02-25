# 音频分割工具

将MP3等音频文件按照指定时间间隔分割为多个文件，并保存到原文件所在文件夹的子文件夹中。

## 📦 安装依赖

```bash
# 安装Python库
pip install pydub

# 安装ffmpeg（必需）
# Mac
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Windows
# 下载ffmpeg并添加到PATH: https://ffmpeg.org/download.html
```

## 🚀 快速开始

### 方式1: Python函数调用

```python
from audio_splitter import split_audio

# 按时间间隔分割
output_files = split_audio(
    audio_file_path="my_audio.mp3",
    interval_seconds=60,  # 每60秒分割一次
    output_folder_name="split_audio"  # 输出到子文件夹
)

print(f"生成了 {len(output_files)} 个文件")
```

### 方式2: 命令行使用

```bash
# 按时间间隔分割（每60秒）
python audio_splitter.py my_audio.mp3 -i 60

# 按数量分割（分为5个文件）
python audio_splitter.py my_audio.mp3 -n 5

# 指定输出文件夹
python audio_splitter.py my_audio.mp3 -i 30 -o my_output_folder
```

## 📖 功能说明

### 1. 按时间间隔分割

```python
from audio_splitter import split_audio

output_files = split_audio(
    audio_file_path="audio.mp3",
    interval_seconds=60,  # 每60秒分割
    output_folder_name="split_audio"
)
```

**参数说明**：
- `audio_file_path`: 音频文件路径（支持MP3、WAV、M4A等格式）
- `interval_seconds`: 分割时间间隔（秒）
- `output_folder_name`: 输出子文件夹名称，默认"split_audio"

**返回值**：
- 分割后的文件路径列表

### 2. 按数量分割

```python
from audio_splitter import split_audio_by_count

output_files = split_audio_by_count(
    audio_file_path="audio.mp3",
    num_parts=5,  # 分割为5个文件
    output_folder_name="split_audio"
)
```

**参数说明**：
- `audio_file_path`: 音频文件路径
- `num_parts`: 分割数量
- `output_folder_name`: 输出子文件夹名称

## 💡 使用示例

### 示例1: 基本使用

```python
from audio_splitter import split_audio

# 将音频每60秒分割一次
output_files = split_audio(
    audio_file_path="/path/to/my_audio.mp3",
    interval_seconds=60
)

# 输出文件将保存在: /path/to/split_audio/
# 文件名格式: my_audio_part_001.mp3, my_audio_part_002.mp3, ...
```

### 示例2: 自定义输出文件夹

```python
output_files = split_audio(
    audio_file_path="podcast.mp3",
    interval_seconds=300,  # 每5分钟分割
    output_folder_name="podcast_segments"
)
```

### 示例3: 平均分割

```python
from audio_splitter import split_audio_by_count

# 将音频平均分为10个文件
output_files = split_audio_by_count(
    audio_file_path="long_audio.mp3",
    num_parts=10
)
```

### 示例4: 批量处理

```python
import os
from audio_splitter import split_audio

audio_folder = "/path/to/audio_files"

for filename in os.listdir(audio_folder):
    if filename.endswith(".mp3"):
        audio_path = os.path.join(audio_folder, filename)
        try:
            output_files = split_audio(
                audio_file_path=audio_path,
                interval_seconds=60
            )
            print(f"✅ {filename}: 生成 {len(output_files)} 个文件")
        except Exception as e:
            print(f"❌ {filename}: {e}")
```

### 示例5: 带错误处理

```python
from audio_splitter import split_audio

try:
    output_files = split_audio(
        audio_file_path="audio.mp3",
        interval_seconds=60
    )
    print(f"成功! 生成 {len(output_files)} 个文件")
    
except FileNotFoundError:
    print("错误: 文件不存在")
except ValueError as e:
    print(f"参数错误: {e}")
except Exception as e:
    print(f"发生错误: {e}")
```

## 📂 输出文件结构

```
原文件目录/
├── my_audio.mp3          # 原始文件
└── split_audio/          # 输出文件夹
    ├── my_audio_part_001.mp3
    ├── my_audio_part_002.mp3
    ├── my_audio_part_003.mp3
    └── ...
```

## 🎯 命令行参数

```bash
python audio_splitter.py <音频文件> [选项]

选项:
  -i, --interval SECONDS    分割时间间隔（秒），默认60秒
  -n, --num-parts NUMBER    分割数量（与-i互斥）
  -o, --output FOLDER       输出文件夹名称，默认'split_audio'
  -h, --help               显示帮助信息
```

### 命令行示例

```bash
# 每60秒分割一次
python audio_splitter.py podcast.mp3 -i 60

# 分割为5个文件
python audio_splitter.py podcast.mp3 -n 5

# 每30秒分割，输出到custom_folder
python audio_splitter.py audio.mp3 -i 30 -o custom_folder

# 每2分钟分割
python audio_splitter.py lecture.mp3 -i 120
```

## 🎨 支持的音频格式

- MP3
- WAV
- M4A
- FLAC
- OGG
- AAC
- 其他pydub支持的格式

## ⚙️ 工作原理

1. **加载音频**: 使用pydub加载音频文件
2. **计算分割点**: 根据时间间隔或数量计算分割位置
3. **提取片段**: 按照分割点提取音频片段
4. **导出文件**: 将每个片段导出为独立文件
5. **保存到子文件夹**: 所有分割文件保存到指定子文件夹

## 📊 性能说明

- **处理速度**: 取决于音频文件大小和格式
- **内存占用**: 整个音频文件会加载到内存
- **建议**: 对于超大文件（>500MB），建议分批处理

## ⚠️ 注意事项

1. **ffmpeg依赖**: 必须安装ffmpeg才能处理MP3等格式
2. **文件覆盖**: 如果输出文件夹已存在同名文件，会被覆盖
3. **磁盘空间**: 确保有足够的磁盘空间存储分割后的文件
4. **文件路径**: 支持相对路径和绝对路径

## 🐛 常见问题

### Q1: 提示"ffmpeg not found"
**A**: 需要安装ffmpeg
```bash
# Mac
brew install ffmpeg

# Ubuntu
sudo apt-get install ffmpeg
```

### Q2: 分割后的文件音质下降
**A**: pydub默认使用原始音频的编码参数，不会降低音质

### Q3: 如何处理大文件？
**A**: 对于超大文件，可以：
- 增加系统内存
- 使用更小的分割间隔
- 考虑使用流式处理（需要自定义实现）

### Q4: 支持视频文件吗？
**A**: 可以提取视频中的音频轨道，但需要修改代码

## 📝 完整示例代码

```python
from audio_splitter import split_audio, split_audio_by_count

# 示例1: 按时间分割
output_files = split_audio(
    audio_file_path="my_podcast.mp3",
    interval_seconds=300,  # 每5分钟
    output_folder_name="podcast_parts"
)

print(f"生成了 {len(output_files)} 个文件:")
for i, file_path in enumerate(output_files, 1):
    print(f"{i}. {file_path}")

# 示例2: 按数量分割
output_files = split_audio_by_count(
    audio_file_path="lecture.mp3",
    num_parts=10,  # 分为10个文件
    output_folder_name="lecture_parts"
)
```

## 🔗 相关文件

- `audio_splitter.py` - 核心工具文件
- `example_audio_split.py` - 使用示例
- `README_AUDIO_SPLITTER.md` - 本文档

## 📄 License

MIT

---

**创建时间**: 2025年10月21日  
**版本**: v1.0.0

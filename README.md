# douyin-tools 🎬

抖音视频下载、音频提取、转文字工具集。

> 由 [heer-labs](https://github.com/heer-labs) 维护

## 功能

- ✅ **视频下载** — 从抖音下载无水印视频
- ✅ **音频提取** — 从视频中提取 MP3 音频
- ✅ **语音转文字** — 使用 whisper 将音频转为文字
- ✅ **批量处理** — 支持批量下载和转换

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 下载单个视频
python douyin_extractor.py --url "https://v.douyin.com/xxxxx/"

# 批量下载
python douyin_extractor.py --file urls.txt

# 提取音频并转文字
python douyin_extractor.py --url "https://v.douyin.com/xxxxx/" --transcribe
```

## 依赖

- Python 3.8+
- ffmpeg（用于音频提取）
- openai-whisper（用于语音转文字）
- playwright（用于页面数据拦截）

## 项目结构

```
douyin-tools/
├── douyin_extractor.py   # 核心工具
├── requirements.txt      # Python 依赖
├── README.md             # 本文件
└── examples/             # 使用示例
```

## License

MIT

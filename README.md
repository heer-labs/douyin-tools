# douyin-tools 🎬

面向短视频运营的实用工具集：素材整理、音频提取、转文字、脚本 brief 生成。

> 由 [heer-labs](https://github.com/heer-labs) 维护。定位不是“炫技项目”，而是能给个体商家/博主交付结果的小工具。

## 能解决什么

- ✅ **视频/音频处理**：视频直链下载、MP3 音频提取
- ✅ **语音转文字**：配合 Whisper 做口播/直播录音转写
- ✅ **内容 Brief 生成**：把乱文本整理成选题、钩子、脚本、标题、拍摄清单
- ✅ **批量处理思路**：适合给短视频博主、商家、接单客户定制

## 快速开始

```bash
# 安装依赖（基础 brief 生成不需要第三方依赖）
pip install -r requirements.txt

# 生成短视频脚本 brief
python content_brief_generator.py \
  --text "瘦子增肌总是吃不够，训练也不知道从哪开始，练了一个月没变化" \
  --niche "瘦子增肌" \
  --audience "健身新手" \
  -o brief.md

# 提取视频 ID / 音频 / 转文字相关能力
python douyin_extractor.py --url "https://v.douyin.com/xxxxx/"
python douyin_extractor.py --url "https://v.douyin.com/xxxxx/" --transcribe
```

## 接单服务方向

如果你需要的是“能直接干活的自动化脚本”，可以参考这些定制方向：

| 类型 | 可做内容 | 参考价格 |
|---|---|---:|
| 爬虫/采集 | 商品、账号、评论、表格数据采集 | 500-2000 |
| 办公自动化 | Excel 合并拆分、文件整理、图片压缩、批量重命名 | 300-800 |
| 短视频运营工具 | 文案整理、字幕/口播处理、选题 brief、素材归档 | 300-1500 |
| 数据清洗 | CSV/Excel 去重、格式转换、报表生成 | 200-500 |

## 项目结构

```
douyin-tools/
├── content_brief_generator.py  # 短视频脚本 brief 生成器
├── douyin_extractor.py         # 视频/音频/转文字工具
├── requirements.txt            # Python 依赖
└── README.md                   # 本文件
```

## 注意

- `content_brief_generator.py` 是无依赖工具，适合展示和快速交付。
- 抖音下载相关能力受平台限制影响，实际商用建议按客户授权和合规范围做。
- 本仓库会逐步沉淀 heer-labs 的自动化接单案例。

## License

MIT

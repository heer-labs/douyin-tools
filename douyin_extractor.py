# douyin-tools - 抖音工具集
# 核心提取器 - 支持视频下载、音频提取、语音转文字

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import requests
except ImportError:
    requests = None

try:
    import whisper
except ImportError:
    whisper = None


def extract_video_id(url: str) -> str:
    """从抖音链接中提取视频ID"""
    patterns = [
        r'video/(\d+)',
        r'v.douyin.com/(\w+)',
        r'share/video/(\d+)',
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)
    return ""


def download_video(url: str, output_dir: str = ".") -> str | None:
    """
    下载抖音视频（需配合 Playwright 获取真实视频地址）
    
    实际使用中，需要通过 Playwright 拦截 API 获取视频直链。
    详见 README。
    """
    print(f"[douyin-tools] 准备下载: {url}")
    print("[douyin-tools] 请使用 Playwright 获取视频直链后调用 download_from_url()")
    return None


def download_from_url(video_url: str, output_path: str) -> str | None:
    """从视频直链下载"""
    if not requests:
        print("[douyin-tools] 需要安装 requests: pip install requests")
        return None
    
    try:
        r = requests.get(video_url, stream=True, timeout=30)
        r.raise_for_status()
        with open(output_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"[douyin-tools] ✅ 下载完成: {output_path}")
        return output_path
    except Exception as e:
        print(f"[douyin-tools] ❌ 下载失败: {e}")
        return None


def extract_audio(video_path: str, audio_path: str | None = None) -> str | None:
    """从视频中提取音频"""
    if audio_path is None:
        audio_path = str(Path(video_path).with_suffix(".mp3"))
    
    try:
        subprocess.run(
            ["ffmpeg", "-i", video_path, "-vn", "-acodec", "libmp3lame",
             "-q:a", "4", audio_path, "-y"],
            capture_output=True, check=True
        )
        print(f"[douyin-tools] ✅ 音频提取完成: {audio_path}")
        return audio_path
    except FileNotFoundError:
        print("[douyin-tools] ❌ 需要安装 ffmpeg")
        return None
    except subprocess.CalledProcessError as e:
        print(f"[douyin-tools] ❌ 音频提取失败: {e.stderr.decode()[:200]}")
        return None


def transcribe(audio_path: str, model_name: str = "tiny") -> str | None:
    """语音转文字"""
    if not whisper:
        print("[douyin-tools] 需要安装 openai-whisper: pip install openai-whisper")
        return None
    
    try:
        print(f"[douyin-tools] 🎯 加载模型: {model_name}")
        model = whisper.load_model(model_name)
        print(f"[douyin-tools] 🎯 开始转写: {audio_path}")
        result = model.transcribe(audio_path, language="zh")
        text = result["text"].strip()
        print(f"[douyin-tools] ✅ 转写完成 ({len(text)} 字)")
        return text
    except Exception as e:
        print(f"[douyin-tools] ❌ 转写失败: {e}")
        return None


def save_text(text: str, output_path: str):
    """保存转写结果"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"[douyin-tools] ✅ 已保存: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="douyin-tools: 抖音视频下载 + 音频提取 + 转文字"
    )
    parser.add_argument("--url", help="抖音视频链接")
    parser.add_argument("--file", help="包含多个链接的文本文件")
    parser.add_argument("--transcribe", action="store_true",
                        help="同时进行语音转文字")
    parser.add_argument("--model", default="tiny",
                        choices=["tiny", "base", "small", "medium", "large"],
                        help="whisper 模型大小 (默认: tiny)")
    parser.add_argument("--output", "-o", default="output",
                        help="输出目录")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    urls = []
    if args.url:
        urls.append(args.url)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            urls.extend([line.strip() for line in f if line.strip()])

    if not urls:
        print("[douyin-tools] 请提供 --url 或 --file")
        parser.print_help()
        return

    for i, url in enumerate(urls):
        print(f"\n{'='*50}")
        print(f"[{i+1}/{len(urls)}] {url}")

        vid = extract_video_id(url)
        if not vid:
            print(f"[douyin-tools] ⚠️ 无法识别视频ID: {url}")
            continue

        video_name = f"douyin_{vid}.mp4"
        video_path = os.path.join(args.output, video_name)

        # 下载
        result = download_video(url, args.output)
        if not result:
            print(f"[douyin-tools] ⚠️ 跳过: {url}")
            continue

        if args.transcribe:
            # 提取音频
            audio_path = os.path.join(args.output, f"douyin_{vid}.mp3")
            audio = extract_audio(result, audio_path)
            if audio:
                # 转文字
                text = transcribe(audio, args.model)
                if text:
                    txt_path = os.path.join(args.output, f"douyin_{vid}.txt")
                    save_text(text, txt_path)

    print(f"\n{'='*50}")
    print("[douyin-tools] ✅ 全部完成！")


if __name__ == "__main__":
    main()

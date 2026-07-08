#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
content_brief_generator.py

把抖音/短视频原始口播、竞品文案、评论需求，整理成可交付的短视频脚本 brief。
定位：给 heer-labs 接单展示用的小工具 —— 客户丢一段乱文本，输出选题、钩子、脚本、标题、拍摄清单。

用法：
  python content_brief_generator.py --text "瘦子增肌一天吃什么..." -o brief.md
  python content_brief_generator.py --file raw.txt --niche 瘦子增肌 --audience 新手小白
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


STOPWORDS = {
    "的", "了", "和", "是", "我", "你", "他", "她", "它", "我们", "你们", "他们", "一个", "这个", "那个",
    "就是", "然后", "因为", "所以", "但是", "如果", "可以", "没有", "不是", "什么", "怎么", "为什么",
    "the", "a", "an", "and", "or", "to", "of", "in", "for", "with", "is", "are", "on", "that",
}

HOOK_TEMPLATES = [
    "别再{bad_action}了，真正有效的是{core_action}",
    "如果你是{audience}，先把这 3 件事做对",
    "我踩过的坑：{pain}，其实一开始就能避开",
    "{niche}不是玄学，关键就这一个顺序",
    "多数人失败不是不努力，而是把{wrong_focus}当重点",
]

TITLE_TEMPLATES = [
    "{niche}新手避坑：先做这 3 步",
    "别再乱试了，{audience}的{niche}路线图",
    "我用一条视频讲清楚：{core}",
    "{pain}怎么办？按这个方法改",
    "适合{audience}的低成本执行清单",
]


@dataclass
class Brief:
    niche: str
    audience: str
    keywords: list[str]
    pain: str
    core: str
    hook: str
    title_options: list[str]
    script: str
    shot_list: list[str]
    cta: str


def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"[#@][\w\u4e00-\u9fff_-]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def split_sentences(text: str) -> list[str]:
    parts = re.split(r"[。！？!?；;\n]+", text)
    return [p.strip(" ，,、") for p in parts if len(p.strip()) >= 4]


def extract_keywords(text: str, limit: int = 10) -> list[str]:
    # 中文 2-6 字连续词 + 英文词，轻量无依赖，够做展示/接单 demo
    tokens = re.findall(r"[\u4e00-\u9fff]{2,6}|[A-Za-z][A-Za-z0-9_-]{2,}", text)
    freq: dict[str, int] = {}
    for t in tokens:
        if t in STOPWORDS:
            continue
        if len(t) <= 1:
            continue
        freq[t] = freq.get(t, 0) + 1
    return [k for k, _ in sorted(freq.items(), key=lambda kv: (-kv[1], -len(kv[0]), kv[0]))[:limit]]


def pick_pain(sentences: list[str], fallback: str) -> str:
    pain_words = ["难", "不会", "失败", "焦虑", "坑", "贵", "麻烦", "没效果", "没人", "涨粉", "不懂", "卡"]
    for s in sentences:
        if any(w in s for w in pain_words):
            return s[:40]
    return fallback


def fill_template(template: str, **kwargs: str) -> str:
    out = template
    for k, v in kwargs.items():
        out = out.replace("{" + k + "}", v)
    return out


def generate_brief(raw: str, niche: str = "短视频内容", audience: str = "新手") -> Brief:
    text = clean_text(raw)
    sentences = split_sentences(text)
    keywords = extract_keywords(text)

    core = keywords[0] if keywords else niche
    pain = pick_pain(sentences, fallback=f"{audience}不知道从哪开始")
    bad_action = "盲目模仿"
    core_action = f"围绕“{core}”做一个可执行步骤"
    wrong_focus = keywords[1] if len(keywords) > 1 else "形式"

    hook = fill_template(
        HOOK_TEMPLATES[0],
        bad_action=bad_action,
        core_action=core_action,
        audience=audience,
        pain=pain,
        niche=niche,
        wrong_focus=wrong_focus,
    )

    title_options = [
        fill_template(t, niche=niche, audience=audience, core=core, pain=pain)
        for t in TITLE_TEMPLATES
    ]

    support_points = sentences[:3] or [
        f"先明确目标人群：{audience}",
        f"再围绕关键词展开：{', '.join(keywords[:3]) or niche}",
        "最后给出一个能立刻执行的动作",
    ]
    while len(support_points) < 3:
        support_points.append("补一个真实案例或前后对比，增强可信度")

    script = f"""开头 0-3 秒：
{hook}

主体 3-25 秒：
1. 先指出问题：{pain}
2. 给出方法：围绕 {core} 拆成 3 个动作。
3. 具体执行：{support_points[0]}；{support_points[1]}；{support_points[2]}。

结尾 25-35 秒：
如果你也在做{niche}，先照这个清单做一遍。想要模板/工具，评论区留“资料”。"""

    shot_list = [
        "正脸开场：一句话抛出痛点，字幕放大关键词",
        "屏幕录制/白板：列出 3 步执行清单",
        "前后对比：展示错误做法 vs 正确做法",
        "结尾定格：放评论引导和账号定位",
    ]
    cta = "评论区留“资料”，我把模板发你；需要自动化处理/批量脚本可以私信。"

    return Brief(niche, audience, keywords, pain, core, hook, title_options, script, shot_list, cta)


def render_markdown(brief: Brief) -> str:
    keywords = "、".join(brief.keywords) if brief.keywords else "暂无"
    titles = "\n".join(f"{i+1}. {t}" for i, t in enumerate(brief.title_options))
    shots = "\n".join(f"- {s}" for s in brief.shot_list)
    return f"""# 短视频内容 Brief

## 定位
- 赛道：{brief.niche}
- 目标人群：{brief.audience}
- 关键词：{keywords}
- 核心切入点：{brief.core}
- 用户痛点：{brief.pain}

## 爆款钩子
{brief.hook}

## 标题备选
{titles}

## 口播脚本
{brief.script}

## 拍摄/剪辑清单
{shots}

## 评论/私信转化话术
{brief.cta}
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="生成短视频脚本 brief / 接单展示工具")
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--text", help="直接输入原始文本")
    src.add_argument("--file", help="从文本文件读取")
    parser.add_argument("--niche", default="短视频内容", help="赛道/领域，例如：瘦子增肌、办公自动化")
    parser.add_argument("--audience", default="新手", help="目标人群，例如：健身小白、个体商家")
    parser.add_argument("-o", "--output", help="输出 Markdown 文件路径")
    args = parser.parse_args()

    raw = args.text if args.text is not None else Path(args.file).read_text(encoding="utf-8")
    brief = generate_brief(raw, niche=args.niche, audience=args.audience)
    md = render_markdown(brief)

    if args.output:
        Path(args.output).write_text(md, encoding="utf-8")
        print(f"✅ 已生成: {args.output}")
    else:
        print(md)


if __name__ == "__main__":
    main()

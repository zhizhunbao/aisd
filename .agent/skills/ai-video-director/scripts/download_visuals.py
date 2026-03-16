"""
自动素材搜索下载器 — 根据旁白自动找图
====================================
从 Pexels 免费素材库自动搜索下载匹配图片。

Usage:
    python download_visuals.py <script_file> [--output-dir visuals/] [--api-key xxx]

示例:
    python download_visuals.py narration/script.txt --output-dir visuals/
    python download_visuals.py narration/script.txt --api-key YOUR_PEXELS_KEY

Pexels API Key（免费）:
    1. 注册 https://www.pexels.com/api/
    2. 获取 API Key
    3. 设为环境变量: $env:PEXELS_API_KEY = "your_key"
       或在命令行传入: --api-key your_key

原理:
    1. 读取 script.txt 每段旁白
    2. 提取关键词（中文→英文翻译）
    3. 搜索 Pexels 匹配图片
    4. 下载为 scene_01.jpg, scene_02.jpg, ...
"""
import argparse
import os
import re
import json
import urllib.request
import urllib.parse
from pathlib import Path

# 中文关键词 → 英文搜索词映射（技术/历史题材）
KEYWORD_MAP = {
    # 人物/历史
    "科学家": "scientist portrait vintage",
    "数学家": "mathematician vintage",
    "论文": "research paper academic",
    "学术": "university laboratory",
    "研究": "research laboratory",
    "实验室": "laboratory vintage",
    "大学": "university campus",
    "教授": "professor teaching",
    "发明": "invention vintage",
    "历史": "history vintage",
    "年代": "vintage technology",
    "1950": "1950s technology vintage",
    "1960": "1960s technology vintage",
    "1970": "1970s computer vintage",
    "1980": "1980s computer retro",
    # AI/技术
    "算法": "algorithm visualization",
    "数据": "data visualization abstract",
    "KNN": "data points classification",
    "分类": "sorting classification",
    "机器学习": "machine learning artificial intelligence",
    "AI": "artificial intelligence technology",
    "神经网络": "neural network brain",
    "深度学习": "deep learning network",
    "模型": "mathematical model",
    "向量": "vector space abstract",
    "搜索": "search technology",
    "计算": "computing calculation",
    "编程": "programming code screen",
    "代码": "programming code dark",
    # 抽象概念
    "距离": "distance measurement",
    "维度": "dimensions space abstract",
    "邻居": "neighborhood community",
    "投票": "voting democracy",
    "速度": "speed fast motion",
    "困难": "challenge difficulty",
    "突破": "breakthrough success light",
    "简单": "simple minimal clean",
    "复杂": "complex network structure",
    "朴素": "simple elegant minimal",
    # 应用场景
    "推荐": "recommendation shopping",
    "服务器": "server room data center",
    "互联网": "internet technology",
    "手机": "smartphone technology",
    "Facebook": "social media technology",
    "数据库": "database server technology",
    "GPU": "graphics card technology",
    # 情感/氛围
    "困境": "storm dark clouds",
    "希望": "sunrise hope light",
    "成功": "success celebration light",
    "失败": "failure broken dark",
    "智慧": "wisdom ancient light",
    "未来": "future technology bright",
}


def extract_search_terms(text: str) -> str:
    """从中文文本提取英文搜索词"""
    terms = []

    # 匹配关键词映射
    for cn, en in KEYWORD_MAP.items():
        if cn in text:
            terms.append(en)

    # 提取年份
    years = re.findall(r'(1\d{3}|20\d{2})年?', text)
    for y in years:
        terms.append(f"{y}s vintage")

    # 提取英文单词（人名、术语）
    en_words = re.findall(r'[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*', text)
    for w in en_words:
        if len(w) > 2 and w not in ('The', 'And', 'For'):
            terms.append(f"{w} portrait")

    if not terms:
        # 默认用技术主题
        terms = ["technology abstract"]

    # 取前2个最相关的
    return " ".join(terms[:2])


def search_pexels(query: str, api_key: str, per_page: int = 5) -> list[dict]:
    """搜索 Pexels 图片"""
    url = f"https://api.pexels.com/v1/search?query={urllib.parse.quote(query)}&per_page={per_page}&orientation=landscape"
    req = urllib.request.Request(url, headers={"Authorization": api_key})

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            return data.get("photos", [])
    except Exception as e:
        print(f"  ⚠️ 搜索失败: {e}")
        return []


def download_image(url: str, output_path: Path) -> bool:
    """下载图片"""
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0"
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            output_path.write_bytes(resp.read())
        return True
    except Exception as e:
        print(f"  ⚠️ 下载失败: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="自动素材搜索下载器")
    parser.add_argument("script", type=str, help="旁白稿路径")
    parser.add_argument("--output-dir", type=str, default="visuals", help="输出目录")
    parser.add_argument("--api-key", type=str, default=None, help="Pexels API Key")
    args = parser.parse_args()

    # API Key
    api_key = args.api_key or os.environ.get("PEXELS_API_KEY")
    if not api_key:
        print("❌ 需要 Pexels API Key")
        print("   免费获取: https://www.pexels.com/api/")
        print("   设置: $env:PEXELS_API_KEY = 'your_key'")
        print("   或:   --api-key your_key")
        return

    # 读取脚本
    script_path = Path(args.script)
    if not script_path.exists():
        print(f"❌ 文件不存在: {script_path}")
        return

    lines = [l.strip() for l in script_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"🔍 自动素材搜索器")
    print(f"   旁白: {len(lines)} 段")
    print(f"   输出: {output_dir}/\n")

    downloaded = 0
    for i, line in enumerate(lines):
        scene_num = f"{i+1:02d}"
        output_file = output_dir / f"scene_{scene_num}.jpg"

        # 已有素材则跳过
        if output_file.exists():
            print(f"  [{scene_num}] ⏭️ 已存在")
            continue

        # 提取搜索词
        search_query = extract_search_terms(line)
        print(f"  [{scene_num}] 🔍 \"{search_query}\"")
        print(f"         📝 {line[:40]}...")

        # 搜索
        photos = search_pexels(search_query, api_key)
        if not photos:
            print(f"         ⚠️ 无结果，用默认搜索")
            photos = search_pexels("technology abstract", api_key)

        if photos:
            # 下载第一张 landscape 大图
            photo = photos[0]
            img_url = photo.get("src", {}).get("large2x") or photo.get("src", {}).get("large")
            photographer = photo.get("photographer", "unknown")

            if img_url and download_image(img_url, output_file):
                size_kb = output_file.stat().st_size / 1024
                print(f"         ✅ {output_file.name} ({size_kb:.0f}KB) by {photographer}")
                downloaded += 1
            else:
                print(f"         ❌ 下载失败")
        else:
            print(f"         ❌ 搜索+下载均失败")

    print(f"\n{'='*60}")
    print(f"  ✅ 完成！下载了 {downloaded}/{len(lines)} 张图片")
    print(f"  📁 {output_dir}/")
    print(f"\n  ⚠️ 建议人工检查图片是否匹配旁白内容")
    print(f"     不合适的可以手动替换")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()

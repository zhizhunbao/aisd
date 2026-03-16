"""
视频项目脚手架 — 创建项目目录 + 准备 History 文件
================================================
文稿由 Claude 直接生成，不再需要粘贴到 Gemini。

Usage:
    python generate_video_script.py <course> <topic> [--style yuan|laogao|luoxiang|clean]

工作流：
    1. 本脚本创建项目结构 + 读取 History 文件
    2. 用户让 Claude 直接根据 History + 风格生成旁白稿
    3. Claude 输出存为 narration/script.txt
    4. TTS 生成音频
    5. 组装视频
"""
import argparse
import sys
from pathlib import Path
from datetime import date

WORKSPACE = Path(__file__).resolve().parent.parent.parent.parent.parent
KNOWLEDGE_MAP = WORKSPACE / "knowledge-map"
VIDEO_CONTENT = WORKSPACE / "video-content"

# ============================================================
# 四种叙事风格
# ============================================================
STYLES = {
    "yuan": {
        "name": "袁腾飞",
        "tagline": "用现代人视角吐槽技术史，把论文讲成段子",
        "rules": [
            "像朋友在饭桌上聊天，不像老师讲课",
            "学术人物要讲八卦（恩怨、打脸时刻）",
            "每30秒至少一个笑点或反转",
            "用现代人视角吐槽历史",
            "金句收尾",
        ],
    },
    "laogao": {
        "name": "老高",
        "tagline": "悬疑+好奇心驱动，层层揭秘",
        "rules": [
            "开头抛出震惊事实",
            "用'更可怕的是...'、'但真相是...'制造悬疑",
            "像讲都市传说一样讲技术",
            "每段结尾留悬念",
            "收尾感叹式总结",
        ],
    },
    "luoxiang": {
        "name": "罗翔",
        "tagline": "用'张三'式荒诞类比解释概念",
        "rules": [
            "每个概念必须用张三式荒诞场景类比",
            "先让人笑，再让人懂",
            "术语一律转成生活场景",
            "保持理性分析底色",
            "感悟金句：'跟人生一样'",
        ],
    },
    "clean": {
        "name": "精简",
        "tagline": "纯干货，无废话，适合自己的声音",
        "rules": [
            "每句话都有信息量",
            "不用语气词（哎、嘿、好家伙）",
            "可以类比但不荒诞",
            "逻辑清晰：问题→方法→原理→局限→现状",
            "用短句，一个概念一句话",
        ],
    },
}


def find_history_file(course, topic):
    for subdir in ["courses", "tools", "projects"]:
        p = KNOWLEDGE_MAP / subdir / course / topic / f"{topic}_history.md"
        if p.exists():
            return p
    return None


def main():
    parser = argparse.ArgumentParser(description="视频项目脚手架")
    parser.add_argument("course", help="课程分类")
    parser.add_argument("topic", help="主题名")
    parser.add_argument("--style", choices=STYLES.keys(), default="clean")
    args = parser.parse_args()

    style = STYLES[args.style]
    print(f"\n🎬 视频项目: {args.course}/{args.topic}")
    print(f"   风格: {style['name']} — {style['tagline']}\n")

    # 1. 创建项目目录
    project_dir = VIDEO_CONTENT / args.course / args.topic
    (project_dir / "narration").mkdir(parents=True, exist_ok=True)
    (project_dir / "visuals").mkdir(parents=True, exist_ok=True)
    (project_dir / "output").mkdir(parents=True, exist_ok=True)

    # 2. 查找 History 文件
    history_path = find_history_file(args.course, args.topic)
    if history_path:
        print(f"  📖 History: {history_path.relative_to(WORKSPACE)}")
        content = history_path.read_text(encoding="utf-8")
        print(f"     {len(content)} 字符")
    else:
        print(f"  ⚠️ 未找到 {args.topic}_history.md")

    # 3. 输出项目信息
    info = f"""---
topic: {args.topic}
course: {args.course}
style: {style['name']}
created: {date.today().isoformat()}
---

# {args.topic} 视频项目

## 风格：{style['name']}
{style['tagline']}

### 规则
{chr(10).join(f'- {r}' for r in style['rules'])}

## 三幕结构（3分钟）
- 第一幕（15秒）：钩子
- 第二幕（2分15秒）：起源→困境→突破
- 第三幕（30秒）：总结+收尾

## 文件清单
- [ ] narration/script.txt — 旁白稿（每行一段）
- [ ] narration/full_narration_myvoice.mp3 — TTS 音频
- [ ] visuals/scene_01.png/.mp4 — 视觉素材
- [ ] output/final.mp4 — 成品
- [ ] output/subtitles.srt — 字幕
"""
    info_path = project_dir / "README.md"
    info_path.write_text(info, encoding="utf-8")
    print(f"  ✅ {info_path.relative_to(WORKSPACE)}")

    print(f"\n{'='*60}")
    print(f"  下一步：")
    print(f"  1. 让 Claude 生成旁白稿（告诉它风格+主题）")
    print(f"  2. 存为 narration/script.txt")
    print(f"  3. python generate_narration_qwen.py --script narration/script.txt --clone voice.mp3")
    print(f"  4. 放视觉素材到 visuals/")
    print(f"  5. python assemble_video_v3.py {project_dir}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()

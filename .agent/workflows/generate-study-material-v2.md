---
description: Lightweight pipeline – PPTX → PDF → Markdown → Format → Chinese translation
---

# 📖 自学材料生成工作流 v2 (Generate Study Material v2)

精简版流水线：PPTX → PDF → Markdown → 格式化 → 中文翻译。

## 🎯 使用方式

```
/generate-study-material-v2 [课程] [主题]

示例:
/generate-study-material-v2 ml svm
/generate-study-material-v2 nlp transformer --from=phase2
```

## 📋 流程概览

```
Phase 1   PPTX → PDF     → dev-pptx-to-pdf skill
Phase 2   PDF  → MD      → dev-pdf-processing skill
Phase 3   格式化 .md     → learning-slide-formatting skill
Phase 4   中文翻译       → learning-note-taking skill (§10)
```

---

## ⚖️ 执行协议

1. **串行执行**: 按 Phase 顺序，禁止跨阶段
2. **检查点验证**: 每 Phase 末尾验证后才进入下一阶段
3. **中断恢复**: `--from=<phase>` 从指定阶段继续
4. **Skill 优先**: 每个 Phase 开始前**必须先读取对应 skill 的 SKILL.md**
5. **跳过条件**: 如果输入已是 PDF，跳过 Phase 1；如果已有 MD，跳过 Phase 1–2

---

## Phase 1: PPTX → PDF 📄

**Skill**: `dev-pptx-to-pdf`

1. 读取 `dev-pptx-to-pdf` 的 SKILL.md
2. 在 `courses/[course]/slides/` 找到 `[topic].pptx`
3. 转换为 PDF
4. 跳过条件: 已有 PDF 或 `--from=phase2`

**输出**: `courses/[course]/slides/[topic].pdf`

---

## Phase 2: PDF → Markdown 📝

**Skill**: `dev-pdf-processing`

1. 读取 `dev-pdf-processing` 的 SKILL.md
2. 使用 `pdf_to_md_hybrid.py` 将 PDF 转为 Markdown
3. 提取图片到 `[topic]_slides_images/`
4. 验证 Markdown 完整性（页数、图片引用）
5. 跳过条件: 已有 MD 或 `--from=phase3`

**输出**: `courses/[course]/notes/[topic]_slides.md` + images/

---

## Phase 3: 格式化 📐

**Skill**: `learning-slide-formatting`

1. 读取 `learning-slide-formatting` 的 SKILL.md
2. Follow skill 完整指令：
   - 双语章节标题
   - 清理 PDF 转换残留（乱码、多余空行、断行）
   - 整理图片引用路径
   - 规范 Markdown 结构（标题层级、列表格式）
3. 跳过条件: `--from=phase4`

**输出**: `courses/[course]/notes/[topic]_slides.md` (格式化后)

---

## Phase 4: 中文翻译 🌐

**Skill**: `learning-note-taking` (§10 教师资料格式化模式)

1. 读取 `learning-note-taking` 的 SKILL.md，定位 §10 模式
2. Follow §10 模式执行：
   - 所有英文内容加中文翻译
   - 表格双语化
   - 保留原始英文术语（括号标注）
   - **不加** `📝 Notes:` 块
3. 最终检查：确认无遗漏未翻译段落

**输出**: `courses/[course]/notes/[topic]_slides.md` (带中文翻译)

---

## 💡 快捷子命令

| 命令 | 说明 |
|------|------|
| `/generate-study-material-v2 ml svm` | 完整流程 (Phase 1–4) |
| `--from=phase2` | 从 PDF→MD 开始（已有 PDF） |
| `--from=phase3` | 从格式化开始（已有 MD） |
| `--from=phase4` | 只做中文翻译 |

## 📊 支持的课程

| 代码 | 课程 | Skill |
|------|------|-------|
| `ml` | Machine Learning | `ai-learning-ml` |
| `nlp` | NLP | `ai-learning-nlp` |
| `mv` | Machine Vision | `ai-learning-mv` |
| `cv` | Computer Vision | `ai-learning-cv` |
| `dl` | Deep Learning | `ai-learning-dl` |
| `rl` | Reinforcement Learning | `ai-learning-rl` |
| `pj` | Project Management | `ai-learning-pj` |

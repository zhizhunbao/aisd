# 📖 Official Documentation — 官方文档库

> 与 `textbooks/` 平行的官方文档库，存放各工具链的离线官方文档。
> 教科书放 `textbooks/`，官方文档放 `official-docs/`。

## 目录结构

```
official-docs/
├── README.md                  ← 本文件
├── veo/                       ← Google Veo 3.1 视频生成
├── imagen/                    ← Google Imagen 3 图像生成
├── gemini/                    ← Google Gemini LLM
├── flow/                      ← Google Flow AI 剪辑
├── capcut/                    ← 剪映/CapCut 视频编辑
├── vertex-ai/                 ← Google Cloud Vertex AI 平台
└── ...                        ← 其他工具按需添加
```

## 命名规则

文件命名格式：`{工具}_{内容}_{日期}.{格式}`

示例：
- `veo_prompt_guide_202603.md`
- `imagen_capabilities_202603.md`
- `gemini_prompt_strategies_202603.md`

## 在线文档索引

### 🎬 Veo 3.1（文字→视频）

| 文档 | URL | 状态 |
|------|-----|------|
| Veo Prompt Guide | https://cloud.google.com/vertex-ai/generative-ai/docs/video/video-prompts | ⬜ 待下载 |
| Ultimate Prompting Guide | https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo | ⬜ 待下载 |
| Veo 3.1 in Gemini API | https://ai.google.dev/gemini-api/docs/video | ⬜ 待下载 |
| Veo on DeepMind | https://deepmind.google/technologies/veo/ | ⬜ 待下载 |

### 🖼️ Imagen 3（封面图生成）

| 文档 | URL | 状态 |
|------|-----|------|
| Imagen Prompt Guide | https://cloud.google.com/vertex-ai/generative-ai/docs/image/image-prompts | ⬜ 待下载 |
| Imagen 3 Capabilities | https://cloud.google.com/vertex-ai/generative-ai/docs/image/overview | ⬜ 待下载 |
| Imagen 3 in Gemini API | https://ai.google.dev/gemini-api/docs/image-generation | ⬜ 待下载 |

### 🧠 Gemini（脚本生成）

| 文档 | URL | 状态 |
|------|-----|------|
| Prompt Engineering Strategies | https://ai.google.dev/gemini-api/docs/prompting-strategies | ⬜ 待下载 |
| System Instructions | https://ai.google.dev/gemini-api/docs/system-instructions | ⬜ 待下载 |
| Structured Output | https://ai.google.dev/gemini-api/docs/structured-output | ⬜ 待下载 |
| Agentic Prompt Design | https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/prompt-design | ⬜ 待下载 |

### ✂️ Flow（AI 剪辑）

| 文档 | URL | 状态 |
|------|-----|------|
| Google Flow | https://flow.google/ | ⬜ 待下载 |

### 🎬 剪映/CapCut（旁白+字幕）

| 文档 | URL | 状态 |
|------|-----|------|
| CapCut Official Tutorials | https://www.capcut.com/resource/capcut-tutorial | ⬜ 待下载 |
| CapCut Auto Captions | https://www.capcut.com/tools/auto-caption | ⬜ 待下载 |
| CapCut Text-to-Speech | https://www.capcut.com/tools/text-to-speech | ⬜ 待下载 |

## 下载方式

手动下载：浏览器打开 URL → Ctrl+S 保存为 HTML/PDF → 放入对应子目录

或使用脚本：
```bash
# 未来可以写一个类似 search_github_books.py 的脚本批量下载
python official-docs/download_docs.py
```

## 与工作流的关系

- `generate-knowledge-map.md` Phase 0 扫描 `official-docs/` 目录
- `ai-video-director` skill 引用此目录下的工具文档
- 定期更新（工具迭代快，建议每 3 个月检查一次）

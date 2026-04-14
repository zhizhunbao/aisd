# 🎤 ROS 2 Voice Q&A — Part 2 操作手册

> Loaner Laptop: `aisd@192.168.2.33` | Ubuntu 22.04 | ROS 2 Humble

---

## 🚀 快速启动

```powershell
# 从 Windows PowerShell 一键启动（SSH 到 loaner laptop）
ssh -t aisd@192.168.2.33 "bash ~/run_loaner.sh"
```

启动后会进入 tmux，看到 5 个窗格分别显示 5 个节点的输出。

## 🛑 停止 / 重连

```powershell
# 停止所有节点
ssh aisd@192.168.2.33 "bash ~/stop_loaner.sh"

# 重新连接（节点继续运行时）
ssh -t aisd@192.168.2.33 "tmux attach -t nlp_rag"
```

**tmux 快捷键：**
- `Ctrl+B` → `D` — 退出 tmux（节点继续运行）
- `Ctrl+B` → `[` — 滚动模式（查看历史输出）
- `Ctrl+C` — 停止当前窗格的节点

---

## 🎯 可以问的 20 个问题

知识库覆盖以下 20 个主题，**对着麦克风说英文即可**：

### ML 机器学习 (5 题)

| # | 问法 | 知识来源 |
|---|------|----------|
| 1 | "What is neural attention?" | Eisenstein NLP §18.3.1 |
| 2 | "What is the difference between generative and discriminative classifiers?" | Murphy PML1 §9.4 |
| 3 | "How do you compute the gradient for logistic regression?" | Jurafsky SLP3 §4.6.1 |
| 10 | "What is cost-sensitive classification?" | Murphy PML1 §5.1.2.2 |
| 19 | "What is transfer learning?" | Murphy PML1 §19.1 |

### NLP 自然语言处理 (6 题)

| # | 问法 | 知识来源 |
|---|------|----------|
| 4 | "What is an N-gram language model?" | Eisenstein NLP §6.1 |
| 5 | "What is skip-gram?" | Jurafsky SLP3 §5.5.2 |
| 6 | "How are RNNs used as language models?" | Jurafsky SLP3 §13.2 |
| 14 | "What is Word2Vec?" | Jurafsky SLP3 §5.2 |
| 15 | "What is named entity recognition?" | Jurafsky SLP3 §17.1 |
| 20 | "What is BLEU score?" | Eisenstein NLP §9.3.2 |

### Deep Learning 深度学习 (5 题)

| # | 问法 | 知识来源 |
|---|------|----------|
| 8 | "Why is weight initialization important?" | Kelleher ML §8.4.2 |
| 9 | "What does network depth mean?" | Kelleher ML §8.2.3 |
| 12 | "What is backpropagation?" | Kelleher ML §8.3.1 |
| 17 | "What is dropout regularization?" | Kelleher ML §8.4.4 |
| 18 | "What is batch normalization?" | Kelleher ML §8.4.3 |

### Transformer & Search (3 题)

| # | 问法 | 知识来源 |
|---|------|----------|
| 11 | "What is TF-IDF?" | Jurafsky SLP3 §6.5 |
| 13 | "Explain the Transformer architecture" | Eisenstein NLP §18.4 |
| 16 | "What is beam search?" | Jurafsky SLP3 §10.5 |

### Computer Vision (1 题)

| # | 问法 | 知识来源 |
|---|------|----------|
| 7 | "What is a 3D rigid body transformation?" | Szeliski CV §2.1.2 |

---

## 💡 Demo 演示建议

### 推荐演示顺序（由浅入深）

1. **热身** — "What is Word2Vec?" （简短、清晰的回答）
2. **核心 NLP** — "What is an N-gram language model?" （课程核心）
3. **对比题** — "What is the difference between generative and discriminative classifiers?" （展示理解力）
4. **深度题** — "Explain the Transformer architecture" （展示复杂回答能力）

### 提问技巧

- 🗣️ **说清楚、慢一点** — Whisper 对清晰英文识别最好
- ⏱️ **等 15 秒** — 每次回答后有冷却时间（防回声循环）
- 🔇 **周围安静** — 减少 Whisper 幻觉
- 📏 **短问题优先** — "What is X?" 比长句子识别率高

### ⚠️ 避免问的问题

- ❌ 知识库外的问题（如 "What is GPT-4?"） — 会得到不准确或编造的答案
- ❌ 中文问题 — 知识库只有英文内容
- ❌ 多轮追问 — 系统是单轮问答，没有对话记忆

---

## 📂 文件说明

```
ros2/
├── start_loaner.bat      # Windows 一键部署+启动
├── stop_loaner.bat       # Windows 一键停止
├── run_loaner.sh         # Ubuntu 端 tmux 启动 5 节点
├── stop_loaner.sh        # Ubuntu 端停止
├── _deploy_helper.sh     # 部署辅助
├── ollama_publisher.py   # 核心节点（RAG + LLM 桥梁）
└── knowledge.txt         # 简化知识库（20 条教科书摘要）
```

## 🏗️ 5 节点架构

```
🎤 Mic → [1] RecordingPublisher → /recording
                                      ↓
         [2] WordsPublisher (Whisper) → /words
                                          ↓
         [3] OllamaPublisher (RAG+LLM) → /ollama_reply
                                              ↓
         [4] SpeakClient → /speak (service call)
                               ↓
         [5] SpeakService (gTTS) → 🔊 Speaker
                                       ↓
                              ⏱️ 15s cooldown → 回到 [1]
```

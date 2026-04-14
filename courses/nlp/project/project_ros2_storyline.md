# Project Part 2 故事线：从文字问答到语音对话 — 把 RAG 装进机器人

> **Source:** `CST 8507_Project_Presentation_v3.pdf` (Part 2, Pages 13–16, 18)
> **核心主题：** 如何把一个桌面端的 RAG 问答系统变成一个能"听"能"说"的语音交互机器人？
> **故事线：** 一条消息在 5 个 ROS 2 节点之间的旅行 — 从麦克风到扬声器

---

## 🎬 序幕：我们在解决什么问题？

Part 1 已经完成了一个强大的 RAG 问答系统：46 本教科书、4 种检索方法、双重评分、深度溯源。但它只有一个 React 网页界面 — 用户必须**打字输入、阅读输出**。

> 💡 **设想一个场景：** 一个教育机器人站在教室里，学生对它说"什么是注意力机制？"，它立刻**用语音回答**并引用教科书来源。这需要什么？
>
> 1. **耳朵** — 录音 + 语音识别（STT）
> 2. **大脑** — RAG 检索 + LLM 生成答案
> 3. **嘴巴** — 文字转语音（TTS）+ 播放

这正是 Part 2 要解决的：把 Part 1 的"大脑"包上"耳朵"和"嘴巴"，用 **ROS 2** 框架把它们连起来。

**为什么选 ROS 2？**

- ROS 2 (Robot Operating System 2) 是机器人领域的标准通信框架
- **话题（Topic）发布/订阅模型** 天然适合流式管道：每个环节只关心"输入什么、输出什么"
- 目标硬件是 **iRobot Create 3**，它原生支持 ROS 2 Humble
- 部署平台：Ubuntu 22.04（借用笔记本），通过 `colcon build` 编译

---

## 📚 第一章：五节点管道 — 消息的旅程

### 1.1 一句话定义

> **五节点管道 = 五个独立程序通过 ROS 2 话题接力传递消息，从麦克风到扬声器。**

### 1.2 架构全景

```
麦克风 → [Node 1] → /recording → [Node 2] → /words → [Node 3] → /ollama_reply → [Node 4] → /speak(srv) → [Node 5] → 扬声器
         录音发布者      音频流     语音识别       文字       RAG+LLM        答案文字      朗读客户端    TTS请求     朗读服务      声音输出
```

| 节点 # | 节点名 | 输入 | 输出 | 核心技术 | 所属包 |
|--------|--------|------|------|----------|--------|
| 1 | RecordingPublisher | 麦克风 | `/recording` (音频流) | Silero VAD（语音活动检测） | aisd_hearing（自写） |
| 2 | WordsPublisher | `/recording` | `/words` (文字) | faster-whisper (int8, 自动语言检测) | aisd_hearing（自写） |
| 3 | OllamaPublisher | `/words` | `/ollama_reply` (答案) | RAG + Ollama qwen2.5:0.5b | aisd_hearing（自写） |
| 4 | SpeakClient | `/ollama_reply` | `/speak` (服务调用) | ROS 2 Service Client | aisd_speaking（提供） |
| 5 | SpeakService | `/speak` | 扬声器播放 | gTTS → 音频播放 | aisd_speaking（提供） |

> 💡 **类比：** 想象一条工厂流水线 — 每个工人只做一件事：
> - 工人 1（Node 1）听声音，判断"有人在说话"就录下来
> - 工人 2（Node 2）把录音翻译成文字
> - 工人 3（Node 3）拿文字去查 46 本书，写出答案
> - 工人 4（Node 4）把答案交给播音员
> - 工人 5（Node 5）把文字读出来

### 1.3 关键设计决策

**话题 vs 服务：**

| 通信方式 | 用在哪里 | 为什么 |
|----------|----------|--------|
| **Topic（话题）** | Node 1→2→3→4 | 异步、单向、适合流式数据 |
| **Service（服务）** | Node 4→5 (`/speak`) | 请求-响应模式，等 TTS 播完再继续 |

> 为什么 Node 4→5 用 Service 而不是 Topic？因为必须**等 TTS 播放完毕**才能开始下一轮录音，否则麦克风会录到自己的声音（回声循环问题 — 见第三章）。

---

## 📖 第二章：核心节点 — ollama_publisher.py

### 2.1 Part 1 和 Part 2 的桥梁

`ollama_publisher.py` 是整个系统中最重要的一个节点 — 它是 **Part 1（RAG 问答）和 Part 2（ROS 2 语音）的桥梁**。

**它做什么：**

1. **启动时**加载 `knowledge.txt`（46 本教科书的精华摘要）
2. **订阅** `/words` 话题 — 接收 Whisper 识别出的文字
3. **构建系统提示词** — 把 RAG 检索到的上下文塞进 Ollama 的 system prompt
4. **调用本地 Ollama API** (`localhost:11434`) — 发送查询，获取生成的答案
5. **发布**答案到 `/ollama_reply` 话题

### 2.2 简化的 RAG vs Part 1 的完整 RAG

| 维度 | Part 1（React UI） | Part 2（ROS 2 语音） |
|------|--------------------|--------------------|
| 知识库 | 85,356 chunks + ChromaDB + SQLite | 简化的 `knowledge.txt` 文件 |
| 检索 | 4 种方法 + RRF + Cross-Encoder | 基于 knowledge.txt 的上下文匹配 |
| LLM | qwen2.5:0.5b via Ollama | 同 — qwen2.5:0.5b via Ollama |
| 输出 | 带 PDF 溯源链接的富文本 | 纯文本语音回答 |

> 💡 **为什么简化？** 因为语音场景不需要 PDF 高亮和页面定位 — 用户听的是**答案内容**，不需要视觉溯源。而且 CPU 资源有限（3 个 AI 模型同时运行），简化知识库能降低延迟。

### 2.3 防护机制

- **幻觉过滤（Hallucination filtering）：** 在输入端检测 Whisper 常见的"幻觉"输出（如重复句子、已知无意义短语），过滤后才发给 LLM
- **15 秒冷却**：每次回复后 15 秒内不处理新输入（防回声 — 下一章详述）

---

## 🎭 第三章：三大挑战 — 在真实环境中遇到的"Boss"

### 3.1 Boss 1: Whisper 幻觉

**问题：** Whisper 在安静环境或背景噪声中会产生"幻觉" — 输出重复的句子、已知的无意义短语（如 "Thank you for watching"）。这些假输入会触发 LLM 生成不相关的回答。

**解决方案 — 三重过滤：**

1. **Silero VAD 前置过滤** — 只在检测到真正的人声时才启动 Whisper，安静时不转录
2. **重复检查（Repetition check）** — 如果连续两次识别结果完全相同，丢弃
3. **三元组分析（Trigram analysis）** — 检测不自然的重复模式，标记为幻觉

### 3.2 Boss 2: 回声循环（Echo Loop）

**问题：** TTS 播放答案时，麦克风会录到自己说的话 → Whisper 再识别 → 再触发 LLM → 再生成答案 → 无限循环！

**解决方案 — 15 秒冷却计时器：**

```
[用户提问] → [RAG 处理] → [TTS 播放答案 ~10s] → [冷却 15s] → [重新开始监听]
                                                    ↑
                                              这段时间忽略所有输入
```

> 💡 **为什么是 15 秒？** 因为 TTS 播放一段答案通常需要约 10 秒，留 5 秒余量确保声音完全消散。这比用 Service 等待回调更简单可靠。

### 3.3 Boss 3: 资源限制

**问题：** 在一台普通 CPU 笔记本上同时运行 3 个 AI 模型：

| 模型 | 用途 | 大小 |
|------|------|------|
| faster-whisper int8 | 语音识别 | ~300MB |
| Ollama qwen2.5:0.5b | 答案生成 | ~400MB |
| gTTS | 文字转语音 | 在线 API，几乎不占内存 |

**总内存 < 1.5GB** — 通过以下策略实现：
- Whisper 使用 **int8 量化** — 模型体积减半
- Ollama 选择 **0.5B 参数** 的最小模型 — 够用就好
- gTTS 用谷歌在线 API — 不在本地运行 TTS 模型

**代价：** CPU 推理速度慢，每次回复约 10–15 秒。但对教育场景可接受。

---

## 🏆 第四章：一键部署 — 从 Windows 到 Ubuntu

### 4.1 跨平台挑战

开发在 Windows 上，但 ROS 2 只能在 Ubuntu 上运行。需要：
1. 把代码从 Windows 传到 Ubuntu 笔记本
2. 编译 ROS 2 包
3. 启动 5 个节点

### 4.2 自动化方案

**`start_loaner.bat`（Windows 上运行）：**

```bash
Step 1: SCP sync (4 .py + knowledge.txt)     # 传代码
Step 2: Stop existing tmux session            # 停旧会话
Step 3: colcon build --symlink-install        # 编译
Step 4: tmux launch 5 panes                   # 启动 5 节点
```

**`stop_loaner.bat`：** Kill tmux + cleanup orphan processes — 终止 + 清理

> 💡 **为什么用 tmux？** tmux 可以在一个终端窗口里开 5 个窗格（pane），每个窗格运行一个 ROS 2 节点。调试时可以同时看到所有节点的输出，非常方便。

### 4.3 效果

一键 `start_loaner.bat` → 代码同步 → 编译 → 5 个节点全部启动 → 对着麦克风说话即可开始语音问答。

---

## 🗺️ 全局回顾：消息如何走完全程

```
┌────────────────────────────────────────────────────────────────┐
│                    语音问答完整流程                              │
│                                                                │
│  👤 学生说话                                                    │
│        │                                                       │
│        ▼                                                       │
│  🎤 Node 1: RecordingPublisher                                 │
│     Silero VAD 检测人声 → 录音                                  │
│        │ /recording (音频流)                                    │
│        ▼                                                       │
│  📝 Node 2: WordsPublisher                                     │
│     faster-whisper 语音识别 → 幻觉过滤                          │
│        │ /words (文字)                                          │
│        ▼                                                       │
│  🧠 Node 3: OllamaPublisher                                   │
│     knowledge.txt 上下文 + Ollama qwen2.5:0.5b 生成答案         │
│        │ /ollama_reply (答案文字)                                │
│        ▼                                                       │
│  📞 Node 4: SpeakClient                                        │
│     调用 TTS 服务                                               │
│        │ /speak (Service 请求)                                  │
│        ▼                                                       │
│  🔊 Node 5: SpeakService                                      │
│     gTTS 合成 → 扬声器播放                                      │
│        │                                                       │
│        ▼                                                       │
│  ⏱️ 15 秒冷却（防回声）→ 返回 Node 1 继续监听                   │
└────────────────────────────────────────────────────────────────┘
```

### 关键转折总结

| 从 → 到 | 解决了什么核心问题？ |
|---------|---------------------|
| Part 1 → Part 2 | 从"打字问答"变成"语音对话" — 让 RAG 能装进机器人 |
| 单节点 → 5 节点管道 | 职责分离，每个节点独立、可替换、可调试 |
| 无过滤 → 三重幻觉过滤 | 解决 Whisper 在安静环境下的假输出问题 |
| 无冷却 → 15 秒冷却 | 解决 TTS 播放触发麦克风的回声循环 |
| 手动部署 → 一键 bat 脚本 | 跨平台（Windows → Ubuntu）自动化，降低部署门槛 |

---

## 📝 复习重点检查清单

- [ ] 能画出 5 节点管道的完整架构图（节点名 + 话题名 + 数据流向）
- [ ] 能解释 Topic 和 Service 两种 ROS 2 通信方式的区别，以及本项目中各用在哪里
- [ ] 能说明 `ollama_publisher.py` 的作用 — 为什么它是 Part 1 和 Part 2 的桥梁
- [ ] 能描述 Whisper 幻觉问题及三重过滤方案（Silero VAD + 重复检查 + 三元组分析）
- [ ] 能解释回声循环问题及 15 秒冷却方案
- [ ] 能说明为什么选择 qwen2.5:0.5b + faster-whisper int8 — 资源限制下的权衡
- [ ] 能描述 `start_loaner.bat` 的四步自动化部署流程
- [ ] 能对比 Part 1（完整 RAG）和 Part 2（简化 knowledge.txt）的知识库差异及原因

---

## 📚 参考资料

- [ROS 2 Humble Documentation](https://docs.ros.org/en/humble/)
- [Silero VAD](https://github.com/snakers4/silero-vad) — 语音活动检测
- [faster-whisper](https://github.com/SYSTRAN/faster-whisper) — CTranslate2 加速的 Whisper
- [Ollama](https://ollama.com/) — 本地 LLM 运行框架
- [gTTS](https://gtts.readthedocs.io/) — Google Text-to-Speech
- Source slides: `courses/nlp/notes/project_presentation_slides.md` (§8–§11)

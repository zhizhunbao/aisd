# W12: LLM & RAG (大语言模型 & 检索增强生成)

## 1. Definitions (定义)

### LLM Core Concepts (LLM 核心概念)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| LLM (大语言模型) | 参数量 >1B 的大规模语言模型，基于 Transformer 架构，在海量文本上训练，能理解并生成类人文本 | GPT-4, LLaMA-70B, Qwen2.5 |
| Foundation Model (基础模型) | 在广泛数据上预训练的通用模型，可适配多种下游任务 | GPT-4 可做翻译/摘要/代码/问答 |
| Token (词元) | LLM 处理文本的基本单位，由分词器 (tokenizer) 切分，非严格等于"词" | "unhappiness" 可能被切成 3-4 个 token |
| Context Window (上下文窗口) | LLM 一次能处理的最大 token 数，包括 prompt + 对话历史 + 生成响应 | GPT-4: 128K tokens; BERT: 512 tokens |
| Parameters (参数) | 模型中可学习的权重数量，决定模型容量和内存需求 | BERT:340M; LLaMA-70B:70B; GPT-4:~200B |
| Hallucination (幻觉) | 模型自信地生成看似合理但事实上不正确的信息——LLM 的核心风险 | "BERT was released in 2020" (实际是2018) |
| Temperature (温度) | 控制生成随机性：0→确定性(始终选最高概率); 1→创造性(更多样化) | T=0: 总是"Paris"; T=1: 可能说"Lyon" |
| Top-k / Top-p | 采样策略：Top-k 限制候选为 k 个最高概率 token; Top-p 限制累积概率达到 p | Top-k=50: 从50个最可能中选; Top-p=0.9: 保留90%概率质量 |

### LLM Types (LLM 类型)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| General-purpose LLM (通用LLM) | 在广泛数据上训练的通用任务模型 | GPT 系列 |
| Instruction-tuned LLM (指令微调LLM) | 在指令-响应对上微调，更好地遵循人类指令 | AllenNLP's 指令微调模型 |
| Dialogue-tuned LLM (对话微调LLM) | 专门为多轮对话场景优化 | Microsoft DialoGPT |
| Domain-specific LLM (领域特定LLM) | 在特定领域 (医学/法律/金融) 数据上训练或微调 | BioBERT (生物医学) |

### LLM Training (LLM 训练)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| ChatGPT Training (ChatGPT训练) | 预训练 → RLHF (人类反馈强化学习) → 部署；通过人类评评价对齐行为 | 预训练→SFT→Reward Model→PPO |
| Constitutional AI (宪法AI, CAI) | Anthropic 提出的现代对齐方法 (Claude, GPT-4o)，用原则而非人类反馈来约束模型 | 模型自我审查是否违反预设"宪法"原则 |

### LLM Limitations (LLM 局限)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Knowledge Cutoff (知识截止) | LLM 知识受限于预训练数据的截止日期，无法获取最新信息 | "Who is the current PM?" → 可能给出过时答案 |
| Limited Context Size (有限上下文) | 超过上下文窗口的内容会被截断或丢失 | 处理100页PDF → 只能看前几页 |
| Pricing Per Token (按Token定价) | 商用 API 按输入/输出 token 数量收费 | 1M tokens 输入 ≈ $2.50 (GPT-4o) |
| Energy Consumption (能源消耗) | 训练和推理 LLM 消耗大量计算资源和电力 | 训练 GPT-3 ≈ 1,287 MWh |
| No Real Understanding (无真正理解) | LLM 做模式匹配而非推理，不理解因果关系 | 9.11 > 9.9? LLM可能回答Yes (字符串比较) |
| Privacy Risks (隐私风险) | 可能记忆并泄漏训练数据中的敏感信息 | 训练数据含邮箱/电话 → 可能被提取 |

### RAG Architecture (RAG 架构)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| RAG (检索增强生成) | 检索相关文档 → 增强提示 → 生成基于文档的答案；解决LLM知识过时和幻觉问题 | 动机: 领域精确/数据更新/可追溯/成本可控/隐私保护 |
| Knowledge Base (知识库) | RAG 的前提条件：收集文档 → 分块 → 嵌入 → 存入向量数据库 | Collect → Divide → Embed → Store |
| Chunking (分块) | 把长文档切成小段用于嵌入，方法: 固定大小 / 按自然边界 (段落/句子) | 固定512 tokens vs 按段落分割 |
| Embedding Model (嵌入模型) | 把文本块转换为稠密向量用于语义搜索 | [0.48, 0.33, ..., -0.51] |
| Vector Store (向量数据库) | 存储文档嵌入的专用数据库，支持高效相似度搜索 | Chroma, Weaviate, Milvus, Qdrant, Faiss |
| Retriever (检索器) | 用查询嵌入在向量数据库中搜索最相关的文档块 | query embedding → cosine similarity → top-k chunks |
| Generator (生成器) | LLM 根据检索到的上下文生成基于文档的答案 | prompt = context + question → LLM → answer |
| Prompt Template (提示模板) | RAG 中组合上下文和问题的固定模板 | "Answer based on context: {context}\nQuestion: {question}" |

### RAG Frameworks (RAG 框架)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| LangChain (链式框架) | 模块化 LLM 集成框架：链接多个服务、目标驱动代理、记忆持久化、开源 | 链接: 检索→嵌入→LLM→后处理 |
| HELM (全面评估) | 斯坦福的 LLM 全面评估框架，从6个维度评估: 准确/校准/鲁棒/公平/偏见/效率 | Holistic Evaluation of Language Models |

### LLM Deployment (LLM 部署)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Ollama (本地部署工具) | 最简单的本地 LLM 运行工具，一条命令部署 | `ollama pull llama3.3:8b` |
| vLLM (高效推理引擎) | 使用 PagedAttention 优化 GPU 内存的生产级推理引擎，支持多GPU | 生产部署首选 |
| HuggingFace (模型平台) | 模型/数据集/实验的一站式平台，支持 Accelerate 多GPU | 研究和微调首选 |

## 2. Comparisons (对比)

### LLM Model Comparison (LLM 模型对比)

| Model (模型) | Parameters (参数) | Size FP32 | Memory FP16 | Training Data | Example (示例) |
|-------|-----------|------|------|-------|---------|
| BERT-large | 340M | ~1.3 GB | ~1.5-2 GB | 3.3B words | 理解任务基线 |
| GPT-4o | ~200B | ~350 GB | ~400 GB | ~300B tokens | 最强商用模型 |
| LLaMA-13B | 13B | ~26 GB | ~26 GB | ~1T tokens | 中等开源模型 |
| LLaMA-70B | 70B | ~140 GB | ~140 GB | ~1T tokens | 大型开源模型 |
| Mistral 7B | 7B | ~14 GB | ~14 GB | ~1T tokens | 高效小模型 |

### LLM Deployment Tools (部署工具对比)

| Dimension (维度) | Ollama | vLLM | HuggingFace | Example (示例) |
|-----------|--------|------|-------------|---------|
| Ease of use (易用性) | ✅ 最简单 | 中等 | 复杂 | Ollama: 一条命令; HF: 需要代码 |
| GPU optimization (GPU优化) | 基本 | ✅ PagedAttention | ✅ Accelerate | vLLM 内存效率最高 |
| Multi-GPU (多GPU) | ❌ 不支持 | ✅ 支持 | ✅ 支持 | 70B模型需要多GPU |
| Best for (适合) | 本地开发/测试 | 生产部署 | 研究/微调 | 根据场景选择 |

### RAG vs Pure LLM (RAG vs 纯LLM)

| Dimension (维度) | Pure LLM (纯LLM) | RAG (检索增强) | Example (示例) |
|-----------|----------|-----|---------|
| Knowledge (知识) | 仅训练数据 (静态) | 动态 (检索最新文档) | RAG 可以访问最新信息 |
| Hallucination (幻觉) | ⚠️ 风险高 | ✅ 基于文档回答 (减少) | 无RAG: "2020" (错); 有RAG: "2018" (对) |
| Domain knowledge (领域知识) | ❌ 有限 | ✅ 自定义知识库 | 公司内部文档 → RAG 可用 |
| Transparency (透明度) | ❌ 黑箱 | ✅ 可展示源文档 | "According to Chapter 3, page 45..." |
| Cost (成本) | 高 (需更大模型) | 低 (小模型+检索) | Qwen 0.5B + RAG ≈ GPT-4 on domain QA |

### 8GB vs 16GB RAM 可运行的开源模型

| RAM | Model (模型) | Size (大小) | Ollama Command | Example (示例) |
|-----|-------|------|------|---------|
| 8GB | Llama 3.3 8B | 4.9 GB | `ollama pull llama3.3:8b` | 笔记本/低端PC |
| 8GB | Mistral 7B | 4.1 GB | `ollama pull mistral:7b` | 高效通用 |
| 16GB | DeepSeek R1 14B | ~9 GB | `ollama pull deepseek-r1:14b` | 思维链QA |
| 16GB | Qwen 2.5 14B | ~9 GB | `ollama pull qwen2.5:14b` | 多语言QA |

## 3. Formulas (公式)

### Retrieval Evaluation Metrics (检索评估指标)

| Metric (指标) | Formula (公式) | Description (说明) | Example (示例) |
|--------|---------|-------------|---------|
| Precision@k | $P@k = \frac{\text{relevant in top-}k}{k}$ | top-k 中相关文档的比例 | top-5 中 3 个相关 → P@5=0.6 |
| Recall@k | $R@k = \frac{\text{relevant in top-}k}{\text{total relevant}}$ | 所有相关文档中被检索到的比例 | 10个相关文档中找到3个 → R@5=0.3 |
| MRR (Mean Reciprocal Rank) | $\text{MRR} = \frac{1}{\text{rank of first relevant}}$ | 第一个相关结果的排名倒数 | 第一个相关在第2位 → MRR=0.5 |
| NDCG@k | $\text{NDCG}@k = \frac{\text{DCG}@k}{\text{IDCG}@k}$ | 归一化折损累积增益，考虑排序质量 | DCG=4.28, IDCG=5.19 → NDCG≈0.82 |
| DCG@k | $\text{DCG}@k = \sum_{i=1}^{k} \frac{rel_i}{\log_2(i+1)}$ | 折损累积增益：排名越靠后惩罚越大 | rel=[1,3,2,0,1] → 1+1.89+1+0+0.39=4.28 |

### RAG Pipeline Steps (RAG 流水线步骤)

| Step (步骤) | Operation (操作) | Description (说明) | Example (示例) |
|------|-----------|-------------|---------|
| 1. Parsing (解析) | 文档解析为文本 | PDF/HTML/DOCX → 纯文本 | PyMuPDF 提取 PDF 文本 |
| 2. Chunking (分块) | 文本切分为块 | 固定大小 or 自然边界 | 256-512 tokens + 50 overlap |
| 3. Embedding (嵌入) | 块 → 向量 → 存入向量DB | 文本 → [0.48, 0.33, ...] | Sentence-BERT 编码 |
| 4. Retrieval (检索) | 查询嵌入 → 相似搜索 → top-k | cosine similarity → 最相关块 | top-5 chunks |
| 5. Augment (增强) | 检索结果插入 prompt | context + question → LLM | "Based on: {chunks}\nQ: {question}" |
| 6. Generate (生成) | LLM 基于上下文生成答案 | 有据可依的回答 | "According to the document..." |

## 4. Practical / Lab (实战结论)

### 🔑 Key RAG Distinctions (关键RAG区别)

| Distinction (区别) | Detail (详情) | Example (示例) |
|-------------|--------|---------| 
| Temperature=0 → 确定性 | Temperature=1 → 创造性/随机 | T=0: 总是"Paris"; T=1: 可能说"Lyon" |
| Top-k 限制候选 token 数 | Top-p 按累积概率限制 | Top-k=50: 50个最可能; Top-p=0.9: 保留90%概率 |
| Chunk 太小 → 丢失上下文 | Chunk 太大 → 噪声稀释答案 | 50字: 太短信息不完整; 5000字: 无关信息混入 |
| RAG ≠ Fine-tuning | RAG = 运行时外部检索; Fine-tune = 修改模型权重 | RAG: 搜索文档; Fine-tune: 重训模型 |
| NDCG@k 评估检索排序质量 | 不仅考虑是否检索到，还考虑排序是否正确 | 相关文档排第1位 > 排第5位 |
| 向量数据库选择影响性能 | Chroma(简单), Faiss(快速), Milvus(分布式) → 根据场景选 | 本地开发: Chroma; 生产: Milvus |

### 📊 Assignment 2 Conclusions (作业2结论): RAG System

| Conclusion (结论) | Detail (详情) | Example (示例) |
|------------|--------|---------| 
| RAG 减少幻觉 | 答案基于文档，有据可依 | 无RAG: "2020"(错); 有RAG: "2018"(对) |
| 小模型 (0.5B) + RAG 可以有效 | 不需要巨大模型做领域 QA | Qwen2.5-0.5B + RAG ≈ GPT-4 on domain QA |
| Chunk size 至关重要 | 太小→丢上下文; 太大→噪声 | 最优: 256-512 tokens + 50 token overlap |
| 显示来源建立用户信任 | 用户可以对照文档验证答案 | "According to Chapter 3, page 45: ..." |
| 内存约束: <1.5 GB 3组件共存 | Whisper + Ollama + gTTS 必须同时运行 | Whisper~0.4G + Qwen~0.4G + gTTS~0.1G ≈ 0.9G |

### ⚠️ W12 考试陷阱 (Exam Traps)

| Trap (陷阱) | Correct Answer (正确答案) | Example (示例) |
|------|----------------|---------| 
| LLM "理解"语言? | ❌ 模式匹配，非推理! 没有真正的因果理解 | 9.11 > 9.9? LLM可能说Yes (字符串比较非数学) |
| 更多参数一定更好? | ❌ DistilBERT (66M) ≈ BERT (110M) 多数任务 | 参数多不一定好; 有时小模型+RAG更实用 |
| RAG 完全解决幻觉? | ❌ 减少但不消除! 可能检索到错误段落仍会幻觉 | RAG检索了错误chunk → 仍可能生成错误答案 |
| LLM 知识是最新的? | ❌ 训练数据有截止日期! 之后的事件不知道 | 问2026年的事 → 2024训练截止的模型不知道 |
| Temperature 越高越好? | ❌ 高→创造性但不准确; 低→准确但单调；精确QA用低T | 事实问答: T=0; 创意写作: T=0.7-1.0 |
| RAG = Fine-tuning? | ❌ 完全不同! RAG=运行时检索文档; Fine-tuning=修改模型权重 | RAG不改模型; Fine-tuning改模型 |

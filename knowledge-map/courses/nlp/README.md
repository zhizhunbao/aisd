# Natural Language Processing Knowledge Map

> 来源课程：Stanford CS224N (Diyi Yang) · CMU 11-711 · Jurafsky & Martin 教材
> 级别：研究生 Master · 角色：ML 工程师
> 前置课程：`deep-learning` (研究生级) · `machine-learning` (研究生级)

## 课程定位

NLP 是研究生级别独立课程，覆盖从经典语言学到大语言模型的完整链路：

| 维度 | Deep Learning (研究生) | NLP (研究生) |
|------|----------------------|-------------|
| 重点 | 通用神经网络架构与训练 | 语言理解与生成的模型与应用 |
| 核心模型 | CNN / RNN / Transformer | Word2Vec / BERT / GPT / LLM |
| 核心任务 | 分类 / 回归 / 生成 | 翻译 / 摘要 / QA / 对话 / Agent |
| 数据类型 | 通用张量数据 | 文本序列 + 多模态 |

## 主题列表

| 主题 | 文件数 | 状态 | 描述 |
|------|--------|------|------|
| linguistic_foundations | 0 | 🔲 planned | 语言学基础：音素/词素/句法/语义/依存分析 |
| text_preprocessing | 0 | 🔲 planned | 文本预处理：BPE/WordPiece/SentencePiece 分词 |
| word_vectors | 9 | ✅ current | 词向量：完整 9 维知识地图 (Word2Vec CBOW/Skip-gram/负采样/GloVe/FastText/ELMo/余弦相似度/词类比) |
| language_models | 0 | 🔲 planned | 语言模型：N-gram/神经LM/自回归/掩码LM |
| rnn_seq_models | 0 | 🔲 planned | 序列模型：RNN/LSTM/GRU/Seq2Seq/Teacher Forcing |
| attention_transformer | 9 | ✅ current | 注意力与Transformer：完整 9 维知识地图 (Self-Attention/MHA/位置编码/Encoder-Decoder) |
| pretrained_lm (bert) | 9 | ✅ current | 预训练模型：BERT 完整 9 维知识地图 (Map/Concepts/Math/Tutorial/Code/Pitfalls/History/Bridge/First Principles) |
| pretrained_lm (gpt) | 9 | ✅ current | 预训练模型：GPT 完整 9 维知识地图 (Map/Concepts/Math/Tutorial/Code/Pitfalls/History/Bridge/First Principles) |
| llm | 0 | 🔲 planned | 大语言模型：GPT-4/LLaMA/缩放定律/涌现/ICL/CoT |
| peft | 0 | 🔲 planned | 参数高效微调：LoRA/QLoRA/Adapter/Prefix Tuning |
| nlp_tasks | 0 | 🔲 planned | 核心任务：分类/NER/翻译/摘要/QA/对话 |
| evaluation | 0 | 🔲 planned | 评估指标：BLEU/ROUGE/BERTScore/Perplexity/MMLU |
| rag | 0 | 🔲 planned | 检索增强生成：向量数据库/稠密检索/Chunking/Grounding |
| ai_agents | 0 | 🔲 planned | AI Agent：ReAct/工具调用/多步推理/多智能体 |

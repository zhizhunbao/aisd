# W13: LLM Compression & Prompt Engineering (LLM压缩 & 提示工程)

## 1. Definitions (定义)

### Model Compression (模型压缩)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Model Compression (模型压缩) | 在不显著损失准确性的前提下，减小模型体积和计算成本的技术，实现低成本高效部署 | 三种主要技术: 量化、剪枝、蒸馏 |
| Quantization (量化) | 降低权重数值精度：FP32→FP16→INT8→INT4；无需重训练，直接压缩模型 | 65B×4B=260GB(FP32) → 65B×1B=65GB(INT8) |
| FP32 / FP16 / INT8 / INT4 | 不同精度格式：FP32=32位浮点(1+8+23); FP16=半精度; INT8=8位整数; INT4=4位 | FP32: N×4字节; FP16: N×2; INT8: N×1; INT4: N×0.5 |
| Dynamic Quantization (动态量化) | 训练后直接对已有模型做量化，无需额外训练数据 | `torch.quantization.quantize_dynamic(model, {nn.Linear}, dtype=qint8)` |
| Binarized Neural Network (二值化网络) | 极端量化: 权重只用1-bit表示 (0或1)，体积可缩小32倍 | Microsoft BitNet: 1-bit 权重量化 |
| Knowledge Distillation (知识蒸馏) | 训练小"学生"模型模仿大"教师"模型的输出分布，保留大部分性能 | BERT(teacher) → DistilBERT(student): 97%性能, 60%更小 |
| Teacher Model (教师模型) | 蒸馏中提供知识的大模型，产生 soft predictions 用于指导学生 | BERT-large (340M params) |
| Student Model (学生模型) | 蒸馏中学习知识的小模型，从教师的软标签中学习 | DistilBERT (66M params) |
| Pruning (剪枝) | 移除不重要的权重/神经元/层；基于幅值(Magnitude-Based)裁剪训练后的模型 | 移除90%的小权重 → 需重训来恢复准确率 |
| Structured vs Unstructured Pruning | 结构化: 移除整个神经元/层; 非结构化: 单独权重置零 | 结构化硬件友好; 非结构化压缩率更高 |

### Transfer Learning & PEFT (迁移学习与参数高效微调)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Transfer Learning (迁移学习) | 冻结预训练模型，只训练新加的分类头 (0.1%参数)，最快最节省 | 冻结BERT→加Dense层→训练分类 |
| Full Fine-tuning (全量微调) | 调整模型的全部参数 (100%)，效果最好但内存极高，存在灾难性遗忘风险 | 7B模型全量微调需要大量GPU内存 |
| SFT (Supervised Fine-Tuning, 监督微调) | 在指令-响应对上做监督微调，GPT-3用1.3万条，LLaMA 3用1000万条 | 高质量标注数据的数量决定微调效果 |
| PEFT (Parameter-Efficient Fine-Tuning) | 只调少量参数的微调方法总称：Prompt/Prefix、Adapters、BitFit、LoRA | 不调所有参数，只调一部分! |
| LoRA (Low-Rank Adaptation) | 冻结原模型，只训练两个小低秩矩阵 A(d×r) 和 B(r×d)，r=4~16，参数减98% | W'=W+ΔW; ΔW=A×B; d²→2dr (r≪d) |
| LoRA 应用位置 | 通常应用于 Transformer 的注意力权重矩阵 Wq, Wk, Wv, Wo | 只在注意力层加适配器 |
| LoRA 实证发现 | LoRA 需要比全量微调更高的学习率；在大batch size下表现较差 | LoRA lr > Full FT lr |
| QLoRA | LoRA + 4-bit 量化基座模型；可在消费级 GPU 上微调大模型! | 65B模型 → 48GB GPU 可训练! |

### Prompt Engineering (提示工程)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Prompt Engineering (提示工程) | 向 LLM 提出正确问题以获得最佳输出的技术；仅用自然语言提示即可交互 | 提升任务表现/控制输出/减轻偏见/增强可解释性 |
| Prompt Elements (提示四要素) | 一个完整 prompt 由 4 部分组成: Context(上下文) + Instructions(指令) + Input(输入) + Output Indicator(输出指示) | "你是数据科学家(Context), 做情感分析(Instruction), 文本:…(Input), Sentiment:(Output)" |
| Zero-shot (零样本提示) | 只给任务指令，不给任何示例，依靠模型自身知识 | "Translate: Hello → French" → "Bonjour" |
| One-shot (单样本提示) | 任务指令 + 1个示例，给模型格式参考 | "'great!'→Positive. Classify: 'okay'" |
| Few-shot (少样本提示) | 任务指令 + 2-5个示例，适合复杂或歧义任务 | GPT-3论文: "Language Models are Few-Shot Learners" |
| Chain-of-Thought (思维链, CoT) | "Let's think step by step" → 强制模型展示推理过程，适合数学/逻辑/多步骤问题 | "5-2=? Step1:从5开始 Step2:减2 Step3:答案3" |
| Chain Prompts (链式提示) | 多个 prompt 串联处理复杂任务，前一步输出作为后一步输入 | 步骤1:提取关键词 → 步骤2:根据关键词分类 |
| Role-Based Prompting (角色提示) | "You are a [domain expert]..." → 赋予模型特定角色身份以获得领域专业回答 | "You are a hiring manager. Conduct a mock interview." |
| Persona-Guided Prompting (人格引导) | 赋予模型特定历史人物/名人的写作风格和性格 | "You are Shakespeare. Write a poem about night." |
| System Prompt (系统提示) | 设定模型的人格、约束和行为规范的特殊提示 | "你是一个礼貌的助手，不回答政治问题" |

### Prompt Best Practices (提示最佳实践)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| 10 Best Practices (10条最佳实践) | 1.具体清晰 2.提供上下文 3.分解任务 4.用CoT推理 5.尝试few-shot 6.用角色提示 7.要求澄清 8.注意偏见 9.要求结构化输出 10.迭代优化 | 持续调整 prompt 是关键 |

## 2. Comparisons (对比)

### Quantization vs Pruning vs Distillation (压缩三法对比)

| Dimension (维度) | Quantization (量化) | Pruning (剪枝) | Distillation (蒸馏) | Example (示例) |
|-----------|---------------------|----------------|---------------------|---------|
| What it does (做什么) | 降低数值精度 (FP32→INT8) | 移除不重要的连接/权重 | 训练小模型模仿大模型 | 精度↓ vs 连接↓ vs 全新模型 |
| Parameters changed (参数变化) | 不改变参数值，只改精度 | 部分参数置零，其余不变 | 所有参数都改变 (新模型) | 量化保留结构; 蒸馏重新训练 |
| Re-training (重训练) | ❌ 训练后直接压缩 | ⚠️ 可能需要重训练 | ✅ 需要完整训练周期 | 量化最快; 蒸馏最慢 |
| Size reduction (体积缩小) | ~2-8× | ~2-10× | 取决于学生模型设计 | INT8≈4×; INT4≈8× |
| Quality loss (质量损失) | FP16极小; INT4中等 | 可能显著 (需重训) | 取决于学生模型大小 | BERT FP16:99.5%; INT4:~95% |
| Example (示例) | BERT FP32→INT8: 1.3G→340MB | 移除90%权重→重训 | BERT→DistilBERT: 97%性能 | 各方法优缺互补 |

### Transfer Learning vs Full Fine-tuning vs LoRA

| Dimension (维度) | Transfer Learning (迁移学习) | Full Fine-tuning (全量微调) | LoRA (低秩适配) | Example (示例) |
|-----------|-------------------|------------------|------|---------|
| What changes (改什么) | 冻结基座 + 训练分类头 | 所有参数 | 小适配矩阵 (A, B) | 调的参数量不同 |
| Parameters trained (训练参数) | ~0.1% | 100% | ~0.1-1% | LoRA 极省内存 |
| Memory (内存) | 低 | 非常高 | 低 | 7B全量→需40GB+; LoRA→8GB |
| Speed (速度) | 快 | 慢 | 中等 | 全量微调需数天 |
| Catastrophic Forgetting (灾难遗忘) | 低风险 | 高风险 | 低风险 | 全量微调可能丢失预训练知识 |

### Distilled Models (蒸馏模型案例)

| Teacher (教师) | Student (学生) | Size Reduction (缩小) | Speed (加速) | Quality (性能保留) | Example (示例) |
|--------|---------|------|------|------|---------|
| BERT | DistilBERT | 60% | 2× | 97% | 实时/移动应用 |
| GPT-2 | DistilGPT-2 | 60% | 2× | 97% | 文本生成/聊天 |
| T5 | Distilled T5 | 60% | >1× | 96% | 翻译/摘要/QA |

### Prompt Engineering Types (提示工程类型对比)

| Type (类型) | When to use (适用场景) | Pros (优点) | Example (示例) |
|------|------------|------|---------|
| Zero-shot (零样本) | 简单任务，模型有知识 | 最快，无需准备 | "Translate: Hello → French" |
| One-shot (单样本) | 需要格式引导 | 一个例子就够 | "'great!'→Pos. Classify: 'okay'" |
| Few-shot (少样本) | 复杂/歧义任务 | 效果最稳定 | 2-5个标注示例 + 新输入 |
| CoT (思维链) | 数学/推理/多步骤 | 强制逻辑推理 | "Let's think step by step..." |
| Role-based (角色) | 需要领域专家回答 | 领域匹配度高 | "You are a senior Python developer" |
| Persona (人格) | 需要特定风格 | 创意输出 | "You are Shakespeare" |

### LLM Model Sizes (模型大小对比)

| Model (模型) | Params (参数) | FP32 | FP16 | INT8 | INT4 | Example (示例) |
|-------|--------|------|------|------|------|---------|
| BERT-large | 340M | 1.3 GB | 680 MB | 340 MB | 170 MB | 理解任务基线 |
| LLaMA-7B | 7B | 28 GB | 14 GB | 7 GB | 3.5 GB | 消费级GPU可运行 |
| LLaMA-70B | 70B | 280 GB | 140 GB | 70 GB | 35 GB | 需多GPU |
| Rule (规则) | N params | N×4 | N×2 | N×1 | N×0.5 | **考试必记公式** |

## 3. Formulas (公式)

### Quantization Size Calculation (量化大小计算)

| Formula (公式) | Description (说明) | Example (示例) |
|---------|-------------|---------|
| $\text{FP32}: N_{\text{params}} \times 4 \text{ bytes}$ | 全精度: 每个参数占4字节 | 340M × 4 = 1.36 GB |
| $\text{FP16}: N_{\text{params}} \times 2 \text{ bytes}$ | 半精度: 每个参数占2字节 | 340M × 2 = 680 MB |
| $\text{INT8}: N_{\text{params}} \times 1 \text{ byte}$ | 8位整数: 每个参数占1字节 | 340M × 1 = 340 MB |
| $\text{INT4}: N_{\text{params}} \times 0.5 \text{ bytes}$ | 4位整数: 每个参数占0.5字节 | 340M × 0.5 = 170 MB |

### Floating Point Format (浮点格式)

| Format (格式) | Sign (符号位) | Exponent (指数位) | Mantissa (尾数位) | Example (示例) |
|--------|------|----------|----------|---------|
| FP16 | 1 | 5 | 10 | 半精度: 16位 = 1+5+10 |
| FP32 | 1 | 8 | 23 | 单精度: 32位 = 1+8+23 |
| FP64 | 1 | 11 | 52 | 双精度: 64位 = 1+11+52 |

### Distillation Loss (蒸馏损失)

| Formula (公式) | Description (说明) | Example (示例) |
|---------|-------------|---------|
| $\mathcal{L} = \alpha \cdot \mathcal{L}_{\text{hard}} + (1-\alpha) \cdot \mathcal{L}_{\text{soft}}$ | 组合损失: hard label + soft label | α 平衡两项损失 |
| $\mathcal{L}_{\text{hard}} = \text{CE}(\hat{y}_{\text{student}}, y_{\text{true}})$ | 标准交叉熵: 学生预测 vs 真实标签 | 监督学习部分 |
| $\mathcal{L}_{\text{soft}} = \text{KL}\!\left(\frac{\hat{y}_s}{T},\ \frac{\hat{y}_t}{T}\right)$ | KL散度: 学生 vs 教师的软概率分布 | T=温度, 越大分布越软 |

### LoRA Math (LoRA 数学)

| Formula (公式) | Description (说明) | Example (示例) |
|---------|-------------|---------|
| $W' = W + \Delta W$ | 新权重 = 原始权重 + 适配器增量 | 训练后直接加入, 无新组件 |
| $\Delta W = A \times B,\ A \in \mathbb{R}^{d \times r},\ B \in \mathbb{R}^{r \times d}$ | 低秩分解: d²个参数 → 2dr个参数 (r≪d) | r=4, d=768 → 98%参数减少 |
| $d^2 \to 2dr$ | 参数量从 d² 降到 2dr (r 越小越节省) | d=768, r=4: 590K→6K/层 |

## 4. Practical / Lab (实战结论)

### 🔑 Key Compression Distinctions (关键压缩区别)

| Distinction (区别) | Detail (详情) | Example (示例) |
|-------------|--------|---------| 
| 量化 = 无需重训练 | 训练后直接 FP32→INT8，~4× 更小 | BERT 1.3GB(FP32) → 340MB(INT8) |
| 剪枝可能需要重训练 | 移除连接后可能降低质量，需 fine-tune 恢复 | 移除90%权重 → 重训恢复准确率 |
| 蒸馏 = 完整训练周期 | 从头训练学生模型模仿教师 | BERT→DistilBERT: 保留97%质量 |
| LoRA r=4~16 | 越小的 r = 越少参数; r太小→欠拟合 | r=4: 6K params/层; r=16: 24K/层 |
| QLoRA = LoRA + 4-bit量化基座 | 在消费级 GPU 上微调大模型! | 65B模型 → 48GB GPU 可训练 |
| 量化/剪枝/蒸馏可以组合使用 | 三种方法互补不冲突 | 先蒸馏得小模型→再量化→再剪枝 |

### 📊 Prompt Engineering Exam Templates (提示工程考试模板)

| Type (类型) | Template (模板) | When (适用场景) | Example (示例) |
|------|----------|------|---------| 
| Zero-shot | "Classify: '{text}'" | 简单任务, 模型有知识 | "Classify sentiment: 'I love this'" → Positive |
| Few-shot | "Ex: 'Great!'→Pos ... Classify: '{text}'" | 需要格式/模式引导 | 给2-5个示例后 classify |
| CoT | "Let's think step by step..." | 数学, 推理, 多步骤 | "17×24? Step1:17×20=340 Step2:17×4=68 Answer:408" |
| Role-based | "You are a [domain] expert..." | 需要领域专家回答 | "You are a cardiologist. Explain chest pain." |
| Persona | "You are [historical figure]..." | 需要特定风格 | "You are Shakespeare. Write a poem about night." |

### ⚠️ W13 考试陷阱 (Exam Traps)

| Trap (陷阱) | Correct Answer (正确答案) | Example (示例) |
|------|----------------|---------| 
| FP16 vs INT8 质量损失? | FP16 = 极小 (99.5%); INT8 = 轻微; INT4 = 中等 (~95%) | BERT FP16: 99.5% of FP32 |
| DistilBERT = 蒸馏示例 | 97% BERT性能, 40% 更小内存, 60% 更快 | 110M → 66M params; 推理2×快 |
| LoRA 训练所有参数? | ❌ 只训练小适配矩阵 (~0.1-1%)! 基座模型冻结! | 7B模型: 全量=7B params; LoRA=~7M params |
| 大小规则: N params × ? bytes | FP32=×4, FP16=×2, INT8=×1, INT4=×0.5 → **必记!** | 340M × 4 = 1.36GB (FP32); × 1 = 340MB (INT8) |
| QLoRA 只是 LoRA? | ❌ QLoRA = LoRA + 4-bit 量化基座！量化减内存+LoRA减训练参数 | 65B model → 48GB GPU 可训练 |
| Quantization 改变参数值? | ❌ 量化不改变参数值, 只降低精度表示! 剪枝才移除参数 | 量化: 值不变精度降; 剪枝: 值=0移除 |
| Zero-shot 总是比 Few-shot 好? | ❌ Few-shot 通常更稳定! Zero-shot 只在简单任务上够用 | 复杂歧义任务 → Few-shot 必须 |
| CoT 适用于所有任务? | ❌ CoT 适合推理/数学/多步骤; 简单分类用 Zero/Few-shot 更高效 | 情感分类不需要 step-by-step |

# W12: LLM Fine-Tuning & LoRA (LLM 微调与 LoRA)

> **本页缩写 (Abbreviations used)**
> **API** = Application Programming Interface  
> **GIGO** = Garbage In, Garbage Out  
> **GPT** = Generative Pre-trained Transformer  
> **GPU** = Graphics Processing Unit  
> **ML** = Machine Learning  
> **RAG** = Retrieval Augmented Generation  
> **YAML** = YAML Aint Markup Language


## 1. Definitions (定义)

### Fine-Tuning Basics (微调基础)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| LLM Fine-Tuning (LLM 微调) | 用领域数据"再训练"一个已经学过通用知识的模型，使其在特定任务上成为专家 (re-train a pre-trained model on domain-specific data to become a specialist)——从"全科医生"到"专科医生" | Home Cook (Homer) → Sushi Chef (Kenji) |
| Pre-trained LLM (预训练大语言模型) | 在海量通用数据上训练好的模型 (model trained on massive general data)，拥有广泛但浅层的知识——像"家庭厨师"什么都会一点 | GPT-4, Llama-3 |
| Full Fine-Tuning (全量微调) | 更新模型的全部参数 (update all parameters, billions)，效果最强但成本极高且可能导致灾难性遗忘 | 需要多张 H100 GPU |
| Catastrophic Forgetting (灾难性遗忘) | 微调学了新领域知识后忘记了原有通用知识 (learning new domain knowledge causes forgetting of general knowledge) | 学了网络安全后忘了怎么翻译 |

### LoRA (低秩适配)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| LoRA (Low-Rank Adaptation) | 冻结原始权重 + 训练低秩适配器矩阵的微调方法 (freeze original weights, train small low-rank adapter matrices)，核心公式 $W_{new} = W_{orig} + A \times B$，不到 1% 的参数即可达到接近全量微调的效果 | d=4096, r=16 → LoRA 参数仅占 0.78% |
| $W_{orig}$ (原始权重) | 预训练模型的原始权重矩阵 (original pre-trained weights)，大小 d×d，状态 **Frozen（冻结不动）** | 一本 1000 页的百科全书 |
| $A$ (低秩矩阵 A) | LoRA 适配器的下投影矩阵 (down-projection matrix)，大小 d×r（r≪d），状态 **Trainable** | 便利贴的一半 |
| $B$ (低秩矩阵 B) | LoRA 适配器的上投影矩阵 (up-projection matrix)，大小 r×d（r≪d），状态 **Trainable** | 便利贴的另一半 |
| Rank $r$ (秩) | LoRA 适配器的秩/维度 (rank of adapter)，r≪d，决定适配器的大小和表达能力 | r=16 时仅 0.78% 参数 |
| Base LLM (基座模型) | LoRA 架构中的核心通用知识层 (generalist core)，参数 Billions 级，**Frozen** 状态 | Llama-3-8B |
| LoRA Adapter (LoRA 适配器) | LoRA 架构中的新任务/领域技能层 (specialist layer)，参数 Millions 级，**Updatable** 状态 | 网络安全 Adapter |

### Fine-Tuning Frameworks (微调框架)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Unsloth | 极致速度和低显存的微调框架 (speed + low VRAM optimized)，适合个人学习和单卡消费级 GPU | RTX 4090 上微调 Llama-3 |
| Axolotl | 面向可复现性和大规模训练的微调框架 (reproducibility + large-scale)，原生多卡支持最佳 | H100 集群上训练 70B 模型 |
| LLaMA-Factory | 易用一体化微调框架 (easy all-in-one)，提供 Web UI (LlamaBoard)，不写代码即可微调 | 通过网页界面一键启动微调 |
| HF PEFT | HuggingFace 的 Parameter-Efficient Fine-Tuning 库，纯 Python API，最灵活适合深度集成 (flexible API for custom integration) | 嵌入到已有 ML pipeline 中 |

## 2. Comparisons (对比)

### Full Fine-Tuning vs LoRA

| Dimension (维度) | Full Fine-Tuning (全量微调) | LoRA (低秩适配) | Example (示例) |
|-----------|---|---|---------| 
| 更新范围 | **全部**参数 | 冻结原始 + 训练小型适配器 | 重新印刷整本书 vs 贴便利贴 |
| 参数量 | Billions（数十亿） | Millions（百万级，<1%） | d=4096: 1677 万 vs 13 万 |
| 计算成本 | ❌ 极高 | ✅ 低 | 多张 H100 vs 单张 RTX 4090 |
| 灾难性遗忘 | ⚠️ 可能 | ✅ 不会（原始权重冻结） | 学了寿司忘了做意面 vs 不会忘 |
| 多任务切换 | ❌ 每个任务一份完整模型 | ✅ 换个 Adapter 就行 | 存 N 个完整模型 vs 存 N 个小 Adapter |
| 效果 | ✅ 最强 | ✅ 接近全量微调 | — |

### 微调决策：何时微调 vs 不微调

| Dimension (维度) | ✅ 需要微调 | ❌ 不需要/不该微调 | Example (示例) |
|-----------|---|---|---------| 
| 复杂任务 | ✅ 像专家一样完成高难度工作 | — | 像资深开发者一样写代码 |
| 简单任务 | — | ❌ 杀鸡用牛刀 → 用 Prompt Engineering | 简单 Q&A |
| 数据变化快 | — | ❌ 训完就过时 → 用 RAG 实时检索 | 股票价格预测 |
| 低质量数据 | — | ❌ GIGO 比不微调更差 → 先清洗数据 | 充满噪声的标注 |
| 隐私限制 | — | ❌ 敏感数据不能训练 → RAG + 本地部署 | 医疗患者数据 |

### 四大微调框架选型

| Dimension (维度) | Unsloth | Axolotl | LLaMA-Factory | HF PEFT | Example (示例) |
|-----------|---|---|---|---|---------| 
| 定位 | 极致速度/低显存 | 可复现性/大规模 | 易用一体化 | 核心逻辑/灵活 | — |
| 界面 | Python / No-code | YAML 配置 | **Web UI** | Python API | — |
| 硬件 | 单卡消费级 | 多卡 H100/A100 | 灵活 | 任意 | — |
| 上手难度 | 低~中 | 高 | **低** | 中~高 | — |
| 适合场景 | 个人/小项目 | 企业大规模 | 快速上手 | 深度集成 | — |

## 3. Formulas (公式)

### LoRA 核心公式

| Formula (公式) | Description (说明) | Example (示例) |
|---------|-------------|---------|
| $W_{new} = W_{orig} + A \times B$ | LoRA 核心公式：最终权重 = 冻结的原始权重 + 低秩适配器贡献 | d=4096, r=16 → Adapter 参数仅 0.78% |
| $LoRA\ params = d \times r + r \times d = 2dr$ | LoRA 适配器参数量：两个低秩矩阵 A(d×r) 和 B(r×d) 的参数总和 | d=4096, r=16 → 2×4096×16 = 131,072 |
| $Ratio = \frac{2dr}{d^2} = \frac{2r}{d}$ | LoRA 参数占原始参数的比例 | r=16, d=4096 → 比例 ≈ 0.78% |

## 4. Practical / Lab (实战结论)

### 📊 Lab/Assignment Conclusions (实验/作业结论)

| Conclusion (结论) | Detail (详情) | Example (示例) |
|------------|--------|---------| 
| Colab 微调 Llama 完整流程 5 步 | ① 加载 Base Model → ② 配置 LoRA (rank, alpha) → ③ 准备领域数据 → ④ 训练 Adapter → ⑤ 合并推理 | 用网络安全 Q&A 数据微调 Llama-3-8B |
| LoRA 实现了"训练民主化" | 消费级 GPU（如 RTX 4090）就能微调大模型，不再需要 H100 集群 | 个人开发者也能微调 8B 模型 |
| 同一个 Base LLM + 不同 LoRA Adapter = 不同领域专家 | 医疗/法律/代码 Adapter 随时切换，只需存储小型 Adapter 文件 | 医疗 LoRA + 法律 LoRA + 代码 LoRA 共享同一 Base |

## 5. Exam Traps (考试陷阱)

### ⚠️ Common Traps (常见陷阱)

| Trap (陷阱) | Correct Answer (正确答案) | Example (示例) |
|------|----------------|---------| 
| 一遇到 LLM 不够好就想微调 | 微调是**"最后手段"**——先试 Prompt Engineering，再试 RAG，都不行才微调 | 简单格式问题用 Few-shot 就够了 |
| 以为全量微调总是比 LoRA 好 | LoRA 效果**接近全量微调**，但成本低得多且**无灾难性遗忘** | Full FT 可能反而因遗忘把通用能力弄差 |
| 以为 LoRA 需要更新所有参数 | LoRA **冻结全部原始权重** ($W_{orig}$ = Frozen)，只训练两个小矩阵 $A$ 和 $B$ | 原始的 Billions 参数一个不动 |
| 搞混 LoRA 中各矩阵的状态 | $W_{orig}$: **Frozen** / Billions；$A$, $B$: **Trainable** / Millions (< 1%) | 考试会考哪个是冻结的、哪个是可训练的 |
| 以为微调后就不需要管了 | 如果数据分布变化快（如股票），微调模型也会**过时**——这种场景应该用 RAG 而非微调 | 股票模型微调 → 下个月就失效 |
| 以为低质量数据微调会"至少有点用" | 低质量数据微调 **Garbage In → Garbage Out**，效果可能比不微调更差 | 充满错误标注的数据 → 模型学到错误模式 |

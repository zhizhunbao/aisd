# W6: Model Deployment & Compression (模型部署与压缩)

> **本页缩写 (Abbreviations used)**
> **API** = Application Programming Interface  
> **BF16** = Brain Floating Point 16-bit  
> **DB** = Database  
> **HPA** = Horizontal Pod Autoscaler  
> **ML** = Machine Learning  
> **NLU** = Natural Language Understanding  
> **AWS** = Amazon Web Services  
> **FP16** = 16-bit Floating Point  
> **FP32** = 32-bit Floating Point  



## 1. Definitions (定义)

### Deployment Myths (部署误区)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Model Decay (模型衰退) | 模型性能随时间自然下降 (model performance degrades over time)，根因是数据分布漂移 | 2019 年训练的房价模型在 2020 年疫情后预测失准 |
| Data Distribution Shift (数据分布漂移) | 训练数据和实际使用数据的分布不一致 (mismatch between training and production data)，导致模型衰退 | 训练数据主要是北京用户，上线后全国用户涌入 |

### Scaling Strategies (扩展策略)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Vertical Scaling (垂直扩展) | 给单台机器增加 CPU/内存 (add more resources to single machine)，简单但有天花板 | 从 8GB 升级到 64GB 内存 |
| Horizontal Scaling (水平扩展) | 增加更多机器 (add more machines)，适合无状态服务 | 从 1 台服务器扩展到 10 台 |
| Auto-scaling (自动扩展) | 根据负载自动调节机器数量 (auto-adjust based on load) | AWS Auto Scaling / K8s HPA |
| Microservices (微服务) | 系统拆分为独立服务各自扩展 (split system into independent services) | 推理服务和数据处理服务分开扩展 |
| Hybrid Scaling (混合扩展) | 垂直 + 水平结合 (combine vertical and horizontal)，大多数实际系统采用 | 先升级单机能力，不够再加机器 |

### Prediction Modes (预测模式)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Batch Prediction (批量预测) | 预测结果定期批量生成并存入数据库，用户需要时直接查 (asynchronous, pre-computed)，也叫异步预测 | Netflix 推荐列表——提前算好存着 |
| Online Prediction (在线预测) | 请求到达后立即生成并返回预测结果 (synchronous, real-time)，通过 RESTful API 接收请求 | 在线翻译——输入后立刻返回翻译结果 |

### Model Compression (模型压缩)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Low-Rank Factorization (低秩分解) | 用低维张量替换高维张量 (replace high-dimensional tensors with low-dimensional ones)，减少参数量 | SqueezeNet: 3×3 → 1×1 卷积，参数减少 50% |
| Knowledge Distillation (知识蒸馏) | 用大模型 Teacher 训练小模型 Student (large Teacher trains small Student)，Student 学到 Teacher 的知识用于部署 | DistilBERT: 大小 60%, 能力 97%, 速度 160% |
| Pruning (剪枝) | 将不重要的神经元权重设为零使网络变稀疏 (set unimportant weights to zero → sparse network)，可减少高达 90% 非零参数 | 绝对值 < 阈值的权重设为 0 |
| Quantization (量化) | 用更少的位数表示模型参数 (use fewer bits to represent parameters)，**最常用的压缩方法** | FP32 → FP16 → INT8 |
| DistilBERT | 知识蒸馏的典型成果 (Knowledge Distillation case study)，大小 60%、NLU 能力 97%、推理速度 160%，几乎无损 | BERT → DistilBERT 用于生产推理 |
| SqueezeNet | 低秩分解的典型成果 (Low-Rank Factorization case)，用 1×1 卷积替换 3×3 卷积，准确率与 AlexNet 相当但参数减半 | AlexNet 精度 + 50% 参数量 |

## 2. Comparisons (对比)

### 批量 vs 在线预测 (核心考试知识点)

| Dimension (维度) | Batch Prediction (批量预测) | Online Prediction (在线预测) | Example (示例) |
|-----------|---|---|---------| 
| 延迟 (Latency) | ✅ 低感知延迟（提前算好） | ⚠️ 可能高延迟 | 查 DB vs 现场推理 |
| 当前上下文 (Context) | ❌ 可能错过当前上下文 | ✅ 捕获当前上下文 | 不知用户"刚搜了什么" vs 实时捕获 |
| 计算效率 (Efficiency) | ✅ 批量推理很高效 | ⚠️ 单条推理开销大 | GPU 批推理 vs 逐条推理 |
| 输入需求 (Input) | ❌ 需要提前知道输入 | ✅ 输入随请求提供 | 预算所有商品推荐 vs 按搜索词推荐 |
| 资源浪费 (Waste) | ❌ 预测可能浪费（算了没人用） | ✅ 按需推理无浪费 | 预测 100 万结果只查 1 万 |
| 特征类型 (Features) | 仅批量特征 | 批量 + 流式特征都可 | — |
| 基础设施 (Infra) | ✅ 相对简单 | ❌ 需额外基础设施 | 定时任务 vs API Gateway + 推理服务 |

### GPU vs CPU 推理 (Roblox 案例)

| Dimension (维度) | GPU (V100) | CPU (Xeon 36 核) | Example (示例) |
|-----------|---|---|---------| 
| 训练 | ✅ 远快于 CPU | ❌ 慢 | — |
| 单条推理成本 | ❌ 贵 | ✅ 便宜 | — |
| 实际吞吐 | 400-500 次/秒 | **3,000 次/秒** | 同等成本下 CPU 吞吐量是 GPU 的 6-7 倍 |

### 四种压缩技术对比

| Dimension (维度) | Low-Rank Factorization | Knowledge Distillation | Pruning | Quantization | Example (示例) |
|-----------|---|---|---|---|---------| 
| 核心思想 | 低维矩阵替代高维 | 大模型教小模型 | 删除不重要权重 | 减少位数表示 | — |
| 比喻 | 简笔画替代油画 | 教授教本科生 | 修剪树枝 | 精装修降简装 | — |
| 常用程度 | 中 | 高 | 中 | **最高** | 量化是工业界最常用 |

### 蒸馏 vs 直接训练小模型

| Dimension (维度) | Knowledge Distillation (知识蒸馏) | Direct Training (直接训练小模型) | Example (示例) |
|-----------|---|---|---------| 
| 迁移学习 (Transfer) | ✅ Student 从 Teacher 学到通用知识 | ❌ 从零学 | DistilBERT 继承 BERT 的语言理解 |
| 正则化 (Regularization) | ✅ soft labels 包含更多信息 | ❌ 只有 hard labels | soft labels 提供类间关系 |
| 泛化 (Generalization) | ✅ Teacher 帮助避免过拟合 | ⚠️ 更容易过拟合 | — |

## 3. Formulas (公式)

### 量化存储计算

| Formula (公式) | Description (说明) | Example (示例) |
|---------|-------------|---------|
| 存储 = 参数量 × 位数 / 8 | 模型存储占用与精度的关系 | 1 亿参数: FP32=400MB, FP16=200MB, INT8=100MB |

## 4. Practical / Lab (实战结论)

### 📊 Lab/Assignment Conclusions (实验/作业结论)

| Conclusion (结论) | Detail (详情) | Example (示例) |
|------------|--------|---------| 
| Roblox 四步优化实现 CPU 上 10 亿次/天 BERT 推理 | BERT(固定128) → DistilBERT(蒸馏) → 动态输入(去 padding) → 量化(INT8) | 三种技术串联：蒸馏 + 动态输入 + 量化 |
| 将 PyTorch 线程数设为 1 反而更快 | 默认多线程导致多 worker 间线程竞争→性能停滞；每进程 1 线程避免切换开销 | 反直觉优化 |
| 在线预测延迟增加 500ms → 用户流量下降 20% | Google 研究：微小延迟对业务影响巨大 | 延迟对用户留存至关重要 |

## 5. Exam Traps (考试陷阱)

### ⚠️ Common Traps (常见陷阱)

| Trap (陷阱) | Correct Answer (正确答案) | Example (示例) |
|------|----------------|---------| 
| 以为模型上线后性能不会变 | 模型会因 **Data Distribution Shift** 自然衰退，需持续监控和定期重训 | 疫情导致房价模型完全失准 |
| 以为"加机器"是唯一扩展方式 | 有 **5 种扩展策略**：垂直/水平/自动/微服务/混合 | 混合扩展是大多数实际系统的选择 |
| 以为 GPU 推理一定比 CPU 好 | 同等成本下 CPU 推理吞吐量可以是 GPU 的 **6-7 倍** | Xeon 36核: 3000次/秒 vs V100: 400-500次/秒 |
| 量化的最新趋势搞混 | 训练: **FP16/BF16 可用、INT8 不可用**；推理: **INT8 可用** | INT8 训练精度损失太大，暂不可行 |
| 以为知识蒸馏不如直接训练小模型 | 蒸馏比直接训练**效果更好**：迁移学习 + 正则化 + 中间表示 + 改善泛化 | DistilBERT 比同规模直接训练的模型好 |
| 更多线程 = 更高性能 | Roblox 发现**每进程 1 线程**反而最快——多线程导致线程竞争和切换开销 | PyTorch 默认多线程在多 worker 下性能停滞 |
| 以为一个团队只需管理一两个模型 | 大公司如 Uber 同时运行 **200+ 个 ML 模型**，架构必须支持多模型并行管理 | 需求预测、ETA、定价、欺诈检测各有独立模型 |

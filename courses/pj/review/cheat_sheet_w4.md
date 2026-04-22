# W4: Algorithm Selection, Distributed Training & AutoML (算法选择、分布式训练与 AutoML)

> **本页缩写 (Abbreviations used)**
> **API** = Application Programming Interface  
> **BERT** = Bidirectional Encoder Representations from Transformers  
> **DNN** = Deep Neural Network  
> **GPT** = Generative Pre-trained Transformer  
> **GPU** = Graphics Processing Unit  
> **RF** = Random Forest  



## 1. Definitions (定义)

### Algorithm Selection (算法选择)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Six Rules for Algorithm Selection (六条军规) | 工业界选择 ML 算法的六条实战原则 (practical rules for choosing ML algorithms)：不追 SOTA、从简入手、看学习曲线、评权衡、查假设、用速查表 | 先 Logistic Regression → XGBoost → DNN 逐步升级 |
| SOTA (State-of-the-Art) | 学术基准上的最佳模型 (best model on academic benchmarks)，但不一定适合你的数据、成本高、延迟大 | GPT-4 在 ImageNet 最强，但你的 10MB 表格数据用不着 |
| Model Assumptions (模型假设) | 每个算法隐含的数学假设 (implicit mathematical assumptions)，违反假设→模型静默失败且不报错 | 线性回归假设正态性，朴素贝叶斯假设条件独立 |
| Learning Curve (学习曲线) | 在不同数据量下评估模型性能随训练的变化 (performance vs training samples/epochs)，用于判断过拟合/欠拟合 | 训练误差低但验证误差高 → 过拟合 |

### Distributed Training (分布式训练)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Gradient Checkpointing (梯度检查点) | 前向传播时只保存 √N 个检查点而非所有中间激活值，反向传播时重新计算 (trade 20% compute for 10x memory)，单机内存优化技巧 | 100 层网络只存 10 个检查点 |
| Data Parallelism (数据并行) | 训练数据分片到多台机器，每台持有完整模型副本，各自计算梯度后汇总 (split data, replicate model) | 8 个 GPU 各跑 1/8 的 batch，最后 AllReduce 梯度 |
| Model Parallelism (模型并行) | 模型太大放不下单机，将不同层放在不同机器上 (split model across machines) | 大模型的前 20 层在 GPU 0，后 20 层在 GPU 1 |
| Pipeline Parallelism (流水线并行) | 模型并行 + 微批次交错执行 (model parallel + micro-batch interleaving)，消除机器间的空闲等待"气泡" | Llama 2 70B 训练使用的策略 |
| Straggler Problem (落后者问题) | 同步模式下最慢的机器拖慢全局的问题 (slowest worker blocks all) | 8 台 GPU 中 1 台有硬件故障，其余 7 台空等 |
| Gradient Staleness (梯度过时) | 异步模式下旧梯度更新新权重的问题 (outdated gradient updating newest weights) | Worker A 用 5 步前的旧模型计算的梯度去更新当前模型 |
| DDP (分布式数据并行) | PyTorch DistributedDataParallel，每个 Worker 持有完整模型副本，All-Reduce 汇总梯度 | 模型 < 单卡显存 → 用 DDP |
| FSDP (全分片数据并行) | PyTorch FullyShardedDataParallel，参数/优化器/梯度在 GPU 间分片存储 (shard parameters across GPUs)，极高内存效率 | 模型 > 单卡显存 → 用 FSDP |

### AutoML (自动机器学习)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Soft AutoML (软 AutoML) | 自动化超参数调优 (automated hyperparameter tuning)：Grid Search / Random Search / Bayesian Optimization | 自动搜索学习率、BatchSize、层数的最优组合 |
| Hard AutoML / NAS (硬 AutoML / 神经架构搜索) | 自动设计神经网络架构 (automated network architecture design)，包含搜索空间、搜索策略、性能估计三大组件 | NASNet 在 ImageNet 上击败人工设计的模型 |
| Grid Search (网格搜索) | 穷举所有超参数组合 (exhaustive search over all combinations)，保证最优但维度灾难 | 3 个学习率 × 3 个 batch size = 9 次试验 |
| Random Search (随机搜索) | 随机采样超参数组合 (random sampling of parameter space)，高维空间效率更高但不保证最优 | 随机尝试 20 组参数 |
| Bayesian Optimization (贝叶斯优化) | 用概率模型（代理模型）预测下一个最优采样点 (surrogate model predicts next best point)，样本效率最高 | Bayesian 用 10 次试验就找到接近最优的学习率 |
| NAS Search Space (NAS/Neural Architecture Search 搜索空间) | 定义可选的"积木块" (defines available building blocks)：3×3 Conv、Pooling、Skip Connection 等 | 卷积核大小、跳跃连接类型 |
| NAS Search Strategy (NAS/Neural Architecture Search 搜索策略) | 如何组合积木块的方法 (how to combine building blocks)，需要平衡探索 vs 利用 | RL、进化算法、可微分方法 |
| NASNet | 基于 RL 的 NAS 方法的代表成果 (RL-Based NAS)，Controller (RNN) 提出架构→训练→评估→反馈，击败人工设计模型 | ImageNet SOTA 由 NASNet 自动发现 |
| AmoebaNet | 基于进化算法的 NAS 成果 (Evolutionary NAS)，通过变异-淘汰发现人类直觉从未考虑的高性能架构 | 随机初始化种群→淘汰差的→变异好的→重复 |
| DARTS (Differentiable Architecture Search / 可微分架构搜索) | 将离散架构选择转化为连续优化问题 (differentiable NAS)，用 Supernet + 梯度下降同时优化架构权重 α 和模型参数 w，搜索效率提升 1000 倍 | 数千 GPU 小时 → 几小时 |

## 2. Comparisons (对比)

### 同步 vs 异步数据并行 (梯度汇总模式)

| Dimension (维度) | Synchronous (同步) | Asynchronous (异步) | Example (示例) |
|-----------|---|---|---------| 
| 工作方式 | 等所有 Worker 算完，统一汇总 | 不等待，谁算完谁更新 | 全班一起交作业 vs 谁写完谁交 |
| 致命问题 | **Straggler** (最慢的拖全局) | **Gradient Staleness** (旧梯度更新新权重) | 1 台慢 GPU 拖慢 7 台 vs 用 5 步前的梯度 |
| 解决方案 | 负载均衡、动态资源分配 | 参数稀疏时问题自动缓解 | — |

### DDP vs FSDP (PyTorch 分布式 API)

| Dimension (维度) | DDP | FSDP | Example (示例) |
|-----------|---|---|---------| 
| 模型存储 | 每个 Worker 持有**完整模型副本** | 参数/优化器/梯度在 GPU 间**分片** | 每人一本完整教材 vs 教材拆成章节分着拿 |
| 内存效率 | ⚠️ 冗余存储 | ✅ 极高 | — |
| 适用场景 | 模型**放得进**单卡 | 模型**放不进**单卡 | 7B 模型单卡放得下 用 DDP；70B 放不下 用 FSDP |

### 三种 NAS 方法 (RL vs 进化 vs DARTS)

| Dimension (维度) | RL-Based NAS | Evolutionary NAS | DARTS | Example (示例) |
|-----------|---|---|---|---------| 
| 搜索方式 | 中央控制器"指挥" | 群体变异-淘汰"自涌现" | 连续优化（梯度下降） | RL 有指挥官，进化靠群众，DARTS 靠数学 |
| 搜索时间 | 数千 GPU 小时 | 数千 GPU 小时 | **几小时** | DARTS 效率提升 1000 倍 |
| 代表成果 | NASNet | AmoebaNet | DARTS | — |

### 超参数搜索三方法 (Grid vs Random vs Bayesian)

| Dimension (维度) | Grid Search | Random Search | Bayesian Optimization | Example (示例) |
|-----------|---|---|---|---------| 
| 策略 | 穷举所有组合 | 随机采样 | 概率模型预测下一个最优点 | 地毯式搜索 vs 随机扔飞镖 vs 看上一个飞镖再决定 |
| 保证最优 | ✅ 是 | ❌ 否 | ⚠️ 高概率 | — |
| 高维效率 | ❌ 维度灾难 | ✅ 更高效 | ✅ 样本效率最高 | — |

## 3. Formulas (公式)

### 梯度检查点

| Formula (公式) | Description (说明) | Example (示例) |
|---------|-------------|---------|
| 内存: $O(\sqrt{N})$ 检查点，时间: $1.2×$ | 梯度检查点的核心权衡：每 $\sqrt{N}$ 个节点标记一个检查点，用 20% 额外计算换 10× 内存容量 | 100 层网络标记 10 个检查点 |

## 4. Practical / Lab (实战结论)

### 📊 Lab/Assignment Conclusions (实验/作业结论)

| Conclusion (结论) | Detail (详情) | Example (示例) |
|------------|--------|---------| 
| 实战中混合数据预测连续值首选 Random Forest / GBM | 天然支持数值+类别混合类型、无需太多预处理、可解释性好、处理大数据高效 | 大数据集回归任务 → RF/GBM 优于线性回归和 DNN |

## 5. Exam Traps (考试陷阱)

### ⚠️ Common Traps (常见陷阱)

| Trap (陷阱) | Correct Answer (正确答案) | Example (示例) |
|------|----------------|---------| 
| 直接选最新 SOTA 模型 | **不要只用 SOTA**——先问"适不适合"再问"先不先进"，SOTA 在学术基准评估，不一定适合你的数据 | BERT-Large 对 10 行 CSV 表格过于复杂 |
| 梯度检查点"既省时又省内存" | 梯度检查点是用**20% 额外计算换 10× 内存**——时间会增加，不是"免费的午餐" | 训练时间从 10h → 12h，但能装 10× 大的模型 |
| DDP 和 FSDP 可以随意互换 | DDP 适用于模型**放得进单卡**的场景；FSDP 适用于模型**放不进单卡**的超大模型 | 7B 模型用 DDP，175B 模型必须用 FSDP |
| DARTS = 一种强化学习方法 | DARTS 是**可微分方法**，把离散搜索转成连续优化问题，与 RL 完全不同；DARTS 用 Supernet + 梯度下降 | RL-NAS 有 Controller (RNN)，DARTS 没有 |
| 以为所有 NAS 方法都极其昂贵 | DARTS 将搜索时间从数千 GPU 小时降到**几小时**，使普通实验室也能用 NAS | DARTS: 几小时 vs RL-NAS: 数千 GPU 小时 |

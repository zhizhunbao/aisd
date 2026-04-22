# W3: Feature Engineering (特征工程)

> **本页缩写 (Abbreviations used)**
> **CNN** = Convolutional Neural Network  
> **IID** = Independent and Identically Distributed  
> **KNN** = K-Nearest Neighbors  
> **RF** = Random Forest  
> **SMOTE** = Synthetic Minority Over-sampling Technique  
> **SVM** = Support Vector Machine


## 1. Definitions (定义)

### Feature Engineering Core (特征工程核心概念)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Feature Engineering (特征工程) | 从原始数据中分离信号与噪声的过程 (separating Signals from Noise)，将脏数据转化为 ML 模型可用的高质量特征 | 年龄/收入/品牌名等原始数据 → 清洗/缩放/编码后的特征矩阵 |
| Feature (特征) | ML 模型的输入变量，相当于信号 (Features are Signals)，传统 ML 需要人工设计，深度学习可自动学习 | 用户年龄、购买频率、IP 地址嵌入向量 |

### Missing Values (缺失值处理)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| MCAR (完全随机缺失) | 缺失与任何变量都无关，纯随机误差 (Missing Completely at Random)，是最不严重的类型，不引入偏差 | 问卷因印刷错误漏了一题 |
| MAR (随机缺失) | 缺失与其他已观测变量有关，但与缺失值本身无关 (Missing at Random)，可用统计方法纠正 | 年轻人更不愿填收入——缺失与年龄有关，但与收入本身无关 |
| MNAR (非随机缺失) | 缺失与缺失值本身有关 (Missing Not at Random)，是最严重的类型，引入系统性偏差 | 重度抑郁者不愿回答心理健康问题——越严重越不填 |
| Deletion (删除法) | 通过删除缺失数据来处理，包括行删除和列删除 (Column/Row Deletion)，简单但可能丢失信息 | 某列 80% 缺失 → 删除整列 |
| Imputation (插补法) | 用估计值填充缺失数据 (fill missing with estimated values)，包括 Mean/Median/Mode/KNN，但可能引入偏差或数据泄漏 | 用训练集均值填充缺失的年龄字段 |

### Feature Scaling & Transformation (特征缩放与变换)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Min-Max Normalization (最小最大归一化) | 将特征缩放到 [0,1] 范围，公式 $x' = \frac{x - min(x)}{max(x) - min(x)}$，对离群值敏感 | 年龄 25-65 → 缩放到 0-1 |
| Box-Cox Transformation (Box-Cox 变换) | 将非正态分布的特征变换为近似正态分布 (transform to Normal distribution)，$x' = (x^a - 1)/a$ 当 $a≠0$；$x' = \log(x)$ 当 $a=0$ | 右偏的收入分布 → 变换后接近正态 |
| Discretization / Binning (离散化/分箱) | 将连续特征转换为离散类别 (converting continuous to discrete)，也称 Quantization，需谨慎选择边界 | 年龄 → 0-10/10-18/18-30/30-50/50-65 年龄段 |

### Encoding & Embeddings (编码与嵌入)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Embedding (嵌入) | 将类别变量映射为低维稠密向量 (numerical vector representation of categorical variable)，保留语义关系，维度可控 | "king" → [0.2, 0.8, -0.1, ...] 50 维向量 |
| Word2Vec | 通过预测上下文窗口中相邻词来学习词嵌入的方法 (predict neighboring words in context window) | 单词级嵌入，语义相近的词向量距离近 |
| GloVe | 通过全局共现矩阵分解来学习词嵌入的方法 (global co-occurrence matrix factorization) | 单词级嵌入，捕获全局统计关系 |
| Sentence Transformers (句子变换器) | 用 Transformer 编码整个句子为单一向量的嵌入方法 (Transformer encoding full sentences) | 句子/段落级嵌入 |

### Data Leakage (数据泄漏)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Data Leakage (数据泄漏) | 训练时使用了预测时不应拥有的信息 (using information not expected to be available during prediction)，导致模型指标虚高 | 模型准确率 99%+ → 先查泄漏再庆祝 |
| Feature Leakage (特征泄漏) | 某个特征是目标变量的副本或代理 (feature is duplicate/proxy of target) | 用月薪预测年薪——月薪×12=年薪 |
| Sample Leakage (样本泄漏) | 训练集和测试集之间存在重复样本 (duplicate samples between train and test) | 同一张 CT 图出现在 train 和 test |
| Non-IID Leakage (非 IID 泄漏) | 时序数据被随机拆分导致未来信息泄入过去 (splitting time series randomly) | 用周五的股价"预测"周三的价格 |

### Feature Selection & Importance (特征选择与重要性)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| SHAP (Shapley 加法解释) | 借鉴合作博弈论中的 Shapley 值，通过扰动特征并测量预测变化来公平衡量每个特征的贡献 (average marginal contribution of a feature to overall model score) | Global SHAP bar plot 显示"年收入"是最重要特征 |
| Feature Coverage (特征覆盖率) | 该特征在多大比例的数据中有值 (proportion of data having value for this feature)，覆盖率低则泛化差 | "VIP 等级"只有 5% 用户有值 → 覆盖率太低 |

## 2. Comparisons (对比)

### 传统 ML vs 深度学习 (对特征工程的依赖)

| Dimension (维度) | Traditional ML (传统 ML) | Deep Learning (深度学习) | Example (示例) |
|-----------|---|---|---------| 
| 特征来源 | 人工设计 (Manual) | 模型自动学习 (Auto-learned) | SVM 需手工特征 vs CNN 自动提取图像特征 |
| 对特征工程的依赖 | ⭐⭐⭐⭐⭐ 极度依赖 | ⭐⭐ 较少（但数据清洗仍不可少） | RF 需要大量特征工程；Transformer 只需 tokenize |

### 删除法 vs 插补法 (处理缺失值)

| Dimension (维度) | Deletion (删除法) | Imputation (插补法) | Example (示例) |
|-----------|---|---|---------| 
| 做法 | 删除含缺失值的行/列 | 用估计值填充缺失值 | 列删除整列 vs 用均值填充 |
| 优点 | 简单、不引入假数据 | 保留更多数据 | — |
| 缺点 | 数据量减少→准确性降低 | 可能引入偏差、可能导致数据泄漏 | 均值插补会压缩方差 |

### One-Hot vs Embeddings (类别编码)

| Dimension (维度) | One-Hot Encoding | Embeddings (嵌入) | Example (示例) |
|-----------|---|---|---------| 
| 维度 (Dimensionality) | 类别数 = 维度数，高基数爆炸 | 固定低维（50-300 维），不随类别数增长 | 1000 品牌 → 1000 维 vs 50 维 |
| 语义关系 | ❌ 不保留（每个类别独立） | ✅ 语义相似的向量距离近 | "苹果"和"梨"的嵌入向量相近 |
| 新值处理 | ❌ 无法处理未见过的值 | ✅ 通过语义相似性处理 | 新品牌用已有近似品牌的向量 |

### SHAP 的两种用法 (全局 vs 单次预测)

| Dimension (维度) | Global Feature Importance (全局重要性) | Single Prediction Importance (单次预测) | Example (示例) |
|-----------|---|---|---------| 
| 问题 | 哪些特征整体上对模型最重要？ | 对于这一个预测，哪些特征推高/推低了结果？ | Bar plot 排序 vs Waterfall/Force plot |
| 粒度 | 宏观统计 | 微观解释 | "年龄整体排第2" vs "这个用户年龄=65 推高了流失概率" |

## 3. Formulas (公式)

### 特征缩放公式

| Formula (公式) | Description (说明) | Example (示例) |
|---------|-------------|---------|
| $x' = \frac{x - min(x)}{max(x) - min(x)}$ | Min-Max 归一化：将特征缩放到 [0,1] 范围 | 年龄 25, min=18, max=65 → $x' = 7/47 ≈ 0.15$ |
| $x' = (x^a - 1)/a$（$a≠0$）或 $\log(x)$（$a=0$） | Box-Cox 变换：自动找最佳 $a$ 值将偏态分布"拉"成正态 | 右偏收入分布 → 取 log 后接近正态 |

## 4. Practical / Lab (实战结论)

### 📊 Lab/Assignment Conclusions (实验/作业结论)

| Conclusion (结论) | Detail (详情) | Example (示例) |
|------------|--------|---------| 
| SHAP 可同时进行全局和单次预测解释 | Google Colab 练习用 Credit Risk Score 数据集演示 SHAP 的全局 bar plot 和单次预测 waterfall plot | 发现"credit_history"在信用评分模型中全局最重要 |

## 5. Exam Traps (考试陷阱)

### ⚠️ Common Traps (常见陷阱)

| Trap (陷阱) | Correct Answer (正确答案) | Example (示例) |
|------|----------------|---------| 
| 在 train/test 拆分**之前**做插补/缩放 | 所有预处理必须在拆分**之后**做！黄金法则："**先拆分，后处理**"(Split first, process later) | 用全部数据的均值填缺失值 → 测试集信息泄入训练集 |
| 以为插补法不会有风险 | 插补可能导致 **数据泄漏** (Data Leakage)、偏差，且不同方法适用于不同缺失机制 | 用全局均值填 MNAR 型缺失 → 引入系统性偏差 |
| 以为过采样可以在拆分前做 | 过采样 (Oversampling) 必须在拆分**之后**做，否则重复样本跨越 train/test 导致样本泄漏 | 拆分前 SMOTE → test 集出现 train 集的合成近邻 |
| 以为特征越多模型越好 | 特征过多的四大危害：**过拟合 + 泄漏风险 + 内存消耗 + 推理延迟增加** | 100 个特征 vs 精选 20 个 → 后者性能可能更好 |
| SHAP 值高 = 特征一定好 | SHAP 只衡量对模型的重要性，不衡量**泛化能力**——需要同时检查特征覆盖率和分布一致性 | 训练集上 SHAP 很高的特征在新数据上覆盖率仅 5% |
| 缩放时使用全部数据的统计量 | 必须**仅用 train 的统计量**（mean/min/max）来缩放和处理数据 | 用 test + train 的 min/max 做 Min-Max → 信息泄漏 |

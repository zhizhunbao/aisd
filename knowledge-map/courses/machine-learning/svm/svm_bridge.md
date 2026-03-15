---
topic: svm
dimension: bridge
created: 2026-03-13
last_verified: 2026-03-13
source_versions:
  - "📖 Paper: Cortes & Vapnik ML 1995 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/.documents/papers/svm/cortes_vapnik_1995_svm.pdf"
  - "📖 Paper: Schölkopf & Smola 2002 Survey — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/.documents/papers/svm/scholkopf_smola_2002_kernels_survey.pdf"
  - "📚 Book: Hastie et al., ESL Ch.12 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/data/mineru_output/hastie_esl/hastie_esl/auto/hastie_esl.md"
  - "📚 Book: Bishop, PRML Ch.7 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/data/mineru_output/bishop_prml/bishop_prml/auto/bishop_prml.md"
expiry: 12m
status: current
---

# SVM 衔接与扩展

> 📖 Paper: Schölkopf & Smola, [Learning with Kernels](../../../.documents/papers/svm/scholkopf_smola_2002_kernels_survey.pdf), 2002
> 📚 Book: Hastie et al., [ESL Ch.12](../../../data/mineru_output/hastie_esl/hastie_esl/auto/hastie_esl.md)

---

## ← 上一个概念 / 下一个概念 →

| 方向 | 主题 | 关系 | 链接 |
|------|------|------|------|
| ← 前置 | 感知机 (Perceptron) | SVM 继承线性分类器框架，解决感知机解不唯一的缺陷 | — |
| ← 前置 | 逻辑回归 (Logistic Reg.) | 同为线性分类器；SVM 铰链损失 vs 逻辑损失 | — |
| ← 前置 | 优化基础 (凸 QP、KKT) | SVM 训练本质是凸二次规划，KKT 刻画支持向量 | — |
| → 后续 | 核方法 (Kernel Methods) | SVM 是核方法最重要的应用；理解 SVM 是打开 RKHS 的钥匙 | — |
| → 后续 | 高斯过程 (GP) | GP 和 SVM 共享核函数体系，GP 输出概率 | — |
| → 后续 | SVR (支持向量回归) | SVM 的回归版本，ε-不敏感损失 | [svm_code.md](svm_code.md) |
| → 后续 | DBSCAN (对比) | 同在 ML 地图中；有监督(SVM) vs 无监督(DBSCAN) | [../dbscan/dbscan_map.md](../dbscan/dbscan_map.md) |

> 📚 Book: Hastie ESL Sec.12.3.3 (SVM as RKHS function estimation)

---

## 上游依赖

| 来自主题 | 复用的概念 | 在 SVM 中如何使用 |
|----------|-----------|-----------------|
| 线性代数 | 内积 $\langle x, x' \rangle$，范数 $\|w\|$ | 间隔宽度 $2/\|w\|$；核函数 $K=\langle h(x), h(x') \rangle$ |
| 凸优化 | 拉格朗日乘子法，KKT 条件，对偶定理 | SVM 原始 → 对偶推导；KKT 识别支持向量 |
| 概率统计 | 经验风险，泛化误差界 | VC 维理论是最大化间隔的理论基础 |
| 逻辑回归 | L2 正则化，损失函数形式 | SVM = 铰链损失 + L2 正则（$\lambda = 1/C$）|
| 感知机 | 超平面，有符号距离 | SVM 继承几何框架，增加间隔最大化目标 |

> 📚 Book: Bishop PRML Ch.4 (线性分类器体系) + Ch.6 (核函数)

---

## 下游影响

| 去向主题 | SVM 提供的概念 | 在下游如何被使用 |
|----------|--------------|-----------------| 
| **核方法 (Kernel Methods)** | 核技巧：$K(x,x')=\langle h(x),h(x')\rangle$ | SVM 是核方法工程化的第一个成功案例，开创了用核做非线性学习的范式 |
| **高斯过程 (Gaussian Process)** | 正定核、RKHS 函数空间 | GP 回归/分类使用相同核函数族（RBF/Matern 等），理论框架与 SVM 高度重叠 |
| **支持向量回归 (SVR)** | ε-不敏感损失、稀疏解 | SVR 直接继承 SVM 的对偶推导和稀疏性，应用于连续值预测 |
| **结构预测 (Structured SVM)** | 间隔最大化 + 约束优化 | 序列标注、解析树等结构化输出问题中，用 SVM 框架定义结构感知损失 |
| **One-Class SVM** | 支持向量 + 核技巧 | 无监督异常检测：只用正常样本训练，识别异常分布的点 |
| **深度学习 (历史影响)** | 核技巧思想 | 深度网络的每一层可视为隐式特征映射；SVM 的间隔思想影响了 Large-Margin Softmax 等损失设计 |

> 📖 Paper: Schölkopf & Smola 2002; 📚 Hastie ESL Sec.12 + Ch.5 (RKHS)

---

## 概念演变追踪

| 概念 | 在早期 SVM（1992–1995）中 | 在现代实践（2010s+）中 | 变化原因 |
|------|--------------------------|---------------------|---------|
| **求解器** | 通用 QP 求解器（慢）| libsvm SMO（快）| SMO(1998) 将大规模 SVM 变可行 |
| **核选择** | Polynomial 核为主 | RBF 核为默认起点 | RBF 有无限维 RKHS，通用性更强 |
| **参数 C** | 理论上 C → ∞（硬间隔）| 交叉验证选 C，通常 0.1~100 | 现实数据总有噪声，软间隔必须 |
| **多分类** | 一对一 (OvO) 手动实现 | sklearn 自动 OvO；LinearSVC 用 OvR | 工程封装使多分类对用户透明 |
| **并行化** | 单线程 | `n_jobs=-1`；大数据用 LinearSVC | 现代 CPU 有多核，liblinear 支持并行 |
| **概率输出** | 不输出概率 | `probability=True` + Platt scaling | 工程需求倒逼，但有准确率代价 |
| **SVM 地位** | 1990s 最强分类器 | 可解释基线 + 核方法基础 | 深度学习在大数据场景超越 SVM |

> 📚 Book: Hastie ESL Sec.12.3.8 (Discussion); 📖 Paper: Chang & Lin 2011

---

## 📚 扩展阅读

### 深入理解

| 资源 | 类型 | 为什么值得读 | 难度 |
|------|------|-------------|------|
| [Cortes & Vapnik ML 1995](../../../.documents/papers/svm/cortes_vapnik_1995_svm.pdf) | 📖 论文 | SVM 原始论文，软间隔的完整推导，必读 | ⭐⭐⭐ |
| [Hastie ESL Ch.12](../../../data/mineru_output/hastie_esl/hastie_esl/auto/hastie_esl.md) | 📚 教科书 | 最清晰的数学推导 + 核技巧 + SVR + SRM 关系 | ⭐⭐⭐ |
| [Bishop PRML Ch.7](../../../data/mineru_output/bishop_prml/bishop_prml/auto/bishop_prml.md) | 📚 教科书 | 贝叶斯视角；概率输出；与 RVM 对比 | ⭐⭐⭐ |
| [Schölkopf & Smola 2002](../../../.documents/papers/svm/scholkopf_smola_2002_kernels_survey.pdf) | 📖 论文 | 核方法完整理论；RKHS；SVM 的现代视角 | ⭐⭐⭐⭐ |

### 横向对比

| 资源 | 对比点 | 何时读 |
|------|--------|--------|
| [Hastie ESL Sec.12.3.3](../../../data/mineru_output/hastie_esl/hastie_esl/auto/hastie_esl.md) | SVM vs 逻辑回归：为什么铰链损失 = 估计符号，对数损失 = 估计概率 | 理解损失函数设计时 |
| [Hastie ESL Table 12.2](../../../data/mineru_output/hastie_esl/hastie_esl/auto/hastie_esl.md) | SVM vs BRUTO vs MARS（"orange skin"实验） | 理解核 SVM 在高维噪声下的表现 |

### 上层应用

| 资源 | 说明 | 何时读 |
|------|------|--------|
| [sklearn SVM 用户指南](https://scikit-learn.org/stable/modules/svm.html) | 官方实践指南，包含选核建议和参数调节 | 准备上手实战时 |
| [Chang & Lin LIBSVM](../../../.documents/papers/svm/chang_lin_2011_libsvm.pdf) | libsvm 内部实现，SMO 变体，多类策略 | 需要理解 sklearn SVC 底层行为时 |

> 📖 Paper: Schölkopf & Smola 2002; 📚 Hastie ESL Ch.12

---

## 与工作区已有知识库的关联

| 类别 | 数量 | 代表 | 学习点 |
|------|------|------|--------|
| 无监督聚类 | 1 | [DBSCAN 知识地图](../dbscan/dbscan_map.md) | 有监督(SVM 最大间隔) vs 无监督(DBSCAN 密度传播)的对比；两者都以"支持数据点"定义边界 |
| ML 知识地图目录 | — | [ml/README.md](../README.md) | 查看同层级已有主题，规划下一个 |

---
topic: kmeans
dimension: bridge
created: 2026-03-13
last_verified: 2026-03-13
source_versions:
  - "📚 Book: Murphy K.P., PML1 Ch.21 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/murphy_pml1.pdf"
  - "📚 Book: Hastie T. et al., ESL Ch.13-14 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/hastie_esl.pdf"
  - "📖 Paper: Arthur & Vassilvitskii 2007 SODA — https://dl.acm.org/doi/10.5555/1283383.1283494"
expiry: 12m
status: current
---

# K-Means 衔接与扩展

> 📚 Book: Murphy K.P., [《PML1》](../../../textbooks/murphy_pml1.pdf), Ch.21 Clustering
> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.13-14

---


## ← 上一个概念 / 下一个概念 →

| 方向 | 主题 | 关系 | 链接 |
|------|------|------|------| 
| ← 前置 | 欧氏距离 / 距离度量 | K-Means 的核心度量单元 | — |
| ← 前置 | 向量均值 / 线性代数 | M 步取质心均值的基础 | — |
| ← 前置 | 优化基础（坐标下降） | Lloyd 算法是坐标下降的实例 | — |
| → 后续 | K-Means++ | K-Means 的改进初始化版本 | — |
| → 后续 | GMM + EM | K-Means 的概率推广（软分配） | — |
| → 后续 | DBSCAN | 密度聚类，不需 K，处理非球形 | [dbscan_bridge.md](../dbscan/dbscan_bridge.md) |
| → 后续 | 谱聚类 Spectral | 图拉普拉斯，处理任意形状 | — |
| → 后续 | 向量量化 VQ | K-Means 的工程应用（图像压缩） | — |

> 📚 Murphy §21.1 聚类方法概览; Hastie §13.2

---


## 上游依赖

| 来自主题 | 复用的概念 | 在本主题中如何使用 |
|----------|-----------|-------------------| 
| 线性代数 | 向量均值计算 | M 步：计算簇内均值重置质心 |
| 距离度量 | 欧氏距离 $\|\cdot\|_2^2$ | E 步：判断点属于哪个最近质心 |
| 优化理论 | 坐标下降 | Lloyd 算法的收敛性证明框架 |
| 概率论 | 期望（均值）最小化均方误差 | M 步取均值的数学依据 |
| 数据预处理 | 标准化（StandardScaler） | K-Means 必须先标准化才有意义 |

> 📚 Murphy §7 Linear Algebra; §8 Optimization

---


## 下游影响

| 去向主题 | 本主题提供的概念 | 在下游如何被使用 |
|----------|-----------------|-----------------| 
| GMM + EM | 硬分配 → 软分配的思路 | GMM 是 K-Means 的概率推广，E 步变为软 responsibility |
| K-Medoids | WCSS 最小化框架 | K-Medoids 改变了"质心是什么"，用真实数据点代替均值 |
| 层次聚类 HAC | 距离矩阵的聚类概念 | HAC 用相同的距离概念，但用树结构组织 |
| 向量量化 VQ | K 个代表点压缩数据 | 图像压缩：用 K-Means 找颜色 codebook |
| RAG / 索引系统 | 向量空间的语义聚簇 | 对 embedding 做 K-Means，加速 KNN 搜索（如 FAISS） |
| MDA（混合判别分析） | 类内 K-Means 初始化 | ESL §12.7：MDA 用 K-Means 初始化每类的子类中心 |

> 📚 Hastie §12.7 MDA, §13.2.3; Murphy §21.4

---


## 概念演变追踪

| 概念 | 在原版 Lloyd 1957 中 | 在现代 K-Means 中 | 变化 |
|------|-------------|-------------|------| 
| 质心 | "代表点"（量化电平） | 特征空间的均值向量 | 从 1D 信号推广到 D 维任意特征空间 |
| 收敛条件 | 量化误差不再减少 | WCSS 不再下降/质心不再移动 | 等价，更一般化 |
| 初始化 | 未明确指定（实践中随机） | K-Means++（2007）加权概率选点 | 有理论保障的系统化改进 |
| 适用规模 | 1D/低维信号（数百个量化级别） | 高维数据（百万级 N，千维 D） | Mini-Batch 扩展，GPU 加速 |

> 📖 Lloyd 1982; Arthur & Vassilvitskii 2007

---


## 📚 扩展阅读

### 深入理解

| 资源 | 类型 | 为什么值得读 | 难度 |
|------|------|-------------|------| 
| [Lloyd 1982 IEEE](https://ieeexplore.ieee.org/document/1056489) | 📖 论文 | K-Means 算法的原始证明，非常清晰 | ⭐⭐⭐ |
| [Arthur & Vassilvitskii 2007 SODA](https://dl.acm.org/doi/10.5555/1283383.1283494) | 📖 论文 | K-Means++ 的理论推导，读懂后对"好初始化"有直觉 | ⭐⭐⭐⭐ |
| PML1 Ch.21 §21.3 | 📚 教科书 | 从概率视角统一理解 K-Means, GMM, 层次聚类 | ⭐⭐ |
| ESL Ch.13-14 | 📚 教科书 | K-Means 与 LVQ、GMM 的横向对比，非常好的视角 | ⭐⭐⭐ |

### 横向对比

| 资源 | 对比点 | 何时读 |
|------|--------|--------| 
| [DBSCAN 知识地图](../dbscan/dbscan_map.md) | DBSCAN vs K-Means：密度 vs 距离，无 K vs 预设 K | 数据有噪声、非球形时 |
| [sklearn 聚类比较](https://scikit-learn.org/stable/modules/clustering.html) | 各聚类算法适用场景完整对比表 | 选算法前必看 |

### 上层应用

| 资源 | 说明 | 何时读 |
|------|------|--------| 
| [FAISS](https://github.com/facebookresearch/faiss) | K-Means 用于向量索引（Product Quantization） | 做 RAG 或大规模 embedding 搜索时 |
| [scikit-learn 图像压缩示例](https://scikit-learn.org/stable/auto_examples/cluster/plot_color_quantization.html) | K-Means 向量量化压缩图像颜色 | 理解 VQ 的直觉 |

> 📚 Murphy §21; Hastie §13-14

---


## 与工作区已有知识库的关联

| 类别 | 数量 | 代表 | 学习点 |
|------|------|------|--------| 
| 聚类算法 | 1 | [DBSCAN](../dbscan/dbscan_map.md) | DBSCAN 解决了 K-Means 无法处理任意形状簇的问题 |
| 监督学习分类 | 1 | [SVM](../svm/svm_map.md) | 对比监督 vs 无监督：SVM 需要标签，K-Means 不需要 |
| 深度学习 | 多个 | [CNN](../../deep-learning/cnn/cnn_map.md) | K-Means 可用于 CNN 特征的聚类/量化 |

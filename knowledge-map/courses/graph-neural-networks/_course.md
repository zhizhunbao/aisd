# 图神经网络 Graph Neural Networks

> 名词总表 · 来源：Hamilton《Graph Representation Learning》· Stanford CS224W (Jure Leskovec) · 原始论文
>
> 级别：研究生 Master · 角色：ML 工程师

---

### 图基础 Graph Fundamentals

| 名词 | 英文 |
|------|------|
| 图 | Graph G = (V, E) |
| 节点 / 顶点 | Node / Vertex |
| 边 | Edge |
| 有向图 | Directed Graph |
| 无向图 | Undirected Graph |
| 加权图 | Weighted Graph |
| 二部图 | Bipartite Graph |
| 邻接矩阵 | Adjacency Matrix A |
| 度矩阵 | Degree Matrix D |
| 拉普拉斯矩阵 | Laplacian Matrix L = D - A |
| 归一化拉普拉斯 | Normalized Laplacian |
| 入度 / 出度 | In-Degree / Out-Degree |
| 子图 | Subgraph |
| 连通分量 | Connected Component |

---

### 图的传统特征 Traditional Graph Features

| 名词 | 英文 |
|------|------|
| 节点度 | Node Degree |
| 聚类系数 | Clustering Coefficient |
| 中心性 | Centrality (Degree / Betweenness / Closeness) |
| PageRank | PageRank |
| 社区检测 | Community Detection |
| 图核 | Graph Kernel |
| Weisfeiler-Lehman 核 | WL Kernel |
| 随机游走 | Random Walk |
| 图同构 | Graph Isomorphism |
| 小世界网络 | Small-World Network |
| 无标度网络 | Scale-Free Network |
| 幂律分布 | Power-Law Distribution |

---

### 节点嵌入 Node Embedding

| 名词 | 英文 |
|------|------|
| 图表示学习 | Graph Representation Learning |
| 节点嵌入 | Node Embedding |
| DeepWalk | DeepWalk |
| Node2Vec | Node2Vec |
| LINE | Large-scale Information Network Embedding |
| 编码器-解码器框架 | Encoder-Decoder Framework |
| 相似度函数 | Similarity Function |
| 随机游走嵌入 | Random Walk Embedding |
| 矩阵分解方法 | Matrix Factorization Methods |
| 转导式学习 | Transductive Learning |
| 归纳式学习 | Inductive Learning |

---

### 消息传递与 GNN Message Passing & GNN

| 名词 | 英文 |
|------|------|
| 消息传递神经网络 | MPNN (Message Passing Neural Network) |
| 聚合 | Aggregation |
| 更新 | Update |
| 邻域聚合 | Neighborhood Aggregation |
| 图卷积网络 | GCN (Graph Convolutional Network) |
| 图注意力网络 | GAT (Graph Attention Network) |
| GraphSAGE | GraphSAGE (Sample and Aggregate) |
| GIN | Graph Isomorphism Network |
| 谱图卷积 | Spectral Graph Convolution |
| 空域图卷积 | Spatial Graph Convolution |
| 图傅里叶变换 | Graph Fourier Transform |
| 切比雪夫滤波器 | Chebyshev Filter (ChebNet) |
| 过平滑 | Over-Smoothing |
| 过压缩 | Over-Squashing |
| 跳跃连接 | Skip Connection |

---

### GNN 变体 GNN Variants

| 名词 | 英文 |
|------|------|
| 图 Transformer | Graph Transformer |
| 异构图神经网络 | Heterogeneous GNN (HetGNN) |
| 关系图卷积 | R-GCN (Relational GCN) |
| 时空图网络 | Spatio-Temporal GNN (ST-GNN) |
| 超图神经网络 | Hypergraph Neural Network |
| 动态图网络 | Dynamic Graph Network |
| 有向图网络 | Directed GNN |
| 等变图网络 | Equivariant GNN |
| 3D 点云网络 | PointNet / Point Cloud GNN |

---

### 图级任务 Graph-Level Tasks

| 名词 | 英文 |
|------|------|
| 图分类 | Graph Classification |
| 图回归 | Graph Regression |
| 图池化 | Graph Pooling |
| 层次池化 | Hierarchical Pooling |
| DiffPool | Differentiable Pooling |
| Set2Set | Set2Set |
| 全局读出 | Global Readout |
| 求和池化 | Sum Pooling |
| 平均池化 | Mean Pooling |
| 注意力池化 | Attention Pooling |

---

### 节点 / 边级任务 Node / Edge Level Tasks

| 名词 | 英文 |
|------|------|
| 节点分类 | Node Classification |
| 半监督节点分类 | Semi-Supervised Node Classification |
| 链接预测 | Link Prediction |
| 边分类 | Edge Classification |
| 节点聚类 | Node Clustering |
| 社区检测 | Community Detection |
| 影响力最大化 | Influence Maximization |

---

### 知识图谱 Knowledge Graphs

| 名词 | 英文 |
|------|------|
| 知识图谱 | Knowledge Graph (KG) |
| 三元组 | Triple (head, relation, tail) |
| 知识图谱嵌入 | KG Embedding |
| TransE | TransE |
| TransR | TransR |
| DistMult | DistMult |
| ComplEx | ComplEx |
| RotatE | RotatE |
| 知识图谱补全 | KG Completion |
| 关系推理 | Relational Reasoning |
| 多跳推理 | Multi-Hop Reasoning |

---

### 图生成模型 Graph Generative Models

| 名词 | 英文 |
|------|------|
| 图生成 | Graph Generation |
| 自回归图生成 | Autoregressive Graph Generation |
| GraphRNN | GraphRNN |
| 变分图自编码器 | VGAE (Variational Graph Auto-Encoder) |
| 图扩散模型 | Graph Diffusion Model |
| 分子生成 | Molecular Generation |
| 分子图 | Molecular Graph |
| SMILES | SMILES Representation |

---

### 应用 Applications

| 名词 | 英文 |
|------|------|
| 推荐系统 | Recommender Systems |
| 药物发现 | Drug Discovery |
| 蛋白质结构预测 | Protein Structure Prediction |
| 交通网络 | Traffic Networks |
| 社交网络分析 | Social Network Analysis |
| 欺诈检测 | Fraud Detection |
| 组合优化 | Combinatorial Optimization |
| 代码分析 | Code Analysis (AST Graphs) |

---

### 工具 Tools

| 名词 | 英文 |
|------|------|
| PyG | PyTorch Geometric |
| DGL | Deep Graph Library |
| NetworkX | NetworkX |
| OGB | Open Graph Benchmark |
| GraphGym | GraphGym |
| torch_geometric.nn | PyG Neural Network Modules |

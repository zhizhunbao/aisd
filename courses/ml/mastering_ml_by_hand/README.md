# 🧠 Mastering Machine Learning: The Complete Hand-Calculation Codex (算法大宗师：手算究极图鉴)

> **"If you can't compute it by hand with a tiny dataset, you don't truly understand the algorithm."**
>
> 这是一份面向顶级AI工程师的终极修炼地图。这里不仅包含了日常听说的 17 个模型，而是收录了横跨**传统统计学、无监督学习、推荐系统、深度学习、生成式AI（GenAI）以及强化学习**的 **30 个** 核心经典算法。
>
> **终极闭环要求**：手推公式极限极简版 $\rightarrow$ 运行 `handson-ml3` 验证 $\rightarrow$ 扒开 `sklearn/pytorch` 底层源码。

---

## 📈 第一阶段：监督学习基石 (回归与线性分类)

### 1. 最小二乘法与多元线性回归 (Linear Regression & OLS)

- **手算挑战**：3 个点，用正规方程 $W = (X^T X)^{-1} X^T Y$ 算斜率和截距。
- **源码映射**：`sklearn/linear_model/_base.py` （底层调用 Scipy 的 LAPACK 库求解）。

### 2. 带有 L1/L2 正则化的回归 (Ridge, Lasso & Elastic Net)

- **手算挑战**：给损失函数加惩罚。手算带有 $\lambda W^2$ 的偏导数。
- **源码映射**：`sklearn/linear_model/_ridge.py` & `_coordinate_descent.py` (Lasso坐标下降法)。

### 3. 逻辑回归与梯度下降 (Binary Logistic Regression)

- **手算挑战**：2 个特征的数据。线性加权 $\rightarrow$ Sigmoid $\rightarrow$ Log Loss $\rightarrow$ 算出偏导 $\rightarrow$ 手走 1 轮权重更新。
- **源码映射**：`sklearn/linear_model/_logistic.py`。

### 4. Softmax 多分类回归 (Multinomial Logistic Regression)

- **手算挑战**：3 个类别，用 Softmax 公式算概率，确保输出和为 1，计算交叉熵（Cross-Entropy）。

### 5. 牛顿法优化 (Newton's Method for Optimization)

- **手算挑战**：一维函数 $f(x)=x^2-2$，手算一阶导和二阶导（海森矩阵Hessian），走一步牛顿迭代 $x_{n+1} = x_n - f'(x)/f''(x)$。对比它和梯度下降的区别。

---

## 📐 第二阶段：古典概率、空间与邻近分类

### 6. 朴素贝叶斯分类器 (Naive Bayes Classifier)

- **手算挑战**：极简连乘概率比较，带入 Gaussian PDF 算概率密度。**（完成过！）**
- **源码映射**：`sklearn/naive_bayes.py`。

### 7. K-近邻算法 (KNN classification & regression)

- **手算挑战**：二维平面算 5 个点到目标点的欧氏与曼哈顿距离，选取 $K=3$ 投票。
- **源码映射**：`sklearn/neighbors/_classification.py` (底层核心在 KD-Tree 算法中)。

### 8. 支持向量机 (SVM - Hard & Soft Margin, Kernel Trick)

- **手算挑战**：3 个点，列出拉格朗日乘子方程。手动代入多项式核函数 $K(x,y)=(x \cdot y + 1)^2$ 将点升维。
- **源码映射**：`sklearn/svm/_classes.py` (封装底层 C++ 的 libsvm)。

### 9. 决策树 (Decision Tree - ID3 / CART)

- **手算挑战**：5 行数据。手算每个阈值劈开后的基尼系数 (Gini) 和信息熵 (Entropy)，找最佳那一刀。
- **源码映射**：`sklearn/tree/_tree.pyx` (极速 Cython 分裂算法)。

---

## 🤝 第三阶段：集成学习 (Ensemble / 工业界大杀器)

### 10. 随机森林 (Random Forest / Bagging)

- **手算挑战**：Bootstrap 抽样 3 次构建只含部分特征的极小树，三个臭皮匠投票。
- **源码映射**：`sklearn/ensemble/_forest.py`。

### 11. AdaBoost (Adaptive Boosting)

- **手算挑战**：训练一个单层节点树 (Stump) $\rightarrow$ 算错误率 $\rightarrow$ 根据公式放大错题的权重。
- **源码映射**：`sklearn/ensemble/_weight_boosting.py`。

### 12. 梯度提升树 (Gradient Boosting Decision Tree, GBDT)

- **手算挑战**：极简回归。第一棵树预测 $\rightarrow$ 算真值减预测值的残差 $\rightarrow$ 第二棵树暴力拟合这堆残差。

### 13. XGBoost 的二阶泰勒展开 (eXtreme Gradient Boosting)

- **手算挑战**：打败大厂 90% 面试者！手写损失函数在上一轮预测值处的二阶泰勒展开，并以此求出下一棵树分裂增益。
- **源码映射**：去 Github 看纯 C++ 的 `dmlc/xgboost` 库实现。

---

## 🔍 第四阶段：无监督学习与聚类 (Unsupervised & Clustering)

### 14. K-Means 聚类

- **手算挑战**：一维轴挑 2 个质心，算距离分类 $\rightarrow$ 重新计算均值作新质心 $\rightarrow$ 循环 1 次。

### 15. 层次聚类 (Hierarchical Clustering / Agglomerative)

- **手算挑战**：平面上 4 个点。每次找距离最近的两个点绑成一个新“团”，更新距离矩阵，画出树状图(Dendrogram)。

### 16. DBSCAN (基于密度的聚类)

- **手算挑战**：设定 $Epsilon=1$, $MinPts=2$。计算核心点坐标并手动完成点集的扩散蔓延（不用设定 K 值就能聚类的魔法）。

### 17. 高斯混合模型与 EM 算法 (GMM & Expectation-Maximization)

- **手算挑战**：假设数据由 2 个高斯分布混合。**E步**：手算每个点是由 1类 或 2类生成的概率；**M步**：反过来根据概率重新算这俩高斯分布的 $\mu$ 和 $\sigma$。

### 18. 主成分分析 (Principal Component Analysis, PCA)

- **手算挑战**：数据中心化 $\rightarrow$ 计算 $2\times2$ 协方差矩阵 $\rightarrow$ 手解一元二次方程求特征值 $\rightarrow$ 求特征向量并投影。

### 19. FP-Growth / Apriori (关联规则推荐)

- **手算挑战**：给 4 张超市小票（比如尿布和啤酒），设定最小支持度，手算支持度和置信概率。

---

## 🕰️ 第五阶段：图与时序动态系统

### 20. 隐马尔可夫模型与维特比算法 (HMM & Viterbi)

- **手算挑战**：2状态 3观测。给一条序列，用维特比动态规划网格手算所有乘积路径概率，找那条最大的全路线（语音识别与 NLP 词性标注的始祖）。

### 21. 卡尔曼滤波 (Kalman Filter)

- **手算挑战**：用雷达乱飘的观测值和物理运动定律（预测值），手算“卡尔曼增益（Kalman Gain）”，通过权重求出最接近真实的当前位置。

### 22. PageRank (Google 搜索引擎核心原理)

- **手算挑战**：画互相链接的 3 个网页，写出概率转移矩阵，手算一轮随机游走到达每个网页的概率。

---

## 🧠 第六阶段：深度学习骨骼与引擎 (Deep Learning Engines)

### 23. 最经典的反向传播 (Backpropagation in MLP) 👑

- **手算挑战**：输入 2 $\rightarrow$ 隐藏 2 $\rightarrow$ 输出 1。一次前向传播后，手推交叉熵的梯度偏导，手动算 $\delta$ 然后回推所有权重 $W$ 的更新（链式法则封神之战）。
- **源码映射**：研读 `pytorch/c10` (Autograd 自动求导计算图)。

### 24. 词向量 Word2Vec (Skip-gram with Negative Sampling)

- **手算挑战**：输入中心词的 One-hot 向量，手算出经过隐藏层矩阵和 Softmax 之后预测周围关联词的概率输出。
- **源码映射**：早期 `gensim` 库的实现，体会什么是“分布式表示”。

### 25. 卷积计算与感受野 (CNN Convolution, Padding, Pooling)

- **手算挑战**：$4\times4$ 矩阵，扫 $2\times2$ 卷积核和 MaxPooling。手算 $(W-F+2P)/S+1$ 确定输出的图片尺寸。
- **源码映射**：`keras/layers/convolutional` 或底层 `im2col` 加速算子。

### 26. RNN 时间步展开与随时间反向传播 (BPTT)

- **手算挑战**：序列长度仅为 2。手算 $h_t = \tanh(Wxh \cdot x_t + Whh \cdot h_{t-1})$，并尝试展开时间轴往回求一次偏导。

### 27. LSTM 与 GRU 的细胞门控 (Long Short-Term Memory)

- **手算挑战**：代入输入 $x_t$ 和上一刻记忆 $h_{t-1}$，手算 LSTM 中的遗忘门($f$)、输入门($i$)、输出门($o$)和细胞状态 $C_t$ 的开闭。

---

## 🤖 第七阶段：生成式 AI 与大模型心脏 (Generative AI & LLMs)

### 28. 生成对抗网络 (GAN - Generative Adversarial Networks)

- **手算挑战**：手算极其简化的极大极小博弈损失 (Minimax Game)。G(生成器) 想让输出结果尽量靠近 1，D(判别器) 拼命算出它是假的所以靠近 0。手算两端的下降梯度互相对抗。

### 29. 扩散模型原理核心 (Diffusion Models)

- **手算挑战**：Forward 阶段：用马尔可夫链公式 $q(x_t|x_{t-1})$ 给一张像素图连续加 3 次高斯噪音并抽出最终公式；Reverse：用贝叶斯倒推降噪逻辑。

### 30. 自注意力与 Transformer (Self-Attention in Transformers) 🌟

- **手算挑战**：输入 2 个词向量。"Query, Key, Value" 三个基底矩阵相乘，计算 $Q \times K^T$，除以 $\sqrt{d_k}$ 后过 Softmax，最后加权到 $V$。体验 ChatGPT 大脑深处“词与词如何相匹配”的矩阵真理！
- **源码映射**：`pytorch/torch/nn/modules/activation.py` 下的 `MultiheadAttention` 实现。

---

## 🎮 第八阶段：强化学习巅峰 (Reinforcement Learning)

### 31. Q-Learning 与 MDP (Markov Decision Process)

- **手算挑战**：$2 \times 2$ 迷你迷宫，有陷阱有宝藏。用**贝尔曼方程 (Bellman Equation)** 计算当前奖励和未来折扣奖励，手动更新一次 Q-Table 中的价值。

### 32. 策略梯度定理 (Policy Gradient / REINFORCE)

- **手算挑战**：在玩一个非确定性小游戏里，因为某个动作得到了正反馈，手算出网络是如何沿“提高该动作被选取的概率”方向更新梯度的。

---

### 🚀 使用指南 (How to Become a Grandmaster)

这是机器学习领域最核心的 32 把“数学钥匙”。在平时跑完各种高级调包任务后，每周挑一个抽出 1 个小时，不写任何代码，用 A4 纸、笔和计算器。一旦你在纸上算出那个正确的导数和权重更新...
**你对算法的理解深度，将直接秒杀 95% 的“调包侠”。**

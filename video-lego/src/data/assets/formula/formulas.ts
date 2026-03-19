// ═══════════════════════════════════════════════════════════
// 公式素材数据 — 按数学学科分类，科目内按知识依赖排序
// Formula data — sorted by prerequisite order within each discipline
//
// 排序原则: 前面的公式是后面公式的基础
//   calculus:      导数 → 偏导 → 梯度 → Jacobian → Hessian → 链式法则 → 激活函数(Sigmoid/Tanh/ReLU/Softplus/LeakyReLU)
//   linear:        L1范数 → L2范数 → 点积 → 矩阵乘 → 转置 → 行列式 → 特征值 → SVD → 正规方程 → 距离
//   probability:   联合概率 → 条件概率 → 全概率 → 贝叶斯 → 期望 → 高斯 → 多元高斯 → MLE → Softmax
//   statistics:    方差 → 协方差 → Z-Score → MAE → MSE → 闵可夫斯基
//   optimization:  梯度下降 → 动量 → 学习率衰减 → RMSProp → Adam → Xavier初始化 → BatchNorm
//   information:   熵 → 交叉熵 → KL散度
//   deep_learning: 1D卷积 → 2D卷积 → Attention
// ═══════════════════════════════════════════════════════════

import type { Asset } from '@/lib/asset-types'

function fml(id: string, name: string, subCategory: string, tags: string[],
  latex: string, color: string, intuition: string,
  source: { title: string; author: string; year: number; chapter: string; cite: string }
): Asset {
  return {
    id, name, category: 'formula', subCategory, atomType: 'formula',
    tags, knowledgeDimensions: ['math'],
    sources: [{ type: 'textbook', ...source }],
    createdAt: '2026-03-18', compatibleBlocks: ['FormulaBlock'],
    content: {
      category: 'text_overlay',
      data: { overlayType: 'formula', text: name, latex, color, intuition },
    },
  }
}

const CALC = { title: 'Calculus', author: 'Stewart', year: 2015, chapter: 'Ch.2', cite: 'Stewart §2' }
const LA   = { title: 'Linear Algebra', author: 'Strang', year: 2016, chapter: 'Ch.1', cite: 'Strang §1' }
const ESL  = { title: 'ESL', author: 'Hastie et al.', year: 2009, chapter: 'Ch.2', cite: 'ESL §2.3' }
const DL   = { title: 'Deep Learning', author: 'Goodfellow', year: 2016, chapter: 'Ch.6', cite: 'Goodfellow Ch.6' }
const PML  = { title: 'PML1', author: 'Murphy', year: 2022, chapter: 'Ch.2', cite: 'Murphy §2.5' }
const PRML = { title: 'PRML', author: 'Bishop', year: 2006, chapter: 'Ch.1', cite: 'Bishop §1.2' }
const CVX  = { title: 'Convex Optimization', author: 'Boyd', year: 2004, chapter: 'Ch.9', cite: 'Boyd §9' }
const MML  = { title: 'Mathematics for ML', author: 'Deisenroth', year: 2020, chapter: 'Ch.5', cite: 'MML §5.3' }
const ATT  = { title: 'Attention Is All You Need', author: 'Vaswani et al.', year: 2017, chapter: '§3.2', cite: 'Vaswani §3.2' }

export const formulas: Asset[] = [
  // ═══════════════════════════════════════════════════════════
  // 微积分 Calculus — 导数 → 偏导 → 梯度 → Jacobian → Hessian → 链式法则 → 激活函数
  // ═══════════════════════════════════════════════════════════
  fml('fml-derivative', '导数', 'calculus',
    ['切线斜率', '变化率', '所有优化的基础'],
    String.raw`f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}`,
    '#e74c3c', '函数在某点的变化率', CALC),

  fml('fml-partial', '偏导数', 'calculus',
    ['梯度向量', '多变量优化', '反向传播'],
    String.raw`\frac{\partial f}{\partial x_i} = \lim_{h \to 0} \frac{f(\ldots, x_i+h, \ldots) - f(\ldots, x_i, \ldots)}{h}`,
    '#3498db', '固定其他变量，对一个变量求导', CALC),

  fml('fml-gradient', '梯度', 'calculus',
    ['梯度下降', '反向传播', '上升最快方向'],
    String.raw`\nabla f = \left[\frac{\partial f}{\partial x_1}, \frac{\partial f}{\partial x_2}, \ldots, \frac{\partial f}{\partial x_n}\right]`,
    '#2ecc71', '所有偏导数组成的向量', DL),

  // ▼ NEW: Jacobian — 多维输出函数的导数矩阵
  fml('fml-jacobian', 'Jacobian 矩阵', 'calculus',
    ['反向传播', '多输出导数', '变量替换', '生成模型'],
    String.raw`J = \begin{bmatrix} \frac{\partial f_1}{\partial x_1} & \cdots & \frac{\partial f_1}{\partial x_n} \\ \vdots & \ddots & \vdots \\ \frac{\partial f_m}{\partial x_1} & \cdots & \frac{\partial f_m}{\partial x_n} \end{bmatrix}`,
    '#e67e22', '向量函数对向量变量的一阶导数矩阵', MML),

  // ▼ NEW: Hessian — 二阶导数矩阵
  fml('fml-hessian', 'Hessian 矩阵', 'calculus',
    ['Newton法', '优化分析', '曲率', '鞍点检测'],
    String.raw`H_{ij} = \frac{\partial^2 f}{\partial x_i \partial x_j}`,
    '#8e44ad', '二阶偏导组成的矩阵，描述曲率', { ...DL, chapter: 'Ch.4', cite: 'Goodfellow §4.3' }),

  fml('fml-chain-rule', '链式法则', 'calculus',
    ['反向传播', '梯度计算', '所有DL核心', '梯度消失'],
    String.raw`\frac{\partial L}{\partial x} = \frac{\partial L}{\partial y} \cdot \frac{\partial y}{\partial x}`,
    '#9b59b6', '复合函数求导 = 逐层相乘', DL),

  fml('fml-sigmoid', 'Sigmoid', 'calculus',
    ['逻辑回归', '二分类', 'LSTM门控', 'GAN'],
    String.raw`\sigma(x) = \frac{1}{1 + e^{-x}}`,
    '#3498db', '任意实数→(0,1)', DL),

  fml('fml-tanh', 'Tanh', 'calculus',
    ['RNN', 'LSTM', 'BatchNorm', '归一化'],
    String.raw`\tanh(x) = \frac{e^x - e^{-x}}{e^x + e^{-x}}`,
    '#f39c12', '输出在(-1,1)之间', DL),

  fml('fml-relu', 'ReLU', 'calculus',
    ['CNN', 'ResNet', 'DNN', '深度学习标配'],
    String.raw`\text{ReLU}(x) = \max(0, x)`,
    '#e74c3c', '负数归零，正数不变', DL),

  // ▼ NEW: Softplus — ReLU 的平滑版
  fml('fml-softplus', 'Softplus', 'calculus',
    ['ReLU平滑版', '正数保证', '方差参数化', 'VAE'],
    String.raw`\zeta(x) = \log(1 + e^x)`,
    '#27ae60', 'ReLU 的平滑近似，保证输出为正', { ...DL, chapter: '§3.10', cite: 'Goodfellow §3.10' }),

  // ▼ NEW: Leaky ReLU — 解决死亡ReLU
  fml('fml-leaky-relu', 'Leaky ReLU', 'calculus',
    ['死亡ReLU解决', 'ResNet', 'GAN', '深度网络'],
    String.raw`f(x) = \begin{cases} x & x > 0 \\ \alpha x & x \leq 0 \end{cases}`,
    '#e74c3c', '负数区域有小斜率，避免神经元死亡', { ...DL, chapter: '§6.3', cite: 'Goodfellow §6.3' }),

  // ═══════════════════════════════════════════════════════════
  // 线性代数 Linear Algebra — L1 → L2 → 点积 → 矩阵 → 行列式 → 特征值 → SVD → 正规方程 → 距离
  // ═══════════════════════════════════════════════════════════

  // ▼ NEW: L1 范数 — 稀疏正则化基础
  fml('fml-l1-norm', 'L1范数', 'linear',
    ['LASSO', '稀疏正则化', '特征选择', '压缩感知'],
    String.raw`\|\vec{x}\|_1 = \sum_{i=1}^{n} |x_i|`,
    '#27ae60', '向量各分量绝对值之和', { ...ESL, chapter: 'Ch.3', cite: 'ESL §3.4' }),

  fml('fml-l2-norm', 'L2范数', 'linear',
    ['正则化', '权重衰减', 'Ridge回归', '向量长度'],
    String.raw`\|\vec{x}\|_2 = \sqrt{\sum_{i=1}^{n} x_i^2}`,
    '#4ea8de', '向量的长度/模', LA),

  fml('fml-dot-product', '点积', 'linear',
    ['Attention', '相似度计算', '投影', '特征提取'],
    String.raw`\vec{a} \cdot \vec{b} = \sum_{i=1}^{n} a_i b_i = \|\vec{a}\|\|\vec{b}\|\cos\theta`,
    '#2ecc71', '两个向量的投影', LA),

  fml('fml-matrix-multiply', '矩阵乘法', 'linear',
    ['全连接层', 'Transformer', '线性变换', 'PCA'],
    String.raw`(AB)_{ij} = \sum_{k=1}^{n} a_{ik} b_{kj}`,
    '#e67e22', '行×列求和', LA),

  fml('fml-transpose', '矩阵转置', 'linear',
    ['反向传播', 'SVD', '协方差矩阵', '正规方程'],
    String.raw`(A^T)_{ij} = A_{ji}`,
    '#1abc9c', '行列互换', LA),

  // ▼ NEW: 行列式 — 矩阵可逆判断
  fml('fml-determinant', '行列式', 'linear',
    ['矩阵可逆', '高斯分布', '体积缩放', '特征值乘积'],
    String.raw`\det(A) = \sum_{\sigma \in S_n} \text{sgn}(\sigma) \prod_{i=1}^{n} a_{i,\sigma(i)}`,
    '#8e44ad', '矩阵是否可逆的标量指标', { ...LA, chapter: 'Ch.5', cite: 'Strang §5' }),

  fml('fml-eigenvalue', '特征值', 'linear',
    ['PCA', 'SVD', '协方差矩阵', '降维'],
    String.raw`A\vec{v} = \lambda\vec{v}`,
    '#9b59b6', '矩阵作用不改变方向的特殊向量', LA),

  // ▼ NEW: SVD — 矩阵分解核心
  fml('fml-svd', 'SVD 奇异值分解', 'linear',
    ['PCA', '降维', '推荐系统', '矩阵压缩', '伪逆'],
    String.raw`A = U \Sigma V^T`,
    '#3498db', '任意矩阵 = 旋转 × 缩放 × 旋转', { ...MML, chapter: '§4.5', cite: 'MML §4.5' }),

  // ▼ NEW: 正规方程 — 线性回归解析解
  fml('fml-normal-equation', '正规方程', 'linear',
    ['线性回归', '最小二乘', '解析解', 'OLS'],
    String.raw`\hat{\theta} = (X^T X)^{-1} X^T y`,
    '#e67e22', '线性回归的闭式最优解', { ...MML, chapter: '§9.2', cite: 'MML §9.2' }),

  fml('fml-euclidean', '欧氏距离', 'linear',
    ['L2', 'KNN', 'K-Means', 'SVM'],
    String.raw`d(x,y) = \sqrt{\sum_{i=1}^{n}(x_i - y_i)^2}`,
    '#4ea8de', '两点直线距离', ESL),

  fml('fml-manhattan', '曼哈顿距离', 'linear',
    ['L1', 'KNN', 'LASSO', '稀疏学习'],
    String.raw`d(x,y) = \sum_{i=1}^{n}|x_i - y_i|`,
    '#2ecc71', '沿网格线走的距离', ESL),

  fml('fml-cosine', '余弦相似度', 'linear',
    ['NLP', 'Word2Vec', 'TF-IDF', '推荐系统'],
    String.raw`\cos(\theta) = \frac{\vec{a} \cdot \vec{b}}{\|\vec{a}\| \|\vec{b}\|}`,
    '#e67e22', '方向是否一致', { ...PML, chapter: 'Ch.22', cite: 'Murphy Ch.22' }),

  // ═══════════════════════════════════════════════════════════
  // 概率论 Probability — 联合概率 → 条件概率 → 全概率 → 贝叶斯 → 期望 → 高斯 → 多元高斯 → MLE → Softmax
  // ═══════════════════════════════════════════════════════════

  // ▼ NEW: 联合概率 — 概率论基础
  fml('fml-joint-prob', '联合概率', 'probability',
    ['概率基础', '朴素贝叶斯', '独立性', '图模型'],
    String.raw`P(A \cap B) = P(A|B) \cdot P(B)`,
    '#27ae60', '两事件同时发生的概率', { ...PML, chapter: 'Ch.2', cite: 'Murphy §2.1' }),

  fml('fml-conditional', '条件概率', 'probability',
    ['贝叶斯基础', '分类', '马尔可夫链'],
    String.raw`P(A|B) = \frac{P(A \cap B)}{P(B)}`,
    '#1abc9c', '已知B发生，A发生的概率', PML),

  // ▼ NEW: 全概率公式 — 贝叶斯分母
  fml('fml-total-prob', '全概率公式', 'probability',
    ['贝叶斯分母', '边缘化', '概率求和', '隐变量'],
    String.raw`P(A) = \sum_{i} P(A|B_i) P(B_i)`,
    '#4ea8de', '按所有可能拆分求总概率', { ...PML, chapter: 'Ch.2', cite: 'Murphy §2.1' }),

  fml('fml-bayes', '贝叶斯定理', 'probability',
    ['朴素贝叶斯', '贝叶斯网络', '后验推断', 'MAP'],
    String.raw`P(A|B) = \frac{P(B|A) \cdot P(A)}{P(B)}`,
    '#3498db', '根据新证据更新信念', PML),

  fml('fml-expectation', '期望', 'probability',
    ['损失函数', '强化学习回报', '均值估计'],
    String.raw`E[X] = \sum_{i} x_i \cdot P(x_i)`,
    '#e67e22', '加权平均值', PML),

  fml('fml-gaussian', '高斯分布', 'probability',
    ['GMM', '贝叶斯推断', '异常检测', 'GAN'],
    String.raw`f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}`,
    '#9b59b6', '钟形曲线/正态分布', PRML),

  // ▼ NEW: 多元高斯分布 — 多维版
  fml('fml-multivariate-gaussian', '多元高斯分布', 'probability',
    ['GMM', 'VAE', '贝叶斯推断', 'PCA', '马氏距离'],
    String.raw`p(\mathbf{x}) = \frac{1}{(2\pi)^{d/2}|\Sigma|^{1/2}} \exp\!\left(-\tfrac{1}{2}(\mathbf{x}-\boldsymbol{\mu})^T \Sigma^{-1} (\mathbf{x}-\boldsymbol{\mu})\right)`,
    '#8e44ad', '多维钟形分布，协方差控制形状', { ...PRML, chapter: 'Ch.2', cite: 'PRML §2.3' }),

  // ▼ NEW: 最大似然估计 — 参数估计核心
  fml('fml-mle', '最大似然估计', 'probability',
    ['参数估计', '逻辑回归', '神经网络训练', 'EM算法'],
    String.raw`\hat{\theta}_{MLE} = \arg\max_\theta \sum_{i=1}^{n} \log p(x_i | \theta)`,
    '#e74c3c', '找使数据出现概率最大的参数', { ...DL, chapter: 'Ch.5', cite: 'Goodfellow §5.5' }),

  fml('fml-softmax', 'Softmax', 'probability',
    ['分类器', 'Transformer', 'Attention', '多分类'],
    String.raw`\sigma(z_i) = \frac{e^{z_i}}{\sum_{j=1}^{K} e^{z_j}}`,
    '#9b59b6', '分数→概率', DL),

  // ═══════════════════════════════════════════════════════════
  // 数理统计 Statistics — 方差 → 协方差 → Z-Score → MAE → MSE → 闵可夫斯基
  // ═══════════════════════════════════════════════════════════
  fml('fml-variance', '方差', 'statistics',
    ['数据离散度', 'BatchNorm', '特征缩放', '正则化'],
    String.raw`\text{Var}(X) = E[(X - \mu)^2] = \frac{1}{n}\sum_{i=1}^{n}(x_i - \bar{x})^2`,
    '#3498db', '数据偏离均值的程度', PML),

  // ▼ NEW: 协方差 — 变量间关联性
  fml('fml-covariance', '协方差', 'statistics',
    ['PCA', '多元高斯', '特征相关性', '协方差矩阵'],
    String.raw`\text{Cov}(X,Y) = E[(X - \mu_X)(Y - \mu_Y)]`,
    '#9b59b6', '两个变量一起变化的趋势', { ...MML, chapter: '§6.4', cite: 'MML §6.4' }),

  // ▼ NEW: Z-Score 标准化 — 标量版 BatchNorm
  fml('fml-zscore', 'Z-Score 标准化', 'statistics',
    ['特征缩放', 'BatchNorm基础', '标准化', '预处理'],
    String.raw`z = \frac{x - \mu}{\sigma}`,
    '#4ea8de', '数据→标准正态(均值0方差1)', ESL),

  fml('fml-mae', '平均绝对误差', 'statistics',
    ['鲁棒回归', '异常值不敏感', '时间序列'],
    String.raw`\text{MAE} = \frac{1}{n}\sum_{i=1}^{n}|y_i - \hat{y}_i|`,
    '#27ae60', '预测偏差的绝对值平均', ESL),

  fml('fml-mse', '均方误差', 'statistics',
    ['线性回归', '神经网络回归', 'AutoEncoder'],
    String.raw`\text{MSE} = \frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2`,
    '#e67e22', '预测值和真实值的平均偏差', ESL),

  fml('fml-minkowski', '闵可夫斯基距离', 'statistics',
    ['Lp范数', 'KNN', 'L1/L2通用'],
    String.raw`d(x,y) = \left(\sum_{i=1}^{n}|x_i - y_i|^p\right)^{1/p}`,
    '#1abc9c', 'L1/L2 的通用形式', ESL),

  // ═══════════════════════════════════════════════════════════
  // 优化方法 Optimization — SGD → 动量 → LR衰减 → RMSProp → Adam → Xavier → BatchNorm
  // ═══════════════════════════════════════════════════════════
  fml('fml-sgd', '梯度下降', 'optimization',
    ['所有DL模型', '线性回归', '逻辑回归', '基石'],
    String.raw`\theta_{t+1} = \theta_t - \eta \nabla_\theta L(\theta_t)`,
    '#e74c3c', '沿梯度反方向更新参数', CVX),

  fml('fml-momentum', '动量法', 'optimization',
    ['CNN训练', '加速收敛', 'ResNet', 'SGD改进'],
    String.raw`v_t = \gamma v_{t-1} + \eta \nabla L, \quad \theta_{t+1} = \theta_t - v_t`,
    '#3498db', '带惯性的梯度下降', DL),

  fml('fml-learning-rate', '学习率衰减', 'optimization',
    ['训练调参', 'Scheduler', 'Warmup', '收敛策略'],
    String.raw`\eta_t = \eta_0 \cdot \frac{1}{1 + \alpha \cdot t}`,
    '#f39c12', '逐渐减小步长', DL),

  // ▼ NEW: RMSProp — 指数加权移动平均
  fml('fml-rmsprop', 'RMSProp', 'optimization',
    ['自适应学习率', 'RNN训练', 'Adam前身', 'AdaGrad改进'],
    String.raw`r_t = \rho r_{t-1} + (1-\rho) g_t \odot g_t, \quad \Delta\theta = -\frac{\epsilon}{\sqrt{\delta + r_t}} \odot g_t`,
    '#e67e22', '用梯度平方的移动平均自适应调节步长', { ...DL, chapter: '§8.5.2', cite: 'Goodfellow §8.5.2' }),

  // ▼ NEW: Adam — 最常用优化器
  fml('fml-adam', 'Adam 优化器', 'optimization',
    ['默认优化器', 'Transformer', 'GPT', 'BERT', '自适应'],
    String.raw`m_t = \beta_1 m_{t-1} + (1-\beta_1) g_t, \quad v_t = \beta_2 v_{t-1} + (1-\beta_2) g_t^2, \quad \theta_{t+1} = \theta_t - \frac{\eta}{\sqrt{\hat{v}_t}+\epsilon} \hat{m}_t`,
    '#2ecc71', '动量 + 自适应学习率的结合体', { ...DL, chapter: '§8.5.3', cite: 'Goodfellow §8.5.3' }),

  // ▼ NEW: Xavier/Glorot 初始化
  fml('fml-xavier-init', 'Xavier 初始化', 'optimization',
    ['权重初始化', '梯度消失', '梯度爆炸', '训练稳定'],
    String.raw`W_{ij} \sim U\!\left(-\sqrt{\frac{6}{m+n}},\; \sqrt{\frac{6}{m+n}}\right)`,
    '#9b59b6', '根据输入输出维度自动设定权重范围', { ...DL, chapter: '§8.4', cite: 'Goodfellow §8.4' }),

  // ▼ NEW: BatchNorm — 训练稳定性
  fml('fml-batchnorm', '批量归一化', 'optimization',
    ['训练稳定', '加速收敛', '所有现代网络', 'ResNet'],
    String.raw`\hat{x}_i = \frac{x_i - \mu_B}{\sqrt{\sigma_B^2 + \epsilon}}, \quad y_i = \gamma \hat{x}_i + \beta`,
    '#3498db', '每层输出标准化后再缩放平移', { ...DL, chapter: '§8.7.1', cite: 'Goodfellow §8.7.1' }),

  // ═══════════════════════════════════════════════════════════
  // 信息论 Information Theory — 熵 → 交叉熵 → KL散度
  // ═══════════════════════════════════════════════════════════
  fml('fml-entropy', '信息熵', 'information',
    ['决策树', 'ID3/C4.5', '特征选择', '信息增益'],
    String.raw`H(X) = -\sum_{i} p(x_i) \log p(x_i)`,
    '#e74c3c', '不确定性的度量', PML),

  fml('fml-cross-entropy', '交叉熵损失', 'information',
    ['分类', 'Softmax配套', 'NLP', 'CV'],
    String.raw`H(p,q) = -\sum_{x} p(x) \log q(x)`,
    '#e74c3c', '预测和真实的差距', DL),

  fml('fml-kl-divergence', 'KL散度', 'information',
    ['VAE', '知识蒸馏', 'RL策略优化', '信息论'],
    String.raw`D_{KL}(P\|Q) = \sum_{x} P(x) \log\frac{P(x)}{Q(x)}`,
    '#8e44ad', '两个分布的差异(有方向)', PML),

  // ═══════════════════════════════════════════════════════════
  // 深度学习 Deep Learning — 卷积 → Attention (架构专属公式)
  // ═══════════════════════════════════════════════════════════

  // ▼ NEW: 1D 卷积 — 信号/序列处理基础
  fml('fml-conv1d', '1D 卷积', 'deep_learning',
    ['信号处理', '时间序列', '文本CNN', '音频处理'],
    String.raw`(f * g)(t) = \sum_{\tau=-\infty}^{\infty} f(\tau)\, g(t - \tau)`,
    '#e74c3c', '滑动核逐元素相乘求和', { ...DL, chapter: '§9.1', cite: 'Goodfellow §9.1' }),

  // ▼ NEW: 2D 卷积 — CV 核心操作
  fml('fml-conv2d', '2D 卷积', 'deep_learning',
    ['CNN', '图像特征提取', 'ResNet', 'YOLO', 'U-Net'],
    String.raw`S(i,j) = (K * I)(i,j) = \sum_m \sum_n I(i+m, j+n)\, K(m,n)`,
    '#3498db', '卷积核在图像上滑动提取局部特征', { ...DL, chapter: '§9.1', cite: 'Goodfellow §9.1' }),

  // ▼ NEW: Scaled Dot-Product Attention — Transformer 核心
  fml('fml-attention', 'Scaled Dot-Product Attention', 'deep_learning',
    ['Transformer', 'GPT', 'BERT', 'Self-Attention', 'LLM'],
    String.raw`\text{Attention}(Q,K,V) = \text{softmax}\!\left(\frac{QK^T}{\sqrt{d_k}}\right) V`,
    '#9b59b6', '查询与键的相似度加权求和值向量', ATT),

  // ▼ NEW: Multi-Head Attention
  fml('fml-multihead-attn', 'Multi-Head Attention', 'deep_learning',
    ['Transformer', 'GPT', 'BERT', '并行注意力'],
    String.raw`\text{MultiHead}(Q,K,V) = \text{Concat}(\text{head}_1,\ldots,\text{head}_h) W^O`,
    '#e67e22', '多个注意力头并行捕捉不同子空间', ATT),

  // ▼ NEW: Positional Encoding
  fml('fml-pos-encoding', '位置编码', 'deep_learning',
    ['Transformer', '序列位置', 'GPT', 'BERT'],
    String.raw`PE_{(pos,2i)} = \sin\!\left(\frac{pos}{10000^{2i/d}}\right), \quad PE_{(pos,2i+1)} = \cos\!\left(\frac{pos}{10000^{2i/d}}\right)`,
    '#f39c12', '用正余弦编码序列中每个位置', ATT),

  // ▼ NEW: Residual Connection
  fml('fml-residual', '残差连接', 'deep_learning',
    ['ResNet', 'Transformer', '梯度直通', '深层网络'],
    String.raw`y = F(x) + x`,
    '#2ecc71', '输出=变换+原始，梯度直通', { ...DL, chapter: '§7.5', cite: 'He et al. 2015' }),

  // ▼ NEW: Dropout
  fml('fml-dropout', 'Dropout 正则化', 'deep_learning',
    ['过拟合', '正则化', '集成学习', 'Transformer'],
    String.raw`\tilde{h}_i = m_i \cdot h_i, \quad m_i \sim \text{Bernoulli}(p)`,
    '#e74c3c', '训练时随机丢弃神经元，防止过拟合', { ...DL, chapter: '§7.12', cite: 'Goodfellow §7.12' }),

  // ▼ NEW: LayerNorm
  fml('fml-layernorm', 'Layer Normalization', 'deep_learning',
    ['Transformer', 'GPT', 'NLP', 'BatchNorm替代'],
    String.raw`\hat{x}_i = \frac{x_i - \mu}{\sqrt{\sigma^2 + \epsilon}}, \quad \mu = \frac{1}{H}\sum_{i=1}^{H} x_i`,
    '#4ea8de', '在特征维度上归一化，不依赖批大小', { ...DL, chapter: '§8.7', cite: 'Ba et al. 2016' }),

  // ═══════════════════════════════════════════════════════════
  // 序列模型 Sequence Models — RNN → LSTM → GRU
  // ═══════════════════════════════════════════════════════════
  fml('fml-rnn', 'RNN 循环神经网络', 'sequence_model',
    ['序列建模', '时间序列', 'NLP', '语音识别'],
    String.raw`h_t = \tanh(W_h h_{t-1} + W_x x_t + b)`,
    '#e74c3c', '当前隐状态 = f(上一步隐状态, 当前输入)', { ...DL, chapter: '§10.2', cite: 'Goodfellow §10.2' }),

  fml('fml-lstm', 'LSTM 长短期记忆', 'sequence_model',
    ['长序列', '梯度消失解决', 'NLP', '机器翻译'],
    String.raw`f_t = \sigma(W_f [h_{t-1}, x_t] + b_f), \quad c_t = f_t \odot c_{t-1} + i_t \odot \tilde{c}_t`,
    '#3498db', '遗忘门+输入门+输出门控制信息流', { ...DL, chapter: '§10.10', cite: 'Goodfellow §10.10' }),

  fml('fml-gru', 'GRU 门控循环单元', 'sequence_model',
    ['LSTM简化', '序列建模', 'NLP', '高效RNN'],
    String.raw`z_t = \sigma(W_z [h_{t-1}, x_t]), \quad h_t = (1-z_t) \odot h_{t-1} + z_t \odot \tilde{h}_t`,
    '#27ae60', '更新门+重置门，LSTM的简化版', { ...DL, chapter: '§10.10', cite: 'Cho et al. 2014' }),

  // ═══════════════════════════════════════════════════════════
  // ML 算法公式 ML Algorithm — 核心算法的数学公式
  // ═══════════════════════════════════════════════════════════
  fml('fml-linear-regression', '线性回归', 'ml_algorithm',
    ['回归基础', '预测', '最小二乘', '拟合'],
    String.raw`\hat{y} = w^T x + b = \sum_{i=1}^n w_i x_i + b`,
    '#3498db', '加权求和+截距', { ...ESL, chapter: 'Ch.3', cite: 'ESL §3.2' }),

  fml('fml-logistic-regression', '逻辑回归', 'ml_algorithm',
    ['二分类', '信用风险', 'CTR预估', '基线模型'],
    String.raw`P(y=1|x) = \sigma(w^T x + b) = \frac{1}{1+e^{-(w^T x + b)}}`,
    '#e74c3c', 'Sigmoid(线性变换) → 分类概率', { ...ESL, chapter: 'Ch.4', cite: 'ESL §4.4' }),

  fml('fml-svm-hinge', 'SVM 合页损失', 'ml_algorithm',
    ['SVM', '最大间隔', '分类', '核方法'],
    String.raw`L = \sum_{i=1}^n \max(0, 1 - y_i (w^T x_i + b)) + \lambda \|w\|^2`,
    '#9b59b6', '错分惩罚+间隔最大化', { ...ESL, chapter: 'Ch.12', cite: 'ESL §12' }),

  fml('fml-kernel-rbf', 'RBF 核函数', 'ml_algorithm',
    ['SVM', '核方法', '非线性分类', '高斯核'],
    String.raw`K(x,x') = \exp\!\left(-\frac{\|x-x'\|^2}{2\sigma^2}\right)`,
    '#e67e22', '将数据映射到无穷维空间', { ...PRML, chapter: 'Ch.6', cite: 'PRML §6.2' }),

  fml('fml-kmeans', 'K-Means 目标函数', 'ml_algorithm',
    ['聚类', '无监督', '向量量化', '数据压缩'],
    String.raw`J = \sum_{k=1}^K \sum_{x_i \in C_k} \|x_i - \mu_k\|^2`,
    '#2ecc71', '最小化每个点到聚类中心的距离和', { ...ESL, chapter: 'Ch.14', cite: 'ESL §14.3' }),

  fml('fml-pca', 'PCA 主成分分析', 'ml_algorithm',
    ['降维', '特征提取', '数据可视化', '去相关'],
    String.raw`Z = XW, \quad W = \text{top-}k \text{ eigenvectors of } X^T X`,
    '#4ea8de', '找方差最大的方向做投影', { ...MML, chapter: '§10.2', cite: 'MML §10.2' }),

  fml('fml-naive-bayes', '朴素贝叶斯', 'ml_algorithm',
    ['文本分类', '垃圾邮件', '条件独立', '快速分类'],
    String.raw`P(y|x_1,\ldots,x_n) \propto P(y) \prod_{i=1}^n P(x_i|y)`,
    '#1abc9c', '假设特征条件独立的贝叶斯分类', { ...PML, chapter: 'Ch.9', cite: 'Murphy §9.3' }),

  fml('fml-info-gain', '信息增益', 'ml_algorithm',
    ['决策树', 'ID3', 'C4.5', '特征选择'],
    String.raw`IG(D,A) = H(D) - \sum_{v \in \text{Values}(A)} \frac{|D_v|}{|D|} H(D_v)`,
    '#f39c12', '分裂前后信息熵的减少量', { ...PML, chapter: 'Ch.18', cite: 'Murphy §18.2' }),

  fml('fml-gini', '基尼系数', 'ml_algorithm',
    ['决策树', 'CART', '不纯度', '分类'],
    String.raw`\text{Gini}(D) = 1 - \sum_{k=1}^K p_k^2`,
    '#8e44ad', '节点不纯度，越小越纯', { ...ESL, chapter: 'Ch.9', cite: 'ESL §9.2' }),

  // ═══════════════════════════════════════════════════════════
  // 正则化 & 损失函数 Regularization & Loss
  // ═══════════════════════════════════════════════════════════
  fml('fml-l2-reg', 'L2 正则化 (Ridge)', 'regularization',
    ['权重衰减', 'Ridge', '过拟合', '平滑'],
    String.raw`L_{reg} = L + \lambda \sum_{i} w_i^2`,
    '#3498db', '惩罚大权重，让模型更平滑', { ...DL, chapter: '§7.1', cite: 'Goodfellow §7.1' }),

  fml('fml-l1-reg', 'L1 正则化 (LASSO)', 'regularization',
    ['稀疏', 'LASSO', '特征选择', '压缩'],
    String.raw`L_{reg} = L + \lambda \sum_{i} |w_i|`,
    '#27ae60', '让不重要的权重变0，自动特征选择', { ...ESL, chapter: 'Ch.3', cite: 'ESL §3.4' }),

  fml('fml-elastic-net', 'Elastic Net', 'regularization',
    ['L1+L2结合', '稀疏+平滑', '高维回归'],
    String.raw`L_{reg} = L + \lambda_1 \sum |w_i| + \lambda_2 \sum w_i^2`,
    '#e67e22', 'L1+L2的结合体', { ...ESL, chapter: 'Ch.3', cite: 'ESL §3.4' }),

  fml('fml-bce-loss', '二元交叉熵', 'loss_function',
    ['二分类', '逻辑回归', '目标检测', 'GAN'],
    String.raw`L = -\frac{1}{n}\sum_{i=1}^n [y_i \log \hat{y}_i + (1-y_i)\log(1-\hat{y}_i)]`,
    '#e74c3c', '二分类的标准损失函数', { ...DL, chapter: '§6.2', cite: 'Goodfellow §6.2' }),

  fml('fml-focal-loss', 'Focal Loss', 'loss_function',
    ['目标检测', '类别不平衡', 'RetinaNet', '难样本挖掘'],
    String.raw`FL(p_t) = -\alpha_t (1-p_t)^\gamma \log(p_t)`,
    '#9b59b6', '降低易分类样本的权重', { title: 'Focal Loss', author: 'Lin et al.', year: 2017, chapter: '§3', cite: 'Lin et al. 2017' }),

  fml('fml-triplet-loss', 'Triplet Loss', 'loss_function',
    ['人脸识别', '度量学习', '对比学习', 'FaceNet'],
    String.raw`L = \max(0, \|f(a)-f(p)\|^2 - \|f(a)-f(n)\|^2 + \alpha)`,
    '#e67e22', '拉近正样本、推远负样本', { title: 'FaceNet', author: 'Schroff et al.', year: 2015, chapter: '§3', cite: 'Schroff 2015' }),

  fml('fml-contrastive-loss', '对比损失', 'loss_function',
    ['SimCLR', 'CLIP', '自监督', '表示学习'],
    String.raw`L = -\log \frac{\exp(\text{sim}(z_i,z_j)/\tau)}{\sum_{k=1}^{2N} \mathbf{1}_{k \neq i} \exp(\text{sim}(z_i,z_k)/\tau)}`,
    '#2ecc71', 'InfoNCE: 正样本对相似度最大化', { title: 'SimCLR', author: 'Chen et al.', year: 2020, chapter: '§2', cite: 'Chen 2020' }),

  fml('fml-huber-loss', 'Huber Loss', 'loss_function',
    ['回归', '鲁棒', 'RL', '异常值容忍'],
    String.raw`L_\delta(a) = \begin{cases} \frac{1}{2}a^2 & |a| \leq \delta \\ \delta(|a| - \frac{1}{2}\delta) & |a| > \delta \end{cases}`,
    '#f39c12', 'MSE和MAE的折中，对异常值鲁棒', { ...ESL, chapter: 'Ch.10', cite: 'ESL §10.6' }),

  fml('fml-gan-loss', 'GAN 对抗损失', 'loss_function',
    ['GAN', '图像生成', 'StyleGAN', 'Pix2Pix'],
    String.raw`\min_G \max_D\; E[\log D(x)] + E[\log(1-D(G(z)))]`,
    '#8e44ad', '生成器和判别器的博弈', { ...DL, chapter: '§20.10', cite: 'Goodfellow §20.10' }),

  fml('fml-vae-elbo', 'VAE ELBO 损失', 'loss_function',
    ['VAE', '变分推断', '生成模型', '隐空间'],
    String.raw`\mathcal{L} = E_{q(z|x)}[\log p(x|z)] - D_{KL}(q(z|x) \| p(z))`,
    '#3498db', '重构质量 - 隐空间正则化', { ...DL, chapter: '§20.10', cite: 'Kingma & Welling 2013' }),

  // ═══════════════════════════════════════════════════════════
  // 评估指标 Evaluation Metrics
  // ═══════════════════════════════════════════════════════════
  fml('fml-accuracy', '准确率', 'evaluation',
    ['分类指标', '基准', '整体正确率'],
    String.raw`\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}`,
    '#2ecc71', '预测正确的比例', ESL),

  fml('fml-precision', '精确率', 'evaluation',
    ['分类', '信息检索', '垃圾邮件', '查准率'],
    String.raw`\text{Precision} = \frac{TP}{TP + FP}`,
    '#3498db', '预测为正中真正为正的比例', ESL),

  fml('fml-recall', '召回率', 'evaluation',
    ['分类', '医疗诊断', '安全检测', '查全率'],
    String.raw`\text{Recall} = \frac{TP}{TP + FN}`,
    '#e67e22', '真正为正中被找出的比例', ESL),

  fml('fml-f1', 'F1 分数', 'evaluation',
    ['分类', '精确率和召回率的调和平均', 'NLP'],
    String.raw`F_1 = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}`,
    '#e74c3c', '精确率和召回率的平衡点', ESL),

  fml('fml-iou', 'IoU 交并比', 'evaluation',
    ['目标检测', '语义分割', 'YOLO', 'mAP'],
    String.raw`\text{IoU} = \frac{|A \cap B|}{|A \cup B|}`,
    '#9b59b6', '预测框和真实框的重叠程度', { title: 'Object Detection', author: 'Various', year: 2016, chapter: '§', cite: 'Everingham 2010' }),

  fml('fml-r-squared', 'R² 决定系数', 'evaluation',
    ['回归评估', '拟合优度', '线性回归', '模型选择'],
    String.raw`R^2 = 1 - \frac{\sum(y_i - \hat{y}_i)^2}{\sum(y_i - \bar{y})^2}`,
    '#4ea8de', '模型解释了多少比例的方差', ESL),

  fml('fml-bias-variance', '偏差-方差分解', 'evaluation',
    ['过拟合', '欠拟合', '模型选择', '泛化'],
    String.raw`E[(y - \hat{f})^2] = \text{Bias}^2 + \text{Variance} + \text{Noise}`,
    '#f39c12', '误差 = 偏差² + 方差 + 噪声', { ...ESL, chapter: 'Ch.7', cite: 'ESL §7.3' }),

  // ═══════════════════════════════════════════════════════════
  // 概率分布 Probability Distributions — 常见分布族
  // ═══════════════════════════════════════════════════════════
  fml('fml-bernoulli', '伯努利分布', 'distribution',
    ['二分类', '抛硬币', 'Dropout', '二值'],
    String.raw`P(X=k) = p^k (1-p)^{1-k}, \quad k \in \{0,1\}`,
    '#e74c3c', '单次试验的成功/失败', { ...PML, chapter: 'Ch.2', cite: 'Murphy §2.4' }),

  fml('fml-binomial', '二项分布', 'distribution',
    ['多次伯努利', '质量控制', '假设检验'],
    String.raw`P(X=k) = \binom{n}{k} p^k (1-p)^{n-k}`,
    '#3498db', 'n次独立试验中成功k次的概率', { ...PML, chapter: 'Ch.2', cite: 'Murphy §2.4' }),

  fml('fml-poisson', '泊松分布', 'distribution',
    ['事件计数', '稀有事件', '排队论', 'NLP'],
    String.raw`P(X=k) = \frac{\lambda^k e^{-\lambda}}{k!}`,
    '#27ae60', '单位时间内事件发生次数', { ...PML, chapter: 'Ch.2', cite: 'Murphy §2.4' }),

  fml('fml-uniform', '均匀分布', 'distribution',
    ['随机初始化', '随机采样', '蒙特卡洛'],
    String.raw`f(x) = \frac{1}{b-a}, \quad a \leq x \leq b`,
    '#f39c12', '区间内等概率', { ...PML, chapter: 'Ch.2', cite: 'Murphy §2.4' }),

  fml('fml-exponential', '指数分布', 'distribution',
    ['等待时间', '无记忆性', '生存分析'],
    String.raw`f(x) = \lambda e^{-\lambda x}, \quad x \geq 0`,
    '#e67e22', '事件间隔时间的分布', { ...PML, chapter: 'Ch.2', cite: 'Murphy §2.4' }),

  fml('fml-beta', 'Beta 分布', 'distribution',
    ['贝叶斯先验', '概率的概率', 'A/B测试', '共轭先验'],
    String.raw`f(x;\alpha,\beta) = \frac{x^{\alpha-1}(1-x)^{\beta-1}}{B(\alpha,\beta)}`,
    '#9b59b6', '概率值本身的概率分布', { ...PML, chapter: 'Ch.2', cite: 'Murphy §2.4' }),

  fml('fml-categorical', '分类分布', 'distribution',
    ['多分类', 'Softmax输出', '骰子', '离散'],
    String.raw`P(X=k) = p_k, \quad \sum_{k=1}^K p_k = 1`,
    '#1abc9c', 'K类中选一类', { ...PML, chapter: 'Ch.2', cite: 'Murphy §2.4' }),

  // ═══════════════════════════════════════════════════════════
  // 基础数学 Basic Math — 指数/对数/代数/几何/三角/数列/级数
  // ═══════════════════════════════════════════════════════════
  fml('fml-exponent-rules', '指数法则', 'basic_math',
    ['指数运算', '基础代数', '化简', '预备知识'],
    String.raw`a^m \cdot a^n = a^{m+n}, \quad (a^m)^n = a^{mn}, \quad a^{-n} = \frac{1}{a^n}`,
    '#e74c3c', '指数的乘法/幂/负指数规则', CALC),

  fml('fml-log-rules', '对数法则', 'basic_math',
    ['对数运算', '交叉熵计算', '信息论基础', '损失函数'],
    String.raw`\log(ab) = \log a + \log b, \quad \log\frac{a}{b} = \log a - \log b, \quad \log a^n = n \log a`,
    '#3498db', '对数把乘法变加法', CALC),

  fml('fml-change-of-base', '换底公式', 'basic_math',
    ['对数', '计算', '信息论', 'bit/nat转换'],
    String.raw`\log_a b = \frac{\ln b}{\ln a} = \frac{\log_c b}{\log_c a}`,
    '#27ae60', '任意底的对数互相转换', CALC),

  fml('fml-exp-log-inverse', '指数对数互逆', 'basic_math',
    ['指数', '对数', 'Softmax', '交叉熵'],
    String.raw`e^{\ln x} = x, \quad \ln(e^x) = x`,
    '#f39c12', 'exp和log互为逆运算', CALC),

  fml('fml-quadratic', '一元二次方程求根', 'basic_math',
    ['代数基础', '判别式', '抛物线', '方程求解'],
    String.raw`x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}`,
    '#9b59b6', 'ax²+bx+c=0 的通解', CALC),

  fml('fml-binomial-theorem', '二项式定理', 'basic_math',
    ['展开', '组合数', '概率', 'Taylor基础'],
    String.raw`(a+b)^n = \sum_{k=0}^{n} \binom{n}{k} a^{n-k} b^k`,
    '#e67e22', '(a+b)的n次方展开', CALC),

  fml('fml-combination', '组合数 C(n,k)', 'basic_math',
    ['排列组合', '概率', '二项分布', '采样'],
    String.raw`\binom{n}{k} = \frac{n!}{k!(n-k)!}`,
    '#1abc9c', '从n个中选k个的方案数', { ...PML, chapter: 'Ch.2', cite: 'Murphy §2' }),

  fml('fml-factorial', '阶乘', 'basic_math',
    ['排列', '组合', '概率', '泊松分布'],
    String.raw`n! = n \times (n-1) \times \cdots \times 2 \times 1, \quad 0! = 1`,
    '#e74c3c', 'n个元素的全排列数', CALC),

  fml('fml-arithmetic-series', '等差数列求和', 'basic_math',
    ['数列', '序列', '复杂度分析', '求和'],
    String.raw`S_n = \frac{n(a_1 + a_n)}{2} = \frac{n(2a_1 + (n-1)d)}{2}`,
    '#4ea8de', '首尾相加乘项数除2', CALC),

  fml('fml-geometric-series', '等比数列求和', 'basic_math',
    ['指数衰减', '学习率', '动量累积', '折扣因子'],
    String.raw`S_n = a_1 \cdot \frac{1-r^n}{1-r}, \quad S_\infty = \frac{a_1}{1-r}\;(|r|<1)`,
    '#2ecc71', '公比r的n项和/无穷级数', CALC),

  fml('fml-taylor', 'Taylor 展开', 'basic_math',
    ['近似', '线性化', 'Newton法', '优化理论'],
    String.raw`f(x) = \sum_{n=0}^{\infty} \frac{f^{(n)}(a)}{n!}(x-a)^n`,
    '#8e44ad', '用多项式近似任意函数', CALC),

  fml('fml-euler-formula', 'Euler 公式', 'basic_math',
    ['复数', '傅里叶变换', '位置编码', '信号处理'],
    String.raw`e^{i\theta} = \cos\theta + i\sin\theta`,
    '#e74c3c', '指数函数与三角函数的桥梁', CALC),

  fml('fml-pythagorean', '勾股定理', 'basic_math',
    ['距离计算', '欧氏距离基础', '几何', '范数'],
    String.raw`a^2 + b^2 = c^2`,
    '#3498db', '直角三角形三边关系，距离的本质', CALC),

  fml('fml-trig-sin-cos', '三角函数基础', 'basic_math',
    ['旋转', '位置编码', '周期信号', '傅里叶'],
    String.raw`\sin^2\theta + \cos^2\theta = 1`,
    '#27ae60', '单位圆上的基本恒等式', CALC),

  fml('fml-sum-product', '求和与连乘', 'basic_math',
    ['符号', '损失函数', '似然', '梯度'],
    String.raw`\sum_{i=1}^n a_i = a_1 + a_2 + \cdots + a_n, \quad \prod_{i=1}^n a_i = a_1 \cdot a_2 \cdots a_n`,
    '#f39c12', '数学符号 Σ 和 Π 的含义', CALC),

  fml('fml-abs-value', '绝对值', 'basic_math',
    ['距离', 'MAE', 'L1范数', '激活函数'],
    String.raw`|x| = \begin{cases} x & x \geq 0 \\ -x & x < 0 \end{cases}`,
    '#e67e22', '到原点的距离，去掉负号', CALC),

  fml('fml-floor-ceil', '下取整/上取整', 'basic_math',
    ['卷积输出尺寸', '步长计算', '分组', '离散化'],
    String.raw`\lfloor x \rfloor = \max\{n \in \mathbb{Z} : n \leq x\}, \quad \lceil x \rceil = \min\{n \in \mathbb{Z} : n \geq x\}`,
    '#1abc9c', '向下/向上取最近整数', CALC),

  fml('fml-max-min', 'max / min / argmax', 'basic_math',
    ['ReLU', '分类预测', '优化目标', '池化'],
    String.raw`\arg\max_i a_i = j \iff a_j \geq a_i \;\forall i`,
    '#4ea8de', '最大值的索引，分类预测的核心', CALC),

  fml('fml-set-ops', '集合运算', 'basic_math',
    ['概率论基础', 'IoU', '交集并集', '事件空间'],
    String.raw`A \cup B, \quad A \cap B, \quad A^c, \quad |A \cup B| = |A| + |B| - |A \cap B|`,
    '#8e44ad', '并、交、补，容斥原理', { ...PML, chapter: 'Ch.1', cite: 'Murphy §1' }),

  // ═══════════════════════════════════════════════════════════
  // 信息论补充 Information Theory — 互信息/联合熵
  // ═══════════════════════════════════════════════════════════
  fml('fml-mutual-info', '互信息', 'information',
    ['特征选择', '关联性', '信息增益', '独立性'],
    String.raw`I(X;Y) = \sum_{x,y} p(x,y) \log \frac{p(x,y)}{p(x)p(y)}`,
    '#27ae60', '两个变量共享多少信息', PML),

  fml('fml-conditional-entropy', '条件熵', 'information',
    ['决策树', '信息增益', '特征选择', '编码'],
    String.raw`H(Y|X) = -\sum_{x,y} p(x,y) \log p(y|x)`,
    '#4ea8de', '已知X后Y的剩余不确定性', PML),

  fml('fml-joint-entropy', '联合熵', 'information',
    ['信息论', '编码', '互信息计算'],
    String.raw`H(X,Y) = -\sum_{x,y} p(x,y) \log p(x,y)`,
    '#f39c12', 'XY同时的不确定性', PML),

  // ═══════════════════════════════════════════════════════════
  // 线性代数补充 Linear Algebra — Trace/Frobenius/Hadamard/伪逆
  // ═══════════════════════════════════════════════════════════
  fml('fml-trace', '矩阵迹', 'linear',
    ['Frobenius范数', '特征值之和', '矩阵导数'],
    String.raw`\text{tr}(A) = \sum_{i=1}^n a_{ii} = \sum_{i=1}^n \lambda_i`,
    '#e74c3c', '对角线元素之和 = 特征值之和', LA),

  fml('fml-frobenius', 'Frobenius 范数', 'linear',
    ['矩阵范数', '矩阵近似', '低秩近似', 'SVD'],
    String.raw`\|A\|_F = \sqrt{\sum_{i,j} a_{ij}^2} = \sqrt{\text{tr}(A^T A)}`,
    '#3498db', '矩阵所有元素平方和再开根', { ...LA, chapter: 'Ch.7', cite: 'Strang §7' }),

  fml('fml-hadamard', 'Hadamard 逐元素乘', 'linear',
    ['Attention', 'LSTM门控', 'BatchNorm', '逐元素'],
    String.raw`(A \odot B)_{ij} = a_{ij} \cdot b_{ij}`,
    '#27ae60', '对应位置元素相乘', LA),

  fml('fml-outer-product', '外积', 'linear',
    ['秩1矩阵', '投影矩阵', '注意力', '协方差'],
    String.raw`\vec{u} \otimes \vec{v} = \vec{u}\,\vec{v}^T \in \mathbb{R}^{m \times n}`,
    '#e67e22', '列向量×行向量=矩阵', LA),

  fml('fml-pseudo-inverse', 'Moore-Penrose 伪逆', 'linear',
    ['最小二乘', '欠定系统', 'SVD应用', '线性回归'],
    String.raw`A^+ = V \Sigma^+ U^T, \quad \hat{x} = A^+ b`,
    '#9b59b6', '非方阵的"逆"，最小二乘解', { ...MML, chapter: '§4.5', cite: 'MML §4.5' }),
]

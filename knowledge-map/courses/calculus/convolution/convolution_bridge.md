---
topic: convolution
dimension: bridge
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📚 Book: Oppenheim & Willsky, Signals and Systems, Ch.2-4"
  - "📚 Book: Goodfellow et al., Deep Learning Ch.9.1 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
expiry: 12m
status: current
---

# 卷积 (Convolution) 衔接与扩展

> 📚 Book: Oppenheim & Willsky, 《Signals and Systems》, Ch.2–4

---

## ← 上一个概念 / 下一个概念 →

| 方向 | 主题 | 关系 |
|------|------|------|
| ← 前置 | 微积分（积分） | 卷积是一种特殊的积分运算 |
| ← 前置 | δ 函数 | 卷积的单位元 $f * \delta = f$ |
| ← 前置 | 线性代数 | 卷积可表示为 Toeplitz 矩阵乘法 |
| → 后续 | 傅里叶变换 / FFT | 卷积定理连接时域与频域 |
| → 后续 | LTI 系统理论 | $y = x * h$ 描述所有 LTI 系统 |
| → 后续 | 数字滤波器 (FIR/IIR) | FIR = 有限长脉冲响应 = 有限长离散卷积 |
| → 后续 | 图像处理 | 2D 卷积用于模糊/边缘检测/锐化 |
| → 后续 | 深度学习卷积层 | [conv_layer](../../deep-learning/conv_layer/) |

> 📚 Book: Oppenheim & Willsky, Ch.2–4

---

## 信号处理卷积 → DL 卷积的桥梁 ⭐

这是本文件最重要的部分——理解两个"卷积"之间的异同。

| 维度 | 信号处理卷积 | 深度学习"卷积" |
|------|-------------|---------------|
| **数学运算** | 卷积 $\int f(\tau)g(t-\tau)d\tau$（翻转核） | 互相关 $\int f(\tau)g(t+\tau)d\tau$（不翻转） |
| **核的来源** | 预先设计（Sobel、Gaussian 等） | 从数据中自动学习 |
| **核的可变性** | 固定不变 | 通过反向传播更新 |
| **维度** | 通常 1D 或 2D | 3D（$K \times K \times C_{in}$）含通道 |
| **多核** | 通常一个核 | $C_{out}$ 个核，产生多通道输出 |
| **交换律** | ✅ $f*g = g*f$ | ❌ 不满足（互相关不具交换律） |
| **实现方式** | FFT 加速 $O(N\log N)$ | im2col + 矩阵乘法（GPU 优化） |
| **边界处理** | 灵活（wrap/symm/fill） | 通常补零 (zero-padding) |

**关键洞察：** DL 用互相关替代卷积是安全的，因为:
- 滤波器权重是**学出来的**，模型会自动学到"已翻转"的最优权重
- 翻不翻转只影响权重的存储顺序，不影响网络的表达能力

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.1

---

## 上游依赖

| 来自主题 | 复用的概念 | 在本主题中如何使用 |
|---------|-----------|-------------------|
| 微积分 | 黎曼积分、被积函数 | 连续卷积的定义基础 |
| δ 函数 | 筛选性质 $f * \delta = f$ | 卷积的单位元，LTI 推导起点 |
| 复分析 | $e^{j\omega t}$ 指数函数 | 傅里叶变换和卷积定理 |
| 线性代数 | 矩阵乘法 | 卷积等价于 Toeplitz 矩阵乘法 |

---

## 下游影响

| 去向主题 | 本主题提供的概念 | 在下游如何被使用 |
|---------|----------------|-----------------|
| 傅里叶变换 | 卷积定理 | FFT 加速卷积计算 |
| LTI 系统 | $y = x * h$ | 脉冲响应完全描述系统 |
| FIR 滤波器 | 离散有限卷积 | DSP 芯片的核心操作 |
| 图像处理 | 2D 卷积 + 手工核 | 模糊、边缘检测、锐化 |
| DL 卷积层 | 卷积概念 + 局部加权求和 | 可学习滤波器自动提取特征 |
| 概率论 | 独立随机变量之和的分布 | $p_{X+Y} = p_X * p_Y$ |

> 📚 Book: Oppenheim & Willsky, Ch.2–4

---

## 概念演变追踪

| 概念 | 信号处理中 | 深度学习中 | 变化原因 |
|------|-----------|-----------|---------|
| 卷积运算 | 严格数学卷积（翻转） | 互相关（不翻转） | 可学习核使翻转无意义 |
| 卷积核 | 手工设计固定核 | 自动学习的权重 | 端到端训练更优 |
| 维度 | 1D 信号 / 2D 图像 | 3D 张量（含通道维） | 多通道特征图需要 |
| 加速方式 | FFT（$O(N\log N)$） | im2col + GEMM（GPU 优化） | GPU 矩阵乘法更快 |
| 边界处理 | 多种（镜像/周期/零） | 几乎只用零填充 | 工程简化 |

---

## 📚 扩展阅读

| 资源 | 类型 | 为什么值得读 |
|------|------|-------------|
| Oppenheim & Willsky, Ch.2 | 📚 教科书 | 卷积的经典信号处理讲解 |
| Goodfellow Ch.9.1 | 📚 教科书 | 信号处理卷积→DL卷积的桥梁 |
| [3B1B 卷积可视化](https://www.youtube.com/watch?v=KuXjwB4LzSA) | 🎬 视频 | 直觉理解卷积的最佳动画 |
| Cooley & Tukey 1965 | 📖 论文 | FFT 原始论文 |

---

## 与工作区已有知识库的关联

| 类别 | 代表 | 学习点 |
|------|------|--------|
| DL 卷积层 | [conv_layer](../../deep-learning/conv_layer/) | 信号处理卷积→DL 卷积的概念演变 |
| CNN | [cnn](../../deep-learning/cnn/) | 卷积层堆叠成完整架构 |
| MLP | [mlp](../../deep-learning/mlp/) | 卷积层是 MLP 全连接层的受限版本 |

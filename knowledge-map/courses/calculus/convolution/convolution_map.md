---
topic: convolution
dimension: map
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📚 Book: Oppenheim & Willsky, 'Signals and Systems', 2nd Ed. Ch.2-4 — https://www.pearson.com/en-us/subject-catalog/p/signals-and-systems/P200000003519"
  - "📚 Book: Haykin & Van Veen, 'Signals and Systems', 2nd Ed. Ch.2 — https://www.wiley.com/en-us/Signals+and+Systems-p-9780471164746"
  - "📚 Book: Goodfellow et al., Deep Learning Ch.9.1 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📖 Paper: Cooley & Tukey, 'An algorithm for the machine calculation of complex Fourier series', 1965 — https://doi.org/10.1090/S0025-5718-1965-0178586-1"
expiry: never
status: current
---

# 卷积 (Convolution) 知识地图 — 信号处理视角

> 📚 Book: Oppenheim & Willsky, [《Signals and Systems》](https://www.pearson.com/en-us/subject-catalog/p/signals-and-systems/P200000003519), Ch.2–4
> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.1

## 1. 核心问题

- **卷积是什么？** → 两个函数的一种运算：翻转 → 滑动 → 逐点相乘 → 积分/求和
- **卷积解决什么问题？** → 描述线性时不变 (LTI) 系统对任意输入的输出
- **卷积定理是什么？** → 时域卷积 = 频域逐点相乘（可用 FFT 加速）
- **互相关和卷积什么区别？** → 互相关不翻转核，深度学习用的"卷积"其实是互相关
- **连续卷积和离散卷积什么关系？** → 离散卷积是连续卷积的采样版本

> 📚 Book: Oppenheim & Willsky, Ch.2.4, Ch.4.4

---

## 2. 全景位置

```
数学与信号处理 (Mathematics & Signal Processing)
├── 基础运算 (Fundamental Operations)
│   ├── 加法、乘法
│   ├── 微分 / 差分
│   ├── 积分 / 求和
│   └── 【卷积 (Convolution)】 ← 你在这里
│       ├── 连续卷积 (Continuous)
│       ├── 离散卷积 (Discrete)
│       └── 循环卷积 (Circular)
├── 变换域 (Transform Domain)
│   ├── 傅里叶变换 (FT / DFT / FFT)
│   ├── 拉普拉斯变换
│   └── Z 变换
├── 系统理论 (System Theory)
│   ├── 线性时不变系统 (LTI)
│   ├── 脉冲响应 (Impulse Response) h(t)
│   └── 传递函数 H(s) / H(z)
└── 应用
    ├── 数字滤波器 (FIR / IIR)
    ├── 图像处理（模糊、边缘检测）
    └── 深度学习卷积层 ← 向下游延伸
```

> 📚 Book: Oppenheim & Willsky, Ch.1–4

---

## 3. 依赖地图

```
前置知识                          本主题                          后续方向
┌──────────────────────┐    ┌──────────────────────┐    ┌──────────────────────────┐
│ 积分/求和             │───→│                      │───→│ LTI 系统分析              │
│ 函数翻转与平移        │───→│                      │───→│ 傅里叶变换 / FFT          │
│ 狄拉克 δ 函数         │───→│   卷积               │───→│ 数字滤波器 (FIR/IIR)      │
│ 复数/指数函数         │───→│   (Convolution)      │───→│ 图像处理（模糊/边缘检测）  │
│ 线性代数             │───→│                      │───→│ 深度学习卷积层             │
│                      │    │                      │───→│ 去卷积 (Deconvolution)     │
└──────────────────────┘    └──────────────────────┘    └──────────────────────────┘
```

> 📚 Book: Oppenheim & Willsky, Ch.2

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [convolution_map.md](convolution_map.md) | ① 导航 | 第一次接触、需要全局视角 |
| [convolution_concepts.md](convolution_concepts.md) | ② 概念 | 理解术语、辨析卷积vs互相关 |
| [convolution_math.md](convolution_math.md) | ③ 公式 | 卷积定义、性质、卷积定理 |
| [convolution_tutorial.md](convolution_tutorial.md) | ④ 教程 | Why-First 理解卷积的动机 |
| [convolution_code.md](convolution_code.md) | ⑤ 代码 | NumPy/SciPy 实现 |
| [convolution_pitfalls.md](convolution_pitfalls.md) | ⑥ 踩坑 | 常见错误 |
| [convolution_history.md](convolution_history.md) | ⑦ 历史 | 从 Euler 到 FFT 到 DL |
| [convolution_bridge.md](convolution_bridge.md) | ⑧ 衔接 | 信号处理 ↔ 深度学习的桥梁 |
| [convolution_first_principles.md](convolution_first_principles.md) | ⑨ 第一性原理 | 为什么卷积必须这样定义 |

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读 [convolution_tutorial.md](convolution_tutorial.md) Section 1 理解动机
2. 读 [convolution_concepts.md](convolution_concepts.md) 掌握术语
3. 读 [convolution_math.md](convolution_math.md) 手算一次卷积
4. 读 [convolution_history.md](convolution_history.md) → 理解为什么要"翻转再滑动"
5. 跑 [convolution_code.md](convolution_code.md) 看可视化动画

### 已有信号处理基础，学 DL 🔧

1. 读 [convolution_bridge.md](convolution_bridge.md) 理解信号处理卷积→DL卷积的区别
2. 查 [convolution_concepts.md](convolution_concepts.md) 卷积 vs 互相关辨析
3. 转到 [../deep-learning/conv_layer/](../../deep-learning/conv_layer/) 学习 DL 卷积层

---

## 6–7. 缺口检查 & 新鲜度

| 维度 | 上次验证 | 状态 |
|------|---------|------|
| 全部 9 维 | 2026-03-14 | ✅ current |

---

## 8. 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| Oppenheim & Willsky,《Signals and Systems》 | 📚 教科书 | 全文核心参考 |
| Haykin & Van Veen,《Signals and Systems》 | 📚 教科书 | 补充参考 |
| Goodfellow et al.,《Deep Learning》Ch.9.1 | 📚 教科书 | Bridge：DL 中的卷积 |
| Cooley & Tukey 1965 | 📖 论文 | History：FFT 算法 |

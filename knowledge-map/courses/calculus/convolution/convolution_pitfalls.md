---
topic: convolution
dimension: pitfalls
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📚 Book: Oppenheim & Willsky, Signals and Systems, Ch.2,8"
  - "📖 Docs: NumPy np.convolve — https://numpy.org/doc/stable/reference/generated/numpy.convolve.html"
  - "📚 Book: Goodfellow et al., Deep Learning Ch.9.1 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
expiry: 6m
status: current
---

# 卷积 (Convolution) 踩坑记录

---

## 坑 1: 卷积和互相关搞混

**场景：** 从信号处理教材学了卷积（翻转），转到深度学习发现结果对不上

**症状：** 手算结果和 PyTorch `nn.Conv1d` 的输出不一致

**根因：** 数学卷积翻转核 $g(-\tau)$，但 DL 框架的"卷积"**不翻转**（实际是互相关）

**解法：**

❌ 错误认知 — 以为 DL 卷积会翻转核

```python
# 数学卷积: f*g = Σf[k]·g[n-k] (翻转 g)
# DL "卷积": Σf[k]·g[n+k] (不翻转，是互相关!)

# 如果你手动翻转核再传给 nn.Conv1d，等于翻转了两次 = 没翻转
```

✅ 正确理解

```python
import numpy as np
f = np.array([1, 2, 3])
g = np.array([1, -1])

# 数学卷积 (翻转 g)
print(np.convolve(f, g))      # [ 1  1  1 -3]

# 互相关 (不翻转 g) = DL 的 "卷积"
print(np.correlate(f, g, mode='full'))  # [-2 -1  1  3]  ← 不同！

# DL 中滤波器是学出来的，翻不翻转结果等价（学到的权重自然会补偿）
```

**教训：** `np.convolve` = 数学卷积（翻转）；`np.correlate` / DL Conv = 互相关（不翻转）

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.1

---

## 坑 2: FFT 卷积得到循环卷积而非线性卷积

**场景：** 直接对两个序列做 FFT → 相乘 → IFFT，结果和 `np.convolve` 不同

**症状：** 尾部结果有"混叠"错误

**根因：** FFT 隐式做**循环卷积**。长度 $N$ 的循环卷积会将超出部分"卷"回来叠加

**解法：**

❌ 错误写法 — 直接 FFT 不补零

```python
f = np.array([1, 2, 3])
g = np.array([1, 1])
# FFT 长度 = max(3, 2) = 3 → 循环卷积!
Y = np.fft.ifft(np.fft.fft(f, 3) * np.fft.fft(g, 3)).real
print(Y)  # [4. 3. 5.] ← 错误！(循环混叠)
```

✅ 正确写法 — 补零到 N1+N2-1

```python
N = len(f) + len(g) - 1  # = 3+2-1 = 4
Y = np.fft.ifft(np.fft.fft(f, N) * np.fft.fft(g, N)).real
print(Y)  # [1. 3. 5. 3.] ← 正确!

# 或直接用 SciPy 封装好的
from scipy.signal import fftconvolve
print(fftconvolve(f, g))  # [1. 3. 5. 3.] ✓
```

**教训：** FFT 卷积必须补零到 $N_1 + N_2 - 1$，否则得到循环卷积

> 📚 Book: Oppenheim & Willsky, Ch.8

---

## 坑 3: mode 参数选错导致输出长度不符预期

**场景：** 用 `np.convolve` 时没注意 mode 参数

**症状：** 输出长度和预期不一致

**根因：** `mode='full'`(默认) / `'same'` / `'valid'` 含义不同

**解法：**

```python
f = np.array([1, 2, 3, 4, 5])  # 长度 5
g = np.array([1, 1, 1])         # 长度 3

print(np.convolve(f, g, mode='full'))   # [1 3 6 9 12 9 5]   长度 7 = 5+3-1
print(np.convolve(f, g, mode='same'))   # [3 6 9 12 9]        长度 5 = max(5,3)
print(np.convolve(f, g, mode='valid'))  # [6 9 12]            长度 3 = 5-3+1
```

| mode | 输出长度 | 何时用 |
|------|---------|--------|
| `full` | $N_1+N_2-1$ | 完整数学卷积 |
| `same` | $\max(N_1,N_2)$ | 保持输入长度 |
| `valid` | $|N_1-N_2|+1$ | 只保留完全重叠部分 |

> 📖 Docs: [np.convolve](https://numpy.org/doc/stable/reference/generated/numpy.convolve.html)

---

## 坑 4: 2D 卷积的 boundary 处理不当

**场景：** 图像卷积时边缘出现黑边或伪影

**症状：** 输出图像边缘变暗或出现不自然的边界

**根因：** 边界填充方式影响边缘区域的计算结果

**解法：**

```python
from scipy.signal import convolve2d

kernel = np.ones((3,3)) / 9  # 均值模糊

# fill: 边界外补零（可能导致边缘变暗）
r1 = convolve2d(img, kernel, mode='same', boundary='fill')

# wrap: 边界外用另一边的值（适合周期信号）
r2 = convolve2d(img, kernel, mode='same', boundary='wrap')

# symm: 边界外镜像反射（推荐，最自然）
r3 = convolve2d(img, kernel, mode='same', boundary='symm')
```

**教训：** 图像卷积推荐 `boundary='symm'` 或 `'reflect'`

> 📖 Docs: [scipy.signal.convolve2d](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.convolve2d.html)

---

## 坑 5: 卷积输出长度算错

**场景：** 把离散卷积的输出长度误认为 $N_1 \times N_2$ 或 $\max(N_1, N_2)$

**解法：**

```
线性卷积输出长度 = N₁ + N₂ - 1    ← 记住这个！

例: [1,2,3](长3) * [1,1](长2) → 输出长度 = 3+2-1 = 4
```

**教训：** $N_1 + N_2 - 1$，不是 $N_1 \cdot N_2$，也不是 $\max(N_1, N_2)$

---

## 调试清单

1. [ ] **用的是卷积还是互相关？** → `np.convolve` = 卷积(翻转)；DL Conv = 互相关(不翻转)
2. [ ] **FFT 卷积补零了吗？** → 必须补零到 $N_1+N_2-1$
3. [ ] **mode 参数正确？** → `full` / `same` / `valid`
4. [ ] **输出长度 = $N_1 + N_2 - 1$？** → 线性卷积的固定长度
5. [ ] **2D 边界处理方式？** → 推荐 `symm` 或 `reflect`
6. [ ] **因果性？** → 实时系统要求 $h[n]=0$ for $n<0$

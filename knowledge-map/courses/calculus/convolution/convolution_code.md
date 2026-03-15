---
topic: convolution
dimension: code
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📖 Docs: NumPy np.convolve — https://numpy.org/doc/stable/reference/generated/numpy.convolve.html"
  - "📖 Docs: SciPy signal.convolve — https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.convolve.html"
  - "📖 Docs: SciPy signal.fftconvolve — https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.fftconvolve.html"
  - "📚 Book: Oppenheim & Willsky, Signals and Systems, Ch.2"
expiry: 6m
status: current
---

# 卷积 (Convolution) 代码参考 — 信号处理视角

> 📖 Docs: [NumPy convolve](https://numpy.org/doc/stable/reference/generated/numpy.convolve.html)
> 📖 Docs: [SciPy signal](https://docs.scipy.org/doc/scipy/reference/signal.html)


## 快速开始

### 最简示例 — 30 秒上手

```python
import numpy as np

# ============================================================
# 离散卷积 / Discrete convolution
# ============================================================
f = np.array([1, 2, 3])        # 信号 / Signal
g = np.array([1, 0.5])         # 核（脉冲响应）/ Kernel (impulse response)
result = np.convolve(f, g)
print(f"f * g = {result}")     # [1.  2.5 4.  1.5]
print(f"输出长度: {len(result)} = {len(f)} + {len(g)} - 1")  # 4 = 3+2-1
```

> 📖 Docs: [np.convolve](https://numpy.org/doc/stable/reference/generated/numpy.convolve.html)

---

## 完整实现示例

### 示例 1: 从零实现离散卷积

```python
import numpy as np

def convolve_naive(f, g):
    """从零实现离散线性卷积 / Naive discrete linear convolution

    步骤: 翻转 g → 滑动 → 逐位相乘求和
    """
    N1, N2 = len(f), len(g)
    N_out = N1 + N2 - 1                   # 输出长度 / Output length
    result = np.zeros(N_out)

    g_flipped = g[::-1]                   # Step 1: 翻转 g / Flip g

    # 补零 / Zero-pad f
    f_padded = np.pad(f, (N2 - 1, N2 - 1), mode='constant')

    for n in range(N_out):                # Step 2-3: 滑动 + 相乘求和
        result[n] = np.sum(f_padded[n : n + N2] * g_flipped)

    return result

# 测试 / Test
f = np.array([1, 2, 3, 4, 5])
g = np.array([1, 0, -1])
result = convolve_naive(f, g)
print(f"手写: {result}")                  # [ 1.  2.  2.  2.  2. -4. -5.]
print(f"NumPy: {np.convolve(f, g)}")      # 验证一致 / Verify
```

> 📚 Book: Oppenheim & Willsky, Ch.2.4

---

### 示例 2: FFT 加速卷积

```python
import numpy as np
from scipy.signal import fftconvolve
import time

def convolve_fft(f, g):
    """用 FFT 实现卷积 / FFT-based convolution

    原理: f*g = IFFT(FFT(f) · FFT(g))
    需要补零到 N1+N2-1 避免循环卷积混叠
    """
    N = len(f) + len(g) - 1
    # 补零到 2 的幂次（FFT 最高效）
    N_fft = int(2 ** np.ceil(np.log2(N)))

    F = np.fft.fft(f, N_fft)              # FFT of f
    G = np.fft.fft(g, N_fft)              # FFT of g
    Y = F * G                             # 频域相乘 / Frequency multiplication
    y = np.fft.ifft(Y).real               # IFFT 回时域 / Back to time domain

    return y[:N]                           # 截取有效长度 / Trim to valid length

# 性能对比 / Performance comparison
N = 10000
f = np.random.randn(N)
g = np.random.randn(1000)

t0 = time.time()
r1 = np.convolve(f, g)
t_direct = time.time() - t0

t0 = time.time()
r2 = fftconvolve(f, g)
t_fft = time.time() - t0

print(f"直接卷积: {t_direct:.4f}s")
print(f"FFT 卷积: {t_fft:.4f}s")
print(f"加速比: {t_direct/t_fft:.1f}x")
print(f"结果一致: {np.allclose(r1, r2)}")
```

> 📖 Docs: [scipy.signal.fftconvolve](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.fftconvolve.html)

---

### 示例 3: 2D 图像卷积（边缘检测、模糊）

```python
import numpy as np
from scipy.signal import convolve2d
from PIL import Image
import matplotlib.pyplot as plt

# ============================================================
# 常用 2D 卷积核 / Common 2D kernels
# ============================================================
kernels = {
    '均值模糊 (Box Blur)': np.ones((5,5)) / 25,

    '高斯模糊 (Gaussian)': np.array([
        [1, 4, 6, 4, 1],
        [4,16,24,16, 4],
        [6,24,36,24, 6],
        [4,16,24,16, 4],
        [1, 4, 6, 4, 1]
    ]) / 256,

    '水平边缘 (Horizontal Edge)': np.array([
        [-1, -1, -1],
        [ 0,  0,  0],
        [ 1,  1,  1]
    ]),

    '竖直边缘 (Vertical Edge)': np.array([
        [-1, 0, 1],
        [-1, 0, 1],
        [-1, 0, 1]
    ]),

    '拉普拉斯锐化 (Laplacian)': np.array([
        [ 0, -1,  0],
        [-1,  4, -1],
        [ 0, -1,  0]
    ]),

    'Sobel X': np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ]),
}

# 创建测试图像 / Create test image
img = np.random.rand(100, 100) * 255

# 应用各种核 / Apply kernels
for name, kernel in kernels.items():
    result = convolve2d(img, kernel, mode='same', boundary='fill')
    print(f"{name}: input {img.shape} → output {result.shape}")
```

> 📖 Docs: [scipy.signal.convolve2d](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.convolve2d.html)

---

### 示例 4: 卷积定理可视化验证

```python
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# 验证: 时域卷积 = 频域相乘
# ============================================================
f = np.array([1, 1, 1, 1, 0, 0, 0, 0])   # 矩形脉冲
g = np.array([1, 1, 0, 0, 0, 0, 0, 0])   # 短脉冲

# 方法 1: 时域直接卷积（需补零）
N = len(f) + len(g) - 1
f_pad = np.pad(f, (0, N - len(f)))
g_pad = np.pad(g, (0, N - len(g)))
conv_direct = np.convolve(f, g)[:N]

# 方法 2: 频域相乘
F = np.fft.fft(f_pad, N)
G = np.fft.fft(g_pad, N)
conv_fft = np.fft.ifft(F * G).real

print(f"直接卷积: {conv_direct}")
print(f"FFT 卷积: {np.round(conv_fft, 6)}")
print(f"一致: {np.allclose(conv_direct, conv_fft)}")

# 可视化
fig, axes = plt.subplots(2, 3, figsize=(12, 6))
axes[0,0].stem(f); axes[0,0].set_title('f[n]')
axes[0,1].stem(g); axes[0,1].set_title('g[n]')
axes[0,2].stem(conv_direct); axes[0,2].set_title('f * g (时域)')
axes[1,0].stem(np.abs(F)); axes[1,0].set_title('|F(ω)|')
axes[1,1].stem(np.abs(G)); axes[1,1].set_title('|G(ω)|')
axes[1,2].stem(np.abs(F*G)); axes[1,2].set_title('|F·G| (频域)')
plt.tight_layout()
plt.savefig('convolution_theorem_demo.png', dpi=100)
plt.show()
```

> 📚 Book: Oppenheim & Willsky, Ch.4.4

---

## API 速查

### NumPy

| 函数 | 参数 | 说明 |
|------|------|------|
| `np.convolve(a, v, mode)` | `mode='full'/'same'/'valid'` | 1D 离散卷积 |
| `np.correlate(a, v, mode)` | 同上 | 1D 互相关（不翻转） |
| `np.fft.fft(x, n)` | `n`=FFT 长度 | 快速傅里叶变换 |
| `np.fft.ifft(X)` | — | 逆 FFT |

### SciPy

| 函数 | 参数 | 说明 |
|------|------|------|
| `signal.convolve(a, v, mode)` | `mode='full'/'same'/'valid'` | N 维卷积 |
| `signal.fftconvolve(a, v, mode)` | 同上 | FFT 实现，长序列更快 |
| `signal.convolve2d(img, kernel, mode)` | `boundary='fill'/'wrap'` | 2D 卷积 |
| `signal.correlate(a, v, mode)` | 同上 | N 维互相关 |

### mode 参数含义

| mode | 输出长度 | 说明 |
|------|---------|------|
| `'full'` | $N_1 + N_2 - 1$ | 完整卷积结果（默认） |
| `'same'` | $\max(N_1, N_2)$ | 输出与较长输入等长 |
| `'valid'` | $|N_1 - N_2| + 1$ | 只保留完全重叠部分 |

> 📖 Docs: [NumPy convolve](https://numpy.org/doc/stable/reference/generated/numpy.convolve.html)
> 📖 Docs: [SciPy signal](https://docs.scipy.org/doc/scipy/reference/signal.html)

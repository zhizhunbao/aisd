---
topic: integration_summation
dimension: code
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📖 Docs: SciPy integrate — https://docs.scipy.org/doc/scipy/reference/integrate.html"
  - "📖 Docs: NumPy sum — https://numpy.org/doc/stable/reference/generated/numpy.sum.html"
  - "📖 Docs: SymPy integrals — https://docs.sympy.org/latest/modules/integrals/integrals.html"
  - "📚 Book: Bishop, PRML, Ch.11.1 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/bishop_prml.pdf"
expiry: 6m
status: current
---

# 积分与求和 代码参考

> 📖 Docs: [SciPy integrate](https://docs.scipy.org/doc/scipy/reference/integrate.html)
> 📖 Docs: [NumPy sum/cumsum](https://numpy.org/doc/stable/reference/generated/numpy.sum.html)


## 快速开始

### 最简示例 — 30 秒上手

```python
import numpy as np
from scipy import integrate

# ============================================================
# 1. 离散求和 / Discrete Summation
# ============================================================
values = np.array([1, 2, 3, 4, 5])
total = np.sum(values)  # 求和 / sum = 15
print(f"求和 Σ = {total}")  # 求和 Σ = 15

# ============================================================
# 2. 数值积分 / Numerical Integration
# ============================================================
# 计算 ∫₀¹ x² dx = 1/3 ≈ 0.3333
result, error = integrate.quad(lambda x: x**2, 0, 1)
print(f"∫₀¹ x² dx = {result:.4f} (误差 {error:.2e})")

# ============================================================
# 3. 蒙特卡洛积分 / Monte Carlo Integration
# ============================================================
# 用随机采样估计 ∫₀¹ x² dx
N = 100000
samples = np.random.uniform(0, 1, N)       # 从 U[0,1] 采样 / sample from U[0,1]
mc_estimate = np.mean(samples**2)           # 样本平均 / sample mean
print(f"MC 估计 = {mc_estimate:.4f}")       # ≈ 0.3333
```

**测试方法：** 直接运行，检查三个输出值：求和=15，定积分≈0.3333，MC≈0.33

> 📖 Docs: [SciPy quad](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.quad.html)

---

## 完整实现示例

### 示例 1: 概率分布的积分应用（归一化 + 期望 + CDF）

```python
import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt

# ============================================================
# 1. 定义概率密度函数 / Define PDF
# ============================================================
# 标准正态分布 PDF / Standard Normal PDF
# p(x) = (1/√(2π)) * exp(-x²/2)
def normal_pdf(x, mu=0, sigma=1):
    """正态分布概率密度函数 / Normal distribution PDF"""
    return (1 / (np.sqrt(2 * np.pi) * sigma)) * np.exp(-(x - mu)**2 / (2 * sigma**2))

# ============================================================
# 2. 验证归一化 / Verify Normalization: ∫p(x)dx = 1
# ============================================================
norm_check, _ = integrate.quad(normal_pdf, -np.inf, np.inf)
print(f"归一化验证 ∫p(x)dx = {norm_check:.6f}")  # 应为 1.000000

# ============================================================
# 3. 计算期望 / Compute Expectation: E[X] = ∫x·p(x)dx
# ============================================================
# E[X] 对标准正态 = 0
expectation, _ = integrate.quad(lambda x: x * normal_pdf(x), -np.inf, np.inf)
print(f"期望 E[X] = {expectation:.6f}")  # 应为 0.000000

# ============================================================
# 4. 计算方差 / Compute Variance: Var[X] = E[X²] - (E[X])²
# ============================================================
e_x2, _ = integrate.quad(lambda x: x**2 * normal_pdf(x), -np.inf, np.inf)
variance = e_x2 - expectation**2
print(f"方差 Var[X] = {variance:.6f}")  # 应为 1.000000

# ============================================================
# 5. 计算 CDF / Compute CDF: F(x) = ∫₋∞ˣ p(t)dt
# ============================================================
x_values = np.linspace(-4, 4, 200)
cdf_values = np.array([integrate.quad(normal_pdf, -np.inf, x)[0] for x in x_values])

# 绘图 / Plot
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].plot(x_values, normal_pdf(x_values), 'b-', lw=2)
axes[0].fill_between(x_values, normal_pdf(x_values), alpha=0.3)
axes[0].set_title('PDF: p(x)')
axes[0].set_xlabel('x')

axes[1].plot(x_values, cdf_values, 'r-', lw=2)
axes[1].set_title('CDF: F(x) = ∫₋∞ˣ p(t)dt')
axes[1].set_xlabel('x')
axes[1].axhline(y=0.5, color='gray', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig('normal_pdf_cdf.png', dpi=150)
plt.show()
```

> 📖 Docs: [SciPy quad](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.quad.html)
> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.2.3


---

### 示例 2: 蒙特卡洛积分与收敛性验证

```python
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# 1. 目标积分 / Target Integral
# ============================================================
# ∫₀¹ e^(-x²) dx ≈ 0.7468 (无封闭解)
# 解析近似值用高精度数值积分获得 / Analytical approx from high-precision quad
from scipy.integrate import quad
true_value, _ = quad(lambda x: np.exp(-x**2), 0, 1)
print(f"精确值 (数值积分): {true_value:.6f}")

# ============================================================
# 2. MC 积分 / Monte Carlo Integration
# ============================================================
# 均匀分布 p(x)=1 在 [0,1]，所以 ∫f(x)dx = E_U[f(X)] ≈ (1/N)Σf(x_i)
def mc_integrate(f, N, a=0, b=1):
    """蒙特卡洛积分 / Monte Carlo integration over [a,b]"""
    samples = np.random.uniform(a, b, N)  # 从 U[a,b] 采样 / sample from U[a,b]
    return (b - a) * np.mean(f(samples))  # 区间长度 × 样本平均 / interval × sample mean

# ============================================================
# 3. 收敛性实验 / Convergence Experiment
# ============================================================
np.random.seed(42)
sample_sizes = [10, 50, 100, 500, 1000, 5000, 10000, 50000, 100000]
estimates = []
errors = []

for N in sample_sizes:
    est = mc_integrate(lambda x: np.exp(-x**2), N)
    estimates.append(est)
    errors.append(abs(est - true_value))
    print(f"N={N:>7d} → MC估计={est:.6f}, 误差={abs(est - true_value):.6f}")

# ============================================================
# 4. 绘制收敛曲线 / Plot Convergence
# ============================================================
fig, ax = plt.subplots(figsize=(8, 5))
ax.loglog(sample_sizes, errors, 'bo-', label='实际误差 / Actual Error')
# 理论收敛速度 O(1/√N) / Theoretical rate O(1/√N)
theoretical = errors[0] * np.sqrt(sample_sizes[0]) / np.sqrt(sample_sizes)
ax.loglog(sample_sizes, theoretical, 'r--', label='O(1/√N) 理论线')
ax.set_xlabel('样本量 N / Sample Size')
ax.set_ylabel('绝对误差 / Absolute Error')
ax.set_title('蒙特卡洛积分收敛速度 / MC Integration Convergence')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('mc_convergence.png', dpi=150)
plt.show()
```

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.11.1
> 📖 Docs: [NumPy random](https://numpy.org/doc/stable/reference/random/index.html)

---

### 示例 3: 解析积分（SymPy 符号计算）

```python
from sympy import symbols, integrate, exp, sqrt, pi, oo, simplify

# ============================================================
# 1. 符号定义 / Symbol Definition
# ============================================================
x, mu, sigma = symbols('x mu sigma', real=True)
sigma = symbols('sigma', positive=True)

# ============================================================
# 2. 不定积分 / Indefinite Integral
# ============================================================
# ∫ x² dx = x³/3 + C
indef = integrate(x**2, x)
print(f"∫x² dx = {indef}")  # x**3/3

# ============================================================
# 3. 定积分 / Definite Integral
# ============================================================
# ∫₀¹ x² dx = 1/3
defin = integrate(x**2, (x, 0, 1))
print(f"∫₀¹ x² dx = {defin}")  # 1/3

# ============================================================
# 4. 高斯积分验证 / Gaussian Integral Verification
# ============================================================
# ∫₋∞^∞ exp(-x²) dx = √π
gaussian = integrate(exp(-x**2), (x, -oo, oo))
print(f"∫exp(-x²)dx = {gaussian}")  # sqrt(pi)

# ============================================================
# 5. 分部积分示例 / Integration by Parts Example
# ============================================================
# ∫ x·eˣ dx = x·eˣ - eˣ + C
ibp = integrate(x * exp(x), x)
print(f"∫x·eˣ dx = {ibp}")  # (x - 1)*exp(x)
```

> 📖 Docs: [SymPy integrals](https://docs.sympy.org/latest/modules/integrals/integrals.html)

---

## API 速查

### NumPy 求和

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `np.sum(a)` | `a` | — | 数组所有元素求和 / Sum all elements |
| ↳ `axis` | int/tuple | `None` | 沿哪个轴求和 / Along which axis |
| ↳ `keepdims` | bool | `False` | 是否保留维度 / Keep dimensions |
| `np.cumsum(a)` | `a` | — | 累积求和 / Cumulative sum |
| `np.nansum(a)` | `a` | — | 忽略 NaN 的求和 / Sum ignoring NaN |

### SciPy 数值积分

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `integrate.quad(f, a, b)` | `f` | — | 一维定积分 / 1D definite integral |
| ↳ `a, b` | float | — | 积分下/上界（可用 `np.inf`）|
| ↳ `args` | tuple | `()` | 传给 f 的额外参数 / Extra args |
| `integrate.dblquad(f, a, b, g, h)` | `f` | — | 二维积分 / 2D integral |
| `integrate.tplquad(f, a, b, g, h, q, r)` | `f` | — | 三维积分 / 3D integral |
| `integrate.trapezoid(y, x)` | `y, x` | — | 梯形法则 / Trapezoidal rule |
| `integrate.simpson(y, x)` | `y, x` | — | Simpson 法则 / Simpson's rule |

### SymPy 符号积分

| 函数/类 | 参数 | 说明 |
|---------|------|------|
| `integrate(expr, x)` | 表达式, 变量 | 不定积分 / Indefinite integral |
| `integrate(expr, (x, a, b))` | 表达式, (变量, 下界, 上界) | 定积分 / Definite integral |
| `oo` | — | 无穷大符号 $\infty$ |

### 常用工具

| 函数 | 说明 |
|------|------|
| `np.random.uniform(a, b, N)` | 生成 $N$ 个 $U[a,b]$ 样本（MC 采样用） |
| `np.random.normal(mu, sigma, N)` | 生成 $N$ 个正态样本 |
| `np.mean(a)` | 样本均值（MC 估计的核心） |

> 📖 Docs: [SciPy integrate](https://docs.scipy.org/doc/scipy/reference/integrate.html)
> 📖 Docs: [NumPy sum](https://numpy.org/doc/stable/reference/generated/numpy.sum.html)

---

## 目录结构模板

### 简单结构

```
integration_project/
├── basic_integration.py     ← 数值积分基础示例
├── mc_integration.py        ← 蒙特卡洛积分
└── symbolic_integration.py  ← SymPy 符号积分
```

### 标准结构

```
integration_project/
├── numerical/
│   ├── quad_examples.py     ← SciPy quad 示例
│   ├── trapezoid.py         ← 手写梯形法则
│   └── simpson.py           ← 手写 Simpson 法则
├── monte_carlo/
│   ├── basic_mc.py          ← 基础 MC 积分
│   ├── importance.py        ← 重要性采样
│   └── convergence.py       ← 收敛性分析
├── symbolic/
│   ├── sympy_demo.py        ← SymPy 符号积分
│   └── verify.py            ← 符号 vs 数值对比
├── applications/
│   ├── expectation.py       ← 期望计算
│   ├── marginalization.py   ← 边缘化
│   └── normalization.py     ← 分布归一化
└── requirements.txt
```

> 📖 Docs: [SciPy](https://docs.scipy.org/) / [NumPy](https://numpy.org/) / [SymPy](https://docs.sympy.org/)

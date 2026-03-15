---
topic: integration_summation
dimension: pitfalls
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📖 Docs: SciPy integrate — https://docs.scipy.org/doc/scipy/reference/integrate.html"
  - "📖 Docs: NumPy sum — https://numpy.org/doc/stable/reference/generated/numpy.sum.html"
  - "📚 Book: Bishop, PRML, Ch.11 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/bishop_prml.pdf"
  - "🧪 经验: 数值计算常见陷阱"
expiry: 6m
status: current
---

# 积分与求和 踩坑记录

> ⚠️ **这是知识库中最有价值的维度。** 每次踩坑后请追加条目。

---

## 坑 1: 浮点求和的精度丢失

**场景：** 对大量浮点数求和时，累加顺序影响结果精度

**症状：** 同一组数用不同方式求和得到不同结果，微小数值被大数"淹没"

**根因：** IEEE 754 浮点数有限精度。当累加器值很大而被加数很小时，小数的有效位被截断。例如 $10^{10} + 10^{-6}$ 在浮点运算中可能等于 $10^{10}$

**解法：**

❌ 错误写法 — 直接累加，大小数混合

```python
values = [1e10, 1.0, -1e10, 1.0]
result = sum(values)  # Python 内置 sum
print(result)  # 可能得到 0.0 而不是 2.0
```

✅ 正确写法 — 使用 math.fsum 或 Kahan 求和

```python
import math
import numpy as np

values = [1e10, 1.0, -1e10, 1.0]

# 方法 1: math.fsum（完整精度）/ Full precision sum
result = math.fsum(values)
print(result)  # 2.0 ✅

# 方法 2: NumPy（使用 pairwise summation）
result = np.sum(np.array(values))
print(result)  # 2.0 ✅

# 方法 3: 先排序再求和（从小到大）
result = sum(sorted(values, key=abs))
```

**教训：** 涉及大量浮点求和时，优先用 `np.sum` 或 `math.fsum`，避免 Python 内置 `sum`

> 📖 Docs: [math.fsum](https://docs.python.org/3/library/math.html#math.fsum)
> 🧪 经验: 数值计算常见陷阱

---

## 坑 2: 数值积分的 Warning 被忽略

**场景：** 使用 `scipy.integrate.quad` 积分含奇点或振荡函数

**症状：** `IntegrationWarning: The maximum number of subdivisions has been reached` 或结果明显不对

**根因：** `quad` 的默认子区间数 `limit=50` 不够，或函数在某些点不连续/振荡剧烈

**解法：**

❌ 错误写法 — 忽略 warning，直接使用结果

```python
from scipy.integrate import quad
import warnings
warnings.filterwarnings('ignore')  # 千万别这样
result, _ = quad(lambda x: 1/x**0.5, 0, 1)  # x=0 处有奇点
```

✅ 正确写法 — 增大 limit + 使用合适的积分方法

```python
from scipy.integrate import quad

# 方法 1: 增大 limit
result, error = quad(lambda x: 1/x**0.5, 0, 1, limit=200)
print(f"结果={result:.6f}, 误差={error:.2e}")  # 2.000000

# 方法 2: 对奇点使用 points 参数，或用 quad 的 weight 选项
# 方法 3: 手动拆分区间避开奇点
result1, _ = quad(lambda x: 1/x**0.5, 1e-10, 0.5)
result2, _ = quad(lambda x: 1/x**0.5, 0.5, 1)
result = result1 + result2
```

**教训：** 永远检查 `quad` 的第二个返回值（误差估计），不要忽略 IntegrationWarning

> 📖 Docs: [SciPy quad](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.quad.html)

---

## 坑 3: 蒙特卡洛积分不设随机种子导致不可复现

**场景：** MC 积分结果每次运行不同，调试和论文报告困难

**症状：** 同一段代码多次运行得到不同的积分估计值

**根因：** 蒙特卡洛方法基于随机采样，未固定种子则每次采样不同

**解法：**

❌ 错误写法 — 不设种子

```python
import numpy as np
samples = np.random.uniform(0, 1, 10000)
estimate = np.mean(np.exp(-samples**2))
print(estimate)  # 每次不同
```

✅ 正确写法 — 固定种子 + 使用 Generator

```python
import numpy as np

# 现代方法: 使用 Generator（推荐）
rng = np.random.default_rng(seed=42)
samples = rng.uniform(0, 1, 10000)
estimate = np.mean(np.exp(-samples**2))
print(estimate)  # 可复现

# 旧方法: np.random.seed（全局状态，不推荐）
# np.random.seed(42)
```

**教训：** 所有涉及随机性的数值实验必须设置种子；优先使用 `np.random.default_rng()`

> 📖 Docs: [NumPy Random Generator](https://numpy.org/doc/stable/reference/random/generator.html)
> 🧪 经验: 可复现性最佳实践

---

## 坑 4: 求和/积分顺序随意交换

**场景：** 推导 ML 公式时，随意交换 $\sum$ 与 $\int$ 的顺序

**症状：** 推导出的公式数值结果不对，或与文献不一致

**根因：** 积分与求和的交换并非总是合法。需要满足 Fubini 定理（绝对可积）或一致收敛等条件。典型反例：$\sum_{n=1}^{\infty} \int_0^1 f_n(x)\,dx \neq \int_0^1 \sum_{n=1}^{\infty} f_n(x)\,dx$ 当 $f_n$ 不满足条件时

**解法：**

❌ 错误写法 — 直接交换，没有检查条件

```python
# 数学推导中：
# "显然 Σ∫ = ∫Σ"  ← 不一定正确！
```

✅ 正确写法 — 验证交换条件

```python
# 在推导中明确检查：
# 1. Fubini 定理: ∫∫|f(x,y)|dxdy < ∞ → 可交换
# 2. 一致收敛: Σf_n 一致收敛 → 可逐项积分
# 3. Dominated Convergence: 存在可积上界 g(x) ≥ |f_n(x)| → 可交换

# 数值验证示例
import numpy as np
from scipy.integrate import quad

# 计算两种顺序的结果并比较
def verify_interchange():
    # 方式 1: 先求和再积分
    def sum_then_int():
        def summed(x, N=100):
            return sum(np.sin(n * x) / n**2 for n in range(1, N+1))
        return quad(summed, 0, np.pi)[0]

    # 方式 2: 先积分再求和
    def int_then_sum(N=100):
        return sum(quad(lambda x, n=n: np.sin(n * x) / n**2, 0, np.pi)[0]
                   for n in range(1, N+1))

    r1, r2 = sum_then_int(), int_then_sum()
    print(f"Σ∫ = {r1:.6f}, ∫Σ = {r2:.6f}, 差异 = {abs(r1-r2):.2e}")
```

**教训：** 交换积分/求和顺序前，必须验证数学条件；不确定时，用数值实验双向计算对比

> 📚 Book: 数学分析教材（Fubini 定理、一致收敛定理）
> 🧪 经验: ML 公式推导常见错误

---

## 坑 5: np.sum 轴向参数搞错

**场景：** 多维数组求和时 `axis` 参数理解错误

**症状：** 结果的 shape 不符合预期，或得到标量而非向量

**根因：** `axis=0` 是沿第一维（行方向）求和，结果消去行；`axis=1` 是沿第二维（列方向）求和，结果消去列。初学者常搞反

**解法：**

❌ 错误写法 — axis 搞反

```python
import numpy as np
A = np.array([[1, 2, 3],
              [4, 5, 6]])  # shape (2, 3)

# 想对每一行求和（横向），错用 axis=0
row_sum_wrong = np.sum(A, axis=0)  # [5, 7, 9] ← 这是列求和！
```

✅ 正确写法 — 记住"axis=k 消去第 k 维"

```python
import numpy as np
A = np.array([[1, 2, 3],
              [4, 5, 6]])  # shape (2, 3)

# axis=0: 消去第 0 维(行) → 结果 shape (3,)，即列求和
col_sum = np.sum(A, axis=0)  # [5, 7, 9]

# axis=1: 消去第 1 维(列) → 结果 shape (2,)，即行求和
row_sum = np.sum(A, axis=1)  # [6, 15]

# 记忆口诀: "axis=k 意味着第 k 维被压缩掉"
print(f"原 shape: {A.shape}")       # (2, 3)
print(f"axis=0 后: {col_sum.shape}")  # (3,) — 第 0 维被消去
print(f"axis=1 后: {row_sum.shape}")  # (2,) — 第 1 维被消去
```

**教训：** `axis=k` = "沿第 k 维压缩"；结果 shape 等于去掉原 shape 的第 k 维

> 📖 Docs: [NumPy sum axis](https://numpy.org/doc/stable/reference/generated/numpy.sum.html)
> 🧪 经验: NumPy 维度操作常见混淆

---

## 坑 6: 对数概率求和时溢出 (LogSumExp)

**场景：** 对概率取对数后需要求和再取指数（如 softmax、边缘化）

**症状：** `exp` 溢出得到 `inf`，或下溢得到 `0.0`，导致 `log(0) = -inf` 或 `nan`

**根因：** 直接计算 $\log(\sum_i e^{a_i})$ 时，如果 $a_i$ 很大则 $e^{a_i}$ 溢出，如果 $a_i$ 很小则 $e^{a_i}$ 下溢

**解法：**

❌ 错误写法 — 先 exp 求和再 log

```python
import numpy as np
logits = np.array([1000, 1001, 1002])
result = np.log(np.sum(np.exp(logits)))  # inf → nan
```

✅ 正确写法 — LogSumExp 技巧

```python
import numpy as np
from scipy.special import logsumexp

logits = np.array([1000, 1001, 1002])

# 方法 1: scipy.special.logsumexp（推荐）
result = logsumexp(logits)  # 正确结果

# 方法 2: 手动 LogSumExp
# log(Σ exp(a_i)) = max(a) + log(Σ exp(a_i - max(a)))
max_a = np.max(logits)
result = max_a + np.log(np.sum(np.exp(logits - max_a)))
print(f"LogSumExp = {result:.4f}")  # 1002.4076
```

**教训：** 任何涉及 $\log \sum \exp$ 的计算都必须使用 LogSumExp 技巧，这在 softmax、交叉熵损失中是标准做法

> 📖 Docs: [scipy.special.logsumexp](https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.logsumexp.html)
> 🧪 经验: 深度学习数值稳定性

---

## 调试清单

1. [ ] **求和结果异常？** → 检查浮点精度，改用 `np.sum` 或 `math.fsum`
2. [ ] **积分结果 Warning？** → 检查 `quad` 的误差返回值，增大 `limit` 参数
3. [ ] **MC 结果不可复现？** → 设置 `np.random.default_rng(seed=42)`
4. [ ] **推导公式不对？** → 检查是否非法交换了 $\sum$ 和 $\int$ 的顺序
5. [ ] **多维求和 shape 错误？** → 确认 `axis` 参数（axis=k 消去第 k 维）
6. [ ] **exp 溢出/下溢？** → 使用 `scipy.special.logsumexp`
7. [ ] **积分值为 0 或 inf？** → 检查被积函数是否有奇点、是否在正确区间
8. [ ] **MC 收敛太慢？** → 考虑重要性采样（Importance Sampling）降低方差
9. [ ] **二重积分太慢？** → 考虑是否可以解析地积掉一个维度
10. [ ] **级数不收敛？** → 检查收敛条件（比值判别法、根值判别法）

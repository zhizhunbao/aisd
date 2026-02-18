# %% [markdown]
"""
# 📐 线性代数可视化教程 / Linear Algebra Visual Tutorial

> **教学理念**: 先建立几何直觉，再学形式化定义，用图形验证。
>
> 每一节对应一个核心概念，配有 **交互式图形**。

**依赖**: `pip install numpy matplotlib`
"""

# %%
import numpy as np
import matplotlib.pyplot as plt

# 全局设置
plt.rcParams['figure.figsize'] = (8, 6)
plt.rcParams['font.size'] = 12
plt.rcParams['axes.grid'] = True


def draw_vector(ax, origin, vec, color='blue', label=None, lw=2):
    """在 ax 上画一个从 origin 出发的箭头向量"""
    ax.annotate('', xy=(origin[0] + vec[0], origin[1] + vec[1]),
                xytext=origin,
                arrowprops=dict(arrowstyle='->', color=color, lw=lw))
    if label:
        mid = (origin[0] + vec[0] / 2, origin[1] + vec[1] / 2)
        ax.text(mid[0] + 0.1, mid[1] + 0.1, label,
                fontsize=12, color=color, fontweight='bold')


def setup_axes(ax, xlim=(-1, 5), ylim=(-1, 5), title=''):
    """统一设置坐标轴"""
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_aspect('equal')
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.set_title(title, fontsize=14, fontweight='bold')


print('✅ 工具函数加载完成!')

# %% [markdown]
"""
---

## 1. 向量 Vectors

**直觉**: 向量 = 有方向和大小的箭头。`[3, 2]` = 「向右3步，向上2步」。

| 运算 | 公式 | 几何意义 |
|------|------|----------|
| 加法 | u + v | 首尾相连（平行四边形法则） |
| 缩放 | c·v | 拉伸/压缩箭头长度 |
| 点积 | u·v = u₁v₁ + u₂v₂ | 投影长度 × 被投影向量长度 |
"""

# %%
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# 1a: 向量 = 箭头
ax = axes[0]
setup_axes(ax, (-1, 5), (-1, 5), '向量 = 有方向的箭头')
draw_vector(ax, (0, 0), (3, 2), 'blue', 'v = [3,2]')
ax.plot(3, 2, 'bo', markersize=8)
ax.text(3.1, 2.1, '(3, 2)', fontsize=11)

# 1b: 向量加法 = 首尾相连
ax = axes[1]
setup_axes(ax, (-1, 6), (-1, 6), '向量加法 (首尾相连)')
u = np.array([3, 1])
v = np.array([1, 3])
draw_vector(ax, (0, 0), u, 'blue', 'u=[3,1]')
draw_vector(ax, u, v, 'red', 'v=[1,3]')
draw_vector(ax, (0, 0), u + v, 'purple', 'u+v=[4,4]', lw=3)
ax.plot([u[0], u[0]+v[0]], [u[1], u[1]+v[1]], 'r--', alpha=0.4)
ax.plot([v[0], u[0]+v[0]], [v[1], u[1]+v[1]], 'b--', alpha=0.4)
draw_vector(ax, (0, 0), v, 'red', '', lw=1)

# 1c: 标量乘法 = 缩放
ax = axes[2]
setup_axes(ax, (-4, 7), (-3, 5), '标量乘法 (缩放)')
v = np.array([2, 1])
draw_vector(ax, (0, 0), v, 'blue', 'v', lw=2)
draw_vector(ax, (0, 0), 2*v, 'green', '2v', lw=2)
draw_vector(ax, (0, 0), -1.5*v, 'red', '-1.5v', lw=2)

plt.suptitle('第1章: 向量 Vectors', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()

# %%
# 数值验证
u = np.array([3, 2])
v = np.array([1, 4])
print('加法:', u + v)                    # [4, 6]
print('缩放:', 2 * u)                    # [6, 4]
print('点积:', np.dot(u, v))             # 11
print('模:',  np.linalg.norm(u))         # ≈ 3.61

# %% [markdown]
"""
---

## 2. 张成空间 Span

**直觉**: 线性组合 = 缩放 + 相加。Span = 所有可能的线性组合能到达的点的集合。

- 2个**不共线**向量 → Span = 整个 R² 平面
- 2个**共线**向量 → Span = 一条直线
"""

# %%
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# 2a: 不共线 → Span = R²
ax = axes[0]
setup_axes(ax, (-4, 4), (-4, 4), 'Span{v₁,v₂} = R² (不共线)')
v1 = np.array([1, 0.5])
v2 = np.array([-0.5, 1])
cs = np.linspace(-3, 3, 15)
for c1 in cs:
    for c2 in cs:
        p = c1 * v1 + c2 * v2
        ax.plot(p[0], p[1], 'c.', markersize=3, alpha=0.5)
draw_vector(ax, (0, 0), v1*2, 'blue', 'v₁', lw=3)
draw_vector(ax, (0, 0), v2*2, 'red', 'v₂', lw=3)

# 2b: 共线 → Span = 直线
ax = axes[1]
setup_axes(ax, (-4, 4), (-4, 4), 'Span{v₁,v₂} = 直线 (共线)')
v1 = np.array([1, 2])
v2 = np.array([2, 4])  # = 2 * v1
t = np.linspace(-2, 2, 100)
ax.plot(t*v1[0], t*v1[1], 'c-', lw=8, alpha=0.3, label='Span (一条线)')
draw_vector(ax, (0, 0), v1, 'blue', 'v₁=[1,2]', lw=3)
draw_vector(ax, (0, 0), v2, 'red', 'v₂=[2,4]=2v₁', lw=3)
ax.legend(fontsize=11)

plt.suptitle('第2章: 张成空间 Span', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()

# %% [markdown]
"""
---

## 3. 线性无关与基 Linear Independence & Basis

**直觉**:
- **线性无关** = 没有一个向量是「多余的」
- **基 (Basis)** = 一组线性无关的向量，能张成整个空间
- 检验方法: det ≠ 0 → 线性无关
"""

# %%
# 线性无关 vs 相关
v1 = np.array([1, 2])
v2 = np.array([3, 4])
A = np.column_stack([v1, v2])
print(f'v1={v1}, v2={v2}')
print(f'det = {np.linalg.det(A):.1f}  → 线性无关 ✓')

print()
v3 = np.array([2, 4])  # = 2 * v1
B = np.column_stack([v1, v3])
print(f'v1={v1}, v3={v3} (= 2·v1)')
print(f'det = {np.linalg.det(B):.1f}  → 线性相关 ✗')

# %% [markdown]
"""
---

## 4. 矩阵 = 线性变换 (⭐ 最重要的直觉!)

**矩阵不只是数字表格——它是一个空间变换！**

- 矩阵的**第 1 列** = 基向量 e₁ 变换后的去向
- 矩阵的**第 2 列** = 基向量 e₂ 变换后的去向

下面展示 6 种经典变换对单位正方形的效果：
"""

# %%
fig, axes = plt.subplots(2, 3, figsize=(18, 11))

transforms = [
    ('单位矩阵 I\n(不变)', np.eye(2)),
    ('水平拉伸 2x\n[[2,0],[0,1]]', np.array([[2,0],[0,1]])),
    ('旋转 45°', np.array([
        [np.cos(np.pi/4), -np.sin(np.pi/4)],
        [np.sin(np.pi/4),  np.cos(np.pi/4)]
    ])),
    ('剪切\n[[1,1],[0,1]]', np.array([[1,1],[0,1]])),
    ('反射 (y轴)\n[[-1,0],[0,1]]', np.array([[-1,0],[0,1]])),
    ('压缩到线\n[[1,2],[0.5,1]]', np.array([[1,2],[0.5,1]])),
]

square = np.array([[0,0],[1,0],[1,1],[0,1],[0,0]]).T
gx, gy = np.meshgrid(np.linspace(-0.5,1.5,8), np.linspace(-0.5,1.5,8))
grid = np.vstack([gx.ravel(), gy.ravel()])

for idx, (title, M) in enumerate(transforms):
    ax = axes[idx//3][idx%3]
    setup_axes(ax, (-3,3), (-3,3), title)

    # 变换前
    ax.plot(square[0], square[1], 'b--', alpha=0.4, lw=1, label='变换前')
    ax.plot(grid[0], grid[1], 'b.', alpha=0.2, markersize=2)

    # 变换后
    new_sq = M @ square
    new_grid = M @ grid
    ax.fill(new_sq[0], new_sq[1], alpha=0.3, color='red')
    ax.plot(new_sq[0], new_sq[1], 'r-', lw=2, label='变换后')
    ax.plot(new_grid[0], new_grid[1], 'r.', alpha=0.4, markersize=3)

    # 基向量变换
    draw_vector(ax, (0,0), M[:,0], 'green', '', lw=2)
    draw_vector(ax, (0,0), M[:,1], 'orange', '', lw=2)

    det = np.linalg.det(M)
    ax.text(-2.8, -2.5, f'det={det:.2f}', fontsize=11, color='darkred',
            bbox=dict(boxstyle='round', facecolor='wheat'))
    ax.legend(fontsize=9, loc='upper left')

plt.suptitle('第4章: 矩阵 = 线性变换\n(绿=变换后e₁, 橙=变换后e₂)',
             fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()

# %% [markdown]
"""
### ⚠️ 注意: 矩阵乘法不满足交换律！AB ≠ BA
"""

# %%
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
print('AB =\n', A @ B)
print('BA =\n', B @ A)
print('AB == BA?', np.allclose(A @ B, B @ A))  # False!
print()
print('(AB)^T == B^T A^T?', np.allclose((A@B).T, B.T @ A.T))  # True

# %% [markdown]
"""
---

## 5. 线性方程组 & 高斯消元

**直觉**: Ax = b → 「什么输入经过变换A后得到b？」

三种几何情况：
"""

# %%
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

cases = [
    ('唯一解 (两线相交)', 1, 2, 5, 3, -1, 1),
    ('无穷多解 (两线重合)', 1, 2, 4, 2, 4, 8),
    ('无解 (两线平行)', 1, 2, 4, 1, 2, 6),
]

for idx, (title, a1, b1, c1, a2, b2, c2) in enumerate(cases):
    ax = axes[idx]
    setup_axes(ax, (-2, 6), (-2, 6), title)
    x_range = np.linspace(-2, 6, 100)

    if b1 != 0:
        ax.plot(x_range, (c1 - a1*x_range)/b1, 'b-', lw=2,
                label=f'{a1}x + {b1}y = {c1}')
    if b2 != 0:
        ax.plot(x_range, (c2 - a2*x_range)/b2, 'r-', lw=2,
                label=f'{a2}x + {b2}y = {c2}')

    if idx == 0:  # 唯一解
        A = np.array([[a1,b1],[a2,b2]])
        sol = np.linalg.solve(A, [c1,c2])
        ax.plot(sol[0], sol[1], 'ko', markersize=12, zorder=5)
        ax.text(sol[0]+0.2, sol[1]+0.2, f'({sol[0]:.1f}, {sol[1]:.1f})',
                fontsize=12, fontweight='bold')
    ax.legend(fontsize=11)

plt.suptitle('第5章: 线性方程组的几何意义', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()

# %%
# 高斯消元数值验证
A = np.array([[1, 2, 3], [2, 5, 7], [3, 6, 10]])
b = np.array([9, 22, 29])
x = np.linalg.solve(A, b)
print('解 x =', x)              # [-1, 2, 2]
print('验证 Ax=b:', np.allclose(A @ x, b))  # True

# %% [markdown]
"""
---

## 6. 行列式 Determinant

**直觉**: 行列式 = 变换后面积/体积的缩放因子。
- det > 0: 保持方向
- det < 0: 翻转方向
- det = 0: 空间被压扁，**不可逆！**
"""

# %%
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

cases = [
    ('det > 0: 面积放大', np.array([[2,0],[0,1.5]]), 'green'),
    ('det < 0: 翻转', np.array([[1,0],[0,-1]]), 'orange'),
    ('det = 0: 压扁!', np.array([[1,2],[0.5,1]]), 'red'),
]

square = np.array([[0,0],[1,0],[1,1],[0,1],[0,0]]).T

for idx, (title, M, color) in enumerate(cases):
    ax = axes[idx]
    setup_axes(ax, (-2, 4), (-2, 4), title)

    ax.fill(square[0], square[1], alpha=0.2, color='blue')
    ax.plot(square[0], square[1], 'b-', lw=1, label='原始 (面积=1)')

    new_sq = M @ square
    det = np.linalg.det(M)
    ax.fill(new_sq[0], new_sq[1], alpha=0.3, color=color)
    ax.plot(new_sq[0], new_sq[1], '-', color=color, lw=2,
            label=f'变换后 (面积={abs(det):.1f})')

    ax.text(0.5, -1.5, f'det(A) = {det:.2f}', fontsize=14,
            fontweight='bold', color='darkred', ha='center',
            bbox=dict(boxstyle='round', facecolor='lightyellow'))
    ax.legend(fontsize=10)

plt.suptitle('第6章: 行列式 = 面积的缩放因子', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()

# %% [markdown]
"""
---

## 7. 逆矩阵 Inverse

**直觉**: 逆矩阵 = 撤销操作（Ctrl+Z）。A·A⁻¹ = I
"""

# %%
A = np.array([[3, 1], [2, 1]])
A_inv = np.linalg.inv(A)

print('A =')
print(A)
print('\nA⁻¹ =')
print(A_inv)
print('\nA × A⁻¹ =')
print(np.round(A @ A_inv))
print('\n用逆矩阵解方程 Ax=b:')
b = np.array([5, 3])
print(f'b = {b}')
print(f'x = A⁻¹b = {A_inv @ b}')

# %% [markdown]
"""
---

## 8. 向量空间 & 子空间

**四个重要子空间：**
- **Column Space** C(A): 变换能到达的所有输出
- **Null Space** N(A): 被「压扁」到原点的所有输入
- **Rank（秩）** = Column Space 的维度
"""

# %%
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

A = np.array([[1, 2], [2, 4], [3, 6]])

# Column Space
ax = axes[0]
ax.set_xlim(-4, 8); ax.set_ylim(-8, 16)
ax.set_title('Column Space of A\n(A能到达的所有输出)',
             fontsize=13, fontweight='bold')
col1 = A[:, 0]; col2 = A[:, 1]
t = np.linspace(-2, 3, 100)
ax.plot(t*col1[0], t*col1[1], 'b-', lw=4, alpha=0.3,
        label='Column Space (一条线)')
draw_vector(ax, (0,0), (col1[0], col1[1]), 'blue', f'col₁={col1[:2]}', lw=3)
draw_vector(ax, (0,0), (col2[0], col2[1]), 'red', f'col₂={col2[:2]}=2·col₁', lw=3)
ax.text(-3.5, 13, f'A = [[1,2],[2,4],[3,6]]\nrank={np.linalg.matrix_rank(A)}\ncol₂ = 2·col₁ → 线性相关!',
        fontsize=11, bbox=dict(boxstyle='round', facecolor='lightyellow'))
ax.legend(fontsize=11); ax.grid(True)
ax.set_xlabel('x₁'); ax.set_ylabel('x₂')

# Null Space
ax = axes[1]
setup_axes(ax, (-4, 4), (-4, 4), 'Null Space of A\n(Ax=0 的所有解)')
null_vec = np.array([-2, 1])
t = np.linspace(-3, 3, 100)
ax.plot(t*null_vec[0], t*null_vec[1], 'r-', lw=4, alpha=0.3,
        label='Null Space (一条线)')
draw_vector(ax, (0,0), null_vec, 'red', 'n=[-2,1]', lw=3)
ax.text(-3.5, 3, 'Ax = 0 的解:\nx₁ = -2x₂\n即 x = t[-2, 1]',
        fontsize=11, bbox=dict(boxstyle='round', facecolor='lightyellow'))
ax.set_xlabel('x₁'); ax.set_ylabel('x₂'); ax.legend(fontsize=11)

plt.suptitle('第8章: Column Space & Null Space',
             fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()

# %% [markdown]
"""
---

## 9. 特征值与特征向量 ⭐

**直觉**: 大多数向量变换后方向改变，但**特征向量**方向不变，只被拉伸。

$$Av = \\lambda v$$

- v = 特征向量（方向不变）
- λ = 特征值（拉伸倍数）
"""

# %%
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

A = np.array([[2, 1], [1, 2]])
eigenvalues, eigenvectors = np.linalg.eig(A)
print(f'A = {A.tolist()}')
print(f'特征值: λ₁={eigenvalues[0]:.1f}, λ₂={eigenvalues[1]:.1f}')

# 左图: 普通向量 vs 特征向量
ax = axes[0]
setup_axes(ax, (-4,5), (-4,5),
           f'A=[[2,1],[1,2]]  λ₁={eigenvalues[0]:.1f}, λ₂={eigenvalues[1]:.1f}')
angles = np.linspace(0, 2*np.pi, 12, endpoint=False)
for ang in angles:
    v = np.array([np.cos(ang), np.sin(ang)])
    Av = A @ v
    ax.plot([0,v[0]], [0,v[1]], 'b-', alpha=0.3, lw=1)
    ax.plot([0,Av[0]], [0,Av[1]], 'r-', alpha=0.3, lw=1)
for i in range(2):
    ev = eigenvectors[:, i]; lam = eigenvalues[i]
    draw_vector(ax, (0,0), ev*1.5, 'blue', f'v{i+1}', lw=3)
    draw_vector(ax, (0,0), A@(ev*1.5), 'red', f'Av{i+1}={lam:.0f}·v{i+1}', lw=3)
ax.plot([],[], 'b-', lw=2, label='变换前')
ax.plot([],[], 'r-', lw=2, label='变换后 (Av)')
ax.legend(fontsize=11)

# 右图: 单位圆 → 椭圆
ax = axes[1]
setup_axes(ax, (-4,4), (-4,4), '特征向量: 只缩放, 不改变方向!')
theta = np.linspace(0, 2*np.pi, 100)
circle = np.array([np.cos(theta), np.sin(theta)])
ellipse = A @ circle
ax.plot(circle[0], circle[1], 'b-', lw=2, label='单位圆 (变换前)', alpha=0.5)
ax.plot(ellipse[0], ellipse[1], 'r-', lw=2, label='变换后 (椭圆)')
for i in range(2):
    ev = eigenvectors[:,i]; lam = eigenvalues[i]
    ax.plot([-ev[0]*4, ev[0]*4], [-ev[1]*4, ev[1]*4], '--',
            color=['green','purple'][i], lw=2, alpha=0.7,
            label=f'特征方向 λ={lam:.1f}')
ax.legend(fontsize=10)

plt.suptitle('第9章: 特征值与特征向量', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()

# %%
# 数值验证: Av = λv
for i in range(2):
    v = eigenvectors[:, i]
    lam = eigenvalues[i]
    print(f'v{i+1} = {v}')
    print(f'  Av  = {A @ v}')
    print(f'  λv  = {lam * v}')
    print(f'  相等? {np.allclose(A @ v, lam * v)}\n')

# %% [markdown]
"""
---

## 10. 正交投影 Projection

**直觉**: 投影 = 影子。把 b 投影到 a 上。

$$\\text{proj}_a(b) = \\frac{a \\cdot b}{a \\cdot a} a$$

误差 (b - proj) 与 a **垂直**！
"""

# %%
fig, ax = plt.subplots(1, 1, figsize=(8, 8))
setup_axes(ax, (-1, 6), (-1, 6), '向量投影 = 影子')

a = np.array([4, 1])
b = np.array([2, 4])

proj = (np.dot(a, b) / np.dot(a, a)) * a
error = b - proj

# a 方向延长线
t = np.linspace(-0.5, 1.5, 100)
ax.plot(t*a[0], t*a[1], 'b--', alpha=0.3, lw=1)

draw_vector(ax, (0,0), a, 'blue', 'a=[4,1]', lw=3)
draw_vector(ax, (0,0), b, 'green', 'b=[2,4]', lw=3)
draw_vector(ax, (0,0), proj, 'red', f'proj={proj[0]:.1f},{proj[1]:.1f}', lw=3)

ax.plot([proj[0], b[0]], [proj[1], b[1]],
        'orange', lw=2, linestyle='--', label='误差 (⊥a)')

# 直角标记
sc = 0.3
pd = error / np.linalg.norm(error)
ad = a / np.linalg.norm(a)
c1 = proj + sc*pd; c2 = proj + sc*pd + sc*ad; c3 = proj + sc*ad
ax.plot([c1[0],c2[0],c3[0]], [c1[1],c2[1],c3[1]], 'k-', lw=1.5)

dot_check = np.dot(a, error)
ax.text(1, 5, f'a · 误差 = {dot_check:.6f} ≈ 0  ✓',
        fontsize=13, color='darkred',
        bbox=dict(boxstyle='round', facecolor='lightyellow'))
ax.legend(fontsize=12)

plt.suptitle('第10章: 正交投影', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()

# %% [markdown]
"""
---

## 11. 最小二乘法 Least Squares

**直觉**: 方程组无精确解时（数据有噪音），找「最接近的」解 → **线性回归**！

$$\\hat{x} = (A^TA)^{-1}A^Tb$$
"""

# %%
fig, ax = plt.subplots(1, 1, figsize=(9, 7))

np.random.seed(42)
x = np.linspace(0, 10, 20)
y_true = 2.5 * x + 3
y = y_true + np.random.normal(0, 3, len(x))

A = np.column_stack([x, np.ones(len(x))])
x_hat = np.linalg.lstsq(A, y, rcond=None)[0]
m, c = x_hat

ax.scatter(x, y, s=80, c='blue', zorder=3, label='数据点')
ax.plot(x, y_true, 'g--', lw=2, alpha=0.5, label='真实: y = 2.5x + 3')

y_fit = A @ x_hat
ax.plot(x, y_fit, 'r-', lw=3, label=f'拟合: y = {m:.2f}x + {c:.2f}')

for i in range(len(x)):
    ax.plot([x[i], x[i]], [y[i], y_fit[i]], 'orange', lw=1, alpha=0.5)

ax.set_xlabel('x', fontsize=13)
ax.set_ylabel('y', fontsize=13)
ax.set_title('最小二乘法: 找最佳拟合直线\n(最小化橙色线段长度的平方和)',
             fontsize=14, fontweight='bold')
ax.legend(fontsize=12)
ax.text(0.5, max(y)-2, r'$\hat{x} = (A^TA)^{-1}A^Tb$',
        fontsize=14, color='darkred',
        bbox=dict(boxstyle='round', facecolor='lightyellow'))
plt.tight_layout()
plt.show()

# %% [markdown]
"""
---

## 12. 奇异值分解 SVD

**直觉**: 任何矩阵 = 旋转 → 缩放 → 旋转

$$A = U \\Sigma V^T$$

**应用**: 图像压缩 — 只保留前 k 个最大的奇异值
"""

# %%
# 创建测试图像
n = 100
img = np.zeros((n, n))
for i in range(n):
    for j in range(n):
        img[i, j] = 0.3 * (i + j) / (2 * n)
cx, cy, r = 50, 50, 25
for i in range(n):
    for j in range(n):
        if (i-cx)**2 + (j-cy)**2 < r**2:
            img[i, j] += 0.5
img[20:40, 60:90] = 0.8

U, s, Vt = np.linalg.svd(img, full_matrices=False)

fig, axes = plt.subplots(2, 3, figsize=(16, 10))
ranks = [1, 3, 5, 10, 30, 100]

for idx, k in enumerate(ranks):
    ax = axes[idx//3][idx%3]
    img_k = U[:,:k] @ np.diag(s[:k]) @ Vt[:k,:]
    ax.imshow(img_k, cmap='viridis', vmin=0, vmax=1)
    ax.set_title(f'秩 k={k}\n存储: {k*(n+n+1)} ({100*k*(n+n+1)/(n*n):.0f}%)',
                 fontsize=12)
    ax.axis('off')
    err = np.linalg.norm(img - img_k) / np.linalg.norm(img)
    ax.text(5, n-8, f'误差: {err:.4f}', fontsize=10, color='white',
            bbox=dict(boxstyle='round', facecolor='black', alpha=0.6))

plt.suptitle('第12章: SVD 低秩近似 (图像压缩)\n用更少的数据重建原始图像',
             fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()

# %%
# 奇异值衰减图
fig, ax = plt.subplots(figsize=(8, 5))
ax.semilogy(s, 'b.-', lw=2, markersize=5)
ax.set_xlabel('Index', fontsize=13)
ax.set_ylabel('Singular Value (log scale)', fontsize=13)
ax.set_title('奇异值衰减图\n(前几个值最重要，后面的可以丢弃!)',
             fontsize=14, fontweight='bold')
ax.axhline(s[5], color='r', linestyle='--', alpha=0.5,
           label=f'k=5 截断线 (σ={s[5]:.2f})')
ax.legend(fontsize=12)
plt.tight_layout()
plt.show()

print(f'\n前5个奇异值占总能量的 {100*np.sum(s[:5]**2)/np.sum(s**2):.1f}%')

# %% [markdown]
"""
---

## 📊 概念关系总结

```
向量 (Vectors)
  ↓
线性组合 → Span → 线性无关 → 基 (Basis)
  ↓                              ↓
矩阵 = 线性变换                  维度
  ↓        ↓
行列式    逆矩阵 ←→ 线性方程组 (Ax=b)
  ↓
特征值/特征向量 → 对角化
  ↓
正交性 → 投影 → 最小二乘
  ↓
SVD（集大成者）
```

> 💡 线性代数的核心思想：**一切都是关于空间和变换的。**
> 矩阵是变换的语言，向量是变换的对象，行列式衡量变换的效果，特征值揭示变换的本质。
"""

"""
SVM 完整演示脚本 - 基于 02_SVM_notes.md
目标：从零开始展示 SVM 的所有核心概念，不留任何"凭空出现"的数字

作者：AI Assistant
日期：2026-01-29
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.datasets import make_blobs, make_circles
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体（如果需要）
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

print("=" * 80)
print("SVM 完整演示 - 从数据生成到模型训练")
print("=" * 80)


# ============================================================================
# 第1部分：线性可分数据 + 硬间隔 SVM (MMC - Maximum Margin Classifier)
# ============================================================================
print("\n" + "=" * 80)
print("第1部分：线性可分数据 + 硬间隔 SVM (MMC)")
print("=" * 80)

# 1.1 生成线性可分的数据
np.random.seed(42)
X_linear, y_linear = make_blobs(n_samples=100, centers=2, n_features=2, 
                                 center_box=(-5, 5), cluster_std=1.0, random_state=42)

# 转换标签为 -1 和 +1（符合 SVM 理论）
y_linear = np.where(y_linear == 0, -1, 1)

print(f"\n生成的数据：")
print(f"  样本数量: {len(X_linear)}")
print(f"  特征维度: {X_linear.shape[1]}")
print(f"  类别分布: {np.bincount(y_linear + 1)}")  # [负类数, 正类数]
print(f"\n前5个样本:")
for i in range(5):
    print(f"  x{i+1} = {X_linear[i]}, y{i+1} = {y_linear[i]:+d}")

# 1.2 训练硬间隔 SVM（C 很大，接近无穷）
print("\n" + "-" * 80)
print("训练硬间隔 SVM (C=1000，接近无穷大，不允许误分类)")
print("-" * 80)

svm_hard = SVC(kernel='linear', C=1000.0)  # C 很大 = 硬间隔
svm_hard.fit(X_linear, y_linear)

# 1.3 提取训练后的参数（这就是 w 和 b 的来源！）
w_hard = svm_hard.coef_[0]
b_hard = svm_hard.intercept_[0]

print(f"\n训练完成！得到的参数：")
print(f"  权重向量 w = {w_hard}")
print(f"  偏置 b = {b_hard:.4f}")
print(f"  ||w|| = {np.linalg.norm(w_hard):.4f}")
print(f"  间隔 margin = 2/||w|| = {2/np.linalg.norm(w_hard):.4f}")

# 1.4 找出支持向量
support_vectors = svm_hard.support_vectors_
support_indices = svm_hard.support_
print(f"\n支持向量：")
print(f"  数量: {len(support_vectors)}")
print(f"  索引: {support_indices}")
for i, sv in enumerate(support_vectors):
    sv_label = y_linear[support_indices[i]]
    decision_value = np.dot(w_hard, sv) + b_hard
    print(f"  SV{i+1}: {sv}, 标签={sv_label:+d}, f(x)={decision_value:.4f}")

# 1.5 手动验证决策函数
print("\n" + "-" * 80)
print("手动验证决策函数 f(x) = w·x + b")
print("-" * 80)

test_points = [
    X_linear[0],   # 第一个样本
    X_linear[50],  # 第51个样本
    np.array([0, 0])  # 原点
]

for i, x_test in enumerate(test_points):
    # 手动计算
    f_manual = np.dot(w_hard, x_test) + b_hard
    # sklearn 预测
    f_sklearn = svm_hard.decision_function([x_test])[0]
    y_pred = svm_hard.predict([x_test])[0]
    
    print(f"\n测试点 {i+1}: x = {x_test}")
    print(f"  手动计算: f(x) = {w_hard[0]:.4f}×{x_test[0]:.4f} + {w_hard[1]:.4f}×{x_test[1]:.4f} + {b_hard:.4f}")
    print(f"           = {f_manual:.4f}")
    print(f"  sklearn: f(x) = {f_sklearn:.4f}")
    print(f"  预测类别: {y_pred:+d} ({'正类' if y_pred > 0 else '负类'})")

# 1.6 可视化
print("\n生成可视化图表...")
fig, ax = plt.subplots(1, 1, figsize=(10, 8))

# 绘制数据点
ax.scatter(X_linear[y_linear == -1, 0], X_linear[y_linear == -1, 1], 
           c='red', marker='o', s=100, label='负类 (y=-1)', edgecolors='k')
ax.scatter(X_linear[y_linear == 1, 0], X_linear[y_linear == 1, 1], 
           c='blue', marker='s', s=100, label='正类 (y=+1)', edgecolors='k')

# 绘制支持向量（用圆圈标记）
ax.scatter(support_vectors[:, 0], support_vectors[:, 1], 
           s=300, facecolors='none', edgecolors='green', linewidths=3, 
           label='支持向量')

# 绘制决策边界和间隔边界
x_min, x_max = X_linear[:, 0].min() - 1, X_linear[:, 0].max() + 1
y_min, y_max = X_linear[:, 1].min() - 1, X_linear[:, 1].max() + 1
xx, yy = np.meshgrid(np.linspace(x_min, x_max, 200), 
                     np.linspace(y_min, y_max, 200))
Z = svm_hard.decision_function(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

# 决策边界 (f(x) = 0)
ax.contour(xx, yy, Z, levels=[0], colors='black', linewidths=2, linestyles='-')
# 间隔边界 (f(x) = ±1)
ax.contour(xx, yy, Z, levels=[-1, 1], colors='black', linewidths=1, linestyles='--')

ax.set_xlabel('特征 x₁', fontsize=12)
ax.set_ylabel('特征 x₂', fontsize=12)
ax.set_title(f'硬间隔 SVM (MMC)\nw={w_hard}, b={b_hard:.4f}, margin={2/np.linalg.norm(w_hard):.4f}', 
             fontsize=14)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('svm_demo_1_hard_margin.png', dpi=150, bbox_inches='tight')
print("  保存图表: svm_demo_1_hard_margin.png")


# ============================================================================
# 第2部分：线性可分数据 + 软间隔 SVM (SVC - Support Vector Classifier)
# ============================================================================
print("\n" + "=" * 80)
print("第2部分：软间隔 SVM (SVC) - 对比不同的 C 值")
print("=" * 80)

# 2.1 添加一些噪声点（制造轻微重叠）
np.random.seed(123)
noise_points = np.random.randn(10, 2) * 0.5
noise_labels = np.random.choice([-1, 1], 10)
X_noisy = np.vstack([X_linear, noise_points])
y_noisy = np.hstack([y_linear, noise_labels])

print(f"\n添加噪声后的数据：")
print(f"  总样本数: {len(X_noisy)}")
print(f"  类别分布: {np.bincount(y_noisy + 1)}")

# 2.2 训练不同 C 值的 SVM
C_values = [0.01, 1.0, 1000.0]
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

for idx, C in enumerate(C_values):
    print(f"\n" + "-" * 80)
    print(f"训练 SVM with C={C}")
    print("-" * 80)
    
    svm = SVC(kernel='linear', C=C)
    svm.fit(X_noisy, y_noisy)
    
    w = svm.coef_[0]
    b = svm.intercept_[0]
    margin = 2 / np.linalg.norm(w)
    n_support = len(svm.support_vectors_)
    
    print(f"  w = {w}")
    print(f"  b = {b:.4f}")
    print(f"  间隔 = {margin:.4f}")
    print(f"  支持向量数量 = {n_support}")
    
    # 可视化
    ax = axes[idx]
    ax.scatter(X_noisy[y_noisy == -1, 0], X_noisy[y_noisy == -1, 1], 
               c='red', marker='o', s=80, label='负类', edgecolors='k', alpha=0.7)
    ax.scatter(X_noisy[y_noisy == 1, 0], X_noisy[y_noisy == 1, 1], 
               c='blue', marker='s', s=80, label='正类', edgecolors='k', alpha=0.7)
    ax.scatter(svm.support_vectors_[:, 0], svm.support_vectors_[:, 1], 
               s=250, facecolors='none', edgecolors='green', linewidths=2.5, 
               label='支持向量')
    
    x_min, x_max = X_noisy[:, 0].min() - 1, X_noisy[:, 0].max() + 1
    y_min, y_max = X_noisy[:, 1].min() - 1, X_noisy[:, 1].max() + 1
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 200), 
                         np.linspace(y_min, y_max, 200))
    Z = svm.decision_function(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    
    ax.contour(xx, yy, Z, levels=[0], colors='black', linewidths=2)
    ax.contour(xx, yy, Z, levels=[-1, 1], colors='black', linewidths=1, linestyles='--')
    
    ax.set_xlabel('特征 x₁', fontsize=11)
    ax.set_ylabel('特征 x₂', fontsize=11)
    
    if C < 1:
        c_desc = f"C={C} (小C，宽间隔)"
    elif C == 1:
        c_desc = f"C={C} (默认)"
    else:
        c_desc = f"C={C} (大C，窄间隔)"
    
    ax.set_title(f'{c_desc}\nmargin={margin:.3f}, SVs={n_support}', fontsize=12)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('svm_demo_2_soft_margin.png', dpi=150, bbox_inches='tight')
print("\n保存图表: svm_demo_2_soft_margin.png")


# ============================================================================
# 第3部分：非线性数据 + 核函数 (Kernel SVM)
# ============================================================================
print("\n" + "=" * 80)
print("第3部分：非线性数据 + 核函数对比")
print("=" * 80)

# 3.1 生成非线性可分数据（同心圆）
np.random.seed(42)
X_circles, y_circles = make_circles(n_samples=200, factor=0.5, noise=0.1, random_state=42)
y_circles = np.where(y_circles == 0, -1, 1)

print(f"\n生成的非线性数据（同心圆）：")
print(f"  样本数量: {len(X_circles)}")
print(f"  类别分布: {np.bincount(y_circles + 1)}")

# 3.2 对比不同核函数
kernels = [
    ('linear', '线性核'),
    ('poly', '多项式核 (degree=3)'),
    ('rbf', 'RBF核 (高斯核)')
]

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

for idx, (kernel, kernel_name) in enumerate(kernels):
    print(f"\n" + "-" * 80)
    print(f"训练 SVM with kernel='{kernel}'")
    print("-" * 80)
    
    if kernel == 'poly':
        svm = SVC(kernel=kernel, degree=3, C=1.0, gamma='auto')
    else:
        svm = SVC(kernel=kernel, C=1.0, gamma='auto')
    
    svm.fit(X_circles, y_circles)
    
    # 计算准确率
    y_pred = svm.predict(X_circles)
    accuracy = accuracy_score(y_circles, y_pred)
    n_support = len(svm.support_vectors_)
    
    print(f"  训练准确率: {accuracy:.4f}")
    print(f"  支持向量数量: {n_support}")
    
    # 可视化
    ax = axes[idx]
    ax.scatter(X_circles[y_circles == -1, 0], X_circles[y_circles == -1, 1], 
               c='red', marker='o', s=50, label='负类', edgecolors='k', alpha=0.6)
    ax.scatter(X_circles[y_circles == 1, 0], X_circles[y_circles == 1, 1], 
               c='blue', marker='s', s=50, label='正类', edgecolors='k', alpha=0.6)
    ax.scatter(svm.support_vectors_[:, 0], svm.support_vectors_[:, 1], 
               s=200, facecolors='none', edgecolors='green', linewidths=2, 
               label='支持向量')
    
    # 绘制决策边界
    x_min, x_max = X_circles[:, 0].min() - 0.5, X_circles[:, 0].max() + 0.5
    y_min, y_max = X_circles[:, 1].min() - 0.5, X_circles[:, 1].max() + 0.5
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 200), 
                         np.linspace(y_min, y_max, 200))
    Z = svm.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    
    ax.contourf(xx, yy, Z, alpha=0.2, levels=[-1, 0, 1], colors=['red', 'blue'])
    ax.contour(xx, yy, Z, levels=[0], colors='black', linewidths=2)
    
    ax.set_xlabel('特征 x₁', fontsize=11)
    ax.set_ylabel('特征 x₂', fontsize=11)
    ax.set_title(f'{kernel_name}\n准确率={accuracy:.3f}, SVs={n_support}', fontsize=12)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('svm_demo_3_kernels.png', dpi=150, bbox_inches='tight')
print("\n保存图表: svm_demo_3_kernels.png")


# ============================================================================
# 第4部分：核函数的数学原理演示
# ============================================================================
print("\n" + "=" * 80)
print("第4部分：核函数的数学计算演示")
print("=" * 80)

# 4.1 定义两个测试点
x1 = np.array([1.0, 2.0])
x2 = np.array([3.0, 1.0])

print(f"\n测试点:")
print(f"  x1 = {x1}")
print(f"  x2 = {x2}")

# 4.2 线性核
print(f"\n" + "-" * 80)
print("1. 线性核 (Linear Kernel)")
print("-" * 80)
print("公式: K(x1, x2) = x1 · x2")

K_linear = np.dot(x1, x2)
print(f"\n计算过程:")
print(f"  K(x1, x2) = {x1[0]}×{x2[0]} + {x1[1]}×{x2[1]}")
print(f"            = {x1[0]*x2[0]} + {x1[1]*x2[1]}")
print(f"            = {K_linear}")

# 4.3 多项式核
print(f"\n" + "-" * 80)
print("2. 多项式核 (Polynomial Kernel)")
print("-" * 80)
print("公式: K(x1, x2) = (γ × x1·x2 + r)^d")

gamma = 0.5
r = 0
degree = 3

dot_product = np.dot(x1, x2)
K_poly = (gamma * dot_product + r) ** degree

print(f"\n参数: γ={gamma}, r={r}, d={degree}")
print(f"计算过程:")
print(f"  x1·x2 = {dot_product}")
print(f"  K(x1, x2) = ({gamma} × {dot_product} + {r})^{degree}")
print(f"            = ({gamma * dot_product})^{degree}")
print(f"            = {K_poly}")

# 4.4 RBF核
print(f"\n" + "-" * 80)
print("3. RBF核 / 高斯核 (Radial Basis Function)")
print("-" * 80)
print("公式: K(x1, x2) = exp(-γ × ||x1 - x2||²)")

gamma_rbf = 0.5
diff = x1 - x2
dist_squared = np.dot(diff, diff)
K_rbf = np.exp(-gamma_rbf * dist_squared)

print(f"\n参数: γ={gamma_rbf}")
print(f"计算过程:")
print(f"  x1 - x2 = {diff}")
print(f"  ||x1 - x2||² = {diff[0]}² + {diff[1]}² = {diff[0]**2} + {diff[1]**2} = {dist_squared}")
print(f"  K(x1, x2) = exp(-{gamma_rbf} × {dist_squared})")
print(f"            = exp({-gamma_rbf * dist_squared})")
print(f"            = {K_rbf:.6f}")

print(f"\n" + "-" * 80)
print("RBF核的距离效应演示:")
print("-" * 80)

test_points = [
    (np.array([1.0, 2.0]), "相同点"),
    (np.array([1.5, 2.5]), "近距离点"),
    (np.array([5.0, 8.0]), "远距离点")
]

for x_test, desc in test_points:
    diff = x1 - x_test
    dist_sq = np.dot(diff, diff)
    K = np.exp(-gamma_rbf * dist_sq)
    print(f"\n{desc}: x = {x_test}")
    print(f"  距离² = {dist_sq:.2f}")
    print(f"  相似度 K(x1, x) = {K:.6f}")


# ============================================================================
# 第5部分：超参数调优 (C 和 gamma)
# ============================================================================
print("\n" + "=" * 80)
print("第5部分：超参数调优 - Grid Search")
print("=" * 80)

# 5.1 准备数据
X_train, X_test, y_train, y_test = train_test_split(
    X_circles, y_circles, test_size=0.3, random_state=42
)

print(f"\n数据划分:")
print(f"  训练集: {len(X_train)} 样本")
print(f"  测试集: {len(X_test)} 样本")

# 5.2 定义参数网格
param_grid = {
    'C': [0.1, 1, 10, 100],
    'gamma': [0.001, 0.01, 0.1, 1, 'scale', 'auto']
}

print(f"\n参数网格:")
print(f"  C: {param_grid['C']}")
print(f"  gamma: {param_grid['gamma']}")
print(f"  总组合数: {len(param_grid['C']) * len(param_grid['gamma'])}")

# 5.3 网格搜索
print(f"\n开始网格搜索（使用3折交叉验证）...")
grid_search = GridSearchCV(
    SVC(kernel='rbf'),
    param_grid,
    cv=3,
    scoring='accuracy',
    verbose=0,
    n_jobs=-1
)

grid_search.fit(X_train, y_train)

print(f"\n网格搜索完成！")
print(f"\n最佳参数:")
print(f"  C = {grid_search.best_params_['C']}")
print(f"  gamma = {grid_search.best_params_['gamma']}")
print(f"\n最佳交叉验证得分: {grid_search.best_score_:.4f}")

# 5.4 在测试集上评估
best_svm = grid_search.best_estimator_
y_pred = best_svm.predict(X_test)
test_accuracy = accuracy_score(y_test, y_pred)

print(f"测试集准确率: {test_accuracy:.4f}")
print(f"\n分类报告:")
print(classification_report(y_test, y_pred, target_names=['负类', '正类']))

# 5.5 可视化最佳模型
fig, ax = plt.subplots(1, 1, figsize=(10, 8))

ax.scatter(X_test[y_test == -1, 0], X_test[y_test == -1, 1], 
           c='red', marker='o', s=100, label='负类（测试）', edgecolors='k', alpha=0.7)
ax.scatter(X_test[y_test == 1, 0], X_test[y_test == 1, 1], 
           c='blue', marker='s', s=100, label='正类（测试）', edgecolors='k', alpha=0.7)

# 标记错误分类的点
misclassified = y_test != y_pred
if np.any(misclassified):
    ax.scatter(X_test[misclassified, 0], X_test[misclassified, 1], 
               s=300, facecolors='none', edgecolors='orange', linewidths=3, 
               label='误分类', marker='x')

# 绘制决策边界
x_min, x_max = X_circles[:, 0].min() - 0.5, X_circles[:, 0].max() + 0.5
y_min, y_max = X_circles[:, 1].min() - 0.5, X_circles[:, 1].max() + 0.5
xx, yy = np.meshgrid(np.linspace(x_min, x_max, 200), 
                     np.linspace(y_min, y_max, 200))
Z = best_svm.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

ax.contourf(xx, yy, Z, alpha=0.2, levels=[-1, 0, 1], colors=['red', 'blue'])
ax.contour(xx, yy, Z, levels=[0], colors='black', linewidths=2)

ax.set_xlabel('特征 x₁', fontsize=12)
ax.set_ylabel('特征 x₂', fontsize=12)
ax.set_title(f'最佳 SVM 模型\nC={grid_search.best_params_["C"]}, '
             f'gamma={grid_search.best_params_["gamma"]}, '
             f'准确率={test_accuracy:.3f}', fontsize=14)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('svm_demo_4_best_model.png', dpi=150, bbox_inches='tight')
print("\n保存图表: svm_demo_4_best_model.png")


# ============================================================================
# 第6部分：MMC vs SVC vs SVM 对比总结
# ============================================================================
print("\n" + "=" * 80)
print("第6部分：MMC vs SVC vs SVM 对比总结")
print("=" * 80)

summary = """
┌─────────────────────────────────────────────────────────────────────────┐
│                    SVM 方法演进对比                                      │
├──────────────┬──────────────────┬──────────────────┬───────────────────┤
│   方法       │   间隔类型       │   核函数         │   适用场景        │
├──────────────┼──────────────────┼──────────────────┼───────────────────┤
│ MMC          │ 硬间隔 (C→∞)    │ 线性             │ 完全线性可分      │
│ (Maximum     │ 不允许误分类     │                  │ 无噪声数据        │
│  Margin      │                  │                  │                   │
│  Classifier) │                  │                  │                   │
├──────────────┼──────────────────┼──────────────────┼───────────────────┤
│ SVC          │ 软间隔 (C有限)  │ 线性             │ 近似线性可分      │
│ (Support     │ 允许少量误分类   │                  │ 有噪声/重叠       │
│  Vector      │                  │                  │                   │
│  Classifier) │                  │                  │                   │
├──────────────┼──────────────────┼──────────────────┼───────────────────┤
│ SVM          │ 软间隔 (C有限)  │ 非线性           │ 非线性可分        │
│ (Support     │ 允许少量误分类   │ (poly, RBF等)    │ 复杂边界          │
│  Vector      │                  │                  │                   │
│  Machine)    │                  │                  │                   │
└──────────────┴──────────────────┴──────────────────┴───────────────────┘

演进关系:
  MMC → SVC: 引入软间隔（松弛变量 ξᵢ），允许误分类
  SVC → SVM: 引入核函数（核技巧），处理非线性问题

关键参数:
  • C: 控制间隔宽度 vs 误分类惩罚的权衡
    - C 大 → 严格分类，窄间隔，可能过拟合
    - C 小 → 宽松分类，宽间隔，可能欠拟合
  
  • gamma (仅 RBF/poly 核): 控制单个样本的影响范围
    - gamma 大 → 影响范围小，决策边界复杂，可能过拟合
    - gamma 小 → 影响范围大，决策边界平滑，可能欠拟合

sklearn 使用:
  from sklearn.svm import SVC
  
  # MMC (近似)
  svm = SVC(kernel='linear', C=1000.0)
  
  # SVC
  svm = SVC(kernel='linear', C=1.0)
  
  # SVM
  svm = SVC(kernel='rbf', C=1.0, gamma='scale')
"""

print(summary)

# ============================================================================
# 总结
# ============================================================================
print("\n" + "=" * 80)
print("演示完成！")
print("=" * 80)

print(f"""
生成的图表:
  1. svm_demo_1_hard_margin.png  - 硬间隔 SVM (MMC)
  2. svm_demo_2_soft_margin.png  - 软间隔 SVM，不同 C 值对比
  3. svm_demo_3_kernels.png      - 不同核函数对比
  4. svm_demo_4_best_model.png   - 超参数调优后的最佳模型

关键要点:
  ✓ 所有参数 (w, b) 都是通过训练数据学习得到的，不是"假设"的
  ✓ 支持向量是最接近决策边界的点，它们决定了超平面
  ✓ 间隔 = 2/||w||，最大化间隔等价于最小化 ||w||
  ✓ C 控制间隔宽度和误分类的权衡
  ✓ 核函数允许 SVM 处理非线性问题，无需显式映射到高维
  ✓ RBF 核是最常用的核函数，适用于大多数非线性问题

下一步:
  • 运行脚本: uv run python courses/ml/labs/svm_complete_demo.py
  • 查看生成的图表理解 SVM 的工作原理
  • 尝试修改参数观察效果变化
""")

print("=" * 80)

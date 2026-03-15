---
topic: activation_functions
dimension: code
created: 2026-03-15
last_verified: 2026-03-15
source_versions:
  - "📖 Docs: Keras Activations — https://keras.io/api/layers/activations/"
  - "📖 Docs: PyTorch nn.Module Activations — https://pytorch.org/docs/stable/nn.html#non-linear-activations-weighted-sum-nonlinearity"
  - "📖 Docs: scikit-learn MLPClassifier — https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html"
  - "📚 Book: Goodfellow et al., 'Deep Learning' Ch.6 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
expiry: 6m
status: current
---

# Activation Functions 代码参考

> 📖 Docs: [Keras Activations](https://keras.io/api/layers/activations/)
> 📖 Docs: [scikit-learn MLPClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html)


## 快速开始

### 最简示例 — 30 秒上手

```python
import numpy as np

# ============================================================
# 从零实现 5 种激活函数（不依赖任何框架）
# Implement 5 activation functions from scratch (no framework)
# ============================================================

# Sigmoid: 把任意实数压缩到 (0, 1)
# Sigmoid: squash any real number to (0, 1)
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

# Tanh: 把任意实数压缩到 (-1, 1)，零中心化
# Tanh: squash any real number to (-1, 1), zero-centered
def tanh(z):
    return np.tanh(z)

# ReLU: 正数通过，负数归零
# ReLU: pass positive, zero out negative
def relu(z):
    return np.maximum(0, z)

# Leaky ReLU: 正数通过，负数乘以小系数
# Leaky ReLU: pass positive, scale negative by small alpha
def leaky_relu(z, alpha=0.01):
    return np.where(z > 0, z, alpha * z)

# Softmax: 把向量变成概率分布（和为 1）
# Softmax: convert vector to probability distribution (sum to 1)
def softmax(z):
    exp_z = np.exp(z - np.max(z))  # 数值稳定 / numerical stability
    return exp_z / exp_z.sum()

# 测试 / Test
z = np.array([-2.0, -1.0, 0.0, 1.0, 2.0])
print(f"Input:      {z}")
print(f"Sigmoid:    {sigmoid(z)}")
print(f"Tanh:       {tanh(z)}")
print(f"ReLU:       {relu(z)}")
print(f"Leaky ReLU: {leaky_relu(z)}")
print(f"Softmax:    {softmax(z)}")
```

**测试方法：** 直接运行脚本，检查输出范围是否符合预期。Sigmoid 输出在 (0,1)，Tanh 在 (-1,1)，ReLU ≥ 0，Softmax 和为 1。

> 📖 Docs: [NumPy Mathematical Functions](https://numpy.org/doc/stable/reference/routines.math.html)

---

## 完整实现示例

### 示例 1: Scikit-Learn MLPClassifier 激活函数对比

```python
# ============================================================
# 1. 数据准备 / Data Preparation
# ============================================================
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

# 生成非线性数据集 / Generate nonlinear dataset
# make_moons: 两个交错的半月形，测试非线性分类能力
X, y = make_moons(n_samples=1000, noise=0.2, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# ============================================================
# 2. 不同激活函数的 MLP 对比 / Compare activations in MLP
# ============================================================
# scikit-learn 支持 4 种激活函数
# scikit-learn supports 4 activation functions:
#   'identity': f(x) = x          (线性，无非线性)
#   'logistic': f(x) = sigmoid(x) (Sigmoid 函数)
#   'tanh':     f(x) = tanh(x)    (双曲正切)
#   'relu':     f(x) = max(0, x)  (默认，推荐)

activations = ['identity', 'logistic', 'tanh', 'relu']
results = {}

for act in activations:
    # hidden_layer_sizes=(100,50): 两层隐藏层，分别 100 和 50 个神经元
    # max_iter=500: 最大训练 500 轮
    # random_state=42: 固定随机种子保证可复现
    mlp = MLPClassifier(
        hidden_layer_sizes=(100, 50),     # 隐藏层架构
        activation=act,                    # 激活函数
        solver='adam',                     # 优化器
        max_iter=500,                      # 最大迭代次数
        random_state=42,                   # 随机种子
        early_stopping=True,               # 验证集提前停止
        validation_fraction=0.1            # 验证集比例
    )
    mlp.fit(X_train, y_train)
    y_pred = mlp.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    results[act] = acc
    print(f"Activation: {act:10s} | Accuracy: {acc:.4f} | Iterations: {mlp.n_iter_}")

# ============================================================
# 3. 结果分析 / Results Analysis
# ============================================================
print("\n--- 对比总结 ---")
for act, acc in sorted(results.items(), key=lambda x: x[1], reverse=True):
    print(f"  {act:10s}: {acc:.4f}")
```

> 📖 Docs: [scikit-learn MLPClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html)

---

### 示例 2: Keras Dense 层激活函数对比（MNIST 分类）

```python
# ============================================================
# 1. 数据准备 / Data Preparation
# ============================================================
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers

# 加载 MNIST 手写数字数据集 / Load MNIST handwritten digits
(X_train, y_train), (X_test, y_test) = keras.datasets.mnist.load_data()

# 数据预处理 / Preprocessing
# 展平 28x28 图像为 784 维向量，归一化到 [0, 1]
X_train = X_train.reshape(-1, 784).astype('float32') / 255.0
X_test = X_test.reshape(-1, 784).astype('float32') / 255.0

# ============================================================
# 2. 构建不同激活函数的模型 / Build models with different activations
# ============================================================
def build_model(activation_name):
    """构建 MLP 模型，指定隐藏层激活函数
    Build MLP model with specified hidden layer activation"""
    model = keras.Sequential([
        # 第一隐藏层：128 个神经元
        # First hidden layer: 128 units
        layers.Dense(128, activation=activation_name, input_shape=(784,)),

        # 第二隐藏层：64 个神经元
        # Second hidden layer: 64 units
        layers.Dense(64, activation=activation_name),

        # 输出层：10 个类别，用 softmax 将输出转为概率分布
        # Output layer: 10 classes, softmax converts to probability distribution
        layers.Dense(10, activation='softmax')
    ])

    # compile: 配置训练过程
    # optimizer='adam': Adam 优化器（自适应学习率）
    # loss: 稀疏分类交叉熵（标签是整数，不是 one-hot）
    # metrics: 监控准确率
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    return model

# 对比不同激活函数 / Compare different activations
# Keras 支持的所有激活函数
keras_activations = ['sigmoid', 'tanh', 'relu', 'elu', 'selu', 'swish', 'gelu']

for act in keras_activations:
    print(f"\n{'='*50}")
    print(f"Training with activation: {act}")
    print(f"{'='*50}")

    model = build_model(act)

    # fit: 执行训练
    # epochs=5: 遍历数据集 5 次
    # batch_size=128: 每次用 128 个样本更新权重
    # validation_split=0.1: 从训练集中留 10% 作为验证集
    history = model.fit(
        X_train, y_train,
        epochs=5,
        batch_size=128,
        validation_split=0.1,
        verbose=0                          # 静音训练过程
    )

    # 评估测试集 / Evaluate on test set
    test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
    print(f"  Test Accuracy: {test_acc:.4f}")
    print(f"  Final Val Acc: {history.history['val_accuracy'][-1]:.4f}")
```

> 📖 Docs: [Keras Activations](https://keras.io/api/layers/activations/)
> 📖 Docs: [Keras Dense Layer](https://keras.io/api/layers/core_layers/dense/)

---

### 示例 3: 激活函数可视化（函数形状 + 梯度）

```python
# ============================================================
# 1. 导入和配置 / Import and Configuration
# ============================================================
import numpy as np
import matplotlib.pyplot as plt

# 输入范围 / Input range
z = np.linspace(-5, 5, 200)

# ============================================================
# 2. 定义激活函数和梯度 / Define activations and gradients
# ============================================================
activations = {
    'Sigmoid': {
        'func': lambda z: 1 / (1 + np.exp(-z)),
        'grad': lambda z: (1 / (1 + np.exp(-z))) * (1 - 1 / (1 + np.exp(-z)))
    },
    'Tanh': {
        'func': np.tanh,
        'grad': lambda z: 1 - np.tanh(z)**2
    },
    'ReLU': {
        'func': lambda z: np.maximum(0, z),
        'grad': lambda z: (z > 0).astype(float)
    },
    'Leaky ReLU': {
        'func': lambda z: np.where(z > 0, z, 0.1 * z),
        'grad': lambda z: np.where(z > 0, 1.0, 0.1)
    },
    'ELU': {
        'func': lambda z: np.where(z > 0, z, 1.0 * (np.exp(z) - 1)),
        'grad': lambda z: np.where(z > 0, 1.0, np.exp(z))
    },
    'Swish': {
        'func': lambda z: z / (1 + np.exp(-z)),
        'grad': lambda z: (1/(1+np.exp(-z))) + z*(1/(1+np.exp(-z)))*(1-1/(1+np.exp(-z)))
    }
}

# ============================================================
# 3. 绘图 / Plotting
# ============================================================
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.flatten()

for idx, (name, funcs) in enumerate(activations.items()):
    ax = axes[idx]
    # 画激活函数和梯度 / Plot activation and gradient
    ax.plot(z, funcs['func'](z), 'b-', linewidth=2, label=f'{name}(z)')
    ax.plot(z, funcs['grad'](z), 'r--', linewidth=2, label=f"{name}'(z)")
    ax.axhline(y=0, color='gray', linewidth=0.5)
    ax.axvline(x=0, color='gray', linewidth=0.5)
    ax.set_title(name, fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_xlim(-5, 5)

plt.tight_layout()
plt.savefig('activation_functions_comparison.png', dpi=150)
plt.show()
print("Plot saved to activation_functions_comparison.png")
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.3

---

## API 速查

### scikit-learn MLPClassifier

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|-----|--------|------|
| `MLPClassifier()` | `activation` | `'relu'` | 隐藏层激活函数 |
| ↳ | `'identity'` | — | $f(z) = z$（线性） |
| ↳ | `'logistic'` | — | $f(z) = \sigma(z)$（Sigmoid） |
| ↳ | `'tanh'` | — | $f(z) = \tanh(z)$ |
| ↳ | `'relu'` | — | $f(z) = \max(0, z)$（推荐） |

### Keras Dense Layer

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|-----|--------|------|
| `Dense()` | `activation` | `None` | 层的激活函数 |
| ↳ | `'sigmoid'` | — | Sigmoid 函数 |
| ↳ | `'tanh'` | — | Tanh 函数 |
| ↳ | `'relu'` | — | ReLU（隐藏层推荐） |
| ↳ | `'elu'` | — | ELU 函数 |
| ↳ | `'selu'` | — | Scaled ELU（自归一化） |
| ↳ | `'softmax'` | — | 多分类输出层 |
| ↳ | `'swish'` / `'silu'` | — | Swish/SiLU 函数 |
| ↳ | `'gelu'` | — | GELU（Transformer 用） |
| ↳ | `'softplus'` | — | $\ln(1+e^z)$（ReLU 光滑版） |
| ↳ | `'linear'` / `None` | — | 恒等函数（回归输出层） |

### Keras Activation Layer

| 函数/类 | 参数 | 说明 |
|---------|-----|------|
| `layers.Activation('relu')` | `activation` | 独立的激活层（等价于 Dense 中指定） |
| `layers.LeakyReLU(alpha=0.3)` | `alpha` | Leaky ReLU 层（可调斜率） |
| `layers.PReLU()` | — | PReLU 层（斜率可学习） |
| `layers.ELU(alpha=1.0)` | `alpha` | ELU 层 |

### 常用工具

| 函数 | 说明 |
|------|------|
| `tf.nn.relu(x)` | TensorFlow ReLU 函数 |
| `tf.nn.sigmoid(x)` | TensorFlow Sigmoid 函数 |
| `tf.nn.softmax(x)` | TensorFlow Softmax 函数 |
| `keras.activations.get('relu')` | 通过名字获取激活函数对象 |

> 📖 Docs: [Keras Activations API](https://keras.io/api/layers/activations/)
> 📖 Docs: [scikit-learn MLPClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html)

---

## 目录结构模板

### 简单结构

```
activation_study/
├── compare_activations.py   ← 激活函数对比实验
├── visualize.py             ← 函数形状可视化
└── results/
    └── figures/             ← 生成的图表
```

### 标准结构

```
activation_study/
├── config.py                ← 实验配置（激活函数列表、超参数）
├── activations.py           ← 自定义激活函数实现
├── train_sklearn.py         ← scikit-learn MLP 实验
├── train_keras.py           ← Keras MLP 实验
├── visualize.py             ← 可视化脚本
├── utils.py                 ← 通用工具（数据加载、评估）
├── data/                    ← 数据集
├── results/
│   ├── figures/             ← 图表输出
│   └── logs/                ← 训练日志
└── requirements.txt
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6

---
topic: optimizers
dimension: code
created: 2026-03-15
last_verified: 2026-03-15
source_versions:
  - "📖 Docs: Keras Optimizers — https://keras.io/api/optimizers/"
  - "📖 Docs: scikit-learn MLPClassifier — https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html"
  - "📚 Book: Goodfellow et al., 'Deep Learning' Ch.8 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
expiry: 6m
status: current
---

# Optimizers 代码参考

> 📖 Docs: [Keras Optimizers](https://keras.io/api/optimizers/)
> 📖 Docs: [scikit-learn MLPClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html)


## 快速开始

### 最简示例 — 30 秒上手

```python
import numpy as np

# ============================================================
# 从零实现 SGD 和 Adam（不依赖任何框架）
# Implement SGD and Adam from scratch (no framework)
# ============================================================

# Vanilla SGD / 随机梯度下降
def sgd_update(W, grad, lr=0.01):
    """最简单的优化器：沿梯度反方向走一步
    Simplest optimizer: take one step against gradient"""
    return W - lr * grad

# Adam 优化器 / Adam optimizer
class Adam:
    """Adam: 自适应矩估计优化器
    Adam: Adaptive Moment Estimation optimizer"""
    def __init__(self, lr=0.001, beta1=0.9, beta2=0.999, eps=1e-8):
        self.lr = lr          # 学习率 / learning rate
        self.beta1 = beta1    # 一阶矩衰减 / first moment decay
        self.beta2 = beta2    # 二阶矩衰减 / second moment decay
        self.eps = eps        # 数值稳定 / numerical stability
        self.m = 0            # 一阶矩 / first moment
        self.v = 0            # 二阶矩 / second moment
        self.t = 0            # 时间步 / time step

    def step(self, W, grad):
        self.t += 1
        self.m = self.beta1 * self.m + (1 - self.beta1) * grad      # 动量
        self.v = self.beta2 * self.v + (1 - self.beta2) * grad**2   # 方差
        m_hat = self.m / (1 - self.beta1**self.t)                    # 偏差修正
        v_hat = self.v / (1 - self.beta2**self.t)                    # 偏差修正
        return W - self.lr * m_hat / (np.sqrt(v_hat) + self.eps)

# 测试：最小化 f(W) = W^2，最优解 W* = 0
W_sgd, W_adam = 5.0, 5.0
adam = Adam(lr=0.1)

for i in range(20):
    grad = 2 * W_sgd              # f'(W) = 2W
    W_sgd = sgd_update(W_sgd, grad, lr=0.1)
    W_adam = adam.step(W_adam, 2 * W_adam)

print(f"SGD  final W: {W_sgd:.6f}")   # → 接近 0
print(f"Adam final W: {W_adam:.6f}")   # → 接近 0
```

**测试方法：** 运行脚本，两个 W 都应趋近 0。Adam 通常更快收敛到更接近 0 的值。

> 📖 Paper: Kingma & Ba, [Adam](https://arxiv.org/abs/1412.6980), ICLR 2015

---

## 完整实现示例

### 示例 1: scikit-learn 三种 solver 对比

```python
# ============================================================
# 1. 数据准备 / Data Preparation
# ============================================================
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
import time

X, y = make_moons(n_samples=2000, noise=0.2, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# ============================================================
# 2. 三种 solver 对比 / Compare 3 solvers
# ============================================================
# scikit-learn MLPClassifier 支持 3 种 solver:
#   'lbfgs': 拟牛顿法，小数据集快
#   'sgd':   随机梯度下降
#   'adam':  自适应矩估计（默认）

solvers = {
    'lbfgs': {'solver': 'lbfgs', 'max_iter': 500},
    'sgd':   {'solver': 'sgd', 'learning_rate_init': 0.01, 'max_iter': 500,
              'learning_rate': 'adaptive'},          # 自适应学习率调度
    'adam':  {'solver': 'adam', 'learning_rate_init': 0.001, 'max_iter': 500},
}

for name, params in solvers.items():
    start = time.time()
    mlp = MLPClassifier(
        hidden_layer_sizes=(100, 50),
        activation='relu',
        random_state=42,
        **params
    )
    mlp.fit(X_train, y_train)
    elapsed = time.time() - start
    acc = accuracy_score(y_test, mlp.predict(X_test))
    print(f"Solver: {name:6s} | Acc: {acc:.4f} | Iters: {mlp.n_iter_:4d} | Time: {elapsed:.3f}s")
```

> 📖 Docs: [scikit-learn MLPClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html)

---

### 示例 2: Keras 多种 optimizer 对比（MNIST）

```python
# ============================================================
# 1. 数据准备 / Data Preparation
# ============================================================
from tensorflow import keras
from tensorflow.keras import layers

(X_train, y_train), (X_test, y_test) = keras.datasets.mnist.load_data()
X_train = X_train.reshape(-1, 784).astype('float32') / 255.0
X_test = X_test.reshape(-1, 784).astype('float32') / 255.0

# ============================================================
# 2. 定义模型工厂 / Model factory
# ============================================================
def build_model(optimizer):
    """用指定 optimizer 构建并编译模型
    Build and compile model with specified optimizer"""
    model = keras.Sequential([
        layers.Dense(128, activation='relu', input_shape=(784,)),
        layers.Dense(64, activation='relu'),
        layers.Dense(10, activation='softmax')
    ])
    # compile: 配置训练过程
    # optimizer: 权重更新策略
    # loss: 优化目标
    # metrics: 监控指标
    model.compile(
        optimizer=optimizer,
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    return model

# ============================================================
# 3. 对比不同优化器 / Compare optimizers
# ============================================================
optimizers = {
    'SGD':         keras.optimizers.SGD(learning_rate=0.01),
    'SGD+Momentum':keras.optimizers.SGD(learning_rate=0.01, momentum=0.9),
    'RMSprop':     keras.optimizers.RMSprop(learning_rate=0.001),
    'Adam':        keras.optimizers.Adam(learning_rate=0.001),
    'AdamW':       keras.optimizers.AdamW(learning_rate=0.001, weight_decay=0.01),
}

for name, opt in optimizers.items():
    print(f"\n{'='*50}")
    print(f"Optimizer: {name}")
    print(f"{'='*50}")
    model = build_model(opt)

    # fit: 执行训练
    # epochs=5: 遍历数据 5 次
    # batch_size=128: 每次 128 个样本更新一次权重
    # validation_split=0.1: 留 10% 做验证
    history = model.fit(
        X_train, y_train,
        epochs=5,
        batch_size=128,
        validation_split=0.1,
        verbose=0
    )
    _, test_acc = model.evaluate(X_test, y_test, verbose=0)
    print(f"  Test Accuracy: {test_acc:.4f}")
```

> 📖 Docs: [Keras Optimizers](https://keras.io/api/optimizers/)

---

### 示例 3: 学习率对训练的影响

```python
# ============================================================
# 学习率敏感性实验 / Learning rate sensitivity experiment
# ============================================================
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers

(X_train, y_train), (X_test, y_test) = keras.datasets.mnist.load_data()
X_train = X_train.reshape(-1, 784).astype('float32') / 255.0
X_test = X_test.reshape(-1, 784).astype('float32') / 255.0

# 测试不同学习率 / Test different learning rates
learning_rates = [0.0001, 0.001, 0.01, 0.1, 1.0]

for lr in learning_rates:
    model = keras.Sequential([
        layers.Dense(128, activation='relu', input_shape=(784,)),
        layers.Dense(10, activation='softmax')
    ])
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=lr),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    history = model.fit(X_train, y_train, epochs=5, batch_size=128, verbose=0)
    _, acc = model.evaluate(X_test, y_test, verbose=0)
    final_loss = history.history['loss'][-1]
    print(f"lr={lr:<8} | Final Loss: {final_loss:.4f} | Test Acc: {acc:.4f}")
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8

---

## API 速查

### scikit-learn MLPClassifier

| 参数 | 值 | 说明 |
|------|-----|------|
| `solver` | `'adam'` | **默认**，自适应矩估计 |
| ↳ | `'sgd'` | 随机梯度下降 |
| ↳ | `'lbfgs'` | 拟牛顿法（小数据集） |
| `learning_rate_init` | `0.001` | 初始学习率 |
| `learning_rate` | `'constant'` | 学习率策略（solver='sgd' 时） |
| ↳ | `'invscaling'` | $\eta_t = \eta_0 / t^{power_t}$ |
| ↳ | `'adaptive'` | 验证集不提升时自动减小 |
| `batch_size` | `'auto'` | 批量大小（auto = min(200, n_samples)） |
| `max_iter` | `200` | 最大迭代次数（epoch 数） |
| `early_stopping` | `False` | 是否启用提前停止 |

### Keras Optimizers

| 类 | 关键参数 | 默认值 | 说明 |
|-----|---------|--------|------|
| `SGD()` | `learning_rate` | `0.01` | 随机梯度下降 |
| ↳ | `momentum` | `0.0` | 动量系数 |
| ↳ | `nesterov` | `False` | 是否用 Nesterov 动量 |
| `Adam()` | `learning_rate` | `0.001` | **推荐默认** |
| ↳ | `beta_1` | `0.9` | 一阶矩衰减 |
| ↳ | `beta_2` | `0.999` | 二阶矩衰减 |
| ↳ | `epsilon` | `1e-7` | 数值稳定 |
| `AdamW()` | `weight_decay` | `0.004` | 解耦权重衰减 |
| `RMSprop()` | `learning_rate` | `0.001` | RNN/LSTM 推荐 |
| ↳ | `rho` | `0.9` | 衰减系数 |
| `Adagrad()` | `learning_rate` | `0.001` | 稀疏数据/NLP |

### 常用工具

| 用法 | 说明 |
|------|------|
| `model.compile(optimizer='adam')` | 字符串形式（用默认参数） |
| `model.compile(optimizer=Adam(lr=0.0005))` | 对象形式（自定义参数） |
| `keras.optimizers.schedules.ExponentialDecay(...)` | 学习率衰减调度 |
| `model.optimizer.learning_rate.numpy()` | 查看当前学习率 |

> 📖 Docs: [Keras Optimizers API](https://keras.io/api/optimizers/)
> 📖 Docs: [scikit-learn MLPClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html)

---

## 目录结构模板

### 简单结构

```
optimizer_study/
├── compare_optimizers.py    ← 优化器对比实验
├── lr_sensitivity.py        ← 学习率敏感性实验
└── results/
    └── figures/             ← 训练曲线图
```

### 标准结构

```
optimizer_study/
├── config.py                ← 实验配置
├── train_sklearn.py         ← scikit-learn solver 对比
├── train_keras.py           ← Keras optimizer 对比
├── lr_experiment.py         ← 学习率实验
├── visualize.py             ← 可视化训练曲线
├── utils.py                 ← 通用工具
├── data/
├── results/
│   ├── figures/
│   └── logs/
└── requirements.txt
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8

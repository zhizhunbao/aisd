# Week 4: RNN & LSTM — 代码参考

> **Source:** lab4 code (`Lab4_TimeSeries.md`)
> **Scope:** 代码基础 → 时间序列预处理 → Dense/SimpleRNN/LSTM 模型
> **See also:** [week4_rnn_cheatsheet.md](week4_rnn_cheatsheet.md) (概念速查) | [week4_rnn_math.md](week4_rnn_math.md) (公式+手算)
> **阅读建议：** 先看本文件的"代码基础"部分，再看 Lab4 代码和 demo 脚本会更轻松

---

## ★ 代码基础 (Code Foundations)

> 📌 这一部分是理解 RNN/LSTM 代码的**前置知识**。如果你已熟悉 numpy 矩阵运算和 Keras Sequential，可以跳到 "Imports & Setup"。
>
> 📌 This section covers **prerequisites** for understanding RNN/LSTM code. Skip to "Imports & Setup" if you already know numpy matrix ops and Keras Sequential.

### 🔧 Numpy 矩阵运算 (Matrix Operations)

```python
import numpy as np

# --- 矩阵乘法 vs 逐元素乘法 (Matrix multiply vs Element-wise multiply) ---
# ⚠️ RNN 用矩阵乘法 (@), LSTM 门用逐元素乘法 (*)
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

# 矩阵乘法 / Matrix multiplication: 行 × 列求和
# RNN核心: h_t = tanh(W_x @ x_t + W_h @ h_{t-1})
C = A @ B         # = [[19, 22], [43, 50]]
# 等价写法: C = np.dot(A, B) 或 np.matmul(A, B)

# 逐元素乘法 / Element-wise (Hadamard) product: 对应位置相乘
# LSTM核心: C_t = f_t * C_{t-1} + i_t * C_tilde
D = A * B         # = [[5, 12], [21, 32]]
# 数学符号: ⊙ (Hadamard product)
```

> ⚠️ **关键区别：** `@` = 矩阵乘法（RNN hidden state），`*` = 逐元素乘法（LSTM gates）
>
> ⚠️ **Key difference:** `@` = matrix multiply (RNN hidden state), `*` = element-wise multiply (LSTM gates)

### 🔧 向量拼接与 Reshape (Concatenation & Reshape)

```python
# --- 向量拼接 / Vector concatenation ---
# LSTM 门接收 [h_{t-1}, x_t] 的拼接作为输入
h_prev = np.array([[0.5], [0.3]])    # shape: (2, 1) — 隐藏状态
x_t = np.array([[1.0]])              # shape: (1, 1) — 当前输入

# 纵向拼接 / Vertical stack: [h, x] → combined input
concat = np.vstack([h_prev, x_t])    # shape: (3, 1)
# concat = [[0.5], [0.3], [1.0]]

# --- Reshape: 时间序列需要 3D 输入 ---
# Keras RNN 要求输入 shape = (样本数, 时间步, 特征数)
# Keras RNN requires input shape = (samples, timesteps, features)
data = np.array([1, 2, 3, 4, 5, 6])

# 1D → 2D: 列向量 / Column vector
col = data.reshape(-1, 1)            # shape: (6, 1)

# 2D → 3D: 加上 batch 维度 / Add batch dimension
batch = data.reshape(1, 6, 1)        # shape: (1, 6, 1)
#   1 个样本, 6 个时间步, 每步 1 个特征
#   1 sample, 6 timesteps, 1 feature per step
```

### 🔧 Sigmoid 和 Tanh 的代码实现 (Sigmoid & Tanh in Code)

```python
# --- Sigmoid: 门控函数 / Gate function ---
# σ(x) = 1/(1+e^(-x)), 输出 (0, 1)
def sigmoid(x):
    return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
    # clip 防止 overflow / clip prevents overflow

# Python 验证数学基础部分的手算:
print(sigmoid(0))     # 0.5
print(sigmoid(1.5))   # ≈ 0.818
print(sigmoid(-2))    # ≈ 0.119

# --- Tanh: 隐藏状态激活 / Hidden state activation ---
# tanh(x) = (e^x - e^(-x))/(e^x + e^(-x)), 输出 (-1, 1)
print(np.tanh(0))     # 0.0
print(np.tanh(1.5))   # ≈ 0.905
# numpy 内置 tanh，不需要手写 / numpy has built-in tanh
```

### 🔧 Keras Sequential 模式 (Keras Sequential Pattern)

```python
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Keras 标准流程：Build → Compile → Fit → Predict
# Keras standard workflow: Build → Compile → Fit → Predict

# 1. Build: 堆叠层 / Stack layers
model = Sequential([
    Dense(64, activation='relu', input_shape=(12, 1)),  # 第一层指定输入形状
    Dense(32, activation='relu'),                        # 中间层
    Dense(1)                                             # 输出层（回归=无激活）
])

# 2. Compile: 配置优化器+损失+指标
model.compile(
    optimizer='adam',       # 自适应学习率优化器
    loss='mse',            # 回归用 MSE，分类用 cross_entropy
    metrics=['mae']        # 额外指标（不影响训练，只用于监控）
)

# 3. Fit: 训练
model.fit(X_train, y_train, epochs=30, verbose=1)

# 4. Predict: 预测
predictions = model.predict(X_test)
```

> 💡 **从 Dense 到 RNN 只需改一层：** 把 `Dense` 换成 `SimpleRNN` 或 `LSTM`，其他流程完全一样。
>
> 💡 **From Dense to RNN, just change one layer:** Replace `Dense` with `SimpleRNN` or `LSTM`, everything else stays the same.

---

## Imports & Setup

### 🔧 Code

```python
# Core imports for time series analysis with neural networks
# 时间序列分析核心导入
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

# Keras imports for building models
# Keras 模型构建导入
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, SimpleRNN, LSTM, Dropout, Flatten
from tensorflow.keras.preprocessing.sequence import TimeseriesGenerator

# Reproducibility / 可重复性
np.random.seed(42)
import tensorflow as tf
tf.random.set_seed(42)

# Hyperparameters / 超参数
WINDOW_SIZE = 12   # Past 12 weeks to predict next week / 用过去 12 周预测下一周
EPOCHS = 30        # Training epochs / 训练轮数
BATCH_SIZE = 32    # Batch size / 批大小
```

---

## Data Loading & Preprocessing

### 🔧 Code

- 🔧 **Load CSV and convert to weekly averages:**

```python
# Load daily temperature data / 加载每日温度数据
df = pd.read_csv('daily-minimum-temperatures.csv',
                 parse_dates=['Date'], index_col='Date')

# Convert daily → weekly averages / 每日 → 每周平均
weekly = df.resample('W').mean()
print(weekly.head())
```

- 🔧 **Plot time series:**

```python
# Plot full time series / 绘制完整时间序列
plt.figure(figsize=(14, 5))
plt.plot(weekly.index, weekly['Temp'], color='blue')
plt.title('Weekly Average Temperature')
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.show()
```

---

## Time Series Decomposition

### 🔧 Code

```python
# Decompose: Original = Trend + Seasonal + Residual
# 分解：原始 = 趋势 + 季节性 + 残差
# period=52 → 52 weeks = 1 year seasonal cycle
# period=52 → 52 周 = 1 年季节周期
result = seasonal_decompose(weekly['Temp'], model='additive', period=52)

fig, axes = plt.subplots(4, 1, figsize=(14, 10))
result.observed.plot(ax=axes[0], title='Original')
result.trend.plot(ax=axes[1], title='Trend')
result.seasonal.plot(ax=axes[2], title='Seasonal')
result.resid.plot(ax=axes[3], title='Residual')
plt.tight_layout()
plt.show()
```

> ⚠️ Use `model='additive'` when seasonal amplitude is constant; `model='multiplicative'` when it grows with trend.
>
> ⚠️ 季节振幅恒定用 `additive`；随趋势增长用 `multiplicative`。

---

## Train/Test Split & Normalization

### 🔧 Code

```python
# Chronological split — NEVER shuffle time series!
# 按时间顺序分割 — 时间序列绝不能随机打乱！
values = weekly['Temp'].values.reshape(-1, 1)
split = int(len(values) * 0.8)
train = values[:split]
test = values[split:]

# Min-Max normalization using ONLY training data
# 仅用训练集的 min/max 做归一化（避免数据泄露）
train_min = train.min()
train_max = train.max()
train_norm = (train - train_min) / (train_max - train_min)
test_norm = (test - train_min) / (train_max - train_min)  # ⚠️ Use TRAIN min/max!

# Create sliding window generators
# 创建滑动窗口生成器
# Each sample: 12-week input window → next week target
# 每个样本：12 周输入窗口 → 下一周目标
train_gen = TimeseriesGenerator(train_norm, train_norm,
                                length=WINDOW_SIZE, batch_size=BATCH_SIZE)
test_gen = TimeseriesGenerator(test_norm, test_norm,
                               length=WINDOW_SIZE, batch_size=BATCH_SIZE)
```

> ⚠️ **Data leakage trap:** Normalize test data using **training set's** min/max, NOT test set's own statistics.
>
> ⚠️ **数据泄露陷阱：** 用**训练集**的 min/max 归一化测试数据，不能用测试集自己的统计量。

---

## Dense Neural Network Model

### 🔧 Code

```python
# Dense (FFN) model — treats 12-week window as flat features
# 全连接网络 — 把 12 周窗口当作平坦特征，无序列概念
model_dense = Sequential([
    Flatten(input_shape=(WINDOW_SIZE, 1)),   # (12, 1) → 12
    Dense(64, activation='relu'),             # Hidden layer 1
    Dense(32, activation='relu'),             # Hidden layer 2
    Dense(1)                                  # Output: 1 temperature value
])

# Compile: Adam optimizer, MSE loss (regression), MAE metric
# 编译：Adam 优化器，MSE 损失（回归任务），MAE 指标
model_dense.compile(optimizer='adam', loss='mse', metrics=['mae'])

# Train / 训练
model_dense.fit(train_gen, epochs=EPOCHS, verbose=1)

# Predict & denormalize / 预测并反归一化
pred_dense_norm = model_dense.predict(test_gen)
pred_dense = pred_dense_norm * (train_max - train_min) + train_min
```

---

## SimpleRNN Model

### 🔧 Code

```python
# RNN model — processes input as SEQUENCE with memory
# RNN 模型 — 以序列方式处理输入，具有记忆能力
model_rnn = Sequential([
    # First RNN: return_sequences=True → pass full sequence to next RNN
    # 第一层 RNN：return_sequences=True → 传递完整序列给下一层
    SimpleRNN(64, activation='relu', return_sequences=True,
              input_shape=(WINDOW_SIZE, 1)),
    Dropout(0.2),          # 20% dropout — prevent overfitting / 防止过拟合

    # Second RNN: return_sequences=False → output only final hidden state
    # 第二层 RNN：return_sequences=False → 只输出最终隐藏状态
    SimpleRNN(32, activation='relu'),
    Dropout(0.2),

    Dense(64, activation='relu'),
    Dense(32, activation='relu'),
    Dense(1)               # Output: 1 temperature value
])

model_rnn.compile(optimizer='adam', loss='mse', metrics=['mae'])
model_rnn.fit(train_gen, epochs=EPOCHS, verbose=1)

pred_rnn_norm = model_rnn.predict(test_gen)
pred_rnn = pred_rnn_norm * (train_max - train_min) + train_min
```

> ⚠️ **`return_sequences` key rule:**
>
> - Stacking multiple RNN layers → all but last must have `return_sequences=True`
> - Last RNN (or only RNN) → `return_sequences=False` (default)
>
> ⚠️ **`return_sequences` 关键规则：**
>
> - 堆叠多层 RNN → 除最后一层外都设 `return_sequences=True`
> - 最后一层（或单层）→ `return_sequences=False`（默认）

---

## LSTM Model

### 🔧 Code

```python
# LSTM model — same structure as SimpleRNN but with gating mechanism
# LSTM 模型 — 结构同 SimpleRNN，但有门控机制
model_lstm = Sequential([
    LSTM(64, activation='tanh', return_sequences=True,
         input_shape=(WINDOW_SIZE, 1)),
    Dropout(0.2),
    LSTM(32, activation='tanh'),
    Dropout(0.2),
    Dense(64, activation='relu'),
    Dense(32, activation='relu'),
    Dense(1)
])

model_lstm.compile(optimizer='adam', loss='mse', metrics=['mae'])
model_lstm.fit(train_gen, epochs=EPOCHS, verbose=1)
```

> 💡 Simply replace `SimpleRNN` with `LSTM` — Keras handles all 3 gates + cell state internally.
>
> 💡 只需把 `SimpleRNN` 换成 `LSTM`——Keras 内部自动处理 3 个门 + 细胞状态。

---

## Prediction Visualization

### 🔧 Code

```python
# Plot original data + both model predictions
# 绘制原始数据 + 两个模型预测
plt.figure(figsize=(14, 6))
plt.plot(weekly.index, values, label='Original', color='blue')

# Denormalized predictions need to be aligned with test time indices
# 反归一化的预测需要对齐到测试时间索引
test_dates = weekly.index[split + WINDOW_SIZE:]
plt.plot(test_dates[:len(pred_dense)], pred_dense,
         label='Dense Prediction', color='red', linestyle='-')
plt.plot(test_dates[:len(pred_rnn)], pred_rnn,
         label='RNN Prediction', color='orange', linestyle='--')

# Train/test split line / 训练/测试分界线
plt.axvline(x=weekly.index[split], color='green', linestyle=':',
            label='Train/Test Split')

plt.title('Temperature Forecast: Dense vs RNN')
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.legend()
plt.show()
```

---

## Denormalization Formula

### 🔧 Code

```python
# Denormalize: reverse Min-Max scaling
# 反归一化：逆 Min-Max 缩放
# Formula 公式: original = normalized × (max - min) + min
prediction_original = prediction_normalized * (train_max - train_min) + train_min
```

> ⚠️ Must use **training set's** min/max for denormalization — same values used for normalization.
>
> ⚠️ 反归一化必须用**训练集**的 min/max——与归一化使用的相同值。

---

## Key API Cheat Sheet

### 🔧 Code

| API                       | 用途 (Usage)     | 关键参数 (Key Params)            |
| ------------------------- | ---------------- | -------------------------------- |
| `TimeseriesGenerator`     | 滑动窗口数据生成 | `length`=窗口大小, `batch_size`  |
| `Sequential`              | 堆叠式模型构建   | 传入 layer 列表                  |
| `SimpleRNN(n)`            | 简单循环层       | `return_sequences`, `activation` |
| `LSTM(n)`                 | LSTM 循环层      | 同 SimpleRNN，自带门控           |
| `Dense(n)`                | 全连接层         | `activation`                     |
| `Dropout(rate)`           | 随机丢弃防过拟合 | `rate`=丢弃比例 (0.2=20%)        |
| `Flatten()`               | 展平输入         | 用于 Dense 模型                  |
| `model.compile()`         | 配置优化器+损失  | `optimizer`, `loss`, `metrics`   |
| `model.fit()`             | 训练模型         | `epochs`, `verbose`              |
| `model.predict()`         | 生成预测         | 输出归一化值，需反归一化         |
| `seasonal_decompose()`    | 时间序列分解     | `model`, `period`                |
| `df.resample('W').mean()` | 重采样为周平均   | `'W'`=周, `'M'`=月               |

import os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import SimpleRNN, Dense, LSTM
from sklearn.model_selection import train_test_split

"""
RNN Complete Demo | 循环神经网络完整演示
Topic: Time Series Prediction (Sine Wave) | 话题：时间序列预测（正弦波）
"""

# 1. Setup paths | 设置路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "rnn_complete_demo_pages")
if not os.path.exists(ASSETS_DIR):
    os.makedirs(ASSETS_DIR)

def save_plot(filename):
    plt.tight_layout()
    plt.savefig(os.path.join(ASSETS_DIR, filename))
    print(f"✓ Saved plot to {filename}")
    plt.close()

# 2. Generate Synthetic Data | 生成合成数据
print("1. Generating sine wave data...")
t = np.linspace(0, 100, 1000)
data = np.sin(t) + 0.1 * np.random.randn(1000)  # Sine wave with noise

plt.figure(figsize=(10, 4))
plt.plot(t[:200], data[:200])
plt.title("Synthetic Sine Wave with Noise | 带噪正弦波")
plt.xlabel("Time")
plt.ylabel("Value")
save_plot("01_synthetic_data.png")

# 3. Data Preprocessing (Windowing) | 数据预处理（窗口化）
# We use the past N values to predict the next value
WINDOW_SIZE = 50

def create_sequences(data, window_size):
    X, y = [], []
    for i in range(len(data) - window_size):
        X.append(data[i:i + window_size])
        y.append(data[i + window_size])
    return np.array(X), np.array(y)

X, y = create_sequences(data, WINDOW_SIZE)

# RNN expects input shape: (samples, time_steps, features)
X = X.reshape((X.shape[0], X.shape[1], 1))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Build RNN Model | 构建 RNN 模型
print("2. Building Vanilla RNN model...")
model = Sequential([
    SimpleRNN(32, input_shape=(WINDOW_SIZE, 1), activation='tanh'),
    Dense(1)
])

model.compile(optimizer='adam', loss='mse')
print(model.summary())

# 5. Train Model | 训练模型
print("3. Training model...")
history = model.fit(X_train, y_train, epochs=20, batch_size=32, validation_split=0.1, verbose=0)

plt.figure(figsize=(10, 4))
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Val Loss')
plt.title("Training History | 训练历史")
plt.legend()
save_plot("02_training_history.png")

# 6. Prediction & Visualization | 预测与可视化
print("4. Making predictions...")
y_pred = model.predict(X_test, verbose=0)

plt.figure(figsize=(10, 4))
plt.plot(y_test[:100], label='Actual', alpha=0.7)
plt.plot(y_pred[:100], label='Predicted', alpha=0.7)
plt.title("RNN Prediction Result (First 100 samples) | 预测结果")
plt.legend()
save_plot("03_prediction_result.png")

# 7. Compare with LSTM | 与 LSTM 对比
print("5. Building LSTM model for comparison...")
lstm_model = Sequential([
    LSTM(32, input_shape=(WINDOW_SIZE, 1)),
    Dense(1)
])
lstm_model.compile(optimizer='adam', loss='mse')
lstm_history = lstm_model.fit(X_train, y_train, epochs=20, batch_size=32, validation_split=0.1, verbose=0)

plt.figure(figsize=(10, 4))
plt.plot(history.history['val_loss'], label='Vanilla RNN Val Loss')
plt.plot(lstm_history.history['val_loss'], label='LSTM Val Loss')
plt.title("Vanilla RNN vs LSTM | RNN 与 LSTM 对比")
plt.legend()
save_plot("04_comparison.png")

print("\n✓ Demo execution completed.")

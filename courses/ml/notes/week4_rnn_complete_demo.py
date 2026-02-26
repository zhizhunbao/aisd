"""
Week 4: RNN & LSTM Complete Demo
第四周：循环神经网络 & 长短期记忆网络 完整演示

Topics Covered 涵盖主题:
  1. Time Series Decomposition 时间序列分解
  2. Vanilla RNN from scratch 从零实现 RNN
  3. LSTM from scratch 从零实现 LSTM
  4. Keras SimpleRNN vs LSTM comparison 比较
  5. Vanishing Gradient visualization 梯度消失可视化
  6. Loss Functions comparison 损失函数对比

Dependencies 依赖:
  pip install numpy matplotlib tensorflow scikit-learn
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# ============================================================================
# Setup: Output directory for saved figures
# 设置：保存图片的输出目录
# ============================================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "week4_rnn_complete_demo_pages")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Reproducibility / 可重复性
np.random.seed(42)


# ============================================================================
# Part 1: Time Series Decomposition
# 第一部分：时间序列分解
# ============================================================================
def demo_time_series_decomposition():
    """
    Demonstrate time series components: Trend + Seasonal + Noise
    演示时间序列成分：趋势 + 季节性 + 噪声

    Key Concept 核心概念:
      Y(t) = Trend + Seasonal + Noise
      Any time series can be decomposed into these components.
      任何时间序列都可以分解为这些成分。
    """
    print("=" * 60)
    print("Part 1: Time Series Decomposition")
    print("第一部分：时间序列分解")
    print("=" * 60)

    # Generate synthetic time series with known components
    # 生成具有已知成分的合成时间序列
    t = np.arange(0, 200)

    # Trend: gradual upward slope / 趋势：逐渐上升
    trend = 0.05 * t

    # Seasonal: repeating cycle with period=52 (weekly in year)
    # 季节性：周期为 52 的重复循环（一年中的周）
    seasonal = 5 * np.sin(2 * np.pi * t / 52)

    # Noise: random fluctuations / 噪声：随机波动
    noise = np.random.normal(0, 1, len(t))

    # Combined signal / 合并信号
    y = trend + seasonal + noise + 10  # offset to keep positive

    fig, axes = plt.subplots(4, 1, figsize=(14, 10))
    fig.suptitle("Time Series Decomposition / 时间序列分解",
                 fontsize=16, fontweight='bold')

    # Original / 原始信号
    axes[0].plot(t, y, color='steelblue', linewidth=0.8)
    axes[0].set_title("Original = Trend + Seasonal + Noise")
    axes[0].set_ylabel("Value")

    # Trend / 趋势
    axes[1].plot(t, trend + 10, color='darkorange', linewidth=2)
    axes[1].set_title("Trend (Long-term direction / 长期方向)")
    axes[1].set_ylabel("Value")

    # Seasonal / 季节性
    axes[2].plot(t, seasonal, color='green', linewidth=1.5)
    axes[2].set_title("Seasonal (Fixed period / 固定周期)")
    axes[2].set_ylabel("Value")

    # Noise / 噪声
    axes[3].plot(t, noise, color='gray', linewidth=0.5, alpha=0.7)
    axes[3].set_title("Noise / Residual (Random / 随机)")
    axes[3].set_ylabel("Value")
    axes[3].set_xlabel("Time Step")

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "01_time_series_decomposition.png"),
                dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ Saved: 01_time_series_decomposition.png")

    return t, y


# ============================================================================
# Part 2: Vanilla RNN from Scratch
# 第二部分：从零实现 Vanilla RNN
# ============================================================================
def demo_vanilla_rnn():
    """
    Implement a single-layer RNN from scratch using numpy.
    从零使用 numpy 实现单层 RNN。

    Core Formula 核心公式:
      h_t = tanh(W_x · x_t + W_h · h_{t-1} + b)
      y_t = W_y · h_t + b_y

    This demonstrates:
      - Weight sharing across time steps / 权重在时间步间共享
      - Hidden state as memory / 隐藏状态作为记忆
      - Vanishing gradient problem / 梯度消失问题
    """
    print("\n" + "=" * 60)
    print("Part 2: Vanilla RNN from Scratch")
    print("第二部分：从零实现 Vanilla RNN")
    print("=" * 60)

    # --- Hyperparameters / 超参数 ---
    input_size = 1      # 1D input (temperature) / 1维输入（温度）
    hidden_size = 16     # Hidden state dimension / 隐藏状态维度
    output_size = 1      # 1D output (predicted temperature) / 1维输出
    seq_length = 20      # Sequence length / 序列长度

    # --- Initialize weights (Xavier initialization) ---
    # 初始化权重（Xavier 初始化）
    W_x = np.random.randn(hidden_size, input_size) * np.sqrt(2.0 / input_size)
    W_h = np.random.randn(hidden_size, hidden_size) * np.sqrt(2.0 / hidden_size)
    b_h = np.zeros((hidden_size, 1))
    W_y = np.random.randn(output_size, hidden_size) * np.sqrt(2.0 / hidden_size)
    b_y = np.zeros((output_size, 1))

    # --- Generate a simple sine wave sequence ---
    # 生成简单的正弦波序列
    t = np.linspace(0, 4 * np.pi, seq_length)
    x_seq = np.sin(t).reshape(-1, 1)  # shape: (seq_length, 1)

    # --- Forward pass / 前向传播 ---
    # h_t = tanh(W_x · x_t + W_h · h_{t-1} + b_h)
    h_prev = np.zeros((hidden_size, 1))  # h_0 = zero vector / 初始隐藏状态
    hidden_states = []                    # Store all h_t / 存储所有隐藏状态
    outputs = []

    for t_step in range(seq_length):
        x_t = x_seq[t_step].reshape(-1, 1)  # shape: (1, 1)

        # RNN core formula / RNN 核心公式
        # h_t = tanh(W_x · x_t + W_h · h_{t-1} + b_h)
        h_t = np.tanh(W_x @ x_t + W_h @ h_prev + b_h)

        # Output / 输出
        y_t = W_y @ h_t + b_y

        hidden_states.append(h_t.flatten())
        outputs.append(y_t.flatten()[0])
        h_prev = h_t  # Pass hidden state to next step / 传递隐藏状态

    hidden_states = np.array(hidden_states)
    outputs = np.array(outputs)

    # --- Visualize / 可视化 ---
    fig, axes = plt.subplots(2, 1, figsize=(14, 8))
    fig.suptitle("Vanilla RNN Forward Pass / 原始 RNN 前向传播",
                 fontsize=16, fontweight='bold')

    # Input vs Output / 输入 vs 输出
    axes[0].plot(x_seq, 'b-o', markersize=3, label='Input (sin wave)')
    axes[0].plot(outputs, 'r-s', markersize=3, label='RNN Output')
    axes[0].set_title("Input vs Output (random weights → random output)")
    axes[0].legend()
    axes[0].set_xlabel("Time Step")

    # Hidden state heatmap / 隐藏状态热力图
    im = axes[1].imshow(hidden_states.T, aspect='auto', cmap='RdBu_r',
                        interpolation='nearest')
    axes[1].set_title("Hidden State h_t across Time Steps / 隐藏状态随时间变化")
    axes[1].set_xlabel("Time Step")
    axes[1].set_ylabel("Hidden Dimension")
    plt.colorbar(im, ax=axes[1])

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "02_vanilla_rnn_forward.png"),
                dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ Saved: 02_vanilla_rnn_forward.png")


# ============================================================================
# Part 3: LSTM from Scratch
# 第三部分：从零实现 LSTM
# ============================================================================
def demo_lstm_from_scratch():
    """
    Implement a single LSTM cell forward pass from scratch.
    从零实现单个 LSTM 单元的前向传播。

    Core Formulas 核心公式:
      Step 1: f_t = σ(W_f · [h_{t-1}, x_t] + b_f)       Forget Gate / 遗忘门
      Step 2: i_t = σ(W_i · [h_{t-1}, x_t] + b_i)       Input Gate / 输入门
              C̃_t = tanh(W_C · [h_{t-1}, x_t] + b_C)    Candidate / 候选值
      Step 3: C_t = f_t ⊙ C_{t-1} + i_t ⊙ C̃_t          Cell State Update / 细胞状态更新
      Step 4: o_t = σ(W_o · [h_{t-1}, x_t] + b_o)       Output Gate / 输出门
              h_t = o_t ⊙ tanh(C_t)                      Hidden State / 隐藏状态
    """
    print("\n" + "=" * 60)
    print("Part 3: LSTM from Scratch")
    print("第三部分：从零实现 LSTM")
    print("=" * 60)

    def sigmoid(x):
        """Sigmoid activation: σ(x) = 1/(1+e^(-x)), output (0,1)"""
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))

    # --- Hyperparameters / 超参数 ---
    input_size = 1
    hidden_size = 8
    seq_length = 30

    # --- Initialize LSTM weights ---
    # 初始化 LSTM 权重
    # Each gate has weights for [h_{t-1}, x_t] concatenation
    # 每个门有 [h_{t-1}, x_t] 拼接的权重
    concat_size = hidden_size + input_size
    scale = np.sqrt(2.0 / concat_size)

    # Forget gate weights / 遗忘门权重
    W_f = np.random.randn(hidden_size, concat_size) * scale
    b_f = np.ones((hidden_size, 1))  # ⚠️ Bias=1 → initial f_t ≈ 1 (keep memory)

    # Input gate weights / 输入门权重
    W_i = np.random.randn(hidden_size, concat_size) * scale
    b_i = np.zeros((hidden_size, 1))

    # Candidate weights / 候选值权重
    W_C = np.random.randn(hidden_size, concat_size) * scale
    b_C = np.zeros((hidden_size, 1))

    # Output gate weights / 输出门权重
    W_o = np.random.randn(hidden_size, concat_size) * scale
    b_o = np.zeros((hidden_size, 1))

    # --- Generate sequence / 生成序列 ---
    t = np.linspace(0, 6 * np.pi, seq_length)
    x_seq = np.sin(t).reshape(-1, 1)

    # --- Forward pass / 前向传播 ---
    h_prev = np.zeros((hidden_size, 1))
    C_prev = np.zeros((hidden_size, 1))

    gate_values = {'forget': [], 'input': [], 'output': []}
    cell_states = []
    hidden_states = []

    for step in range(seq_length):
        x_t = x_seq[step].reshape(-1, 1)

        # Concatenate [h_{t-1}, x_t] / 拼接 [h_{t-1}, x_t]
        concat = np.vstack([h_prev, x_t])

        # Step 1: Forget Gate / 遗忘门
        # f_t = σ(W_f · [h_{t-1}, x_t] + b_f)
        f_t = sigmoid(W_f @ concat + b_f)

        # Step 2: Input Gate + Candidate / 输入门 + 候选值
        # i_t = σ(W_i · [h_{t-1}, x_t] + b_i)
        i_t = sigmoid(W_i @ concat + b_i)
        # C̃_t = tanh(W_C · [h_{t-1}, x_t] + b_C)
        C_tilde = np.tanh(W_C @ concat + b_C)

        # Step 3: Update Cell State / 更新细胞状态
        # C_t = f_t ⊙ C_{t-1} + i_t ⊙ C̃_t
        # ⚠️ Key: element-wise multiply + addition (NOT matrix multiply)
        # ⚠️ 关键：逐元素乘法 + 加法（不是矩阵乘法）
        C_t = f_t * C_prev + i_t * C_tilde

        # Step 4: Output Gate + Hidden State / 输出门 + 隐藏状态
        # o_t = σ(W_o · [h_{t-1}, x_t] + b_o)
        o_t = sigmoid(W_o @ concat + b_o)
        # h_t = o_t ⊙ tanh(C_t)
        h_t = o_t * np.tanh(C_t)

        # Store values / 存储值
        gate_values['forget'].append(f_t.mean())
        gate_values['input'].append(i_t.mean())
        gate_values['output'].append(o_t.mean())
        cell_states.append(C_t.flatten())
        hidden_states.append(h_t.flatten())

        h_prev = h_t
        C_prev = C_t

    # --- Visualize LSTM internals / 可视化 LSTM 内部 ---
    fig, axes = plt.subplots(3, 1, figsize=(14, 12))
    fig.suptitle("LSTM Internal States / LSTM 内部状态",
                 fontsize=16, fontweight='bold')

    # Gate activations / 门激活值
    axes[0].plot(gate_values['forget'], 'r-', linewidth=2, label='Forget Gate (遗忘门)')
    axes[0].plot(gate_values['input'], 'g-', linewidth=2, label='Input Gate (输入门)')
    axes[0].plot(gate_values['output'], 'b-', linewidth=2, label='Output Gate (输出门)')
    axes[0].set_title("Gate Activations (avg across dimensions) / 门激活值")
    axes[0].set_ylabel("Activation (0-1)")
    axes[0].legend()
    axes[0].axhline(y=0.5, color='gray', linestyle='--', alpha=0.5)

    # Cell state heatmap / 细胞状态热力图
    cell_arr = np.array(cell_states)
    im1 = axes[1].imshow(cell_arr.T, aspect='auto', cmap='RdBu_r',
                         interpolation='nearest')
    axes[1].set_title("Cell State C_t (The 'Highway') / 细胞状态（'高速公路'）")
    axes[1].set_ylabel("Dimension")
    plt.colorbar(im1, ax=axes[1])

    # Hidden state heatmap / 隐藏状态热力图
    hidden_arr = np.array(hidden_states)
    im2 = axes[2].imshow(hidden_arr.T, aspect='auto', cmap='viridis',
                         interpolation='nearest')
    axes[2].set_title("Hidden State h_t (Output) / 隐藏状态（输出）")
    axes[2].set_xlabel("Time Step")
    axes[2].set_ylabel("Dimension")
    plt.colorbar(im2, ax=axes[2])

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "03_lstm_internals.png"),
                dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ Saved: 03_lstm_internals.png")


# ============================================================================
# Part 4: Vanishing Gradient Visualization
# 第四部分：梯度消失可视化
# ============================================================================
def demo_vanishing_gradient():
    """
    Visualize why vanilla RNN suffers from vanishing gradients.
    可视化 Vanilla RNN 为什么会梯度消失。

    Key Insight 核心洞察:
      Gradient at step 1 = ∏(t=2 to T) ∂h_t/∂h_{t-1}
      Each factor ≈ tanh'(·) × W_h, where tanh' ∈ (0, 1]
      Product of many values < 1 → exponentially shrinks to 0
      多个 < 1 的值相乘 → 指数级衰减到 0
    """
    print("\n" + "=" * 60)
    print("Part 4: Vanishing Gradient Visualization")
    print("第四部分：梯度消失可视化")
    print("=" * 60)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Vanishing Gradient Problem / 梯度消失问题",
                 fontsize=16, fontweight='bold')

    # --- Plot 1: tanh vs sigmoid derivatives ---
    # 图 1：tanh 和 sigmoid 的导数
    x = np.linspace(-5, 5, 200)

    # Sigmoid and its derivative
    sig = 1 / (1 + np.exp(-x))
    sig_deriv = sig * (1 - sig)

    # Tanh and its derivative
    tanh_val = np.tanh(x)
    tanh_deriv = 1 - tanh_val ** 2

    axes[0, 0].plot(x, sig, 'b-', linewidth=2, label='σ(x)')
    axes[0, 0].plot(x, sig_deriv, 'b--', linewidth=2, label="σ'(x), max=0.25")
    axes[0, 0].plot(x, tanh_val, 'r-', linewidth=2, label='tanh(x)')
    axes[0, 0].plot(x, tanh_deriv, 'r--', linewidth=2, label="tanh'(x), max=1.0")
    axes[0, 0].set_title("Activation Functions & Derivatives / 激活函数及导数")
    axes[0, 0].legend(fontsize=9)
    axes[0, 0].axhline(y=0, color='gray', linewidth=0.5)
    axes[0, 0].axhline(y=0.25, color='blue', linewidth=0.5, linestyle=':',
                        alpha=0.5)
    axes[0, 0].set_xlabel("x")

    # --- Plot 2: Gradient magnitude over time steps ---
    # 图 2：梯度幅度随时间步的变化
    time_steps = np.arange(1, 101)
    gradient_05 = 0.5 ** time_steps   # avg tanh' = 0.5
    gradient_09 = 0.9 ** time_steps   # avg tanh' = 0.9
    gradient_025 = 0.25 ** time_steps  # sigmoid max

    axes[0, 1].semilogy(time_steps, gradient_05, 'r-', linewidth=2,
                        label='factor=0.5 (tanh avg)')
    axes[0, 1].semilogy(time_steps, gradient_09, 'g-', linewidth=2,
                        label='factor=0.9 (best case)')
    axes[0, 1].semilogy(time_steps, gradient_025, 'b-', linewidth=2,
                        label='factor=0.25 (sigmoid max)')
    axes[0, 1].set_title("Gradient Magnitude vs Time Steps / 梯度幅度随时间步")
    axes[0, 1].set_xlabel("Time Steps Back")
    axes[0, 1].set_ylabel("Gradient Magnitude (log scale)")
    axes[0, 1].legend(fontsize=9)
    axes[0, 1].axhline(y=1e-7, color='gray', linestyle='--', alpha=0.5,
                        label='Machine precision threshold')

    # --- Plot 3: LSTM vs RNN gradient comparison ---
    # 图 3：LSTM vs RNN 梯度对比
    # LSTM: when forget gate ≈ 1, gradient ≈ 1 for all steps
    lstm_gradient = np.ones(100) * 0.95  # f_t ≈ 0.95
    lstm_gradient_cum = np.cumprod(lstm_gradient)

    rnn_gradient = np.ones(100) * 0.5
    rnn_gradient_cum = np.cumprod(rnn_gradient)

    axes[1, 0].semilogy(time_steps, rnn_gradient_cum, 'r-', linewidth=2,
                        label='RNN (tanh chain)')
    axes[1, 0].semilogy(time_steps, lstm_gradient_cum, 'g-', linewidth=2,
                        label='LSTM (f_t ≈ 0.95)')
    axes[1, 0].set_title("LSTM vs RNN: Gradient Preservation / 梯度保持对比")
    axes[1, 0].set_xlabel("Time Steps Back")
    axes[1, 0].set_ylabel("Gradient Magnitude")
    axes[1, 0].legend(fontsize=9)

    # --- Plot 4: Additive vs Multiplicative paths ---
    # 图 4：加法路径 vs 乘法路径
    steps = np.arange(1, 51)
    # Multiplicative: s_t = α^t · s_0
    mult_08 = 0.8 ** steps
    mult_12 = 1.2 ** steps
    # Additive: s_t = s_0 + t·δ (gradient ∂s_t/∂s_0 = 1, always!)
    add_path = np.ones(50)  # gradient = 1 regardless of distance

    axes[1, 1].plot(steps, mult_08, 'r-', linewidth=2,
                    label='Multiplicative (α=0.8) → vanish')
    axes[1, 1].plot(steps, mult_12, 'b-', linewidth=2,
                    label='Multiplicative (α=1.2) → explode')
    axes[1, 1].plot(steps, add_path, 'g-', linewidth=3,
                    label='Additive (LSTM cell state) → stable!')
    axes[1, 1].set_title("Additive vs Multiplicative Path / 加法 vs 乘法路径")
    axes[1, 1].set_xlabel("Time Steps")
    axes[1, 1].set_ylabel("∂s_t / ∂s_0")
    axes[1, 1].legend(fontsize=9)
    axes[1, 1].set_ylim(-0.1, 3)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "04_vanishing_gradient.png"),
                dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ Saved: 04_vanishing_gradient.png")


# ============================================================================
# Part 5: Loss Functions Comparison
# 第五部分：损失函数对比
# ============================================================================
def demo_loss_functions():
    """
    Visualize and compare regression and classification loss functions.
    可视化和对比回归与分类的损失函数。

    Covered 涵盖:
      - MSE (Mean Squared Error) / 均方误差
      - MAE (Mean Absolute Error) / 平均绝对误差
      - Cross Entropy / 交叉熵
      - Hinge Loss / 合页损失
    """
    print("\n" + "=" * 60)
    print("Part 5: Loss Functions Comparison")
    print("第五部分：损失函数对比")
    print("=" * 60)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Loss Functions / 损失函数", fontsize=16, fontweight='bold')

    # --- Regression Losses ---
    errors = np.linspace(-5, 5, 200)

    # MSE: (y - ŷ)² — penalizes large errors more
    mse = errors ** 2
    # MAE: |y - ŷ| — linear penalty, robust to outliers
    mae = np.abs(errors)

    axes[0, 0].plot(errors, mse, 'r-', linewidth=2, label='MSE = (y-ŷ)²')
    axes[0, 0].plot(errors, mae, 'b-', linewidth=2, label='MAE = |y-ŷ|')
    axes[0, 0].set_title("MSE vs MAE / 均方误差 vs 平均绝对误差")
    axes[0, 0].set_xlabel("Error (y - ŷ)")
    axes[0, 0].set_ylabel("Loss")
    axes[0, 0].legend()
    axes[0, 0].set_ylim(0, 15)

    # --- MSE sensitivity to outliers ---
    np.random.seed(42)
    y_true = np.array([10, 12, 11, 13, 12, 11, 10, 50])  # outlier at 50
    y_pred = np.array([10, 12, 11, 13, 12, 11, 10, 12])

    mse_per_sample = (y_true - y_pred) ** 2
    mae_per_sample = np.abs(y_true - y_pred)

    x_pos = np.arange(len(y_true))
    bar_width = 0.35

    bars1 = axes[0, 1].bar(x_pos - bar_width/2, mse_per_sample, bar_width,
                           label='MSE loss', color='salmon')
    bars2 = axes[0, 1].bar(x_pos + bar_width/2, mae_per_sample, bar_width,
                           label='MAE loss', color='skyblue')
    axes[0, 1].set_title("Outlier Sensitivity / 离群值敏感度")
    axes[0, 1].set_xlabel("Sample Index")
    axes[0, 1].set_ylabel("Loss per Sample")
    axes[0, 1].legend()
    axes[0, 1].annotate("Outlier!\n离群值!",
                        xy=(7, mse_per_sample[7]),
                        xytext=(6, mse_per_sample[7] * 0.8),
                        arrowprops=dict(arrowstyle='->', color='red'),
                        fontsize=10, color='red')

    # --- Cross Entropy ---
    # CE = -y · log(ŷ) for binary case where y=1
    y_hat = np.linspace(0.01, 0.99, 200)
    ce_loss = -np.log(y_hat)  # when true label = 1

    axes[1, 0].plot(y_hat, ce_loss, 'purple', linewidth=2)
    axes[1, 0].set_title("Binary Cross Entropy (true class=1) / 二元交叉熵")
    axes[1, 0].set_xlabel("Predicted Probability ŷ")
    axes[1, 0].set_ylabel("Loss = -log(ŷ)")
    axes[1, 0].axvline(x=0.5, color='gray', linestyle='--', alpha=0.5)
    axes[1, 0].annotate("High loss when\nconfident & wrong\n自信且错误时\n损失很大",
                        xy=(0.1, 2.3), fontsize=10, color='darkred')

    # --- Hinge Loss ---
    # Hinge = max(0, 1 - y·ŷ), where y ∈ {-1, +1}
    y_hat_raw = np.linspace(-3, 3, 200)
    hinge_pos = np.maximum(0, 1 - y_hat_raw)   # y = +1
    hinge_neg = np.maximum(0, 1 + y_hat_raw)    # y = -1

    axes[1, 1].plot(y_hat_raw, hinge_pos, 'green', linewidth=2,
                    label='True class = +1')
    axes[1, 1].plot(y_hat_raw, hinge_neg, 'red', linewidth=2,
                    label='True class = -1')
    axes[1, 1].set_title("Hinge Loss (SVM) / 合页损失")
    axes[1, 1].set_xlabel("Raw Prediction ŷ")
    axes[1, 1].set_ylabel("Loss")
    axes[1, 1].legend()
    axes[1, 1].axvline(x=0, color='gray', linestyle='--', alpha=0.5)
    axes[1, 1].annotate("⚠️ Labels must be\n-1 and +1, NOT 0/1!\n标签必须是-1和+1!",
                        xy=(1.5, 2), fontsize=10, color='darkred',
                        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "05_loss_functions.png"),
                dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ Saved: 05_loss_functions.png")


# ============================================================================
# Part 6: RNN Architecture Comparison (Input-Output Types)
# 第六部分：RNN 架构对比（输入输出类型）
# ============================================================================
def demo_rnn_architectures():
    """
    Visualize the 4 RNN input-output configuration types.
    可视化 4 种 RNN 输入输出配置。

    Types 类型:
      1-to-1: Classification / 分类
      1-to-N: Image Captioning / 图像描述
      N-to-1: Sentiment Analysis / 情感分析
      N-to-N: Translation / 翻译
    """
    print("\n" + "=" * 60)
    print("Part 6: RNN Architecture Types")
    print("第六部分：RNN 架构类型")
    print("=" * 60)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("RNN Input-Output Types / RNN 输入输出类型",
                 fontsize=16, fontweight='bold')

    configs = [
        ("One-to-One (1:1)\nClassification / 分类",
         [1], [1], 'steelblue'),
        ("One-to-Many (1:N)\nImage Captioning / 图像描述",
         [1], [1, 2, 3, 4], 'darkorange'),
        ("Many-to-One (N:1)\nSentiment Analysis / 情感分析",
         [1, 2, 3, 4], [1], 'forestgreen'),
        ("Many-to-Many (N:N)\nTranslation / 翻译",
         [1, 2, 3, 4], [1, 2, 3, 4], 'purple'),
    ]

    for ax, (title, inputs, outputs, color) in zip(axes.flat, configs):
        # Draw input nodes
        n_in = len(inputs)
        n_out = len(outputs)

        for i, inp in enumerate(inputs):
            x_pos = i / max(n_in - 1, 1) if n_in > 1 else 0.5
            ax.scatter(x_pos, 0, s=300, color=color, zorder=5, edgecolors='black')
            ax.annotate(f'x{inp}', (x_pos, -0.15), ha='center', fontsize=10)

        # Draw output nodes
        for i, out in enumerate(outputs):
            x_pos = i / max(n_out - 1, 1) if n_out > 1 else 0.5
            ax.scatter(x_pos, 1, s=300, color=color, marker='s',
                      zorder=5, edgecolors='black')
            ax.annotate(f'y{out}', (x_pos, 1.15), ha='center', fontsize=10)

        # Draw RNN box in middle
        ax.add_patch(plt.Rectangle((0.2, 0.35), 0.6, 0.3,
                                    facecolor=color, alpha=0.2,
                                    edgecolor=color, linewidth=2))
        ax.text(0.5, 0.5, 'RNN', ha='center', va='center',
                fontsize=14, fontweight='bold', color=color)

        # Draw arrows
        for i in range(n_in):
            x_pos = i / max(n_in - 1, 1) if n_in > 1 else 0.5
            ax.annotate('', xy=(x_pos, 0.35), xytext=(x_pos, 0.05),
                       arrowprops=dict(arrowstyle='->', color='gray', lw=1.5))
        for i in range(n_out):
            x_pos = i / max(n_out - 1, 1) if n_out > 1 else 0.5
            ax.annotate('', xy=(x_pos, 0.95), xytext=(x_pos, 0.65),
                       arrowprops=dict(arrowstyle='->', color='gray', lw=1.5))

        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.set_xlim(-0.3, 1.3)
        ax.set_ylim(-0.4, 1.4)
        ax.axis('off')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "06_rnn_architectures.png"),
                dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ Saved: 06_rnn_architectures.png")


# ============================================================================
# Part 7: Keras RNN vs LSTM Comparison on Synthetic Data
# 第七部分：Keras RNN vs LSTM 在合成数据上的对比
# ============================================================================
def demo_keras_comparison():
    """
    Compare SimpleRNN and LSTM on a synthetic sequence prediction task.
    在合成序列预测任务上对比 SimpleRNN 和 LSTM。

    Uses Keras Sequential API — same pattern as Lab4.
    使用 Keras Sequential API——与 Lab4 相同的模式。
    """
    print("\n" + "=" * 60)
    print("Part 7: Keras SimpleRNN vs LSTM")
    print("第七部分：Keras SimpleRNN vs LSTM 对比")
    print("=" * 60)

    try:
        import tensorflow as tf
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import SimpleRNN, LSTM, Dense, Dropout

        tf.random.set_seed(42)
    except ImportError:
        print("⚠️ TensorFlow not installed. Skipping Keras demo.")
        print("   Run: pip install tensorflow")
        return

    # --- Generate synthetic data: sum of two sine waves ---
    # 生成合成数据：两个正弦波的叠加
    t = np.linspace(0, 20 * np.pi, 500)
    data = np.sin(t) + 0.5 * np.sin(3 * t) + 0.3 * np.random.randn(len(t))

    # --- Prepare sequences / 准备序列 ---
    window = 20
    X, y = [], []
    for i in range(len(data) - window):
        X.append(data[i:i+window])
        y.append(data[i+window])
    X = np.array(X).reshape(-1, window, 1)
    y = np.array(y)

    # Train/test split / 训练/测试分割
    split = int(len(X) * 0.8)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    # --- Build models / 构建模型 ---
    # SimpleRNN model
    model_rnn = Sequential([
        SimpleRNN(32, activation='tanh', return_sequences=True,
                  input_shape=(window, 1)),
        Dropout(0.2),
        SimpleRNN(16, activation='tanh'),
        Dropout(0.2),
        Dense(1)
    ])
    model_rnn.compile(optimizer='adam', loss='mse')

    # LSTM model
    model_lstm = Sequential([
        LSTM(32, activation='tanh', return_sequences=True,
             input_shape=(window, 1)),
        Dropout(0.2),
        LSTM(16, activation='tanh'),
        Dropout(0.2),
        Dense(1)
    ])
    model_lstm.compile(optimizer='adam', loss='mse')

    # --- Train / 训练 ---
    print("Training SimpleRNN...")
    hist_rnn = model_rnn.fit(X_train, y_train, epochs=30,
                             validation_split=0.1, verbose=0)
    print("Training LSTM...")
    hist_lstm = model_lstm.fit(X_train, y_train, epochs=30,
                               validation_split=0.1, verbose=0)

    # --- Predict / 预测 ---
    pred_rnn = model_rnn.predict(X_test, verbose=0).flatten()
    pred_lstm = model_lstm.predict(X_test, verbose=0).flatten()

    # --- Visualize / 可视化 ---
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))
    fig.suptitle("Keras: SimpleRNN vs LSTM / Keras 对比",
                 fontsize=16, fontweight='bold')

    # Predictions
    test_range = np.arange(len(y_test))
    axes[0].plot(test_range, y_test, 'b-', linewidth=1, label='True', alpha=0.7)
    axes[0].plot(test_range, pred_rnn, 'r--', linewidth=1.5,
                 label=f'SimpleRNN (MSE={np.mean((pred_rnn-y_test)**2):.4f})')
    axes[0].plot(test_range, pred_lstm, 'g--', linewidth=1.5,
                 label=f'LSTM (MSE={np.mean((pred_lstm-y_test)**2):.4f})')
    axes[0].set_title("Test Set Predictions / 测试集预测")
    axes[0].legend()
    axes[0].set_xlabel("Sample")
    axes[0].set_ylabel("Value")

    # Training loss
    axes[1].plot(hist_rnn.history['loss'], 'r-', linewidth=2,
                 label='SimpleRNN train loss')
    axes[1].plot(hist_rnn.history['val_loss'], 'r--', linewidth=1,
                 label='SimpleRNN val loss')
    axes[1].plot(hist_lstm.history['loss'], 'g-', linewidth=2,
                 label='LSTM train loss')
    axes[1].plot(hist_lstm.history['val_loss'], 'g--', linewidth=1,
                 label='LSTM val loss')
    axes[1].set_title("Training Loss / 训练损失")
    axes[1].set_xlabel("Epoch")
    axes[1].set_ylabel("MSE Loss")
    axes[1].legend()

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "07_keras_rnn_vs_lstm.png"),
                dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ Saved: 07_keras_rnn_vs_lstm.png")


# ============================================================================
# Main: Run all demos
# 主函数：运行所有演示
# ============================================================================
if __name__ == "__main__":
    print("🧠 Week 4: RNN & LSTM Complete Demo")
    print("=" * 60)

    demo_time_series_decomposition()
    demo_vanilla_rnn()
    demo_lstm_from_scratch()
    demo_vanishing_gradient()
    demo_loss_functions()
    demo_rnn_architectures()
    demo_keras_comparison()

    print("\n" + "=" * 60)
    print("✅ All demos complete!")
    print(f"📁 Output saved to: {OUTPUT_DIR}")
    print("=" * 60)

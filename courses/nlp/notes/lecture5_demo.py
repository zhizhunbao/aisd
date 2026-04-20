# %%
# ============================================================
# 工具函数（唯一共享单元）
# Utility Functions (Only shared cell)
# ============================================================
# 设计: 每个概念单元格均自包含 — 数据和辅助函数在单元格内定义,
#       唯一共享: import math 和 ptable() 格式化输出。
# Design: Each concept cell is fully self-contained.
#         Only shared: import math + ptable() for formatted output.
# ============================================================
import math
import tabulate as _tabulate_mod
_tabulate_mod.WIDE_CHARS_MODE = True  # 修复中文对齐 / Fix CJK alignment
from tabulate import tabulate as _tabulate_fn

def ptable(rows, **kwargs):
    """格式化表格输出 / Formatted table output"""
    print(_tabulate_fn(rows, **kwargs, tablefmt="simple_grid"))

print("✅ 工具函数已加载 — 以下30个概念单元格均可独立运行")


# %%
# ============================================================
# 概念01：神经元 / 感知器
# Concept 01: Neuron / Perceptron
# ============================================================
# 定义：神经网络的最小计算单元。
#       接收一组数字 → 加权求和 → 加偏置 → 过激活函数 → 输出一个数字。
# Definition: The smallest computing unit. y = f(w·x + b)
# ============================================================

# ── 本单元自包含数据 ──
# 输入向量："students" 的4维嵌入 / Input: "students" 4-dim embedding
x_test = [0.80, 0.50, 0.30, 0.70]
# 权重向量：每维输入的重要程度 / Weights: importance of each input dim
w_test = [0.2, 0.7, -0.1, 0.3]
# 偏置：即使输入全零也能产生输出 / Bias: ensures output even when input=0
b_test = 0.1

def neuron(x, w, b):
    """一个神经元的完整前向计算 / Forward pass of a single neuron"""
    z = sum(xi * wi for xi, wi in zip(x, w)) + b
    return math.tanh(z)

ptable([
    ["输入 Input", f"'students' → {x_test}"],
    ["权重 Weights", f"{w_test}"],
    ["偏置 Bias", f"{b_test}"],
    ["输出 Output", f"{neuron(x_test, w_test, b_test):.4f}"],
], headers=["概念01: 神经元", "值"])


# %%
# ============================================================
# 概念02：权重
# Concept 02: Weights
# ============================================================
# 定义：神经元内部的可学习参数，决定每个输入的重要程度。
# Definition: Learnable parameters that control each input's importance.
# ============================================================

# ── 本单元自包含数据 ──
# 权重向量：正值=正相关，负值=反相关 / Weights: +corr, -corr
weights_demo = [0.2, 0.7, -0.1, 0.3]
# 输入向量："students" 的4维嵌入 / Input: "students" embedding
x_demo = [0.80, 0.50, 0.30, 0.70]

rows = []
for i, (xi, wi) in enumerate(zip(x_demo, weights_demo)):
    rows.append([f"维度{i}", f"{xi:.2f}", f"{wi:.2f}", f"{xi*wi:+.3f}"])
rows.append(["总和", "", "", f"{sum(xi*wi for xi,wi in zip(x_demo, weights_demo)):.4f}"])
ptable(rows, headers=["概念02: 权重", "输入", "权重", "贡献"])


# %%
# ============================================================
# 概念03：偏置
# Concept 03: Bias
# ============================================================
# 定义：加在加权求和上的额外常数 (类似 y=kx+b 的截距)。
# Definition: A constant added after weighted sum. Like intercept in y=kx+b.
# ============================================================

# 全零输入：演示偏置的作用 / All-zero input: shows why bias matters
x_zero = [0.0, 0.0, 0.0, 0.0]
# 任意权重（全零输入时不影响结果）/ Any weights (irrelevant when input=0)
w_any = [0.5, 0.3, -0.2, 0.1]
# 偏置值 / Bias value
bias = 0.3
# 加权和: Σ(xi×wi)，全零输入时必为0 / Weighted sum: always 0 for zero input
ws = sum(xi*wi for xi,wi in zip(x_zero, w_any))
ptable([
    ["无偏置", f"{ws:.1f}", f"{math.tanh(ws):.4f}", "❌ 死了"],
    ["有偏置(b=0.3)", f"{ws+bias:.1f}", f"{math.tanh(ws+bias):.4f}", "✅ 有输出"],
], headers=["概念03: 偏置(全零输入)", "加权和", "tanh输出", "状态"])


# %%
# ============================================================
# 概念04：激活函数
# Concept 04: Activation Function
# ============================================================
# 定义：非线性函数，没有它多层坍缩为单层（见概念21）。
# Definition: Non-linear function. Without it, layers collapse (see Concept 21).
# ============================================================

def tanh(z):
    """tanh: (e^z - e^(-z)) / (e^z + e^(-z))，输出 (-1, 1)"""
    if z > 20: return 1.0
    if z < -20: return -1.0
    return (math.exp(z) - math.exp(-z)) / (math.exp(z) + math.exp(-z))

def sigmoid(z):
    """sigmoid: 1 / (1 + e^(-z))，输出 (0, 1)"""
    if z > 20: return 1.0
    if z < -20: return 0.0
    return 1.0 / (1.0 + math.exp(-z))

def relu(z):
    """ReLU: max(0, z)，负数归零"""
    return max(0.0, z)

rows = [[f"{z:+.1f}", f"{tanh(z):+.4f}", f"{sigmoid(z):.4f}", f"{relu(z):.1f}"]
        for z in [-2.0, 0.0, 1.0, 3.0]]
ptable(rows, headers=["概念04: z值", "tanh", "sigmoid", "ReLU"])


# %%
# ============================================================
# 概念05：点积 / 加权求和
# Concept 05: Dot Product / Weighted Sum
# ============================================================
# 定义：a·b = Σ(aᵢ×bᵢ)。方向相同→正, 相反→负, 垂直→0。
# Definition: Element-wise multiply then sum. Measures directional alignment.
# ============================================================

# ── 本单元自包含数据 ──
v_students = [0.80, 0.50, 0.30, 0.70]   # students 嵌入向量
v_books    = [0.75, 0.55, 0.35, 0.65]   # books 嵌入向量
v_cat      = [-0.30, 0.60, -0.50, 0.40]  # cat 嵌入向量

def dot_product(a, b):
    """纯Python点积 / Pure Python dot product"""
    return sum(ai * bi for ai, bi in zip(a, b))

ptable([
    ["students · books", f"{dot_product(v_students, v_books):.4f}", "高 → 语义相关 ✅"],
    ["students · cat",   f"{dot_product(v_students, v_cat):.4f}", "低 → 语义无关 ❌"],
], headers=["概念05: 点积", "值", "含义"])


# %%
# ============================================================
# 概念06：层
# Concept 06: Layer
# ============================================================
# 定义：多个神经元并排，各用不同权重分析同一输入。
# Definition: Multiple neurons in parallel, same input, different weights.
# ============================================================

# ── 本单元自包含数据与函数 ──
# 输入向量："students" 的4维嵌入 / Input: "students" embedding
v_students = [0.80, 0.50, 0.30, 0.70]

def tanh(z):
    if z > 20: return 1.0
    if z < -20: return -1.0
    return (math.exp(z) - math.exp(-z)) / (math.exp(z) + math.exp(-z))

def dot_product(a, b): return sum(ai * bi for ai, bi in zip(a, b))

# 权重矩阵：3个神经元×4维输入 → 3行4列 / Weight matrix: 3 neurons × 4 inputs
W_demo = [[ 0.5, 0.3,-0.2, 0.1],[-0.1, 0.4, 0.6, 0.2],[ 0.3,-0.5, 0.1, 0.7]]
# 偏置向量：每个神经元一个偏置 / Bias: one per neuron
b_demo = [0.1, -0.1, 0.05]

def layer(x, W, biases):
    """一层的前向计算 / Forward pass of one layer"""
    return [tanh(dot_product(x, W[i]) + biases[i]) for i in range(len(W))]

# 层输出：3个神经元各产生一个值 / Layer output: one value per neuron
out = layer(v_students, W_demo, b_demo)
ptable([
    [f"神经元{i}", f"{out[i]:.4f}"] for i in range(len(out))
], headers=["概念06: 层(输入=students)", "输出"])


# %%
# ============================================================
# 概念07：神经网络 = 多层叠加
# Concept 07: Neural Network = Stacked Layers
# ============================================================
# 定义：前一层输出作为后一层输入，层层抽象。
# Definition: Stack layers — output of one feeds into the next.
# ============================================================

# ── 本单元自包含数据与函数 ──
# 输入向量："students" 的4维嵌入 / Input: "students" embedding
v_students = [0.80, 0.50, 0.30, 0.70]

def tanh(z):
    if z > 20: return 1.0
    if z < -20: return -1.0
    return (math.exp(z) - math.exp(-z)) / (math.exp(z) + math.exp(-z))

def dot_product(a, b): return sum(ai * bi for ai, bi in zip(a, b))

def layer(x, W, biases):
    return [tanh(dot_product(x, W[i]) + biases[i]) for i in range(len(W))]

# 第1层：4维输入 → 3维输出 (3个神经元) / Layer1: 4d → 3d
L1_W = [[ 0.5, 0.3,-0.2, 0.1],[-0.1, 0.4, 0.6, 0.2],[ 0.3,-0.5, 0.1, 0.7]]
L1_b = [0.1, -0.1, 0.05]
# 第2层：3维输入 → 2维输出 (2个神经元) / Layer2: 3d → 2d
L2_W = [[ 0.4,-0.3, 0.2],[-0.2, 0.5, 0.1]]
L2_b = [0.05, -0.05]

def neural_network(x, layers_params):
    """多层前馈网络 / Multi-layer feedforward network"""
    current = x
    for (W, b) in layers_params:
        current = layer(current, W, b)
    return current

# 整个网络的最终输出 / Final output of the entire network
result = neural_network(v_students, [(L1_W, L1_b), (L2_W, L2_b)])
ptable([
    ["输入", "students 4维", f"{v_students}"],
    ["隐藏层", "→ 3维", f"{[f'{v:.4f}' for v in layer(v_students, L1_W, L1_b)]}"],
    ["输出层", "→ 2维", f"{[f'{v:.4f}' for v in result]}"],
], headers=["概念07: 神经网络", "维度变化", "值"])


# %%
# ============================================================
# 概念08：前馈 vs 循环
# Concept 08: Feedforward vs Recurrent
# ============================================================
# 前馈: 单行道无记忆。循环: 有回路有记忆。
# Feedforward: one-way, no memory. Recurrent: feedback loop.
# ============================================================

# ── 本单元自包含数据与函数 ──
# 输入向量："students" 的4维嵌入 / Input: "students" embedding
v_students = [0.80, 0.50, 0.30, 0.70]

def tanh(z):
    if z > 20: return 1.0
    if z < -20: return -1.0
    return (math.exp(z) - math.exp(-z)) / (math.exp(z) + math.exp(-z))

def dot_product(a, b): return sum(ai * bi for ai, bi in zip(a, b))

def layer(x, W, biases):
    return [tanh(dot_product(x, W[i]) + biases[i]) for i in range(len(W))]

# 输入→隐藏 权重：4维输入 → 2维隐藏 / Input-to-hidden weights: 4d → 2d
W_xh = [[0.3, 0.1, -0.2, 0.4],[0.1, -0.3, 0.2, 0.1]]
# 隐藏→隐藏 权重：上一步记忆的影响 / Hidden-to-hidden weights: memory
W_hh = [[0.5, -0.1],[0.2, 0.3]]
# 初始隐藏状态：全零=无记忆 / Initial hidden state: zero = no memory
h0 = [0.0, 0.0]

def feedforward_pass(x, W, b):
    """前馈：无记忆 / No memory"""
    return layer(x, W, b)

def recurrent_step(x, h_prev, W_xh, W_hh, b):
    """循环一步 / Input + previous hidden state"""
    z = [dot_product(x, W_xh[i]) + dot_product(h_prev, W_hh[i]) + b[i]
         for i in range(len(b))]
    return [tanh(zi) for zi in z]

# 前馈：同样的输入调用两次
# 前馈第1次输出 / Feedforward pass 1
ff1 = feedforward_pass(v_students, W_xh, [0.1, -0.1])
# 前馈第2次输出：结果应完全相同（无记忆）/ Pass 2: should equal ff1 (no memory)
ff2 = feedforward_pass(v_students, W_xh, [0.1, -0.1])

# 循环：同样的输入调用两次
# 循环第1步：初始记忆 h0=[0,0] / RNN step 1: starts from h0
h1 = recurrent_step(v_students, h0, W_xh, W_hh, [0.1, -0.1])
# 循环第2步：携带 h1 记忆 → 结果不同 / RNN step 2: carries h1 memory → different
h2 = recurrent_step(v_students, h1, W_xh, W_hh, [0.1, -0.1])

ptable([
    ["前馈 第1次", f"{[f'{v:.4f}' for v in ff1]}", ""],
    ["前馈 第2次", f"{[f'{v:.4f}' for v in ff2]}", f"相同={ff1==ff2} → 无记忆"],
    ["循环 第1步", f"{[f'{v:.4f}' for v in h1]}", "h0=[0,0]"],
    ["循环 第2步", f"{[f'{v:.4f}' for v in h2]}", f"相同={h1==h2} → 有记忆"],
], headers=["概念08: 前馈vs循环", "输出", "说明"])


# %%
# ============================================================
# 概念09：隐藏层
# Concept 09: Hidden Layer
# ============================================================
# 定义：夹在输入和输出之间，用户看不到中间值。
# Definition: Layer between input and output. "Hidden" = user can't see it.
# ============================================================

# ── 本单元自包含数据与函数 ──
# 输入向量："students" 的4维嵌入 / Input: "students" embedding
v_students = [0.80, 0.50, 0.30, 0.70]

def tanh(z):
    if z > 20: return 1.0
    if z < -20: return -1.0
    return (math.exp(z) - math.exp(-z)) / (math.exp(z) + math.exp(-z))

def dot_product(a, b): return sum(ai * bi for ai, bi in zip(a, b))

def layer(x, W, biases):
    return [tanh(dot_product(x, W[i]) + biases[i]) for i in range(len(W))]

# 隐藏层(W_h)：4维输入 → 3维隐藏 / Hidden layer: 4d → 3d
L1_W = [[ 0.5, 0.3,-0.2, 0.1],[-0.1, 0.4, 0.6, 0.2],[ 0.3,-0.5, 0.1, 0.7]]
L1_b = [0.1, -0.1, 0.05]
# 输出层(W_o)：3维隐藏 → 2维输出 / Output layer: 3d → 2d
L2_W = [[ 0.4,-0.3, 0.2],[-0.2, 0.5, 0.1]]
L2_b = [0.05, -0.05]

def network_with_hidden(x, W_h, b_h, W_o, b_o):
    """展示隐藏层 / Show hidden layer"""
    hidden = layer(x, W_h, b_h)
    output = layer(hidden, W_o, b_o)
    return hidden, output

# h=隐藏层输出（用户不可见）, o=输出层输出 / h=hidden, o=output
h, o = network_with_hidden(v_students, L1_W, L1_b, L2_W, L2_b)
ptable([
    ["输入层", f"{v_students}", "✅ 用户可见"],
    ["隐藏层", f"{[f'{v:.4f}' for v in h]}", "❌ 用户不可见"],
    ["输出层", f"{[f'{v:.4f}' for v in o]}", "✅ 用户可见"],
], headers=["概念09: 隐藏层", "值", "可见性"])


# %%
# ============================================================
# 概念10：隐藏层节点数（超参数）
# Concept 10: Hidden Layer Size (Hyperparameter)
# ============================================================
# 定义：由人选择。节点越多→容量越大，但更慢更易过拟合。
# Definition: Number of neurons. More = more capacity but slower.
# ============================================================

# ── 本单元自包含数据 ──
# 上下文窗口大小：用前 N 个词预测下一个词（N-gram 中的 N）
# Context window: use previous N words to predict next (N in N-gram)
CONTEXT_SIZE = 3

# 每个词的嵌入维度（每个词用 d 个数字表示）
# Embedding dimension: each word represented as d-dimensional vector
EMBED_DIM = 4

# 输入维度 = N个词 × 每词d维 → 拼接后的总长度
# Input dim = N words × d dims = length of concatenated vector
input_dim = CONTEXT_SIZE * EMBED_DIM  # 3×4 = 12

# 参数量公式：h×input_dim + h
#   h×input_dim = 每个神经元有 input_dim 个权重，共 h 个神经元
#   + h          = 每个神经元还有 1 个偏置，共 h 个
# Formula: h × input_dim (weights) + h (biases)
rows = [[f"{name}({h})", f"{h*input_dim+h:,}"]
        for name, h in [("极小",1),("小",10),("中",100),("大",1000)]]
ptable(rows, headers=[f"概念10: 节点数(输入{input_dim}维)", "参数量"])


# %%
# ============================================================
# 概念11：词嵌入 / 嵌入查找
# Concept 11: Word Embedding / Lookup
# ============================================================
# 定义：词→编号→取嵌入矩阵那一行。纯查表。
# Definition: Word → ID → fetch row. Pure lookup.
# ============================================================

# ── 本单元自包含数据 ──
VOCAB = ["the", "students", "opened", "their", "books",
         "cat", "sat", "on", "mat", "dog"]
WORD2ID = {w: i for i, w in enumerate(VOCAB)}
EMBEDDING_MATRIX = [
    [ 0.10,  0.20, -0.30,  0.05],
    [ 0.80,  0.50,  0.30,  0.70],
    [ 0.20, -0.40,  0.60,  0.10],
    [ 0.05,  0.15, -0.10,  0.25],
    [ 0.75,  0.55,  0.35,  0.65],
    [-0.30,  0.60, -0.50,  0.40],
    [ 0.15, -0.20,  0.45, -0.10],
    [ 0.05,  0.10,  0.05, -0.05],
    [ 0.30, -0.10,  0.20,  0.15],
    [-0.25,  0.55, -0.45,  0.35],
]
CONTEXT_WORDS = ["students", "opened", "their"]

def embedding_lookup(word):
    """词嵌入查找 / Word → ID → vector"""
    return EMBEDDING_MATRIX[WORD2ID[word]]

rows = [[w, WORD2ID[w], f"{embedding_lookup(w)}"] for w in CONTEXT_WORDS]
ptable(rows, headers=["概念11: 词嵌入查找", "编号", "向量"])


# %%
# ============================================================
# 概念12：嵌入矩阵
# Concept 12: Embedding Matrix
# ============================================================
# 定义：V×d 数组。每行=一个词的含义向量。可学习参数。
# Definition: V×d array. Each row = word's meaning. Learnable.
# ============================================================

# ── 本单元自包含数据 ──
VOCAB = ["the", "students", "opened", "their", "books",
         "cat", "sat", "on", "mat", "dog"]
VOCAB_SIZE = len(VOCAB)
EMBED_DIM = 4
EMBEDDING_MATRIX = [
    [ 0.10,  0.20, -0.30,  0.05],
    [ 0.80,  0.50,  0.30,  0.70],
    [ 0.20, -0.40,  0.60,  0.10],
    [ 0.05,  0.15, -0.10,  0.25],
    [ 0.75,  0.55,  0.35,  0.65],
    [-0.30,  0.60, -0.50,  0.40],
    [ 0.15, -0.20,  0.45, -0.10],
    [ 0.05,  0.10,  0.05, -0.05],
    [ 0.30, -0.10,  0.20,  0.15],
    [-0.25,  0.55, -0.45,  0.35],
]

rows = [[i, w, f"{EMBEDDING_MATRIX[i]}"] for i, w in enumerate(VOCAB)]
ptable(rows, headers=[f"概念12: 嵌入矩阵[{VOCAB_SIZE}×{EMBED_DIM}]", "词", "向量"])


# %%
# ============================================================
# 概念13：嵌入维度选择
# Concept 13: Embedding Dimension Choice
# ============================================================
# 定义：向量长度d。越高→语义越精细，参数越多。
# Definition: Higher d = finer semantics but more parameters.
# ============================================================

# ── 本单元自包含数据 ──
EMBED_DIM = 4

rows = [[m, d, f"{50000*d:,}"] for m,d in [("Word2Vec",300),("BERT",768),("GPT-3",12288),("本Demo",EMBED_DIM)]]
ptable(rows, headers=["概念13: 嵌入维度", "d", "参数量(V=50000)"])


# %%
# ============================================================
# 概念14：One-hot 编码
# Concept 14: One-hot Encoding
# ============================================================
# 定义：长度V向量，该词位置=1，其余=0。极稀疏。
# Definition: Vector of length V, 1 at word's index, 0 elsewhere.
# ============================================================

# ── 本单元自包含数据 ──
VOCAB = ["the", "students", "opened", "their", "books",
         "cat", "sat", "on", "mat", "dog"]
WORD2ID = {w: i for i, w in enumerate(VOCAB)}
VOCAB_SIZE = len(VOCAB)

def one_hot(word_id, vocab_size):
    """生成 one-hot 向量 / Generate one-hot vector"""
    vec = [0.0] * vocab_size
    vec[word_id] = 1.0
    return vec

rows = [[w, f"{one_hot(WORD2ID[w], VOCAB_SIZE)}"] for w in ["students","books","cat"]]
ptable(rows, headers=["概念14: One-hot", "向量"])
print("⚠️ students 和 books 的 one-hot 完全正交，无法体现语义相似!")


# %%
# ============================================================
# 概念15：嵌入来源（预训练 vs 随机初始化）
# Concept 15: Embedding Source (Pre-trained vs Random Init)
# ============================================================
# 预训练: Word2Vec/GloVe 大语料训好直接用。随机: 从零训练。
# ============================================================

ptable([
    ["预训练 students", "[0.80, 0.50, 0.30, 0.70]", "✅ 已有语义"],
    ["预训练 books",    "[0.75, 0.55, 0.35, 0.65]", "✅ 与student接近"],
    ["随机 students",   "[0.01, -0.02, 0.03, -0.01]", "❌ 无语义"],
    ["随机 books",      "[-0.02, 0.01, -0.03, 0.02]", "❌ 无语义"],
], headers=["概念15: 嵌入来源", "向量", "状态"])


# %%
# ============================================================
# 概念16：嵌入不可解释性（黑盒）
# Concept 16: Embedding Non-interpretability (Black Box)
# ============================================================
# 定义：每维含义不可解读，只能观察效果。
# Definition: Individual dimensions have no human-readable meaning.
# ============================================================

# ── 本单元自包含数据 ──
VOCAB = ["the", "students", "opened", "their", "books",
         "cat", "sat", "on", "mat", "dog"]
WORD2ID = {w: i for i, w in enumerate(VOCAB)}
EMBEDDING_MATRIX = [
    [ 0.10,  0.20, -0.30,  0.05],
    [ 0.80,  0.50,  0.30,  0.70],
    [ 0.20, -0.40,  0.60,  0.10],
    [ 0.05,  0.15, -0.10,  0.25],
    [ 0.75,  0.55,  0.35,  0.65],
    [-0.30,  0.60, -0.50,  0.40],
    [ 0.15, -0.20,  0.45, -0.10],
    [ 0.05,  0.10,  0.05, -0.05],
    [ 0.30, -0.10,  0.20,  0.15],
    [-0.25,  0.55, -0.45,  0.35],
]

def cosine_similarity(a, b):
    """余弦相似度 / Cosine similarity"""
    dot = sum(ai*bi for ai, bi in zip(a, b))
    norm_a = math.sqrt(sum(ai**2 for ai in a))
    norm_b = math.sqrt(sum(bi**2 for bi in b))
    if norm_a == 0 or norm_b == 0: return 0.0
    return dot / (norm_a * norm_b)

# 待比较词对列表 / Word pairs to compare similarity
pairs = [("students","books"),("cat","dog"),("students","cat"),("the","on")]
rows = []
for w1, w2 in pairs:
    sim = cosine_similarity(EMBEDDING_MATRIX[WORD2ID[w1]], EMBEDDING_MATRIX[WORD2ID[w2]])
    label = "语义近✅" if sim > 0.7 else "语义远❌" if sim < 0.3 else "一般"
    rows.append([f"{w1} ↔ {w2}", f"{sim:.4f}", label])
ptable(rows, headers=["概念16: 黑盒相似度", "cos_sim", "判定"])


# %%
# ============================================================
# 概念17：One-hot × 嵌入矩阵 = 查表
# Concept 17: One-hot × E = Lookup (Math Equivalence)
# ============================================================
# 教科书 e = one_hot·E 本质是取矩阵那一行。
# ============================================================

# ── 本单元自包含数据与函数 ──
VOCAB = ["the", "students", "opened", "their", "books",
         "cat", "sat", "on", "mat", "dog"]
WORD2ID = {w: i for i, w in enumerate(VOCAB)}
VOCAB_SIZE = len(VOCAB)
EMBEDDING_MATRIX = [
    [ 0.10,  0.20, -0.30,  0.05],
    [ 0.80,  0.50,  0.30,  0.70],
    [ 0.20, -0.40,  0.60,  0.10],
    [ 0.05,  0.15, -0.10,  0.25],
    [ 0.75,  0.55,  0.35,  0.65],
    [-0.30,  0.60, -0.50,  0.40],
    [ 0.15, -0.20,  0.45, -0.10],
    [ 0.05,  0.10,  0.05, -0.05],
    [ 0.30, -0.10,  0.20,  0.15],
    [-0.25,  0.55, -0.45,  0.35],
]

def one_hot(word_id, vocab_size):
    vec = [0.0] * vocab_size
    vec[word_id] = 1.0
    return vec

def mat_vec_multiply(matrix, vec):
    """vec × matrix"""
    result = [0.0] * len(matrix[0])
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            result[j] += vec[i] * matrix[i][j]
    return result

# "books" 的 one-hot 向量 / One-hot vector for "books"
oh = one_hot(WORD2ID["books"], VOCAB_SIZE)
# 矩阵乘法结果：one_hot × E / Result via matrix multiplication
r_mat = mat_vec_multiply(EMBEDDING_MATRIX, oh)
# 直接查表结果：E[books_id] / Result via direct index lookup
r_idx = EMBEDDING_MATRIX[WORD2ID["books"]]
ptable([
    ["one-hot × E", f"{r_mat}"],
    ["直接查表 E[4]", f"{r_idx}"],
    ["完全相同?", f"{r_mat == r_idx}"],
], headers=["概念17: 数学等价", "'books'结果"])


# %%
# ============================================================
# 概念18：语言模型任务定义
# Concept 18: Language Model Task Definition
# ============================================================
# 定义：给定前N个词，预测下一个词的概率分布。
# Definition: Given N previous words, predict P(next word).
# ============================================================

# ── 本单元自包含数据 ──
CONTEXT_WORDS = ["students", "opened", "their"]
CONTEXT_SIZE = 3
TARGET_WORD = "books"
VOCAB_SIZE = 10

ptable([
    ["输入上下文", f"{CONTEXT_WORDS}"],
    ["窗口大小 N", f"{CONTEXT_SIZE}"],
    ["预测目标", f"P('{TARGET_WORD}' | context)"],
    ["输出形式", f"{VOCAB_SIZE}个概率，总和=1"],
], headers=["概念18: 语言模型任务", "值"])


# %%
# ============================================================
# 概念19：拼接
# Concept 19: Concatenation
# ============================================================
# 定义：多个向量首尾相连 → 更长向量。
# Definition: Join vectors end-to-end.
# ============================================================

# ── 本单元自包含数据 ──
VOCAB = ["the", "students", "opened", "their", "books",
         "cat", "sat", "on", "mat", "dog"]
WORD2ID = {w: i for i, w in enumerate(VOCAB)}
EMBEDDING_MATRIX = [
    [ 0.10,  0.20, -0.30,  0.05],
    [ 0.80,  0.50,  0.30,  0.70],
    [ 0.20, -0.40,  0.60,  0.10],
    [ 0.05,  0.15, -0.10,  0.25],
    [ 0.75,  0.55,  0.35,  0.65],
    [-0.30,  0.60, -0.50,  0.40],
    [ 0.15, -0.20,  0.45, -0.10],
    [ 0.05,  0.10,  0.05, -0.05],
    [ 0.30, -0.10,  0.20,  0.15],
    [-0.25,  0.55, -0.45,  0.35],
]
CONTEXT_WORDS = ["students", "opened", "their"]

def concatenate(vectors):
    """向量拼接 / Concatenate vectors"""
    result = []
    for v in vectors:
        result.extend(v)
    return result

context_vecs = [EMBEDDING_MATRIX[WORD2ID[w]] for w in CONTEXT_WORDS]
x_concat = concatenate(context_vecs)
rows = [[w, f"{v}", f"{len(v)}维"] for w,v in zip(CONTEXT_WORDS, context_vecs)]
rows.append(["拼接结果", f"{x_concat}", f"{len(x_concat)}维"])
ptable(rows, headers=["概念19: 拼接", "向量", "维度"])


# %%
# ============================================================
# 概念20：隐藏层计算 h = f(W·x + b)
# Concept 20: Hidden Layer Computation
# ============================================================
# x: 拼接向量, W: 权重矩阵, b: 偏置, f: 激活函数
# ============================================================

# ── 本单元自包含数据与函数 ──
# 词汇表：10个词 / Vocabulary: 10 words
VOCAB = ["the", "students", "opened", "their", "books",
         "cat", "sat", "on", "mat", "dog"]
# 词→编号映射 / Word-to-index mapping
WORD2ID = {w: i for i, w in enumerate(VOCAB)}
# 嵌入矩阵 [10×4]：每行是一个词的4维含义向量 / Embedding [10×4]
EMBEDDING_MATRIX = [
    [ 0.10,  0.20, -0.30,  0.05],
    [ 0.80,  0.50,  0.30,  0.70],
    [ 0.20, -0.40,  0.60,  0.10],
    [ 0.05,  0.15, -0.10,  0.25],
    [ 0.75,  0.55,  0.35,  0.65],
    [-0.30,  0.60, -0.50,  0.40],
    [ 0.15, -0.20,  0.45, -0.10],
    [ 0.05,  0.10,  0.05, -0.05],
    [ 0.30, -0.10,  0.20,  0.15],
    [-0.25,  0.55, -0.45,  0.35],
]
# 上下文词：预测 "books" 的前3个词 / Context: 3 words before "books"
CONTEXT_WORDS = ["students", "opened", "their"]
# 隐藏层权重 [3×12]：3个神经元×12维拼接输入 / Hidden weights [3×12]
W_HIDDEN = [
    [ 0.1, -0.2,  0.3, -0.1,  0.2,  0.1, -0.3,  0.2,  0.1, -0.1,  0.2,  0.3],
    [-0.1,  0.3, -0.2,  0.2, -0.1,  0.3,  0.1, -0.2,  0.3,  0.1, -0.2,  0.1],
    [ 0.2, -0.1,  0.1,  0.3, -0.2,  0.2,  0.2,  0.1, -0.1,  0.2,  0.1, -0.3],
]
# 隐藏层偏置：每个神经元一个 / Hidden biases: one per neuron
B_HIDDEN = [0.1, -0.05, 0.05]

def tanh(z):
    if z > 20: return 1.0
    if z < -20: return -1.0
    return (math.exp(z) - math.exp(-z)) / (math.exp(z) + math.exp(-z))

def dot_product(a, b): return sum(ai * bi for ai, bi in zip(a, b))

# ── 计算拼接向量 ──
# 各上下文词的嵌入向量 / Embedding vectors for each context word
context_vecs = [EMBEDDING_MATRIX[WORD2ID[w]] for w in CONTEXT_WORDS]
# 拼接后的输入向量 (3词×4维=12维) / Concatenated input (3×4=12d)
x_concat = []
for v in context_vecs:
    x_concat.extend(v)

def hidden_layer_forward(x, W, b):
    """h = tanh(Wx + b)"""
    return [tanh(dot_product(W[i], x) + b[i]) for i in range(len(W))]

# 隐藏层输出 / Hidden layer output
h = hidden_layer_forward(x_concat, W_HIDDEN, B_HIDDEN)
rows = []
for i in range(len(W_HIDDEN)):
    # 第i个神经元的加权和 z=Wx+b / Weighted sum for neuron i
    z_i = dot_product(W_HIDDEN[i], x_concat) + B_HIDDEN[i]
    rows.append([f"神经元{i}", f"{z_i:.4f}", f"{tanh(z_i):.4f}"])
ptable(rows, headers=["概念20: h=tanh(Wx+b)", "z=Wx+b", "h=tanh(z)"])


# %%
# ============================================================
# 概念21：为什么需要激活函数（线性坍缩证明）
# Concept 21: Why Activation (Linear Collapse Proof)
# ============================================================
# 无激活: W₂(W₁x) = (W₂W₁)x → 多层=一层
# ============================================================

# ── 本单元自包含函数 ──
def dot_product(a, b): return sum(ai * bi for ai, bi in zip(a, b))

# 第1层权重 [2×2] / Layer-1 weight matrix
W1 = [[0.5, 0.3], [0.2, 0.8]]
# 第2层权重 [2×2] / Layer-2 weight matrix
W2 = [[0.1, 0.4], [0.7, 0.2]]
# 测试输入 / Test input vector
x21 = [1.0, 2.0]
# 第1层输出（无激活函数）/ Layer-1 output (no activation)
y1 = [dot_product(W1[i], x21) for i in range(2)]
# 第2层输出（无激活函数）/ Layer-2 output (no activation)
y2 = [dot_product(W2[i], y1) for i in range(2)]
# 合并矩阵 W₂×W₁ / Collapsed matrix W₂·W₁
W_new = [[sum(W2[i][k]*W1[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
# 单层合并输出（应等于 y2）/ Single-layer output (should equal y2)
y_one = [dot_product(W_new[i], x21) for i in range(2)]
ptable([
    ["两层分开算", f"{[f'{v:.4f}' for v in y2]}"],
    ["合并成一层", f"{[f'{v:.4f}' for v in y_one]}"],
    ["结论", "完全相同 → 无激活叠层无意义!"],
], headers=["概念21: 线性坍缩", "结果"])


# %%
# ============================================================
# 概念22：Softmax
# Concept 22: Softmax
# ============================================================
# 定义：任意实数 → 概率分布 (≥0, 总和=1)。
# Definition: softmax(zᵢ) = e^zᵢ / Σⱼ e^zⱼ
# ============================================================

# ── 本单元自包含数据与函数 ──
# 词汇表：10个词 / Vocabulary: 10 words
VOCAB = ["the", "students", "opened", "their", "books",
         "cat", "sat", "on", "mat", "dog"]
VOCAB_SIZE = len(VOCAB)  # 词汇量 V=10 / Vocabulary size
# 词→编号映射 / Word-to-index mapping
WORD2ID = {w: i for i, w in enumerate(VOCAB)}
# 嵌入矩阵 [10×4] / Embedding matrix
EMBEDDING_MATRIX = [
    [ 0.10,  0.20, -0.30,  0.05],
    [ 0.80,  0.50,  0.30,  0.70],
    [ 0.20, -0.40,  0.60,  0.10],
    [ 0.05,  0.15, -0.10,  0.25],
    [ 0.75,  0.55,  0.35,  0.65],
    [-0.30,  0.60, -0.50,  0.40],
    [ 0.15, -0.20,  0.45, -0.10],
    [ 0.05,  0.10,  0.05, -0.05],
    [ 0.30, -0.10,  0.20,  0.15],
    [-0.25,  0.55, -0.45,  0.35],
]
# 上下文词：预测 "books" 的前3个词 / Context: 3 words before target
CONTEXT_WORDS = ["students", "opened", "their"]
# 隐藏层权重 [3×12]：3神经元×(3词×4维)拼接输入 / Hidden weights [3×12]
W_HIDDEN = [
    [ 0.1, -0.2,  0.3, -0.1,  0.2,  0.1, -0.3,  0.2,  0.1, -0.1,  0.2,  0.3],
    [-0.1,  0.3, -0.2,  0.2, -0.1,  0.3,  0.1, -0.2,  0.3,  0.1, -0.2,  0.1],
    [ 0.2, -0.1,  0.1,  0.3, -0.2,  0.2,  0.2,  0.1, -0.1,  0.2,  0.1, -0.3],
]
# 隐藏层偏置 / Hidden biases
B_HIDDEN = [0.1, -0.05, 0.05]
# 输出层权重 [10×3]：10个词×3维隐藏 / Output weights [V×h]
W_OUTPUT = [
    [ 0.1,  0.2, -0.1],  [ 0.3, -0.1,  0.2],  [-0.2,  0.1,  0.3],
    [ 0.1,  0.1,  0.1],  [ 0.5,  0.3,  0.4],  [-0.1,  0.2, -0.2],
    [ 0.2, -0.3,  0.1],  [ 0.0,  0.1,  0.0],  [-0.1, -0.1,  0.2],
    [ 0.1,  0.2, -0.1],
]
# 输出层偏置：每个词一个 / Output biases: one per word
B_OUTPUT = [0.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0]

def tanh(z):
    if z > 20: return 1.0
    if z < -20: return -1.0
    return (math.exp(z) - math.exp(-z)) / (math.exp(z) + math.exp(-z))

def dot_product(a, b): return sum(ai * bi for ai, bi in zip(a, b))

def softmax(logits):
    """Softmax: 分数 → 概率"""
    max_val = max(logits)
    exps = [math.exp(z - max_val) for z in logits]
    total = sum(exps)
    return [e / total for e in exps]

# ── 前向传播 ──
# 各上下文词的嵌入向量 / Embedding vectors for context words
context_vecs = [EMBEDDING_MATRIX[WORD2ID[w]] for w in CONTEXT_WORDS]
# 拼接后的输入向量 / Concatenated input vector
x_concat = []
for v in context_vecs:
    x_concat.extend(v)
# 隐藏层输出 h = tanh(W·x + b) / Hidden layer output
h = [tanh(dot_product(W_HIDDEN[i], x_concat) + B_HIDDEN[i])
     for i in range(len(W_HIDDEN))]
# 输出层原始分数（未归一化）/ Raw scores before softmax
logits = [dot_product(W_OUTPUT[i], h) + B_OUTPUT[i] for i in range(VOCAB_SIZE)]
# Softmax 后的概率分布 / Probability distribution
probs = softmax(logits)

rows = [[w, f"{logits[i]:.4f}", f"{probs[i]:.4f}", "█"*int(probs[i]*50)]
        for i, w in enumerate(VOCAB)]
ptable(rows, headers=["概念22: Softmax", "logit", "概率", "分布"])
print(f"概率总和: {sum(probs):.6f}")


# %%
# ============================================================
# 概念23：模型参数汇总
# Concept 23: Model Parameter Summary
# ============================================================
# 所有需训练的数字 = 模型"知识"。
# ============================================================

# ── 本单元自包含数据 ──
# 词汇量（V）/ Vocabulary size
VOCAB_SIZE = 10
# 嵌入维度（d）：每词用几个数字表示 / Embedding dim
EMBED_DIM = 4
# 隐藏层神经元数（h）/ Number of hidden neurons
HIDDEN_SIZE = 3
# 上下文窗口（N）：用前几个词预测 / Context window size
CONTEXT_SIZE = 3

def count_params(V, d, h, N):
    """计算各层参数量 / Count parameters per layer
    V=词汇量, d=嵌入维度, h=隐藏节点数, N=上下文窗口"""
    return {"嵌入E": V*d, "隐藏W": h*(N*d), "隐藏b": h,
            "输出W": V*h, "输出b": V, "总计": V*d+h*(N*d)+h+V*h+V}

# Demo规模 vs 真实规模对比 / Demo vs real-world scale
demo = count_params(VOCAB_SIZE, EMBED_DIM, HIDDEN_SIZE, CONTEXT_SIZE)
real = count_params(50000, 300, 100, 3)
rows = [[k, f"{demo[k]:,}", f"{real[k]:,}"] for k in demo]
ptable(rows, headers=["概念23: 参数汇总", "Demo", "真实规模"])


# %%
# ============================================================
# 概念24：梯度下降
# Concept 24: Gradient Descent
# ============================================================
# w_new = w_old - lr × gradient
# ============================================================

# 初始参数值（距最优解 x=3 很远）/ Initial param (far from optimal x=3)
x24 = 10.0
# 学习率：每步调整幅度 / Learning rate: step size per update
lr = 0.2
rows = []
for step in range(8):
    # 当前损失值 (x-3)² / Current loss
    loss = (x24 - 3) ** 2
    # 梯度 = 损失对x的导数 / Gradient = dLoss/dx
    grad = 2 * (x24 - 3)
    x24 = x24 - lr * grad
    rows.append([step, f"{x24:.4f}", f"{loss:.4f}", f"{grad:+.2f}"])
ptable(rows, headers=["概念24: 梯度下降", "x", "loss", "grad"])


# %%
# ============================================================
# 概念25：交叉熵损失
# Concept 25: Cross-Entropy Loss
# ============================================================
# Loss = -log(P(正确答案))。概率越低→惩罚越大。
# ============================================================

# ── 本单元自包含数据与函数 ──
# 词汇表 / Vocabulary
VOCAB = ["the", "students", "opened", "their", "books",
         "cat", "sat", "on", "mat", "dog"]
VOCAB_SIZE = len(VOCAB)  # 词汇量 V=10
# 词→编号映射 / Word-to-index mapping
WORD2ID = {w: i for i, w in enumerate(VOCAB)}
# 嵌入矩阵 [10×4] / Embedding matrix
EMBEDDING_MATRIX = [
    [ 0.10,  0.20, -0.30,  0.05],
    [ 0.80,  0.50,  0.30,  0.70],
    [ 0.20, -0.40,  0.60,  0.10],
    [ 0.05,  0.15, -0.10,  0.25],
    [ 0.75,  0.55,  0.35,  0.65],
    [-0.30,  0.60, -0.50,  0.40],
    [ 0.15, -0.20,  0.45, -0.10],
    [ 0.05,  0.10,  0.05, -0.05],
    [ 0.30, -0.10,  0.20,  0.15],
    [-0.25,  0.55, -0.45,  0.35],
]
# 上下文词 / Context words
CONTEXT_WORDS = ["students", "opened", "their"]
# 目标词：模型应该预测出的正确答案 / Target: correct answer
TARGET_WORD = "books"
# 目标词编号：用于计算交叉熵 / Target index for cross-entropy
TARGET_ID = WORD2ID[TARGET_WORD]
# 隐藏层权重 [3×12] / Hidden weights
W_HIDDEN = [
    [ 0.1, -0.2,  0.3, -0.1,  0.2,  0.1, -0.3,  0.2,  0.1, -0.1,  0.2,  0.3],
    [-0.1,  0.3, -0.2,  0.2, -0.1,  0.3,  0.1, -0.2,  0.3,  0.1, -0.2,  0.1],
    [ 0.2, -0.1,  0.1,  0.3, -0.2,  0.2,  0.2,  0.1, -0.1,  0.2,  0.1, -0.3],
]
# 隐藏层偏置 / Hidden biases
B_HIDDEN = [0.1, -0.05, 0.05]
# 输出层权重 [10×3] / Output weights [V×h]
W_OUTPUT = [
    [ 0.1,  0.2, -0.1],  [ 0.3, -0.1,  0.2],  [-0.2,  0.1,  0.3],
    [ 0.1,  0.1,  0.1],  [ 0.5,  0.3,  0.4],  [-0.1,  0.2, -0.2],
    [ 0.2, -0.3,  0.1],  [ 0.0,  0.1,  0.0],  [-0.1, -0.1,  0.2],
    [ 0.1,  0.2, -0.1],
]
# 输出层偏置 / Output biases
B_OUTPUT = [0.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0]

def tanh(z):
    if z > 20: return 1.0
    if z < -20: return -1.0
    return (math.exp(z) - math.exp(-z)) / (math.exp(z) + math.exp(-z))

def dot_product(a, b): return sum(ai * bi for ai, bi in zip(a, b))

def softmax(logits):
    max_val = max(logits)
    exps = [math.exp(z - max_val) for z in logits]
    total = sum(exps)
    return [e / total for e in exps]

def cross_entropy_loss(probabilities, correct_index):
    """交叉熵: -log(正确答案概率)"""
    return -math.log(probabilities[correct_index] + 1e-10)

# ── 前向传播 ──
# 各上下文词的嵌入向量 / Embedding vectors for context words
context_vecs = [EMBEDDING_MATRIX[WORD2ID[w]] for w in CONTEXT_WORDS]
# 拼接后的输入向量 / Concatenated input vector
x_concat = []
for v in context_vecs:
    x_concat.extend(v)
# 隐藏层输出 / Hidden layer output
h = [tanh(dot_product(W_HIDDEN[i], x_concat) + B_HIDDEN[i])
     for i in range(len(W_HIDDEN))]
# 输出层原始分数 / Raw output scores (logits)
logits = [dot_product(W_OUTPUT[i], h) + B_OUTPUT[i] for i in range(VOCAB_SIZE)]
# Softmax 概率分布 / Probability distribution
probs = softmax(logits)

# 交叉熵损失 / Cross-entropy loss
loss = cross_entropy_loss(probs, TARGET_ID)
ptable([
    [f"P('{TARGET_WORD}')", f"{probs[TARGET_ID]:.4f}", f"{loss:.4f}"],
    ["假设 P=0.99", "0.9900", f"{-math.log(0.99):.4f}"],
    ["假设 P=0.01", "0.0100", f"{-math.log(0.01):.4f}"],
], headers=["概念25: 交叉熵", "概率", "Loss"])


# %%
# ============================================================
# 概念26：Softmax 计算过程
# Concept 26: Softmax Step-by-Step
# ============================================================
# logits → 减最大值 → exp → 归一化 → 概率
# ============================================================

# ── 本单元自包含数据与函数 ──
# 词汇表 / Vocabulary
VOCAB = ["the", "students", "opened", "their", "books",
         "cat", "sat", "on", "mat", "dog"]
VOCAB_SIZE = len(VOCAB)  # 词汇量 V=10
# 词→编号映射 / Word-to-index mapping
WORD2ID = {w: i for i, w in enumerate(VOCAB)}
# 嵌入矩阵 [10×4] / Embedding matrix
EMBEDDING_MATRIX = [
    [ 0.10,  0.20, -0.30,  0.05],
    [ 0.80,  0.50,  0.30,  0.70],
    [ 0.20, -0.40,  0.60,  0.10],
    [ 0.05,  0.15, -0.10,  0.25],
    [ 0.75,  0.55,  0.35,  0.65],
    [-0.30,  0.60, -0.50,  0.40],
    [ 0.15, -0.20,  0.45, -0.10],
    [ 0.05,  0.10,  0.05, -0.05],
    [ 0.30, -0.10,  0.20,  0.15],
    [-0.25,  0.55, -0.45,  0.35],
]
# 上下文词 / Context words
CONTEXT_WORDS = ["students", "opened", "their"]
# 隐藏层权重 [3×12] / Hidden weights
W_HIDDEN = [
    [ 0.1, -0.2,  0.3, -0.1,  0.2,  0.1, -0.3,  0.2,  0.1, -0.1,  0.2,  0.3],
    [-0.1,  0.3, -0.2,  0.2, -0.1,  0.3,  0.1, -0.2,  0.3,  0.1, -0.2,  0.1],
    [ 0.2, -0.1,  0.1,  0.3, -0.2,  0.2,  0.2,  0.1, -0.1,  0.2,  0.1, -0.3],
]
# 隐藏层偏置 / Hidden biases
B_HIDDEN = [0.1, -0.05, 0.05]
# 输出层权重 [10×3] / Output weights
W_OUTPUT = [
    [ 0.1,  0.2, -0.1],  [ 0.3, -0.1,  0.2],  [-0.2,  0.1,  0.3],
    [ 0.1,  0.1,  0.1],  [ 0.5,  0.3,  0.4],  [-0.1,  0.2, -0.2],
    [ 0.2, -0.3,  0.1],  [ 0.0,  0.1,  0.0],  [-0.1, -0.1,  0.2],
    [ 0.1,  0.2, -0.1],
]
# 输出层偏置 / Output biases
B_OUTPUT = [0.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0]

def tanh(z):
    if z > 20: return 1.0
    if z < -20: return -1.0
    return (math.exp(z) - math.exp(-z)) / (math.exp(z) + math.exp(-z))

def dot_product(a, b): return sum(ai * bi for ai, bi in zip(a, b))

# ── 前向传播到 logits ──
# 各上下文词的嵌入向量 / Embedding vectors for context words
context_vecs = [EMBEDDING_MATRIX[WORD2ID[w]] for w in CONTEXT_WORDS]
# 拼接后的输入向量 / Concatenated input vector
x_concat = []
for v in context_vecs:
    x_concat.extend(v)
# 隐藏层输出 / Hidden layer output
h = [tanh(dot_product(W_HIDDEN[i], x_concat) + B_HIDDEN[i])
     for i in range(len(W_HIDDEN))]
# 输出层原始分数 / Raw output scores (logits)
logits = [dot_product(W_OUTPUT[i], h) + B_OUTPUT[i] for i in range(VOCAB_SIZE)]

# ── 逐步演示 Softmax ──
# 取前5个词的 logit（演示用）/ First 5 logits for demo
sub = logits[:5]
# 最大值（数值稳定性：防 exp 溢出）/ Max value for numerical stability
max_v = max(sub)
# 减去最大值后的 logits / Shifted logits (subtract max)
shifted = [z - max_v for z in sub]
# e^(shifted) 指数值 / Exponentials of shifted values
exps = [math.exp(s) for s in shifted]
# 指数值总和（归一化分母）/ Sum of exponentials (denominator)
total = sum(exps)
# 归一化概率 = exp / total / Normalized probabilities
ps = [e/total for e in exps]
rows = [[VOCAB[i], f"{sub[i]:.3f}", f"{shifted[i]:.3f}", f"{exps[i]:.4f}", f"{ps[i]:.4f}"]
        for i in range(5)]
ptable(rows, headers=["概念26: 逐步Softmax", "logit", "-max", "exp", "概率"])


# %%
# ============================================================
# 概念27：反向传播 / 链式法则
# Concept 27: Backpropagation / Chain Rule
# ============================================================
# dL/dw = (dL/dy) × (dy/dz) × (dz/dw)
# ============================================================

# 输入x, 权重w, 偏置b（单神经元简化版）/ Single neuron: input, weight, bias
x27, w27, b27 = 2.0, 0.5, 0.1
# 目标值：期望神经元输出接近0.9 / Target: desired output ≈ 0.9
target27 = 0.9
# 加权和 z = wx + b / Weighted sum
z27 = w27 * x27 + b27
# 激活输出 y = tanh(z) / Activated output
y27 = math.tanh(z27)
# 均方误差损失 (y - target)² / MSE loss
loss27 = (y27 - target27) ** 2
# ∂L/∂y = 2(y - target) / Loss gradient w.r.t. output
dL_dy = 2 * (y27 - target27)
# ∂y/∂z = 1 - tanh²(z)（tanh导数）/ Activation gradient (tanh derivative)
dy_dz = 1 - math.tanh(z27) ** 2
# ∂z/∂w = x（权重的梯度因子）/ Weight gradient factor
dz_dw = x27
ptable([
    ["前向: z=wx+b", f"{z27:.2f}"],
    ["前向: y=tanh(z)", f"{y27:.4f}"],
    ["Loss=(y-target)²", f"{loss27:.6f}"],
    ["dL/dy", f"{dL_dy:.4f}"],
    ["dy/dz = 1-tanh²", f"{dy_dz:.4f}"],
    ["dz/dw = x", f"{dz_dw}"],
    ["dL/dw (链式相乘)", f"{dL_dy*dy_dz*dz_dw:.6f}"],
    ["dL/db (链式相乘)", f"{dL_dy*dy_dz*1.0:.6f}"],
], headers=["概念27: 反向传播", "值"])


# %%
# ============================================================
# 概念28：梯度 = 方向信号
# Concept 28: Gradient = Directional Signal
# ============================================================
# 正→减小参数, 负→增大参数, 零→极值点
# ============================================================

# 初始权重（最优解是 w=2.0）/ Initial weight (optimal = 2.0)
w28 = 5.0
# 学习率 / Learning rate
lr28 = 0.1
rows = []
for step in range(6):
    # 梯度 = 2(w - 最优值) / Gradient
    grad = 2 * (w28 - 2.0)
    # 方向判定：正梯度→减小，负梯度→增大 / Direction label
    direction = "减小↓" if grad > 0 else "增大↑" if grad < 0 else "不动"
    # 更新后的权重 w_new = w - lr×grad / Updated weight
    w_new = w28 - lr28 * grad
    rows.append([step, f"{w28:.2f}", f"{grad:+.2f}", direction, f"{w_new:.2f}"])
    w28 = w_new
ptable(rows, headers=["概念28: 方向信号", "w", "grad", "方向", "w_new"])


# %%
# ============================================================
# 概念29：前馈 NN 无梯度消失
# Concept 29: FFNN Has No Vanishing Gradient
# ============================================================
# 前馈1~2层衰减小。RNN几十层→指数衰减→消失。
# ============================================================

# 每层梯度衰减因子（模拟 tanh 导数最大值）/ Gradient decay per layer
decay = 0.5
rows = []
for name, n in [("前馈NN",2),("短RNN",10),("长RNN",20),("超长RNN",50)]:
    # 经过 n 层后剩余梯度比例 / Remaining gradient ratio after n layers
    r = decay ** n
    # 状态标签：根据梯度剩余量判定 / Status based on remaining gradient
    s = "✅正常" if r > 0.01 else "⚠️微弱" if r > 0.0001 else "❌消失"
    rows.append([f"{name}({n}层)", f"{r:.10f}", s])
ptable(rows, headers=["概念29: 梯度衰减", "剩余梯度", "状态"])


# %%
# ============================================================
# 概念30：完整前馈 NN 语言模型
# Concept 30: Complete Feedforward NN Language Model
# ============================================================
# 串联概念11~29，构成完整可训练模型。
# ============================================================

# ── 本单元自包含数据与函数 ──
# 词汇表 / Vocabulary
VOCAB = ["the", "students", "opened", "their", "books",
         "cat", "sat", "on", "mat", "dog"]
VOCAB_SIZE = len(VOCAB)  # 词汇量 V=10
# 词→编号 / Word-to-index
WORD2ID = {w: i for i, w in enumerate(VOCAB)}
# 编号→词（预测时反查）/ Index-to-word (for prediction output)
ID2WORD = {i: w for w, i in WORD2ID.items()}
# 嵌入矩阵 [10×4]：可学习参数 / Embedding matrix (learnable)
EMBEDDING_MATRIX = [
    [ 0.10,  0.20, -0.30,  0.05],
    [ 0.80,  0.50,  0.30,  0.70],
    [ 0.20, -0.40,  0.60,  0.10],
    [ 0.05,  0.15, -0.10,  0.25],
    [ 0.75,  0.55,  0.35,  0.65],
    [-0.30,  0.60, -0.50,  0.40],
    [ 0.15, -0.20,  0.45, -0.10],
    [ 0.05,  0.10,  0.05, -0.05],
    [ 0.30, -0.10,  0.20,  0.15],
    [-0.25,  0.55, -0.45,  0.35],
]
# 上下文词 / Context: "students opened their ___"
CONTEXT_WORDS = ["students", "opened", "their"]
# 上下文编号列表（传给模型）/ Context IDs for model input
CONTEXT_IDS = [WORD2ID[w] for w in CONTEXT_WORDS]
# 目标词和编号 / Target word and its index
TARGET_WORD = "books"
TARGET_ID = WORD2ID[TARGET_WORD]
# 隐藏层权重 [3×12] / Hidden weights
W_HIDDEN = [
    [ 0.1, -0.2,  0.3, -0.1,  0.2,  0.1, -0.3,  0.2,  0.1, -0.1,  0.2,  0.3],
    [-0.1,  0.3, -0.2,  0.2, -0.1,  0.3,  0.1, -0.2,  0.3,  0.1, -0.2,  0.1],
    [ 0.2, -0.1,  0.1,  0.3, -0.2,  0.2,  0.2,  0.1, -0.1,  0.2,  0.1, -0.3],
]
# 隐藏层偏置 / Hidden biases
B_HIDDEN = [0.1, -0.05, 0.05]
# 输出层权重 [10×3] / Output weights
W_OUTPUT = [
    [ 0.1,  0.2, -0.1],  [ 0.3, -0.1,  0.2],  [-0.2,  0.1,  0.3],
    [ 0.1,  0.1,  0.1],  [ 0.5,  0.3,  0.4],  [-0.1,  0.2, -0.2],
    [ 0.2, -0.3,  0.1],  [ 0.0,  0.1,  0.0],  [-0.1, -0.1,  0.2],
    [ 0.1,  0.2, -0.1],
]
# 输出层偏置 / Output biases
B_OUTPUT = [0.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0]

def tanh(z):
    if z > 20: return 1.0
    if z < -20: return -1.0
    return (math.exp(z) - math.exp(-z)) / (math.exp(z) + math.exp(-z))

def dot_product(a, b): return sum(ai * bi for ai, bi in zip(a, b))

def concatenate(vectors):
    result = []
    for v in vectors:
        result.extend(v)
    return result

def softmax(logits):
    max_val = max(logits)
    exps = [math.exp(z - max_val) for z in logits]
    total = sum(exps)
    return [e / total for e in exps]

def cross_entropy_loss(probabilities, correct_index):
    return -math.log(probabilities[correct_index] + 1e-10)

class FeedForwardLM:
    """纯Python前馈NN语言模型 / Pure Python FFNN LM"""
    def __init__(self, E, W_h, b_h, W_o, b_o):
        """初始化模型参数（深拷贝，训练不影响原始数据）
        E: 嵌入矩阵 [V×d], W_h: 隐藏层权重 [h×(N*d)],
        b_h: 隐藏层偏置 [h], W_o: 输出层权重 [V×h],
        b_o: 输出层偏置 [V]"""
        self.E = [row[:] for row in E]      # 嵌入矩阵 / Embedding
        self.W_h = [row[:] for row in W_h]  # 隐藏层权重 / Hidden weights
        self.b_h = b_h[:]                   # 隐藏层偏置 / Hidden biases
        self.W_o = [row[:] for row in W_o]  # 输出层权重 / Output weights
        self.b_o = b_o[:]                   # 输出层偏置 / Output biases

    def forward(self, word_ids):
        # 各上下文词的嵌入向量 / Embeddings for input words
        embeds = [self.E[wid] for wid in word_ids]
        # 拼接后的输入向量 / Concatenated input vector
        x = concatenate(embeds)
        # 隐藏层输出 h = tanh(W·x + b) / Hidden layer output
        h = [tanh(dot_product(self.W_h[i], x) + self.b_h[i]) for i in range(len(self.W_h))]
        # 输出层原始分数 / Raw output scores (logits)
        logits = [dot_product(self.W_o[i], h) + self.b_o[i] for i in range(len(self.W_o))]
        return softmax(logits)

    def predict(self, word_ids):
        # 概率分布 / Probability distribution
        probs = self.forward(word_ids)
        # 最高概率词的编号 / Index of highest-probability word
        best_id = probs.index(max(probs))
        return ID2WORD[best_id], probs[best_id]

    def train_step(self, word_ids, target_id, lr=0.01):
        # 当前损失 / Current loss
        loss = cross_entropy_loss(self.forward(word_ids), target_id)
        # 数值微分步长 / Epsilon for numerical gradient
        eps = 1e-4
        for i in range(len(self.b_o)):
            self.b_o[i] += eps
            lp = cross_entropy_loss(self.forward(word_ids), target_id)
            self.b_o[i] -= eps
            self.b_o[i] -= lr * (lp - loss) / eps
        for i in range(len(self.W_o)):
            for j in range(len(self.W_o[i])):
                self.W_o[i][j] += eps
                lp = cross_entropy_loss(self.forward(word_ids), target_id)
                self.W_o[i][j] -= eps
                self.W_o[i][j] -= lr * (lp - loss) / eps
        return loss

# 实例化模型（深拷贝参数）/ Instantiate model (deep-copies params)
model = FeedForwardLM(EMBEDDING_MATRIX, W_HIDDEN, B_HIDDEN, W_OUTPUT, B_OUTPUT)

# 训练前预测结果 / Prediction before training
w0, p0 = model.predict(CONTEXT_IDS)
rows = [["训练前", w0, f"{p0:.4f}", "-"]]
for step in range(30):
    # 本步训练损失 / Training loss at this step
    loss = model.train_step(CONTEXT_IDS, TARGET_ID, lr=0.1)
    if step % 5 == 0:
        # 中间检查点预测 / Checkpoint prediction
        w_s, p_s = model.predict(CONTEXT_IDS)
        # 目标词 "books" 的概率 / Probability of target word
        pb = model.forward(CONTEXT_IDS)[TARGET_ID]
        rows.append([f"第{step}步", w_s, f"{p_s:.4f}", f"{loss:.4f}"])
# 训练后最终预测 / Final prediction after training
w_f, p_f = model.predict(CONTEXT_IDS)
rows.append(["训练后", w_f, f"{p_f:.4f}", "-"])
ptable(rows, headers=[f"概念30: 完整模型", "预测词", "最高P", "loss"])
print(f"\n✅ 30个概念全部演示完毕 — tabulate 表格输出")

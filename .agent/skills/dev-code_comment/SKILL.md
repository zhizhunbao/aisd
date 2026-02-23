---
name: code-comment
description: 中英文双语代码注释规范。Use when (1) 为代码添加注释, (2) 需要中英双语文档, (3) 规范化代码注释格式, (4) 学习类项目代码注释
---

# Code Comment (Bilingual)

## Objectives

- Add bilingual (Chinese & English) comments to code
- Follow consistent comment formatting rules
- Explain complex logic with reasons
- Maintain clear code documentation

## Comment Rules Overview

| Location                      | Language          | Format                                      |
| ----------------------------- | ----------------- | ------------------------------------------- |
| File-level docstring          | English only      | Standard docstring                          |
| Code block divider            | Chinese + English | 60 '=' separator with bilingual title       |
| Function docstring            | Chinese + English | Two-line format: Chinese line, English line |
| Method/Function Documentation | Bilingual         | Box-style Header ABOVE definition           |
| Inline comments               | Chinese + English | Chinese line, English line, above code      |
| Algorithm/Concept comments    | Chinese + English | Structured template: 定义/公式/举例/优点    |
| Step Output                   | English           | print_step usage for formatted I/O          |

## 1. File-level Docstring (English Only)

```python
"""
Lab 2: Q-Learning Agent for Cliff Walking
Student ID: 041107730
Implements Q-Learning using Bellman equation: Q(s,a) = r + γ * max Q(s',a')
Modified from Hybrid Activity 1 to solve the Cliff Walking problem.
"""
```

## 2. Code Block Dividers (60 Characters)

Use exactly 60 '=' characters to separate major logical sections (Steps, Phases, Modules). Includes a bilingual title.

```python
# ============================================================
# 步骤 1：数据加载与预处理
# Step 1: Data Loading and Preprocessing
# ============================================================
```

**Rules:**

- Exactly 60 '=' characters.
- Chinese title first, then English title.
- Placed between major logical blocks.
- One blank line before and after the divider (except at the very start of file).
- All step dividers are at the **top level** of the script (no `main()` wrapper).

**Flat sequential example:**

```python
# ============================================================
# 步骤 1：数据加载
# Step 1: Data Loading
# ============================================================

# [Bilingual comments + code]
df = pd.read_csv('data.csv')

# ============================================================
# 步骤 2：数据预处理
# Step 2: Data Preprocessing
# ============================================================

# [Bilingual comments + code]
df = preprocess(df)
```

## 2.1 Algorithm/Concept/Math Comments (Structured Template)

For algorithms, mathematical concepts, or technical definitions, use a **structured template** with the following sections. This template should be placed **directly above** the related code.

### Template Structure Overview

```
# ================================================================
# 概念：中文名 (英文名)
# Concept: English Name
# ================================================================
#
# -------- 术语解释 / Terminology --------
#
# 【术语1 English Term 1】
#   中文定义
#   English definition
#
# -------- 算法原理 / Algorithm --------
#
# 定义 / Definition:
#   ...
#
# 公式 / Formula:
#   ...
#
# 举例 / Example:
#   ...
#
# 优点 / Advantages:
#   ...
# ================================================================
```

### ⚠️ 严格规则 / Strict Rules

**只允许以下两个 section（不允许自定义 section）:**

1. `-------- 术语解释 / Terminology --------`
2. `-------- 算法原理 / Algorithm --------`

**❌ 禁止自定义子项名称，如:**

- ❌ `输出格式 / Output Format`
- ❌ `评估意义 / Evaluation Significance`
- ❌ `训练流程 / Training Process`
- ❌ `分析要点 / Analysis Points`

**✅ 如需说明这些内容，应放入标准子项中:**

- 输出格式 → 放入 `举例 / Example:`
- 意义/目的 → 放入 `定义 / Definition:` 或 `优点 / Advantages:`
- 流程/步骤 → 放入 `举例 / Example:`

---

### 术语解释 / Terminology Section

**格式:** `【术语名 English Term】`

**每个术语必须包含:**

- 中文定义（一行）
- 英文定义（一行）
- 公式（如有，紧跟定义后）

**示例:**

```python
# -------- 术语解释 / Terminology --------
#
# 【卷积 Convolution】
#   用滤波器在输入上滑动，计算元素乘积之和
#   Slide filter over input, compute element-wise product sum
#
# 【ReLU 激活函数】
#   公式：f(x) = max(0, x)
#   引入非线性，解决梯度消失问题
#   Formula: f(x) = max(0, x)
#   Introduces non-linearity, solves vanishing gradient
```

---

### 算法原理 / Algorithm Section

**必须包含的 4 个子项（顺序固定）:**

| 序号 | 子项                 | 说明                            |
| ---- | -------------------- | ------------------------------- |
| 1    | `定义 / Definition:` | 算法的核心定义，一句话概括      |
| 2    | `公式 / Formula:`    | 数学公式（无公式写 "无 / N/A"） |
| 3    | `举例 / Example:`    | 具体的计算例子，用数字演示      |
| 4    | `优点 / Advantages:` | 算法的优势（至少 1-2 点）       |

**示例 / Example:**

```python
# -------- 算法原理 / Algorithm --------
#
# 定义 / Definition:
#   通过 softmax 将线性输出映射到概率分布
#   Map linear output to probability distribution via softmax
#
# 公式 / Formula:
#   P(y=k|x) = e^(z_k) / Σ e^(z_j)
#
# 举例 / Example:
#   输入 z = [2.0, 1.0, 0.1]
#   softmax(z) = [0.659, 0.242, 0.099]
#   预测类别 = argmax = 0
#
# 优点 / Advantages:
#   - 输出可解释为概率
#   - 所有类别概率之和为 1
```

### Complete Template Example

```python
# ================================================================
# 概念：卷积神经网络 (CNN)
# Concept: Convolutional Neural Network
# ================================================================
#
# -------- 术语解释 / Terminology --------
#
# 【卷积层 Conv2D】
#   用滤波器在图像上滑动，提取局部特征（边缘、纹理等）
#   Slide filters over image to extract local features (edges, textures, etc.)
#
# 【池化层 MaxPooling2D】
#   在小区域内取最大值，压缩特征图尺寸
#   Take max value in small regions, compress feature map size
#
# -------- 算法原理 / Algorithm --------
#
# 定义 / Definition:
#   通过卷积操作提取图像的空间特征，用于图像分类等任务
#   Extract spatial features from images via convolution for classification tasks
#
# 公式 / Formula:
#   output[i,j] = Σ (input[i+m, j+n] × kernel[m,n]) + bias
#
# 举例 / Example:
#   3x3 滤波器在 28x28 图像上滑动：
#   输入像素 [[1,2,3],[4,5,6],[7,8,9]], 滤波器 [[1,0,-1],[1,0,-1],[1,0,-1]]
#   输出 = 1×1 + 2×0 + 3×(-1) + 4×1 + ... = -6 (检测垂直边缘)
#
# 优点 / Advantages:
#   - 参数共享，减少参数数量
#   - 平移不变性，对位置不敏感
# ================================================================
model = Sequential([...])
```

**Example 1: Evaluation Metric (Accuracy)**

```python
# ================================================================
# 评估指标 1：Accuracy（准确率）
# Metric 1: Accuracy
# ================================================================
# 定义 / Definition:
#   Accuracy = 正确预测数 / 总样本数
#   Accuracy = Number of correct predictions / Total samples
#
# 公式 / Formula:
#   Accuracy = (TP + TN) / (TP + TN + FP + FN)
#   其中 TP=真正例, TN=真负例, FP=假正例, FN=假负例
#
# 举例 / Example:
#   100 个样本，80 个预测正确，20 个预测错误
#   Accuracy = 80 / 100 = 0.80 (80%)
#
# 局限性 / Limitation:
#   对于不平衡数据集，Accuracy 可能误导
#   例如：95% 是正类，模型全预测正类也有 95% 准确率
# ================================================================
acc = accuracy_score(y_test, y_pred)
```

**Example 2: Machine Learning Algorithm (Logistic Regression)**

```python
# ================================================================
# 分类器 1：Logistic Regression（逻辑回归）
# Classifier 1: Logistic Regression
# ================================================================
# 定义 / Definition:
#   通过 sigmoid/softmax 函数将线性输出映射到概率
#   Map linear output to probability via sigmoid/softmax function
#
# 公式 / Formula:
#   二分类：P(y=1|x) = 1 / (1 + e^(-w·x))
#   多分类：P(y=k|x) = e^(w_k·x) / Σ e^(w_j·x)  (softmax)
#   损失函数：交叉熵 Cross-entropy loss
#
# 举例 / Example:
#   x=[0.5,0.3,0.8], w=[0.2,-0.1,0.5]
#   线性输出 = 0.5×0.2 + 0.3×(-0.1) + 0.8×0.5 = 0.47
#   概率 = sigmoid(0.47) = 0.615 → 预测为正类
#
# 优点 / Advantages:
#   - 输出概率值，可解释性强
#   - 训练速度快，适合大规模数据
#   - 有正则化，不易过拟合
# ================================================================
model = LogisticRegression(max_iter=1000, multi_class="multinomial")
```

**Example 3: NLP Feature Extraction (TF-IDF)**

```python
# ================================================================
# 特征提取：TF-IDF（词频-逆文档频率）
# Feature Extraction: TF-IDF (Term Frequency-Inverse Document Frequency)
# ================================================================
# 定义 / Definition:
#   衡量词对文档的重要性：常见词权重低，稀有词权重高
#   Measure word importance: common words get low weight, rare words get high weight
#
# 公式 / Formula:
#   TF(t,d) = 词 t 在文档 d 中出现的次数 / 文档 d 的总词数
#   IDF(t) = log(总文档数 N / 包含词 t 的文档数 df(t)) + 1
#   TF-IDF(t,d) = TF(t,d) × IDF(t)
#
# 举例 / Example:
#   文档: "good product good"
#   TF("good") = 2/3 = 0.67
#   若 "good" 在 100 篇中的 50 篇出现：IDF = log(100/50) + 1 = 1.69
#   TF-IDF("good") = 0.67 × 1.69 = 1.13
#
# 优点 / Advantages:
#   - 降低常见停用词的权重
#   - 突出对文档有区分度的关键词
# ================================================================
tfidf_vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=5000)
```

**Example 4: Hyperparameter (Regularization)**

```python
# ================================================================
# 超参数：C（正则化强度的倒数）
# Hyperparameter: C (inverse of regularization strength)
# ================================================================
# 定义 / Definition:
#   C 控制正则化的强度，防止过拟合
#   C controls regularization strength, prevents overfitting
#
# 公式 / Formula:
#   C 越大 → 正则化越弱 → 模型越复杂 → 可能过拟合
#   C 越小 → 正则化越强 → 模型越简单 → 可能欠拟合
#
# 举例 / Example:
#   C=0.01：强正则化，简单模型，可能欠拟合
#   C=1.0： 适中正则化，平衡复杂度
#   C=10.0：弱正则化，复杂模型，可能过拟合
# ================================================================
lr_param_grid = {"C": [0.01, 0.1, 1.0, 10.0]}
```

**Example 5: Algorithm with Terminology Section (for complex concepts)**

When an algorithm uses technical terms that may not be familiar, add a **Terminology section** to explain them:

```python
# ================================================================
# 分类器：Logistic Regression（逻辑回归）
# Classifier: Logistic Regression
# ================================================================
#
# -------- 术语解释 / Terminology --------
#
# 【二分类 Binary Classification】
#   只有两个类别的分类问题，如：垃圾邮件(1) vs 正常邮件(0)
#   Classification with only 2 classes, e.g., spam(1) vs normal(0)
#
# 【sigmoid 函数】
#   将任意实数压缩到 (0,1) 区间，输出可解释为概率
#   公式：σ(z) = 1 / (1 + e^(-z))
#   举例：σ(0)=0.5, σ(2)=0.88, σ(-2)=0.12
#   Compresses any real number to (0,1), output = probability
#
# 【交叉熵 Cross-entropy】
#   分类问题常用的损失函数，惩罚错误的概率预测
#   公式：L = -Σ y_true × log(y_pred)
#   举例：真实=1，预测概率=0.9 → L=-log(0.9)=0.105（小损失，好）
#   Common loss for classification, penalizes wrong probability predictions
#
# -------- 算法原理 / Algorithm --------
#
# 定义 / Definition:
#   通过 sigmoid(二分类) 或 softmax(多分类) 将线性输出映射到概率
#
# 公式 / Formula:
#   P(y=1|x) = sigmoid(w·x) = 1 / (1 + e^(-w·x))
#
# 举例 / Example:
#   特征 x=[0.5,0.3,0.8], 权重 w=[0.2,-0.1,0.5]
#   线性输出 z = 0.47 → 概率 = sigmoid(0.47) = 0.615 → 预测为正类
# ================================================================
model = LogisticRegression()
```

**When to Use This Template:**

- Machine learning algorithms (Logistic Regression, SVM, Random Forest, etc.)
- Evaluation metrics (Accuracy, F1-score, Precision, Recall, etc.)
- Mathematical concepts (Confusion Matrix, Cross-entropy, Gradient Descent, etc.)
- Feature extraction methods (TF-IDF, Word2Vec, BoW, etc.)
- Hyperparameters with mathematical meaning (learning rate, regularization, etc.)
- Statistical concepts (mean, variance, normalization, etc.)
- Loss functions and optimization algorithms

**When to Add Terminology Section:**

- When using terms like: sigmoid, softmax, 交叉熵, 损失函数, 超平面, 支持向量, etc.
- When the algorithm has domain-specific jargon
- When teaching/learning code where understanding concepts is important

**Rules:**

- Place the template **directly above** the related code
- Use `# ================================================================` (64 characters) for top and bottom borders
- Include **at minimum**: 定义/Definition, 公式/Formula (if applicable), 举例/Example
- Add **术语解释 / Terminology** section when technical terms need explanation
- Use 【术语名 English】 format for each term in terminology section
- Add optional sections as needed: 优点/Advantages, 局限性/Limitation, 备注/Notes
- Keep Chinese and English paired throughout
- Blank line between each section inside the template

## 2. Function Docstring (Two-Line Bilingual Format)

Two lines with Chinese first line, English second line:

```python
def train(env, episodes: int = 50, gamma: float = 0.9) -> list:
    """训练Q-Learning智能体
    Train Q-Learning agent"""

def reset() -> tuple:
    """重置环境到初始状态
    Reset environment to initial state"""
```

**Rules:**

- Use triple quotes `"""`
- Chinese description on first line
- English description on second line
- Keep it concise, no blank line between Chinese and English
- No parameter or return value details in docstring (use section headers instead, see below)

### 2.1 Class, Method & Function Documentation (Box-Style Headers)

For all classes, functions, and class methods, use box-style section headers:

**Module-level Classes or Functions:**

```python
# ============================================================
# QLearningAgent: 封装有 Q-Table 及其更新法则的强化学习类
#                 Reinforcement learning class encapsulating Q-Table and its update rules
# ============================================================
class QLearningAgent:
    ...
```

**Class Methods (Indented):**

```python
# ============================================================
# train: 训练Q-Learning智能体
#        Train Q-Learning agent
#
# Parameters:
#   env: Gymnasium环境实例
#        Gymnasium environment instance
#   episodes: 训练回合数
#             Number of training episodes
#   gamma: 折扣因子
#          Discount factor
#   line_width: 分隔线宽度
#               Width of the divider line
#
# Returns:
#   tuple[list, list]: (episode_returns, episode_steps)
# ============================================================
def train(env, episodes: int, gamma: float, line_width: int) -> tuple[list, list]:
    """训练Q-Learning智能体
    Train Q-Learning agent"""
    ...
```

**Rules for Methods:**

- Place the header **above** the `def` inside the class.
- Align descriptions vertically under the parameter name.
- English-only section headers (`Parameters:`, `Returns:`, `Notes:`).
- Bilingual item descriptions.

## 3. Inline Comments (Line-by-Line Bilingual)

Chinese comment immediately followed by English comment, placed ABOVE code:

```python
# 初始化Q表，使用随机值
# Initialize Q-table with random values
qtable = [[random.random() for _ in range(env.actions())] for _ in range(env.states())]

# 增加步数计数
# Increment step count
steps += 1
```

**Rules:**

- Comment goes ABOVE the code, NOT beside it
- Chinese line first, English line immediately after (no blank line between)
- Blank line AFTER comments and before next code block
- For complex logic, add explanation:

```python
# 使用贝尔曼方程更新Q表：Q(s,a) = r + γ * max Q(s',a')
# Update Q-table using Bellman equation: Q(s,a) = r + γ * max Q(s',a')
qtable[state][action] = reward + gamma * max(qtable[next_state])

# 衰减探索率，随着学习进行减少随机探索
# Decay exploration rate, reduce random exploration as learning progresses
epsilon -= decay * epsilon
```

## 4. Code Spacing

**IMPORTANT:** Always add blank lines between code blocks:

```python
# 打印程序标题
# Print program header
print("=" * 50)

# 创建悬崖行走环境
# Create Cliff Walking environment
env = GridEnv(size=12)

# 设置超参数
# Set hyperparameters
EPISODES = 50
GAMMA = 0.9
```

**Rules:**

- Blank line after each code block
- No blank line between Chinese and English comments
- Comments always above code, never beside it

## 5. Complex Logic Comments

For complex logic with multiple lines, keep Chinese and English paired line-by-line:

```python
# 使用贝尔曼方程更新Q表：Q(s,a) = r + γ * max Q(s',a')
# Update Q-table using Bellman equation: Q(s,a) = r + γ * max Q(s',a')
# 这里alpha=1，即完全替换旧值（不使用加权平均）
# Here alpha=1, meaning completely replace old value (no weighted average)
# 完整公式应为：Q(s,a) = Q(s,a) + α * [r + γ * max Q(s',a') - Q(s,a)]
# Full formula should be: Q(s,a) = Q(s,a) + α * [r + γ * max Q(s',a') - Q(s,a)]
qtable[state][action] = reward + gamma * max(qtable[next_state])

# 检查是否掉下悬崖（底行，第1-10列）
# Check if agent fell off cliff (bottom row, columns 1-10)
# 原因：悬崖行走问题的核心机制，大负奖励惩罚掉入悬崖
# Reason: Core mechanism of Cliff Walking problem, large negative reward penalizes falling
if self.y == 3 and 1 <= self.x <= 10:
    reward = -100
```

## 6. API Parameter Comments

When calling APIs with multiple parameters (e.g. OpenCV, scikit-learn), explain **what each parameter does** and **why that value was chosen**, not just restate the parameter name.

```python
# ❌ BAD - Just restating parameter names (读完还是不知道在做什么)
# 参数：127 是阈值，255 是最大值，THRESH_BINARY 是二值化模式
# Parameters: 127 is threshold, 255 is max value, THRESH_BINARY is binarization mode
_, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# ✅ GOOD - Explain what each value actually does
# 参数：127 是明暗分界线（亮度 > 127 的像素变白，≤ 127 的变黑），
#       255 是"变白"后赋予的像素值（纯白），
#       THRESH_BINARY 表示输出只有纯黑(0)和纯白(255)两种结果
# Parameters: 127 is the brightness cutoff (pixels > 127 become white, ≤ 127 become black),
#       255 is the value assigned to "white" pixels (pure white),
#       THRESH_BINARY means output has only two values: black(0) and white(255)
_, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
```

```python
# ❌ BAD - Parameter names without meaning
# 参数：[img] 是源图，[i] 是通道索引，None 是掩码，[256] 是分箱数
# Parameters: [img] is source, [i] is channel index, None is mask, [256] is bin count

# ✅ GOOD - Explain purpose and effect of each value
# 参数：[img] 将原图包在列表里传入（API 支持同时处理多张图），
#       [i] 指定计算第几个通道（0=蓝, 1=绿, 2=红），
#       None 表示不使用掩码（即统计整幅图而非局部区域），
#       [256] 表示将像素值分成 256 个柱子来统计（每个亮度值一个柱子），
#       [0, 256] 限定只统计亮度在 0~255 之间的像素
# Parameters: [img] wraps image in a list (API supports multiple images at once),
#       [i] specifies which channel to compute (0=Blue, 1=Green, 2=Red),
#       None means no mask (count all pixels, not just a sub-region),
#       [256] splits pixel values into 256 bins (one bin per intensity level),
#       [0, 256] only counts pixels with intensity between 0 and 255
hist = cv2.calcHist([img], [i], None, [256], [0, 256])
```

**Rules:**

- Explain what the value **does** (effect), not just what it **is** (name)
- For numeric values: explain why this specific number was chosen, and what changing it would do
- For enum/flag values: explain the behavior it selects
- For optional values like `None`: explain what it means to omit it
- Use `#       ` (7 spaces) for continuation lines to align with the first parameter description
- Keep Chinese and English paired, same as inline comments

## 7. Import Comments

### 7.1 Simple Imports (单独/不相关的 import)

Add bilingual comments above imports:

```python
# 导入抽象基类模块，用于定义环境接口
# Import abstract base class module for defining environment interface
import abc

# 导入操作系统、时间和随机模块
# Import os, time and random modules
import os
import time
import random
```

### 7.2 Storyline Imports (故事线风格 — 用于有逻辑关联的 import 组)

When multiple imports form a **logical pipeline** (e.g., ML/DL framework, data processing chain), use a **storyline narrative** with a causal chain: **problem → motivation → solution → next problem**.

**Rules:**

- Use ❶❷❸❹ numbered steps to show the causal chain
- **Chinese on top, English on bottom** (same as all comments)
- Each step answers: "Why do we need this?" — motivated by the previous step's gap
- Wrap in `# ================================================================` (64 chars) borders
- All `import` statements go together **after** the storyline block

**Example:**

```python
# ================================================================
# 导入 TensorFlow 和 Keras 模块
# Import TensorFlow and Keras modules
# ================================================================
#
# 🎬 故事线：从"有一堆温度数据"到"能预测未来温度"，我们需要哪些工具？
# 🎬 Storyline: from "a pile of temperature data" to "predicting future temps", what tools do we need?
#
# ❶ 首先，我们需要一个能做大量数学运算的引擎 → TensorFlow
#    First, we need an engine for heavy math (matrix ops, gradients) → TensorFlow
#    但直接用太底层了，所以它自带了 Keras 这个简化工具包
#    But raw TensorFlow is too low-level, so it ships with Keras as a simplified toolkit
#
# ❷ 有了引擎，我们要搭建一个神经网络模型 → Sequential
#    With the engine ready, we need to build a model → Sequential
#    Sequential 就是"流水线"：按顺序放入各层，数据自动从头流到尾
#    Sequential is a "pipeline": stack layers in order, data flows start to end
#
# ❸ 流水线里放什么层？取决于任务需求：
#    What layers go in? Depends on the task:
#    → Dense：全连接层，每个神经元看到上一层所有输出
#      Dense: fully connected layer, each neuron sees all previous outputs
#    → SimpleRNN：循环层，逐步处理时间数据，有"记忆"能力
#      SimpleRNN: recurrent layer, processes time data step by step, has "memory"
#    → Dropout：随机关掉一部分神经元，防止过拟合
#      Dropout: randomly shuts off neurons, prevents overfitting
#    → Flatten：把二维数据拍平成一维，因为 Dense 只接受一维输入
#      Flatten: reshapes 2D to 1D, because Dense only accepts 1D input
#
# ❹ 模型有了，但神经网络不能直接吃一整条时间序列
#    Model is ready, but neural networks can't consume an entire time series
#    它需要固定大小的"输入→输出"样本对 → TimeseriesGenerator
#    They need fixed-size "input→output" pairs → TimeseriesGenerator
#
# ================================================================

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, SimpleRNN, Dropout, Flatten
from tensorflow.keras.preprocessing.sequence import TimeseriesGenerator
```

**When to use storyline style:**

- ML/DL framework imports (TensorFlow, Keras, PyTorch, scikit-learn pipelines)
- Data processing chains (load → transform → visualize)
- Any group of 3+ related imports that form a logical workflow

## 10. Environment Setup Pattern

All "environment noise" (loading env, setting plot styles, student info) should be placed **inline at the top** of the script, right after imports and constants. Do NOT wrap in a function.

```python
# ============================================================
# 环境设置
# Environment Setup
# ============================================================

# 加载环境变量
# Load environment variables
load_dotenv('.env.local')
STUDENT_NAME = os.getenv('NAME', '[Your Name]')

# 创建输出目录
# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)
```

## 9. No Magic Numbers

All numeric literals with domain meaning must be extracted to named constants at module or class level. Only trivially obvious values (0, 1, -1, 2 for halving/doubling) may remain inline.

```python
# ❌ BAD - Magic numbers scattered in code
model = DQN("MultiInputPolicy", env, learning_rate=1e-3, buffer_size=50000)
if steps > 1000:
    break
window = pygame.display.set_mode((800, 300))

# ✅ GOOD - Named constants grouped with box-style section headers
# ============================================================
# 训练超参数
# Training Hyperparameters
# ============================================================

# DQN学习率：0.001（即 1/1000），控制网络权重更新步长
# DQN learning rate: 0.001, controls the step size of network weight updates
DQN_LEARNING_RATE = 0.001

# 经验回放缓冲区大小
# Experience replay buffer size
DQN_BUFFER_SIZE = 50000

# ============================================================
# 安全与限制常量
# Safety & Limit Constants
# ============================================================

# 每回合最大步数（安全机制，防止无限循环）
# Max steps per episode (safety mechanism to prevent infinite loops)
MAX_STEPS_PER_EPISODE = 1000

# ============================================================
# 渲染常量
# Rendering Constants
# ============================================================

# PyGame窗口宽度（像素）
# PyGame window width (pixels)
WINDOW_WIDTH = 800

model = DQN("MultiInputPolicy", env, learning_rate=DQN_LEARNING_RATE, buffer_size=DQN_BUFFER_SIZE)
if steps > MAX_STEPS_PER_EPISODE:
    break
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
```

**Rules:**

- Constants go at module level (after imports) or class level (class attributes)
- Use UPPER_SNAKE_CASE naming
- Each constant gets a bilingual comment explaining its purpose
- Group related constants under box-style section headers (`# ============...` top and bottom, bilingual title)
- Colors, dimensions, thresholds, hyperparameters, limits — all must be constants
- **No scientific notation**: Use descriptive decimal constants (e.g., `0.001`) instead of scientific notation (`1e-3`) for accessibility.
- Exception: 0, 1, -1, True, False, None, and simple arithmetic factors (2 for halving) may stay inline

## Comment Checklist

Before finishing:

- [ ] File-level docstring is English only
- [ ] All function docstrings use two-line format: Chinese first line, English second line
- [ ] All inline comments have Chinese line immediately followed by English line
- [ ] Comments are placed ABOVE code, not beside it
- [ ] No blank line between Chinese and English lines (in both docstrings and comments)
- [ ] Blank line between each code block
- [ ] Complex logic has explanation and reason
- [ ] API parameters explain what each value does, not just its name
- [ ] EVERY single line of code has a bilingual comment above it
- [ ] Import statements have bilingual comments
- [ ] **Box-style class headers ABOVE all class definitions**
- [ ] **Dividers are exactly 60 characters long**
- [ ] **Every step uses 60-char `=` dividers at top level (not plain comments)**
- [ ] **No scientific notation (use decimal 0.001 instead)**
- [ ] No magic numbers — all meaningful numeric literals are named constants
- [ ] **Algorithm/Concept comments use structured template** (定义/公式/举例/优点)

## Quick Reference

```python
# File docstring (English only)
"""
Lab 2: Q-Learning Agent
Implements Q-Learning algorithm
"""

# Function docstring (two-line bilingual)
def train(env):
    """训练Q-Learning智能体
    Train Q-Learning agent"""

# Inline comment (line-by-line bilingual, above code)
# 初始化Q表，使用随机值
# Initialize Q-table with random values
qtable = [[random.random() for _ in range(env.actions())] for _ in range(env.states())]

# 增加步数计数
# Increment step count
steps += 1
```

## Key Rules Summary

1. **Function docstrings**: Two lines - Chinese first line, English second line (NO blank line between)
2. **Inline comments**: Chinese line, English line, then code (NO blank line between Chinese/English)
3. **Comment placement**: Always ABOVE code, never beside it
4. **Code spacing**: Blank line after each code block
5. **No blank line**: Between Chinese and English lines (both in docstrings and comments)
6. **API parameters**: Explain what each value DOES and WHY, not just restate parameter names
7. **No magic numbers**: All meaningful numeric literals must be named constants (UPPER_SNAKE_CASE)
8. **Flat sequential style**: All code runs top-to-bottom, no `main()` wrapper — step dividers are at the top level

## Complete Example

```python
"""
Lab 4: Webcam Video with Timestamp Overlay
Student ID: 041107730
Streams live webcam video and overlays current time.
"""

# 导入OpenCV库
# Import OpenCV library
import cv2

# 导入时间模块
# Import time modules
from datetime import datetime
import time

# ============================================================
# 配置常量
# Configuration Constants
# ============================================================

# 默认摄像头索引
# Default camera index
CAMERA_INDEX = 0

# 字体设置
# Font settings
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.7
FONT_COLOR = (0, 255, 0)
FONT_THICKNESS = 2

# ============================================================
# 步骤 1：初始化摄像头
# Step 1: Initialize Webcam
# ============================================================

# 创建VideoCapture对象
# Create VideoCapture object
cap = cv2.VideoCapture(CAMERA_INDEX)

# ============================================================
# 步骤 2：视频流主循环
# Step 2: Video Stream Main Loop
# ============================================================

# 无限循环，持续捕获帧画面
# Infinite loop to continuously capture frames
while True:
    # 读取一帧
    # Read one frame
    ret, frame = cap.read()

    # 获取当前时间戳
    # Get current timestamp
    timestamp = datetime.now().strftime("%H:%M:%S")

    # 叠加时间戳
    # Overlay timestamp
    cv2.putText(frame, timestamp, (10, 30), FONT, FONT_SCALE,
                FONT_COLOR, FONT_THICKNESS)

    # 显示画面
    # Display frame
    cv2.imshow("Webcam", frame)

    # 按 'q' 退出
    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ============================================================
# 步骤 3：清理资源
# Step 3: Cleanup Resources
# ============================================================

# 释放摄像头
# Release webcam
cap.release()

# 关闭窗口
# Close windows
cv2.destroyAllWindows()
```

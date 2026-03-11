---
name: source-annotation
description: 基于库源码的代码注释。Use when (1) 为调用第三方库函数的代码添加注释, (2) 用户说"源码注释"或"source annotation", (3) 需要解释库函数的内部工作原理, (4) 用户指向 .github/ 目录中的源码
---

# Source Code Annotation (源码注释)

## 核心原则 / Core Principle

> **注释必须来自源码，不能凭空编写。**
> 先去 `.github/` 查源码 → 读懂实现 → 再写注释。

## 源码仓库映射 / Source Repository Mapping

| 库 Library   | `.github/` 路径         | GitHub URL 前缀                                         |
| ------------ | ----------------------- | ------------------------------------------------------- |
| Keras        | `.github/keras/`        | https://github.com/keras-team/keras/blob/main/          |
| TensorFlow   | `.github/tensorflow/`   | https://github.com/tensorflow/tensorflow/blob/master/   |
| scikit-learn | `.github/scikit-learn/` | https://github.com/scikit-learn/scikit-learn/blob/main/ |
| NumPy        | `.github/numpy/`        | https://github.com/numpy/numpy/blob/main/               |
| PyTorch      | `.github/pytorch/`      | https://github.com/pytorch/pytorch/blob/main/           |
| statsmodels  | (本地 site-packages)    | https://github.com/statsmodels/statsmodels/blob/main/   |

## 工作流程 / Workflow

1. **识别**：找到代码中调用的库函数/类
2. **查找**：用 `grep_search` 在 `.github/` 对应库中找到定义
3. **阅读**：用 `view_code_item` 读取核心方法（`__init__`、`__getitem__`、`fit`、`call` 等）
4. **提炼**：提取核心源码逻辑 + 构造具体举例
5. **写注释**：按下方模板输出

---

## 注释模板 / Comment Template

### 结构（5 个子项，顺序固定）

```
# ================================================================
# 源码解析：中文名（英文名）
# Source Analysis: English Name
# ================================================================
#
# -------- Source Analysis --------
#
# Source:
#   文件路径 → 类名/函数名
#   GitHub URL
#
# What:
#   中文一句话概括
#   English one-line summary
#
# Why:
#   中文解释为什么需要它
#   English explanation
#
# How:
#   源码核心逻辑（简化版）：
#   代码行1
#   代码行2
#
#   举例（假设 具体数字）：
#   步骤1 → 结果
#   步骤2 → 结果
#   中文总结
#   English summary
#
# API:
#   签名: ClassName(param1, param2, param3=default, ...)
#   用法: ClassName(我们传的值1, 我们传的值2, param3=我们的值)
#   中文解释为什么这样传参
#   English explanation
# ================================================================
```

### 子项说明

| 序号 | 子项   | 说明                                                     |
| ---- | ------ | -------------------------------------------------------- |
| 1    | Source | 源码文件路径 → 类/函数名 + GitHub URL                    |
| 2    | What   | 一句话概括功能（中英双语）                               |
| 3    | Why    | 为什么需要它（中英双语）                                 |
| 4    | How    | 源码核心逻辑（简化伪代码）+ 具体数字举例 + 中英文总结    |
| 5    | API    | 源码方法签名 + 我们的实际用法 + 参数选择原因（中英双语） |

### 语言规则

| 位置           | 语言                               |
| -------------- | ---------------------------------- |
| 盒子标题       | 第一行中文+英文名，第二行 English  |
| section 分隔线 | English only (`Source Analysis`)   |
| 子项标签       | English only (`What`, `Why`, etc.) |
| 内容           | 中英双语（中文在上，英文在下）     |
| 源码/代码引用  | 代码原文，不翻译                   |
| How 的举例     | 数字 + 符号，不需要翻译            |

### ⚠️ 重要规则

- **所有**源码注释都使用完整盒子格式，不存在"简化版"
- 无论是独立 API 调用还是 Sequential 内部的层，格式完全一致
- 每个盒子紧贴在对应的代码行上方

---

## 完整示例 / Examples

### 示例 1: TimeseriesGenerator

```python
# ================================================================
# 源码解析：时间序列样本生成器（TimeseriesGenerator）
# Source Analysis: TimeseriesGenerator
# ================================================================
#
# -------- Source Analysis --------
#
# Source:
#   keras/src/legacy/preprocessing/sequence.py → class TimeseriesGenerator
#   https://github.com/keras-team/keras/blob/main/keras/src/legacy/preprocessing/sequence.py
#
# What:
#   把一整条时间序列自动切成"前N步→预测下一步"的固定大小样本对
#   Auto-slices a time series into fixed-size "past N steps → predict next" sample pairs
#
# Why:
#   神经网络不能直接吃一整条长度不定的序列，必须切成固定窗口喂进去
#   Neural networks require fixed-size inputs, not variable-length sequences
#
# How:
#   源码 __getitem__ 核心逻辑（简化版）：
#   for row in rows:
#       samples.append( data[row - length : row] )
#       targets.append( targets[row] )
#
#   举例（data=[10,11,12,13,14,15], length=3）：
#   row=3 → input=[10,11,12], target=13
#   row=4 → input=[11,12,13], target=14
#   row=5 → input=[12,13,14], target=15
#   窗口每次前移一步，取前3个预测下一个
#   Window slides forward one step, takes 3 past points to predict the next
#
# API:
#   签名: TimeseriesGenerator(data, targets, length, sampling_rate=1, stride=1, batch_size=128, ...)
#   用法: TimeseriesGenerator(train_normalized, train_normalized, length=WINDOW_SIZE, batch_size=BATCH_SIZE)
#   data 和 targets 传同一个数组 = 自回归（用 past 预测 future）
#   Same array for data & targets = autoregressive (predict future from past)
# ================================================================
train_generator = TimeseriesGenerator(train_normalized, train_normalized,
                                       length=WINDOW_SIZE, batch_size=BATCH_SIZE)
```

### 示例 2: Dense 层

```python
    # ================================================================
    # 源码解析：全连接层（Dense）
    # Source Analysis: Dense Layer
    # ================================================================
    #
    # -------- Source Analysis --------
    #
    # Source:
    #   keras/src/layers/core/dense.py → class Dense
    #   https://github.com/keras-team/keras/blob/main/keras/src/layers/core/dense.py
    #
    # What:
    #   每个神经元与所有输入做矩阵乘法 + 偏置 + 激活
    #   Each neuron performs matrix multiply with all inputs + bias + activation
    #
    # Why:
    #   将输入特征进行线性组合再通过激活函数引入非线性，是神经网络的基本构建块
    #   Linearly combines input features then applies non-linearity; the basic building block of neural networks
    #
    # How:
    #   源码 call() 核心逻辑：
    #   x = ops.matmul(inputs, self.kernel)
    #   x = ops.add(x, self.bias)
    #   x = self.activation(x)
    #
    #   举例（输入 12 维, units=64）：
    #   输入 (12,) × kernel (12, 64) + bias (64,) → 输出 (64,)
    #   没有 activation 时直接输出 matmul + bias 的原始值（用于回归）
    #   Without activation, raw matmul + bias value is output directly (for regression)
    #
    # API:
    #   签名: Dense(units, activation=None, use_bias=True, ...)
    #   用法: Dense(64, activation='relu')
    #   64 个神经元提取特征，ReLU 引入非线性（没有它多层 Dense 等价于一层）
    #   64 neurons extract features, ReLU adds non-linearity (without it, stacked Dense = single layer)
    # ================================================================
    Dense(DENSE_UNITS_1, activation='relu'),
```

---

## 判断规则 / When to Use

| 场景                                     | 使用源码注释？ |
| ---------------------------------------- | -------------- |
| 用户明确说"源码注释"/"source annotation" | ✅ 必须        |
| 用户指向了 `.github/` 中的某个库         | ✅ 必须        |
| ML/DL 框架核心构建 API                   | ✅ 推荐        |
| 简单语句（`print`, 赋值, 控制流）        | ❌ 用普通注释  |
| `.github/` 中没有该库源码                | ⚠️ 标注来源    |

## 与 code-comment skill 的关系

- **格式基础**：盒子边框用 64 字符 `=`（与 code-comment 概念模板一致）
- **互补使用**：算法/数学概念 → `code-comment` 的算法原理模板；库 API 调用 → 本 skill 的源码解析模板
- **所有源码注释统一用完整盒子**，无简化版

## Checklist

- [ ] 盒子用 `# ================================================================`（64 字符）
- [ ] section 用 `# -------- Source Analysis --------`
- [ ] 5 个子项齐全且顺序正确：Source → What → Why → How → API
- [ ] How 包含源码核心逻辑 + 具体数字举例 + 中英文总结
- [ ] Source 包含文件路径 + GitHub URL
- [ ] API 包含签名 + 用法 + 参数选择原因
- [ ] 子项标签用 English，内容用中英双语
- [ ] `.github/` 中找不到源码时已标注来源

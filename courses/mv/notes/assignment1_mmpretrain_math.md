# Assignment 1 数学公式速查 — Math Quick Reference

> **See also:** [概念速查](assignment1_mmpretrain_cheatsheet.md) | [代码参考](assignment1_mmpretrain_code.md)  
> **来源:** CST8508 Assignment 1 + Week 4-5 Slides

---

## 📏 卷积输出尺寸

$$O = \frac{W - F + 2P}{S} + 1$$

| 符号 | 含义           | 常用值 |
| ---- | -------------- | ------ |
| W    | 输入尺寸       | 224    |
| F    | 滤波器尺寸     | 3      |
| P    | 填充 (padding) | 1      |
| S    | 步幅 (stride)  | 1      |
| O    | 输出尺寸       | —      |

### 📝 手算练习

```
Q: 输入 224×224，滤波器 3×3，padding=1，stride=1，输出？
A: O = (224 - 3 + 2×1) / 1 + 1 = 224

Q: 输入 224×224，滤波器 7×7，padding=3，stride=2，输出？
A: O = (224 - 7 + 2×3) / 2 + 1 = 112
```

---

## ⚖️ 深度可分离卷积参数量

**标准卷积：**

$$\text{Params}_{\text{standard}} = K \times K \times C_{in} \times C_{out}$$

**深度可分离卷积：**

$$\text{Params}_{\text{depthwise}} = K \times K \times C_{in} + C_{in} \times C_{out}$$

### 📝 手算练习

```
Q: 3×3 卷积，输入 64 通道，输出 128 通道
标准: 3 × 3 × 64 × 128 = 73,728
深度可分离: 3 × 3 × 64 + 64 × 128 = 576 + 8,192 = 8,768
节省: 1 - 8768/73728 = 88.1%
```

---

## 🎯 Softmax 函数

$$\text{Softmax}(z_i) = \frac{e^{z_i}}{\sum_{j=1}^{C} e^{z_j}}$$

| 符号  | 含义                                |
| ----- | ----------------------------------- |
| $z_i$ | 第 i 类的 logit（全连接层原始输出） |
| C     | 类别总数（Assignment 1 = 17）       |

### 📝 手算练习

```
Q: logits = [2.0, 1.0, 0.5]，求 Softmax
A: e^z = [7.389, 2.718, 1.649]
   sum = 11.756
   Softmax = [0.629, 0.231, 0.140]
   验证: 0.629+0.231+0.140 = 1.000 ✓
```

---

## 📉 交叉熵损失 (Cross-Entropy Loss)

$$L = -\sum_{i=1}^{C} y_i \log(\hat{y}_i) = -\log(\hat{y}_c)$$

| 符号        | 含义                          |
| ----------- | ----------------------------- |
| $y_i$       | one-hot 真实标签的第 i 个元素 |
| $\hat{y}_i$ | Softmax 输出的第 i 个元素     |
| $c$         | 正确类别的索引                |

**化简：** 对 one-hot 标签，只有正确类别 $y_c=1$，其余为 0

### 📝 手算练习

```
Q: 真实类别=0，预测概率 ŷ=[0.8, 0.1, 0.1]，损失？
A: L = -log(0.8) = 0.223

Q: 真实类别=0，预测概率 ŷ=[0.1, 0.8, 0.1]，损失？
A: L = -log(0.1) = 2.303  ← 差的预测，损失大！
```

---

## 🏃 SGD + Momentum 更新规则

$$v_t = \mu \cdot v_{t-1} + g_t$$
$$W_t = W_{t-1} - \eta \cdot v_t$$

| 符号   | 含义     | Assignment 1 值 |
| ------ | -------- | --------------- |
| $\eta$ | 学习率   | 0.01 (ResNet)   |
| $\mu$  | 动量系数 | 0.9             |
| $g_t$  | 梯度     | ∂L/∂W           |

---

## 🧠 Adam 更新规则

$$m_t = \beta_1 m_{t-1} + (1-\beta_1) g_t$$
$$v_t = \beta_2 v_{t-1} + (1-\beta_2) g_t^2$$
$$\hat{m}_t = m_t / (1-\beta_1^t), \quad \hat{v}_t = v_t / (1-\beta_2^t)$$
$$W_t = W_{t-1} - \eta \cdot \hat{m}_t / (\sqrt{\hat{v}_t} + \epsilon)$$

| 符号      | 含义       | Assignment 1 值   |
| --------- | ---------- | ----------------- |
| $\eta$    | 学习率     | 0.001 (MobileNet) |
| $\beta_1$ | 一阶矩衰减 | 0.9               |
| $\beta_2$ | 二阶矩衰减 | 0.999             |

---

## 🌊 余弦退火学习率

$$\eta_t = \eta_{min} + \frac{1}{2}(\eta_{max} - \eta_{min})\left(1 + \cos\left(\frac{t}{T_{max}} \cdot \pi\right)\right)$$

| 符号         | 含义        | 值           |
| ------------ | ----------- | ------------ |
| $T_{max}$    | 总 epoch 数 | 100          |
| $\eta_{max}$ | 初始学习率  | 0.01 / 0.001 |
| $\eta_{min}$ | 最终学习率  | 0            |

### 📝 手算练习

```
Q: η_max=0.01, T_max=100, t=50
A: η = 0.5 × 0.01 × (1 + cos(π/2)) = 0.005 × 1 = 0.005
```

---

## 📊 评估指标

$$\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}$$

$$\text{Precision} = \frac{TP}{TP + FP}$$

$$\text{Recall} = \frac{TP}{TP + FN}$$

$$\text{F1} = \frac{2 \times P \times R}{P + R} = \frac{2 \cdot TP}{2 \cdot TP + FP + FN}$$

### 📝 手算练习

```
Q: TP=7, TN=6, FP=2, FN=3
A: Accuracy = (7+6)/(7+6+2+3) = 13/18 = 0.722
   Precision = 7/(7+2) = 0.778
   Recall = 7/(7+3) = 0.700
   F1 = 2×0.778×0.700/(0.778+0.700) = 0.737
```

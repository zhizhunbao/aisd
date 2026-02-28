# Assignment 1: mmpretrain Image Classification — Quiz

> **课程:** CST8508 Machine Vision  
> **范围:** Assignment 1 (mmpretrain, ResNet-18, MobileNet V2, Oxford Flowers 17)

---

## Part A: Multiple Choice (10 questions)

### Q1. OpenMMLab 的核心设计理念是什么？

A) 所有代码都用 Jupyter Notebook  
B) 每次训练都从零写训练循环  
C) **配置驱动 + 模块化 + 注册器机制**  
D) 仅支持 ResNet 系列模型

### Q2. mmpretrain 的 SubFolder 格式要求数据如何组织？

A) 所有图片放在一个文件夹，用 CSV 标注  
B) **每个类别一个子文件夹，文件夹名 = 类名**  
C) 所有图片按编号命名，用 JSON 标注  
D) 按日期分文件夹

### Q3. ResNet 的核心创新是什么？

A) 使用 3×3 卷积核  
B) Dropout 正则化  
C) **残差连接（Skip Connection），让输入跳过若干层直接加到输出**  
D) 深度可分离卷积

### Q4. ResNet 的残差连接解决了什么问题？

A) 过拟合问题  
B) 数据不平衡问题  
C) **退化问题（更深的网络训练误差反而更高）**  
D) 梯度爆炸问题

### Q5. MobileNet V2 用什么技术减少参数量？

A) 减少网络层数  
B) **深度可分离卷积 = 深度卷积 + 逐点卷积**  
C) 只使用 1×1 卷积  
D) 移除池化层

### Q6. 在 Assignment 1 中，参数更少的 MobileNet V2 反而比 ResNet-18 准确率更高，最可能的原因是？

A) MobileNet V2 的架构本身就比 ResNet 先进  
B) MobileNet V2 用了预训练权重  
C) **Adam 优化器在小数据集上收敛更好 + 更少参数减少过拟合**  
D) ResNet-18 的配置文件有错误

### Q7. 余弦退火（Cosine Annealing）学习率调度的特点是？

A) 学习率线性下降  
B) 学习率每 10 个 epoch 减半  
C) **学习率按余弦曲线从大到小衰减，前期慢降后期快降**  
D) 学习率保持不变

### Q8. 在 mmpretrain 配置文件中，`_base_` 的作用是？

A) 定义数据集路径  
B) 指定 GPU 编号  
C) **继承父配置文件，子配置只需写需要修改的部分**  
D) 设定随机种子

### Q9. 交叉熵损失 CrossEntropy Loss 对 one-hot 标签简化后等于？

A) MSE(y, ŷ)  
B) |y - ŷ|  
C) **-log(ŷ_c)，其中 c 是正确类别的索引**  
D) -(y × ŷ)

### Q10. 混淆矩阵的主要用途是？

A) 计算训练时间  
B) 衡量模型大小  
C) **找出哪些类别容易互相混淆**  
D) 确定最佳学习率

---

## Part B: True/False (5 questions)

### Q11. 数据增强（Data Augmentation）应该同时应用于训练集和验证集。

**False** — 验证集不做数据增强，保持确定性以准确评估模型泛化能力。

### Q12. 在 mmpretrain 中，改变模型架构（如从 ResNet 换到 MobileNet）需要修改训练循环代码。

**False** — 只需修改配置文件中的 `model` 字典，训练代码完全不用改。

### Q13. SGD 优化器在所有情况下都比 Adam 差。

**False** — SGD 在大数据集上经过精心调参后可以达到比 Adam 更好的最终解。Adam 在小数据集和默认参数下表现更好。

### Q14. ResNet-18 的 "18" 指的是 18 个卷积层。

**False** — 指的是 18 层（包括卷积层和全连接层），具体有 4 个残差阶段。

### Q15. 深度可分离卷积（3×3, 64→128）的参数量约为标准卷积的 12%。

**True** — 标准: 3×3×64×128=73,728; 深度可分离: 3×3×64+64×128=8,768; 比例: 8768/73728≈11.9%

---

## Part C: Short Answer (3 questions)

### Q16. 计算题：给定输入 112×112，滤波器 3×3，padding=0，stride=2，输出尺寸是多少？

**答案：**
$$O = \frac{W - F + 2P}{S} + 1 = \frac{112 - 3 + 0}{2} + 1 = \frac{109}{2} + 1 = 54 + 1 = 55$$

输出尺寸为 **55×55**。

---

### Q17. 为什么 Assignment 1 的配置文件必须添加 `test_dataloader = val_dataloader`？

**答案：**
`ImageClassificationInferencer` 推理器在初始化时需要读取完整配置，其中包括 `test_dataloader` 字段。如果配置中只定义了 `train_dataloader` 和 `val_dataloader` 而没有 `test_dataloader`，推理器会报 `KeyError`。将验证集配置复用为测试集配置是最简单的解决方案。

---

### Q18. 对比 ResNet-18 和 MobileNet V2 在 Assignment 1 中的表现，分析 MobileNet V2 获胜的三个可能原因。

**答案：**

1. **优化器差异：** MobileNet V2 使用 Adam（自适应学习率），在小数据集（每类仅 62 张）上收敛更稳定；ResNet-18 使用 SGD，对学习率更敏感且在噪声大的小数据集上需要更精细的调参。

2. **模型容量匹配：** MobileNet V2 只有 3.4M 参数，与小数据集的规模更匹配，过拟合风险更低。ResNet-18 有 11.7M 参数，在仅 1054 张训练图上更容易过拟合。

3. **架构效率：** MobileNet V2 的倒残差结构在低维→高维→低维的过程中保留了更多信息，深度可分离卷积虽然参数少但表达能力并不弱。

---

## Answer Key

| 题号 | 答案 | 题号 | 答案        |
| ---- | ---- | ---- | ----------- |
| Q1   | C    | Q11  | False       |
| Q2   | B    | Q12  | False       |
| Q3   | C    | Q13  | False       |
| Q4   | C    | Q14  | False       |
| Q5   | B    | Q15  | True        |
| Q6   | C    | Q16  | 55×55       |
| Q7   | C    | Q17  | (see above) |
| Q8   | C    | Q18  | (see above) |
| Q9   | C    |      |             |
| Q10  | C    |      |             |

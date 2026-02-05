# CST8506 - Lab 3

## Classification by CNN

**Student Name:** Peng Wang

**Student Number:** 041107730

---

For every step, include screenshot of the code and the corresponding results in this document (screenshot from colab/jupyter notebook). Also, in your words, explain your code and results. If there is no explanation, no marks will be given. No need to write long paragraphs, but one or 2 lines per step. Even if you are using default parameters, you must mention the default values and its meaning.

---

## 1. Load data

**Code Screenshot:**

![Step 1 Code](../code/lab3/lab3_images/lab3_cnn_step01_code.png)

**Output Screenshot:**

![Step 1 Output](../code/lab3/lab3_images/lab3_cnn_step01_result.png)

**Explanation:** 使用 Keras 的 `mnist.load_data()` 加载 MNIST 数据集，返回训练集和测试集的图像及标签。

---

## 2. Number of images in the train set:

**Number of images in train set:** 60000

**Number of images in test set:** 10000

**Code Screenshot:**

![Step 2 Code](../code/lab3/lab3_images/lab3_cnn_step02_code.png)

**Output Screenshot:**

![Step 2 Output](../code/lab3/lab3_images/lab3_cnn_step02_result.png)

**Explanation:** 使用 `shape[0]` 获取数据集第一维的大小，即图片数量。每张图片为 28x28 像素的灰度图。

---

## 3. First 5 images (all images in one row, parallel):

**Code Screenshot:**

![Step 3 Code](../code/lab3/lab3_images/lab3_cnn_step03_code.png)

**Output Screenshot:**

![Step 3 Output](../code/lab3/lab3_images/step3_first_5_images.png)

**Explanation:** 使用 `matplotlib.subplots(1, 5)` 创建 1 行 5 列布局，用 `imshow(cmap='gray')` 显示灰度图像。

---

## 4. Reshape

**Code Screenshot:**

![Step 4 Code](../code/lab3/lab3_images/lab3_cnn_step04_code.png)

**Output Screenshot:**

![Step 4 Output](../code/lab3/lab3_images/lab3_cnn_step04_result.png)

**Explanation:** 将图像 reshape 为 (samples, 28, 28, 1)，添加 channel 维度。灰度图 channel=1，RGB 图 channel=3。

---

## 5. Normalize

**Code Screenshot:**

![Step 5 Code](../code/lab3/lab3_images/lab3_cnn_step05_code.png)

**Output Screenshot:**

![Step 5 Output](../code/lab3/lab3_images/lab3_cnn_step05_result.png)

**Explanation:** 将像素值从 [0, 255] 归一化到 [0, 1]，除以 255.0。归一化帮助加速收敛和提高训练稳定性。

---

## 6. Encoding

**Code Screenshot:**

![Step 6 Code](../code/lab3/lab3_images/lab3_cnn_step08_code.png)

**Output Screenshot:**

![Step 6 Output](../code/lab3/lab3_images/lab3_cnn_step08_result.png)

**Explanation:** 使用 `to_categorical()` 进行 One-Hot 编码。数字 5 编码为 [0,0,0,0,0,1,0,0,0,0]，第 6 位为 1。

---

## 7. Model

**Code Screenshot:**

![Step 7 Code](../code/lab3/lab3_images/lab3_cnn_step08_code.png)

**Output Screenshot:**

![Step 7 Output](../code/lab3/lab3_images/lab3_cnn_step08_result.png)

**Model Architecture:**
```
Input(28,28,1) → Conv2D(32) → MaxPool → Conv2D(64) → MaxPool → Flatten → Dense(128) → Dense(10)
```

**Parameter Explanation:**

| Parameter | Value | Meaning |
|-----------|-------|---------|
| filters | 32, 64 | 学习 32/64 个特征滤波器 |
| kernel_size | (3,3) | 3x3 卷积核大小 |
| activation | 'relu' | ReLU 激活函数，f(x)=max(0,x) |
| padding | 'same' | 零填充保持空间维度 |
| pool_size | (2,2) | 2x2 池化，维度减半 |
| units | 128, 10 | 全连接层神经元数 |
| softmax | output | 输出 10 类的概率分布 |

---

## 8. Compile model

**Code Screenshot:**

![Step 8 Code](../code/lab3/lab3_images/lab3_cnn_step09_code.png)

**Output Screenshot:**

![Step 8 Output](../code/lab3/lab3_images/lab3_cnn_step09_result.png)

**Parameters:**
- **optimizer='adam'**: Adam 优化器，自适应学习率
- **loss='categorical_crossentropy'**: 多分类交叉熵损失函数
- **metrics=['accuracy']**: 评估指标为准确率

---

## 9. Model summary

**Code Screenshot:**

![Step 9 Code](../code/lab3/lab3_images/lab3_cnn_step10_code.png)

**Output Screenshot:**

![Step 9 Output](../code/lab3/lab3_images/lab3_cnn_step10_result.png)

**Explanation:** 模型共有 421,642 个可训练参数。Dense 层占主要参数量 (3136×128=401,536)。

---

## 10. Fit, predict and print accuracy

**Code Screenshot:**

![Step 10 Code](../code/lab3/lab3_images/lab3_cnn_step11_code.png)

**Training Output:**

![Step 10 Training](../code/lab3/lab3_images/step11_training_history.png)

**Accuracy:**

![Step 10 Accuracy](../code/lab3/lab3_images/lab3_cnn_step13_result.png)

**Training Parameters:**
- **batch_size=128**: 每批 128 个样本
- **epochs=10**: 训练 10 轮
- **validation_split=0.1**: 10% 验证集

**Results:** Test Accuracy = **98.89%**, Test Loss = 0.0398

---

## 11. Predictions of first 20 instances in the given format

**Code Screenshot:**

![Step 11 Code](../code/lab3/lab3_images/lab3_cnn_step12_code.png)

**Output Screenshot:**

![Step 11 Output](../code/lab3/lab3_images/lab3_cnn_step12_result.png)

| Highest Probability | Predicted Digit | Actual Digit |
|---------------------|-----------------|--------------|
| [0.9999994] | 7 | 7 |
| [1.0000000] | 2 | 2 |
| [0.9999995] | 1 | 1 |
| [1.0000000] | 0 | 0 |
| ... | ... | ... |

**Explanation:** 使用 `np.argmax()` 找概率最高的索引作为预测数字。前 20 个中有 1 个错误预测。

---

## 12. Misclassifications

**Code Screenshot:**

![Step 12 Code](../code/lab3/lab3_images/lab3_cnn_step16_code.png)

**Output Screenshot:**

![Step 12 Output](../code/lab3/lab3_images/step16_misclassified_images.png)

**Results:**
- **Total misclassified:** 111 out of 10,000
- **Misclassification rate:** 1.11%

**Explanation:** 错分图片多为书写模糊或与其他数字相似的样本，人类也可能难以正确识别这些图像。

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

**Explanation:** 使用 Keras 的 `mnist.load_data()` 函数加载 MNIST 手写数字数据集。该数据集包含 60,000 张训练图片和 10,000 张测试图片，每张图片是 28x28 像素的灰度图像。

---

## 2. Number of images in the train set:

**Code Screenshot:**

![Step 2 Code](../code/lab3/lab3_images/lab3_cnn_step02_code.png)

**Output Screenshot:**

![Step 2 Output](../code/lab3/lab3_images/lab3_cnn_step02_result.png)

**Results:**
- Number of images in train set: **60000**
- Number of images in test set: **10000**

**Explanation:** 使用 `x_train.shape[0]` 和 `x_test.shape[0]` 获取训练集和测试集的图片数量。训练集有 60,000 张图片用于模型训练，测试集有 10,000 张图片用于评估模型性能。

---

## 3. First 5 images (all images in one row, parallel):

**Code Screenshot:**

![Step 3 Code](../code/lab3/lab3_images/lab3_cnn_step03_code.png)

**Output Screenshot:**

![Step 3 Output](../code/lab3/lab3_images/step3_first_5_images.png)

**Explanation:** 使用 matplotlib 的 `subplots(1, 5)` 创建 1 行 5 列的子图，显示前 5 张训练图片及其对应标签。使用 `imshow()` 显示灰度图像，`cmap='gray'` 指定灰度色彩映射。

---

## 4. Reshape

**Code Screenshot:**

![Step 4 Code](../code/lab3/lab3_images/lab3_cnn_step04_code.png)

**Output Screenshot:**

![Step 4 Output](../code/lab3/lab3_images/lab3_cnn_step04_result.png)

**Explanation:** 使用 `reshape()` 将图像从 (60000, 28, 28) 转换为 (60000, 28, 28, 1)，添加第 4 维度作为通道数。灰度图像使用 1 个通道，RGB 图像使用 3 个通道。CNN 的 Conv2D 层需要 4D 输入格式 (batch, height, width, channels)。

---

## 5. Normalize

**Code Screenshot:**

![Step 5 Code](../code/lab3/lab3_images/lab3_cnn_step05_code.png)

**Output Screenshot:**

![Step 5 Output](../code/lab3/lab3_images/lab3_cnn_step05_result.png)

**Explanation:** 将像素值从 [0, 255] 归一化到 [0, 1]，通过除以 255.0 实现。归一化有助于加速模型收敛、提高训练稳定性，并防止较大的像素值主导梯度更新。

---

## 6. Encoding

**Code Screenshot:**

![Step 6 Code](../code/lab3/lab3_images/step06_encoding_code.png)

**Output Screenshot:**

![Step 6 Output](../code/lab3/lab3_images/step06_encoding.png)

**Explanation:** 使用 `to_categorical()` 对标签进行 One-Hot 编码。例如数字 5 变成 [0,0,0,0,0,1,0,0,0,0]，第 6 个位置为 1。这是多分类问题中神经网络输出层的标准格式，与 softmax 激活函数配合使用。

---

## 7. Model

**Code Screenshot:**

![Step 8 Code](../code/lab3/lab3_images/step08_build_model_code.png)

**Output Screenshot:**

![Step 8 Output](../code/lab3/lab3_images/step08_build_model.png)

**Model Architecture:**
```
Input(28,28,1) → Conv2D(32) → MaxPool → Conv2D(64) → MaxPool → Flatten → Dense(128) → Dense(10)
```

**Parameter Explanation:**

| Parameter | Value | Meaning |
|-----------|-------|---------|
| filters | 32, 64 | Number of feature maps to learn |
| kernel_size | (3,3) | Size of convolution filter |
| activation | 'relu' | ReLU: f(x)=max(0,x), prevents vanishing gradient |
| padding | 'same' | Zero padding to maintain spatial dimensions |
| pool_size | (2,2) | Downsamples by factor of 2 |
| units (Dense) | 128, 10 | Neurons in fully connected layers |
| activation (output) | 'softmax' | Outputs probability distribution over 10 classes |

---

## 8. Compile model

**Code Screenshot:**

![Step 9 Code](../code/lab3/lab3_images/step09_compile_code.png)

**Output Screenshot:**

![Step 9 Output](../code/lab3/lab3_images/step09_compile.png)

**Explanation:** 
- **optimizer='adam'**: Adam 优化器，自适应学习率，结合 Momentum 和 RMSprop 优点
- **loss='categorical_crossentropy'**: 多分类交叉熵损失函数，用于多类别分类问题
- **metrics=['accuracy']**: 评估指标为准确率

---

## 9. Model summary

**Code Screenshot:**

![Step 10 Code](../code/lab3/lab3_images/step10_summary_code.png)

**Output Screenshot:**

![Step 10 Output](../code/lab3/lab3_images/step10_summary.png)

**Explanation:** 模型共有 421,642 个可训练参数。主要参数来自 Dense 层，因为 Flatten 后有 3136 个神经元连接到 128 个 Dense 神经元 (3136 × 128 = 401,536 参数)。

---

## 10. Fit, predict and print accuracy

**Code Screenshot:**

![Step 11 Code](../code/lab3/lab3_images/step11_fit_code.png)

**Training Output Screenshot:**

![Step 11 Training](../code/lab3/lab3_images/step11_training_history.png)

**Accuracy Screenshot:**

![Step 13 Accuracy](../code/lab3/lab3_images/step13_accuracy.png)

**Training Parameters:**
- **batch_size=128**: 每批处理 128 个样本
- **epochs=10**: 训练 10 轮
- **validation_split=0.1**: 10% 数据用于验证

**Results:**
- **Test Accuracy: 98.89%**
- **Test Loss: 0.0398**

---

## 11. Predictions of first 20 instances in the given format

**Code Screenshot:**

![Step 14-15 Code](../code/lab3/lab3_images/step14_predictions_code.png)

**Output Screenshot:**

![Step 14-15 Output](../code/lab3/lab3_images/step14_predictions.png)

| Highest Probability | Predicted Digit | Actual Digit |
|---------------------|-----------------|--------------|
| [0.9999994] | 7 | 7 |
| [1.0000000] | 2 | 2 |
| [0.9999995] | 1 | 1 |
| [1.0000000] | 0 | 0 |
| [0.9830225] | 4 | 4 |
| ... | ... | ... |

**Explanation:** 使用 `np.argmax()` 找到每行概率最高的索引作为预测数字。前 20 个预测中只有 1 个错误（第 19 个，预测为 5 实际为 3）。

---

## 12. Misclassifications

**Code Screenshot:**

![Step 16 Code](../code/lab3/lab3_images/step16_misclassified_code.png)

**Output Screenshot:**

![Step 16 Output](../code/lab3/lab3_images/step16_misclassified.png)

**Misclassified Images Visualization:**

![Misclassified Images](../code/lab3/lab3_images/step16_misclassified_images.png)

**Results:**
- **Total misclassified: 111 out of 10,000**
- **Misclassification rate: 1.11%**

**Explanation:** 模型错误分类了 111 张图片。分析错误样本可以发现，这些图片通常是书写模糊、不规范或与其他数字相似的手写体，即使人类也可能难以正确识别。

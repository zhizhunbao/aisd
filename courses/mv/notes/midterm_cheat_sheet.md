# CST8508 Machine Vision — Midterm Cheat Sheet 速查表

> 📅 Exam: Feb 19, 7PM | 60 min | 25 marks | Calculator ✅ | No devices ❌

---

## 1. MV Workflow 工作流

```
Image Acquisition → Image Processing → Interpretation/Action
```

- **MV定义:** Imaging-based automatic inspection & analysis
- **Pixel:** Grayscale = single value (0-255) | Color = (R, G, B)
- **Image types:** Binary (0/1), Grayscale (0-255), RGB (3 channels)

---

## 2. Image Processing 图像处理

### Filtering 滤波
| 操作 | 效果 |
|------|------|
| **Blurring** (Avg/Gaussian/Median) | 平滑降噪 |
| **Sharpening** | 增强边缘细节 |

### Canny Edge Detection (5 steps)
1. **Noise Reduction** → Gaussian blur
2. **Gradient Calculation** → Sobel (magnitude + direction)
3. **Non-Maximum Suppression** → 细化边缘
4. **Double Thresholding** → 强/弱/非边缘
5. **Edge Tracking by Hysteresis** → 弱边缘连强边缘则保留

### Histogram 直方图
- **X轴** = brightness levels (0-255)
- **Y轴** = pixel count

### Thresholding 阈值
| 类型 | 用途 |
|------|------|
| Binary | 固定阈值，均匀光照 |
| **Adaptive** | **不均匀光照** ← 考点! |
| Otsu's | 自动选最优阈值 |

### Morphological Operations 形态学
| 操作 | = | 效果 |
|------|---|------|
| Erosion 腐蚀 | — | 缩小前景 |
| Dilation 膨胀 | — | 扩大前景 |
| **Opening** | E→D | 去小噪点 |
| **Closing** | D→E | 填小孔 |

> **记忆:** "Processing images based on shapes"

---

## 3. Feature Detection 特征检测

### Segmentation → 输出 Binary Image

### Contours: `cv2.findContours()` 找 / `cv2.drawContours()` 画

### Image Gradient: F(x,y) 在 X/Y 方向的变化量

### Algorithm Comparison 算法对比

| | SIFT | SURF | ORB |
|--|------|------|-----|
| 速度 | 慢 | 中 | **最快** |
| 描述符 | **128-D** | 64-D | 32B binary |
| Scale不变 | ✅ | ✅ | ❌ |
| Rotation不变 | ✅ | ✅ | ✅ |
| 免费 | ✅ | ❌ | **✅** |

**SIFT 步骤:** DoG极值 → 关键点定位 → 方向分配 → 128D描述符 → 匹配

**ORB = FAST (keypoint) + BRIEF (descriptor)** ← 必考!

**HOG** = 人体/行人检测 (配合 SVM)

---

## 4. CNN 卷积神经网络

### Architecture 架构
```
Input → [Conv → ReLU → Pooling]×N → Flatten → FC → Softmax → Output
```

### Layers 各层
| 层 | 作用 |
|----|------|
| **Conv** | Kernel 滑动做点积 → Feature Map |
| **ReLU** | f(x)=max(0,x) 非线性激活 |
| **Pooling** | 下采样 (Max/Avg) ← 考点! |
| **FC** | 展平+分类 |
| **Softmax** | 概率分布 (sum=1) |

### Activation Functions 激活函数
| 函数 | 输出范围 | 优势 |
|------|----------|------|
| **ReLU** | [0, ∞) | 减少梯度消失, 最常用 |
| Sigmoid | (0, 1) | 输出概率 |
| Tanh | (-1, 1) | 零中心 |

### ANN → CNN 的原因
- ANN 展平图像 → 丢失空间信息 + 参数爆炸

---

## 5. Deep Learning 深度学习

### Training Steps
Init Weights → Forward Prop → Loss → Backprop → Optimizer

### Overfitting 过拟合 (train acc >> val acc)
**防止方法:** Dropout | L1/L2正则化 | Data Augmentation | Early Stopping | 简化模型

### Underfitting 欠拟合 (都低)
**解决:** 增加复杂度 | 更久训练 | 更好特征

### Optimizers
- **SGD:** 简单有效
- **Adam:** 自适应, 最通用 ← 常考
- **RMSprop:** 自适应学习率

### Loss Functions
- **Cross-Entropy:** 分类
- **MSE:** 回归

### Hardware: CPU(通用) < **GPU(并行, DL首选)** < TPU(专用最快)

### Optimization: **Quantization**(降精度) 通常优于 **Pruning**(剪枝)

---

## 6. Performance Metrics 指标公式

```
Accuracy  = (TP+TN) / (TP+TN+FP+FN)   ← 总体正确率
Precision = TP / (TP+FP)               ← 预测正中真正的
Recall    = TP / (TP+FN)               ← 实际正中被检出的
F1        = 2×P×R / (P+R)              ← P/R调和平均
```

**Confusion Matrix:**
```
              Predicted
              Pos   Neg
Actual Pos  | TP  | FN |
Actual Neg  | FP  | TN |
```

---

## 7. Key Formulas 计算公式

### Feature Map Size 输出尺寸
```
Output = (Input - Kernel + 2×Padding) / Stride + 1
```
**例:** Input=32, K=5, P=0, S=1 → (32-5+0)/1+1 = **28**

### Parameters 参数量
```
Params = (K_h × K_w × C_in + 1) × C_out
```
**例:** 3×3 kernel, 3 channels, 32 filters → (3×3×3+1)×32 = **896**

### Max Pooling
取窗口内最大值, stride=窗口大小
```
4×4 input + 2×2 pool → 2×2 output
```

---

## 8. OpenCV 常用命令

```python
cv2.imread('img.jpg')                    # 读图
cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    # 转灰度
cv2.GaussianBlur(img, (5,5), 0)          # 高斯模糊
cv2.Canny(img, 100, 200)                 # Canny边缘
cv2.threshold(g, 127, 255, THRESH_BINARY)# 阈值
cv2.findContours(bin, RETR_TREE, ...)    # 找轮廓
cv2.drawContours(img, contours, -1, ...) # 画轮廓
orb = cv2.ORB_create()                   # ORB特征
kp, des = orb.detectAndCompute(img, None)# 检测+描述
```

---

## 9. DL vs Traditional CV

| | Traditional CV | Deep Learning |
|--|----------------|---------------|
| 特征 | 手工设计 (SIFT/HOG) | CNN自动学 |
| 数据需求 | 少 | 大量 |
| 透明度 | 高, 可解释 | 黑盒 |
| 计算 | 低 | GPU/TPU |
| 精度 | 简单任务够用 | 复杂任务更高 |

**Hybrid = CV预处理 + DL分类 → 最佳实践**

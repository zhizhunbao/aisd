"""
CST8506 Lab 3: Convolutional Neural Networks
Student Name: Peng Wang
Student Number: 041107730

Implements CNN for MNIST handwritten digit classification using Keras.
Architecture: Input -> Conv2D -> MaxPool -> Conv2D -> MaxPool -> Flatten -> Dense -> Output
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense
from keras.utils import to_categorical

# ============================================================
# 配置
# Configuration
# ============================================================

# 随机种子：学号最后3位 (041107730 -> 730)
# Random seed: last 3 digits of student number (041107730 -> 730)
SEED = 730

# 输出目录
# Output directory
OUTPUT_DIR = 'lab3_images'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 设置随机种子以确保可重复性
# Set random seed for reproducibility
np.random.seed(SEED)
keras.utils.set_random_seed(SEED)

# ============================================================
# 步骤 1：加载数据集
# Step 1: Load Dataset
# ============================================================

print("=" * 60)
print("Step 1: Loading MNIST Dataset")
print("=" * 60)

# 加载 MNIST 数据集（Modified National Institute of Standards and Technology）
# Load MNIST dataset (Modified National Institute of Standards and Technology)
(x_train, y_train), (x_test, y_test) = mnist.load_data()

print(f"Dataset loaded successfully!")

# ============================================================
# 步骤 2：打印训练集和测试集的图像数量
# Step 2: Print Number of Images in Train and Test Set
# ============================================================

print("\n" + "=" * 60)
print("Step 2: Number of Images")
print("=" * 60)

# 打印训练集图像数量
# Print number of training images
print(f"Number of images in train set: {x_train.shape[0]}")

# 打印测试集图像数量
# Print number of test images
print(f"Number of images in test set: {x_test.shape[0]}")

# 打印图像尺寸
# Print image dimensions
print(f"Image shape: {x_train.shape[1]} x {x_train.shape[2]} pixels")

# ============================================================
# 步骤 3：显示前5张训练图像及其对应数字
# Step 3: Display First 5 Training Images with Labels
# ============================================================

print("\n" + "=" * 60)
print("Step 3: First 5 Training Images")
print("=" * 60)

# 创建 1x5 子图布局
# Create 1x5 subplot layout
fig, axes = plt.subplots(1, 5, figsize=(15, 3))

# 遍历前5张图像并显示
# Loop through first 5 images and display
for i in range(5):
    # 显示灰度图像
    # Display grayscale image
    axes[i].imshow(x_train[i], cmap='gray')
    
    # 设置标题为对应的标签
    # Set title to corresponding label
    axes[i].set_title(f"Label: {y_train[i]}")
    
    # 隐藏坐标轴
    # Hide axis
    axes[i].axis('off')

# 设置总标题
# Set overall title
plt.suptitle("First 5 Images in Training Set")
plt.tight_layout()

# 保存图像到输出目录
# Save figure to output directory
plt.savefig(os.path.join(OUTPUT_DIR, 'step3_first_5_images.png'), dpi=150, bbox_inches='tight')
plt.close()

print(f"Saved: {OUTPUT_DIR}/step3_first_5_images.png")

# ============================================================
# 步骤 4：Reshape - 设置通道数（灰度图像 channel=1）
# Step 4: Reshape - Set Channel (Grayscale channel=1)
# ============================================================

print("\n" + "=" * 60)
print("Step 4: Reshape for CNN (add channel dimension)")
print("=" * 60)

# 打印原始形状
# Print original shape
print(f"Original x_train shape: {x_train.shape}")
print(f"Original x_test shape: {x_test.shape}")

# 重塑数据以添加通道维度
# Reshape data to add channel dimension
# 原始形状 (samples, 28, 28) -> 目标形状 (samples, 28, 28, 1)
# Original shape (samples, 28, 28) -> Target shape (samples, 28, 28, 1)
x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)

# 打印重塑后的形状
# Print reshaped shape
print(f"x_train shape after reshape: {x_train.shape}")
print(f"x_test shape after reshape: {x_test.shape}")
print("Channel = 1 (grayscale images)")

# ============================================================
# 步骤 5：归一化图像
# Step 5: Normalize Images
# ============================================================

print("\n" + "=" * 60)
print("Step 5: Normalize Images")
print("=" * 60)

# 打印归一化前的像素值范围
# Print pixel value range before normalization
print(f"Pixel value range before normalization: {x_train.min()} - {x_train.max()}")

# 将像素值从 [0, 255] 归一化到 [0, 1]
# Normalize pixel values from [0, 255] to [0, 1]
# 原因：归一化有助于神经网络更快收敛，避免梯度问题
# Reason: Normalization helps neural network converge faster and avoids gradient issues
x_train = x_train.astype('float32') / 255.0
x_test = x_test.astype('float32') / 255.0

# 打印归一化后的像素值范围
# Print pixel value range after normalization
print(f"Pixel value range after normalization: {x_train.min():.2f} - {x_train.max():.2f}")

# ============================================================
# 步骤 6 & 7：One-Hot 编码 & 打印前5个实例的新旧值
# Step 6 & 7: One-Hot Encoding & Print Old/New Values for First 5 Instances
# ============================================================

print("\n" + "=" * 60)
print("Step 6 & 7: One-Hot Encoding")
print("=" * 60)

# 保存原始标签用于后续对比
# Save original labels for later comparison
y_train_original = y_train.copy()
y_test_original = y_test.copy()

# 应用 One-Hot 编码
# Apply One-Hot Encoding
# 例如：数字 5 -> [0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
# Example: digit 5 -> [0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
y_train = to_categorical(y_train, num_classes=10)
y_test = to_categorical(y_test, num_classes=10)

# 打印前5个实例的旧值和新值对比
# Print old vs new values for first 5 instances
print("First 5 instances - Old vs New values:")
print("-" * 60)
print(f"{'Old Value':<12} {'New Value (One-Hot Encoded)'}")
print("-" * 60)

for i in range(5):
    old_val = y_train_original[i]
    new_val = y_train[i].astype(int)
    print(f"{old_val:<12} {new_val}")

# ============================================================
# 步骤 8：构建 CNN 模型
# Step 8: Build CNN Model
# ============================================================

print("\n" + "=" * 60)
print("Step 8: Build CNN Model")
print("=" * 60)

# ============================================================
# model: 构建序贯CNN模型
#        Build Sequential CNN model
#
# Architecture:
#   Input(28,28,1) -> Conv2D(32) -> MaxPool -> Conv2D(64) -> MaxPool -> Flatten -> Dense(128) -> Dense(10)
# ============================================================
model = Sequential([
    # 输入层 - 明确定义输入形状 (Keras 3.x 最佳实践)
    # Input Layer - explicitly define input shape (Keras 3.x best practice)
    Input(shape=(28, 28, 1)),
    
    # 卷积层 1
    # Conv Layer 1
    # filters=32: 32个卷积核，学习32种不同特征（如边缘、角点等）
    # filters=32: 32 kernels to learn 32 different features (edges, corners, etc.)
    # kernel_size=(3,3): 3x3 卷积核，适合小图像的局部特征提取
    # kernel_size=(3,3): 3x3 filter size, suitable for local feature extraction
    # activation='relu': ReLU激活函数 f(x)=max(0,x)，引入非线性，防止梯度消失
    # activation='relu': ReLU activation f(x)=max(0,x), adds non-linearity, prevents vanishing gradient
    # padding='same': 零填充，保持输出与输入相同的空间尺寸
    # padding='same': Zero padding to keep output same spatial dimensions as input
    Conv2D(filters=32, kernel_size=(3, 3), activation='relu', padding='same'),
    
    # 最大池化层 1
    # Max Pooling Layer 1
    # pool_size=(2,2): 2x2 池化窗口，取窗口内最大值
    # pool_size=(2,2): 2x2 pooling window, takes maximum value in window
    # strides=2: 步长为2，将空间尺寸减半 (28->14)
    # strides=2: Stride of 2, reduces spatial dimensions by half (28->14)
    MaxPooling2D(pool_size=(2, 2), strides=2),
    
    # 卷积层 2
    # Conv Layer 2
    # filters=64: 64个卷积核，捕捉更复杂的特征组合
    # filters=64: 64 kernels to capture more complex feature combinations
    Conv2D(filters=64, kernel_size=(3, 3), activation='relu', padding='same'),
    
    # 最大池化层 2
    # Max Pooling Layer 2
    # 进一步减小空间尺寸 (14->7)
    # Further reduce spatial dimensions (14->7)
    MaxPooling2D(pool_size=(2, 2), strides=2),
    
    # 展平层
    # Flatten Layer
    # 将3D特征图 (7,7,64) 展平为1D向量 (3136)，用于全连接层
    # Flatten 3D feature maps (7,7,64) to 1D vector (3136) for dense layers
    Flatten(),
    
    # 全连接层 1
    # Dense Layer 1 (Fully Connected)
    # units=128: 128个神经元，学习高级特征组合
    # units=128: 128 neurons to learn high-level feature combinations
    Dense(units=128, activation='relu'),
    
    # 输出层
    # Output Layer
    # units=10: 10个输出神经元，对应数字0-9
    # units=10: 10 output neurons corresponding to digits 0-9
    # activation='softmax': Softmax输出概率分布，所有值之和为1
    # activation='softmax': Softmax outputs probability distribution summing to 1
    Dense(units=10, activation='softmax')
])

print("Model Architecture:")
print("-" * 40)
print("Input(28,28,1) -> Conv2D(32) -> MaxPool -> Conv2D(64) -> MaxPool -> Flatten -> Dense(128) -> Dense(10)")

# 打印模型参数说明
# Print model parameters explanation
print("\n" + "-" * 60)
print("Model Parameters Explanation:")
print("-" * 60)
print("""
Layer 1 - Conv2D:
  - filters=32: Number of filters/kernels to learn 32 different features
  - kernel_size=(3,3): 3x3 filter size, common choice for small images
  - activation='relu': ReLU activation, f(x)=max(0,x), prevents vanishing gradient
  - padding='same': Zero padding to keep output size same as input

Layer 2 - MaxPooling2D:
  - pool_size=(2,2): 2x2 pooling window
  - strides=2: Move 2 pixels at a time, reduces dimension by half (28->14)

Layer 3 - Conv2D:
  - filters=64: More filters to capture complex features

Layer 4 - MaxPooling2D:
  - Same as Layer 2, reduces dimension (14->7)

Layer 5 - Flatten:
  - Converts 3D feature maps (7,7,64) to 1D vector (3136)

Layer 6 - Dense:
  - units=128: 128 neurons in hidden layer

Layer 7 - Dense (Output):
  - units=10: 10 classes (digits 0-9)
  - activation='softmax': Outputs probability distribution summing to 1
""")

# ============================================================
# 步骤 9：编译模型
# Step 9: Compile Model
# ============================================================

print("\n" + "=" * 60)
print("Step 9: Compile Model")
print("=" * 60)

# 编译模型，指定优化器、损失函数和评估指标
# Compile model with optimizer, loss function, and metrics
# optimizer='adam': Adam优化器，自适应学习率，结合AdaGrad和RMSprop的优点
# optimizer='adam': Adam optimizer with adaptive learning rate
# loss='categorical_crossentropy': 多分类交叉熵损失，适用于One-Hot编码标签
# loss='categorical_crossentropy': Multi-class cross-entropy loss for one-hot labels
# metrics=['accuracy']: 追踪准确率作为评估指标
# metrics=['accuracy']: Track accuracy as evaluation metric
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print("Model compiled successfully!")
print("Optimizer: Adam (Adaptive Moment Estimation)")
print("Loss Function: Categorical Crossentropy (for multi-class classification)")
print("Metrics: Accuracy")

# ============================================================
# 步骤 10：打印模型摘要
# Step 10: Print Model Summary
# ============================================================

print("\n" + "=" * 60)
print("Step 10: Model Summary")
print("=" * 60)

model.summary()

# ============================================================
# 步骤 11：训练模型
# Step 11: Fit/Train Model
# ============================================================

print("\n" + "=" * 60)
print("Step 11: Training Model")
print("=" * 60)

# 训练模型
# Train the model
# epochs=10: 训练10轮，每轮遍历整个训练集
# epochs=10: Train for 10 epochs, each epoch iterates through entire training set
# batch_size=128: 每批128个样本，平衡内存使用和训练速度
# batch_size=128: 128 samples per batch, balancing memory and training speed
# validation_split=0.1: 10%训练数据用于验证，监控过拟合
# validation_split=0.1: 10% of training data for validation to monitor overfitting
history = model.fit(
    x_train, y_train,
    epochs=10,
    batch_size=128,
    validation_split=0.1,
    verbose=1
)

# 绘制训练历史曲线
# Plot training history curves
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# 准确率曲线
# Accuracy curves
axes[0].plot(history.history['accuracy'], label='Train Accuracy')
axes[0].plot(history.history['val_accuracy'], label='Validation Accuracy')
axes[0].set_title('Model Accuracy')
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Accuracy')
axes[0].legend()

# 损失曲线
# Loss curves
axes[1].plot(history.history['loss'], label='Train Loss')
axes[1].plot(history.history['val_loss'], label='Validation Loss')
axes[1].set_title('Model Loss')
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('Loss')
axes[1].legend()

plt.tight_layout()

# 保存训练历史图
# Save training history plot
plt.savefig(os.path.join(OUTPUT_DIR, 'step11_training_history.png'), dpi=150, bbox_inches='tight')
plt.close()

print(f"Saved: {OUTPUT_DIR}/step11_training_history.png")

# ============================================================
# 步骤 12：预测测试数据
# Step 12: Predict Test Data
# ============================================================

print("\n" + "=" * 60)
print("Step 12: Predict Test Data")
print("=" * 60)

# 对测试集进行预测
# Make predictions on test set
predictions = model.predict(x_test)

print(f"Predictions shape: {predictions.shape}")
print(f"Each prediction is a probability distribution over 10 classes")

# ============================================================
# 步骤 13：打印模型准确率
# Step 13: Print Model Accuracy
# ============================================================

print("\n" + "=" * 60)
print("Step 13: Model Accuracy")
print("=" * 60)

# 评估模型在测试集上的性能
# Evaluate model performance on test set
test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)

print(f"Test Loss: {test_loss:.4f}")
print(f"Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")

# ============================================================
# 步骤 14 & 15：找到最高概率的索引并打印前20个结果
# Step 14 & 15: Find Highest Probability Index and Print First 20 Results
# ============================================================

print("\n" + "=" * 60)
print("Step 14 & 15: First 20 Predictions")
print("=" * 60)

# 找到每行最高概率的索引（即预测的数字）
# Find index of highest probability for each row (predicted digit)
predicted_digits = np.argmax(predictions, axis=1)

# 获取每行的最高概率值
# Get highest probability value for each row
highest_probs = np.max(predictions, axis=1)

# 打印前20个预测结果
# Print first 20 prediction results
print(f"{'Highest Probability':<25} {'Predicted Digit':<18} {'Actual Digit'}")
print("-" * 60)

for i in range(20):
    prob = highest_probs[i]
    pred = predicted_digits[i]
    actual = y_test_original[i]
    match = "✓" if pred == actual else "✗"
    print(f"[{prob:.7f}]              {pred:<18} {actual} {match}")

# ============================================================
# 步骤 16：打印所有误分类实例
# Step 16: Print All Misclassified Instances
# ============================================================

print("\n" + "=" * 60)
print("Step 16: All Misclassified Instances")
print("=" * 60)

# 找出所有误分类的索引
# Find all misclassified indices
misclassified_indices = np.where(predicted_digits != y_test_original)[0]

# 打印误分类统计
# Print misclassification statistics
print(f"Total misclassified: {len(misclassified_indices)} out of {len(y_test_original)}")
print(f"Misclassification rate: {len(misclassified_indices)/len(y_test_original)*100:.2f}%")
print()

# 打印所有误分类实例的详细信息
# Print details of all misclassified instances
print(f"{'Highest Probability':<25} {'Predicted Digit':<18} {'Actual Digit'}")
print("-" * 60)

for idx in misclassified_indices:
    prob = highest_probs[idx]
    pred = predicted_digits[idx]
    actual = y_test_original[idx]
    print(f"[{prob:.7f}]              {pred:<18} {actual}")

# ============================================================
# 额外：可视化误分类的图像
# Bonus: Visualize Misclassified Images
# ============================================================

print("\n" + "=" * 60)
print("Bonus: Visualizing Some Misclassified Images")
print("=" * 60)

# 显示前10个误分类的图像
# Display first 10 misclassified images
num_to_show = min(10, len(misclassified_indices))

if num_to_show > 0:
    fig, axes = plt.subplots(2, 5, figsize=(15, 6))
    axes = axes.flatten()
    
    for i in range(num_to_show):
        idx = misclassified_indices[i]
        
        # 显示图像
        # Display image
        axes[i].imshow(x_test[idx].reshape(28, 28), cmap='gray')
        
        # 设置标题：预测值、实际值、概率
        # Set title: predicted, actual, probability
        axes[i].set_title(f"Pred: {predicted_digits[idx]}, Actual: {y_test_original[idx]}\nProb: {highest_probs[idx]:.4f}")
        axes[i].axis('off')
    
    # 隐藏多余的子图
    # Hide extra subplots
    for i in range(num_to_show, 10):
        axes[i].axis('off')
    
    plt.suptitle("Misclassified Images")
    plt.tight_layout()
    
    # 保存误分类图像
    # Save misclassified images plot
    plt.savefig(os.path.join(OUTPUT_DIR, 'step16_misclassified_images.png'), dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"Saved: {OUTPUT_DIR}/step16_misclassified_images.png")

print("\n" + "=" * 60)
print("Lab 3 Completed!")
print("=" * 60)

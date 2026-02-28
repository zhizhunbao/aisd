# Week 2: 图像处理基础 (Fundamentals of Image Processing)

> Source: `Week 2 - Fundamentals of Image Processing1.pptx`
> Total slides: 24
> Instructor: Stephin Rachel Thomas | 22-01-2026

---

## 1. 今日主题 (Today's Topics)

![Page 1](week2_image_processing_slides_pages/page_001.png)

![Page 2](week2_image_processing_slides_pages/page_002.png)

- Introduction to Image Processing — 图像处理简介
- Importance in Machine Vision — 在机器视觉中的重要性
- Steps involved in Image Processing — 图像处理的步骤
- Image Filtering (Blurring, Sharpening) — 图像滤波（模糊、锐化）
- Edge Detection using Canny — 使用Canny进行边缘检测
- Image Histograms — 图像直方图
- Image Thresholding — 图像阈值化
- Morphological Operations — 形态学操作
- Image Transformation Techniques — 图像变换技术

---

## 2. 图像处理简介 (Introduction to Image Processing)

### 2.1 图像处理定义 (Image Processing Definition)

![Page 3](week2_image_processing_slides_pages/page_003.png)

- **Image Processing** is the building block of Machine Vision — **图像处理**是机器视觉的构建基石
- It involves **manipulation** and **analysis of images** — 它涉及图像的**操作**和**分析**
- It **enhances** quality of image and **extract** meaningful information — 它**增强**图像质量并**提取**有意义的信息

### 2.2 图像处理的重要性 (Importance in Machine Vision)

![Page 4](week2_image_processing_slides_pages/page_004.png)

1. **Enhancement**: Improves image quality by **reducing noise, enhancing contrast, and sharpening details**, making it easier to analyze — **增强**：通过**降噪、增强对比度和锐化细节**来改善图像质量，使其更易于分析
2. **Feature Extraction**: Identifies and extracts important features like **edges, corners, and textures**, which are crucial for recognizing objects and patterns — **特征提取**：识别和提取重要特征，如**边缘、角点和纹理**，这对识别对象和模式至关重要
3. **Segmentation**: Divides an image into **meaningful regions** or objects, facilitating object detection and classification — **分割**：将图像划分为**有意义的区域**或对象，促进目标检测和分类
4. **Object Recognition**: Helps in identifying and classifying objects within an image, which is essential for applications like automated inspection and robotics — **目标识别**：帮助识别和分类图像中的对象，这对自动化检测和机器人等应用至关重要
5. **Measurement**: Allows for precise measurement of object dimensions, distances, and other parameters, which is vital in quality control and industrial automation — **测量**：允许精确测量对象尺寸、距离和其他参数，这对质量控制和工业自动化至关重要

---

## 3. 图像处理的关键阶段 (Key Stages in Image Processing)

### 3.1 九阶段概览 (Nine Stages Overview)

![Page 5](week2_image_processing_slides_pages/page_005.png)

### 3.2 阶段详解第1部分 (Stages Detail — Part 1)

![Page 6](week2_image_processing_slides_pages/page_006.png)

**Stages detail slide (part 1):** Detailed descriptions of Acquisition, Enhancement, Restoration, and Morphological processing.

**阶段详解页（第1部分）：** 采集、增强、复原和形态学处理的详细描述。

### 3.3 阶段详解第2部分 (Stages Detail — Part 2)

![Page 7](week2_image_processing_slides_pages/page_007.png)

**Nine Key Stages:**

1. **Acquisition** — Capturing image using digital camera or sensors — **采集** — 使用数码相机或传感器获取图像
2. **Enhancement** — Manipulates image to be more suitable for specific application; brings out hidden details — **增强** — 使图像更适合特定应用；显现隐藏细节
3. **Restoration** — Improving appearance (e.g., noise removal); uses mathematical models of degradation — **复原** — 改善外观（如去噪）；使用退化的数学模型
4. **Morphological processing** — Tools for extracting image components useful for shape description (e.g., fingerprint) — **形态学处理** — 提取对形状描述有用的图像组件的工具（如指纹）
5. **Segmentation** — Partitions image into constituent parts or objects (one of the most difficult tasks) — **分割** — 将图像划分为组成部分或对象（最困难的任务之一）
6. **Object Recognition** — Assigns a label to an object based on its description — **目标识别** — 根据描述为对象分配标签
7. **Representation & Description** — Transforms raw data into a form suitable for processing (boundary or region) — **表示与描述** — 将原始数据转换为适合处理的形式（边界或区域）
8. **Image Compression** — Reducing storage required to save an image — **图像压缩** — 减少保存图像所需的存储空间
9. **Color Image Processing** — Using color information to extract meaningful data — **彩色图像处理** — 利用颜色信息提取有意义的数据

- Not all steps are required for every task — based on application, a combination of 2-3 steps may suffice — 并非每个任务都需要所有步骤 — 根据应用，2-3步的组合可能就足够了

---

## 4. 图像滤波 (Image Filtering)

![Page 8](week2_image_processing_slides_pages/page_008.png)

- Filtering in image processing is a technique used to manipulate or enhance an image by **altering its pixels**. It's a fundamental tool that can either **amplify certain features** or **suppress unwanted distortions** — 图像处理中的滤波是一种通过**改变像素**来操作或增强图像的技术。它是一种基本工具，可以**放大某些特征**或**抑制不需要的失真**
- Filters act like a **sieve** through which the original image is passed: they can highlight specific attributes, remove noise, or prepare the image for further analysis — 滤波器像**筛子**一样，原始图像通过它：可以突出特定属性、去除噪声、或为进一步分析做准备

---

## 5. 图像模糊 (Image Blurring)

![Page 9](week2_image_processing_slides_pages/page_009.png)

- Blurring is a type of filtering that **softens** an image. It's used to **reduce detail and noise** — 模糊是一种**柔化**图像的滤波方式。用于**减少细节和噪声**
- Blurring works by averaging the pixels around a target pixel, which smooths out rapid intensity changes — 模糊通过对目标像素周围的像素取平均值来工作，平滑急剧的强度变化
- The filter used here is: `[[1,1,1],[1,1,1],[1,1,1]]` — 这里使用的滤波核是：`[[1,1,1],[1,1,1],[1,1,1]]`

---

## 6. 图像锐化 (Image Sharpening)

![Page 10](week2_image_processing_slides_pages/page_010.png)

- Sharpening, in contrast to blurring, is a filter that **enhances the edges** and **details** in an image, making it appear clearer and more defined — 锐化与模糊相反，是一种**增强图像边缘**和**细节**的滤波器，使图像看起来更清晰、更精确
- It increases the contrast between adjacent pixels to **highlight boundaries of objects** within the image — 它增加相邻像素之间的对比度，以**突出图像内对象的边界**
- This technique is vital when **details are critical** for analysis, such as in **medical imaging or precision manufacturing** — 当**细节对分析至关重要**时，这种技术至关重要，例如在**医学影像或精密制造**中

---

## 7. 基本图像操作 (Basic Image Manipulations)

![Page 11](week2_image_processing_slides_pages/page_011.png)

- Let's explore basic manipulations like resizing, cropping, and rotating images. These are the bread and butter of image processing – simple yet powerful tools in our visual toolkit — 让我们探索调整大小、裁剪和旋转图像等基本操作。这些是图像处理的基本功 – 简单却强大的视觉工具

---

## 8. Canny边缘检测 (Edge Detection using Canny)

### 8.1 降噪与梯度计算 (Noise Reduction and Gradient Calculation)

![Page 12](week2_image_processing_slides_pages/page_012.png)

**Canny edge detection slide (part 1):** Title "Edge Detection using Canny". Left: introduces the Canny filter as a "sophisticated edge detection algorithm" with high precision. Lists the first 2 stages: Noise Reduction (Gaussian filter) and Gradient Calculation (Sobel kernel in horizontal + vertical directions). Right: side-by-side comparison — original grayscale cameraman image (left) and its extracted white edges on black background (right), captioned "Figure 1: The cameraman image and its edges extracted".

**Canny边缘检测页（第1部分）：** 标题"Edge Detection using Canny"。左侧：介绍Canny滤波器为"精密边缘检测算法"，精度高。列出前2阶段：噪声降低（高斯滤波器）和梯度计算（水平+垂直方向Sobel核）。右侧：并排对比 — 原始灰度摄影师图像（左）与提取的白色边缘黑色背景图（右），标注"Figure 1: The cameraman image and its edges extracted"。

- The Canny filter is a **sophisticated edge detection** algorithm that is known for its precision in detecting a wide range of edges in images — Canny滤波器是一种**精密边缘检测**算法，以其在检测图像中各种边缘的精确度而闻名
- It involves multiple stages: — 它涉及多个阶段：
  1. **Noise Reduction** - By smoothing the image with a Gaussian filter — **降噪** - 用高斯滤波器平滑图像
  2. **Gradient Calculation** - Finding intensity gradients and its direction at each pixel — **梯度计算** - 找到每个像素的强度梯度及其方向
- Smoothened image is then filtered with a **Sobel kernel** in both horizontal and vertical direction to get first derivative in horizontal direction and vertical direction — 平滑后的图像用**Sobel核**在水平和垂直方向上滤波，得到水平方向和垂直方向的一阶导数

### 8.2 NMS、双阈值与滞后跟踪 (NMS, Double Thresholding and Hysteresis)

![Page 13](week2_image_processing_slides_pages/page_013.png)

**Canny edge detection slide (part 2):** Covers the remaining 3 stages: Non-maximum Suppression (suppressing non-maximum gradient values), Double Thresholding (classifying into strong, weak, non-edges), and Edge Tracking by Hysteresis (connecting weak edges to strong edges). Right: NMS diagram — two cross-shaped diagrams showing 3 points (C, A, B) along the gradient direction, with point A on the edge. Left diagram shows the points on the edge itself (green region); right diagram shows the points on the image plane. Arrows indicate gradient direction perpendicular to the edge.

**Canny边缘检测页（第2部分）：** 覆盖剩余3阶段：非极大值抑制（抑制非最大梯度值）、双阈值（分为强、弱、非边缘）和滞后边缘跟踪（将弱边缘连接到强边缘）。右侧：NMS示意图 — 两个十字形图展示沿梯度方向的3个点（C、A、B），A点在边缘上。左图显示这些点在边缘（绿色区域）上的位置；右图显示在图像平面上的位置。箭头指示垂直于边缘的梯度方向。

- **Non-maximum Suppression** – Thins out edges by suppressing non-maximum gradient values — **非极大值抑制** – 通过抑制非最大梯度值来细化边缘
- **Double Thresholding** – Algorithm applies 2 thresholds (high and low) to classify edges into strong, weak and non-edges — **双阈值** – 算法应用2个阈值（高和低）将边缘分为强边缘、弱边缘和非边缘
- **Edge Tracking by Hysteresis**- the algorithm tracks edges by connecting weak edges to strong edges, helps to preserve true edges while discarding isolated weak edges caused by noise — **滞后边缘跟踪** - 算法通过将弱边缘连接到强边缘来跟踪边缘，有助于保留真实边缘同时丢弃由噪声引起的孤立弱边缘
- Ref: https://docs.opencv.org/5.x/da/d22/tutorial_py_canny.html

---

## 9. 图像直方图 (Image Histograms)

### 9.1 直方图定义 (Histogram Definition)

![Page 14](week2_image_processing_slides_pages/page_014.png)

- An image histogram is a chart that shows how many pixels in an image have a particular brightness level. The horizontal axis shows **different brightness levels**, from **dark to light**, and the vertical axis shows **how many pixels are at each level**. It helps us understand if an image is mostly bright, dark, or balanced, and is useful for improving the image's look. — 图像直方图是一个图表，显示图像中有多少像素具有特定亮度级别。水平轴显示**不同的亮度级别**，从**暗到亮**，垂直轴显示**每个级别有多少像素**。它帮助我们了解图像是主要明亮、暗还是均衡的，对改善图像外观有用。

### 9.2 直方图结构 (Histogram Structure)

![Page 15](week2_image_processing_slides_pages/page_015.png)

- Histogram is a graph or plot, which gives you an overall idea about **the intensity distribution of an image**. — 直方图是一种图形或图表，给你关于**图像强度分布**的整体概念。
- It is a plot with pixel values (ranging from **0 to 255**) in X-axis and corresponding number of pixels in the image on Y-axis. — 它是一个X轴为像素值（范围从**0到255**），Y轴为图像中对应像素数量的图表。
- **Left** region of histogram shows the amount of **darker** pixels in image and **right** region shows the amount of **brighter** pixels. — 直方图的**左侧**区域显示图像中**较暗**像素的数量，**右侧**区域显示**较亮**像素的数量。

### 9.3 直方图与分箱 (Histogram and Bins)

![Page 16](week2_image_processing_slides_pages/page_016.png)

- We can segment our range in subparts (called **bins**) — 我们可以将范围分成子部分（称为**bins**）
- [0, 255] = [0, 15] ∪ [16, 31] ∪ ... ∪ [240, 255] — 将0-255的完整范围拆分为16个等宽子区间
- range = bin₁ ∪ bin₂ ∪ ... ∪ bin\_{n=15} — 范围 = 各bin的并集
- Ref: https://docs.opencv.org/5.x/d8/dbc/tutorial_histogram_calculation.html

---

## 10. 图像阈值化 (Image Thresholding)

### 10.1 阈值化简介 (Thresholding Introduction)

![Page 17](week2_image_processing_slides_pages/page_017.png)

- Thresholding is a simple yet effective way to **segment images**. — 阈值化是一种简单而有效的**图像分割**方法。
- By converting an image to black and white based on a threshold value, we can **isolate objects or features easily**. — 通过基于阈值将图像转换为黑白，我们可以轻松地**隔离对象或特征**。

### 10.2 简单阈值与自适应阈值 (Simple vs Adaptive Thresholding)

![Page 18](week2_image_processing_slides_pages/page_018.png)

- **Simple Thresholding**: For every pixel, the **same threshold value** is applied. If the pixel value is smaller than or equal to the threshold, it is set to 0, otherwise it is set to a maximum value. — **简单阈值**：对每个像素应用**相同的阈值**。如果像素值小于或等于阈值，设为0，否则设为最大值。
- **Adaptive Thresholding**: The algorithm determines the threshold for a pixel based on **a small region around it**. So we get different thresholds for different regions of the same image which gives better results for images with varying illumination. — **自适应阈值**：算法基于像素周围的**一个小区域**确定阈值。因此对同一图像的不同区域得到不同的阈值，对光照变化的图像效果更好。

---

## 11. 形态学操作 (Morphological Operations)

### 11.1 腐蚀 (Erosion)

![Page 19](week2_image_processing_slides_pages/page_019.png)

- Morphology is a broad set of image processing operations that process images based on **shapes**. — 形态学是一组广泛的图像处理操作，基于**形状**处理图像。
- **Erosion**: Shrinks objects. — **腐蚀**：缩小对象。
- The kernel slides through the image (as in 2D convolution). A pixel in the original image (either 1 or 0) will be considered 1 **only if all the pixels under the kernel is 1,** otherwise it is eroded (made to zero). — 核在图像上滑动（如2D卷积）。原始图像中的像素（1或0）只有在**核下所有像素都为1**时才被认为是1，否则被腐蚀（变为零）。
- All the pixels near boundary will be discarded depending upon the size of kernel. So the **thickness** or size of the foreground object **decreases** or simply white region decreases in the image. — 所有靠近边界的像素将根据核的大小被丢弃。因此前景对象的**粗细**或大小**减小**，或者简单说图像中的白色区域减小。
- It is useful for **removing small white noises, detach two connected objects** etc. — 对**去除小白噪声、分离两个连通对象**等有用。

### 11.2 膨胀 (Dilation)

![Page 20](week2_image_processing_slides_pages/page_020.png)

- **Dilation**: Expands objects. — **膨胀**：扩展对象。
- A pixel element is '1' if at least one pixel under the kernel is '1'. So it increases the white region in the image or size of foreground object increases. — 如果核下至少有一个像素为'1'，则像素元素为'1'。因此它增加图像中的白色区域或前景对象的大小增加。
- Normally, in cases like **noise removal**, erosion is followed by dilation. — 通常，在**噪声去除**等情况下，腐蚀后跟着膨胀。
- It is also useful in joining broken parts of an object. — 它在连接对象的断裂部分也很有用。

### 11.3 开运算与闭运算 (Opening and Closing)

![Page 21](week2_image_processing_slides_pages/page_021.png)

- **Opening**: Removes small objects (**erosion followed by dilation**). — **开运算**：去除小对象（**腐蚀后膨胀**）。
- Erosion **removes white noises**, but it also shrinks our object. Then we dilate it. Since noise is gone, they won't come back, but our object area increases. It is also useful in joining broken parts of an object. — 腐蚀**去除白噪声**，但也会缩小对象。然后我们膨胀它。由于噪声已消失，它们不会回来，但对象面积增大。它在连接对象断裂部分也有用。
- **Closing**: Fills small holes (**dilation followed by erosion**). — **闭运算**：填充小孔（**膨胀后腐蚀**）。
- It is useful in **closing small holes** (filling the gap) inside the foreground objects, or small black points on the object. — 对前景对象内的**填充小孔**（填补间隙）或对象上的小黑点有用。
- Application: Medical Imaging, Robotics, Computer Vision, Document processing — 应用：医学影像、机器人、计算机视觉、文档处理

---

## 12. 图像变换技术 (Image Transformation Techniques)

### 12.1 仿射变换公式 (Affine Transformation Formula)

![Page 22](week2_image_processing_slides_pages/page_022.png)

- Image transformation techniques are **essential tools** in digital image processing, allowing for various modifications and enhancements to image. — 图像变换技术是数字图像处理中的**基本工具**，允许对图像进行各种修改和增强。
- **Affine transformation** – Preserve lines and parallelism in the image. — **仿射变换** – 保持图像中的直线和平行性。
- y = Ax + b
  - _x_: The input vector (e.g., a point in 2D or 3D space). — _x_：输入向量（如2D或3D空间中的点）。
  - A: A matrix that applies a linear transformation (like rotation, scaling, or shearing). — A：应用线性变换的矩阵（如旋转、缩放或剪切）。
  - b: A vector that applies a translation (shifts the result). — b：应用平移的向量（移动结果）。
  - y: The output vector after the transformation. — y：变换后的输出向量。

### 12.2 变换类型 (Transformation Types)

![Page 23](week2_image_processing_slides_pages/page_023.png)

- **Translation**: Shifting the image in the x or y direction. — **平移**：在x或y方向上移动图像。
- **Rotation**: Rotating the image around a specified point. — **旋转**：围绕指定点旋转图像。
- **Scaling**: Changing the size of the image. — **缩放**：改变图像的大小。
- **Shearing**: Slanting the image along the x or y axis. — **剪切**：沿x或y轴倾斜图像。

---

## 13. 下周预告 (Next Week Preview)

![Page 24](week2_image_processing_slides_pages/page_024.png)

- Next week: **Feature Detection and Description** — 下周：**特征检测与描述**

---

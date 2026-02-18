# Week 1: 机器视觉导论 (Introduction to Machine Vision)

> Source: `Week 1 - Introduction to Machine Vision1.pptx`
> Total slides: 17
> Instructor: Stephin Rachel Thomas | 15-01-2026

---

## 1. 课程信息 (General Information)

- Course Brightspace page: https://brightspace.algonquincollege.com/d2l/le/content/846092/Home
- Read the course outline and course section information (CSI)
- Labs assess your understanding of implementation and demo your work each session
- Professional behaviour expected; assignments done individually
- Any use of online materials, including ChatGPT and LLMs, stated clearly as references

> **📝 Notes / 笔记:**
>
> **📌 What / 是什么:** Course policies and academic integrity rules. 课程政策和学术诚信规则。
>
> **🎯 Why / 为什么:**
> Why emphasize individual work with references? Because MV is hands-on — if you can't explain your code during a live demo, you haven't learned anything. The reference rule isn't about banning AI, it's about ensuring you understand what you submit.
> 为什么强调独立完成并标注引用？因为 MV 是动手课 — 如果你在现场演示时无法解释代码，说明什么都没学到。引用规则不是禁止 AI，而是确保你理解你提交的内容。
>
> **💡 Intuition / 直觉:** —
>
> **⚙️ How / 怎么算:** —
>
> **⚖️ Compare / 对比:** —
>
> **⚠️ Pitfall / 易错点:**
> Using AI tools is allowed, but NOT declaring it = academic dishonesty. Always add a reference line.
> 使用 AI 工具是允许的，但不声明 = 学术不诚实。务必添加引用说明。
>
> **📝 Exam / 考法:**
> Labs require live demos — be ready to explain your code, not just show output.
> 实验课要求现场演示 — 准备好解释代码逻辑，不只是展示输出结果。

---

## 2. 什么是机器视觉 (What is Machine Vision)

Machine vision is a technology that enables machines to interpret and understand visual information from the surrounding environment. It involves:

- Capturing images or videos using cameras or sensors
- Processing these images to extract useful information
- Using this information to make decisions or perform specific tasks

![Picture 3](week1_intro_machine_vision_slides_images/slide04_img1.jpg)

> **📝 Notes / 笔记:**
>
> **📌 What / 是什么:**
> A three-step pipeline: Capture → Process → Decide.
> 三步流水线：采集 → 处理 → 决策。
>
> **🎯 Why / 为什么:**
> Why do machines need "vision"? Because most industrial tasks require spatial understanding — measuring, inspecting, sorting — that humans do with eyes. Replacing human visual inspection enables 24/7 operation, higher consistency, and handling dangerous environments.
> 为什么机器需要"视觉"？因为大多数工业任务需要空间理解 — 测量、检测、分类 — 人类用眼睛完成的事。用机器代替人类视觉检测，可以 24/7 运行、更高一致性、处理危险环境。
>
> **💡 Intuition / 直觉:**
> Think of it as: **Eyes → Brain → Hands**. Cameras = eyes (capture), algorithms = brain (process), actuators = hands (act on decisions). The entire course focuses on building the "brain" part.
> 想象成：**眼睛 → 大脑 → 手**。摄像头=眼睛（采集），算法=大脑（处理），执行器=手（执行决策）。本课程专注于构建"大脑"部分。
>
> **⚙️ How / 怎么算:** —
>
> **⚖️ Compare / 对比:**
> Machine Vision vs Computer Vision: Often used interchangeably, but MV traditionally refers to industrial applications (factory inspection), while CV is the broader academic field. This course covers both.
> 机器视觉 vs 计算机视觉：经常互换使用，但 MV 传统上指工业应用（工厂检测），CV 是更广泛的学术领域。本课程两者都涉及。
>
> **⚠️ Pitfall / 易错点:**
> Don't think of MV as "just cameras." The camera only captures — the real value is in the processing and decision-making algorithms.
> 不要把 MV 理解为"只是摄像头"。摄像头只负责采集 — 真正的价值在于处理和决策算法。
>
> **📝 Exam / 考法:**
> "List and explain the three steps of a machine vision system." Know the pipeline cold.
> "列出并解释机器视觉系统的三个步骤。" 必须熟练掌握这个流水线。

---

## 3. 历史与发展 (History and Evolution)

Key milestones: digital cameras → neural networks → computing power increase.

**Significant turning point:** The rise of deep learning techniques.

![Picture 2](week1_intro_machine_vision_slides_images/slide05_img1.gif)

> **📝 Notes / 笔记:**
>
> **📌 What / 是什么:** Evolution from simple image capture to AI-powered vision systems. 从简单图像采集到 AI 驱动的视觉系统的演进。
>
> **🎯 Why / 为什么:**
> Why was deep learning THE turning point? Before DL, engineers manually designed feature extractors for each task (hand-crafted edges, colors, shapes). Every new problem needed new engineering. Deep learning changed this — CNNs automatically learn relevant features from data, making systems generalizable.
> 为什么深度学习是转折点？DL 之前，工程师为每个任务手动设计特征提取器（手工设计的边缘、颜色、形状）。每个新问题都需要新的工程工作。深度学习改变了这一切 — CNN 从数据中自动学习相关特征，使系统具有泛化能力。
>
> **💡 Intuition / 直觉:**
> Traditional CV = giving a child a rulebook ("look for round shapes, red color"). Deep Learning CV = showing a child 10,000 pictures of apples and letting them figure out what an apple looks like.
> 传统 CV = 给小孩一本规则书（"找圆形、红色"）。深度学习 CV = 给小孩看 10,000 张苹果图片，让他们自己总结苹果长什么样。
>
> **⚙️ How / 怎么算:** —
>
> **⚖️ Compare / 对比:**
> Traditional CV vs Deep Learning CV:
>
> - Traditional: Human designs features → fragile, task-specific
> - DL: Algorithm learns features from data → robust, generalizable
>   This is the most fundamental paradigm shift in the field.
>   传统 CV vs 深度学习 CV：
> - 传统：人设计特征 → 脆弱、特定于任务
> - DL：算法从数据学特征 → 鲁棒、可泛化
>
> **⚠️ Pitfall / 易错点:**
> DL didn't make traditional image processing obsolete. You still need preprocessing (Week 2) before feeding images to a CNN.
> DL 并没有让传统图像处理过时。在将图像输入 CNN 之前，仍然需要预处理（第2周内容）。
>
> **📝 Exam / 考法:**
> "What was the significant turning point in machine vision?" = Rise of deep learning.
> "机器视觉的重要转折点是什么？" = 深度学习的兴起。

---

## 4. 关键技术 (Key Technologies)

- **Image sensors:** CCD and CMOS
- **Image processing techniques:** filtering and edge detection
- **Machine Learning:** particularly deep learning

![Picture 10](week1_intro_machine_vision_slides_images/slide06_img1.jpg)

> **📝 Notes / 笔记:**
>
> **📌 What / 是什么:** Three technology layers: sensors → processing → ML. 三层技术：传感器 → 处理 → 机器学习。
>
> **🎯 Why / 为什么:**
> Why three separate layers? Because each solves a different problem: sensors convert light to numbers, processing cleans those numbers, ML interprets them. Weakness in any layer cripples the whole system — garbage in = garbage out.
> 为什么分三层？因为每层解决不同问题：传感器将光转为数字，处理清洗数字，ML 解读数字。任何一层的弱点都会拖垮整个系统 — 垃圾进 = 垃圾出。
>
> **💡 Intuition / 直觉:**
> Like a photography studio: Camera (sensor) → Photoshop (processing) → Art critic (ML).
> 像摄影工作室：相机（传感器）→ PS修图（处理）→ 艺术评论家（ML）。
>
> **⚙️ How / 怎么算:** —
>
> **⚖️ Compare / 对比:**
> CCD vs CMOS: CCD = higher quality, more expensive → scientific/medical. CMOS = cheaper, faster, lower power → phones, webcams. Today CMOS dominates as quality gap has closed.
> CCD vs CMOS：CCD = 质量更高、更贵 → 科学/医学。CMOS = 更便宜、更快、功耗低 → 手机、网络摄像头。如今 CMOS 占主导，因为质量差距已缩小。
>
> **⚠️ Pitfall / 易错点:**
> Students often skip image processing and jump to ML. But no amount of ML can fix a badly captured, noisy image. Preprocessing is essential.
> 学生经常跳过图像处理直接进入 ML。但再强的 ML 也无法修复采集不好的、有噪声的图像。预处理是必不可少的。
>
> **📝 Exam / 考法:**
> "Name the three key technologies in Machine Vision." Sensors, image processing, machine learning.
> "列出机器视觉的三项关键技术。" 传感器、图像处理、机器学习。

---

## 5. 应用领域 (Applications)

**Everyday:** Retail (barcode), Manufacturing (quality), Entertainment (VFX), Autonomous vehicles (lane keeping)
**Advanced:** Autonomous navigation, Medical imaging diagnostics, Facial recognition

![Picture 2](week1_intro_machine_vision_slides_images/slide07_img1.jpg)

> **📝 Notes / 笔记:**
>
> **📌 What / 是什么:** MV applications spanning daily life to cutting-edge fields. MV 应用跨越日常生活到前沿领域。
>
> **🎯 Why / 为什么:**
> These aren't just "fun facts." Each maps to techniques you'll learn:
> Barcode scanning → thresholding + contours (W2-3). Quality inspection → feature detection + CNN (W3-4). Autonomous driving → object detection + DL (W4-5).
> 这些不是"趣闻"。每个对应你将学的技术：条码扫描→阈值+轮廓(W2-3)。质检→特征检测+CNN(W3-4)。自动驾驶→目标检测+DL(W4-5)。
>
> **💡 Intuition / 直觉:** —
>
> **⚙️ How / 怎么算:** —
>
> **⚖️ Compare / 对比:** —
>
> **⚠️ Pitfall / 易错点:**
> MV in autonomous vehicles is NOT just "detecting objects." It includes lane keeping (edge detection), blind spot checking (depth estimation), adaptive cruise (distance measurement) — multiple subsystems working together.
> 自动驾驶中的 MV 不只是"检测物体"。它包括车道保持（边缘检测）、盲区检查（深度估计）、自适应巡航（距离测量）— 多个子系统协同工作。
>
> **📝 Exam / 考法:**
> "Give 3 real-world applications of Machine Vision and the techniques involved."
> "举出3个机器视觉的实际应用及涉及的技术。"

---

## 6. 系统工作流程 (Basic Workflow)

1. **Image Acquisition** — Capturing the image
2. **Image Processing** — Analyzing and manipulating the image
3. **Interpretation/Action** — Making decisions based on the processed image

> **📝 Notes / 笔记:**
>
> **📌 What / 是什么:** The universal 3-step pipeline for any MV system. 任何 MV 系统的通用三步流水线。
>
> **🎯 Why / 为什么:**
> Why is this pipeline important? Because it gives you a mental framework for every MV problem: "What am I capturing? How do I clean/enhance it? What decision do I make?" Every lab you do follows this structure.
> 为什么这个流水线重要？因为它为每个 MV 问题提供思维框架："我在采集什么？如何清洗/增强？做什么决策？" 你做的每个实验都遵循这个结构。
>
> **💡 Intuition / 直觉:**
> Manufacturing example: Camera photographs each product on conveyor → Algorithm checks for scratches/dents → If defect found, robotic arm removes it. Each step is clear and testable.
> 制造业例子：摄像头拍传送带上的产品→算法检查划痕/凹痕→发现缺陷则机械臂移除。每步清晰可测试。
>
> **⚙️ How / 怎么算:** —
>
> **⚖️ Compare / 对比:** —
>
> **⚠️ Pitfall / 易错点:**
> These aren't independent steps — they form a feedback loop. Poor acquisition (bad lighting, wrong angle) makes processing impossible, no matter how good your algorithm. Always fix the capture first.
> 这些不是独立步骤 — 它们形成反馈回路。采集不好（光照差、角度错），无论算法多好都处理不了。永远先解决采集问题。
>
> **📝 Exam / 考法:**
> "Describe the basic workflow of a machine vision system with an example." Use the manufacturing inspection example.
> "用例子描述机器视觉系统的基本工作流程。" 用制造业检测例子。

---

## 7. 图像处理入门与像素 (Image Processing & Pixels)

- Image Formats: JPEG, PNG, RAW
- Color Spaces: RGB and HSV
- **Pixel**: numerical representation at (x,y). Grayscale = single value (0-255). Color = (R,G,B) tuple.

![Picture 2](week1_intro_machine_vision_slides_images/slide11_img1.jpg)
![Picture 4](week1_intro_machine_vision_slides_images/slide11_img2.png)

> **📝 Notes / 笔记:**
>
> **📌 What / 是什么:**
> A pixel is just a number (grayscale) or three numbers (color) at a grid position. An image is a spreadsheet of numbers.
> 像素就是在网格位置上的一个数字（灰度）或三个数字（彩色）。图像就是一个数字表格。
>
> **🎯 Why / 为什么:**
> Why start with pixels? Because every operation in this course — filtering, edge detection, CNN — is a mathematical operation on pixel values. If you don't understand that images are just numbers, nothing else makes sense.
> 为什么从像素开始？因为本课程的每个操作 — 滤波、边缘检测、CNN — 都是对像素值的数学运算。如果不理解图像就是数字，后面都无法理解。
>
> **💡 Intuition / 直觉:**
> Grayscale image = Excel spreadsheet with numbers 0-255. Image processing = applying formulas to cells. Color image = three stacked spreadsheets (R, G, B channels).
> 灰度图 = Excel表格，数字0-255。图像处理 = 对单元格套公式。彩色图 = 三个叠在一起的表格（R,G,B通道）。
>
> **⚙️ How / 怎么算:** —
>
> **⚖️ Compare / 对比:**
> RGB vs HSV: RGB = how screens display color (hardware). HSV = how humans perceive color (intuition). H=hue makes color filtering trivial — "find red objects" = filter H channel. OpenCV converts to HSV for color detection.
> RGB vs HSV：RGB = 屏幕显示颜色的方式（硬件）。HSV = 人类感知颜色的方式（直觉）。H=色相使颜色过滤很简单 — "找红色物体" = 过滤 H 通道。OpenCV 用 HSV 做颜色检测。
>
> **⚠️ Pitfall / 易错点:**
> OpenCV uses BGR, not RGB! If you load with `cv2.imread()` and display with matplotlib, colors look wrong. Convert with `cv2.cvtColor(img, cv2.COLOR_BGR2RGB)`.
> OpenCV 使用 BGR 而不是 RGB！如果用 `cv2.imread()` 加载再用 matplotlib 显示，颜色会不对。需要 `cv2.cvtColor(img, cv2.COLOR_BGR2RGB)` 转换。
>
> **📝 Exam / 考法:**
> "What is a pixel? How is it represented in grayscale vs color images?" Grayscale=single 0-255, Color=tuple (R,G,B).
> "什么是像素？灰度图和彩色图中如何表示？" 灰度=单值0-255，彩色=三元组(R,G,B)。

---

## 8. AI 与 CNN 预览 (AI in Machine Vision & CNN Preview)

- Deep Learning revolutionized MV — enhancing accuracy, enabling complex pattern recognition
- CNNs: class of deep neural networks for visual imagery, powerful for automated feature extraction

![Picture 2](week1_intro_machine_vision_slides_images/slide12_img1.jpg)
![Picture 2](week1_intro_machine_vision_slides_images/slide13_img1.gif)

> **📝 Notes / 笔记:**
>
> **📌 What / 是什么:**
> CNN = a neural network designed specifically for images, using sliding filters instead of connecting every pixel to every neuron.
> CNN = 专门为图像设计的神经网络，使用滑动滤波器而不是将每个像素连接到每个神经元。
>
> **🎯 Why / 为什么:**
> Why CNN instead of regular neural networks? A 1000×1000 image = 1 million inputs. A regular ANN connecting every pixel to even 1000 neurons = 1 billion parameters — computationally insane and ignores that nearby pixels are related. CNN solves this with small shared filters. Details in Week 4.
> 为什么用 CNN 而不是普通神经网络？1000×1000 图像 = 100万输入。普通 ANN 每个像素连1000个神经元 = 10亿参数 — 计算疯狂且忽略了相邻像素的关联。CNN 用小型共享滤波器解决。详见第4周。
>
> **💡 Intuition / 直觉:**
> ANN looking at an image = reading a book one character at a time with no context. CNN = scanning with a magnifying glass, looking at small patches and recognizing local patterns.
> ANN 看图像 = 逐字读书没有上下文。CNN = 用放大镜扫描，观察小区域并识别局部模式。
>
> **⚙️ How / 怎么算:** — (Covered in Week 4)
>
> **⚖️ Compare / 对比:**
> ANN vs CNN for images: ANN treats pixels independently (loses spatial info), CNN preserves spatial relationships via local filters. This is THE fundamental advantage.
> ANN vs CNN 处理图像：ANN 将像素独立处理（丢失空间信息），CNN 通过局部滤波器保留空间关系。这是根本优势。
>
> **⚠️ Pitfall / 易错点:**
> CNN is not magic — it still needs clean, well-processed input. Weeks 2-3 (image processing, feature detection) are prerequisites, not skippable.
> CNN 不是魔法 — 仍然需要干净、处理好的输入。第2-3周（图像处理、特征检测）是先决条件，不能跳过。
>
> **📝 Exam / 考法:**
> "Why are CNNs preferred over traditional ANNs for image classification?" Parameter sharing + spatial structure preservation.
> "为什么 CNN 优于传统 ANN 用于图像分类？" 参数共享 + 保留空间结构。

---

## 9. 职业与资源 (Career & Resources)

**Careers:** Machine Vision Engineer, Data Scientist, R&D
**Industries:** Healthcare, Automotive, Consumer Electronics
**Tools:** Python, OpenCV, PyTorch
**Video:** https://youtu.be/ArPaAX_PhIs?si=iB53B6NqweLtwVUD

---

## 10. 总结与下周预告 (Summary & Next Week)

**Summary:** MV basics, history, key technologies, applications, workflow, pixels, AI/CNN preview.

**Next week:** Fundamentals of Image Processing.

---

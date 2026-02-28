# Week 1: 机器视觉导论 (Introduction to Machine Vision)

> Source: `Week 1 - Introduction to Machine Vision1.pptx`
> Total slides: 17
> Instructor: Stephin Rachel Thomas | 15-01-2026

---

## 1. 课程信息 (Course Information)

### 1.1 课程标题 (Course Title)

![Page 1](week1_intro_slides_pages/page_001.png)

### 1.2 课程后勤与政策 (Course Logistics and Policy)

![Page 2](week1_intro_slides_pages/page_002.png)

- Course Brightspace page: https://brightspace.algonquincollege.com/d2l/le/content/846092/Home — 课程Brightspace页面
- Please read the course outline and course section information (CSI) — 请阅读课程大纲和课程章节信息
- Main focus of the labs is to assess your understanding of implementation and demo your work in each session — 实验重点是评估你对实现的理解并在每次课上展示你的工作
- Professional behaviour is expected from all students — 要求所有学生保持专业行为
- Lab activities and assignments should be done individually; any use of online materials, including ChatGPT and LLMs, must be stated clearly as references — 实验和作业应独立完成；使用任何在线材料（包括ChatGPT和LLM）必须明确注明引用

---

## 2. 课程概览 (Course Overview)

![Page 3](week1_intro_slides_pages/page_003.png)

- This course takes you on a journey through the world of Machine Vision, combining theoretical knowledge with practical applications — 本课程带你踏上机器视觉之旅，将理论知识与实际应用结合
- Get ready to explore the path from **pixels to perception** — 准备好探索从**像素到感知**的路径
- The field of CV is huge; we will hope to scratch the surface in this class — 计算机视觉领域很大；我们在这门课中只能浅尝辄止

---

## 3. 什么是机器视觉 (What is Machine Vision?)

![Page 4](week1_intro_slides_pages/page_004.png)

- **Machine vision** is a technology that enables machines to interpret and understand visual information from the surrounding environment — **机器视觉**是一种使机器能够解读和理解周围环境视觉信息的技术
- It involves **capturing** images or videos using cameras or sensors, **processing** these images to extract useful information, and then **using** this information to make decisions or perform specific tasks — 包括用摄像头或传感器**采集**图像或视频，**处理**图像以提取有用信息，然后**利用**这些信息做出决策或执行特定任务

---

## 4. 历史与演进 (History and Evolution of Machine Vision)

![Page 5](week1_intro_slides_pages/page_005.png)

- The journey began with simple image capturing devices, evolving through the digital revolution to sophisticated AI algorithms — 从简单的图像采集设备开始，经过数字革命发展为复杂的AI算法
- Key milestones: development of **digital cameras**, the rise of **neural networks**, and significant increases in **computing power** — 关键里程碑：**数码相机**的发展、**神经网络**的兴起、**计算能力**的大幅提升
- Significant turning point: the rise of **deep learning** techniques — 重要转折点：**深度学习**技术的兴起

---

## 5. 关键技术 (Key Technologies in Machine Vision)

![Page 6](week1_intro_slides_pages/page_006.png)

- **Image sensors**: CCD (Charge-Coupled Device) and CMOS (Complementary Metal-Oxide Semiconductor) — **图像传感器**：CCD（电荷耦合器件）和CMOS（互补金属氧化物半导体）
- **Image processing techniques**: filtering, edge detection — **图像处理技术**：滤波、边缘检测
- **Machine Learning**, particularly **deep learning**, in modern Machine Vision systems — **机器学习**，尤其是**深度学习**，在现代机器视觉系统中的作用

---

## 6. 日常应用 (Applications in Everyday Life)

![Page 7](week1_intro_slides_pages/page_007.png)

- **Retail**: barcode scanning and inventory management — **零售**：条码扫描和库存管理
- **Manufacturing**: quality checks on the assembly line — **制造业**：流水线上的质量检测
- **Entertainment**: detection and tracking of objects of interest, enhancing visual effects in movies and games — **娱乐**：感兴趣对象的检测与跟踪，增强电影和游戏中的视觉效果
- **Autonomous vehicles**: lane keeping, blind spot checking, adaptive cruise — **自动驾驶**：车道保持、盲区检查、自适应巡航

---

## 7. 高级应用 (Advanced Applications)

![Page 8](week1_intro_slides_pages/page_008.png)

- **Autonomous vehicles** use it for navigation — **自动驾驶汽车**用于导航
- **Medical imaging** uses it for diagnostics and surgical assistance — **医学影像**用于诊断和手术辅助
- **Facial recognition** systems enhance security and personalized experiences — **人脸识别**系统增强安全性和个性化体验
- Ref: Week 1 Asynchronous material

---

## 8. 机器视觉系统工作流 (Basic Workflow of a Machine Vision System)

![Page 9](week1_intro_slides_pages/page_009.png)

1. **Image Acquisition** — Capturing the image — **图像采集** — 获取图像
2. **Image Processing** — Analyzing and manipulating the image — **图像处理** — 分析和处理图像
3. **Interpretation/Action** — Making decisions based on the processed image — **解读/行动** — 基于处理后的图像做出决策

- Example: in an automated inspection system in manufacturing, this workflow ensures quality control — 例如：在制造业的自动检测系统中，该工作流确保质量控制

---

## 9. 图像处理基础 (Introduction to Image Processing)

### 9.1 图像格式与色彩空间 (Image Formats and Color Spaces)

![Page 10](week1_intro_slides_pages/page_010.png)

- Image processing forms the **core** of Machine Vision — 图像处理是机器视觉的**核心**
- **Image Formats**: JPEG, PNG, RAW — **图像格式**：JPEG、PNG、RAW
- **Color Spaces**: RGB and HSV — **色彩空间**：RGB和HSV
- Quick example of how to read an image using **OpenCV** — 使用**OpenCV**读取图像的快速示例

### 9.2 像素定义 (Pixel Definition)

![Page 11](week1_intro_slides_pages/page_011.png)

- A **pixel** is a numerical representation at location (x, y) in an image — **像素**是图像中位置(x, y)处的数值表示
- **Grayscale**: single value representing black intensity — **灰度图**：单个值表示黑色强度
- **Color (RGB)**: tuple of 3 values representing Red, Green, and Blue intensities — **彩色图（RGB）**：3个值的元组，表示红、绿、蓝的强度

---

## 10. AI与深度学习在机器视觉中的过渡 (Transition to AI in Machine Vision)

### 10.1 AI与深度学习的影响 (Impact of AI and Deep Learning)

![Page 12](week1_intro_slides_pages/page_012.png)

- The evolution of AI, especially **Deep Learning**, has revolutionized Machine Vision — AI的发展，尤其是**深度学习**，已经彻底改变了机器视觉
- AI enhances accuracy and enables recognition of **complex patterns** — AI提高了准确性并使识别**复杂模式**成为可能
- In upcoming sessions: how **CNNs** work and real-world applications — 后续课程：**CNN**的工作原理及实际应用

### 10.2 CNN预览 (CNN Sneak Peek)

![Page 13](week1_intro_slides_pages/page_013.png)

- **Convolutional Neural Networks (CNNs)** are a class of deep neural networks, most commonly applied to analyzing visual imagery — **卷积神经网络（CNN）**是一类深度神经网络，最常用于分析视觉图像
- Powerful for **automated feature extraction** in images — 在图像中进行**自动特征提取**方面非常强大
- Will be covered in detail in later lectures — 将在后续课程中详细讲述

---

## 11. 职业机遇 (Career Opportunities in Machine Vision)

![Page 14](week1_intro_slides_pages/page_014.png)

- Potential roles: **Machine Vision Engineer**, **Data Scientist**, **R&D** positions — 潜在岗位：**机器视觉工程师**、**数据科学家**、**研发**岗位
- Industries: **Healthcare**, **Automotive**, **Consumer Electronics** — 行业：**医疗**、**汽车**、**消费电子**

---

## 12. 学习资源 (Resources for Further Learning)

![Page 15](week1_intro_slides_pages/page_015.png)

- Video resource: https://youtu.be/ArPaAX_PhIs?si=iB53B6NqweLtwVUD
- ChatGPT as a learning resource — ChatGPT作为学习资源
- Tools: **Python**, **OpenCV**, and **PyTorch** — 工具：**Python**、**OpenCV**和**PyTorch**

---

## 13. 本讲小结 (Summary of Today's Lecture)

![Page 16](week1_intro_slides_pages/page_016.png)

- The basics of Machine Vision — 机器视觉基础
- Its history and key technologies — 历史与关键技术
- Real-world applications, from everyday uses to advanced fields — 实际应用，从日常用途到高级领域
- "The world of Machine Vision is as expansive as it is exciting, and you're just getting started!" — "机器视觉世界既广阔又令人兴奋，你才刚刚起步！"

---

## 14. 下周预告 (Next Week Preview)

![Page 17](week1_intro_slides_pages/page_017.png)

- Next week: **Fundamentals of Image Processing** — 下周：**图像处理基础**
- Topics: how images are captured and processed — 主题：图像如何被获取和处理

---

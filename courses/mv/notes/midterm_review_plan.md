# CST8508 Machine Vision — Midterm Review Plan

## 考试范围: Week 1 - Week 5

### 材料盘点

| Week | 主题 | Slides | Notes | Quiz | Lab | Code | Resources | 状态 |
|------|------|--------|-------|------|-----|------|-----------|------|
| 1 | Introduction to Machine Vision | ✅ `Week 1 - Introduction to Machine Vision1.pptx` | ❌ | ✅ quizes1.md (Q1,Q3) | ✅ Lab1 (.ipynb+.py) | — | — | 🟡 需补笔记 |
| 2 | Fundamentals of Image Processing | ✅ `Week 2 - Fundamentals of Image Processing1.pptx` | ❌ | ✅ quizes1.md (Q2,Q4-Q11) | ✅ Lab2 (.ipynb) | — | ✅ week2.md | 🟡 需补笔记 |
| 3 | Object/Feature Detection and Description | ✅ `Week. 3-Object_Feature Detection and Description.pptx` | ❌ | ✅ quizes1.md (Q12,Q13) | ✅ Lab3 (.ipynb+.py) | — | — | 🟡 需补笔记 |
| 4 | Introduction to CNNs | ✅ `Week 4 - Introduction to Convolutional Neural Networks (CNNs)1.pptx` | ❌ | ✅ quizes1.md (Q14,Q15) | ✅ Lab4 (.ipynb) | ✅ lab4/ | — | 🟡 需补笔记 |
| 5 | Deep Learning for Image Classification | ✅ `Week5_ Deep Learning for Image Classification1.pptx` | ❌ | ❌ | ❌ | — | — | 🔴 需补笔记+Quiz |

---

### 已有材料详情

#### 📊 Slides (5/5 完整)

1. `slides/Week 1 - Introduction to Machine Vision1.pptx` (4.4 MB)
2. `slides/Week 2 - Fundamentals of Image Processing1.pptx` (18.3 MB)
3. `slides/Week. 3-Object_Feature Detection and Description.pptx` (9.2 MB)
4. `slides/Week 4 - Introduction to Convolutional Neural Networks (CNNs)1.pptx` (12.5 MB)
5. `slides/Week5_ Deep Learning for Image Classification1.pptx` (9.1 MB)

#### 📝 Notes (0/5 — 全部缺失)

- 尚无任何主题的结构化笔记

#### ❓ Quizzes

- `quizzes/quizes1.md` — 15 道选择题（已有答案和解释），覆盖 Week 1-4：
  - Q1, Q3: Machine Vision 基础 (Week 1)
  - Q2, Q4-Q11: Image Processing 基础 (Week 2)
  - Q12, Q13: Feature Detection - ORB, HOG (Week 3)
  - Q14, Q15: CNN, Accuracy (Week 4)
  - ❌ 无 Week 5 相关题目

#### 🧪 Labs

- `labs/CST8508_26W_Lab1.ipynb` + `.py` — Lab 1
- `labs/CST8508_Lab2.ipynb` — Lab 2
- `labs/lab3_orb.ipynb` + `.py` — Lab 3 (ORB)
- `labs/lab3_vision_basics.ipynb` — Lab 3 (Vision Basics)
- `labs/CST8508_Lab_4.ipynb` — Lab 4

#### 💻 Code

- `code/lab4/` — Lab 4 代码
- `code/test_opencv.py` — OpenCV 测试

#### 📚 Resources

- `resources/week2.md` — Week 2 补充阅读：Digital Image Processing 基础
- `resources/13436_Pruning_vs_Quantization_.pdf` — 论文：Pruning vs Quantization（可能与 Week 5 相关）
- `resources/1910.13796v1.pdf` — 论文（需确认主题）
- `resources/ChiranjiLalChow-ComputerVisionAndReco-2021-13ApplicationOfComput1.pdf` — 教材章节：CV 应用

#### 📖 Textbook

- (空)

---

### 待补充项

#### 🔴 紧急（笔记缺失）
- [ ] Week 1 笔记: Introduction to Machine Vision
- [ ] Week 2 笔记: Fundamentals of Image Processing
- [ ] Week 3 笔记: Object/Feature Detection and Description
- [ ] Week 4 笔记: Introduction to CNNs
- [ ] Week 5 笔记: Deep Learning for Image Classification

#### 🟡 建议（题库补充）
- [ ] Week 5 Quiz 题目（目前无覆盖）
- [ ] 各主题额外练习题
- [ ] 模拟试卷

#### 🟢 可选（深化理解）
- [ ] 代码复习整理
- [ ] 速查表生成
- [ ] 论文摘要提取

---

### 主题关键词速览

| Week | 核心主题 | 关键概念 |
|------|---------|---------|
| 1 | Machine Vision 概论 | MV 定义、应用、工作流（采集→处理→分析→决策） |
| 2 | 图像处理基础 | 像素、直方图、滤波（模糊/锐化）、阈值、形态学操作、边缘检测（Canny）、轮廓 |
| 3 | 特征检测与描述 | FAST、BRIEF、ORB、SIFT、SURF、HOG、关键点匹配 |
| 4 | CNN 基础 | 卷积层、池化层、全连接层、特征图、激活函数 |
| 5 | 深度学习图像分类 | 分类架构、训练流程、迁移学习、模型评估指标 |

---

### 复习优先级建议

1. **最优先**: Week 2 (图像处理) — quiz 题目最多 (10 道)，内容量大
2. **高优先**: Week 3 (特征检测) — Lab 3 代码量大，概念多
3. **高优先**: Week 4 (CNN) — 核心深度学习概念
4. **中优先**: Week 5 (DL 分类) — 无 quiz 覆盖，需要额外关注
5. **低优先**: Week 1 (概论) — 概念性内容，相对简单

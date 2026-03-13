---
name: learning-lecture-history
description: Reorganize lecture/assignment concepts into a historical evolution timeline. Use when (1) user asks to create a "历史线" or "history timeline" from course materials, (2) user wants to understand the historical progression of techniques/algorithms, (3) user mentions understanding "why this technique was invented".
---

# Learning Lecture History (历史线技能)

## 目标 / Objective

将课程中出现的**技术概念**按历史脉络重组，帮助学生理解**"为什么会有这个技术"**——技术不是凭空出现的，每个技术都是为了解决前一个技术的局限性而诞生的。

## 核心理念 / Core Philosophy

> **技术 = 对前一个问题的回答。**

每个技术节点必须回答三个问题：

1. **之前的问题是什么？** — What problem existed before?
2. **这个技术怎么解决的？** — How did this technique solve it?
3. **它又留下了什么新问题？** — What new problem did it create?

## 输出格式 / Output Format

文件命名：`[topic]_history.md`

### 模板结构

```markdown
# 🕰️ [主题] 技术演进历史线

> **课程:** [课程号] | **主题:** [主题]
> **时间跨度:** [最早年份] — [最晚年份]
> **核心脉络:** [一句话概括演进主线]

---

## 📍 全景时间线（Timeline Overview）

[ASCII 时间轴图，从左到右按年代排列关键节点]

---

## 第 N 站：[技术名] ([年份])

### 🧩 之前的问题

[前一个技术留下了什么问题]

### 💡 核心创新

[这个技术怎么解决的，一句话概括]

### 👤 关键人物

[发明者/团队，所属机构，论文名]

### 📊 里程碑数据

[关键性能数据，如 ImageNet 错误率等]

### ⚠️ 遗留问题

[这个技术又创造了什么新问题 → 引出下一站]

### 🔗 与本课程的关联

[这个技术在本课程/assignment 中具体怎么用到的]

---

## 📊 对比总结表

[所有技术节点的横向对比表]

## 🎯 考试相关

[历史线中可能出现的考试知识点]
```

## 写作规则 / Writing Rules

### 规则 1：因果链必须完整（Causal Chain Completeness）

每两个相邻技术节点之间必须有清晰的**因果关系**：

```
技术 A 的遗留问题 → 正好 = 技术 B 要解决的问题
```

如果找不到因果关系，说明中间缺少过渡节点，需要补上。

### 规则 2：数据说话（Data-Driven）

每个技术节点需要**至少一个具体数据点**来证明它的价值：

```
✅ "AlexNet 在 ImageNet 上将 Top-5 错误率从 26.2% 降至 15.3%"
❌ "AlexNet 大幅提高了准确率"
```

### 规则 3：人物不能少（People Matter）

每个技术节点必须标注：

- 发明者姓名
- 所属机构
- 论文/工作的年份
- 命名来源（如果名字有特殊含义）

### 规则 4：与课程的锚定（Course Anchoring）

每个技术节点必须回答：**"这个技术在我们的课程/作业中哪里用到了？"**

```
✅ "ResNet-18 是 Assignment 1 中选的第一个模型"
✅ "ImageNet 的均值/标准差是配置文件中的 data_preprocessor 参数"
❌ 没有任何与课程的关联（那为什么要讲这个？）
```

### 规则 5：聚焦课程涉及的技术（Scope Limiting）

历史线只覆盖**课程/作业直接涉及**的技术及其直接前身。不要写成完整的领域综述。

```
Assignment 1 涉及 ResNet-18 和 MobileNet V2
  → 回溯到 LeNet、AlexNet、VGGNet（ResNet 的前身）
  → 涉及 SGD 和 Adam（优化器演进）
  → 涉及 ImageNet（归一化和预训练的背景）
  → 不需要讲 YOLO、Mask R-CNN、ViT（与本次作业无关）
```

### 规则 6：语言风格

- **纯中文叙事**（与 Storyline 一致）
- 英文术语首次出现时给出中文翻译：`残差连接（Residual Connection / Skip Connection）`
- 论文名保留英文原名

## 与其他阶段的区别

| 阶段                     | 核心问题                | 组织方式                       |
| ------------------------ | ----------------------- | ------------------------------ |
| **Phase 1 翻译**         | "这个 slide 说了什么？" | 逐 slide 翻译                  |
| **Phase 1.5 故事线**     | "为什么需要这个概念？"  | 因果叙事（problem → solution） |
| **Phase 1.55 历史线** ⭐ | "这个技术从哪来？"      | **时间轴（年代 → 演进）**      |
| **Phase 1.7 教程**       | "教科书怎么推导？"      | 定义 → 定理 → 推导             |

**关键区分：**

- **故事线**是"一次课/作业内部的逻辑线"——聚焦当前问题的解决思路
- **历史线**是"跨越多年的技术演进线"——聚焦技术的历史来源和演变

## 使用时机 / When to Use

1. 课程涉及**有明确演进关系的技术栈**（如 CNN 架构、优化器、NLP 模型等）
2. 学生需要理解**为什么选择某个特定技术**而非其替代品
3. Assignment 或 lab 使用了**特定版本的技术**（如 ResNet-18 而非 ResNet-50）

## 跳过条件 / Skip Conditions

- 主题是纯数学/纯理论（如概率论基础），没有明确的技术演进关系
- 主题只涉及一个技术，没有前身也没有后续（罕见）

## 四层递进解释（核心概念解释规范）

在解释每个技术的"核心创新"时，用四层递进：

| 层次 | 内容 | 示例 |
|------|------|------|
| ① 一句话定义 | 最通俗的描述 | "ResNet = 普通 CNN + 捷径" |
| ② 原理/公式 | 精确的技术描述 | `y = F(x) + x`（残差公式）|
| ③ 具体例子 | 课程/作业/现实中的案例 | "Assignment 1 中用的就是 ResNet-18" |
| ④ 类比/记忆技巧 | 生活化比喻 | "就像走路累了可以走直线捷径，不必绕远" |

> 💡 详细写法参考 `learning-lecture-storyline` skill §3.2 四层递进法

## 复习清单要求（必须输出）

每份历史线文末**必须**包含 `## 🎯 考试相关` 一节，用 `- [ ]` checklist 格式：

```markdown
## 🎯 考试相关

- [ ] 能说出[技术A]出现前大家遇到了什么问题？
- [ ] 能解释[技术B]用了什么核心思路解决了这个问题？
- [ ] 记住[关键人物]和对应技术的配对？
- [ ] 能列出至少一个具体性能数据（如 ImageNet 错误率）？
- [ ] 知道这段历史在本课程的哪个作业/实验中用到了？
```


---
description: Complete course assignment from start to submission - handles complex multi-step assignments with environment setup, training, evaluation, and reporting
---

# 📝 课程 Assignment 完成工作流 (Universal Assignment Workflow)

与 Lab 不同，Assignment 通常是更大规模、多步骤的综合项目，涉及环境搭建、模型训练、评估分析和报告撰写。

## 🎯 使用方式

```
/complete-assignment [课程] [作业编号]

示例:
/complete-assignment mv assignment1
/complete-assignment ml assignment2
/complete-assignment nlp assignment1
/complete-assignment rl assignment1    ← 推荐使用 /complete-assignment-rl
```

> **注意**: 对于 RL 课程的 Assignment，推荐使用专门的 `/complete-assignment-rl` 工作流。

## 📋 完整流程概览

```
┌─────────────────────────────────────────────────────────────┐
│ Phase 0: 环境准备 (Environment Setup)                        │
│   ↓ 安装依赖、配置运行环境 (conda/venv/WSL)                    │
├─────────────────────────────────────────────────────────────┤
│ Phase 1: 需求理解 (Requirement Analysis)                     │
│   ↓ 抓取/转换/理解作业文档                                     │
├─────────────────────────────────────────────────────────────┤
│ Phase 2: 数据准备 (Data Preparation)                         │
│   ↓ 下载/处理/划分数据集                                       │
├─────────────────────────────────────────────────────────────┤
│ Phase 3: 代码开发 (Code Development)                         │
│   ↓ 实现核心代码，含训练、评估脚本                               │
├─────────────────────────────────────────────────────────────┤
│ Phase 4: 训练与调参 (Training & Tuning)                      │
│   ↓ 运行训练、超参数调优、多次实验                               │
├─────────────────────────────────────────────────────────────┤
│ Phase 5: 评估与分析 (Evaluation & Analysis)                  │
│   ↓ 模型评估、性能对比、结果可视化                               │
├─────────────────────────────────────────────────────────────┤
│ Phase 6: 报告撰写 (Report Writing)                           │
│   ↓ 截图、分析、撰写报告文档                                    │
├─────────────────────────────────────────────────────────────┤
│ Phase 7: 提交打包 (Submission & Packaging)                   │
│   ↓ 检查、打包、提交                                           │
└─────────────────────────────────────────────────────────────┘
```

---

## ⚖️ 执行协议 (Execution Protocol)

为保证执行的确定性，Agent 必须严格遵守以下原则：

1. **串行执行**: 按 Phase 顺序执行，禁止跨阶段执行。
2. **检查点验证**: 每个 Phase 末尾有验证检查点，必须全部通过后才能进入下一阶段。
3. **中断恢复**: 使用 `--from=<phase>` 参数从指定阶段继续。
4. **作业文档优先**: 老师的作业文档中的要求优先级最高，工作流中的通用规范需让步于老师的具体要求。

---

## Phase 0: 环境准备 📦

**目标**: 搭建能运行 Assignment 所有代码的运行环境。

### 步骤

1. **读取作业要求**: 确认需要哪些框架和工具
2. **检查现有环境**: 查看是否已有可用的虚拟环境
3. **创建/更新环境**:
   - **Python 项目** (常规): 用 `uv` 创建虚拟环境
     ```bash
     uv venv
     uv pip install -r requirements.txt
     ```
   - **深度学习项目** (GPU): 可能需要 conda 或 WSL
     ```bash
     # WSL + conda 示例
     conda create -n assignment python=3.10
     conda activate assignment
     conda install pytorch torchvision torchaudio pytorch-cuda=12.4 -c pytorch -c nvidia
     pip install -r requirements.txt
     ```
   - **特殊框架**: 按老师或框架文档安装 (如 mmcv, mmpretrain, detectron2 等)

4. **验证安装**: 运行 `import` 测试确认所有依赖可用

### 环境脚本（推荐）

为复杂环境创建可重复的安装脚本：

```bash
# setup.sh 或 setup_env.sh
#!/bin/bash
set -e
echo "=== Setting up environment ==="
# ... 安装步骤 ...
echo "=== Environment ready ==="
```

### ✅ 验证检查点

- [ ] 所有依赖安装成功
- [ ] GPU 可用 (如需要): `python -c "import torch; print(torch.cuda.is_available())"`
- [ ] 核心框架能正常导入
- [ ] 无版本冲突

---

## Phase 1: 需求理解 🧠

**Skills**: `learning-brightspace_scraper`, `dev-pdf_processing`, `dev-docx_to_md`, `ai_learning-[course]`

### 步骤

1. **获取作业文档**:
   - 如果尚未下载，使用 `learning-brightspace_scraper` 从 Brightspace 抓取
   - 或直接使用已有的 PDF/DOCX 文件

2. **格式转换**:

   ```
   读取 skill: .shared/skills/dev-pdf_processing/SKILL.md
   转换作业文档到 Markdown
   ```

3. **深度分析** (关键步骤):
   - 列出所有需要完成的任务
   - 识别评分标准 (Rubric)
   - 标注难点和注意事项
   - 确认提交物清单（代码、报告、数据等）

4. **创建任务清单**: 在代码目录创建 `TODO.md` 或在 Assignment Report 中列出所有任务

### 作业分析模板

```markdown
## Assignment 分析

### 基本信息

- 课程: [课程名]
- 作业: [作业编号]
- 截止日期: [日期]
- 提交方式: [Brightspace/Git/email]

### 任务分解

1. [ ] Task 1: ...
2. [ ] Task 2: ...
3. [ ] Task 3: ...

### 提交物清单

- [ ] 代码文件: ...
- [ ] 报告/文档: ...
- [ ] 截图/可视化: ...
- [ ] 其他: ...

### 评分标准

| 项目 | 分值 | 要求 |
| ---- | ---- | ---- |
| ...  | ...  | ...  |
```

### ✅ 验证检查点

- [ ] 作业文档已阅读并理解
- [ ] 任务清单已创建
- [ ] 提交物清单已确认
- [ ] 评分标准已记录

---

## Phase 2: 数据准备 📊

**Skills**: `dev-data_download`, `learning-code_generation`

### 步骤

1. **确认数据来源**:
   - 老师提供的数据集
   - 需要下载的公开数据集 (Kaggle, UCI, HuggingFace 等)
   - 需要自行生成的数据

2. **下载/准备数据**:

   ```bash
   # 从指定来源下载
   python prepare_dataset.py
   # 或使用命令行工具
   wget/curl [url]
   ```

3. **数据集划分** (如需要):

   ```python
   # 训练集/验证集/测试集划分
   from sklearn.model_selection import train_test_split
   train, val = train_test_split(data, test_size=0.2, random_state=SEED)
   ```

4. **数据验证**:
   - 确认数据格式正确
   - 检查标签分布
   - 验证文件路径

### 数据目录结构

```
assignment[n]/
├── data/                    # 数据集目录
│   ├── train/
│   ├── val/
│   └── test/               # 如有
├── configs/                 # 配置文件
└── ...
```

### ✅ 验证检查点

- [ ] 数据集完整下载/准备
- [ ] 数据格式正确
- [ ] 训练/验证划分完成
- [ ] 数据路径配置正确

---

## Phase 3: 代码开发 💻

**Skills**: `learning-code_generation`, `dev-code_comment`, `ai_learning-[course]`

### ⚠️ 前置步骤：读取学生信息

**必须**首先从 `.env.local` 读取学生信息：

```bash
# 读取 .env.local 获取:
# - NAME=Peng Wang
# - NUMBER=041107730
```

### 步骤

1. **必须**先阅读 `.shared/skills/learning-code_generation/SKILL.md`
2. **必须**严格遵守 `.shared/skills/dev-code_comment/SKILL.md` 的双语注释规范
3. **推荐**参考 `.github/` 目录下克隆的开源框架源码
4. 根据作业要求开发代码

### 代码类型

Assignment 通常需要多个代码文件：

| 文件类型 | 说明            | 示例                             |
| -------- | --------------- | -------------------------------- |
| 训练脚本 | 模型训练主程序  | `train.py`                       |
| 评估脚本 | 模型评估程序    | `evaluate.py`                    |
| 数据处理 | 数据预处理/增强 | `prepare_dataset.py`             |
| 配置文件 | 超参数/模型配置 | `configs/*.py`, `configs/*.yaml` |
| 工具函数 | 辅助功能        | `utils.py`                       |
| Notebook | 交互式开发/展示 | `Assignment[N].ipynb`            |

### ⚠️ 关键规范 (CRITICAL)

- **双语注释**: 所有代码块必须有中英双语注释。中文在前，英文在后。
- **Docstrings**: 文件头部 Docstring 仅使用英文。函数 Docstring 使用双语。
- **匹配老师风格**: 如果老师提供了代码模板或示例，必须严格匹配其风格。
- **变量命名**: 变量和函数名必须使用英文。
- **配置外置**: 超参数和路径等配置项提取到文件顶部或配置文件中。

### ✅ 验证检查点

- [ ] 所有代码文件创建完成
- [ ] 双语注释规范符合要求
- [ ] 代码风格匹配老师要求
- [ ] 配置文件正确

---

## Phase 4: 训练与调参 🏋️

**Skills**: `ai_learning-[course]`, `learning-code_generation`

### 步骤

1. **基线训练**: 使用默认/推荐超参数进行第一次训练

   ```bash
   python train.py --config configs/baseline.py
   ```

2. **验证基线**: 确认基线模型能正常收敛

   ```bash
   python evaluate.py --checkpoint work_dirs/latest.pth
   ```

3. **超参数调优** (如需要):

   | 实验     | 改动         | 目的     |
   | -------- | ------------ | -------- |
   | Baseline | 默认参数     | 建立基线 |
   | Exp 1    | 调整学习率   | 优化收敛 |
   | Exp 2    | 调整数据增强 | 提升泛化 |
   | Exp 3    | 调整模型结构 | 对比模型 |

4. **结果记录**: 记录每次实验的关键指标
   ```
   | 实验 | Accuracy | Loss | 训练时间 |
   |------|----------|------|----------|
   | ... | ... | ... | ... |
   ```

### 训练日志管理

- 使用 `tee` 同时输出到终端和文件：
  ```bash
  python train.py 2>&1 | tee training_log.txt
  ```
- 保存训练曲线截图
- 保存最终模型 checkpoint

### ✅ 验证检查点

- [ ] 基线模型训练完成
- [ ] 模型能正常收敛
- [ ] 训练日志已保存
- [ ] 超参数实验已完成（如需要）

---

## Phase 5: 评估与分析 📈

**Skills**: `ai_learning-[course]`, `learning-code_screenshot`

### 步骤

1. **模型评估**: 在验证集/测试集上评估模型

   ```bash
   python evaluate.py --checkpoint best_model.pth
   ```

2. **结果可视化**:
   - 训练曲线 (Loss, Accuracy vs Epoch)
   - 混淆矩阵 (分类任务)
   - 示例预测结果
   - 模型对比图表

3. **结果分析**:
   - 定量分析：准确率、精确率、召回率、F1 等
   - 定性分析：成功和失败案例分析
   - 对比分析：不同模型/参数的对比

### 图表保存规范

```python
OUTPUT_DIR = 'assignment[n]_images'  # 或按老师要求的目录名
os.makedirs(OUTPUT_DIR, exist_ok=True)
plt.savefig(os.path.join(OUTPUT_DIR, 'plot_name.png'), dpi=150, bbox_inches='tight')
plt.close()
```

### ✅ 验证检查点

- [ ] 模型评估结果已获得
- [ ] 可视化图表已保存
- [ ] 结果分析已完成
- [ ] 关键指标已记录

---

## Phase 6: 报告撰写 📝

**Skills**: `learning-assignment_document`, `learning-code_screenshot`, `learning-md_to_docx`

### 步骤

1. **生成截图** (如需要):

   ```
   读取 skill: .shared/skills/learning-code_screenshot/SKILL.md
   生成每个步骤的代码和输出截图
   ```

2. **撰写报告**:

   ```
   读取 skill: .shared/skills/learning-assignment_document/SKILL.md
   按老师的报告模板/评分标准撰写报告
   ```

3. **报告结构** (通用模板，以老师要求为准):

   ```markdown
   # Assignment [N] Report

   ## Student Information

   - Name: [NAME]
   - Student Number: [NUMBER]

   ## 1. Introduction / Problem Description

   [作业目标和问题描述]

   ## 2. Methodology / Approach

   [方法论和实现方案]

   ## 3. Implementation

   [关键代码说明和截图]

   ## 4. Results

   [实验结果和可视化]

   ## 5. Analysis / Discussion

   [结果分析和讨论]

   ## 6. Conclusion

   [总结和改进方向]
   ```

4. **转换格式** (如需要 Word):
   ```bash
   python .shared/skills/learning-md_to_docx/scripts/convert_md_to_docx.py Assignment[N]_Report.md
   ```

### ✅ 验证检查点

- [ ] 截图完整且清晰
- [ ] 报告内容覆盖所有评分项
- [ ] 图表和数据准确
- [ ] 格式符合要求

---

## Phase 7: 提交打包 📤

**Skills**: `learning-lab_submission`, `dev-git`

### 步骤

1. **清理**: 删除不需要的文件

   ```bash
   # 清理缓存
   find . -type d -name "__pycache__" -exec rm -rf {} +
   find . -type f -name "*.pyc" -delete
   # 清理虚拟环境（不要提交）
   # 检查无 venv, .venv 目录在提交物中
   ```

2. **提交前检查**:

   ```
   读取 skill: .shared/skills/learning-lab_submission/SKILL.md
   执行提交前检查
   ```

3. **检查清单**:
   - [ ] 所有要求的代码文件存在
   - [ ] 报告/文档完整
   - [ ] 截图/可视化文件齐全
   - [ ] 文件命名符合要求
   - [ ] 代码可运行（无硬编码的绝对路径）
   - [ ] 没有多余的临时文件

4. **Git 提交**:
   // turbo

   ```bash
   git add courses/[course]/code/assignment[n]/
   git commit -m "Complete [course] Assignment[N]"
   git push
   ```

5. **上传到 Brightspace** (手动):
   - 按老师要求上传指定文件
   - 确认上传成功

---

## 🗂️ 目录结构示例

```
courses/
└── mv/
    ├── labs/                              # 作业说明文档
    │   ├── Assignment1.md
    │   └── Assignment1.pdf
    │
    └── code/
        └── assignment1/                   # 代码和提交文件
            ├── configs/                   # 配置文件目录
            │   ├── baseline.py
            │   └── resnet50.py
            ├── data/                      # 数据目录 (可能 gitignore)
            │   ├── train/
            │   └── val/
            ├── assignment1_images/        # 可视化输出
            │   ├── training_curve.png
            │   ├── confusion_matrix.png
            │   └── sample_predictions.png
            ├── train.py                   # 训练脚本
            ├── evaluate.py                # 评估脚本
            ├── prepare_dataset.py         # 数据准备脚本
            ├── CST8508_Assignment1.py     # 主代码文件
            ├── CST8508_Assignment1.ipynb   # Notebook 版本
            ├── Assignment1_Report.md      # 报告 Markdown
            ├── Assignment1_Report.docx    # 报告 Word (如需要)
            └── setup.sh                   # 环境安装脚本 (可选)
```

---

## 💡 快捷子命令

| 命令                                                | 说明             | 从哪个 Phase 开始  |
| --------------------------------------------------- | ---------------- | ------------------ |
| `/complete-assignment mv assignment1`               | 完整流程         | Phase 0            |
| `/complete-assignment mv assignment1 --from=env`    | 从环境准备开始   | Phase 0            |
| `/complete-assignment mv assignment1 --from=code`   | 从代码开发开始   | Phase 3            |
| `/complete-assignment mv assignment1 --from=train`  | 从训练开始       | Phase 4            |
| `/complete-assignment mv assignment1 --from=eval`   | 从评估开始       | Phase 5            |
| `/complete-assignment mv assignment1 --from=report` | 从报告撰写开始   | Phase 6            |
| `/complete-assignment mv assignment1 --from=submit` | 从提交打包开始   | Phase 7            |
| `/complete-assignment mv assignment1 --check`       | 只运行提交前检查 | Phase 7 (检查部分) |

---

## 📊 支持的课程

| 课程代码 | 课程名称                    | 对应 Skill        | 备注                             |
| -------- | --------------------------- | ----------------- | -------------------------------- |
| `ml`     | Machine Learning            | `ai_learning-ml`  |                                  |
| `nlp`    | Natural Language Processing | `ai_learning-nlp` |                                  |
| `mv`     | Machine Vision              | `ai_learning-mv`  | 可能需要 WSL + GPU               |
| `cv`     | Computer Vision             | `ai_learning-cv`  | 可能需要 WSL + GPU               |
| `dl`     | Deep Learning               | `ai_learning-dl`  | 可能需要 WSL + GPU               |
| `rl`     | Reinforcement Learning      | `ai_learning-rl`  | 推荐用 `/complete-assignment-rl` |

---

## 🚨 常见问题

| 问题                    | 解决方案                                    |
| ----------------------- | ------------------------------------------- |
| GPU 内存不足 (CUDA OOM) | 减小 batch_size、用梯度累积、用混合精度训练 |
| 训练不收敛              | 检查学习率、数据预处理、模型初始化          |
| 数据路径错误            | 使用相对路径或配置文件管理路径              |
| WSL 环境问题            | 检查 CUDA 驱动、确认 WSL2 Ubuntu 版本       |
| 依赖冲突                | 创建独立虚拟环境、检查版本兼容性            |
| 模型保存/加载失败       | 确认 checkpoint 路径、检查磁盘空间          |
| 报告格式不符            | 仔细对照老师的模板和评分标准                |

---

## 🔄 与 complete-lab 的区别

| 特性 | `/complete-lab`    | `/complete-assignment`   |
| ---- | ------------------ | ------------------------ |
| 规模 | 较小，单次课堂练习 | 较大，综合项目           |
| 环境 | 通常用 `uv`/本地   | 可能需要 WSL/GPU/conda   |
| 数据 | 通常内嵌或很小     | 可能需要单独准备         |
| 训练 | 通常不需要         | 通常需要模型训练         |
| 调参 | 很少               | 可能需要超参数实验       |
| 报告 | 简单答题文档       | 完整分析报告             |
| 提交 | .ipynb + .docx     | 代码 + 报告 + 数据(可能) |

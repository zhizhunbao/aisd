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
/complete-assignment rl assignment1    ← 推荐使用 /complete-assignment-rl
```

## 📋 流程概览

```
Phase 0  环境准备    → 安装依赖、配置环境 (conda/venv/WSL)
Phase 1  需求理解    → 抓取/转换/理解作业文档
Phase 2  数据准备    → 下载/处理/划分数据集
Phase 3  代码开发    → 实现核心代码
Phase 4  训练调参    → 运行训练、超参数调优
Phase 5  评估分析    → 模型评估、结果可视化
Phase 6  报告撰写    → 截图、分析、报告文档
Phase 7  提交打包    → 检查、打包、提交
```

---

## ⚖️ 执行协议

1. **串行执行**: 按 Phase 顺序，禁止跨阶段
2. **检查点验证**: 每 Phase 末尾验证后才进入下一阶段
3. **中断恢复**: `--from=<phase>` 从指定阶段继续
4. **作业文档优先**: 老师要求 > 工作流通用规范

---

## Phase 0: 环境准备 📦

1. 读取作业要求，确认框架和工具
2. 创建/更新虚拟环境:
   - Python 常规: `uv venv && uv pip install -r requirements.txt`
   - 深度学习 GPU: conda/WSL + CUDA
   - 特殊框架: 按老师/框架文档安装
3. 验证安装: `import` 测试所有依赖

✅ **检查点**: 依赖安装成功 / GPU 可用 / 无版本冲突

---

## Phase 1: 需求理解 🧠

**Skills**: `brightspace-scraper`, `dev-pdf-processing`, `ai-learning-[course]`

1. 获取作业文档 (follow `brightspace-scraper` 或使用已有文件)
2. 格式转换: follow `dev-pdf-processing` skill
3. 深度分析: 列出任务 + 评分标准 + 提交物清单
4. 创建 TODO.md 任务清单
5. **必须**从 `.env.local` 读取学生信息 (NAME, NUMBER)

✅ **检查点**: 文档已理解 / 任务清单已创建 / 评分标准已记录

---

## Phase 2: 数据准备 📊

**Skill**: `data-download`

1. 确认数据来源 (老师提供 / 公开数据集 / 自行生成)
2. 下载/准备数据: follow `data-download` skill (如需要)
3. 数据集划分 (如需要): train/val/test
4. 数据验证: 格式、标签分布、文件路径

✅ **检查点**: 数据完整 / 格式正确 / 路径配置正确

---

## Phase 3: 代码开发 💻

**Skills**: `learning-code-generation`, `dev-code-comment`, `ai-learning-[course]`

1. Follow `learning-code-generation` skill 的开发规范
2. 双语注释: follow `dev-code-comment` skill
3. 推荐参考 `.github/` 下的开源框架源码

### 关键规范

- **双语注释**: 中文在前，英文在后
- **匹配老师风格**: 严格匹配老师代码模板
- **配置外置**: 超参数提取到文件顶部或配置文件

✅ **检查点**: 代码完成 / 注释规范 / 风格匹配

---

## Phase 4: 训练与调参 🏋️

**Skill**: `ai-learning-[course]`

1. 基线训练: 默认超参数第一次训练
2. 验证基线: 确认模型能正常收敛
3. 超参数调优 (如需要): 学习率 / 数据增强 / 模型结构
4. 结果记录: 每次实验的关键指标表格
5. 保存训练日志和 checkpoint

✅ **检查点**: 基线完成 / 模型收敛 / 日志已保存

---

## Phase 5: 评估与分析 📈

**Skills**: `ai-learning-[course]`, `learning-code-screenshot`

1. 模型评估: 验证集/测试集
2. 结果可视化: 训练曲线 / 混淆矩阵 / 示例预测
3. 结果分析: 定量 + 定性 + 对比

✅ **检查点**: 评估完成 / 图表已保存 / 分析完成

---

## Phase 6: 报告撰写 📝

**Skills**: `learning-assignment-document`, `learning-code-screenshot`, `learning-md-to-docx`

1. 生成截图: follow `learning-code-screenshot` skill
2. 撰写报告: follow `learning-assignment-document` skill
3. 按老师模板/评分标准组织内容
4. 转换格式 (如需 Word): follow `learning-md-to-docx` skill

✅ **检查点**: 截图完整 / 覆盖所有评分项 / 格式正确

---

## Phase 7: 提交打包 📤

**Skills**: `learning-lab-submission`, `git`

1. 清理: 删除 `__pycache__`、`.pyc`、虚拟环境
2. 提交前检查: follow `learning-lab-submission` skill
3. 检查清单:
   - [ ] 所有代码文件存在
   - [ ] 报告/文档完整
   - [ ] 文件命名符合要求
   - [ ] 无硬编码绝对路径

// turbo
4. Git 提交并推送

5. 上传到 Brightspace (手动)

---

## 💡 快捷子命令

| 命令 | Phase |
|------|-------|
| `/complete-assignment mv a1` | 完整 (Phase 0) |
| `--from=code` | Phase 3 |
| `--from=train` | Phase 4 |
| `--from=eval` | Phase 5 |
| `--from=report` | Phase 6 |
| `--from=submit` | Phase 7 |
| `--check` | 只检查 (Phase 7) |

## 📊 支持的课程

| 代码 | 课程 | Skill | 备注 |
|------|------|-------|------|
| `ml` | Machine Learning | `ai-learning-ml` | |
| `nlp` | NLP | `ai-learning-nlp` | |
| `mv` | Machine Vision | `ai-learning-mv` | 可能需 WSL+GPU |
| `cv` | Computer Vision | `ai-learning-cv` | 可能需 WSL+GPU |
| `dl` | Deep Learning | `ai-learning-dl` | 可能需 WSL+GPU |
| `rl` | RL | `ai-learning-rl` | 推荐 `/complete-assignment-rl` |

## 🚨 常见问题

| 问题 | 解决方案 |
|------|---------|
| CUDA OOM | 减 batch_size / 梯度累积 / 混合精度 |
| 不收敛 | 检查 lr / 数据预处理 / 初始化 |
| 路径错误 | 用相对路径或配置文件 |
| WSL 问题 | 检查 CUDA 驱动 / WSL2 版本 |

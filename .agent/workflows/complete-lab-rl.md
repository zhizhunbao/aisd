---
description: Complete RL course lab/assignment - specialized workflow for Reinforcement Learning
---

# 🤖 RL 课程作业完成工作流 (RL Lab Workflow)

## ⚖️ 执行协议 (Execution Protocol)
为保证执行的确定性，Agent 必须严格遵守以下串行流程，禁止跨阶段执行。

---

## Phase 1: 环境构建协议 (Env Construction)
**核心指令**: 通过 `learning-code_generation` 与 `dev-code_comment` 技能定义仿真环境。

1.  **执行目标**: 创建标准的 Gymnasium 环境类。
2.  **强制产出**: 
    - 源码目录: `src/<userid>_<env_name>/`
    - 定义文件: `pyproject.toml`
3.  **确定性验证**: 运行 `pip install -e` 必须成功，且 `gym.make` 能够无误加载该命名空间。
4.  **状态准入**: 只有在环境能被成功初始化后，方可进入 Phase 2。

---

## Phase 2: 智能体演化协议 (Agent Evolution)
**核心指令**: 调用算法生成技能。

1.  **执行目标**: 实现 Q-Learning 等目标算法。
2.  **强制产出**: `<userid>_lab[n]_agent.py`。
3.  **确定性验证**: 必须使用 `null_agent.py` 验证环境与智能体的输入输出 Tensor 形状匹配。
4.  **状态准入**: 验证脚本通过后，方可进入 Phase 3。

---

## Phase 3: 观测与文档协议 (Observability)
**核心指令**: 调用 `learning-notebook_conversion` 技能。

1.  **执行目标**: 自动化实验数据捕获与格式转换。
2.  **强制产出**: 
    - 性能图表: `src/lab[n]_images/` 目录下的 PNG。
    - 交互文档: 与 `.py` 同步的 `.ipynb`。
3.  **确定性验证**: Notebook 必须包含运行后的 Output 单元格。
4.  **状态准入**: 产出物文件路径与命名完全匹配合约后，方可进入 Phase 4。

---

## Phase 4: 交割与打包协议 (Delivery/Packaging)
**核心指令**: 调用 `dev-package_submission` 技能。

1.  **执行目标**: 产出符合课程提交标准的压缩包。
2.  **自动预处理**: 
    - 运行清理逻辑（移除 `__pycache__` 等）。
    - 检查并剔除任何名为 `venv` 或以 `.` 开头的隐藏环境目录。
3.  **强制产出**: `<userid>_lab[n]_submission.zip`。
4.  **最终断言**: 校验压缩包根目录是否为 `src`，验证所有 Phase 要求的文件是否齐全。

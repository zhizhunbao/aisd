---
name: code-comment
description: 中英文双语代码注释规范。Use when (1) 为代码添加注释, (2) 需要中英双语文档, (3) 规范化代码注释格式, (4) 学习类项目代码注释
---

# Code Comment (Bilingual)

## Objectives

- Add bilingual (Chinese & English) comments to code
- Follow consistent comment formatting rules
- Explain complex logic with reasons
- Maintain clear code documentation

## Comment Rules Overview

| Location | Language | Format |
|----------|----------|--------|
| File-level docstring | English only | Standard docstring |
| Function docstring | Chinese + English | Block format with `----` separator |
| Inline comments | Chinese + English | Chinese first, then `#`, then English |
| Section dividers | English only | `# ====== Step X: Description ======` |

## 1. File-level Docstring (English Only)

```python
"""
Lab 2: Q-Learning Agent for Cliff Walking
Student ID: 041107730
Implements Q-Learning using Bellman equation: Q(s,a) = r + γ * max Q(s',a')
Modified from Hybrid Activity 1 to solve the Cliff Walking problem.
"""
```

## 2. Function Docstring (Bilingual Block Format)

Chinese block first, separator `----`, then English block:

```python
def train(env, episodes: int = 50, gamma: float = 0.9) -> list:
    """
    训练Q-Learning智能体

    参数:
        env: 环境实例
        episodes: 训练回合数
        gamma: 折扣因子，决定未来奖励的重要性

    返回:
        qtable: 训练好的Q表

    ----

    Train Q-Learning agent

    Args:
        env: Environment instance
        episodes: Number of training episodes
        gamma: Discount factor, determines importance of future rewards

    Returns:
        qtable: Trained Q-table
    """
```

## 3. Inline Comments (Bilingual Grouped)

Chinese comments first (can be multiple lines), then empty comment `#`, then English:

```python
# 初始化Q表，使用随机值
# 原因：随机初始化可以打破对称性，帮助探索不同的状态-动作组合
# 每个状态有4个动作（左、右、上、下），总共有 rows * cols 个状态
#
# Initialize Q-table with random values
# Reason: Random initialization breaks symmetry and helps explore different state-action pairs
# Each state has 4 actions (left, right, up, down), total of rows * cols states
qtable = [
    [random.random() for _ in range(env.actions())]
    for _ in range(env.states())
]
```

### Simple Inline Comment

```python
# 增加步数计数
#
# Increment step count
steps += 1
```

## 4. Section Dividers (English Only)

Use for main function or logical sections:

```python
def main():
    # ==================== Step 1: Print Program Header ====================
    # 打印程序标题
    #
    # Print program header
    print("=" * 50)

    # ==================== Step 2: Create Environment ====================
    # 创建悬崖行走环境
    #
    # Create Cliff Walking environment
    env = GridEnv(size=12)

    # ==================== Step 3: Set Hyperparameters ====================
    # 设置超参数
    #
    # Set hyperparameters
    EPISODES = 50
    GAMMA = 0.9
```

## 5. Complex Logic Comments

For complex logic, add explanation and reason:

```python
# 使用贝尔曼方程更新Q表
# Q(s,a) = r + γ * max_a' Q(s',a')
# 这里alpha=1，即完全替换旧值（不使用加权平均）
# 完整公式应为：Q(s,a) = Q(s,a) + α * [r + γ * max Q(s',a') - Q(s,a)]
# 当α=1时，简化为：Q(s,a) = r + γ * max Q(s',a')
#
# Update Q-table using Bellman equation
# Q(s,a) = r + γ * max_a' Q(s',a')
# Here alpha=1, meaning completely replace old value (no weighted average)
# Full formula should be: Q(s,a) = Q(s,a) + α * [r + γ * max Q(s',a') - Q(s,a)]
# When α=1, simplifies to: Q(s,a) = r + γ * max Q(s',a')
qtable[state][action] = reward + gamma * max(qtable[next_state])
```

## 6. Import Comments

Group imports and add bilingual comment:

```python
# 导入操作系统模块，用于清屏操作
# 导入时间模块，用于控制动画速度
# 导入随机模块，用于探索策略中的随机动作选择
#
# Import os module for screen clearing operations
# Import time module for controlling animation speed
# Import random module for random action selection in exploration strategy
import os
import time
import random
```

## 7. Entry Point Comment

```python
# 程序入口点
# 运行主函数
#
# Program entry point
# Run main function
if __name__ == "__main__":
    main()
```

## Comment Checklist

Before finishing:

- [ ] File-level docstring is English only
- [ ] All function docstrings have bilingual blocks with `----` separator
- [ ] All inline comments have Chinese first, `#`, then English
- [ ] Section dividers are English only
- [ ] Complex logic has explanation and reason
- [ ] Every code block has comments
- [ ] Import statements have grouped comments

## Quick Reference

```
File docstring:     English only
Function docstring: 中文块 ---- English block
Inline comment:     # 中文
                    #
                    # English
Section divider:    # ====== English Only ======
```

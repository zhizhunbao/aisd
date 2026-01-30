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
| Function docstring | Chinese + English | Two-line format: Chinese first line, English second line |
| Inline comments | Chinese + English | Chinese line, then English line, above code |
| Code spacing | - | Blank line between code blocks |

## 1. File-level Docstring (English Only)

```python
"""
Lab 2: Q-Learning Agent for Cliff Walking
Student ID: 041107730
Implements Q-Learning using Bellman equation: Q(s,a) = r + γ * max Q(s',a')
Modified from Hybrid Activity 1 to solve the Cliff Walking problem.
"""
```

## 2. Function Docstring (Two-Line Bilingual Format)

Two lines with Chinese first line, English second line:

```python
def train(env, episodes: int = 50, gamma: float = 0.9) -> list:
    """训练Q-Learning智能体
    Train Q-Learning agent"""

def reset() -> tuple:
    """重置环境到初始状态
    Reset environment to initial state"""
```

**Rules:**
- Use triple quotes `"""`
- Chinese description on first line
- English description on second line
- Keep it concise, no blank line between Chinese and English
- No parameter or return value details in docstring

## 3. Inline Comments (Line-by-Line Bilingual)

Chinese comment immediately followed by English comment, placed ABOVE code:

```python
# 初始化Q表，使用随机值
# Initialize Q-table with random values
qtable = [[random.random() for _ in range(env.actions())] for _ in range(env.states())]

# 增加步数计数
# Increment step count
steps += 1
```

**Rules:**
- Comment goes ABOVE the code, NOT beside it
- Chinese line first, English line immediately after (no blank line between)
- Blank line AFTER comments and before next code block
- For complex logic, add explanation:

```python
# 使用贝尔曼方程更新Q表：Q(s,a) = r + γ * max Q(s',a')
# Update Q-table using Bellman equation: Q(s,a) = r + γ * max Q(s',a')
qtable[state][action] = reward + gamma * max(qtable[next_state])

# 衰减探索率，随着学习进行减少随机探索
# Decay exploration rate, reduce random exploration as learning progresses
epsilon -= decay * epsilon
```

## 4. Code Spacing

**IMPORTANT:** Always add blank lines between code blocks:

```python
def main():
    # 打印程序标题
    # Print program header
    print("=" * 50)

    # 创建悬崖行走环境
    # Create Cliff Walking environment
    env = GridEnv(size=12)

    # 设置超参数
    # Set hyperparameters
    EPISODES = 50
    GAMMA = 0.9
```

**Rules:**
- Blank line after each code block
- No blank line between Chinese and English comments
- Comments always above code, never beside it

## 5. Complex Logic Comments

For complex logic with multiple lines, keep Chinese and English paired line-by-line:

```python
# 使用贝尔曼方程更新Q表：Q(s,a) = r + γ * max Q(s',a')
# Update Q-table using Bellman equation: Q(s,a) = r + γ * max Q(s',a')
# 这里alpha=1，即完全替换旧值（不使用加权平均）
# Here alpha=1, meaning completely replace old value (no weighted average)
# 完整公式应为：Q(s,a) = Q(s,a) + α * [r + γ * max Q(s',a') - Q(s,a)]
# Full formula should be: Q(s,a) = Q(s,a) + α * [r + γ * max Q(s',a') - Q(s,a)]
qtable[state][action] = reward + gamma * max(qtable[next_state])

# 检查是否掉下悬崖（底行，第1-10列）
# Check if agent fell off cliff (bottom row, columns 1-10)
# 原因：悬崖行走问题的核心机制，大负奖励惩罚掉入悬崖
# Reason: Core mechanism of Cliff Walking problem, large negative reward penalizes falling
if self.y == 3 and 1 <= self.x <= 10:
    reward = -100
```

## 6. API Parameter Comments

When calling APIs with multiple parameters (e.g. OpenCV, scikit-learn), explain **what each parameter does** and **why that value was chosen**, not just restate the parameter name.

```python
# ❌ BAD - Just restating parameter names (读完还是不知道在做什么)
# 参数：127 是阈值，255 是最大值，THRESH_BINARY 是二值化模式
# Parameters: 127 is threshold, 255 is max value, THRESH_BINARY is binarization mode
_, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# ✅ GOOD - Explain what each value actually does
# 参数：127 是明暗分界线（亮度 > 127 的像素变白，≤ 127 的变黑），
#       255 是"变白"后赋予的像素值（纯白），
#       THRESH_BINARY 表示输出只有纯黑(0)和纯白(255)两种结果
# Parameters: 127 is the brightness cutoff (pixels > 127 become white, ≤ 127 become black),
#       255 is the value assigned to "white" pixels (pure white),
#       THRESH_BINARY means output has only two values: black(0) and white(255)
_, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
```

```python
# ❌ BAD - Parameter names without meaning
# 参数：[img] 是源图，[i] 是通道索引，None 是掩码，[256] 是分箱数
# Parameters: [img] is source, [i] is channel index, None is mask, [256] is bin count

# ✅ GOOD - Explain purpose and effect of each value
# 参数：[img] 将原图包在列表里传入（API 支持同时处理多张图），
#       [i] 指定计算第几个通道（0=蓝, 1=绿, 2=红），
#       None 表示不使用掩码（即统计整幅图而非局部区域），
#       [256] 表示将像素值分成 256 个柱子来统计（每个亮度值一个柱子），
#       [0, 256] 限定只统计亮度在 0~255 之间的像素
# Parameters: [img] wraps image in a list (API supports multiple images at once),
#       [i] specifies which channel to compute (0=Blue, 1=Green, 2=Red),
#       None means no mask (count all pixels, not just a sub-region),
#       [256] splits pixel values into 256 bins (one bin per intensity level),
#       [0, 256] only counts pixels with intensity between 0 and 255
hist = cv2.calcHist([img], [i], None, [256], [0, 256])
```

**Rules:**

- Explain what the value **does** (effect), not just what it **is** (name)
- For numeric values: explain why this specific number was chosen, and what changing it would do
- For enum/flag values: explain the behavior it selects
- For optional values like `None`: explain what it means to omit it
- Use `#       ` (7 spaces) for continuation lines to align with the first parameter description
- Keep Chinese and English paired, same as inline comments

## 7. Import Comments

Add bilingual comments above imports:

```python
# 导入抽象基类模块，用于定义环境接口
# Import abstract base class module for defining environment interface
import abc

# 导入操作系统、时间和随机模块
# Import os, time and random modules
import os
import time
import random
```

## 8. Entry Point Comment

```python
# 程序入口点，运行主函数
# Program entry point, run main function
if __name__ == "__main__":
    main()
```

## Comment Checklist

Before finishing:

- [ ] File-level docstring is English only
- [ ] All function docstrings use two-line format: Chinese first line, English second line
- [ ] All inline comments have Chinese line immediately followed by English line
- [ ] Comments are placed ABOVE code, not beside it
- [ ] No blank line between Chinese and English lines (in both docstrings and comments)
- [ ] Blank line between each code block
- [ ] Complex logic has explanation and reason
- [ ] API parameters explain what each value does, not just its name
- [ ] Every code block has comments
- [ ] Import statements have bilingual comments

## Quick Reference

```python
# File docstring (English only)
"""
Lab 2: Q-Learning Agent
Implements Q-Learning algorithm
"""

# Function docstring (two-line bilingual)
def train(env):
    """训练Q-Learning智能体
    Train Q-Learning agent"""

# Inline comment (line-by-line bilingual, above code)
# 初始化Q表，使用随机值
# Initialize Q-table with random values
qtable = [[random.random() for _ in range(env.actions())] for _ in range(env.states())]

# 增加步数计数
# Increment step count
steps += 1
```

## Key Rules Summary

1. **Function docstrings**: Two lines - Chinese first line, English second line (NO blank line between)
2. **Inline comments**: Chinese line, English line, then code (NO blank line between Chinese/English)
3. **Comment placement**: Always ABOVE code, never beside it
4. **Code spacing**: Blank line after each code block
5. **No blank line**: Between Chinese and English lines (both in docstrings and comments)
6. **API parameters**: Explain what each value DOES and WHY, not just restate parameter names

## Complete Example

```python
"""
Lab 2: Q-Learning Agent for Cliff Walking
Student ID: 041107730
Implements Q-Learning using Bellman equation
"""

# 导入抽象基类模块，用于定义环境接口
# Import abstract base class module for defining environment interface
import abc

# 导入操作系统、时间和随机模块
# Import os, time and random modules
import os
import time
import random


class Env(abc.ABC):
    """环境抽象基类
    Environment abstract base class"""

    @abc.abstractmethod
    def actions(self) -> int:
        """返回动作空间的大小
        Return the size of action space"""
        raise NotImplementedError()


def train(env, episodes: int = 50, gamma: float = 0.9) -> list:
    """训练Q-Learning智能体
    Train Q-Learning agent"""

    # 初始化Q表，使用随机值
    # Initialize Q-table with random values
    qtable = [[random.random() for _ in range(env.actions())] for _ in range(env.states())]

    # 训练主循环，遍历所有回合
    # Main training loop, iterate through all episodes
    for episode in range(episodes):
        # 重置环境，获取初始状态
        # Reset environment and get initial state
        state = env.reset()

        # 使用贝尔曼方程更新Q表
        # Update Q-table using Bellman equation
        qtable[state][action] = reward + gamma * max(qtable[next_state])

    # 返回训练好的Q表
    # Return the trained Q-table
    return qtable


# 程序入口点，运行主函数
# Program entry point, run main function
if __name__ == "__main__":
    main()
```

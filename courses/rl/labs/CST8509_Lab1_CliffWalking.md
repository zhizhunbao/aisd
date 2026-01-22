# CST8509 Lab1 CliffWalking

## Overview

Q-learning is a popular Temporal Difference method for Reinforcement Learning. In this lab, you will follow existing examples of a Q-learning implementation, and then modify one of those implementations to solve the CliffWalking grid world as described in the Sutton textbook on Page 132.

When you have completed this lab, you will know how to

- Explain how Temporal Difference learning (specifically Q-learning) works
- Apply Q-Learning to various grid world examples.

```
📝 笔记:
- Q-learning 是时序差分 (TD) 学习方法
- 本实验：修改示例代码实现 Cliff Walking 问题（教材 P132）
- 核心公式：Q(s,a) ← Q(s,a) + α[r + γ max Q(s',a') - Q(s,a)]
```

## Instructions

Complete Hybrid Activity 1: this is the starting tutorial for this lab exercise. You don't need to create an account – close that window if it appears. The URL is [https://medium.com/data-science/math-of-q-learning-python-code-5dcbdc49b6f6](https://medium.com/data-science/math-of-q-learning-python-code-5dcbdc49b6f6) 

This tutorial explains the Bellman equation, which we will revisit in class in the coming weeks. Overall, this tutorial forms the basis for our work with Q-learning grid world examples.

```
📝 笔记:
- 先完成 Hybrid Activity 1 教程（Medium 文章）
- 重点理解 Bellman 方程
- 无需创建账号
```

Your task is to

- After Hybrid Activity 1, download the provided source code files, and make these changes:
	- Rename medium_qlearning_rl.py to **<your_algonquin_id>_lab2_qlearning_agent.py**
	- Rename medium_qlearning_env.py to **<your_algonquin_id>_lab2_environment.py**
	- Change the import at the top of **<your_algonquin_id>_lab2_qlearning_agent.py** to reflect the name change of the environment module.

```
📝 笔记:
- 用你的 Algonquin ID 替换文件名
- 修改 import 语句匹配新文件名
```

- Read the python code. You should have an understanding of how the code works before you run it. 
- Run the example code, and notice that the agent gets better and better at traversing the simple grid world.

```
📝 笔记:
- 先理解代码再运行
- 观察 agent 学习过程的改进
```

- Make changes to the example code solve a different grid world problem, the Cliff Walking problem on Page 132 of the Sutton Textbook, according to these instructions:
	- Do not use an existing solution of the Cliff Walking world – create a new solution by changing the Hybrid 1 example grid world according to the points below.
	- Copy **<your_algonquin_id>_lab2_environment.py** to **<your_algonquin_id>_lab2_cliff_env.py**
	- As you make the following changes to **<your_algonquin_id>_lab2_cliff_env.py**, add a comment in your own words to explain any changes you make.

	- Do not use an existing solution of the Cliff Walking world – create a new solution by changing the Hybrid 1 example grid world according to the points below.
	- Copy **<your_algonquin_id>_lab2_environment.py** to **<your_algonquin_id>_lab2_cliff_env.py**
	- As you make the following changes to **<your_algonquin_id>_lab2_cliff_env.py**, add a comment in your own words to explain any changes you make.

```
📝 笔记:
- Cliff Walking: 4x12 网格，底部中间 10 格是悬崖
- 起点左下角，终点右下角
- 掉入悬崖返回起点，奖励 -100
```

Under **#Hyperparameters** add **alpha=1** step-size hyperparameter to be discussed during your demonstration (it won't be used by your code at this point)

```
📝 笔记:
- 添加 alpha=1（学习率），演示时讨论
```

Change the **Env** class initializer to represent the shape of the Cliff Walking world, and introduce a "cliff" attribute (True/False) to indicate whether the agent fell over the cliff while performing the last action

```
📝 笔记:
- 修改网格形状为 4x12
- 添加 cliff 属性（布尔值）标记是否掉入悬崖
```

Change the **step** method according to the Cliff Walking world. If that step results in falling off the cliff, the **cliff** attribute should be set to **True**; otherwise, the **cliff** attribute should be **False**. Make sure the resulting state is correct if the agent falls off the cliff.

```
📝 笔记:
- 修改 step 方法判断是否掉入悬崖
- 掉入悬崖：cliff=True，返回起点
```

Change the **reward** calculation to match the Cliff Walking world described on Page 132 of the textbook.

```
📝 笔记:
- 掉入悬崖：-100
- 每步移动：-1
```

Change the **render** method to indicate the cliff part of the grid (the ten grey squares) as X's

```
📝 笔记:
- 用 'X' 标记悬崖区域
```

Change the "epoch" term to our preferred term for this context: "episode"

```
📝 笔记:
- 将 "epoch" 改为 "episode"
```

Print the Return (total accumulated reward) under the number of steps when the goal is reached.

```
📝 笔记:
- 打印总回报（所有奖励之和）
```

## Submission

Submit a zip file containing (a folder of) all of the python source code files.

```
📝 笔记:
- 提交 zip 文件，包含所有 Python 源代码
```

## Demonstration

Show your lab instructor your running Cliff World solution.
Be prepared to discuss briefly some aspects of your changes you made to the original code.

```
📝 笔记:
- 演示运行的 Cliff Walking 解决方案
- 准备讨论代码修改（特别是 alpha 参数）
```

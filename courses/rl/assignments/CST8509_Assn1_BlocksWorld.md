# CST8509 Assignment 1 Blocks World

## Note

This is an individual assignment.  You are not allowed to work together with anyone to produce any portion of your solution.  You are not allowed let other students view your solution, and you are not allowed to view any portion of another student’s solution.  If your solution is influenced by a resource like ChatGPT or a web page, be sure to acknowledge that resource in your submission.

> **📝 笔记:**
> 
> **个人作业要求:**
> 
> - 只能独立完成，不可协作
> - 不得查看或让他人查看你的解答
> - 使用 ChatGPT 或网页需注明来源
> 
> **💡 提示:** 提交时写明引用来源

## Overview

We continue to explore Reinforcement Learning by creating a Blocks World environment and training a variety of algorithms on the environment.  This will increase your familiarity with Gymnasium environments and Q-learning, as well as implementing and evaluating Stable-Baselines3 algorithms on arbitrary environments.

When you have completed this assignment, you will know how to

- Convert a Prolog model into a Gymnasium environment `blocksworld_env/BlocksWorld-v0` (initially without information about the target state)
- Implement Q-Learning on the BlocksWorld environment
- Enhance the BlocksWorld environment to include the target state.
- Apply a selection of Stable-Baselines3 algorithms to your Gymnasium environment

> **📝 笔记:**
> 
> **作业目标:**
> 
> - 构建 BlocksWorld 的 Gymnasium 环境
> - 实现与验证 Q-learning
> - 扩展环境以包含目标状态
> - 试跑 Stable-Baselines3 算法
> 
> **💡 提示:** 先保证环境可跑再做算法对比

## Instructions

This work can be completed on your loaner laptop.  You might also be able to use your Ubuntu 22.04 virtual machine, or WSL2 (with GUI support), etc, but if you have issues with those alternatives, it is easiest to use the loaner laptop.

Visit this link to set up your GitHub repository with starter code for this assignment.  Please click on **your own name only**.  Scroll down the list to find your name, and do not “skip to the next step”.  If you accidentally click on someone else’s name, or have problems, please let me know.

[https://classroom.github.com/a/MwJ-OMHo](https://classroom.github.com/a/MwJ-OMHo)

See the Assignment 1 directory structure diagram below. Create a folder for the assignment, Assn1, and then create a python virtual environment in the Assn1 folder, and also clone your GitHub repository into the Assn1 folder.  The python virtual environment folder and the Git repository folder will be the only two items in the Assn1 folder for the duration of this Assignment.

Your loaner-laptop should still have key-access to your GitHub account, but if not, you’ll need to add key access (see CST8504\_Assign2\_Ros2\_Vision for key access instructions, or ask your lab instructor).

```bash
mkdir Assn1
cd Assn1
python3 -m venv pvenv
source pvenv/bin/activate  # activate the python environment for this assignment
git clone <your_repository_SSH>  # do this in folder Assn1
```

```text
Assn1/
├─pvenv/                                    # python virtual environment folder
├─bw-<your GitHub name>                     # your GitHub repository folder
    ├── .git                                # local git repository
    ├── A.png                               # image file of Block A (included in starter code)
    ├── B.png
    ├── C.png
    .                                       # other files from starter code
    .
    .
    ├── screen.py                           # included in starter code
    ├── <python_file1>.py                   # python file you add for your q-learning agent
    ├── <python_file2>.py                   # python file you add for one StableBaselines3 agent
    ├── <python_file3>.py                   # python file you add for second StableBaselines3 agent
    ├── <Algonquin_userid>_blocksworld_env  # folder where you copied starter environment
        ├── blocksworld_env                 # gymnasium_env you renamed to blocksworld_env
        │   ├── envs
        │   │   ├── blocks_world.py
        │   │   ├── blocks_world_target.py
        │   │   └── __init__.py
        │   ├── __init__.py
        │   └── wrappers
        │       ├── clip_reward.py
        │       ├── discrete_actions.py
        │       ├── __init__.py
        │       ├── reacher_weighted_reward.py
        │       └── relative_position.py
        ├── LICENSE
        ├── pyproject.toml
        └── README.md
```

   > **📝 笔记:**
   > 
   > **环境与仓库准备:**
   > 
   > - 优先使用借用笔记本完成
   > - 通过 GitHub Classroom 创建仓库
   > - 按目录结构建立 `Assn1` 与虚拟环境
   > - 仓库与虚拟环境仅保留两项
   > 
   > **💡 提示:** SSH key 若失效需重新配置

## Prolog Blocks World

Install swi-prolog on your development machine:

```bash
sudo apt install swi-prolog
```

Ensure you can run the provided Prolog model of the Blocks World.  For this assignment, we will launch any python (or prolog) program from inside the GitHub repository folder.  For example:

```bash
cd bw-<YourGitHubName>   # this is the starter repository
swipl blocks_world.pl
```

```text
Welcome to SWI-Prolog (threaded, 64 bits, version 8.4.1)
SWI-Prolog comes with ABSOLUTELY NO WARRANTY. This is free software.
Please run ?- license. for legal details.
For online help and background, visit https://www.swi-prolog.org
For built-in help, use ?- help(Topic). or ?- apropos(Word).

?- on(a,A,[]),on(b,B,[]),on(c,C,[]).
A = 1,
B = 3,
C = a ;
false.
?-
```

> **📝 笔记:**
> 
> **Prolog 安装与验证:**
> 
> - 安装 `swi-prolog`
> - 在仓库目录运行 `swipl blocks_world.pl`
> - 通过示例查询验证 Prolog 正常工作
> 
> **💡 提示:** 运行路径应在仓库根目录

### Implement blocksworld\_env/BlocksWorld-v0

Similarly to the process you followed in Lab 2, refer to the notes at the URL below to copy/rename the GridWorld-v0 environment, but in our desired package (`blocksworld_env` instead of `gymnasium_env`) with our desired name (`blocks_world.py` and `BlocksWorld-v0` instead of `grid_world.py` and `GridWorld-v0`).  In later steps, you will make the changes to transform BlocksWorld to be the desired blocks environment (at this step it has the blocks name but it is still a grid world).  The location of the Gymnasium environment python file you create will be

`Assn1/bw-<yourRepository>/<algonquin_id>_blocksworld_env/blocksworld_env/envs/blocks_world.py`

Here’s the documentation you need:

[https://gymnasium.farama.org/tutorials/gymnasium\_basics/environment\_creation/](https://gymnasium.farama.org/tutorials/gymnasium_basics/environment_creation/)

**Notes**:

1. Remember to install the new package into your python virtual environment (first, cd to the directory that contains pyproject.toml):

   ```bash
   pip install -e .
   ```

   The “-e” option makes the source code editable in place, so you can change the environment without having to re-install it

   Notes:
   > **📝 笔记:**
   > 
   > **可编辑安装 (editable install):**
   > 
   > - 使用 `pip install -e .` 进行可编辑安装
   > - 修改源码后无需重复安装
   > 
   > **💡 提示:** 先确保当前目录包含 `pyproject.toml`

2. Using the “null agent” from Lab 2,  do a test run of your renamed environment from its new package, using its new name.  It will be called BlocksWorld-v0, but at this stage it will behave exactly like GridWorld-v0.  When this is confirmed, continue reading these notes on how to change your environment into the true BlocksWorld

   Notes:
   > **📝 笔记:**
   > 
   > **环境验证:**
   > 
   > - 使用“null agent”验证新包与新名称可运行
   > - 此阶段行为应与 GridWorld-v0 一致
   > 
   > **💡 提示:** 先确认运行无误再继续修改

3. `blocks_world.py` imports:  need to bring in the Prolog server, and the PyGame-based Display class.  These notes are for `swiplserver`.

   ```python
   import gymnasium as gym
   from gymnasium import spaces
   import pygame
   from screen import Display
   from swiplserver import PrologMQI, PrologThread
   import numpy as np
   ```

   Notes:
   > **📝 笔记:**
   > 
   > **依赖导入:**
   > 
   > - 引入 Gymnasium (gymnasium) 与空间定义 (spaces)
   > - 引入 PyGame (pygame) 与显示类 `Display`
   > - 引入 Prolog 接口 (swiplserver) 与数值库 (numpy)
   > 
   > **💡 提示:** 先保证依赖可用再运行

4. `blocks_world.py` constructor changes to existing constructor code:
   a. **size** parameter will not be used for now, but no change is necessary

      Notes:
      > **📝 笔记:**
      > 
      > **尺寸参数:**
      > 
      > - 此阶段 `size` 暂不使用
      > - 无需修改已有参数定义
      > 
      > **💡 提示:** 保持原参数以便后续扩展

   b. Add this code to run the Prolog interpreter and load the blocks world.  Note that this code assumes Python scripts (example `<python_file1>.py` in the above hierarchy) will be run from the folder that contains `blocks_world.pl` and `screen.py`.  Notice how we run a query with `prolog_thread.query()`, passing it our query as a string but we don’t end it with a period.  The variable **result** should be set to true in this case.

      ```python
      self.mqi = PrologMQI()
      self.prolog_thread = self.mqi.create_thread()
      result = self.prolog_thread.query('[blocks_world]')
      ```

      Notes:
      > **📝 笔记:**
      > 
      > **Prolog 启动与加载:**
      > 
      > - 创建 MQI 与线程 (PrologMQI / create_thread)
      > - 使用 `query('[blocks_world]')` 加载模型
      > 
      > **💡 提示:** 查询字符串不需要句号

   Notes:
   > **📝 笔记:**
   > 
   > **构造器阶段:**
   > 
   > - 主要完成 Prolog 初始化与基础加载
   > - 为后续状态/动作映射打基础
   > 
   > **💡 提示:** 先保证加载成功再继续

   c. Set up a dictionary to convert Prolog state names returned by Prolog into integers.  Read the blocks\_world.pl file to find the query that will return all of the possible states, and in blocks\_world.py use prolog\_thread.query() to run that query.  The result returned to Python this time will not be simple true or false, but will be a list of dictionaries, like this

   ```text
   [{'State':'bc2'}, {'State':'bc3'}…,…]
   ```

   Use dictionary comprehension with a for clause on “enumerate” of this result to construct the needed dictionary.  The resulting dictionary should be like

   ```text
   {'bc2':0, 'bc3':1, …,…}
   ```

   In this case State “bc2” from Prolog will be Python State 0, “bc3” will be Python State 1, etc.

   Notes:
   > **📝 笔记:**
   > 
   > **状态映射:**
   > 
   > - 通过 Prolog 查询获取所有状态
   > - 用 `enumerate` 构建“状态名 -> 整数”字典
   > - 状态字符串与整数一一对应
   > 
   > **💡 提示:** 确认查询返回为字典列表

   d. Set up a dictionary to convert action numbers into Prolog actions (add python comments to this code to prove you have read and understood it):

   ```python
   self.actions_dict = {}
   result = self.prolog_thread.query("action(A)")
   # result is like this, where the first action is move(a,b,c)
   # [{'A': {'args': ['a', 'b', 'c'], 'functor': 'move'}},...]
   for i, A in enumerate(result):
       action_string = A['A']['functor']
       first = True
       for arg in A['A']['args']:
           if first:
               first = False
               action_string += '('
           else:
               action_string += ','
           action_string += str(arg)
       action_string += ')'
       self.actions_dict[i] = action_string
   ```

   Notes:
   > **📝 笔记:**
   > 
   > **动作映射:**
   > 
   > - 查询 `action(A)` 得到动作结构
   > - 将 functor 与 args 组合为动作字符串
   > - 建立“动作编号 -> 动作字符串”字典
   > 
   > **💡 提示:** 保留注释说明理解过程

   e. Change the observation space from a Dictionary with agent and target components and define your observation space as a simple Discrete space of integers, using the length of your dictionary from Step c above.

   Notes:
   > **📝 笔记:**
   > 
   > **观测空间:**
   > 
   > - 用离散空间 (Discrete) 表示状态
   > - 空间大小来自状态字典长度
   > 
   > **💡 提示:** 观测需与状态映射一致

   f. Define your action space as a simple Discrete space of integers.

   Notes:
   > **📝 笔记:**
   > 
   > **动作空间:**
   > 
   > - 动作空间同样设为离散 (Discrete)
   > - 大小与动作字典一致
   > 
   > **💡 提示:** 确保动作编号可映射到动作字符串

   g. Store an initial starting state of the blocks (an integer) which can simply be the first state in your dictionary.  Similarly for the target state which is also an integer.  Your state dictionary converts state strings to integers, and to convert state integers to state strings, you can use this code (adapt to the actual names of your variables):

   ```python
   list(self.states_dict.keys())[list(self.states_dict.values()).index(self.state)]
   ```

   Notes:
   > **📝 笔记:**
   > 
   > **初始状态:**
   > 
   > - 起始状态与目标状态都用整数表示
   > - 提供整数到字符串的反向转换方法
   > 
   > **💡 提示:** 反查需基于同一状态字典

   h. If the render\_mode is “human”, initialize the PyGame display:

    ```python
    self.display = Display()
    ```

    This makes self.display an instance of the Display class in screen.py.  More information on the display is given in the notes about the render() method below.

   Notes:
   > **📝 笔记:**
   > 
   > **渲染初始化:**
   > 
   > - `render_mode` 为 human 时创建 `Display`
   > - 用于后续可视化更新
   > 
   > **💡 提示:** 仅在需要渲染时初始化

   i. Remove any remaining grid\_world code that doesn’t make sense for the blocks world.

   Notes:
   > **📝 笔记:**
   > 
   > **六位状态生成:**
   > 
   > - 将 `state/1` 扩展为六位状态
   > - 由 Agent 与 Target 两个三位状态拼接
   > 
   > **💡 提示:** 先保留 `state_helper/1` 生成三位状态

5. Reset method changes to existing Reset method:
    a. Randomly set a new target state (an integer).  If the screen self.display is set, then set the attribute variable **self.display.target** to the state string of the randomly generated target.  See above for the code that translates from state integers to state strings.

       Notes:
      > **📝 笔记:**
      > 
      > **目标状态:**
      > 
      > - 重置时随机生成目标状态（整数）
      > - 同步更新 `self.display.target`
      > 
      > **💡 提示:** 需要整数转字符串的映射

    b. Issue the Prolog query to reset.

       Notes:
      > **📝 笔记:**
      > 
      > **重置查询:**
      > 
      > - 调用 Prolog 重置谓词
      > - 确保环境回到初始状态
      > 
      > **💡 提示:** 先重置再读取状态

    c. Issue the Prolog query to retrieve the current state.  Assuming you used a variable named “State” in your Prolog query, and you put the result of this query into **result**, then the state string in python is result[0]['State']

       Notes:
      > **📝 笔记:**
      > 
      > **当前状态读取:**
      > 
      > - 查询返回字典列表
      > - 取 `result[0]['State']` 作为状态字符串
      > 
      > **💡 提示:** 注意变量名需一致

    d. Remove any remaining grid\_world code that doesn’t make sense for the blocks world.

       Notes:
      > **📝 笔记:**
      > 
      > **清理旧逻辑:**
      > 
      > - 删除与 BlocksWorld 不相关的网格逻辑
      > - 保持新状态流程清晰
      > 
      > **💡 提示:** 避免遗留变量干扰

   Notes:
   > **📝 笔记:**
   > 
   > **Reset 汇总:**
   > 
   > - 重置目标与当前状态
   > - 通过 Prolog 同步环境状态
   > 
   > **💡 提示:** 先设目标再读状态

6. Step method changes to existing Step method:
    a. Issue a Prolog query to prolog predicate **step**/1,  passing it the action string (use your action dictionary to convert action integers to action strings).

       Notes:
      > **📝 笔记:**
      > 
      > **动作执行:**
      > 
      > - 调用 Prolog 的 `step/1` 谓词
      > - 用动作字典把编号转为动作字符串
      > 
      > **💡 提示:** 动作编号必须可映射

    b. If the step/1 predicate returns non-false, then use a prolog query to retrieve the current state as before, and the reward is -1.  If the step/1 predicate returns false, that means the action is not possible, and the reward should be -10

       Notes:
      > **📝 笔记:**
      > 
      > **可执行性与奖励:**
      > 
      > - 可执行则读取新状态并奖励 -1
      > - 不可执行则奖励 -10
      > 
      > **💡 提示:** 用返回值判断可行性

    c. If done , the reward is 100

       Notes:
      > **📝 笔记:**
      > 
      > **完成奖励:**
      > 
      > - 终止时奖励设为 100
      > - 与终止条件保持一致
      > 
      > **💡 提示:** 先判断 done 再赋值

    d. You can experiment with different rewards later.

       Notes:
      > **📝 笔记:**
      > 
      > **奖励调参:**
      > 
      > - 允许后续调整奖励策略
      > - 当前仅为基线设置
      > 
      > **💡 提示:** 记录修改以便对比

   Notes:
   > **📝 笔记:**
   > 
   > **Step 汇总:**
   > 
   > - 执行动作并更新状态
   > - 根据可行性与终止设置奖励
   > 
   > **💡 提示:** 保持状态与奖励逻辑一致

7. Render method
    a. Assuming self.display.target is set to the three digit target string, then updating the display is just a matter of calling self.display.step(), passing it the three digit current state string (recall how to convert state integers to state strings).  For more information, find the step() method in screen.py and read the code.

       Notes:
      > **📝 笔记:**
      > 
      > **渲染更新:**
      > 
      > - 将当前状态字符串传给 `self.display.step()`
      > - 依赖目标状态字符串已设置
      > 
      > **💡 提示:** 先确认目标与当前状态字符串

   Notes:
   > **📝 笔记:**
   > 
   > **Render 汇总:**
   > 
   > - 渲染逻辑集中在 `Display.step()`
   > - 需要字符串形式状态输入
   > 
   > **💡 提示:** 状态映射需一致

8. Close method:
    a. Shut down the prolog server: self.mqi.stop()

       Notes:
       > **📝 笔记:**
       > 
       > **资源释放:**
       > 
       > - 调用 `self.mqi.stop()` 关闭 Prolog 服务
       > - 结束时释放相关资源
       > 
       > **💡 提示:** 与 `env.close()` 对应执行

    Notes:
   > **📝 笔记:**
   > 
   > **Close 汇总:**
   > 
   > - 关闭 Prolog 相关资源
   > - 清理环境占用
   > 
   > **💡 提示:** 避免后台线程残留

### Trial run with blocksworld\_env/BlocksWorld-v0

Use the following code as a “null agent” to see your BlocksWorld:

```python
import gymnasium as gym
import blocksworld_env

env = gym.make("blocksworld_env/BlocksWorld-v0", render_mode="human")
observation, info = env.reset()

for _ in range(1000):
    action = env.action_space.sample()  # agent policy that uses the observation and info
    observation, reward, terminated, truncated, info = env.step(action)
    if terminated or truncated:
        observation, info = env.reset()

env.close()
```

> **📝 笔记:**
> 
> **空代理测试:**
> 
> - 使用随机动作验证环境可运行
> - 终止或截断时重新 reset
> 
> **💡 提示:** 先确保渲染模式为 human

### Q-Learning with blocksworld\_env/BlocksWorld-v0

Copy and adapt your <algonquin\_id>\_lab2\_qlearning\_agent.py Q-learning agent from Lab 2 to <algonquin\_id>\_assn1\_qlearning\_agent.py and make it work with your new BlocksWorld-v0 environment.  Remember that the reset and step methods of the BlocksWorld-v0 environment both return an integer state/observation according to the notes above; whereas your Lab 2 environment returned a dictionary of states.

> **📝 笔记:**
> 
> **Q-Learning 迁移:**
> 
> - 复用 Lab 2 的 Q-learning 代码并适配新环境
> - 观测由字典变为整数状态
> 
> **💡 提示:** 先处理状态类型差异

Enhance your <algonquin\_id>\_assn1\_qlearning\_agent.py code to keep track of returns per episode and steps per episode, and plot graphs at the end.  Use “Original Hyperparameters” as the title of the plot. Take a screenshot, give it a meaningful name, and add it to a new folder, called **screenshots**, in your GitHub repository.

> **📝 笔记:**
> 
> **训练记录与截图:**
> 
> - 记录每个 episode 的回报与步数
> - 绘图标题使用 “Original Hyperparameters”
> - 截图保存到仓库中的 `screenshots` 文件夹
> 
> **提交要求:**
> 
> - 截图：保存到 `screenshots` 文件夹
> - 命名：使用有意义的文件名

Try some new values for the Q-learning hyperparameters and graph the results, indicating the hyper-parameter values in the plot title (or use an annotation/notes method).  Add at least three new screenshots to show you’ve tried three different sets of hyper-parameters besides the originals.

> **📝 笔记:**
> 
> **超参数对比:**
> 
> - 尝试多组超参数并绘图
> - 在标题或注释中标注超参数
> - 至少新增三张截图
> 
> **提交要求:**
> 
> - 截图：至少 3 张不同超参数结果

## blocksworld\_env/BlocksWorld-v1 with target as part of state

Enhance your system to work with 6-digit states instead of 3-digit states, by copying and modifying your blocks\_world.py file.  The additional three digits represent the target state.  The changes required are minimal (see Notes below)

Notes:

1. The main change is to make the Prolog **state/1** predicate generate all of the six digit states.  To do this, you can rename it to **state_helper/1** then add a new 6 digit **state/1** predicate:

   ```prolog
   state(State):-
     state_helper(Agent),   % three digit state
     state_helper(Target),  % another three digit state
     atomics_to_string([Agent,Target],State).    % together, they make a six digit state
   ```

   Notes:
   > **📝 笔记:**
   > 
   > **六位状态生成:**
   > 
   > - `state/1` 生成六位状态
   > - 由两个三位状态拼接得到
   > 
   > **💡 提示:** 保留 `state_helper/1` 生成三位状态
2. To generate a random target state upon reset, the Python environment code can still simply pick a random state from the whole state table, but take the last three characters as the target state.  In addition, Prolog will still return a three digit current state string, and the python environment needs to append the saved target string to get the 6 digit current state.   The state dictionary takes that 6 digit state and gives the corresponding integer state to give to the agent.

   Notes:
   > **📝 笔记:**
   > 
   > **目标拼接:**
   > 
   > - 目标从随机状态取后三位
   > - 当前状态三位 + 目标三位 -> 六位状态
   > 
   > **💡 提示:** 最终仍用字典映射为整数状态

### Use your environment with Stable-Baselines3

1. Still with your python virtual environment activated, install Stable-Baselines3:

   ```bash
   pip install stable-baselines3
   ```

   Notes:
   > **📝 笔记:**
   > 
   > **库安装:**
   > 
   > - 在虚拟环境中安装 Stable-Baselines3
   > - 为后续算法调用做准备
   > 
   > **💡 提示:** 确认在已激活环境中执行
2. Run the code for using the BlocksWorld-v0 environment (Slide 14 of CST8509\_03\_Gymnasium, change it to `import blocksworld_env`, and change to use `blocksworld_env/BlocksWorld-V1`).
   Notes:
   > **📝 笔记:**
   > 
   > **环境切换:**
   > 
   > - 将导入改为 `blocksworld_env`
   > - 环境名改为 `blocksworld_env/BlocksWorld-V1`
   > 
   > **💡 提示:** 与当前包名保持一致
3. Try your environment with the **DQN** and **PPO** algorithms.  We want to get the algorithms running, but we WILL NOT see better results than q-learning at this stage.
   Notes:
   > **📝 笔记:**
   > 
   > **算法试跑:**
   > 
   > - 运行 DQN 与 PPO 以验证流程
   > - 关注可运行性而非效果
   > 
   > **💡 提示:** 记录运行结果用于对比

### Submission

Commit to your GitHub repository often with meaningful commit messages, and it will be used instead of submitting code to Brightspace.  Since you’ve followed the directory structure pictured above, your python virtual environment folder IS NOT in your repository, but all of your new content is in your repository.

> **📝 笔记:**
> 
> **提交方式:**
> 
> - 通过 GitHub 提交记录代替 Brightspace 提交
> - 不提交虚拟环境目录
> 
> **提交要求:**
> 
> - 提交：使用有意义的 commit message

### Demonstration

Show your Gymnasium Environment BlocksWorld-v0 (without target state) working with a modified Lab2 q-learning agent.

Show graphs of returns and steps per episode with your modified Lab2 q-learning agent and different sets of hyper-parameters.

Show your BlocksWorld-v1 (with target state enhancement) working with a modified Lab2 q-learning agent.

Show your Gymnasium Environment working with an algorithm from Stable-Baselines3

Be prepared to answer questions about how your code works.

> **📝 笔记:**
> 
> **演示要求:**
> 
> - 展示 BlocksWorld-v0 + Q-learning
> - 展示回报/步数曲线与不同超参数截图
> - 展示 BlocksWorld-v1 + Q-learning
> - 展示 Stable-Baselines3 算法运行
> 
> **💡 提示:** 准备解释核心代码逻辑

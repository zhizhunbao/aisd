# Reinforcement Learning Quiz 7 – RL and Robotics

---

**Question 1** (1 point)
How can RL be applied to environments with huge (10²⁰+) state spaces?
RL 如何应用于巨大（10²⁰+）状态空间的环境？

A) Value Approximation methods with a set of weights can approximate the value function. / 值近似方法用一组权重来逼近价值函数。
B) Q calculations can translate large state spaces into smaller ones.
C) All of these answers.
D) Continuous actions can counter-act the effect of large state spaces.
E) None of these answers.

> **Answer**: A
> For huge state spaces, function approximation (e.g. neural networks) replaces the Q-table with parameterized weights.
> 对巨大状态空间，函数近似（如神经网络）用参数化权重替代 Q 表。

---

**Question 2** (1 point)
What is the basic idea behind Value Function Approximation?
值函数近似的基本思想是什么？

A) A ML model generates interaction samples for Q-Learning.
B) Experience from environment interaction is used as data to train weights of a function approximation. / 与环境交互的经验作为数据来训练近似函数的权重。
C) None of these answers.
D) Q-Learning creates a Q-table which then approximates a value function.
E) All of these answers.

> **Answer**: B
> Use real interaction experience as training data to fit a parameterized function that approximates $V$ or $Q$.
> 用真实交互经验作为训练数据，拟合参数化函数来近似 $V$ 或 $Q$。

---

**Question 3** (1 point)
What is an implication of continuous actions or states in RL?
连续动作或状态对 RL 意味着什么？

A) Discrete table-based Q-learning cannot be used.
B) Continuous space implies a very large number of different actions or states.
C) All of these answers. / 以上全部。
D) A value function approximation method is needed.
E) None of these answers.

> **Answer**: C
> Continuous spaces mean: Q-table is infeasible, the space is effectively infinite, and function approximation is required.
> 连续空间意味着：Q 表不可行、空间实际无限、需要函数近似。

---

**Question 4** (1 point)
What is the DQN algorithm?
什么是 DQN 算法？

A) DQN (Deep Q Network) uses a deep neural network to handle large or continuous state spaces. / DQN 用深度神经网络处理大规模或连续状态空间。
B) None of these answers.
C) DQN updates the Q-table as episodes progress.
D) All of these answers.
E) DQN updates the Q-table using only complete episodes.

> **Answer**: A
> DQN replaces the Q-table with a neural network to generalize across large state spaces. C/E still describe table-based approaches.
> DQN 用神经网络替代 Q 表以泛化大状态空间。C/E 仍在描述表格方法。

---

**Question 5** (1 point)
What is the PPO algorithm?
什么是 PPO 算法？

A) All of these answers.
B) PPO is the same as Q-Learning except Q-table updates after episode ends.
C) PPO is the same as Monte Carlo except Q-table updates before episode ends.
D) None of these answers.
E) PPO (Proximal Policy Optimization) can handle large or continuous action and/or state spaces. / PPO 能处理大规模或连续的动作和/或状态空间。

> **Answer**: E
> PPO is a policy gradient method that works with continuous action/state spaces. It's fundamentally different from Q-Learning or Monte Carlo.
> PPO 是策略梯度方法，适用于连续动作/状态空间，与 Q-Learning 或 Monte Carlo 根本不同。

---

**Question 6** (1 point)
What is Gazebo used for in RL?
Gazebo 在 RL 中用于什么？

A) None of these answers.
B) Hyperparameter tuning tools.
C) Standard interface between agents and environments.
D) A simulation tool for training and working with agents in simulation. / 用于在仿真中训练和使用智能体的仿真工具。
E) All of these answers.

> **Answer**: D
> Gazebo is a 3D robotics simulator — provides physics simulation for training RL agents in virtual environments.
> Gazebo 是 3D 机器人仿真器——提供物理仿真以在虚拟环境中训练 RL 智能体。

---

**Question 7** (1 point)
What is Gymnasium used for in RL?
Gymnasium 在 RL 中用于什么？

A) None of these answers.
B) An environment representation tool providing a standard interface for RL. / 提供 RL 标准接口的环境表示工具。
C) A simulation tool for training agents.
D) Hyperparameter tuning tools.
E) All of these answers.

> **Answer**: B
> Gymnasium (formerly OpenAI Gym) provides a standardized API for RL environments: `reset()`, `step()`, observation/action spaces.
> Gymnasium（原 OpenAI Gym）提供 RL 环境的标准化 API：`reset()`、`step()`、观测/动作空间。

---

**Question 8** (1 point)
What is URDF in the context of robotics?
URDF 在机器人领域是什么？

A) An algorithm similar to PPO.
B) Universal Robot Description Format — an XML language for representing a robot. / 通用机器人描述格式——用 XML 描述机器人。
C) None of these answers.
D) An algorithm similar to DQN.
E) All of these answers.

> **Answer**: B
> URDF is an XML format that describes a robot's links, joints, and physical properties.
> URDF 是描述机器人连杆、关节和物理属性的 XML 格式。

---

**Question 9** (1 point)
What is SDF in the context of robotics?
SDF 在机器人领域是什么？

A) Simulation Description Format — an XML language from Gazebo for describing objects and environments. / 仿真描述格式——源自 Gazebo 的 XML 语言，用于描述物体和环境。
B) An algorithm similar to DQN.
C) An algorithm similar to PPO.
D) All of these answers.
E) None of these answers.

> **Answer**: A
> SDF originated from Gazebo, describing simulation worlds including models, lights, physics, and sensors.
> SDF 源自 Gazebo，描述仿真世界包括模型、灯光、物理和传感器。

---

**Question 10** (1 point)
What is Rviz?
什么是 Rviz？

A) A graphical interface for visualization and ROS topics.
B) A 3D visualizer for ROS displaying images, point clouds, and robot models.
C) A tool that can visualize simulated robots specified in URDF.
D) None of these answers.
E) All of these answers. / 以上全部。

> **Answer**: E
> Rviz is a ROS 3D visualization tool that can display robot models (URDF), sensor data (point clouds, images), and ROS topics.
> Rviz 是 ROS 的 3D 可视化工具，可显示机器人模型(URDF)、传感器数据和 ROS 话题。

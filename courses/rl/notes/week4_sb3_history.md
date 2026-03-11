# Week 4: Stable-Baselines3 — 历史与背景 (History & Context)

> See also: [幻灯片笔记](week4_sb3_slides.md) | [操作教程](week4_sb3_tutorial.md)

---

## 时间轴概览

```
2013           2015           2017           2018          2021           2022+
  │              │              │              │              │              │
  ▼              ▼              ▼              ▼              ▼              ▼
DQN            TRPO           PPO            SAC/TD3        SB3            SB3 Contrib
DeepMind       Schulman       Schulman       Haarnoja/      Raffin et al.  扩展算法库
第一个          信任域          近端策略       Fujimoto       PyTorch 版本   开放贡献
深度 RL         优化            优化           连续控制       稳定实现
```

---

## Station 1: OpenAI Baselines — 从研究代码到可复用库（2017）

**问题：** DeepMind 和 OpenAI 相继发布 DQN、TRPO、PPO 等算法论文，但各论文的参考代码质量极不一致，研究者难以复现或比较结果。

**创新：** OpenAI 发布 **OpenAI Baselines**:
- 收录 DQN, TRPO, PPO, ACKTR 等算法
- 基于 TensorFlow 1.x
- 提供了大量工程细节（如 `VecEnv`、归一化等）

**关键人物：**
- Prafulla Dhariwal（OpenAI）— Baselines 主要贡献者
- John Schulman — PPO、TRPO 作者

**遗留问题：** 代码风格不统一，文档稀少，依赖 TF1 且难以调试，存在多个已知 Bug。

**课程联系：** SB3 是对这段历史的直接回应——"把 Baselines 做对"。

---

## Station 2: PPO — 成为最流行 RL 算法（2017）

**问题：** TRPO（信任域策略优化）效果好但计算复杂，能否简化？

**创新：** John Schulman 等人提出 **PPO (Proximal Policy Optimization)**，用简单的 clip 操作代替 TRPO 的二阶优化：

$$L^{CLIP}(\theta) = \mathbb{E}\left[\min\left(r_t A_t, \text{clip}(r_t, 1-\epsilon, 1+\epsilon) A_t\right)\right]$$

其中 $r_t = \frac{\pi_\theta(a|s)}{\pi_{\theta_{old}}(a|s)}$ 是新旧策略的概率比。

**关键人物：**
- John Schulman（OpenAI，后 Anthropic）— PPO 和 TRPO 的提出者
- Wouter Ziebart, Pieter Abbeel — 合作者

**意义：** PPO 至今仍是最广泛使用的 RL 算法之一。OpenAI 把 PPO 用于训练 ChatGPT 的 RLHF 阶段。

**课程联系：** Week 4 使用 `PPO("MlpPolicy", env)` 就是这个历史节点的实践。

---

## Station 3: SAC 与连续控制算法突破（2018）

**问题：** PPO/A2C 是 on-policy 的，数据效率低（每次更新后数据就扔掉）。如何在连续动作空间中做到 sample-efficient？

**创新：** **SAC (Soft Actor-Critic)** 引入最大熵强化学习框架：

$$\pi^* = \arg\max_\pi \mathbb{E}\left[\sum_t r_t + \alpha \mathcal{H}(\pi(\cdot|s_t))\right]$$

- Off-policy（可复用历史数据）
- 自动调节探索-利用平衡
- 在 MuJoCo 等连续控制任务上显著优于 PPO

**关键人物：**
- Tuomas Haarnoja（UC Berkeley，后 Google）— SAC 作者
- 同期：Scott Fujimoto 提出 TD3（Twin Delayed DDPG）

**课程联系：** SB3 内置了 `SAC` 和 `TD3`，Week 4 教程中有介绍。

---

## Station 4: Stable-Baselines3 — 可靠实现运动（2021）

**问题：** Stable Baselines（PyTorch 前版本）基于 TF1，Antonin Raffin 等人决定从头重写。

**创新：** **Stable-Baselines3 (SB3)** 发布，成为官方推荐的 RL 算法库：

| 特性 | 描述 |
|------|------|
| **框架** | PyTorch（非 TensorFlow） |
| **算法** | DQN, PPO, A2C, SAC, TD3, HER |
| **VecEnv** | 内置向量化环境支持 |
| **Callbacks** | 灵活的训练监控机制 |
| **可靠性** | 每个算法有单元测试和性能验证 |

**关键人物：**
- **Antonin Raffin**（DLR 德国航空航天中心，后 INRIA）— SB3 创始人和主要维护者
- Ashley Hill, Adam Gleave, Maximilian Ernestus — 核心贡献者

**论文：** Raffin et al. (2021) "Stable-Baselines3: Reliable Reinforcement Learning Implementations" — JMLR

**意义：** Week 4 的老师幻灯片专门介绍 Antonin Raffin，因为他是课程核心工具的直接创造者。

**遗留问题：** 基础 SB3 不支持某些新兴算法（Dreamer、DDPO 等），需要通过 `sb3-contrib` 扩展。

---

## Station 5: SB3 在课程中的位置

```
Week 2/Lab 1: 手写 Q-Learning（理解原理）
  ↓
Lab 2: Gymnasium 自定义环境（标准接口）
  ↓
Assignment 1: 完整 Gymnasium 环境
  ↓
Week 4: SB3 第一次接触（PPO, A2C）
  ↓
Week 5: SB3 DQN + DiscreteActionWrapper
  ↓
Final Project: 用 SB3 解决复杂问题
```

**设计哲学：** 先理解算法（手写 Q-Learning），再使用工业级工具（SB3）。这样在使用 `model.learn()` 时，你知道内部发生了什么。

---

## 延伸阅读

- Raffin et al. (2021) — arXiv:2005.05719
- [SB3 官方文档](https://stable-baselines3.readthedocs.io/)
- Schulman et al. (2017) "Proximal Policy Optimization Algorithms" — arXiv:1707.06347
- Haarnoja et al. (2018) "Soft Actor-Critic" — arXiv:1801.01290

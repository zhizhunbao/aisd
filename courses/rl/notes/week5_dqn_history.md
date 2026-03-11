# Week 5: DQN — 历史与背景 (History & Context)

> See also: [幻灯片笔记](week5_dqn_slides.md) | [数学公式](week5_dqn_math.md) | [操作教程](week5_dqn_tutorial.md)

---

## 时间轴概览

```
1989          1992           2013           2015           2016          2022+
  │              │              │              │              │              │
  ▼              ▼              ▼              ▼              ▼              ▼
Q-Learning    TD-Gammon      DQN           DQN Nature     Double/        Rainbow DQN
Watkins       Tesauro        NIPS Paper    Paper          Dueling DQN    多种改进
博士论文       神经网络        7 个 Atari    49 个 Atari   稳定性优化      整合
              近似价值函数    超越人类       超越人类
```

---

## Station 1: Q-Learning — 理论基础（1989）

**问题：** 无模型学习是否可能收敛到最优策略？能否证明？

**创新：** Chris Watkins（剑桥博士论文）提出 Q-Learning，给出了收敛性证明：

> 在有限状态/动作空间中，只要每个 $(s,a)$ 对被充分探索，学习率满足 Robbins-Monro 条件，Q-Learning 必然收敛到最优 Q 函数。

$$Q(s, a) \leftarrow Q(s, a) + \alpha \left[ r + \gamma \max_{a'} Q(s', a') - Q(s, a) \right]$$

**关键人物：**
- Chris Watkins（1989）— Q-Learning 提出者，剑桥博士论文
- Peter Dayan（1992）— 与 Watkins 合作完善收敛性证明

**Q-Learning 的局限：** Q 值存储在表格中，状态空间越大，表格越大。状态空间 $10^{50}$（如围棋）→ 完全不可行。

**课程联系：** Week 2 + Lab 1/2 是表格版 Q-Learning；Week 5 的 DQN 是神经网络版。

---

## Station 2: TD-Gammon — 神经网络 + RL 的第一次成功（1992）

**问题：** Q-Learning 的表格限制能否用神经网络突破？

**创新：** Gerald Tesauro（IBM）用 **TD(λ) + 多层感知机** 训练双陆棋（Backgammon）agent，达到世界级水平：

- 状态：棋盘布局（约 $10^{20}$ 种可能）→ 神经网络输入
- 输出：当前局面的胜率估计 $V(s)$
- 训练方法：自我对弈（self-play），无需人类棋谱

**关键人物：**
- Gerald Tesauro（IBM，1992）— TD-Gammon 的作者

**意义：** 证明了"神经网络近似价值函数"的可行性。但当时：
1. 没有 GPU，训练极慢
2. 训练不稳定（后来 DQN 发现是因为缺乏 Target Network + Replay Buffer）

**遗留问题：** 神经网络训练高度不稳定。直接将 Q-Learning 的 Q 值用神经网络替换时，训练经常发散。

**课程联系：** DQN 的三大创新（§机器网络 + Target Network + Replay Buffer）正是直接回应了这些稳定性问题。

---

## Station 3: DQN — 深度 RL 的革命（2013 NIPS → 2015 Nature）

**问题：** 如何让 agent 直接从像素（原始图像）中学习 Atari 游戏？如何解决神经网络 Q-Learning 的训练不稳定？

**创新：** DeepMind 发布 DQN，引入三大技术解决稳定性：

| 创新 | 解决的问题 |
|------|-----------|
| **Replay Buffer** | 打破数据时间相关性 |
| **Target Network** | 防止"追移动靶"的不稳定 |
| **CNN 特征提取** | 直接处理像素输入 |

**结果：**
- 2013 NIPS：7 个 Atari 游戏中超越人类
- 2015 Nature：49 个 Atari 游戏中超越人类（登上 Nature 封面）

**关键人物：**
- Volodymyr Mnih（DeepMind）— DQN 第一作者
- David Silver（DeepMind）— RL 核心成员，AlphaGo 主要贡献者
- Koray Kavukcuoglu, Daan Wierstra — DeepMind 团队

**论文：** Mnih et al. (2015) "Human-level control through deep reinforcement learning" — Nature 518, 529-533

**课程联系：** 课程 Week 5 用的 SB3 `DQN` 实现就是这篇论文的直接应用。

---

## Station 4: Double DQN 与 Dueling DQN — 算法改进（2015-2016）

**问题：** 原始 DQN 存在 Q 值**高估** (overestimation) 问题，导致某些环境性能不稳定。

**创新 1：Double DQN（van Hasselt 2015）**

用主网络选择动作，用目标网络评估价值，防止高估：

$$y = r + \gamma Q_{target}(s', \arg\max_{a'} Q_\theta(s', a'))$$

**创新 2：Dueling DQN（Wang 2016）**

将 Q 值分解为状态价值 V(s) 和优势函数 A(s,a)：

$$Q(s, a) = V(s) + A(s, a) - \frac{1}{|A|} \sum_{a'} A(s, a')$$

对于很多动作无差异的状态（如 Atari 中的空白画面），可以更高效地学习。

**关键人物：**
- Hado van Hasselt — Double DQN
- Ziyu Wang — Dueling DQN

**课程联系：** SB3 的 DQN 实现包含了 Double DQN（可通过 `target_update_interval` 等参数配置）。

---

## Station 5: Rainbow DQN — 整合全部改进（2017）

**问题：** Double DQN、Dueling DQN、Prioritized Replay、N-step returns 等改进是否可以叠加？

**创新：** DeepMind 的 **Rainbow** 将 6 种 DQN 改进整合到一个算法中，在 Atari 上全面超越单独的任何改进。

| 改进 | 解决的问题 |
|------|-----------|
| Double DQN | Q 值高估 |
| Dueling Network | 状态/动作价值分离 |
| Prioritized Replay | 重要经验更多被采样 |
| Multi-step Returns | 加速传播奖励信号 |
| Distributional RL | 建模回报分布（非期望） |
| Noisy Networks | 参数噪声探索 |

**课程联系：** 工业级 DQN 使用类似 Rainbow 的思路，但课程聚焦基础 DQN，理解核心三大创新即可。

---

## 延伸阅读

- Mnih et al. (2015) — Nature 518 — 原始 DQN 论文
- van Hasselt et al. (2016) "Deep Reinforcement Learning with Double Q-learning"
- Wang et al. (2016) "Dueling Network Architectures for Deep Reinforcement Learning"
- Hessel et al. (2018) "Rainbow: Combining Improvements in Deep Reinforcement Learning"

# Week 3: Gymnasium — 历史与背景 (History & Context)

> See also: [幻灯片笔记](week3_gymnasium_slides.md) | [代码参考](week3_gymnasium_code.md)

---

## 时间轴概览

```
2013           2016           2017           2019          2022           2023+
  │              │              │              │              │              │
  ▼              ▼              ▼              ▼              ▼              ▼
ALE            OpenAI         SB (v1)        SB2            Farama         课程使用
Arcade         Gym            Dhariwal       Stable         Gymnasium      Gymnasium
Learning       Brockman       et al.         Baselines2     (Farama 基金会  0.29.x
Environment    首次统一接口                               接管维护)
```

---

## Station 1: Arcade Learning Environment — 第一个标准化 RL 基准（2013）

**问题：** RL 研究中缺乏统一的测试基准，各论文用不同环境，结果无法比较。

**创新：** Marc Bellemare 等人发布 **ALE (Arcade Learning Environment)**，将 Atari 2600 游戏封装为 RL 测试平台，定义了最早的标准化环境接口。

**关键人物：**
- Marc Bellemare（2013，后加入 Google）— ALE 第一作者
- Joel Veness, Michael Bowling — 合作者

**意义：** 同年（2013）DeepMind 发布 DQN 论文，正是在 ALE 上展示了 Atari 游戏的超人类性能。两者相辅相成，推动了 RL 的复兴。

**遗留问题：** ALE 只包含 Atari 游戏，缺乏 Gridworld、连续控制等其他类型环境。

**课程联系：** ALE 是"RL 环境标准化"思想的开端，直接启发了后来的 OpenAI Gym。

---

## Station 2: OpenAI Gym — 统一 RL 环境接口（2016）

**问题：** 不同 RL 算法在不同环境库中测试，没有通用接口，代码复用率极低。

**创新：** OpenAI 团队发布 **Gym**，提出第一个被广泛采用的 RL 环境 API 标准：

```python
obs = env.reset()
obs, reward, done, info = env.step(action)
env.render()
```

内置环境包括：Atari、CartPole、MountainCar、MuJoCo 等。

**关键人物：**
- Greg Brockman（OpenAI CTO）— Gym 的主要推动者
- John Schulman — 合作者（也是 PPO 的提出者）

**意义：** "任何 RL 算法 + 任何 Gym 兼容环境" = 开箱即用。这极大降低了 RL 研究的门槛。

**遗留问题：**
1. OpenAI 逐渐减少 Gym 维护，更新停滞
2. 旧 API 只返回 4 个值（`done` 混合了 `terminated` 和 `truncated`）
3. 缺乏对向量化环境的原生支持

**课程联系：** 本课程从旧 Gym 的"homemade 环境"（Lab 1）直接升级到 Gymnasium（Lab 2）。

---

## Station 3: Stable Baselines — 可靠算法实现的需求（2017-2019）

**问题：** OpenAI 发布了各种 RL 算法的参考实现（OpenAI Baselines），但代码质量参差不齐，难以直接使用。

**创新：** 法国独立研究者 Ashley Hill 等人发布 **Stable Baselines (SB)**，基于 OpenAI Baselines 重写，提供更清洁的接口和可靠性保证。

**关键人物：**
- Ashley Hill — SB 的主要作者
- 后由 Antonin Raffin 主导 SB3

**背景：** 这个时期 PPO（2017）、SAC（2018）等算法相继提出，研究者急需可靠的对比基线。

**遗留问题：** 原 SB 基于 TensorFlow 1.x，随着 PyTorch 崛起，需要重写。

**课程联系：** Week 4 介绍的 SB3 是这一努力的最终成果。

---

## Station 4: Gymnasium — Farama 基金会接管（2022）

**问题：** OpenAI 在 2021 年宣布不再维护 Gym，社区面临"谁来维护 RL 标准接口"的问题。

**创新：** **Farama 基金会**（非营利组织）接管，发布 **Gymnasium** (0.26+) —— OpenAI Gym 的精神继承者，但有重要改进：

| 变化 | 旧 Gym | 新 Gymnasium |
|------|--------|-------------|
| `step()` 返回值 | 4 个（`done`） | **5 个**（`terminated` + `truncated`） |
| 维护状态 | 停止维护 | 持续活跃开发 |
| 自定义环境文档 | 较少 | 详细完整 |
| 向量化支持 | 有限 | 完善 |

**关键人物：**
- Mark Towers — Gymnasium 主要维护者
- Jordan Terry — Farama 基金会创始人

**`terminated` vs `truncated` 的意义：**

```python
terminated = True    # 自然结束（到达目标 or 失败）
truncated = True     # 超时结束（TimeLimit wrapper）
# 可以分别处理，价值估计更准确
```

**课程联系：** 课程全程使用 `gymnasium`（非 `gym`），`step()` 返回 5 个值是关键知识点。

---

## Station 5: 课程中的环境演进路径

```
Lab 1: 自制 CliffWalking 类（无 Gymnasium 接口）
  ↓ 升级
Lab 2: 标准 Gymnasium 自定义环境
  ↓ 扩展
Assignment 1: 完整自定义 BlocksWorld Gymnasium 环境
  ↓ 集成
Week 4/5: SB3 + Gymnasium 环境，使用 DQN/PPO/A2C
```

每一步代表了课程对真实 RL 开发工作流的逐步还原：从"理解原理"到"工程实践"。

---

## 延伸阅读

- [Gymnasium 官方文档](https://gymnasium.farama.org/)
- [Farama 基金会博客](https://farama.org/Announcing-The-Farama-Foundation)
- Brockman et al. (2016) "OpenAI Gym" — arXiv:1606.01540

# Lab 2 故事线：Gymnasium 自定义环境 — 从手写环境到标准接口

> **Source:** `CST8509_Lab2_Gymnasium.md`
> **核心问题：** 为什么不能一直用 Lab 1 的"手写"环境？Gymnasium 标准接口到底解决了什么问题？
> **前置知识：** [Week 2 MDP](week2_mdp_storyline.md) | [Week 3 Gymnasium](week3_gymnasium_storyline.md)
> **代码速查：** [lab2_gymnasium_code.md](lab2_gymnasium_code.md)

---

## 🗺️ 路线图 (Roadmap)

```
Lab 1                           Lab 2                          Week 5 / Assignment 1
┌──────────────────┐    ┌─────────────────────────┐    ┌────────────────────────────┐
│ 手写 CliffEnv     │ →  │ Gymnasium CliffWalking   │ →  │ SB3 DQN + BlocksWorld       │
│ 自定义 reset/step │    │ 标准 reset()/step() 接口  │    │ MultiDiscrete + Wrappers    │
│ 只兼容手写 agent  │    │ 兼容 Q-Learning + SB3    │    │ 复杂状态 + 多算法对比        │
│ 无 PyGame 渲染    │    │ PyGame 渲染              │    │ PyGame 渲染                 │
└──────────────────┘    └─────────────────────────┘    └────────────────────────────┘
```

---

## 📖 因果叙事 (Causal Narrative)

### 第一章：Lab 1 的局限——手写环境无法扩展

**Lab 1 完成了什么：** 你手写了一个简单的 CliffWalking 环境和 Q-Learning agent，两者通过自定义接口通信：

```python
# Lab 1 风格：完全自定义接口
state = env.get_state()
action = agent.choose(state)
next_state, reward, done = env.step(action)   # 自己定义的返回格式
```

**问题出现了：** 这个接口只属于你的 agent。当你想用 PPO、DQN 或任何第三方算法时：

```
手写 CliffEnv  ←──── 只有你的 Q-Learning agent 能用
                      PPO ❌（接口不匹配）
                      DQN ❌（接口不匹配）
                      SB3 ❌（接口不匹配）
```

**根本矛盾：** RL 算法有几十种，环境有成千上万种。如果每种组合都需要手动适配接口，这个领域根本无法发展。

---

### 第二章：解决方案——Gymnasium 标准接口

**Gymnasium 的思路：** 定义一个所有环境都必须实现的标准接口，所有算法都按这个标准通信：

```
任何环境  ────► reset() / step() / render()  ◄────  任何算法
              (Gymnasium 标准接口)
```

**Lab 2 的任务：** 把你 Lab 1 的手写 CliffWalking 环境，重写为一个符合 Gymnasium 标准的自定义环境 `CliffWalking-v0`。

**接口的核心约定：**

| 方法 | 输入 | 输出 | 说明 |
|------|------|------|------|
| `reset()` | — | `(observation, info)` | 重置环境，返回初始观测 |
| `step(action)` | action | `(obs, reward, terminated, truncated, info)` | 执行一步，返回 5 个值 |
| `render()` | — | None / image | 渲染当前状态 |

> ⚠️ **Lab 1 vs Lab 2 的关键差异：**
> Lab 1 的 `step()` 可能返回 3 个值：`(next_state, reward, done)`
> Lab 2 的 Gymnasium `step()` 返回 **5 个值**：`(obs, reward, terminated, truncated, info)`
> `terminated`（到达目标/失败）和 `truncated`（超时）被拆开了！

---

### 第三章：实现流程——从 GridWorld 到 CliffWalking

Lab 2 没有让你从零开始，而是给了一个模板 `GridWorld-v0`，让你在它基础上修改：

```
GridWorld-v0（5×5 方格）
    │
    ├─ 复制 grid_world.py → cliff_walking.py
    ├─ 改类名：GridWorldEnv → CliffWalkingEnv
    ├─ 改网格：5×5 → 12×4（X轴12列，Y轴4行）
    ├─ 更新 ObservationSpace（spaces.Box 分开定义 X/Y 轴边界）
    ├─ 注册新环境 ID：cliffwalking_env/CliffWalking-v0
    └─ 更新 PyGame 渲染尺寸
```

**为什么 12×4？** 这是经典 CliffWalking 的标准网格：12 列 × 4 行，Agent 从左下角出发，目标是右下角，底边是悬崖。

**ObservationSpace 的关键变化：**

```python
# GridWorld（正方形，单一 size 参数）
spaces.Box(0, self.size - 1, shape=(2,), dtype=int)

# CliffWalking（矩形，X/Y 分开）
spaces.Box(
    low=np.array([0, 0]),
    high=np.array([self.xsize - 1, self.ysize - 1]),
    shape=(2,), dtype=int
)
```

---

### 第四章：Q-Learning 适配——观测值不再是整数了

**新的挑战：** Lab 1 的 Q-table 用整数 state 做索引（`qtable[state]`），但 Gymnasium 的 `step()` 返回的观测是**字典**：

```python
observation = {'agent': array([x, y]), 'target': array([tx, ty])}
```

Q-table 不能用字典作索引——需要手动把 (x, y) 坐标转换为整数 state：

```python
# 坐标 (x, y) → 整数 state
state = y * (env.observation_space['agent'].high[0] + 1) + x
# 等价于：state = y * xsize + x（行优先展平）
```

**总状态数计算：**

```python
numstates = (env.observation_space['agent'].high[0] + 1) * \
            (env.observation_space['agent'].high[1] + 1)
# = 12 * 4 = 48 个状态
```

---

### 第五章：SB3 接入——一行代码换算法

完成自定义 Gymnasium 环境后，接入 SB3 的成本几乎为零：

```python
# Q-Learning agent（Lab 1 改造版）
env = gymnasium.make("cliffwalking_env/CliffWalking-v0")
# 手动 Q-table + 手动循环

# DQN（SB3）—— 换算法只改这两行
model = DQN("MultiInputPolicy", env, verbose=1)
model.learn(total_timesteps=10000)

# PPO（SB3）—— 再换一次
model = PPO("MultiInputPolicy", env, verbose=1)
model.learn(total_timesteps=10000)
```

**这正是 Gymnasium 标准的价值：** 环境写好一次，所有算法都能用。

---

### 第六章：对比三种 Agent 的本质差异

| | 手写 Q-Learning | SB3 DQN | SB3 PPO |
|--|----------------|---------|---------|
| **Q-table / 网络** | 手写 48×4 表格 | 神经网络近似 Q | Actor-Critic 网络 |
| **策略类型** | off-policy | off-policy | on-policy |
| **经验回放** | ❌ | ✅ Replay Buffer | ❌ |
| **适合场景** | 小状态空间 | 小到中状态空间 | 连续 / 大状态空间 |
| **超参数** | α, γ, ε | 以上 + batch_size, target_update | 以上 + clip_range |

> 💡 **考试常见考点：** Q-Learning 是 off-policy，PPO 是 on-policy，DQN 用 Replay Buffer。

---

## ✅ 考试 Checklist

- [ ] `step()` 返回几个值？各是什么？→ 5 个：`(obs, reward, terminated, truncated, info)`
- [ ] `terminated` vs `truncated` 区别？→ 前者自然结束（到目标/失败），后者超时截断
- [ ] 如何把 Gymnasium 观测坐标 (x, y) 转换为 Q-table 整数索引？→ `state = y * xsize + x`
- [ ] 什么是 Gymnasium Wrapper？→ 不修改源码修改环境行为的包装类
- [ ] 为什么需要 `MultiInputPolicy` 而不是 `MlpPolicy`？→ 因为观测是字典（多输入）而非单一数组
- [ ] CliffWalking 网格大小？→ 12×4（X=12列，Y=4行），共 48 个状态
- [ ] 注册环境 ID 的目的？→ 使 `gymnasium.make("cliffwalking_env/CliffWalking-v0")` 能找到该类

---

## 📚 参考资料

| 资源 | 说明 |
|------|------|
| [Lab 2 原文](../labs/CST8509_Lab2_Gymnasium.md) | 完整实验描述 |
| [lab2_gymnasium_code.md](lab2_gymnasium_code.md) | 关键代码速查 |
| [Week 3 Gymnasium 故事线](week3_gymnasium_storyline.md) | Gymnasium 标准接口的完整讲解 |
| [Week 3 Gymnasium slides](week3_gymnasium_slides.md) | 老师 slides |
| [Week 6 期中复习 slides](week6_midterm_review_slides.md) | 考试范围与笔试样题 |

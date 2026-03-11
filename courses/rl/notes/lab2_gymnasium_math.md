# Lab 2 Gymnasium — 数学公式 (Math)

> **See also:** [代码速查](lab2_gymnasium_code.md) | [故事线](lab2_gymnasium_storyline.md) | [教程](lab2_gymnasium_tutorial.md)
> **Source:** Gymnasium API Docs + Sutton §3.1 + Week 3 Math + Lab 2 指导文档

---

## ★ Agent-Environment 交互（MDP 形式化）

在每个时间步 $t$：

$$S_t \xrightarrow{A_t} (S_{t+1},\ R_{t+1},\ \text{terminated},\ \text{truncated})$$

对应 Gymnasium `step()` 返回值：

| 返回值 | MDP 符号 | 含义 |
|--------|---------|------|
| `observation` | $S_{t+1}$ | 下一状态（观测） |
| `reward` | $R_{t+1}$ | 即时奖励 |
| `terminated` | $\mathbb{1}[S_{t+1} \in S_{\text{terminal}}]$ | 自然终止（到达目标 / 掉入悬崖） |
| `truncated` | — | 超时截断（非 MDP 的一部分） |
| `info` | — | 调试信息（距离等） |

---

## ★ 观测空间大小

### Discrete Space

$$|S| = n \quad \text{for } \texttt{spaces.Discrete(n)}$$

### Box Space（整数）

$$|S| = \prod_{i=1}^{d} (\text{high}_i - \text{low}_i + 1)$$

### Dict Space（组合）

$$|S| = \prod_k |S_k|$$

---

## ★ Lab 2 CliffWalking 空间定义

### 观测空间（Dict）

```
observation_space = Dict({
    "agent": Box(low=[0,0], high=[11,3], shape=(2,)),  # agent 的 (x, y) 坐标
    "target": Box(low=[0,0], high=[11,3], shape=(2,))  # 目标的 (x, y) 坐标
})
```

| 维度 | 值 | 说明 |
|------|-----|------|
| agent x | $[0, 11]$ → 12 个值 | 列（左到右） |
| agent y | $[0, 3]$ → 4 个值 | 行（上到下） |
| 位置组合数 | $12 \times 4 = 48$ | 与 Lab 1 状态数相同 |
| Dict 组合数 | $48 \times 48 = 2304$ | agent + target 位置组合 |

### 动作空间（Discrete）

$$|A| = 4 \quad \text{(右=0, 上=1, 左=2, 下=3)}$$

### Q-Table 大小（若用 Q-Learning）

> ⚠️ Dict 观测空间不能直接用于 Q-Table。需要先将观测转换为整数索引。

$$\text{Q-table size} = |S_{\text{agent}}| \times |A| = 48 \times 4 = 192$$

---

## ★ Lab 2 观测 → 整数索引转换

**从 Dict 观测提取 agent 整数 state：**

$$\text{state} = y_{\text{agent}} \times 12 + x_{\text{agent}}$$

```python
obs, info = env.reset()
state = obs["agent"][1] * 12 + obs["agent"][0]  # y * width + x
```

---

## ★ CliffWalking 奖励结构（Lab 2 版本）

$$R(s, a) = \begin{cases} -100 & \text{掉入悬崖（底行 } x \in [1,10]\text{），terminated=True} \\ 0 & \text{到达目标（底行 } x=11\text{），terminated=True} \\ -1 & \text{其他所有步骤} \end{cases}$$

> ⚠️ **Lab 1 vs Lab 2 差异：**
> - Lab 1：掉崖后 `done=False`，episode 继续，agent 返回起点
> - Lab 2 Gymnasium：掉崖后 `terminated=True`，episode 结束

---

## ★ 曼哈顿距离（info 字段）

$$d_1(p, q) = |x_p - x_q| + |y_p - y_q|$$

```python
info = {"distance": np.linalg.norm(agent_loc - target_loc, ord=1)}
```

用于监控训练进展——平均 distance 下降说明 agent 在学习接近目标。

---

## 📝 手算：计算 Dict 观测的 Q-Table 索引

**题目：** agent 在位置 $(x=3, y=2)$，目标在 $(11, 3)$。
1. 计算 agent 的整数状态 index
2. 此时 Q-Table 查找的行是？

**解：**

Step 1: agent state = $y \times 12 + x = 2 \times 12 + 3 = 27$

Step 2: Q-Table 查找 `Q[27, :]`（4 个动作的 Q 值）

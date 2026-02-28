# Week 3: Gymnasium — 数学公式 (Math Reference)

> See also: [概念速查](week3_gymnasium_cheatsheet.md) | [代码参考](week3_gymnasium_code.md)

---

> ℹ️ Week 3 以工程实践为主，数学内容较少。核心数学在 Week 2 MDP 中已覆盖。

## 📐 Agent-Environment 交互公式

### MDP 交互循环（Sutton §3.1）

在每个时间步 $t$：

$$S_t \xrightarrow{A_t} S_{t+1}, R_{t+1}$$

对应 Gymnasium 代码：
```python
obs, reward, terminated, truncated, info = env.step(action)
# S_{t+1}  R_{t+1}   done?       timeout?    debug
```

### 回报（Return）

$$G_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + \cdots = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1}$$

| 符号 | 含义 | Gymnasium 对应 |
|------|------|---------------|
| $S_t$ | 时间步 $t$ 的状态 | `observation`（`reset()` 或 `step()` 返回）|
| $A_t$ | 时间步 $t$ 的动作 | `action`（传入 `step(action)`）|
| $R_{t+1}$ | 执行 $A_t$ 后的即时奖励 | `reward`（`step()` 返回）|
| $\gamma$ | 折扣因子 $\in [0, 1]$ | 在 Agent 中设置，不在环境中 |
| $G_t$ | 从 $t$ 开始的累积折扣回报 | Agent 自行计算 |

---

## 📐 状态空间大小计算

### Discrete Space

$$|S| = n \quad \text{for } \texttt{spaces.Discrete(n)}$$

### Box Space

连续空间，理论上 $|S| = \infty$。实际离散化后：

$$|S| \approx \prod_{i=1}^{d} \frac{high_i - low_i}{\Delta_i}$$

### Dict Space（组合空间）

$$|S| = |S_1| \times |S_2| \times \cdots$$

例如 `Dict({"agent": Discrete(12), "target": Discrete(12)})` → $|S| = 12 \times 12 = 144$

---

## 📐 Q-Table 大小

$$\text{Q-table size} = |S| \times |A|$$

```python
# 对应代码
qtable = np.zeros((env.observation_space.n, env.action_space.n))
# shape: (|S|, |A|)
```

例如 4×3 GridWorld，4 个动作：$12 \times 4 = 48$ 个 Q 值

---

## 📝 手算练习

### 练习 1：计算 Q-Table 大小

BlocksWorld 有 30 个合法状态，6 个动作。Q-Table 有多少个元素？

<details>
<summary>答案</summary>

$30 \times 6 = 180$ 个 Q 值

</details>

### 练习 2：Dict vs Discrete 观测空间大小

如果 agent 有 30 个可能位置，target 有 30 个可能位置：
- `Dict({"agent": Discrete(30), "target": Discrete(30)})` 的总观测空间大小？
- 如果合并为 `Discrete(n)`，n 应该是多少？

<details>
<summary>答案</summary>

- Dict: $30 \times 30 = 900$ 种组合
- Discrete: $n = 900$（每种 agent-target 组合编码为一个唯一整数）

</details>

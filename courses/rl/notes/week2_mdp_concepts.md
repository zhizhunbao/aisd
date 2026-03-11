# Week 2: MDP — 核心概念 (Core Concepts)

> See also: [幻灯片笔记](week2_mdp_slides.md) | [数学公式](week2_mdp_math.md) | [历史背景](week2_mdp_history.md)

---

## 核心术语速查

### MDP（马尔可夫决策过程）

用五元组 $(S, A, P, R, \gamma)$ 描述序列决策问题的数学框架：

| 符号 | 名称 | 说明 |
|------|------|------|
| $S$ | 状态空间 | 所有可能状态的集合 |
| $A$ | 动作空间 | 所有可能动作的集合 |
| $P(s'\|s,a)$ | 转移概率 | 在状态 $s$ 做 $a$ 后到达 $s'$ 的概率 |
| $R(s,a)$ | 奖励函数 | 在状态 $s$ 做 $a$ 所获奖励 |
| $\gamma$ | 折扣因子 | $0 \le \gamma < 1$ |

---

### Bellman Equation（贝尔曼方程）

Q 值的自洽性方程（来自 Bellman 1957）：

$$Q(s, a) = R + \gamma \max_{a'} Q(s', a')$$

**解读：** 好的 $(s, a)$ = 即时奖励 + 下一状态的最大 Q 值（折扣后）

---

### Q-Learning 更新规则（★★★ 必考）

$$Q(s, a) \leftarrow Q(s, a) + \alpha \Big[ r + \gamma \max_{a'} Q(s', a') - Q(s, a) \Big]$$

**三部分拆解：**

| 部分 | 名称 | 含义 |
|------|------|------|
| $r + \gamma \max_{a'} Q(s', a')$ | TD target（时序差分目标） | 我们希望 Q 值达到的目标 |
| $[\ldots] - Q(s,a)$ | TD error（时序差分误差） | 目标与当前估值的差距 |
| $\alpha \times \text{TD error}$ | 更新量 | 每次向目标迈进一小步 |

---

### ε-Greedy 策略

$$a = \begin{cases} \arg\max_{a'} Q(s, a') & \text{以概率 } 1 - \varepsilon \\ \text{random} & \text{以概率 } \varepsilon \end{cases}$$

**作用：** 平衡探索（Exploration）与利用（Exploitation）。

> ⚠️ $\varepsilon$ 太大 → 一直随机，无法利用已学知识；太小 → 过早收敛到局部最优

---

### Off-Policy vs On-Policy

| 概念 | 定义 | 算法 |
|------|------|------|
| Off-policy | 学习策略 ≠ 行为策略（更新目标与执行动作解耦） | Q-Learning |
| On-policy | 学习策略 = 行为策略（用自己执行的动作更新） | SARSA |

**关键差别在更新目标：**

```
Q-Learning:  target = r + γ max_a' Q(s', a')   ← 假设下一步最优
SARSA:        target = r + γ Q(s', a')          ← a' 来自实际执行的策略
```

---

### SARSA

$$Q(s, a) \leftarrow Q(s, a) + \alpha \Big[ r + \gamma Q(s', a') - Q(s, a) \Big]$$

名字来自更新所用的五元组：**S**tate → **A**ction → **R**eward → **S**tate' → **A**ction'

---

### Greedy 动作选择

$$a = \arg\max_{a'} Q(s, a')$$

在 Q-table 中选 Q 值最大的动作，无随机性。

---

## 概念辨析

### Q-Learning vs SARSA（CliffWalking 场景）

| 维度 | Q-Learning | SARSA |
|------|-----------|-------|
| Policy 类型 | Off-policy | On-policy |
| 更新目标 | 假设下一步最优 | 实际执行的下一动作 |
| CliffWalking 路径 | 最短（紧贴悬崖） | 更长但更安全 |
| 为何不同 | 不"感"到随机探索的风险 | 感受到随机探索掉悬崖的惩罚 |

### TD Error vs Bellman Error

- **TD Error**：$r + \gamma \max Q(s', a') - Q(s, a)$（基于一次采样）
- **Bellman Error**：完整期望版本，需要知道所有转移概率
- Q-Learning 用 TD Error 近似 Bellman Error

### Q-Table 初始化的影响

| 初始化 | 探索行为 | 收敛速度 |
|--------|---------|---------|
| 全 0 | 无主动探索动力 | 较慢 |
| 乐观高值 | 主动探索未访问状态 | 较快且更彻底 |
| 随机值 | 行为随机但全面 | 不稳定 |

---

## 易错点速查

| 错误 | 正确理解 |
|------|---------|
| "终止状态 Q 值可以随机初始化" | 必须设为 0，否则 Bellman 更新引入虚假未来奖励 |
| "Q-Learning 比 SARSA 一定更好" | CliffWalking 中 SARSA 实际性能更好（考虑了执行时的随机性） |
| "off-policy 学的是行为策略" | Off-policy 学的是*目标*策略（最优策略），行为策略只用来收集数据 |
| "alpha 越大学得越快越好" | $\alpha$ 过大导致 Q 值震荡不收敛；需满足 Robbins-Monro 条件收敛 |

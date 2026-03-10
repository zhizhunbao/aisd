# Assignment 1 Blocks World — 数学公式 (Math)

> **See also:** [概念速查](assignment1_blocksworld_cheatsheet.md) | [代码参考](assignment1_blocksworld_code.md)
> **Source:** Sutton §3.3-3.5, §6.5 + Week 2 MDP 数学 + Quiz 2

---

## ★ Q-Learning 更新公式 (📚 Sutton §6.5 Eq. 6.8)

$$Q(S, A) \leftarrow Q(S, A) + \alpha \left[ R + \gamma \max_{a'} Q(S', a') - Q(S, A) \right]$$

| 符号                     | 含义                    | BlocksWorld 对应        | 典型值      |
| ------------------------ | ----------------------- | ----------------------- | ----------- |
| $Q(S,A)$                 | 状态-动作对的价值       | `Q[state, action]`      | 初始=0      |
| $\alpha$                 | 学习率                  | `alpha`                 | 0.1         |
| $R$                      | 即时奖励                | `reward`                | -1/-10/+100 |
| $\gamma$                 | 折扣因子 (📚 Quiz 2 Q7) | `gamma`                 | 0.99        |
| $\max_{a'} Q(S', a')$    | 下一状态最大 Q 值       | `np.max(Q[next_state])` | —           |
| $R + \gamma \max Q' - Q$ | TD 误差                 | —                       | —           |

---

## ★ 折扣回报 (📚 Sutton §3.3 Eq. 3.8)

$$G_t = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1} = R_{t+1} + \gamma G_{t+1}$$

> 📚 Quiz 2 Q7: $\gamma \in [0,1)$ 确保收敛

---

## ★ ε-Greedy 策略

$$a = \begin{cases} \text{random action} & \text{with probability } \epsilon \\ \arg\max_{a'} Q(s, a') & \text{with probability } 1 - \epsilon \end{cases}$$

> 📚 Quiz 2 Q12: greedy = 即时奖励优先 = $\arg\max Q$

---

## ★ Q-Table 大小 (📚 Quiz W3 S2)

$$|Q\text{-Table}| = |S| \times |A|$$

| 环境版本 | $    | S   | $     | $   | A   | $   | Q-Table 大小 |
| -------- | ---- | --- | ----- | --- | --- | --- | ------------ |
| v0       | ~13  | ~N  | ~13N  |
| v1       | ~169 | ~N  | ~169N |

---

## 📝 手算: Q-Learning 更新

**题目:** $\alpha=0.5$, $\gamma=0.9$. 当前 $Q(s=3, a=2) = 2.0$. Agent 执行 $a=2$, 得到 $R=-1$, 到达 $s'=5$. $\max_{a'} Q(5, a') = 3.0$.

**解:**

Step 1: TD target = $R + \gamma \max Q' = -1 + 0.9 \times 3.0 = 1.7$

Step 2: TD error = $1.7 - Q(3,2) = 1.7 - 2.0 = -0.3$

Step 3: $Q(3,2) \leftarrow 2.0 + 0.5 \times (-0.3) = 1.85$

> 📚 对照 Week 2 MDP 数学的手算模式

---

## 📝 手算: 折扣回报

**题目 (📚 Week 2 MDP 数学 手算题):** $\gamma=0.9$, 奖励序列 $R_1=-1, R_2=-1, R_3=100$ (达到目标后终止).

**解:**

$G_0 = R_1 + \gamma R_2 + \gamma^2 R_3 = (-1) + 0.9(-1) + 0.81(100) = -1 - 0.9 + 81 = 79.1$

> 💡 正的总回报说明 +100 的目标奖励足以覆盖 -1 的步数惩罚

---

## 📝 手算: 超参数影响

**ε-decay 影响 (Assignment 要求实验):**

| 参数组     | $\alpha$ | $\gamma$ | ε-decay  | 效果预期               |
| ---------- | -------- | -------- | -------- | ---------------------- |
| Original   | 0.1      | 0.99     | 0.995    | 基线                   |
| 高学习率   | **0.2**  | 0.99     | 0.995    | 更快收敛但可能不稳定   |
| 低折扣     | 0.1      | **0.9**  | 0.995    | 更近视, 可能找不到最优 |
| 快探索衰减 | 0.1      | 0.99     | **0.99** | 更快停止探索           |

---

## 速查公式表

| 公式名       | 公式                                               | 关键         |
| ------------ | -------------------------------------------------- | ------------ | ----------- | --- | --- | ---------- |
| Q-Learning   | $Q \leftarrow Q + \alpha[R + \gamma \max Q' - Q]$  | Off-policy   |
| SARSA        | $Q \leftarrow Q + \alpha[R + \gamma Q(S',A') - Q]$ | On-policy    |
| 折扣回报     | $G_t = R_{t+1} + \gamma G_{t+1}$                   | $\gamma < 1$ |
| 贪婪         | $a^* = \arg\max Q(s, \cdot)$                       | Quiz 2 Q12   |
| Q-Table 大小 | $                                                  | S            | \times      | A   | $   | Quiz W3 S2 |
| V-Q 关系     | $V(s) = \sum_a \pi(a                               | s) Q(s,a)$   | V 是 Q 均值 |
| Bellman      | $V(s) = \mathbb{E}[R + \gamma V(s')]$              | Quiz 2 Q11   |

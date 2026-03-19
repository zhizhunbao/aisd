---
topic: foundations
dimension: pitfalls
created: 2026-03-19
last_verified: 2026-03-19
source_versions:
  - "📚 Book: Sutton & Barto, 《Reinforcement Learning: An Introduction》 2nd Ed. Ch.1-2 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/sutton_barto_rl_intro.pdf"
  - "🧪 经验: 常见 RL 初学者误区总结"
expiry: 6m
status: current
---

# RL 基础 踩坑记录

> ⚠️ **围绕学习痛点组织**，不是技术 debug 日志。每次踩坑后请追加条目。

---

## 坑 1: 把 RL 当监督学习来理解

**痛点类别：** #5 名词多黑话多 + #3 知识碎片化

**场景：** 初学者第一次接触 RL，用监督学习的心智模型去理解

**症状：** 疑惑"训练数据在哪？""标签是什么？""Loss 函数怎么定义？"——这些问题在 RL 里都问错了方向

**根因：** RL 和 SL 是完全不同的范式。SL 的核心是"给数据+标签→学映射"，RL 的核心是"自己生成数据→通过奖励信号改进"。当你用 SL 的框架理解 RL 时，很多概念硬套不上去

**解法：**

❌ 错误做法 — 用 SL 类比理解 RL

```python
# ❌ 错误思维：把 RL 当做 "状态→最优动作" 的分类问题
# "我有一堆 (state, best_action) 对，训练一个分类器就行了"
# 问题：你根本不知道 best_action 是什么！
model.fit(states, best_actions)  # 这不是 RL
```

✅ 正确做法 — 从交互循环理解 RL

```python
# ✅ 正确思维：Agent 自己试错，根据奖励改进
for step in range(total_steps):
    action = agent.select_action(state)     # Agent 自己决定
    next_state, reward, done = env.step(action)  # 环境给反馈
    agent.learn(state, action, reward)      # 用奖励改进
    state = next_state
```

**教训：** RL 没有"老师"告诉你正确答案，只有环境给你打分。先忘掉 SL，从"试错-反馈"的角度重新理解。

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.1 §1.1

---

## 坑 2: 混淆奖励 (Reward) 和回报 (Return)

**痛点类别：** #5 名词多黑话多

**场景：** 看公式的时候，搞不清 r 和 G 的区别，或者以为 Agent 的目标是最大化每步的即时奖励

**症状：** 实现代码时只优化单步奖励，导致 Agent 表现短视——比如机器人只会原地打转（因为每步不摔就有正奖励）

**根因：** 奖励 r 是单步信号，回报 G 是所有未来奖励的折扣加权和。RL 的真正目标是最大化 G 而不是 r

**解法：**

❌ 错误做法 — 只看即时奖励

```python
# ❌ 只最大化单步奖励 → Agent 变得短视
action = argmax([immediate_reward(a) for a in actions])
```

✅ 正确做法 — 考虑累积折扣回报

```python
# ✅ RL 的真正目标：最大化 Gₜ = rₜ₊₁ + γrₜ₊₂ + γ²rₜ₊₃ + ...
# 增量更新本质上在追踪长期回报
Q[a] += alpha * (r + gamma * max(Q) - Q[a])  # Q-learning
```

**教训：** 记住口诀：**r 是一步的，G 是一串的**。Agent 要最大化的是 G。

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.3 §3.3

---

## 坑 3: ε 值选太大或太小

**痛点类别：** #1 只甩任务不教思路

**场景：** 实现 ε-greedy 时不知道 ε 该设多少

**症状：** ε=0.5 → Agent 一半时间在瞎试，学得很慢。ε=0.001 → Agent 几乎不探索，卡在次优动作

**根因：** ε 是探索与利用的权衡旋钮。太大=太多探索白费步数，太小=探索不够错过最优

**解法：**

❌ 错误做法 — 凭感觉乱设

```python
# ❌ ε=0.5 太大：一半时间在随机选，性能上不去
epsilon = 0.5  # 50% 时间在探索，太浪费了
```

✅ 正确做法 — 合理范围 + 衰减策略

```python
# ✅ 标准做法：ε ∈ [0.01, 0.1]，可选衰减
epsilon = 0.1                       # 经典起始值
epsilon = max(0.01, epsilon * 0.995) # 每步衰减，逐渐从探索转向利用
```

**教训：** 通用起点 ε=0.1。如果不确定，先跑 ε=0.1，再试 ε=0.01 和 ε=0.3 做对比实验。

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.2 §2.2

---

## 坑 4: Q 值初始化为 0 导致探索不足

**痛点类别：** #2 上课念PPT（老师不讲的重要细节）

**场景：** 所有 Q 值初始化为 0，在奖励全为正的环境中

**症状：** Agent 选了第一个动作得到正奖励后，其他动作的 Q 值还是 0，Agent 就一直选第一个动作，不再探索

**根因：** 初始值相当于"初始偏好"。如果初始值低于环境平均奖励，第一个被选中的动作会持续被选中——因为它的估计值被正奖励抬高了，其他还是 0

**解法：**

❌ 错误做法 — 全零初始化在正奖励环境中

```python
# ❌ 在奖励 ~ N(5, 1) 的环境中，Q 初始化为 0
Q = np.zeros(k)  # 第一个被选中的动作 Q 被拉到 ~5，其他还是 0
```

✅ 正确做法 — 乐观初始化

```python
# ✅ 乐观初始化：Q 值设得比真实值高，鼓励 Agent 探索每个动作
Q = np.ones(k) * 10  # 初始值 10 >> 真实均值，Agent 会逐个"失望"
# "每个动作都先试试，发现没那么好后才收敛"
```

**教训：** 乐观初始化是最简单的探索技巧——让 Agent 一开始"以为每个动作都很好"，自然会去试每一个。

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.2 §2.6

---

## 坑 5: 在非平稳环境用 1/n 步长

**痛点类别：** #7 越学越怀疑自己

**场景：** 环境的奖励分布会随时间变化（非平稳），但你用的是 1/n 步长更新

**症状：** Agent 前期学得好，后期环境变了但 Agent 不再适应——因为步长越来越小，新数据几乎不影响估计

**根因：** 1/n 步长给旧数据和新数据相同权重，适合平稳环境。非平稳环境需要"忘记"旧数据，给新数据更大权重

**解法：**

❌ 错误做法 — 非平稳环境用 1/n

```python
# ❌ 非平稳环境中 1/n 步长：经过 10000 步后，步长 = 0.0001
# 新数据几乎不影响 Q 值，Agent 无法适应变化
N[a] += 1
Q[a] += (1 / N[a]) * (r - Q[a])
```

✅ 正确做法 — 用固定步长 α

```python
# ✅ 固定步长 α = 0.1：始终给新数据 10% 的权重
# 相当于指数加权平均，自动"遗忘"旧数据
alpha = 0.1
Q[a] += alpha * (r - Q[a])
```

**教训：** **平稳环境用 1/n，非平稳环境用固定 α**。不确定时先用固定 α=0.1，它在平稳环境下也不差。

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.2 §2.5

---

## 超级避坑指南

### 学习避坑

1. [ ] **别用 SL 框架套 RL** → RL 没有标签，核心是"试错→反馈→改进"循环
2. [ ] **分清 r 和 G** → r 是单步，G 是未来总和，Agent 最大化 G
3. [ ] **先理解多臂赌博机再学 MDP** → Bandit 是 RL 的最简形式，跳过它容易后面全懵
4. [ ] **别死记公式** → 先用白话理解"在干什么"，再看数学
5. [ ] **γ 的意义** → 不是"衰减"是"多重视未来"，γ=0 只看眼前，γ=1 完全远视

### 作业/项目避坑

1. [ ] **先跑最简代码** → 不要一上来就搞 DQN，先把 10-arm bandit 跑通
2. [ ] **画学习曲线** → 每个实验都画 average reward vs steps，一眼看出有没有收敛
3. [ ] **多次独立实验取平均** → 单次实验方差太大，至少 200 次 runs
4. [ ] **设随机种子** → 保证可复现

### 考试/答辩避坑

1. [ ] **RL vs SL 区别** → 必考题，从"反馈信号、数据来源、时间依赖"三个维度答
2. [ ] **解释 ε-greedy 的原理** → 画概率流程图最清楚
3. [ ] **增量更新公式推导** → 从样本均值推到递推形式，3 步就推完

### 调试清单（技术类）

1. [ ] **Q 值不收敛？** → 检查步长、初始化、ε 值
2. [ ] **性能突然下降？** → 环境可能非平稳，换固定步长 α
3. [ ] **Agent 只选一个动作？** → 检查初始化是否乐观，ε 是否 > 0
4. [ ] **学习曲线震荡？** → ε 可能太大，或步长 α 太大
5. [ ] **结果不可复现？** → 设 `np.random.seed(42)` 固定种子

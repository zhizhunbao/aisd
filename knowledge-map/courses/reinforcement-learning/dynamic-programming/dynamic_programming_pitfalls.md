---
topic: dynamic-programming
dimension: pitfalls
created: 2026-03-19
last_verified: 2026-03-19
source_versions:
  - "📚 Book: Sutton & Barto, 《Reinforcement Learning: An Introduction》 2nd Ed. Ch.4 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/sutton_barto_rl_intro.pdf"
  - "🧪 经验: 常见 DP 实现错误总结"
expiry: 6m
status: current
---

# 动态规划 踩坑记录

> ⚠️ **围绕学习痛点组织**，不是技术 debug 日志。每次踩坑后请追加条目。

---

## 坑 1: 混淆贝尔曼期望方程和最优方程

**痛点类别：** #5 名词多黑话多

**场景：** 实现策略评估时用了 max（该用 Σπ），或实现值迭代时用了策略概率加权（该用 max）

**症状：** 策略评估不收敛到 V^π，或值迭代收敛到错误的 V*

**根因：** 两个贝尔曼方程形式相似但含义完全不同——期望方程评估给定策略，最优方程求最优策略

**解法：**

❌ 错误做法 — 策略评估用 max

```python
# ❌ 策略评估里不该用 max！这是值迭代的公式
V[s] = max(sum(p * (r + gamma * V[s_next]) for s_next, r, p in transitions(s, a))
           for a in actions)
```

✅ 正确做法 — 策略评估用策略概率加权

```python
# ✅ 策略评估：按 π(a|s) 加权
V[s] = sum(policy[s, a] * sum(p * (r + gamma * V[s_next])
           for s_next, r, p in transitions(s, a))
           for a in range(n_actions))
```

**教训：** 记住：**评估用 Σπ，优化用 max**。写代码前先问自己"我在评估还是在优化"。

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.4 §4.1 vs §4.4

---

## 坑 2: 同步更新时混用新旧值

**痛点类别：** #2 上课念PPT（老师不讲的重要细节）

**场景：** 策略评估中更新 V(s) 后，立即用新值更新其他状态——这是异步更新，不是同步更新

**症状：** 结果可能与教科书不一致（虽然异步更新也能收敛，但收敛行为不同）

**根因：** 同步更新要求一轮中所有状态都用旧值计算新值，一轮结束后才替换。如果 in-place 更新，部分状态用了新值部分用旧值，是异步行为

**解法：**

❌ 错误做法 — 以为 in-place 就是同步更新

```python
# ❌ 用一个数组 in-place 更新 → 实际是异步更新
for s in range(n_states):
    V[s] = sum(...)  # 后续状态更新时读到的 V 已经被改过了
```

✅ 正确做法 — 用两个数组实现同步更新

```python
# ✅ 同步更新：读旧写新
V_new = np.copy(V)
for s in range(n_states):
    V_new[s] = sum(...)  # 全部用 V（旧值）计算
V = V_new  # 一轮结束后一次性替换
```

**教训：** **同步更新 = 双数组（读旧写新），异步更新 = 单数组（in-place）**。两种都收敛，但要明确自己在用哪一种。

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.4 §4.5

---

## 坑 3: 忘记跳过终止状态

**痛点类别：** #1 只甩任务不教思路

**场景：** 策略评估或值迭代时，对终止状态也做了更新

**症状：** 终止状态的 V 值不为 0，导致整个值函数错误

**根因：** 终止状态定义上 V(terminal) = 0，不需要更新。如果对终止状态做贝尔曼更新，会算出非零值

**解法：**

❌ 错误做法 — 不跳过终止状态

```python
# ❌ 对所有状态更新，包括终止状态
for s in range(n_states):
    V[s] = ...  # 终止状态也被更新了，V ≠ 0
```

✅ 正确做法 — 跳过终止状态

```python
# ✅ 终止状态不更新
for s in range(n_states):
    if s in terminal_states:
        continue  # V(terminal) 永远是 0
    V[s] = ...
```

**教训：** **终止状态 V=0 是定义，不是计算结果**。在循环开头加 `if s in terminal: continue`。

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.4 Example 4.1

---

## 坑 4: θ 阈值设太大导致"伪收敛"

**痛点类别：** #7 越学越怀疑自己

**场景：** 设 θ=0.1 做收敛检测，算法很快停了但值函数很粗糙

**症状：** 值迭代 3 轮就"收敛"了，但提取的策略是错的

**根因：** θ 太大时，值函数还没有稳定就被误判为收敛。特别是 γ 接近 1 时，值的传播很慢，初期变化就很小

**解法：**

❌ 错误做法 — θ 太大

```python
# ❌ θ=0.1 太大，值函数还远未收敛
theta = 0.1  # 3 轮就停了，策略全是错的
```

✅ 正确做法 — θ 足够小

```python
# ✅ θ=1e-4~1e-8 是常用范围
theta = 1e-6  # 保守但准确

# 也可以用相对变化检测
if delta / (abs(V[s]) + 1e-10) < theta:  # 避免除以零
```

**教训：** **通用起点 θ=1e-4**。如果结果看起来不对，试 θ=1e-8。宁可多跑几轮也不要提前收敛。

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.4 §4.4

---

## 坑 5: 策略改进时没处理多个最优动作的 tie

**痛点类别：** #2 上课念PPT（老师不讲的重要细节）

**场景：** 多个动作的 Q 值完全相同，但你只选了第一个

**症状：** 策略不对称（比如 GridWorld 中上和左都是最优但只选了上），收敛检测不稳定

**根因：** `np.argmax()` 在多个最大值中只返回第一个，导致策略有偏

**解法：**

❌ 错误做法 — 用 argmax 忽略 tie

```python
# ❌ 只选第一个最大值，忽略其他同样好的动作
best_action = np.argmax(q_values)
policy[s] = 0
policy[s, best_action] = 1.0  # 如果有 tie，其他最优动作概率为 0
```

✅ 正确做法 — 在所有最优动作间均匀分配

```python
# ✅ 找所有最优动作，均匀分配概率
best_actions = np.where(q_values == q_values.max())[0]
policy[s] = 0
policy[s, best_actions] = 1.0 / len(best_actions)
```

**教训：** **用 `np.where` 找所有 max 索引，不要只用 `np.argmax`**。特别是在对称环境（如 GridWorld）中。

---

## 超级避坑指南

### 学习避坑

1. [ ] **先理解策略评估，再理解策略迭代** → 评估是迭代的内循环
2. [ ] **画贝尔曼方程的 backup diagram** → 一个状态→所有动作→所有后续状态，手画一遍就理解了
3. [ ] **手算 2-3 步迭代** → 用 2×2 GridWorld 手算，比直接跑代码理解深
4. [ ] **图解同步 vs 异步** → 画更新顺序图，标出哪些值是"新"的

### 作业/项目避坑

1. [ ] **先在 4×4 GridWorld 验证** → 有标准答案（Sutton & Barto Example 4.1）
2. [ ] **打印每轮 Δ** → 看收敛曲线，有没有单调下降
3. [ ] **对比策略迭代和值迭代的结果** → 两者应该得到相同的 V* 和 π*

### 考试/答辩避坑

1. [ ] **策略迭代 vs 值迭代区别** → 必考题，从"评估步数"和"使用方程"两个角度答
2. [ ] **手写策略评估伪代码** → 两层循环：外层迭代，内层遍历状态
3. [ ] **解释 DP 为什么需要模型** → 因为更新公式里有 P(s'|s,a) 和 R

### 调试清单（技术类）

1. [ ] **V 值不收敛？** → 检查是否更新了终止状态、θ 是否太大
2. [ ] **值全是 0？** → 检查奖励是否正确传入，γ 是否为 0
3. [ ] **策略不收敛？** → 检查是否处理了 argmax tie
4. [ ] **结果不对称？** → 检查是否同步更新，或 tie 处理
5. [ ] **速度太慢？** → 试异步更新或截断策略评估

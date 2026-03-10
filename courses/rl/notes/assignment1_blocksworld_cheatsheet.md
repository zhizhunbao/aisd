# Assignment 1 Blocks World — 概念速查 (Cheat Sheet)

> **See also:** [数学公式](assignment1_blocksworld_math.md) | [代码参考](assignment1_blocksworld_code.md) | [故事线](assignment1_blocksworld_storyline.md) | [教程](assignment1_blocksworld_tutorial.md)
> **Sources:** Assignment 文档 + Quiz 2 + Quiz W3 + Quiz 4 + Sutton §3.1, §6.5 + Week 2-5 Notes

---

## 📖 核心概念定义

### 1. Blocks World MDP 五元组 (📚 Sutton §3.1)

| MDP 元素          | 符号            | BlocksWorld 具体值     |
| ----------------- | --------------- | ---------------------- |
| **状态集** $S$    | `states_dict`   | v0: ~13个, v1: ~169个  |
| **动作集** $A$    | `actions_dict`  | N 个 `move(X,From,To)` |
| **转移** $P$      | Prolog `step/1` | **确定性** (非随机)    |
| **奖励** $R$      | Python 计算     | -1 / -10 / +100        |
| **折扣** $\gamma$ | 超参数          | 通常 0.99              |

> 📚 Quiz 2 Q4: MDP 是 RL 的数学模型 (答案 A)

### 2. 状态编码

| 编码         | 含义                      | 图示     |
| ------------ | ------------------------- | -------- |
| `'123'`      | A@位置1, B@位置2, C@位置3 | 全在桌面 |
| `'bc2'`      | A@B上, B@C上, C@位置2     | 三层塔   |
| 数字 `1,2,3` | 桌面位置编号              |          |
| 字母 `a,b,c` | 在积木 A/B/C 上面         |          |

### 3. 两版环境对比

| 维度             | BlocksWorld-v0        | BlocksWorld-v1          |
| ---------------- | --------------------- | ----------------------- |
| 状态编码         | 3位（当前）           | 6位（当前+目标）        |
| 状态数           | ~13                   | ~169 (13×13)            |
| 目标             | 固定                  | 随机（每 episode 不同） |
| Markov性         | ❌ 违反（目标未编码） | ✅ 满足                 |
| Prolog `state/1` | 原始 3 位             | 修改为 6 位（拼接）     |

> 📚 Quiz 2 Q3: Markov 性 = "后续状态不依赖先前状态" (答案 E)
> 📚 Quiz 4 Q6: "Don't break the Markov assumption" — v1 修复了 v0 的 Markov 违反

### 4. 空间与 Policy 对应

| 空间类型      | SB3 Policy         | 📚 来源          |
| ------------- | ------------------ | ---------------- |
| `Discrete(n)` | `MlpPolicy`        | Quiz W3 Q4       |
| `Dict({...})` | `MultiInputPolicy` | Quiz W3 Q4       |
| `Box(H,W,C)`  | `CnnPolicy`        | Week 3 教程 §5.2 |

> ⚠️ BlocksWorld 用 `Discrete` → `MlpPolicy` ✅ (不是 `MultiInputPolicy` ❌)

---

## 💡 要点 (Key Points)

### 映射字典方向 (Assignment §4c-d)

| 字典           | 方向          | 用途                 | 原因                                      |
| -------------- | ------------- | -------------------- | ----------------------------------------- |
| `states_dict`  | **str → int** | Prolog状态 → Gym观测 | Gym 需要整数                              |
| `actions_dict` | **int → str** | Gym动作 → Prolog命令 | Prolog 需要字符串                         |
| 反向查找       | **int → str** | 渲染时用             | `list(keys())[list(values()).index(int)]` |

### Prolog 交互规则 (Assignment §4b)

| 规则     | 正确 ✅                                    | 错误 ❌                               |
| -------- | ------------------------------------------ | ------------------------------------- |
| 查询语法 | `query('state(S)')`                        | `query('state(S).')` — 不加句号!      |
| 加载文件 | `query('[blocks_world]')`                  | `query('blocks_world')` — 需要方括号! |
| 复合结构 | `{'functor':'move', 'args':['a','b','c']}` | 不是字符串 `'move(a,b,c)'`            |

### 奖励设计 (📚 Sutton §3.2 + Quiz 4 Q8)

| 事件       | 奖励 | 理论依据                                         |
| ---------- | ---- | ------------------------------------------------ |
| 合法移动   | -1   | 📚 Sutton §3.2: 负奖励鼓励最短路径 (Week 2 §1.1) |
| 不合法移动 | -10  | 📚 Quiz 4 Q8: shaped reward 惩罚不良行为         |
| 到达目标   | +100 | 📚 Quiz 2 Q5: 奖励假说 — 最大化累积标量奖励      |

### Gymnasium 返回值 (📚 Quiz W3 Q2, Q5)

| 方法         | 返回                                         | Quiz 来源                     |
| ------------ | -------------------------------------------- | ----------------------------- |
| `reset()`    | `(obs: int, info: dict)`                     | Quiz W3: reset 返回 2 值      |
| `step(a)`    | `(obs, reward, terminated, truncated, info)` | Quiz W3 Q2: **5 个值**        |
| `terminated` | 任务自然结束                                 | Quiz W3 Q5: 到达目标          |
| `truncated`  | 超时截断                                     | Quiz W3 Q10: 应继续 bootstrap |

### Q-Learning 条件 (📚 Quiz 2 Q13)

| 条件       | 是否满足 | 如何满足                   |
| ---------- | -------- | -------------------------- |
| 完整状态集 | ✅       | `states_dict` from Prolog  |
| 完整动作集 | ✅       | `actions_dict` from Prolog |
| 可交互     | ✅       | Prolog `step/1`            |
| 有奖励信号 | ✅       | Python 计算                |

> 📚 Quiz 2 Q13 答案 D: 需要完整状态集**和**动作集

---

## ⚠️ 陷阱 (Traps)

### 🪤 Trap 1: Policy 选择错误 (📚 Quiz W3 Q4)

- **错误:** `DQN("MultiInputPolicy", env)` — Dict 才用 MultiInputPolicy
- **正确:** `DQN("MlpPolicy", env)` — Discrete 观测用 MlpPolicy
- **来源:** Quiz W3 Q4 + Week 3 教程 §5.2

### 🪤 Trap 2: 映射方向混淆 (Assignment §4c-d)

- **错误:** 把两个字典当同方向
- **正确:** `states_dict` 是 str→int (查状态), `actions_dict` 是 int→str (查动作)
- **记忆法:** 每个字典的 key 是"输入端"需要的格式

### 🪤 Trap 3: Prolog 查询加句号 (Assignment §4b)

- **错误:** `query('state(S).')`
- **正确:** `query('state(S)')` — swiplserver 自动加句号
- **来源:** Assignment §4b 明确说明

### 🪤 Trap 4: v1 状态拼接 (Assignment §6 Note 2)

- **错误:** 用 Prolog 返回的 3 位状态直接查 6 位的 `states_dict`
- **正确:** 当前3位 + 目标3位 → 6位 → 查字典
- **理论:** 📚 需要包含目标以满足 Markov 性 (Quiz 2 Q3)

### 🪤 Trap 5: step() 返回 False 的处理 (Assignment §6b)

- **错误:** 忽略 Prolog 返回 False（不合法动作时状态不变!）
- **正确:** False → **状态保持不变**, 奖励 = -10

### 🪤 Trap 6: Temporal "Distance" vs "Difference" (📚 Quiz 2 Q14)

- **错误:** 认为 B/C/D 选项正确 — 概念描述看似对,但术语错误
- **正确:** 答案 E (None) — 正确术语是 **Temporal Difference**, 不是 Temporal Distance
- **来源:** Quiz 2 Q14 — 经典术语陷阱题

### 🪤 Trap 7: Policy 和 Value Function 的归属 (📚 Quiz 2 Q15)

- **错误:** 认为 Value Function 在 Environment 中
- **正确:** Policy π 和 V/Q 都在 **Agent** 中。Environment 只负责 P(s'|s,a) 和 R
- **来源:** Quiz 2 Q15 答案 A

### 🪤 Trap 8: 超参数截图要求 (Assignment Submission)

- **错误:** 只截一张图
- **正确:** "Original Hyperparameters" 基线 + **至少3组不同超参数** = 至少4张截图
- **来源:** Assignment "Add at least three new screenshots"

---

## 📊 对比表 (Compare)

### Lab 2 vs Assignment 1 — 完整对照

| 维度       | Lab 2 CliffWalking    | Assn 1 BlocksWorld          |
| ---------- | --------------------- | --------------------------- |
| 后端       | Python                | **Prolog (swiplserver)**    |
| 状态类型   | `Dict{agent, target}` | **`Discrete` 整数**         |
| 状态计算   | `y * xsize + x`       | **直接用** (更简单!)        |
| 动作数     | 4 (上下左右)          | **N (from Prolog)**         |
| 渲染       | PyGame 网格           | **PyGame 积木 (screen.py)** |
| SB3 Policy | `MultiInputPolicy`    | **`MlpPolicy`**             |
| Markov 性  | ✅ (坐标包含全部信息) | v0: ❌ / v1: ✅             |

### 三种算法对比 (📚 Quiz W3 Q8 + Week 5 故事线)

| 算法           | 类型                       | 实现         | BlocksWorld 预期效果 |
| -------------- | -------------------------- | ------------ | -------------------- |
| **Q-Learning** | Off-policy, Tabular        | 手写 Q-table | ✅ 最好 (状态空间小) |
| **DQN**        | Off-policy, Value-based    | SB3          | ⚠️ 一般 (过于复杂)   |
| **PPO**        | On-policy, Policy Gradient | SB3          | ⚠️ 一般 (不如表格)   |

> 📚 Week 5 DQN 故事线 §1: DQN 的优势在大状态空间。BlocksWorld 只有 13/169 个状态, 表格方法精确覆盖。

### On-policy vs Off-policy (📚 Week 2 MDP 故事线 §2)

|                       | Q-Learning            | SARSA                 |
| --------------------- | --------------------- | --------------------- |
| **更新目标**          | $\max_{a'} Q(S', a')$ | $Q(S', A')$           |
| **策略类型**          | **Off-policy**        | On-policy             |
| **学习的策略**        | Greedy (总选 max)     | ε-greedy (含探索风险) |
| **CliffWalking 路径** | 贴崖最短路            | 远离悬崖保守路        |

---

## 🔄 提交工作流程

```
Phase 1: 环境构建
├── 复制 GridWorld → BlocksWorld (重命名类/包/ID)
├── pip install -e .
├── Prolog 集成 (PrologMQI + states_dict + actions_dict)
├── 定义 spaces (Discrete)
└── Null Agent 测试 ✓

Phase 2: Q-Learning
├── 从 Lab 2 复制 + 适配 (Dict→int 简化)
├── 训练 + 记录 episode_rewards/steps
├── 绘图 "Original Hyperparameters" → 截图 1
├── 超参数实验 × 3 → 截图 2/3/4
└── screenshots/ 文件夹 ✓

Phase 3: BlocksWorld-v1
├── Prolog: state_helper + 6位 state
├── Python: reset 时取后3位目标, step 时拼接6位
└── 验证 Markov 性 ✓

Phase 4: Stable-Baselines3
├── DQN("MlpPolicy", env) → 可运行
├── PPO("MlpPolicy", env) → 可运行
└── 记录结果 ✓

Phase 5: 提交
├── Git commit (有意义的 messages)
├── screenshots/ 包含 ≥4 张
├── 虚拟环境未提交
└── 代码有注释 (Assignment §4d 要求) ✓
```

---

## 📚 Quiz 考点速查（与 Assignment 相关）

| Quiz 题号  | 考点                                    | Assignment 中的对应                        |
| ---------- | --------------------------------------- | ------------------------------------------ |
| Quiz 2 Q2  | Agent + Environment + Reward 三要素     | BlocksWorld 设计分离了三者                 |
| Quiz 2 Q3  | Markov 性                               | v1 扩展修复了 v0 的 Markov 违反            |
| Quiz 2 Q5  | 奖励假说                                | 奖励设计 -1/-10/+100                       |
| Quiz 2 Q7  | γ 解决无穷回报                          | γ=0.99 的选择                              |
| Quiz 2 Q12 | Greedy = 即时奖励优先                   | ε-greedy 中 greedy 部分 = argmax Q         |
| Quiz 2 Q13 | Q-Learning 需要完整 S 和 A              | states_dict + actions_dict                 |
| Quiz 2 Q14 | ⚠️ TD 不是 "Distance" 而是 "Difference" | 术语陷阱                                   |
| Quiz W3 Q2 | step() 返回 5 个值                      | (obs, reward, terminated, truncated, info) |
| Quiz W3 Q4 | Dict → MultiInputPolicy                 | BlocksWorld 用 Discrete → MlpPolicy        |
| Quiz W3 Q8 | DQN 只支持 Discrete 动作                | BlocksWorld 动作是 Discrete                |
| Quiz 4 Q3  | 保存所有实验参数                        | 截图标题标注超参数                         |
| Quiz 4 Q6  | 不违反 Markov 假设                      | v0→v1 扩展                                 |
| Quiz 4 Q8  | 简单奖励 + shaped rewards               | -1/-10/+100 组合                           |
| Quiz 4 Q9  | 算法需匹配动作空间                      | DQN 用于 Discrete                          |

---
name: learning-quiz-note-taking
description: 为各课程 quiz 文件补充结构化学习笔记（Answer + Explanation）。强调"为什么(Why)"帮助理解与记忆，按题目复杂度匹配解释深度。适用于用户要求"写 note/笔记"或整理 quiz 的答案解释。
---

# Quiz Note-Taking (General)

## Objectives

- 为 quiz 题目补充简洁、可复习的笔记
- 保持题干与选项不变，只新增 **Answer + Explanation**
- 中文为主，技术术语保留英文
- Explanation 必须包含 **Why（为什么）**
- **按题目复杂度匹配解释深度**，不对所有题一视同仁

## Scope

- 适用于 `courses/*/quizzes/` 下的 quiz 文件（规范拼写为 `quizzes/`，`quizes/` 为历史遗留，遇到时保持原路径不改名）
- 适用于选择题（MCQ）、判断题（T/F）、简答题（Short Answer）

## Workflow

1. **定位 quiz 文件**：在对应课程目录中找到 quiz 文件。
2. **阅读课程材料**：阅读对应课程的笔记/PPT/demo 代码，确保答案与解释有据可依。
3. **检测格式**：识别 quiz 文件采用的格式风格（见 [Format Detection](#format-detection)），后续笔记需匹配该格式。
4. **逐题检查**：确认每题是否已有 Answer/Explanation。
5. **判断深度**：根据题目复杂度决定解释深度（见 [Explanation Depth](#explanation-depth)）。
6. **补全结构**：每题后追加笔记（见 [Note Structure](#note-structure)）。
7. **术语一致**：保持与课程材料一致的术语、公式写法。

## Note Structure

每道题目下使用如下格式：

```markdown
> **Answer**: [选项字母/简短答案]
> **Explanation**:
> [中文解释，含 Why 推理、错因分析（按深度分级）]
> [涉及公式时附变量注释]
> **Key**: [English 核心定义 + 术语对照，1-2 行]
```

**要点**：
- 中文承载全部推理内容（Why + 错因分析）
- English 只保留**核心定义 + 关键术语对照**，不重复 Why 推理
- English 行以 `**Key**:` 开头，定位为"速查术语行"

## Explanation Depth

根据题目复杂度选择对应的解释深度：

### Tier 1 — 简单定义回忆

**特征**：答案是标准定义，干扰项明显荒谬或无关。

**处理**：一句定义 + Why + 弱干扰项合并带过。

```markdown
Question: What is Reinforcement Learning (RL)?
A) All of these answers.
B) RL is a third type of machine learning, along with supervised learning and unsupervised learning.
C) RL is a form of supervised machine learning used for learning to play games.
D) RL is a form of unsupervised machine learning used in control applications.
E) None of these answers.

> **Answer**: B
> **Explanation**:
> RL 是机器学习三大范式之一（监督/无监督/强化），通过智能体与环境的试错交互学习最优策略；**为什么是 B**：只有 B 正确定位了 RL 与其他两种范式的并列关系。C/D 错误地将 RL 归为监督或无监督的子类；A/E 因此不成立。
> **Key**: RL is the third ML paradigm alongside supervised and unsupervised learning.
```

### Tier 2 — 概念辨析 / 易混淆

**特征**：多个选项看似合理，需要区分细微差异。

**处理**：定义 + Why + **强干扰项单独一行说明**，弱干扰项可合并。

```markdown
Question: What is the difference between an action value function and a state value function?
A) None of these answers.
B) State value functions return total reward to termination, and action-value functions return immediate reward of taking the action.
C) State value functions take a state, and action value functions take just actions.
D) Action value functions return the average reward for taking an action, and State value functions return a state's average total future reward.
E) Action value functions take state-action pairs, whereas state value functions take just states.

> **Answer**: E
> **Explanation**:
> 核心区别在于输入：$V(s)$ 只接受状态，$Q(s,a)$ 接受状态-动作对；**为什么是 E**：E 准确描述了两者的输入差异。
>   - **B 错**：$V(s)$ 返回期望累积回报（非"到终止的总回报"），$Q(s,a)$ 也非"即时奖励"。
>   - **C 错**：$Q(s,a)$ 的输入是状态-动作对，不是"只有动作"。
>   - **D 错**："平均回报"不准确，$V$ 和 $Q$ 都是期望值。
>   - A 不成立（已有正确选项 E）。
>   - **$V(s)$**: 状态 → 期望回报 | **$Q(s,a)$**: 状态-动作对 → 期望回报
> **Key**: $V(s)$ takes states; $Q(s,a)$ takes state-action pairs. Both output expected cumulative return.
```

### Tier 3 — 公式推导 / 术语陷阱

**特征**：涉及公式理解、变量含义，或选项中藏有术语错误等陷阱。

**处理**：完整推理 + **逐项分析** + 公式变量行内注释 + 必要时指出陷阱机制。

```markdown
Question: Which of the following statements is true in the context of RL?
A) All of these answers.
B) Q-learning is a form of Temporal Distance (TD) learning.
C) Temporal Distance (TD) learning involves learning from differences in time steps as opposed to complete episodes.
D) Temporal Distance (TD) learning does not require that the agent have a model of the environment.
E) None of these answers.

> **Answer**: E
> **Explanation**:
> ⚠️ **术语陷阱**：所有选项使用了错误术语 "Temporal Distance"，正确术语是 **Temporal Difference (TD)**（时序差分）。
> **为什么是 E (None)**：B/C/D 的概念描述对 TD 而言部分成立，但术语错误（Distance ≠ Difference）导致全部无效。
>   - **B 错**：术语错误。若改为 TD，Q-learning 确实是 TD 的一种。
>   - **C 错**：术语错误。若改为 TD，TD 确实逐步更新而非等完整 episode。
>   - **D 错**：术语错误。若改为 TD，TD 确实是 model-free。
>   - A 因此不成立。
>   - **TD (Temporal Difference)**: 利用相邻时间步估计值差异进行学习
> **Key**: Correct term is **Temporal Difference** (not Distance). TD is model-free, step-by-step learning.
```

## Wrong Option Analysis

对错误选项的分析力度取决于干扰项的"迷惑性"：

| 类型 | 判断标准 | 处理方式 | 示例 |
|------|---------|---------|------|
| **强干扰项** | 看似合理，容易混淆 | 单独一行 `- **X 错**：...` | "$Q(s,a)$ 只取即时奖励"（容易与 $R$ 混淆） |
| **弱干扰项** | 明显荒谬或无关 | 合并为一句带过 | "橡胶涂层的链条" |
| **"None/All" 选项** | 取决于其他选项 | 一句话说明联动逻辑 | "A/E 因此不成立" |

## Special Patterns

### All of these (答案为 "All")

需要逐项证明每个选项**为什么对**，用 ✓ 标记：

```markdown
> **Answer**: C (All)
> **Explanation**:
> 贝尔曼方程将价值递归分解为即时奖励 + 折扣后继价值；**为什么是 C (All)**：B/D/E 都正确描述了贝尔曼方程的不同方面。
>   - **B ✓**：确实表达了当前值与后继值的关系。
>   - **D ✓**：确实将价值计算递归拆解为子问题。
>   - **E ✓**：Q-Learning 更新规则直接源自贝尔曼最优性方程。
>   - **$V(s) = \mathbb{E}[R + \gamma V(s')]$**: 贝尔曼方程
> **Key**: Bellman equation: value = reward + discounted successor value. Recursive, foundational to Q-Learning.
```

### None of these (答案为 "None")

需要说明每个选项**具体错在哪**（通常是因为共同的系统性错误）：

见上方 Tier 3 示例（术语陷阱）。

### True/False

选项统一使用 `A) True` / `B) False` 格式，答案写选项字母：

```markdown
Question: In a MDP, taking an action in a state always leads to the same result state.
A) True
B) False

> **Answer**: B
> **Explanation**:
> MDP 的转移由概率分布 $P(s'|s,a)$ 定义；**为什么是 B (False)**：同一状态-动作可到达多个后继状态，非确定性。A (True) 要求每次都到同一状态，与随机转移矛盾。
>   - **$P(s'|s,a)$**: 状态转移概率 (Transition probability)
> **Key**: MDP transitions are stochastic via $P(s'|s,a)$, not deterministic.
```

### Short Answer

```markdown
Question: Briefly explain why a discount factor $\gamma$ is used in RL.

> **Answer**: $\gamma \in [0,1)$ 降低未来奖励权重，使无限步回报收敛。
> **Explanation**:
> 在无限步任务中，不折扣的总回报 $\sum_{k=0}^{\infty} R_{t+k}$ 可能发散；**为什么需要 $\gamma$**：乘以 $\gamma^k$ 后几何级数收敛，策略可以比较。
>   - **$\gamma$**: 折扣因子 (Discount factor)，$0 \le \gamma < 1$
>   - **$G_t = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1}$**: 折扣回报 (Discounted return)
> **Key**: $\gamma$ ensures convergence of infinite-horizon returns via geometric discounting.
```

## Content Guidelines

- ✅ 只基于题干与课程材料，不引入外部知识
- ✅ 每题必须有 **Why** 推理
- ✅ 强干扰项需单独说明错因，弱干扰项合并带过
- ✅ 涉及公式的题目需给出标准表达和变量行内注释
- ✅ 术语陷阱题需用 ⚠️ 标记并指出正确术语
- ❌ 不修改题目、选项、分值格式
- ❌ 不添加与题干无关的扩展内容
- ❌ 不在纯概念题上强加公式注释

## Formatting Rules

- 使用 Markdown blockquote（`>`）包裹 Answer/Explanation
- 中文承载全部推理，English 行以 `**Key**:` 开头
- 公式使用 `$...$`
- 变量/函数名保持英文

## Format Detection

不同课程/老师的 quiz 文件可能采用不同格式，补笔记前需先识别并匹配：

| 格式风格 | 特征 | 笔记位置 | 示例课程 |
|---------|------|---------|---------|
| **Inline** | `Question N options:` + `A) B) C)...`，题目与选项连续排列 | 每题选项后紧跟 blockquote 笔记 | RL |
| **Checkbox** | `- [ ]` / `- [x]` 列表 + 底部 Answer Key | 保持 checkbox 不变，在底部 Answer Key 区追加 Explanation | ML |

**处理规则**：
- 识别文件格式后，笔记结构需与其一致，不要混用
- **Inline 格式**：Answer + Explanation 紧跟每题选项后，用 blockquote
- **Checkbox 格式**：不改动题目区的 `- [ ]`/`- [x]`，在底部 `Answer Key` 或 `Answer Key & Explanations` 区补充解释

## Quality Checklist

- [ ] 每道题都有 Answer + Explanation
- [ ] Explanation 包含 Why 推理
- [ ] 强干扰项有单独错因，弱干扰项已合并
- [ ] 涉及公式的题有变量行内注释
- [ ] 术语陷阱题有 ⚠️ 标记
- [ ] English `**Key**` 行只含定义和术语对照，无重复推理
- [ ] 解释深度与题目复杂度匹配（非所有题都 Tier 3）
- [ ] 公式与术语与课程材料一致

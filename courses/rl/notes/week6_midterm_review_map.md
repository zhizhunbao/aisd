# Week 6: 期中复习 学习地图

## 1. 核心问题

本讲（复习周）回答：
- 考试会考哪些内容，权重怎样？
- Q-Learning 公式中每个符号是什么，能手写推导吗？
- Off-policy 和 On-policy 的核心区别是什么？
- Gymnasium `step()` 5个返回值是什么，能写出来吗？
- SB3 最小训练流程（4步）能背出来吗？
- Q-table 初始化策略如何影响 exploration？

---

## 2. 全景位置

```
Week 1: RL 基础（Agent/Env/Reward/Policy/Return）
Week 2: MDP + Q-Learning（Q-table，Bellman 方程）
Week 3: Gymnasium（step 接口，Wrapper，观测空间）
Week 4: SB3（PPO/DQN API，VecEnv，Callback）
Week 5: DQN（三大创新，DiscreteActionWrapper）
  ↓ 全部考点汇总
Week 6 [你在这里]: 期中复习
  ↓
期中考试 → 后半学期（高级算法，项目）
```

这周没有新技术知识，目的是**建立跨周连接**，用优先级顺序高效复习。

---

## 3. 依赖地图

```
Week 6 依赖（复习所有前5周）：

Q-Learning [最高优先级]
  ├── Week 2: 公式来源
  ├── Week 5: DQN 是其扩展
  └── Week 6 Quiz: 几乎每题都涉及

Gymnasium API [第二优先级]
  ├── Week 3: step() / Wrapper / Spaces
  └── Week 4/5: SB3 和 DQN 都调用 Gymnasium

SB3 API [第三优先级]
  └── Week 4: 4步训练流程

RL 基础概念 [第四优先级]
  └── Week 1: On/Off-policy, Return, γ

后半学期延伸（本周不考但了解）：
  └── DQN 三大创新 → DDPG / PPO2 / A3C
```

---

## 4. 文件地图

> 本周没有新的学科内容——所有文件都是**指向前5周**的复习工具。

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [week6_midterm_review_concepts.md](week6_midterm_review_concepts.md) | **核心复习文件**：跨周高频考点速查 + 易错汇总 | 考前首选 |
| [week6_midterm_review_tutorial.md](week6_midterm_review_tutorial.md) | 深度解答考试模型答案（Q-Learning §3 详解） | 练题不会时 |
| [week6_midterm_review_slides.md](week6_midterm_review_slides.md) | 幻灯片笔记（老师的期中复习 PPT） | 首次系统复习 |
| [week6_midterm_review_storyline.md](week6_midterm_review_storyline.md) | 叙事：5周知识如何成为一条线 | 有遗忘感时 |
| [week6_midterm_review_math.md](week6_midterm_review_math.md) | 所有需要手写公式的集合 | 公式速查 |
| [week6_midterm_review_code.md](week6_midterm_review_code.md) | 考试可能要求写出的代码片段 | 代码速查 |
| [week6_midterm_review_history.md](week6_midterm_review_history.md) | 跨周历史综合（考试背景题） | 想看大图时 |
| [week6_midterm_review_quiz.md](week6_midterm_review_quiz.md) | **老师原版 Quiz**（来自 quize3.md） | 模拟考试 |

**前5周核心文件（复习时配合使用）：**

| 优先级 | 文件 | 复习要点 |
|--------|------|---------|
| ⭐⭐⭐ | [week2_mdp_concepts.md](week2_mdp_concepts.md) | Q-Learning 公式、Bellman、Off/On-policy |
| ⭐⭐⭐ | [week3_gymnasium_concepts.md](week3_gymnasium_concepts.md) | step() 5返回值、Wrapper |
| ⭐⭐ | [week4_sb3_concepts.md](week4_sb3_concepts.md) | 4步 SB3 API、算法选择 |
| ⭐⭐ | [week5_dqn_concepts.md](week5_dqn_concepts.md) | DQN 三大创新 |
| ⭐ | [week1_rl_intro_concepts.md](week1_rl_intro_concepts.md) | 基础术语定义 |

---

## 5. 学习路线

**考前 2 天（高效备考）：**
1. `week6_midterm_review_concepts.md` — 通读高频考点汇总（30分钟内完成）
2. `week6_midterm_review_quiz.md` — 做老师原版 Quiz（测试薄弱环节）
3. 针对薄弱点：回到对应 week 的 `concepts.md` 补强

**考前 1 天（查漏补缺）：**
1. `week6_midterm_review_math.md` — 确认会手写 Q-Learning 更新公式
2. `week6_midterm_review_code.md` — 确认会写 `step()` 调用和 SB3 训练流程
3. `week6_midterm_review_tutorial.md` §3 — 精读 Q-Learning 模型答案语言

**首次系统复习（时间充裕时）：**
1. `storyline.md` — 理解5周的叙事逻辑
2. 每周 `concepts.md`（按 Week1→5 顺序）
3. `quiz.md` 自测

---

## 6. 缺口检查

| 类型 | 状态 |
|------|------|
| 幻灯片笔记 | ✅ |
| 叙事线索 | ✅ |
| 核心概念（跨周汇总） | ✅ |
| 数学公式（汇总版） | ✅ |
| 代码参考（汇总版） | ✅ |
| 操作教程（模型答案） | ✅ |
| 历史背景（跨周综合） | ✅ |
| Quiz | ✅（来自老师原版 quize3.md） |
| 学习地图 | ✅（本文件） |

> **注意**：前5周的学习地图文件（week1-5 `_map.md`）已全部完成，期中复习可通过各周地图文件找到对应材料。

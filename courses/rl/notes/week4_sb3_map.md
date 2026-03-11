# Week 4: Stable Baselines3 学习地图

## 1. 核心问题

本讲回答：
- SB3 是什么，和手写 Q-Learning 的区别？
- 什么时候用 PPO，什么时候用 DQN/SAC？
- `learn()`、`predict()`、`save()`、`load()` 工作流是什么？
- `VecEnv` 和 `SubprocVecEnv` 有什么区别，何时使用？
- `BaseCallback` 怎么写，何时用？
- Policy 网络类型（`MlpPolicy` vs `CnnPolicy` vs `MultiInputPolicy`）如何选？

---

## 2. 全景位置

```
Week 3: Gymnasium 标准环境接口
  ↓ 接入工业级算法库
Week 4 [你在这里]: SB3（PPO / DQN / SAC 等）
  ↓ 深入其中一个算法
Week 5: DQN（SB3 内部原理揭秘）
  ↓
Week 6: 期中（SB3 API 是考点之一）
```

SB3 贯穿后半学期：Week 4 先学会用，Week 5 学懂 DQN 原理，Lab 3/4 持续使用。

---

## 3. 依赖地图

```
前置
  ├── Week 3: 已会写 Gymnasium 环境（SB3 直接消费 gymnasium.Env）
  ├── Week 1/2: Policy / Reward / Return 概念（SB3 训练的是 Policy）
  └── Python 面向对象（Callback 需要继承 BaseCallback）

Week 4 输出 → 被依赖 →
  ├── Lab 3: SB3 LunarLander-v2 训练
  ├── Week 5: DQN 原理 = SB3 DQN 实现的内部
  ├── Week 6: 考题会给 SB3 代码片段让你解释
  └── Assignment 2: 使用 SB3 完成主项目
```

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [week4_sb3_slides.md](week4_sb3_slides.md) | 幻灯片笔记：SB3 API、算法选择、VecEnv、评估 | 第一次学习 |
| [week4_sb3_storyline.md](week4_sb3_storyline.md) | 叙事：从手写到 SB3 的历史跨越 | 第一次学习 |
| [week4_sb3_concepts.md](week4_sb3_concepts.md) | 术语速查：算法对比表、Policy 类型、Callback 结构 | 复习 / 考前 |
| [week4_sb3_math.md](week4_sb3_math.md) | PPO 目标函数、GAE、Clip 参数 | 理解算法时 |
| [week4_sb3_code.md](week4_sb3_code.md) | 完整 SB3 训练 + 评估 + Callback 代码 | 做 Lab 3 / 作业时 |
| [week4_sb3_tutorial.md](week4_sb3_tutorial.md) | 操作教程：5 行训练到自定义 Callback | 做 Lab 3 前 |
| [week4_sb3_history.md](week4_sb3_history.md) | 历史：OpenAI Baselines → PPO → SB3 演进 | 想了解背景时 |
| [week4_sb3_quiz.md](week4_sb3_quiz.md) | 老师原版 Quiz（来自 quize4.md） | 自测 / 考前 |

---

## 5. 学习路线

**第一次学习：**
1. `storyline.md` — 理解为什么 SB3 是工业标准
2. `slides.md` — API 细节（重点：§3 算法对比，§4 VecEnv，§5 Callbacks）
3. `concepts.md` — 确认算法选择逻辑理解正确
4. `code.md` — 跑通 5 行 PPO 训练示例

**做 Lab 3 / Assignment 2：**
1. `code.md` — 复制训练模板，替换环境
2. `tutorial.md` — Callback 写法参考
3. `quiz.md` — 确认 API 用法无误

**期中备考：**
1. `concepts.md` — 算法对比表（On-policy vs Off-policy）
2. `quiz.md` — 练习考题风格
3. Week 6 期中复习文件中有 SB3 考点汇总

---

## 6. 缺口检查

| 类型 | 状态 |
|------|------|
| 幻灯片笔记 | ✅ |
| 叙事线索 | ✅ |
| 核心概念 | ✅ |
| 数学公式 | ✅ |
| 代码参考 | ✅ |
| 操作教程 | ✅ |
| 历史背景 | ✅ |
| Quiz | ✅（来自老师原版 quize4.md） |
| 学习地图 | ✅（本文件） |

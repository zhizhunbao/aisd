# Week 3: Gymnasium 学习地图

## 1. 核心问题

本讲回答：
- 如何创建一个符合 Gymnasium 标准的自定义环境？
- `reset()` 和 `step()` 的签名是什么，各返回什么？
- `terminated` 和 `truncated` 有什么区别？
- `Discrete` / `Box` / `Dict` 观测空间各用在什么场景？
- Policy 类型（`MlpPolicy` vs `MultiInputPolicy`）如何选？
- Gymnasium Wrapper 是什么，怎么用？

---

## 2. 全景位置

```
Week 2: Q-Learning 算法（手写环境类）
  ↓ 标准化接口
Week 3 [你在这里]: Gymnasium 自定义环境
  ↓ 连接工业工具
Week 4: SB3（PPO/DQN 直接用 Gymnasium 环境）
  ↓
Week 5: DQN + DiscreteActionWrapper（需要 Gymnasium Wrapper 知识）
  ↓
Week 6: 期中（Gymnasium 是考点之一）
```

Lab 2 直接在这里：把 Lab 1 的手写环境升级为 Gymnasium 标准接口。  
Assignment 1 也在这里：创建完整的 BlocksWorld Gymnasium 环境（含 Pygame 渲染）。

---

## 3. 依赖地图

```
前置
  ├── Week 1/2: Policy / Reward / State 概念
  ├── Week 2: 知道什么是 RL 环境（CliffWalking 示例）
  └── Python 面向对象（class 继承）

Week 3 输出 → 被依赖 →
  ├── Lab 2: CliffWalkingEnv 升级为 Gymnasium
  ├── Assignment 1: BlocksWorld-v0 自定义环境
  ├── Week 4/5: SB3 直接调用 Gymnasium 的 step()/reset()
  └── Week 5: DiscreteActionWrapper 是 Gymnasium Wrapper 的一种
```

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [week3_gymnasium_slides.md](week3_gymnasium_slides.md) | 幻灯片笔记：API、空间类型、Pygame、SB3 集成 | 第一次学习 |
| [week3_gymnasium_storyline.md](week3_gymnasium_storyline.md) | 叙事：为什么从手写环境升级到 Gymnasium | 第一次学习 |
| [week3_gymnasium_concepts.md](week3_gymnasium_concepts.md) | 术语速查：5 个返回值、空间类型、Policy 选择 | 复习 / 考前 |
| [week3_gymnasium_math.md](week3_gymnasium_math.md) | 空间大小公式、Dict 索引转换 | 做 Lab 2 时 |
| [week3_gymnasium_code.md](week3_gymnasium_code.md) | 完整环境模板代码 | 写 Lab 2 / Assignment 1 时 |
| [week3_gymnasium_tutorial.md](week3_gymnasium_tutorial.md) | 操作教程：从 step() 到完整环境 | 做 Lab 2 前 |
| [week3_gymnasium_history.md](week3_gymnasium_history.md) | 历史：ALE → OpenAI Gym → Gymnasium | 想了解背景时 |

> ⚠️ **没有 Quiz**：本周没有老师提供的原版 Quiz，不生成。

---

## 5. 学习路线

**第一次学习：**
1. `storyline.md` — 理解从手写到 Gymnasium 的动机
2. `slides.md` — API 接口细节（重点：§5 Gym→Gymnasium 迁移，§6 创建环境，§7 空间定义）
3. `concepts.md` — 确认 `terminated` vs `truncated` 理解正确
4. `code.md` — 看完整环境模板

**做 Lab 2 / Assignment 1：**
1. `code.md` — 复制环境模板，按需修改
2. `math.md` — Dict 观测索引转换
3. `tutorial.md` — 参考 CliffWalkingEnv 实现步骤

**期中备考：**
1. `concepts.md` — `step()` 5个返回值、空间类型、Wrapper 定义
2. Gymnasium 相关考点在 `week6_midterm_review_concepts.md` 中有汇总

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
| Quiz | ➖（无老师原版，不生成） |
| 学习地图 | ✅（本文件） |

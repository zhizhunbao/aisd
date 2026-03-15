---
topic: keras
dimension: history
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📖 Paper: Chollet, 'Keras', 2015 — https://arxiv.org/abs/1508.01211"
  - "📖 Docs: Keras 3 Official Blog — https://keras.io/keras_3/"
  - "📖 Docs: Keras 3 Announcement — https://keras.io/getting_started/"
  - "💻 Source: keras/keras GitHub — https://github.com/keras-team/keras"
expiry: never
status: current
---

# Keras 的故事线：从 API 包装器到多后端深度学习标准

> **核心主题：** 深度学习的「易用性革命」——如何让研究想法到可运行代码的距离从数天缩短到数分钟
> **故事线：** 一个不断追求「最低认知负荷」的 API 设计哲学如何在三次重大架构变革中存活并壮大

---

## 🎬 序幕：一切从什么问题开始？

### 一句话概括

> 2015 年，深度学习框架（Theano、Caffe、TensorFlow）功能强大但 API 极度复杂——搭建一个简单的 CNN 需要上百行模板代码，这严重阻碍了研究者的实验效率。

2014-2015 年是深度学习的"寒武纪大爆发"时期。AlexNet (2012) 证明了深度学习的威力，ImageNet 性能每年刷新。但当时的框架对用户极不友好：

- **Theano**：Python 式的符号计算图，debug 困难，错误信息晦涩
- **Caffe**：用 protobuf 定义网络结构，灵活性极低
- **TensorFlow 0.x**：刚发布，API 冗长，`tf.Session()` + `feed_dict` 模式让人头疼

一个研究者想测试一个简单的模型假设，光写代码就得花半天。François Chollet 在 Google 工作时深刻感受到这个痛点。

> 🔑 **问题提出：** 能不能设计一个 API，让"定义模型 → 训练 → 评估"像写伪代码一样简单？

---

## 📚 第一章：Keras 1.0 — 极简主义的诞生（2015-2017）

> **关键人物：** François Chollet (Google Brain 工程师)
> **关键论文：** [Chollet, "Keras", arXiv 2015](https://arxiv.org/abs/1508.01211)

### 发生了什么？

2015 年 3 月，François Chollet 在 GitHub 上发布了 Keras 的第一个版本。设计哲学是 **"Keras 是为人类设计的 API，不是为机器设计的"**：

- **核心创新**：`model.add()` → `model.compile()` → `model.fit()` 三步训练流程
- **后端支持**：最初支持 Theano 后端，很快增加了 TensorFlow 后端
- **一致性原则**：所有层有统一的输入/输出接口，所有模型有统一的训练接口

Keras 1.0 迅速获得社区认可，成为学术研究中最常被引用的深度学习工具之一。它的成功验证了一个关键假设：**开发者体验比性能更重要**（对大多数用户而言）。

### 为什么这很重要？

Keras 1.0 证明了"高层 API"的巨大价值——它不增加任何新的计算能力，但通过出色的 API 设计，将深度学习的准入门槛降低了一个数量级。这直接推动了深度学习在工业界的普及。

### 但还有一个问题……

Keras 作为独立包，与后端（Theano/TF）的集成不够紧密。用户经常遇到版本兼容性问题，且 Keras 缺乏与 TensorFlow 生态（TF Serving、TF Lite）的无缝衔接。

> 🔑 **故事转折点：** Google 注意到了 Keras 的成功，决定将其整合为 TensorFlow 的官方高层 API。

---

## 📚 第二章：tf.keras — 成为 TensorFlow 标准（2017-2023）

> **关键人物：** François Chollet (加入 TensorFlow 团队)
> **关键论文：** TensorFlow 2.0 White Paper, 2019

### 发生了什么？

2017 年，TensorFlow 宣布采纳 Keras 作为其官方高层 API（`tf.keras`）。2019 年 TensorFlow 2.0 发布时，`tf.keras` 成为 TF 2.0 的**唯一推荐 API**——原来的 `tf.layers`、`tf.estimator` 等逐步废弃。

关键变化：
- **Eager Execution 默认开启**：TF 2.0 抛弃了 `Session` 模式，默认使用即时执行（受 PyTorch 启发）
- **tf.keras 深度集成 TF 生态**：与 `tf.data`、`tf.distribute`、`tf.lite` 无缝配合
- **独立 Keras 包逐步停更**：`keras` PyPI 包指向 `tf.keras`，用户被引导到 TF 内部版本

### 为什么这很重要？

`tf.keras` 时期是 Keras 用户量的巅峰——它是全球使用最广泛的深度学习 API。几乎所有 TensorFlow 教程都以 `tf.keras` 为标准。学术论文中，Keras 的引用量超过了 PyTorch。

### 但还有一个问题……

与 TensorFlow 的深度绑定变成了双刃剑：
- **后端锁定**：`tf.keras` 只能在 TensorFlow 上运行，PyTorch 和 JAX 用户被排除在外
- **PyTorch 崛起**：研究社区大规模转向 PyTorch（因为它的灵活性和调试友好性）
- **JAX 的出现**：Google 内部 JAX 框架以其极致的性能（XLA + JIT + vmap）吸引了越来越多用户
- **碎片化**：同一个 "Keras" 品牌，但社区分裂为 TF 阵营和其他框架阵营

> 🔑 **故事转折点：** Chollet 做出了一个大胆决定——让 Keras 再次成为独立的多后端框架，同时支持 JAX、TensorFlow 和 PyTorch。

---

## 📚 第三章：Keras 3 — 多后端复兴（2023-至今）

> **关键人物：** François Chollet, Keras Team
> **关键论文：** [Keras 3 Announcement Blog](https://keras.io/keras_3/)

### 发生了什么？

2023 年底，Chollet 宣布了 Keras 3（最初称为 Keras Core）——一次彻底的重写：

- **多后端架构**：同一份 Keras 代码可以在 JAX、TensorFlow、PyTorch 上运行
- **`keras.ops` 抽象层**：提供 NumPy 兼容的跨后端操作 API
- **后端 Trainer 模式**：`Model` 类在运行时动态选择 `JAXTrainer` / `TensorFlowTrainer` / `TorchTrainer`
- **2024 年初正式发布 Keras 3.0**，后续增加 OpenVINO 支持

技术实现的核心创新：
```
keras.Model 继承链:
  Model → Trainer (基类) + Backend-Specific Trainer + Layer
         TensorFlowTrainer | JAXTrainer | TorchTrainer
```

这个架构允许用户「在 JAX 上用 TPU 训练 → 导出为 TF SavedModel 部署」，或者「用 PyTorch 的数据管道 → 用 Keras 的模型和训练 API」。

### 为什么这很重要？

Keras 3 解决了深度学习生态最根本的碎片化问题——它让模型代码**与框架解耦**。这在实际项目中有巨大价值：
- 研究团队可以在 JAX（训练最快）上开发，然后用 TF（部署最成熟）部署
- 教育场景不再需要"选择 PyTorch 还是 TensorFlow"——Keras 都支持
- 开源模型可以被更多人复用，因为不再绑定特定框架

### 但还有一个问题……

- 多后端的代价是**不能使用后端特有功能**（如 PyTorch 的自定义 CUDA kernel、JAX 的 pmap）
- 生态库（Keras Hub、Keras CV、Keras NLP）仍在追赶 Hugging Face 的覆盖面
- 部分 tf.keras 用户的迁移惯性——大量现有代码仍在 tf.keras 上

> 🔑 **故事转折点：** 深度学习正进入"后框架时代"——API 标准比框架更重要，Keras 3 正押注这个趋势

---

## 🗺️ 全局回顾：技术演进路线图

```
2015: Chollet                    Keras 1.0
      │                          (Theano/TF 后端, 极简 API)
      ▼
2017: Google + Chollet           tf.keras
      │                          (TF 官方高层 API)
      │
      ╳  分裂期 ── PyTorch 崛起, JAX 出现, TF 生态绑定
      │
      ▼
2023: Chollet + Keras Team       Keras 3 (Keras Core)
      │                          (多后端: JAX + TF + PyTorch)
      ▼
2024: Keras Team                 Keras 3.x
                                 (+ OpenVINO, + 量化, + Hub)
```

### 每一步升级解决了什么问题？

| 从 → 到 | 解决了什么核心问题？ |
|---------|---------------------|
| 原生框架 → Keras 1.0 | 深度学习 API 太复杂，需要数百行代码才能训练一个模型 |
| Keras 1.0 → tf.keras | Keras 与 TF 生态不够集成，缺少分布式训练和部署支持 |
| tf.keras → Keras 3 | TF 绑定导致后端锁定，无法利用 JAX/PyTorch 的优势 |

> 📖 Paper: Chollet, [Keras](https://arxiv.org/abs/1508.01211), 2015
> 📖 Docs: [Keras 3 Announcement](https://keras.io/keras_3/)
> 💻 Source: [keras](../../.github/keras/) — 全部源码

# Blackboard Flash Video — 需求文档

## 1. 项目概述

### 1.1 背景

当前 video-lego + video-content 体系已有 `split` 布局（左55%可视化 + 右45%要点），用于 5-7 分钟深度教育视频（如 KNN 视频）。

新需求：增加一种 **60 秒黑板快闪（Blackboard Flash）** 视频类型。

**标题风格**：《一分钟学会｜MIT 线性代数核心公式》

**平台机会**：
- **B站**：几乎无同风格内容，高级感知识快餐的稀缺品类
- **微信公众号/视频号**：完全空白，开创品类
- **抖音/快手**：红海，但我们用代码批量生成，成本碾压手工党

### 1.2 核心概念：知识单元（Knowledge Unit）

> ⚠️ **关键设计理念**：每个概念不是单独闪一个词/公式，而是作为「知识单元」**整体呈现**在一屏黑板上。

一个知识单元 = 一屏黑板，**同时展示**以下维度：

| 维度 | 示例（特征值） | 说明 |
|------|---------------|------|
| 🇨🇳 中文名 | 特征值 | 核心中文术语 |
| 🇺🇸 英文名 | Eigenvalue | 对应英文术语 |
| 🔄 同义词/别名 | 特征值 = 固有值 = Characteristic Value | 同一概念的不同叫法 |
| 📐 2D/3D 图解 | 向量被矩阵拉伸的动画 | SVG/动画可视化 |
| 📝 核心公式 | $Ax = \lambda x$ | LaTeX 公式 |
| 💡 一句话解释 | 矩阵作用后方向不变的向量 | 白话口语化 |

**节奏**：60 秒内展示 8-12 个知识单元，每个单元 4-6 秒。

### 1.3 目标

1. 在现有 Remotion 引擎上新增 `blackboard` 布局模式
2. 实现「知识单元」整体呈现的动画效果
3. 复用 knowledge-map 9 维知识体系作为内容源
4. 支持批量生成：输入知识点列表 → 自动产出 video.data.ts → Remotion 渲染

### 1.4 范围

- **在范围内**：
  - `BlackboardLayout` 新布局组件（Remotion）
  - `KnowledgeUnit` 新积木（整体呈现中英文+别名+图解+公式+释义）
  - 60 秒 video.data.ts 数据模板
  - 示例视频：MIT 线性代数（特征值、矩阵乘法、线性变换等）
- **不在范围内**：
  - AI 配音（已有 video-production workflow Phase 5）
  - 多平台自动发布
  - 真实 3D 渲染引擎（用 SVG 模拟 2D/伪3D）

---

## 2. 目标用户

### 2.1 用户画像

| 维度 | 描述 |
|------|------|
| 角色 | AI 视频编导（自己） |
| 场景 | 从 knowledge-map 选题 → 批量生成 60s 黑板快闪视频 |
| 痛点 | 手工在剪映做一条 30-60 分钟；公式排版痛苦；中英文+别名整理繁琐 |
| 期望 | 10 条 / 10 分钟，代码驱动批量生产 |

### 2.2 用户场景

1. 打开 knowledge-map/courses/linear-algebra/ 或 machine-learning/svm/
2. 阅读 `_math.md` + `_concepts.md` → 提取公式 + 关键词 + 中英文 + 别名
3. 编写 / 脚本生成 `video.data.ts`（知识单元数组）
4. `npx remotion preview` → 预览 60s 黑板快闪
5. `npx remotion render` → 输出 MP4

---

## 3. 功能需求

### 3.1 核心功能（Must Have / P0）

| ID | 功能 | 描述 |
|----|------|------|
| F-01 | `BlackboardLayout` 布局 | 全屏黑板风格，深灰/墨绿磨砂质感背景 |
| F-02 | `KnowledgeUnit` 积木 | 一屏展示：中文名 + 英文名 + 别名 + 公式 + 图解 + 释义 |
| F-03 | 中文关键词 flash | 大号思源黑体，居中弹出，是每屏的视觉主体 |
| F-04 | 英文对照 | 中文下方紧跟英文名，较小字号 |
| F-05 | 同义词/别名 | 显示「也叫：固有值 / Characteristic Value」 |
| F-06 | LaTeX 公式渲染 | KaTeX 渲染，公式区域带淡色背景卡片 |
| F-07 | 2D 图解 | SVG 或 React 组件，展示概念的几何直觉（如向量变换） |
| F-08 | 一句话释义 | 底部或旁侧，口语化白话解释 |
| F-09 | 逐元素入场动画 | 中文名先出 → 英文名跟入 → 别名淡入 → 图解展开 → 公式弹出 → 释义滑入 |
| F-10 | 整体出场动画 | 所有元素统一淡出/缩小，切到下一个知识单元 |
| F-11 | 时间轴驱动 | 每个知识单元有 `startSec` / `endSec`，与旁白同步 |
| F-12 | 字幕安全区 | 底部 15% 留给字幕（复用现有 Subtitle 组件） |

### 3.2 辅助功能（Should Have / P1）

| ID | 功能 | 描述 |
|----|------|------|
| F-13 | 竖屏支持 | 可配置 1080×1920 竖屏（抖音/视频号） |
| F-14 | 主题标题栏 | 顶部常驻显示「MIT 线性代数」课程名 + 进度（3/10） |
| F-15 | 转场动画 | 知识单元之间的切换效果（擦黑板/淡入淡出） |
| F-16 | 图解动画 | 2D 图解本身带动画（如向量从原点延伸、矩阵变换前后对比） |

### 3.3 批量生成（Should Have / P1）

| ID | 功能 | 描述 |
|----|------|------|
| F-17 | 批量数据生成 | Python 脚本，从 knowledge-map 提取 → 生成 video.data.ts |
| F-18 | knowledge-map 接入 | 自动读取 `_math.md`（公式）+ `_concepts.md`（术语/别名） |
| F-19 | 时间轴自动分配 | 60s / N 个单元，自动均分或按内容量加权 |

### 3.4 未来扩展（Could Have / P2）

| ID | 功能 |
|----|------|
| F-20 | 粉笔手写描边动画 |
| F-21 | 名校 Logo 水印（MIT/Stanford/CMU） |
| F-22 | 3D 图解（Three.js / React Three Fiber） |
| F-23 | AI 自动从教科书提取知识单元 |

---

## 4. 知识单元数据结构（核心设计）

```typescript
/** 一个知识单元 = 一屏黑板上的完整内容 */
interface KnowledgeUnitData {
  /** 中文核心术语 */
  zhName: string;             // '特征值'
  /** 英文对照 */
  enName: string;             // 'Eigenvalue'
  /** 同义词/别名列表 */
  aliases?: string[];         // ['固有值', 'Characteristic Value']
  /** LaTeX 核心公式 */
  formula?: string;           // 'Ax = \\lambda x'
  /** 公式标注 */
  formulaLabel?: string;      // '特征值定义'
  /** 2D/3D 图解组件名 */
  diagram?: string;           // 'EigenvalueDiagram'
  /** 一句话释义 */
  explanation: string;        // '矩阵作用后方向不变的向量'
  /** 时间轴 */
  startSec: number;
  endSec: number;
}
```

---

## 5. 视觉规范

### 5.1 黑板背景
- 颜色：`#1e2a1e`（墨绿）或 `#1a1a2e`（深灰，复用 THEME.bg）
- 质感：叠加细微噪点纹理
- 边框：无

### 5.2 排版
- 中文名：72px，白色，居中偏上，思源黑体加粗
- 英文名：36px，`#cccccc`，中文名正下方
- 别名：24px，`#888888`，英文名下方，格式 `也叫：xxx / yyy`
- 公式：居中，带 `rgba(255,215,0,0.08)` 背景卡片，金色边框
- 图解：右侧或中央偏右，最大高度 40%
- 释义：底部（字幕安全区上方），28px，`#f0f0f0`

### 5.3 动画节奏（单个知识单元 5 秒示例）
```
0.0s - 0.3s: 中文名淡入 + 缩放
0.3s - 0.6s: 英文名滑入
0.6s - 0.9s: 别名淡入
0.9s - 1.5s: 图解展开
1.5s - 2.0s: 公式弹入
2.0s - 2.3s: 释义滑入
2.3s - 4.5s: 全部停留（配合旁白）
4.5s - 5.0s: 整体淡出
```

### 5.4 配色
- 沿用 THEME 色系：gold `#ffd700`、blue `#4ea8de`、red `#e74c3c`、green `#2ecc71`
- 公式卡片边框：gold
- 图解描边：blue
- 释义文字：white

---

## 6. 非功能需求

### 6.1 性能
- 单条 60s 视频 Remotion 渲染 < 30 秒
- 批量 10 条 < 5 分钟

### 6.2 兼容性
- 复用现有 video-lego 积木系统（@blocks、@lego 别名）
- 不破坏现有 KNN 等 split 布局视频
- 新积木遵循 `.motion.tsx` / `.view.tsx` 分离模式

### 6.3 类型安全
- 扩展 `BlockDataMap` 注册新积木
- 扩展 `LayoutType` 增加 `'blackboard'`
- 扩展 `SceneData` 支持知识单元布局

---

## 7. 约束条件

- 技术栈：Remotion + React + TypeScript（已有）
- 字体：Noto Sans SC（正文）+ KaTeX（公式）
- 时长：严格 60 秒（±2 秒）
- 图解：纯 SVG/React 组件，不依赖外部图片

---

## 8. 验收标准

1. ✅ `npx remotion preview` 可预览「MIT 线性代数」60s 黑板快闪视频
2. ✅ 每个知识单元整体呈现：中文名 + 英文名 + 别名 + 公式 + 图解 + 释义
3. ✅ KaTeX 公式渲染正确，无 warning
4. ✅ 逐元素入场动画流畅，节奏感强
5. ✅ 60 秒内展示 8-12 个知识单元
6. ✅ 现有 KNN split 视频仍可正常预览/渲染
7. ✅ TypeScript 无编译错误

---

## 9. 内容示例：MIT 线性代数

| # | 中文 | English | 别名 | 公式 | 图解 |
|---|------|---------|------|------|------|
| 1 | 矩阵 | Matrix | — | $A_{m \times n}$ | 网格数组 |
| 2 | 矩阵乘法 | Matrix Multiplication | — | $C = AB$ | 行×列点积动画 |
| 3 | 线性变换 | Linear Transformation | 线性映射 | $T(x) = Ax$ | 网格变形动画 |
| 4 | 行列式 | Determinant | det | $\det(A) = ad - bc$ | 面积缩放动画 |
| 5 | 逆矩阵 | Inverse Matrix | $A^{-1}$ | $AA^{-1} = I$ | 变换→逆变换 |
| 6 | 特征值 | Eigenvalue | 固有值 | $Ax = \lambda x$ | 向量拉伸方向 |
| 7 | 特征向量 | Eigenvector | 固有向量 | $Ax = \lambda x$ | 不变方向 |
| 8 | 线性无关 | Linear Independence | — | $c_1v_1 + \cdots = 0$ | 向量不共线 |
| 9 | 基 | Basis | 基底 | $\text{span}(v_1, \ldots, v_n)$ | 坐标系 |
| 10 | 正交 | Orthogonal | 垂直 | $u \cdot v = 0$ | 90°向量 |
| 11 | SVD | Singular Value Decomposition | 奇异值分解 | $A = U\Sigma V^T$ | 旋转→缩放→旋转 |
| 12 | 最小二乘 | Least Squares | OLS | $\hat{x} = (A^TA)^{-1}A^Tb$ | 投影到列空间 |

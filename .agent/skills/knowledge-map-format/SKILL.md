---
name: knowledge-map-format
description: "知识地图文件格式模板与质量规范。Make sure to use this skill whenever generating knowledge map files via /generate-knowledge-map, reviewing or fixing knowledge map formatting issues, the user says \"格式不对\" or \"format template\" for knowledge map files, creating any of the 8 dimensions (Map/Concepts/Math/Tutorial/Code/Pitfalls/History/Bridge), or checking knowledge map quality. Also use when the user mentions \"知识地图\", \"知识库格式\", \"维度模板\", or asks about how to structure a knowledge map topic. Enforces consistent structure, mandatory source citations, and fixed chapter counts across all 8 dimensions."
---

# Knowledge Map Format Templates

> 本 Skill 定义 `/generate-knowledge-map` 生成的**每个维度文件的固定结构**。
> 模板从已验证的 `knowledge-map/deep-learning/cnn/` 系列文件提取，每个章节编号固定。

---

## 来源限制

知识地图的所有内容必须来自可信赖、可验证的来源。这确保知识库的长期可靠性。

### 允许的来源（白名单）及**引用优先级**

> ⚠️ **引用必须按优先级从高到低选择最权威的来源。低优先级来源只在更高级来源不可用时使用。**

| 优先级 | 来源类型 | 具体来源 | 说明 |
|-------|---------|---------|------|
| 🥇 **P1 最高** | 📖 学术原始论文 | arXiv, ACM, IEEE, NeurIPS, ICML, JMLR 等 | 第一手知识来源，最权威 |
| 🥈 **P2** | 📚 出版教科书 | 教材 PDF（引用具体章节+方程编号）| 系统整理，有同行评审 |
| 🥉 **P3** | 📖 官方文档 | scikit-learn docs, PyTorch docs, RFC, W3C… | 实现权威，但非算法权威 |
| 🔵 **P4 最低** | 💻 开源代码仓库 | GitHub: sklearn, numpy, huggingface… | 验证实现细节，补充文档 |

**规则**：每个知识声明优先引用 P1 论文；论文未涵盖时引用 P2 教科书；P1+P2 均无时才用 P3/P4。`source_versions` frontmatter 中，论文应**排在教科书之前**。

### 严禁的来源（黑名单）

| 严禁                       | 原因                                 |
| -------------------------- | ------------------------------------ |
| 教师 PPT / 课件 / 讲义     | 非权威，有简化或错误，无法被他人验证 |
| 课程作业题 / 考试题        | 同上                                 |
| 百度百科 / CSDN / 知乎博客 | 非同行评审，质量无保障               |
| 自己写的生成内容           | 循环引证，无意义                     |

---

## ⛔ 重入检查点（会话截断/Checkpoint 重启时强制执行）

> **这是防止格式错误的关键规则。上下文摘要信息不可信任，必须重新读取原始模板。**

每次使用本 Skill **之前**，无论是新会话还是断点恢复，**必须**先调用：

```
view_file(.agent/skills/knowledge-map-format/references/dimension_templates.md)
```

**禁止**依赖记忆或摘要中对模板结构的描述，因为：
- 章节计数（Map=8章、Concepts=4章、Math=5章 等）很容易在压缩摘要中丢失
- 核心属性、故事线格式、Frontmatter 裸 URL 等细节极易被遗漏
- 跳过此步骤是导致格式不合规的**唯一根本原因**

---

## 通用格式规则

以下规则适用于所有维度文件，确保知识库在格式上保持一致。

### R1. Frontmatter 格式

> ⚠️ **YAML 不渲染 Markdown 链接**：`[text](url)` 在 YAML 中只是纯字符串，无法点击。
> `source_versions` 必须使用**裸 URL**，VS Code 会自动高亮并允许 Ctrl+Click 跳转。

```yaml
---
topic: { topic_name }
dimension: { dimension } # map | concepts | math | tutorial | code | pitfalls | history | bridge
created: { YYYY-MM-DD }
last_verified: { YYYY-MM-DD }
source_versions:
  # 教科书：用 file:/// 绝对路径（VS Code 可 Ctrl+Click 直接打开 PDF）
  - "📚 Book: 作者, 《书名》 Ch.X — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/文件名.pdf"
  # 公开论文：用完整 https:// URL（VS Code 自动识别超链接）
  - "📖 Paper: 作者 会议/期刊 年份 — https://链接"
  # 官方文档：在线文档用完整 URL；已下载到本地用 file:/// 路径
  - "📖 Docs: 名称 章节 — https://链接"
  # 开源仓库：GitHub 链接
  - "💻 Source: 仓库名 文件:行号 — https://github.com/org/repo/blob/main/path/to/file.py"
  # 实践经验（仅 Pitfalls 维度）
  - "🧪 经验: 简短说明"
expiry: 3m # 3m | 6m | 12m | never
status: current # current | needs_review | outdated
---
```

### R2. 来源引证

每个 `##` 章节结尾必须有 `>` 引用块。格式严格为：

```
> 📚 Book: 作者, [《书名》](../../textbooks/文件名.pdf), Ch.X
> 📖 Docs: [名称](../../.documents/分类/文件) — 章节
> 📖 Paper: [简称](URL)；已下载到本地用 file:///
> 💻 Source: [仓库名](../../.github/仓库名/) `文件:行号`
> 🧪 经验: 简短说明
```

### R3. 代码块禁止嵌套

❌ **绝对禁止** ` ```markdown ` 中嵌套 ` ```bash ` — 会导致渲染崩坏。

替代方案：用 **4 空格缩进** 表示内层代码：

    ```bash
    npm run build
    ```

### R4. ❌/✅ 对比格式（Pitfalls 维度专用）

**在实际生成的 `.md` 文件中，❌/✅ 后面必须用语言标注的代码块（有语法高亮）：**

````markdown
❌ 错误写法 — 原因说明（一句话）

```python
# 错误的代码
bad_code()
```

✅ 正确写法 — 原因说明（一句话）

```python
# 正确的代码
good_code()
```
````

> ⚠️ **注意区分**：
> - 在**生成的 `.md` 文件正文**中：直接写 ` ```python ` 代码块，不需要缩进
> - 在**本 skill 文档内部嵌套展示**时（如上方示例）：才需要 4 空格缩进来避免渲染崩坏（R3）
> - ❌ **禁止**在实际 pitfalls 文件里用 4 空格缩进代替代码块——缺少语法高亮，体验差

### R4b. Pitfalls 维度结构规范

每个"坑"的结构严格固定（**加粗关键字 + 同行内容**，不用三级标题）：

````markdown
## 坑 N: {标题}

**场景：** 描述

**症状：** 用户看到的现象（如 `错误信息`）

**根因：** 为什么

**解法：**

❌ 错误写法 — 原因

```python
# 错误代码
```

✅ 正确写法 — 原因

```python
# 正确代码
```

**教训：** 一句话总结

> 📖 来源引证
````

### R5. 易混淆标注（Concepts 维度专用）

每个 `###` 术语条目，若存在**常见混淆点**，在定义段落后直接加：

```
> 易混淆：**概念A vs 概念B** — 一句话说清楚区别；再补一句为什么容易混
```

- 仅在真正存在混淆风险时写，不强制每个术语都有
- 语言：中文优先，技术术语保留英文

### R6. 分隔线

- `##` 章节之间用 `---` 分隔
- `###` 小节之间**不用** `---`

### R7. 标题后引证

每个文件 `# 标题` 下紧跟一行全局引证：

```
# {Topic} {维度名}

> 📚 Book: 作者, [《书名》](../../textbooks/文件.pdf), Ch.X
```

### R8. 素材目录规范

**工作区素材结构（固定）：**

| 来源类型       | 目录                         | 说明                                |
| -------------- | ---------------------------- | ----------------------------------- |
| 📚 教科书 PDF  | `textbooks/`                 | 原始 PDF，引用时必须链接到此目录    |
| 📚 MinerU 解析 | `data/mineru_output/{book}/` | 教科书的 MinerU 输出（.md + .json） |
| 💻 开源项目    | `.github/`                   | 参考代码仓库                        |
| 📖 官方文档    | `.documents/`                | 下载到本地的官方文档                |
| 📖 论文 PDF    | `.documents/papers/{topic}/` | 用 `download_papers.py` 下载到本地  |

---

## 维度模板（强制引用）

> 🚨 **所有维度的固定章节结构、frontmatter 示例、格式规则均在下方文件中定义。**
> **生成任何维度文件前，必须先读取此文件，严格按其中的模板执行。**

📖 **唯一格式来源：** [references/dimension_templates.md](references/dimension_templates.md)

该文件包含 **DIM-1 (Map) 到 DIM-9 (First Principles)** 的完整固定模板，基于 `knowledge-map/deep-learning/cnn/` 的实际格式写死。每个维度模板包括：

- 完整 frontmatter 示例
- 固定章节结构（章节名、顺序、数量不可改）
- 格式规则清单（✅ 必须 / ❌ 禁止）
- 质量检查清单

| DIM | 名称     | 章节数                        |
| --- | -------- | ----------------------------- |
| 1   | Map      | 8 章                          |
| 2   | Concepts | 4 章                          |
| 3   | Math     | 5 章                          |
| 4   | Tutorial | 6 Section + 参考来源表        |
| 5   | Code     | 4 章                          |
| 6   | Pitfalls | 坑 + 调试清单                 |
| 7   | History  | 序幕 + N章 + 全局回顾         |
| 8   | Bridge   | 6 章                          |
| 9   | First Principles | 5 章                  |

### 各维度固定章节概览

| DIM | 名称     | 固定章节                                                                 |
| --- | -------- | ------------------------------------------------------------------------ |
| 1   | Map      | 核心问题 → 全景位置 → 依赖地图 → 文件地图 → 学习路线 → 缺口检查 → 新鲜度 → 参考来源表 |
| 2   | Concepts | 术语定义（### 标题 + 段落 + `> 易混淆:`）→ 概念辨析表 → 核心属性(架构+适用/不适用) → 速查表 |
| 3   | **Math** | **符号对照表 → 核心公式(直觉+推导) → 公式关系图 → 手算练习 → 公式速查表** |
| 4   | Tutorial | Section 0(前置) → 1(Why) → 2(How) → 3(局限) → 4(对比) + 参考来源表      |
| 5   | Code     | 快速开始 → 完整实现示例 → API 速查 → 目录结构模板                        |
| 6   | Pitfalls | 坑(场景/症状/根因/解法/教训) + 调试清单                                  |
| 7   | History  | 🎬序幕 → 📚第N章(发生了什么/为什么重要/但还有问题+🔑转折) → 🗺️全局回顾  |
| 8   | Bridge   | ←/→导航表 → 上游依赖 → 下游影响 → 概念演变 → 📚扩展阅读 → 知识库关联   |
| 9   | First Principles | 核心问题链(5Why) → 公理与假设(陈述/白话/来源/可验证性) → 推导链(公理→技术) → 如果公理不成立 → 速查表 |

> 📖 See [references/dimension_templates.md](references/dimension_templates.md) for complete templates of all dimensions (based on CNN actual format).

---

## 论文下载工具

> 有 Paper 来源时，**优先下载到本地** `.documents/papers/{topic}/`，再用 `file:///` 路径引用。
> ⚠️ **下载失败时不阻塞生成流程**——见下方「下载失败处理规则」。

### 🥇 首选：arXiv 直接下载（无需 API Key，无限速）

```bash
# 知道 arXiv ID 时，直接用 --url 模式，完全免费，不经过 Semantic Scholar
python .agent/skills/knowledge-map-format/scripts/download_papers.py \
    --url "https://arxiv.org/abs/1410.5329" --topic naive_bayes \
    --filename raschka_2014_naive_bayes.pdf
```

### 🥈 次选：Semantic Scholar 关键词搜索（仅在不知道 arXiv ID 时使用）

> ⚠️ **--search 模式会调用 Semantic Scholar API，匿名状态下容易触发 429 限速。**
> 优先用 arXiv 搜索（arxiv.org）找到 ID 后，再用 --url 直接下载。

```bash
# 带 API Key 时（推荐先申请：https://www.semanticscholar.org/product/api#api-key）
python .agent/skills/knowledge-map-format/scripts/download_papers.py \
    --search "DBSCAN density based clustering" --topic dbscan \
    --api-key YOUR_KEY

# 或设置环境变量后省略 --api-key 参数
set S2_API_KEY=YOUR_KEY
python .agent/skills/knowledge-map-format/scripts/download_papers.py \
    --search "DBSCAN" --topic dbscan
```

**推荐平台（均免费）：**

| 平台                 | 特点                                | 适合场景                  |
| -------------------- | ----------------------------------- | ------------------------- |
| **Semantic Scholar** | 学术论文搜索 + open access PDF 直链 | 按标题/关键词找论文并下载 |
| **Papers With Code** | 论文 + 对应 GitHub 代码仓库         | 需要同时找论文和实现代码  |
| **arXiv**            | 预印本直接 PDF                      | 已知 arXiv ID 时最快      |

**使用方式（三选一）：**

```bash
# 1. 按关键词搜索并下载（Semantic Scholar）
python .agent/skills/knowledge-map-format/scripts/download_papers.py \
    --search "DBSCAN density based clustering" --topic dbscan

# 2. 搜索 + 显示 Papers With Code 结果
python .agent/skills/knowledge-map-format/scripts/download_papers.py \
    --search "DBSCAN" --topic dbscan --pwc

# 3. 从已有知识地图批量下载
python .agent/skills/knowledge-map-format/scripts/download_papers.py \
    --from-km knowledge-map/ml/dbscan/dbscan_map.md
```

---

## 📋 下载失败处理规则（必须遵守）

> **论文无法自动下载（无 open access、网络错误、脚本交互卡住等）时，不允许阻塞知识地图生成。**

### 处理步骤

1. **继续生成**：不等待、不暂停，立即继续当前维度文件的生成
2. **标注占位符**：在 `source_versions` frontmatter 和正文引证中，将该论文标注为：

   ```yaml
   - "📖 Paper: 作者, '论文标题', 刊物 年份 — ⚠️ 待下载 见 papers_index.md"
   ```

3. **写入 papers_index.md**：在知识地图目录下创建/追加 `papers_index.md`，记录该论文的完整信息：

   | 字段 | 内容 |
   |------|------|
   | 标题 | 完整论文标题 |
   | 作者 | 第一作者 et al. |
   | 年份 | 发表年份 |
   | 刊物 | 期刊/会议全名 + 卷期页 |
   | 重要性 | ⭐ 数量（1-5）+ 说明 |
   | 状态 | ⚠️ 待下载 |
   | 手动搜索链接 | IEEE Xplore / ACM DL / arXiv / Semantic Scholar 链接 |

4. **下载后更新**：用户手动下载后，将 `papers_index.md` 中的状态改为 `✅ 已下载`，并将各维度文件中的占位符替换为 `file:///` 绝对路径

### papers_index.md 格式模板

```markdown
# {Topic} 论文索引 / Papers Index

> ⚠️ 无法自动下载的重要论文。手动下载后放入 `.documents/papers/{topic}/`，并更新此文件的状态。

## 待下载论文

| # | 论文 | 作者 | 年份 | 刊物 | 重要性 | 状态 | 手动搜索链接 |
|---|------|------|------|------|--------|------|------------|
| 1 | 论文标题 | 作者 | 年份 | 刊物 卷(期):页 | ⭐⭐⭐⭐⭐ 说明 | ⚠️ 待下载 | [平台名](URL) |

## 手动下载说明

下载后放入：.documents/papers/{topic}/
命名格式：第一作者_年份_关键词.pdf
下载后更新状态为 ✅ 已下载，并替换各维度文件中的占位符
```

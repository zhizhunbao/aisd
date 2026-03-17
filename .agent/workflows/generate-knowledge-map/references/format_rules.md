# 知识地图通用格式规则

> 本文件从 `knowledge-map-format` skill 迁移而来，是所有维度文件的格式规范。
> 每个 step 文件遵循此规则 + 自身的完整模板（教科书依据 + 格式 + 检查清单）。

---

## 来源限制

知识地图的所有内容必须来自可信赖、可验证的来源。

### 允许的来源（白名单）及引用优先级

> ⚠️ **引用必须按优先级从高到低选择最权威的来源。**

| 优先级 | 来源类型 | 具体来源 | 说明 |
|-------|---------|---------|------|
| 🥇 **P1 最高** | 📖 学术原始论文 | arXiv, ACM, IEEE, NeurIPS, ICML, JMLR 等 | 第一手知识来源，最权威 |
| 🥈 **P2** | 📚 出版教科书 | 教材 PDF（引用具体章节+方程编号）| 系统整理，有同行评审 |
| 🥉 **P3** | 📖 官方文档 | scikit-learn docs, PyTorch docs, RFC, W3C… | 实现权威，但非算法权威 |
| 🔵 **P4 最低** | 💻 开源代码仓库 | GitHub: sklearn, numpy, huggingface… | 验证实现细节，补充文档 |

**规则**：每个知识声明优先引用 P1 论文；论文未涵盖时引用 P2 教科书；P1+P2 均无时才用 P3/P4。

### 严禁的来源（黑名单）

| 严禁 | 原因 |
|------|------|
| 教师 PPT / 课件 / 讲义 | 非权威，有简化或错误，无法被他人验证 |
| 课程作业题 / 考试题 | 同上 |
| 百度百科 / CSDN / 知乎博客 | 非同行评审，质量无保障 |
| 自己写的生成内容 | 循环引证，无意义 |

---

## R1. Frontmatter 格式

> ⚠️ **YAML 不渲染 Markdown 链接**：`source_versions` 必须使用**裸 URL**。

```yaml
---
topic: { topic_name }
dimension: { dimension } # map | concepts | math | tutorial | code | pitfalls | history | bridge | first_principles
created: { YYYY-MM-DD }
last_verified: { YYYY-MM-DD }
source_versions:
  # 教科书：用 file:/// 绝对路径
  - "📚 Book: 作者, 《书名》 Ch.X — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/文件名.pdf"
  # 公开论文：用完整 https:// URL
  - "📖 Paper: 作者 会议/期刊 年份 — https://链接"
  # 官方文档
  - "📖 Docs: 名称 章节 — https://链接"
  # 开源仓库
  - "💻 Source: 仓库名 文件:行号 — https://github.com/org/repo/blob/main/path/to/file.py"
  # 实践经验（仅 Pitfalls 维度）
  - "🧪 经验: 简短说明"
expiry: 3m # 3m | 6m | 12m | never
status: current # current | needs_review | outdated
---
```

## R2. 来源引证

每个 `##` 章节结尾必须有 `>` 引用块：

```
> 📚 Book: 作者, [《书名》](../../textbooks/文件名.pdf), Ch.X
> 📖 Docs: [名称](../../.documents/分类/文件) — 章节
> 📖 Paper: [简称](URL)
> 💻 Source: [仓库名](../../.github/仓库名/) `文件:行号`
> 🧪 经验: 简短说明
```

## R3. 代码块禁止嵌套

❌ **绝对禁止** ` ```markdown ` 中嵌套 ` ```bash ` — 会导致渲染崩坏。

替代方案：用 **4 空格缩进** 表示内层代码。

## R4. ❌/✅ 对比格式（Pitfalls 维度专用）

在生成的 `.md` 文件中，❌/✅ 后面用语言标注的代码块（有语法高亮）：

````markdown
❌ 错误写法 — 原因说明

```python
# 错误的代码
bad_code()
```

✅ 正确写法 — 原因说明

```python
# 正确的代码
good_code()
```
````

> ❌ **禁止**在实际 pitfalls 文件里用 4 空格缩进代替代码块——缺少语法高亮

## R5. 易混淆标注（Concepts 维度专用）

每个 `###` 术语条目，若存在常见混淆点：

```
> 易混淆：**概念A vs 概念B** — 一句话说清楚区别
```

仅在真正存在混淆风险时写，不强制每个术语都有。

## R6. 分隔线

- `##` 章节之间用 `---` 分隔
- `###` 小节之间**不用** `---`

## R7. 标题后引证

每个文件 `# 标题` 下紧跟一行全局引证：

```
# {Topic} {维度名}

> 📚 Book: 作者, [《书名》](../../textbooks/文件.pdf), Ch.X
```

## R8. 素材目录规范

| 来源类型 | 目录 | 说明 |
|---------|------|------|
| 📚 教科书 PDF | `textbooks/` | 原始 PDF |
| 📚 MinerU 解析 | `data/mineru_output/{book}/` | 教科书的 MinerU 输出 |
| 💻 开源项目 | `.github/` | 参考代码仓库 |
| 📖 官方文档 | `.documents/` | 下载到本地的官方文档 |
| 📖 论文 PDF | `.documents/papers/{topic}/` | 用 `download_papers.py` 下载 |

---

## 论文下载工具

> 下载失败时不阻塞生成流程。

### 🥇 首选：arXiv 直接下载

```bash
python .agent/workflows/generate-knowledge-map/scripts/download_papers.py \
    --url "https://arxiv.org/abs/1410.5329" --topic naive_bayes \
    --filename raschka_2014_naive_bayes.pdf
```

### 🥈 次选：Semantic Scholar 关键词搜索

```bash
python .agent/workflows/generate-knowledge-map/scripts/download_papers.py \
    --search "DBSCAN density based clustering" --topic dbscan \
    --api-key YOUR_KEY
```

### 下载失败处理

1. **继续生成**：不等待，立即继续
2. **标注占位符**：
   ```yaml
   - "📖 Paper: 作者, '标题', 刊物 年份 — ⚠️ 待下载 见 papers_index.md"
   ```
3. **写入 `papers_index.md`**：在主题目录下创建/追加
4. **用户手动下载后更新**

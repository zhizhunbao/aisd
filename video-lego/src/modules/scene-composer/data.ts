// ═══════════════════════════════════════════════════════════
// M9 场景编排器 — 场景数据（KNN）
// Scene Composer — KNN scene data
//
// 这是从 video-content/knn/video.data.ts 中
// 提取场景部分到管理系统的存储版本。
// 数据结构使用 @/lib/types.ts 中的 SceneData。
// ═══════════════════════════════════════════════════════════

import type { SceneData } from '@/lib/types'
import type { VideoSceneProject, SceneRegistry } from './types'

// ─────────── KNN 幕定义 ───────────

const KNN_ACTS = {
  a1: '第一幕 · 起源',
  a2: '第二幕 · 人话翻译',
  a3: '第三幕 · 三公理',
  a4: '第四幕 · 避坑指南',
  a5: '第五幕 · 现代演进',
}

// ─────────── KNN 场景数据 ───────────

const KNN_SCENE_LIST: SceneData[] = [
  // ══════ Scene 01: 1951 开场 ══════
  {
    layout: 'landscape', act: KNN_ACTS.a1,
    title: '1951 · 分类问题的诞生',
    visuals: [
      { block: 'ImageDisplay', data: { src: 'photos/knn/repr_person_fix.jpg', caption: 'Evelyn Fix (1904–1965)' } },
      { block: 'StatCards', data: { cards: [
        { label: '提出者', value: 'Fix & Hodges', icon: '👤', color: '#4ea8de' },
        { label: '机构', value: 'UC Berkeley', icon: '🎓', color: '#2ecc71' },
      ] } },
    ],
    points: [
      { icon: '✈️', text: '美国空军 · 统计分类问题', bold: true },
      { icon: '❓', text: '飞行员体检数据 → 适不适合飞行？' },
      { icon: '💡', text: '找最像的人 → 直接抄他的答案', variant: 'highlight', color: '#ffd700' },
    ],
    conclusion: { text: '思路极其简单 — 找最近 → 抄标签', icon: '⭐' },
  },

  // ══════ Scene 02: 最近邻搜索 ══════
  {
    layout: 'landscape', act: KNN_ACTS.a1,
    title: '最近邻搜索',
    visuals: [
      { block: 'StatCards', data: { cards: [
        { label: '步骤 1', value: '找距离', icon: '📏', color: '#4ea8de', description: '计算到所有点的距离' },
        { label: '步骤 2', value: '选最近', icon: '🎯', color: '#ffd700', description: '找到最近的那个' },
        { label: '步骤 3', value: '抄标签', icon: '📋', color: '#2ecc71', description: '复制他的类别' },
        { label: '结果', value: '1-NN', icon: '✅', color: '#e74c3c', description: '最近邻分类器' },
      ] } },
    ],
    points: [
      { icon: '⭐', text: '你是一个新数据点，不知道自己属于哪一类' },
      { icon: '🔍', text: '计算你和所有已知数据点的距离' },
      { icon: '📋', text: '找到离你最近的那个 → 抄他的标签', variant: 'highlight' },
    ],
    conclusion: { text: '这就是 1-NN（最近邻分类器）' },
  },

  // ══════ Scene 03: 勾股定理 → 欧氏距离 ══════
  {
    layout: 'landscape', act: KNN_ACTS.a1,
    title: '勾股定理 → 欧氏距离',
    visuals: [
      { block: 'FormulaDerivation', data: {
        source: 'PRML Ch.2.5.2',
        steps: [
          { latex: 'a^2 + b^2 = c^2', annotation: '勾股定理 — 初中知识' },
          { latex: 'c = \\sqrt{a^2 + b^2}', annotation: '解出距离' },
          { latex: 'd = \\sqrt{(x_1-y_1)^2 + (x_2-y_2)^2}', annotation: '两个维度' },
          { latex: 'd = \\sqrt{\\sum_{i=1}^{n}(x_i - y_i)^2}', annotation: '推广到 n 维 — 欧氏距离', highlight: true },
        ],
      } },
    ],
    points: [
      { icon: '📐', text: '从直角三角形出发' },
      { icon: '🚀', text: '推广到 n 维空间', bold: true },
      { icon: '📏', text: '距离小 = 像，距离大 = 不像', variant: 'highlight' },
    ],
  },

  // ══════ Scene 04: 石沉大海 ══════
  {
    layout: 'landscape', act: KNN_ACTS.a1,
    title: '石沉大海',
    visuals: [
      { block: 'ImageDisplay', data: { src: 'photos/knn/repr_paper_fix_hodges_1951.png', caption: 'Fix & Hodges (1951) 原始报告' } },
      { block: 'Timeline', data: { events: [
        { year: '1951', text: '报告写完', color: '#4ea8de', icon: '📄' },
        { year: '1951–1967', text: '无人引用，石沉大海', color: '#888888', icon: '😶' },
        { year: '1967', text: '被斯坦福学者发现……', color: '#ffd700', icon: '💡' },
      ] } },
    ],
    points: [
      { icon: '📄', text: 'USAF School of Aviation Medicine 技术报告' },
      { icon: '😶', text: '没人在意……埋了 16 年' },
      { icon: '❓', text: '直到两位斯坦福学者发现了它……', bold: true, variant: 'highlight' },
    ],
  },

  // ══════ Scene 05: Cover-Hart 定理 ══════
  {
    layout: 'landscape', act: KNN_ACTS.a1,
    title: 'Cover-Hart 定理 (1967)',
    visuals: [
      { block: 'ImageDisplay', data: { src: 'photos/knn/repr_person_cover.jpg', caption: 'Thomas Cover (Stanford)' } },
      { block: 'FormulaBlock', data: { latex: 'P^{*} \\leq P_{\\text{1-NN}} \\leq 2P^{*}', label: '最近邻误差 ≤ 最优误差的 2 倍', color: '#ffd700' } },
    ],
    points: [
      { icon: '🎓', text: 'Thomas Cover + Peter Hart (SRI)', bold: true },
      { icon: '📜', text: '证明了「蠢方法」在数学上是靠谱的' },
      { icon: '🔥', text: '被引用 18,000+ 次', variant: 'highlight', color: '#e74c3c' },
    ],
    conclusion: { text: '最近邻方法从此走上正轨', icon: '🏆' },
  },

  // ══════ Scene 06: KNN = 抄邻居作业 ══════
  {
    layout: 'landscape', act: KNN_ACTS.a1,
    title: 'KNN = 抄邻居作业',
    visuals: [
      { block: 'ComparisonSplit', data: {
        left: { label: '1-NN', value: '问 1 个人', icon: '👤', color: '#e74c3c', subItems: ['只问旁边一个人', '那人是学渣你就完了'] },
        right: { label: 'K-NN', value: '问 K 个人', icon: '🗳️', color: '#2ecc71', subItems: ['问 K 个邻座', '投票取多数'] },
      } },
    ],
    points: [
      { icon: '🏫', text: '考场上不会做 → 偷看旁边', bold: true },
      { icon: '👀', text: '1-NN：只问一个人 → 风险大' },
      { icon: '🗳️', text: 'K-NN：问 K 个 → 投票', variant: 'highlight' },
    ],
    conclusion: { text: 'K = 问几个人，投票 = 少数服从多数' },
  },

  // ══════ Scene 07: K 值的两个极端 ══════
  {
    layout: 'landscape', act: KNN_ACTS.a2,
    title: 'K 值的两个极端',
    visuals: [
      { block: 'ComparisonSplit', data: {
        left: { label: '过拟合', value: 'K = 1', icon: '⚡', color: '#e74c3c', subItems: ['只问旁边一个人', '学渣你就完了', '决策边界锯齿状'] },
        right: { label: '欠拟合', value: 'K = 100', icon: '🌊', color: '#4ea8de', subItems: ['问全班', '等于看多数票', '边界过于平滑'] },
      } },
    ],
    points: [
      { icon: '⚡', text: 'K 太小 → 噪声敏感（过拟合）', color: '#e74c3c' },
      { icon: '🌊', text: 'K 太大 → 细节丢失（欠拟合）', color: '#4ea8de' },
      { icon: '🎯', text: '存在最优 K，让总误差最小', variant: 'highlight' },
    ],
    conclusion: { text: 'K 太小噪声敏感，K 太大细节丢失', icon: '⚖️' },
  },

  // ══════ Scene 08: 偏差-方差权衡 ══════
  {
    layout: 'landscape', act: KNN_ACTS.a2,
    title: '偏差-方差权衡',
    visuals: [
      { block: 'UCurve', data: {
        source: 'ISL Fig 2.9',
        points: Array.from({ length: 30 }, (_, i) => ({
          x: i + 1,
          y: 0.35 + 0.25 * Math.pow((i + 1 - 8) / 12, 2) + 0.05 * Math.sin((i + 1) * 0.5),
        })),
        xLabel: 'K 值', yLabel: '错误率',
        zones: [
          { start: 1, end: 6, color: '#e74c3c', label: '过拟合' },
          { start: 18, end: 30, color: '#4ea8de', label: '欠拟合' },
        ],
        bestPoint: { x: 8, annotation: '最优 K = 8' },
      } },
    ],
    points: [
      { icon: '📉', text: 'K 小 → 方差大（过拟合）' },
      { icon: '📈', text: 'K 大 → 偏差大（欠拟合）' },
      { icon: '⭐', text: '最优 K 让总误差最小', bold: true },
      { icon: '🎯', text: '交叉验证 — 让数据自己说话', variant: 'highlight' },
    ],
    conclusion: { text: '偏差↑方差↓ — 永恒的 tradeoff', icon: '⚖️' },
  },

  // ══════ Scene 09: 惰性学习 ══════
  {
    layout: 'landscape', act: KNN_ACTS.a2,
    title: '惰性学习 Lazy Learning',
    visuals: [
      { block: 'ComparisonSplit', data: {
        left: { label: '训练', value: '⚡ 0.1s', icon: '🎓', color: '#2ecc71', subItems: ['数据存入内存', '训练 = 不训练', '秒完'] },
        right: { label: '预测', value: '🐢 600s', icon: '🔍', color: '#e74c3c', subItems: ['遍历全部数据', '每个新点都要比', '龟速'] },
      } },
    ],
    points: [
      { icon: '⚡', text: '训练零点一秒 — 啥也没干', color: '#2ecc71' },
      { icon: '🐢', text: '预测可能要十分钟 — 逐个翻', color: '#e74c3c' },
      { icon: '⏳', text: '所以叫「惰性学习」', variant: 'highlight' },
    ],
    conclusion: { text: '伏笔：后面会讲怎么加速', icon: '⏳' },
  },

  // ══════ Scene 10: 公理 1 ══════
  {
    layout: 'landscape', act: KNN_ACTS.a3,
    title: '公理 1：局部连续性',
    visuals: [
      { block: 'StatCards', data: { cards: [
        { label: '核心假设', value: '像 → 同标签', icon: '🟢', color: '#2ecc71' },
        { label: '类比', value: '豪宅区邻居', icon: '🏠', color: '#4ea8de', description: '住豪宅的邻居大概率有钱' },
      ] } },
    ],
    points: [
      { icon: '🟢', text: '离得近的点 → 大概率同一类', bold: true, variant: 'highlight' },
      { icon: '🏠', text: '类比：住在豪宅区的邻居都有钱' },
      { icon: '⚠️', text: '失效场景：类别交错、噪声大', variant: 'warning' },
    ],
    conclusion: { text: '公理 1：像 → 同标签' },
  },

  // ══════ Scene 11: 公理 2 ══════
  {
    layout: 'landscape', act: KNN_ACTS.a3,
    title: '公理 2：距离必须管用',
    visuals: [
      { block: 'ComparisonSplit', data: {
        left: { label: '歪的尺', value: '❌ 错误距离', icon: '📏', color: '#e74c3c', subItems: ['错误距离 → 错误邻居', '垃圾进 → 垃圾出'] },
        right: { label: '准的尺', value: '✅ 正确距离', icon: '📐', color: '#2ecc71', subItems: ['正确距离 → 正确邻居', '公理 2 成立'] },
      } },
    ],
    points: [
      { icon: '📏', text: '尺子歪了 → 量出的最近邻是错的', color: '#e74c3c' },
      { icon: '📐', text: '尺子准了 → 公理成立', color: '#2ecc71' },
      { icon: '🔑', text: '距离度量 = KNN 的生命线', variant: 'highlight', bold: true },
    ],
    conclusion: { text: '正确的距离度量 = KNN 的生命线', icon: '🔑' },
  },

  // ══════ Scene 12: 公理 3 ══════
  {
    layout: 'landscape', act: KNN_ACTS.a3,
    title: '公理 3：数据要够多',
    visuals: [
      { block: 'ProgressBars', data: { bars: [
        { label: '5 个点', value: 10, color: '#e74c3c', displayValue: '❌ 不靠谱' },
        { label: '50 个点', value: 50, color: '#ffd700', displayValue: '⚠️ 稍好' },
        { label: '500 个点', value: 95, color: '#2ecc71', displayValue: '✅ 稳定' },
      ] } },
    ],
    points: [
      { icon: '5️⃣', text: '5 个点 → 方差巨大，不靠谱' },
      { icon: '🔢', text: '50 个点 → 边界模糊' },
      { icon: '✅', text: '500 个点 → 统计稳定', bold: true, variant: 'highlight' },
    ],
    conclusion: { text: 'n→∞ 时 KNN 误差趋近最优', icon: '📊' },
  },

  // ══════ Scene 13: 三公理总结 ══════
  {
    layout: 'landscape', act: KNN_ACTS.a3,
    title: '三公理 → 定理保底',
    visuals: [
      { block: 'StatCards', data: { cards: [
        { label: '公理 1', value: '局部连续', icon: '1️⃣', color: '#2ecc71' },
        { label: '公理 2', value: '距离管用', icon: '2️⃣', color: '#4ea8de' },
        { label: '公理 3', value: '数据够多', icon: '3️⃣', color: '#ffd700' },
        { label: '结论', value: '定理保底', icon: '🛡️', color: '#e74c3c' },
      ] } },
      { block: 'FormulaBlock', data: { latex: 'P^{*} \\leq P_{\\text{NN}} \\leq 2P^{*}', label: '三条全满足 → Cover-Hart 保底' } },
    ],
    points: [
      { icon: '1️⃣', text: '局部连续：像 → 同标签', bold: true },
      { icon: '2️⃣', text: '距离管用：尺子不能歪', bold: true },
      { icon: '3️⃣', text: '数据够多：越多越稳', bold: true },
      { text: 'Cover-Hart 定理保底', variant: 'formula', latex: 'P^{*} \\leq P_{\\text{NN}} \\leq 2P^{*}' },
    ],
    conclusion: { text: '任何一条不满足 → 全崩', icon: '🚨' },
  },

  // ══════ Scene 14: 坑 1 ══════
  {
    layout: 'landscape', act: KNN_ACTS.a4,
    title: '坑 1：忘记归一化',
    visuals: [
      { block: 'ComparisonSplit', data: {
        left: { label: '不归一化', value: '❌ 距离失真', icon: '❌', color: '#e74c3c', subItems: ['收入 (0~100000)', 'vs 评分 (0~5)', '距离被收入主导'] },
        right: { label: '归一化后', value: '✅ 距离合理', icon: '✅', color: '#2ecc71', subItems: ['所有特征 [0,1]', '等权参与', '距离有意义'] },
      } },
      { block: 'CodeBlock', data: {
        code: 'Pipeline([\n  ("scaler", StandardScaler()),\n  ("knn", KNeighborsClassifier(5))\n])',
        label: '✅ sklearn 正确做法', color: '#2ecc71',
      } },
    ],
    points: [
      { icon: '💰', text: '收入 0~100000 vs 评分 0~5', variant: 'warning' },
      { icon: '❌', text: '距离被高量纲特征完全主导', color: '#e74c3c' },
      { icon: '✅', text: '归一化后每个特征等权参与', color: '#2ecc71', variant: 'highlight' },
    ],
  },

  // ══════ Scene 15: 维度灾难 ══════
  {
    layout: 'landscape', act: KNN_ACTS.a4,
    title: '坑 2：维度灾难', titleColor: '#e74c3c',
    visuals: [
      { block: 'ProgressBars', data: { bars: [
        { label: '2D 距离范围', value: 90, color: '#2ecc71', displayValue: '0.5 ~ 8.2 ✅' },
        { label: '10D 距离范围', value: 50, color: '#ffd700', displayValue: '3.1 ~ 5.4 ⚠️' },
        { label: '100D 距离范围', value: 10, color: '#e74c3c', displayValue: '4.8 ~ 5.1 ❌' },
      ] } },
    ],
    points: [
      { icon: '2️⃣', text: '2D：距离清晰可区分 ✅' },
      { icon: '🔟', text: '10D：差异缩小 ⚠️' },
      { icon: '💯', text: '100D：几乎无差异 ❌', bold: true, variant: 'warning' },
    ],
    conclusion: { text: '所有距离 ≈ 相等 → "最近邻"没意义', icon: '⚠️' },
  },

  // ══════ Scene 16: 维度灾难解法 ══════
  {
    layout: 'landscape', act: KNN_ACTS.a4,
    title: '维度灾难的解法',
    visuals: [
      { block: 'ComparisonSplit', data: {
        left: { label: '方案 A', value: 'PCA 降维', icon: '🅰️', color: '#4ea8de', subItems: ['高维 → 低维投影', '压到 100 维以下'] },
        right: { label: '方案 B', value: '余弦距离', icon: '🅱️', color: '#2ecc71', subItems: ['比方向不比位置', '高维仍然有效'] },
      } },
      { block: 'FormulaBlock', data: {
        latex: '\\cos(\\theta) = \\frac{\\vec{a} \\cdot \\vec{b}}{\\|\\vec{a}\\| \\|\\vec{b}\\|}',
        label: '余弦相似度', color: '#2ecc71',
      } },
    ],
    points: [
      { icon: '🅰️', text: 'PCA 降维到低维空间', bold: true },
      { icon: '🅱️', text: '余弦距离 — 量方向不量位置', bold: true },
      { icon: '📐', text: '维度 > 50 → 必须处理', variant: 'warning' },
    ],
    conclusion: { text: '维度 > 50 → 必须降维或换距离', icon: '🔧' },
  },

  // ══════ Scene 17: KD-Tree ══════
  {
    layout: 'landscape', act: KNN_ACTS.a5,
    title: 'KD-Tree 加速 (1975)',
    visuals: [
      { block: 'ImageDisplay', data: { src: 'photos/knn/repr_person_bentley.jpg', caption: 'Jon Bentley' } },
      { block: 'ComparisonSplit', data: {
        left: { label: '暴力搜索', value: 'O(n)', icon: '🐌', color: '#e74c3c', subItems: ['逐个比较', 'n=100万 → 慢'] },
        right: { label: 'KD-Tree', value: 'O(log n)', icon: '🌲', color: '#2ecc71', subItems: ['空间二叉切割', 'n=100万 → 快'] },
      } },
    ],
    points: [
      { icon: '👤', text: 'Jon Bentley — 二分查找 × 多维' },
      { icon: '🐌', text: '暴力 O(n)', color: '#e74c3c' },
      { icon: '🌲', text: 'KD-Tree O(log n)', color: '#2ecc71', variant: 'highlight' },
      { icon: '⚠️', text: '维度 > 20 → KD-Tree 也失效', variant: 'warning' },
    ],
  },

  // ══════ Scene 18: ANN 演进 ══════
  {
    layout: 'landscape', act: KNN_ACTS.a5,
    title: '近似最近邻 ANN 演进',
    visuals: [
      { block: 'Timeline', data: { events: [
        { year: '1975', text: 'KD-Tree — 精确搜索', color: '#4ea8de', icon: '🌲' },
        { year: '1999', text: 'LSH — 差不多近就行', color: '#ffd700', icon: '🔀' },
        { year: '2017', text: 'FAISS (Meta) — 十亿级毫秒搜', color: '#2ecc71', icon: '🚀' },
      ] } },
      { block: 'StatCards', data: { cards: [
        { label: '速度提升', value: '1000×', icon: '🚀', color: '#2ecc71' },
        { label: '数据规模', value: '10 亿+', icon: '📊', color: '#ffd700' },
      ] } },
    ],
    points: [
      { icon: '1️⃣', text: '1999 LSH：牺牲精度换速度', bold: true },
      { icon: '2️⃣', text: '2017 FAISS：GPU 加速', bold: true },
      { icon: '🚀', text: '精确 → 近似，速度 ×1000', variant: 'highlight' },
    ],
    conclusion: { text: '从精确搜索 → 近似搜索', icon: '⚡' },
  },

  // ══════ Scene 19: ChatGPT = KNN ══════
  {
    layout: 'landscape', act: KNN_ACTS.a5,
    title: 'ChatGPT 的核心 = KNN 搜索',
    visuals: [
      { block: 'Timeline', data: { events: [
        { year: '步骤 1', text: '用户提问 → 文本 embedding', color: '#4ea8de', icon: '💬' },
        { year: '步骤 2', text: 'FAISS 最近邻 → 找相关文档', color: '#ffd700', icon: '🔍' },
        { year: '步骤 3', text: 'LLM 基于检索结果生成', color: '#2ecc71', icon: '🤖' },
      ] } },
    ],
    points: [
      { icon: '💬', text: '用户提问 → 向量化' },
      { icon: '🔍', text: 'FAISS 搜索 → 找最相关文档' },
      { icon: '🤖', text: 'LLM 生成答案 (RAG 架构)', variant: 'highlight' },
    ],
    conclusion: { text: '1951 蠢方法 → 2024 AI 基础设施', icon: '🏗️' },
  },

  // ══════ Scene 20: 下期预告 ══════
  {
    layout: 'landscape', act: KNN_ACTS.a5,
    title: '下期预告', titleColor: '#ffd700',
    visuals: [
      { block: 'StatCards', data: { cards: [
        { label: '下期主题', value: 'LOF', icon: '🔮', color: '#ffd700', description: '异常检测算法' },
        { label: '应用', value: '抓诈骗犯', icon: '🕵️', color: '#e74c3c', description: '基于 KNN 的异常检测' },
      ] } },
    ],
    points: [
      { icon: '🔮', text: 'LOF 异常检测 — 用 KNN 抓诈骗犯', bold: true, variant: 'highlight' },
      { icon: '📺', text: '关注不迷路 · 下期见！' },
    ],
    conclusion: { text: '关注不迷路 · 下期见！', icon: '👋' },
  },
]

// ─────────── KNN 项目导出 ───────────

export const KNN_SCENES: VideoSceneProject = {
  course: 'machine-learning',
  topic: 'knn',
  acts: KNN_ACTS,
  scenes: KNN_SCENE_LIST,
}

// ─────────── 场景注册表 ───────────

export const SCENE_REGISTRY: SceneRegistry = [
  KNN_SCENES,
]

/** 按 course + topic 查找场景项目 */
export function findSceneProject(course: string, topic: string): VideoSceneProject | null {
  return SCENE_REGISTRY.find(p => p.course === course && p.topic === topic) || null
}

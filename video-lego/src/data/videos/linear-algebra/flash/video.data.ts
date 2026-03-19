// ═══════════════════════════════════════════════════════════
// MIT 线性代数 60 秒黑板快闪 — 视频数据文件
// MIT Linear Algebra 60s Blackboard Flash — Video Data
//
// 标题风格：《一分钟学会｜MIT 线性代数 24 个核心概念》
//
// 知识来源：MIT 18.06 Linear Algebra (Gilbert Strang)
// 教科书：Introduction to Linear Algebra, 5th Ed.
//
// 节奏：2.5 秒/概念 × 24 = 60 秒
// 排序：基础 → 运算 → 空间 → 变换 → 分解 → 应用
// ═══════════════════════════════════════════════════════════

import type { VideoData, SceneData, KnowledgeUnitData } from '@lego/types';

const COURSE = 'MIT 线性代数';

// ══════ 24 个核心概念（覆盖 MIT 18.06 全课程）══════

const UNITS: { data: KnowledgeUnitData }[] = [
  // ── §1 基础对象 ──
  {
    data: {
      zhName: '向量',
      enName: 'Vector',
      formula: '\\vec{v} = \\begin{bmatrix} v_1 \\\\ v_2 \\\\ \\vdots \\\\ v_n \\end{bmatrix}',
      explanation: '有大小和方向的量，线性代数的基本元素',
    },
  },
  {
    data: {
      zhName: '矩阵',
      enName: 'Matrix',
      formula: 'A_{m \\times n}',
      diagram: 'MatrixDiagram',
      explanation: '按行列排列的矩形数组，线性代数的基本语言',
    },
  },
  {
    data: {
      zhName: '矩阵乘法',
      enName: 'Matrix Multiplication',
      formula: 'C_{ij} = \\sum_k A_{ik} B_{kj}',
      explanation: '行 × 列点积求和，线性变换的组合',
    },
  },
  {
    data: {
      zhName: '转置',
      enName: 'Transpose',
      formula: '(A^T)_{ij} = A_{ji}',
      explanation: '行变列，列变行——矩阵的镜像翻转',
    },
  },
  // ── §2 线性方程组 ──
  {
    data: {
      zhName: '高斯消元',
      enName: 'Gaussian Elimination',
      aliases: ['行化简', 'Row Reduction'],
      formula: 'A \\to U \\text{ (上三角)}',
      explanation: '消元法解方程组，把矩阵化成阶梯形',
    },
  },
  {
    data: {
      zhName: 'LU 分解',
      enName: 'LU Decomposition',
      formula: 'A = LU',
      formulaLabel: '下三角 × 上三角',
      explanation: '高斯消元的矩阵写法，一次分解多次复用',
    },
  },
  // ── §3 向量空间 ──
  {
    data: {
      zhName: '向量空间',
      enName: 'Vector Space',
      aliases: ['线性空间'],
      formula: '\\alpha \\vec{u} + \\beta \\vec{v} \\in V',
      explanation: '对加法和数乘封闭的集合',
    },
  },
  {
    data: {
      zhName: '线性无关',
      enName: 'Linear Independence',
      formula: '\\sum c_i \\vec{v}_i = \\vec{0} \\Rightarrow c_i = 0',
      explanation: '谁也不能被其他向量的组合表示出来',
    },
  },
  {
    data: {
      zhName: '基',
      enName: 'Basis',
      aliases: ['基底'],
      formula: '\\text{span}(\\vec{v}_1, \\ldots, \\vec{v}_n) = V',
      diagram: 'BasisDiagram',
      explanation: '线性无关 + 张成全空间 = 坐标系',
    },
  },
  {
    data: {
      zhName: '维数',
      enName: 'Dimension',
      aliases: ['dim'],
      formula: '\\dim(V) = |\\text{basis}|',
      explanation: '基向量的个数，就是空间的"自由度"',
    },
  },
  {
    data: {
      zhName: '秩',
      enName: 'Rank',
      formula: '\\text{rank}(A) = \\dim(\\text{Col}(A))',
      explanation: '列空间的维数，衡量矩阵有多少"有效信息"',
      color: '#ffd700',
    },
  },
  // ── §4 四个基本子空间 ──
  {
    data: {
      zhName: '列空间',
      enName: 'Column Space',
      aliases: ['像空间', 'Range'],
      formula: 'C(A) = \\{A\\vec{x} : \\vec{x} \\in \\mathbb{R}^n\\}',
      explanation: 'A 能到达的所有地方，方程 Ax=b 有解的条件',
    },
  },
  {
    data: {
      zhName: '零空间',
      enName: 'Null Space',
      aliases: ['核', 'Kernel'],
      formula: 'N(A) = \\{\\vec{x} : A\\vec{x} = \\vec{0}\\}',
      explanation: '被 A 消灭的所有向量，方程 Ax=0 的解集',
    },
  },
  // ── §5 核心变换 ──
  {
    data: {
      zhName: '线性变换',
      enName: 'Linear Transformation',
      aliases: ['线性映射'],
      formula: 'T(\\vec{x}) = A\\vec{x}',
      diagram: 'LinearTransformDiagram',
      explanation: '一个矩阵就是一次空间变换——旋转、缩放、剪切',
    },
  },
  {
    data: {
      zhName: '行列式',
      enName: 'Determinant',
      formula: '\\det(A) = ad - bc',
      diagram: 'DeterminantDiagram',
      explanation: '空间被拉伸了多少倍？零意味着降维',
      color: '#ffd700',
    },
  },
  {
    data: {
      zhName: '逆矩阵',
      enName: 'Inverse Matrix',
      formula: 'AA^{-1} = I',
      explanation: 'A 把你送过去，A⁻¹ 把你送回来',
    },
  },
  // ── §6 正交 ──
  {
    data: {
      zhName: '正交',
      enName: 'Orthogonal',
      aliases: ['垂直'],
      formula: '\\vec{u} \\cdot \\vec{v} = 0',
      diagram: 'OrthogonalDiagram',
      explanation: '两个向量互相垂直，正交基最好用',
    },
  },
  {
    data: {
      zhName: '投影',
      enName: 'Projection',
      formula: 'P = A(A^T A)^{-1} A^T',
      formulaLabel: '投影矩阵',
      explanation: '把向量"压"到子空间上——最小二乘的几何本质',
    },
  },
  {
    data: {
      zhName: 'Gram-Schmidt',
      enName: 'Gram-Schmidt Process',
      aliases: ['正交化'],
      formula: 'A = QR',
      formulaLabel: '正交 × 上三角',
      explanation: '把任意基变成正交基的标准方法',
    },
  },
  // ── §7 特征分析 ──
  {
    data: {
      zhName: '特征值',
      enName: 'Eigenvalue',
      aliases: ['固有值'],
      formula: 'A\\vec{x} = \\lambda \\vec{x}',
      diagram: 'EigenvalueDiagram',
      explanation: '矩阵作用后方向不变，被拉伸 λ 倍',
      color: '#ffd700',
    },
  },
  {
    data: {
      zhName: '对角化',
      enName: 'Diagonalization',
      formula: 'A = S \\Lambda S^{-1}',
      explanation: '用特征向量做基，矩阵变对角——计算 Aⁿ 的捷径',
    },
  },
  {
    data: {
      zhName: '正定矩阵',
      enName: 'Positive Definite',
      aliases: ['PD'],
      formula: '\\vec{x}^T A \\vec{x} > 0',
      explanation: '所有特征值 > 0，能量永远为正，优化的好朋友',
      color: '#2ecc71',
    },
  },
  // ── §8 高级分解 ──
  {
    data: {
      zhName: '奇异值分解',
      enName: 'SVD',
      formula: 'A = U \\Sigma V^T',
      explanation: '旋转→缩放→再旋转，数据科学的瑞士军刀',
      color: '#4ea8de',
    },
  },
  // ── §9 应用 ──
  {
    data: {
      zhName: '最小二乘',
      enName: 'Least Squares',
      aliases: ['OLS'],
      formula: '\\hat{x} = (A^T A)^{-1} A^T b',
      explanation: '数据不完美？投影到列空间，找最近的解',
      color: '#2ecc71',
    },
  },
];

// ══════ 自动生成场景（含累积 pinnedItems）══════

const TOTAL = UNITS.length; // 24
const SEC_PER_UNIT = 60 / TOTAL; // 2.5 秒/单元

const scenes: SceneData[] = UNITS.map((unit, i) => ({
  layout: 'blackboard' as const,
  act: COURSE,
  title: unit.data.zhName,
  progress: { current: i + 1, total: TOTAL },
  pinnedItems: UNITS.slice(0, i).map((prev) => ({
    zhName: prev.data.zhName,
    enName: prev.data.enName,
    color: prev.data.color,
  })),
  visuals: [
    {
      block: 'KnowledgeUnit' as const,
      data: unit.data,
    },
  ],
  points: [],
}));

// ══════ 自动生成字幕 ══════

const subtitles = UNITS.map((unit, i) => ({
  start: i * SEC_PER_UNIT,
  end: (i + 1) * SEC_PER_UNIT,
  text: `${unit.data.zhName}——${unit.data.explanation}`,
}));

// ══════ 导出视频数据 ══════

export const LINEAR_ALGEBRA_FLASH: VideoData = {
  meta: {
    topic: 'linear-algebra-flash',
    course: 'linear-algebra',
    title: '一分钟学会｜MIT 线性代数 24 个核心概念',
    textbookSource: 'Strang, Introduction to Linear Algebra, 5th Ed.',
    contentSources: ['MIT 18.06', 'Strang Textbook'],
    totalDurationSec: 60,
  },

  narration: {
    audioFile: 'narration/linear-algebra-flash/full_narration.mp3',
    timestamps: UNITS.map((_, i) => ({
      start: i * SEC_PER_UNIT,
      end: (i + 1) * SEC_PER_UNIT,
    })),
    subtitles,
  },

  scenes,
};

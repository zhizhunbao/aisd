// ═══════════════════════════════════════════════════════════
// 积木元数据 SSOT — 唯一数据源
// Block Catalog — Single Source of Truth for all block metadata
//
// 添加新积木 = 在对应分类里加一个 BlockMeta 对象
// ═══════════════════════════════════════════════════════════

// ─────────── 类型定义 Types ───────────

export type BlockStatus = 'todo' | 'in_progress' | 'review' | 'rework' | 'ready';
export type ClarkMayerType = 'representational' | 'organizational' | 'transformational' | 'interpretive';

export interface BlockRating {
  mayer: number;        // 0-2 Mayer 多媒体原则
  crap: number;         // 0-2 CRAP 设计原则
  animation: number;    // 0-2 动画节奏
  flexibility: number;  // 0-2 数据灵活性
  codeQuality: number;  // 0-2 代码质量（三层分离）
  total: number;        // 0-10 总分
  notes?: string;       // 评审备注
  lastReviewed?: string;// 最后评审日期
}

export interface BlockMeta {
  name: string;
  status: BlockStatus;
  description: string;
  props: string;
  file: string;
  cmType?: ClarkMayerType;
  rating?: BlockRating;
  /** 支持的动画原子 ID — 来自 animation-atoms.ts */
  animations?: string[];
  /** 视觉子类型（用于筛选） */
  visualType?: string;
  /** 可接受的素材分类 — 来自 asset-types.ts */
  acceptsAssets?: string[];
}

export interface CategoryMeta {
  id: string;
  name: string;
  icon: string;
  color: string;
  description: string;
  dir: string;           // 目录前缀
  blocks: BlockMeta[];
}

// ─────────── 积木分类数据 Block Categories ───────────

export const BLOCK_CATEGORIES: CategoryMeta[] = [
  // ══════════════════════════════════
  // 📐 公式类 Formula — 展示数学公式
  // ══════════════════════════════════
  {
    id: 'formula',
    name: '公式 Formula',
    icon: '📐',
    color: '#e74c3c',
    description: '展示数学公式、定理、推导过程',
    dir: 'formula/',
    blocks: [
      {
        name: 'FormulaBlock',
        status: 'ready',
        description: '单个 LaTeX 公式展示，支持标签和高亮色',
        props: 'latex: string\nlabel?: string\ncolor?: string',
        file: 'formula/FormulaBlock.tsx',
        cmType: 'interpretive',
        animations: ['fade-in', 'spring-scale', 'slide-up', 'pulse-glow'],
        visualType: 'single-formula',
        acceptsAssets: ['formula'],
        rating: {
          mayer: 2, crap: 2, animation: 2, flexibility: 2, codeQuality: 2,
          total: 10,
          notes: 'KaTeX 渲染流畅，spring 动画到位，view/motion 三层分离',
          lastReviewed: '2026-03-17',
        },
      },
      {
        name: 'FormulaDerivation',
        status: 'ready',
        description: '多步公式推导动画，逐步显示推导过程',
        props: 'steps: { latex: string; annotation?: string; highlight?: boolean }[]\nsource?: string',
        file: 'formula/FormulaDerivation.tsx',
        cmType: 'interpretive',
        animations: ['stagger', 'slide-up', 'highlight-step'],
        visualType: 'step-derivation',
        acceptsAssets: ['formula'],
        rating: {
          mayer: 2, crap: 2, animation: 2, flexibility: 2, codeQuality: 2,
          total: 10,
          notes: '逐步展开极具教学价值，view/motion 三层分离',
          lastReviewed: '2026-03-17',
        },
      },
      {
        name: 'FormulaComparison',
        status: 'todo',
        description: '两个公式并排对比，高亮差异部分',
        props: 'left: { latex: string; label: string }\nright: { latex: string; label: string }',
        file: 'formula/FormulaComparison.tsx',
        cmType: 'interpretive',
      },
    ],
  },

  // ══════════════════════════════════
  // ⚖️ 对比类 Compare — 展示 A vs B
  // ══════════════════════════════════
  {
    id: 'compare',
    name: '对比 Compare',
    icon: '⚖️',
    color: '#e67e22',
    description: '展示对比、优劣、进度差异',
    dir: 'structure/',
    blocks: [
      {
        name: 'ComparisonSplit',
        status: 'ready',
        description: 'A vs B 左右对比面板，支持子项列表',
        props: 'left: CompareColumnData\nright: CompareColumnData',
        file: 'structure/ComparisonSplit.tsx',
        cmType: 'organizational',
        animations: ['split-reveal', 'stagger', 'slide-left', 'slide-right'],
        visualType: 'side-by-side',
        acceptsAssets: ['comparison'],
        rating: {
          mayer: 2, crap: 2, animation: 1, flexibility: 2, codeQuality: 2,
          total: 9,
          notes: '对比清晰，支持 subItems，view/motion 分离',
          lastReviewed: '2026-03-17',
        },
      },
      {
        name: 'ProgressBars',
        status: 'ready',
        description: '多条进度条对比，支持数值标签和颜色',
        props: 'bars: { label: string; value: number; color: string; displayValue?: string }[]',
        file: 'data/ProgressBars.tsx',
        cmType: 'organizational',
        animations: ['progress-fill', 'stagger', 'fade-in'],
        visualType: 'bar-progress',
        acceptsAssets: ['data'],
        rating: {
          mayer: 1, crap: 2, animation: 2, flexibility: 2, codeQuality: 2,
          total: 9,
          notes: '动画增长直观，view/motion + getBarProgress 分离',
          lastReviewed: '2026-03-17',
        },
      },
    ],
  },

  // ══════════════════════════════════
  // 📊 图表类 Chart — 数据可视化
  // ══════════════════════════════════
  {
    id: 'chart',
    name: '图表 Chart',
    icon: '📊',
    color: '#2ecc71',
    description: '数据可视化图表',
    dir: 'chart/',
    blocks: [
      {
        name: 'UCurve',
        status: 'ready',
        description: 'U 形曲线（偏差-方差权衡等），支持区域标注和最优点',
        props: 'points: { x: number; y: number }[]\nxLabel: string\nyLabel: string\nzones?: Zone[]\nbestPoint?: BestPoint',
        file: 'chart/UCurve.tsx',
        cmType: 'interpretive',
        animations: ['chart-draw', 'fade-in', 'progress-fill'],
        visualType: 'u-curve',
        acceptsAssets: ['data'],
        rating: {
          mayer: 2, crap: 2, animation: 2, flexibility: 2, codeQuality: 2,
          total: 10,
          notes: '满分！SVG 动画+区域+最优点，数据完全驱动',
          lastReviewed: '2026-03-17',
        },
      },
      {
        name: 'ScatterPlot2D',
        status: 'todo',
        description: '2D 散点图，支持多类别颜色',
        props: 'points: ScatterPoint[]\nxLabel?: string\nyLabel?: string',
        file: 'chart/ScatterPlot2D.tsx',
        cmType: 'transformational',
      },
      {
        name: 'BarChart',
        status: 'todo',
        description: '柱状图，支持动画增长',
        props: 'bars: { label: string; value: number; color: string }[]',
        file: 'chart/BarChart.tsx',
        cmType: 'interpretive',
      },
      {
        name: 'HeatMap',
        status: 'todo',
        description: '热力图矩阵',
        props: 'data: number[][]\nrowLabels?: string[]\ncolLabels?: string[]',
        file: 'chart/HeatMap.tsx',
        cmType: 'interpretive',
      },
    ],
  },

  // ══════════════════════════════════
  // 📍 关系类 Relation — 结构/流程/演进
  // ══════════════════════════════════
  {
    id: 'relation',
    name: '关系 Relation',
    icon: '📍',
    color: '#4ea8de',
    description: '展示时间线、树状结构、流程图、网络关系',
    dir: 'structure/',
    blocks: [
      {
        name: 'Timeline',
        status: 'ready',
        description: '垂直时间线，展示技术演进或历史事件',
        props: 'events: { year: string; text: string; color?: string; icon?: string }[]',
        file: 'structure/Timeline.tsx',
        cmType: 'organizational',
        animations: ['stagger', 'slide-up', 'fade-in'],
        visualType: 'vertical-timeline',
        acceptsAssets: ['timeline'],
        rating: {
          mayer: 2, crap: 2, animation: 2, flexibility: 2, codeQuality: 2,
          total: 10,
          notes: '渐变竖线+逐步出现，view/motion 三层分离',
          lastReviewed: '2026-03-17',
        },
      },
      {
        name: 'TreeDiagram',
        status: 'todo',
        description: '树状层级图（分类体系、决策树）',
        props: 'root: TreeNode\norientation?: "vertical" | "horizontal"',
        file: 'structure/TreeDiagram.tsx',
        cmType: 'organizational',
      },
      {
        name: 'FlowDiagram',
        status: 'todo',
        description: '流程图（算法步骤、Pipeline）',
        props: 'nodes: FlowNode[]\nedges: FlowEdge[]',
        file: 'structure/FlowDiagram.tsx',
        cmType: 'organizational',
      },
      {
        name: 'NetworkDiagram',
        status: 'todo',
        description: '网络关系图（神经网络层、图结构）',
        props: 'layers: NetworkLayer[]',
        file: 'structure/NetworkDiagram.tsx',
        cmType: 'organizational',
      },
    ],
  },

  // ══════════════════════════════════
  // 🖼️ 展示类 Display — 静态内容展示
  // ══════════════════════════════════
  {
    id: 'display',
    name: '展示 Display',
    icon: '🖼️',
    color: '#9b59b6',
    description: '展示卡片、图片、代码块等静态内容',
    dir: 'data/',
    blocks: [
      {
        name: 'StatCards',
        status: 'ready',
        description: '统计卡片网格，弹簧动画入场',
        props: 'cards: StatCardData[]',
        file: 'data/StatCards.tsx',
        cmType: 'organizational',
        animations: ['spring-scale', 'stagger', 'count-up'],
        visualType: 'stat-grid',
        acceptsAssets: ['data'],
        rating: {
          mayer: 1, crap: 2, animation: 2, flexibility: 2, codeQuality: 2,
          total: 9,
          notes: 'spring 缩放入场效果好，view/motion 三层分离',
          lastReviewed: '2026-03-17',
        },
      },
      {
        name: 'CodeBlock',
        status: 'ready',
        description: '代码块展示，支持行高亮',
        props: 'code: string\nlanguage?: string\nlabel?: string\ncolor?: string',
        file: 'data/CodeBlock.tsx',
        cmType: 'interpretive',
        animations: ['fade-in', 'spring-scale', 'slide-up'],
        visualType: 'code-snippet',
        acceptsAssets: ['code'],
        rating: {
          mayer: 1, crap: 2, animation: 1, flexibility: 2, codeQuality: 2,
          total: 8,
          notes: '暗色代码风格专业，view/motion 分离',
          lastReviewed: '2026-03-17',
        },
      },
      {
        name: 'ImageDisplay',
        status: 'ready',
        description: '图片展示，支持标题和说明文字',
        props: 'src: string\ncaption?: string\nmaxHeight?: number',
        file: 'data/ImageDisplay.tsx',
        cmType: 'representational',
        animations: ['fade-in', 'spring-scale'],
        visualType: 'single-image',
        acceptsAssets: ['image'],
        rating: {
          mayer: 2, crap: 1, animation: 1, flexibility: 2, codeQuality: 2,
          total: 8,
          notes: '基础展示完善，view/motion 分离',
          lastReviewed: '2026-03-17',
        },
      },
    ],
  },

  // ══════════════════════════════════
  // 🎬 过程类 Process — 动态过程演示
  // ══════════════════════════════════
  {
    id: 'process',
    name: '过程 Process',
    icon: '🎬',
    color: '#ffd700',
    description: '展示算法运行过程、数据变换动画',
    dir: 'process/',
    blocks: [
      {
        name: 'MatrixAnimation',
        status: 'todo',
        description: '矩阵运算动画（转置、乘法、SVD）',
        props: 'matrix: number[][]\noperation: "transpose" | "multiply" | "svd"',
        file: 'process/MatrixAnimation.tsx',
        cmType: 'transformational',
      },
      {
        name: 'GradientDescent',
        status: 'todo',
        description: '梯度下降动画（损失曲面 + 步进）',
        props: 'steps: { x: number; y: number; loss: number }[]',
        file: 'process/GradientDescent.tsx',
        cmType: 'transformational',
      },
      {
        name: 'ConvolutionAnimation',
        status: 'todo',
        description: '卷积核滑动动画',
        props: 'kernel: number[][]\ninput: number[][]',
        file: 'process/ConvolutionAnimation.tsx',
        cmType: 'transformational',
      },
      {
        name: 'DataTransform',
        status: 'todo',
        description: '数据变换过程（标准化、PCA 降维）',
        props: 'before: DataPoint[]\nafter: DataPoint[]\ntransformName: string',
        file: 'process/DataTransform.tsx',
        cmType: 'transformational',
      },
    ],
  },

  // ══════════════════════════════════
  // 💬 文本类 Text — 要点、结论、标注
  // ══════════════════════════════════
  {
    id: 'text',
    name: '文本 Text',
    icon: 'T',
    color: '#1abc9c',
    description: '要点列表、结论高亮、文字标注',
    dir: 'text/',
    blocks: [
      {
        name: 'KeyPoints',
        status: 'ready',
        description: '要点列表，带图标和颜色标注',
        props: 'points: { icon?: string; text: string; color?: string; bold?: boolean }[]',
        file: 'text/KeyPoints.tsx',
        cmType: 'organizational',
        animations: ['stagger', 'slide-up', 'fade-in'],
        visualType: 'bullet-list',
        rating: {
          mayer: 2, crap: 2, animation: 1, flexibility: 2, codeQuality: 1,
          total: 8,
          notes: '要点列表是高频组件，支持图标和颜色',
          lastReviewed: '2026-03-17',
        },
      },
      {
        name: 'ConclusionBanner',
        status: 'ready',
        description: '结论高亮横幅，金色强调',
        props: 'text: string\\nicon?: string',
        file: 'text/ConclusionBanner.tsx',
        cmType: 'organizational',
        animations: ['fade-in', 'slide-up'],
        visualType: 'conclusion',
        rating: {
          mayer: 1, crap: 2, animation: 1, flexibility: 2, codeQuality: 1,
          total: 7,
          notes: '简单但有效的结论展示',
          lastReviewed: '2026-03-17',
        },
      },
      {
        name: 'TitleCard',
        status: 'todo',
        description: '大标题卡片，用于章节过渡',
        props: 'title: string\\nsubtitle?: string\\ncolor?: string',
        file: 'text/TitleCard.tsx',
        cmType: 'organizational',
      },
    ],
  },
];

// ─────────── 辅助函数 Helpers ───────────

export function getAllBlocks(): BlockMeta[] {
  return BLOCK_CATEGORIES.flatMap((cat) => cat.blocks);
}

export function getBlocksByCategory(catId: string): BlockMeta[] {
  return BLOCK_CATEGORIES.find((c) => c.id === catId)?.blocks || [];
}

export function getBlockMeta(name: string): (BlockMeta & { category: CategoryMeta }) | null {
  for (const cat of BLOCK_CATEGORIES) {
    const block = cat.blocks.find((b) => b.name === name);
    if (block) return { ...block, category: cat };
  }
  return null;
}

export function getCatalogStats() {
  const all = getAllBlocks();
  return {
    total: all.length,
    ready: all.filter((b) => b.status === 'ready').length,
    todo: all.filter((b) => b.status === 'todo').length,
    review: all.filter((b) => b.status === 'review').length,
    rework: all.filter((b) => b.status === 'rework').length,
    inProgress: all.filter((b) => b.status === 'in_progress').length,
    avgScore: (() => {
      const rated = all.filter((b) => b.rating);
      return rated.length > 0
        ? Math.round((rated.reduce((s, b) => s + (b.rating?.total || 0), 0) / rated.length) * 10) / 10
        : 0;
    })(),
  };
}

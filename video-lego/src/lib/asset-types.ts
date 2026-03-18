// ═══════════════════════════════════════════════════════════
// 素材类型定义 — 按视频制作维度分类（基于 Mayer 多媒体学习理论）
// Asset Type Definitions — Categorized by video production dimension
//
// Mayer's Dual-Channel Model:
//   语言通道: narration + text_overlay
//   视觉通道: visual + transition
//   辅助层:   audio + data + reference
//
// 分类原则:
//   素材 = 做视频时你需要准备的最小单元
//   分类 = 在剪辑台上你按什么柜子找素材
//   知识维度(map/concepts/math...) → 用 tags 筛选
//   教科书来源 → 用 sources 字段追溯
// ═══════════════════════════════════════════════════════════

// ─────────── 来源类型 Source Type ───────────

export type SourceType = 'textbook' | 'paper' | 'wikipedia' | 'documentation' | 'course' | 'source_code' | 'original';

export interface AssetSource {
  type: SourceType;
  title: string;
  author?: string;
  year?: number;
  chapter?: string;
  page?: string;
  url?: string;
  cite: string;
}

// ─────────── 视频制作维度分类 Video Production Categories ───────────

export interface SubCategory {
  id: string;
  name: string;
}

export interface CategoryDef {
  id: string;
  name: string;
  icon: string;
  color: string;
  description: string;
  subCategories: SubCategory[];
}

export const ASSET_CATEGORIES: CategoryDef[] = [
  {
    id: 'formula',
    name: '公式', icon: '📐', color: '#ffd700',
    description: '数学公式、方程式、定理',
    subCategories: [
      { id: 'calculus',        name: '微积分' },
      { id: 'linear',          name: '线性代数' },
      { id: 'probability',     name: '概率论' },
      { id: 'statistics',      name: '数理统计' },
      { id: 'optimization',    name: '优化方法' },
      { id: 'information',     name: '信息论' },
      { id: 'deep_learning',   name: '深度学习' },
      { id: 'sequence_model',  name: '序列模型' },
      { id: 'ml_algorithm',    name: 'ML算法' },
      { id: 'regularization',  name: '正则化' },
      { id: 'loss_function',   name: '损失函数' },
      { id: 'evaluation',      name: '评估指标' },
      { id: 'distribution',    name: '概率分布' },
      { id: 'basic_math',      name: '基础数学' },
    ],
  },
  {
    id: 'code',
    name: '代码', icon: '💻', color: '#e67e22',
    description: 'Python、JS 等代码片段',
    subCategories: [
      { id: 'python',  name: 'Python' },
      { id: 'js',      name: 'JavaScript' },
      { id: 'shell',   name: '命令行' },
      { id: 'other',   name: '其他' },
    ],
  },
  {
    id: 'person',
    name: '人物', icon: '👤', color: '#4ea8de',
    description: '人物头像、科学家、讲师形象',
    subCategories: [
      { id: 'portrait',  name: '肖像' },
      { id: 'avatar',    name: '头像' },
      { id: 'character', name: '人物卡' },
    ],
  },
];

export type AssetCategory = string;

// ─────────── 知识维度标签 — 原9维降级为 tags 筛选 ───────────
// 这些不再是分类，而是标签，用于筛选"这个素材讲的是什么知识"

export const KNOWLEDGE_DIMENSIONS = [
  'map', 'concepts', 'math', 'tutorial', 'code',
  'pitfalls', 'history', 'bridge', 'first_principles',
] as const;

export type KnowledgeDimension = typeof KNOWLEDGE_DIMENSIONS[number];

// ─────────── 数据结构 ───────────

/** 文字叠层 — 公式 / 代码片段 */
export interface TextOverlayAssetData {
  /** 叠层类型 */
  overlayType: 'formula' | 'code' | 'title' | 'bullet' | 'caption' | 'quote';
  /** 文字内容（纯文本或 LaTeX） */
  text: string;
  /** 如果是公式，LaTeX 源码 */
  latex?: string;
  /** 如果是代码，语言 */
  language?: string;
  /** 颜色 */
  color?: string;
  /** 直觉解释（用于公式旁边的小字） */
  intuition?: string;
  /** 配图 SVG（内联 SVG 字符串，用于公式旁边的示意图） */
  diagramSvg?: string;
}

/** 人物卡片数据 */
export interface PersonAssetData {
  /** 人物名字 */
  name: string;
  /** 标题/头衔 */
  title?: string;
  /** 简介 */
  bio?: string;
  /** 头像路径 */
  avatarUrl?: string;
  /** 相关贡献 */
  contributions?: string[];
}

// ─────────── 数据联合类型 ───────────

export type AssetData =
  | { category: 'text_overlay';  data: TextOverlayAssetData }
  | { category: 'person';        data: PersonAssetData };

// ─────────── 原子类型 ───────────

export type AtomType =
  | 'formula'            // 单个公式（LaTeX）
  | 'code_snippet'       // 代码片段
  | 'person_card'        // 人物卡片
  ;

// ─────────── 统一素材接口 ───────────

export interface Asset {
  id: string;
  name: string;
  /** 视频制作维度分类 */
  category: AssetCategory;
  subCategory?: string;
  tags: string[];
  /** 知识维度标签（可多选，对应原9维） */
  knowledgeDimensions?: KnowledgeDimension[];
  /** 原子类型 — 描述数据长什么样 */
  atomType: AtomType;
  /** 归属课程 */
  course?: string;
  /** 归属主题 */
  topic?: string;
  /** 所属幕/段落 */
  act?: string;
  /** 结构化来源 */
  sources: AssetSource[];
  createdAt: string;
  updatedAt?: string;
  /** 可绑定积木 */
  compatibleBlocks?: string[];
  /** knowledge-map 原文件路径（可溯源） */
  knowledgeMapFile?: string;
  /** 在原文件中的 section 标题（精确定位） */
  knowledgeMapSection?: string;
  content: AssetData;
}

// ─────────── 辅助 ───────────

export function getCategoryMeta(catId: AssetCategory): CategoryDef | undefined {
  return ASSET_CATEGORIES.find(c => c.id === catId);
}

export function getSubCategoryName(catId: AssetCategory, subId: string): string {
  const cat = getCategoryMeta(catId);
  return cat?.subCategories.find(s => s.id === subId)?.name || subId;
}

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
  // ── 1. 旁白文稿 — 视频的语言层 ──
  {
    id: 'narration',
    name: '旁白文稿', icon: '🎙️', color: '#4ea8de',
    description: '视频的语言层：讲什么话、怎么讲',
    subCategories: [
      { id: 'hook',        name: '开场钩子' },
      { id: 'explain',     name: '讲解旁白' },
      { id: 'transition',  name: '过渡语' },
      { id: 'summary',     name: '总结收尾' },
      { id: 'aside',       name: '旁白补充' },
    ],
  },
  // ── 2. 视觉画面 — 视频的视觉层 ──
  {
    id: 'visual',
    name: '视觉画面', icon: '🎨', color: '#2ecc71',
    description: '视频的视觉层：观众看到什么',
    subCategories: [
      { id: 'animation',   name: '动画' },
      { id: 'diagram',     name: '示意图' },
      { id: 'chart',       name: '图表' },
      { id: 'screencast',  name: '屏幕录制' },
      { id: 'illustration', name: '插画' },
      { id: 'photo',       name: '实拍/照片' },
    ],
  },
  // ── 3. 文字叠层 — 画面上叠加的文字 ──
  {
    id: 'text_overlay',
    name: '文字叠层', icon: '✏️', color: '#ffd700',
    description: '画面上叠加的文字信息：标题、要点、公式',
    subCategories: [
      { id: 'title',       name: '标题' },
      { id: 'bullet',      name: '要点列表' },
      { id: 'formula',     name: '公式' },
      { id: 'code',        name: '代码' },
      { id: 'caption',     name: '字幕/标注' },
      { id: 'quote',       name: '引用/金句' },
    ],
  },
  // ── 4. 音频音效 — 除旁白外的声音 ──
  {
    id: 'audio',
    name: '音频音效', icon: '🔊', color: '#9b59b6',
    description: '听觉体验：BGM、音效、提示音',
    subCategories: [
      { id: 'bgm',         name: '背景音乐' },
      { id: 'sfx',         name: '转场音效' },
      { id: 'alert',       name: '提示音' },
      { id: 'ambient',     name: '环境音' },
    ],
  },
  // ── 5. 数据素材 — 驱动视觉的结构化源数据 ──
  {
    id: 'data',
    name: '数据素材', icon: '📊', color: '#e67e22',
    description: '结构化数据：驱动图表/动画的源数据',
    subCategories: [
      { id: 'dataset',     name: '数值数据' },
      { id: 'timeline',    name: '时间线' },
      { id: 'comparison',  name: '对比表' },
      { id: 'code_sample', name: '代码示例' },
      { id: 'table',       name: '参数/属性表' },
    ],
  },
  // ── 6. 引用来源 — 溯源与信用标注 ──
  {
    id: 'reference',
    name: '引用来源', icon: '📖', color: '#e74c3c',
    description: '溯源信息：教科书、论文、文档出处',
    subCategories: [
      { id: 'textbook',    name: '教科书' },
      { id: 'paper',       name: '论文' },
      { id: 'docs',        name: '官方文档' },
      { id: 'wiki',        name: '百科' },
    ],
  },
  // ── 7. 转场衔接 — 段落间的过渡设计 ──
  {
    id: 'transition',
    name: '转场衔接', icon: '🔄', color: '#1abc9c',
    description: '段落/幕之间的衔接：章节卡、过渡动画',
    subCategories: [
      { id: 'chapter_card', name: '章节卡' },
      { id: 'progress',     name: '进度指示' },
      { id: 'recap',        name: '回顾摘要' },
      { id: 'bridge_anim',  name: '过渡动画' },
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

// ─────────── 各维度数据结构 ───────────

/** 旁白文稿 — 一段旁白文字 + 预估时长 */
export interface NarrationAssetData {
  /** 旁白文字 */
  text: string;
  /** 预估时长（秒） */
  durationSec?: number;
  /** 语气/风格 */
  tone?: 'casual' | 'serious' | 'humorous' | 'dramatic';
  /** 关键词（用于字幕高亮） */
  keywords?: string[];
}

/** 视觉画面 — 动画/图表/插画描述 */
export interface VisualAssetData {
  /** 视觉类型 */
  visualType: 'animation' | 'diagram' | 'chart' | 'screencast' | 'illustration' | 'photo';
  /** 描述（用于设计/生成） */
  description: string;
  /** 画面关键元素 */
  elements?: string[];
  /** 绑定的积木名 */
  blockName?: string;
  /** 图片/视频路径 */
  filePath?: string;
}

/** 文字叠层 — 画面上显示的文字 */
export interface TextOverlayAssetData {
  /** 叠层类型 */
  overlayType: 'title' | 'bullet' | 'formula' | 'code' | 'caption' | 'quote';
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
}

/** 音频音效 */
export interface AudioAssetData {
  /** 音频类型 */
  audioType: 'bgm' | 'sfx' | 'alert' | 'ambient';
  /** 文件路径 */
  filePath?: string;
  /** 描述 */
  description: string;
  /** 时长（秒） */
  durationSec?: number;
}

/** 数据素材 — 驱动图表/动画的结构化数据 */
export interface DataAssetData {
  /** 数据类型 */
  dataType: 'dataset' | 'timeline' | 'comparison' | 'code_sample' | 'table';
  /** 时间线事件 */
  events?: { year: string; text: string; color?: string; icon?: string }[];
  /** 对比结构 */
  comparison?: {
    left: { icon?: string; value: string; label: string; color: string; subItems?: string[] };
    right: { icon?: string; value: string; label: string; color: string; subItems?: string[] };
  };
  /** 表格数据 */
  rows?: { key: string; value: string }[];
  /** 代码示例 */
  code?: string;
  codeLanguage?: string;
}

/** 引用来源 — 一条溯源信息 */
export interface ReferenceAssetData {
  /** 引用类型 */
  refType: 'textbook' | 'paper' | 'docs' | 'wiki';
  /** 完整引用 */
  citation: string;
  /** 相关章节/页码 */
  location?: string;
  /** URL */
  url?: string;
}

/** 转场衔接 — 章节卡/进度/回顾 */
export interface TransitionAssetData {
  /** 转场类型 */
  transType: 'chapter_card' | 'progress' | 'recap' | 'bridge_anim';
  /** 标题 */
  title?: string;
  /** 内容 */
  content?: string;
  /** 章节编号 */
  chapterNum?: number;
  /** 进度百分比 */
  progress?: number;
}

// ─────────── 数据联合类型 ───────────

export type AssetData =
  | { category: 'narration';     data: NarrationAssetData }
  | { category: 'visual';        data: VisualAssetData }
  | { category: 'text_overlay';  data: TextOverlayAssetData }
  | { category: 'audio';         data: AudioAssetData }
  | { category: 'data';          data: DataAssetData }
  | { category: 'reference';     data: ReferenceAssetData }
  | { category: 'transition';    data: TransitionAssetData };

// ─────────── 原子类型（保留，仍然有用） ───────────
// 原子类型描述的是"这块数据长什么样"，与分类正交

export type AtomType =
  | 'narration_segment'  // 一段旁白
  | 'formula'            // 单个公式（LaTeX）
  | 'code_snippet'       // 代码片段
  | 'timeline_event'     // 时间线
  | 'comparison'         // A vs B 对比
  | 'person_card'        // 人物卡片
  | 'story'              // 叙事故事
  | 'term_definition'    // 术语定义
  | 'bullet_points'      // 要点列表
  | 'chapter_card'       // 章节卡
  | 'diagram_spec'       // 动画/图表规格
  | 'data_table'         // 数据表
  | 'quote'              // 引用/金句
  | 'audio_clip'         // 音频片段
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

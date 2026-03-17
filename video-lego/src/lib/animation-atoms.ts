// ═══════════════════════════════════════════════════════════
// 动画原子注册表 — 所有可用的动画效果
// Animation Atom Registry — All configurable animation effects
//
// 动画 = 原子化的运动效果
// 可以被任意积木使用，通过配置组合
// ═══════════════════════════════════════════════════════════

// ─────────── 动画类型 ───────────

export type AnimationCategory = 'entrance' | 'emphasis' | 'transition' | 'data' | 'loop';

export interface AnimationAtom {
  id: string;
  name: string;
  category: AnimationCategory;
  description: string;
  /** CSS 动画（管理 UI 预览用） */
  cssKeyframe: string;
  /** 默认参数 */
  defaults: Record<string, number | string>;
  /** 可调参数定义 */
  params: AnimationParam[];
  /** 适用的积木类型 */
  compatibleBlocks: string[] | 'all';
}

export interface AnimationParam {
  key: string;
  label: string;
  type: 'number' | 'select';
  min?: number;
  max?: number;
  step?: number;
  options?: { value: string; label: string }[];
  default: number | string;
}

// ─────────── 动画注册表 ───────────

export const ANIMATION_ATOMS: AnimationAtom[] = [
  // ── 入场动画 Entrance ──
  {
    id: 'fade-in',
    name: '淡入',
    category: 'entrance',
    description: '从透明到不透明',
    cssKeyframe: 'from { opacity: 0 } to { opacity: 1 }',
    defaults: { duration: 0.5, delay: 0 },
    params: [
      { key: 'duration', label: '时长(s)', type: 'number', min: 0.1, max: 3, step: 0.1, default: 0.5 },
      { key: 'delay', label: '延迟(s)', type: 'number', min: 0, max: 5, step: 0.1, default: 0 },
    ],
    compatibleBlocks: 'all',
  },
  {
    id: 'spring-scale',
    name: '弹簧缩放',
    category: 'entrance',
    description: '从小到大弹性缩放',
    cssKeyframe: 'from { opacity: 0; transform: scale(0.5) } to { opacity: 1; transform: scale(1) }',
    defaults: { damping: 12, stiffness: 80, delay: 0 },
    params: [
      { key: 'damping', label: '阻尼', type: 'number', min: 5, max: 30, step: 1, default: 12 },
      { key: 'stiffness', label: '刚度', type: 'number', min: 20, max: 200, step: 10, default: 80 },
      { key: 'delay', label: '延迟(帧)', type: 'number', min: 0, max: 60, step: 1, default: 0 },
    ],
    compatibleBlocks: 'all',
  },
  {
    id: 'slide-up',
    name: '上滑入场',
    category: 'entrance',
    description: '从下方滑入',
    cssKeyframe: 'from { opacity: 0; transform: translateY(30px) } to { opacity: 1; transform: translateY(0) }',
    defaults: { distance: 30, duration: 0.4, delay: 0 },
    params: [
      { key: 'distance', label: '距离(px)', type: 'number', min: 10, max: 100, step: 5, default: 30 },
      { key: 'duration', label: '时长(s)', type: 'number', min: 0.1, max: 2, step: 0.1, default: 0.4 },
      { key: 'delay', label: '延迟(s)', type: 'number', min: 0, max: 5, step: 0.1, default: 0 },
    ],
    compatibleBlocks: 'all',
  },
  {
    id: 'slide-left',
    name: '左滑入场',
    category: 'entrance',
    description: '从左侧滑入',
    cssKeyframe: 'from { opacity: 0; transform: translateX(-40px) } to { opacity: 1; transform: translateX(0) }',
    defaults: { distance: 40, duration: 0.5, delay: 0 },
    params: [
      { key: 'distance', label: '距离(px)', type: 'number', min: 10, max: 100, step: 5, default: 40 },
      { key: 'duration', label: '时长(s)', type: 'number', min: 0.1, max: 2, step: 0.1, default: 0.5 },
    ],
    compatibleBlocks: 'all',
  },
  {
    id: 'slide-right',
    name: '右滑入场',
    category: 'entrance',
    description: '从右侧滑入',
    cssKeyframe: 'from { opacity: 0; transform: translateX(40px) } to { opacity: 1; transform: translateX(0) }',
    defaults: { distance: 40, duration: 0.5, delay: 0 },
    params: [
      { key: 'distance', label: '距离(px)', type: 'number', min: 10, max: 100, step: 5, default: 40 },
      { key: 'duration', label: '时长(s)', type: 'number', min: 0.1, max: 2, step: 0.1, default: 0.5 },
    ],
    compatibleBlocks: 'all',
  },

  // ── 强调动画 Emphasis ──
  {
    id: 'pulse-glow',
    name: '脉冲发光',
    category: 'emphasis',
    description: '边框或背景呼吸式发光',
    cssKeyframe: '0% { box-shadow: 0 0 0 rgba(255,215,0,0) } 50% { box-shadow: 0 0 20px rgba(255,215,0,0.3) } 100% { box-shadow: 0 0 0 rgba(255,215,0,0) }',
    defaults: { color: '#ffd700', intensity: 20, duration: 1.5 },
    params: [
      { key: 'color', label: '颜色', type: 'select', options: [{ value: '#ffd700', label: '金色' }, { value: '#4ea8de', label: '蓝色' }, { value: '#2ecc71', label: '绿色' }, { value: '#e74c3c', label: '红色' }], default: '#ffd700' },
      { key: 'intensity', label: '强度(px)', type: 'number', min: 5, max: 40, step: 5, default: 20 },
      { key: 'duration', label: '周期(s)', type: 'number', min: 0.5, max: 5, step: 0.5, default: 1.5 },
    ],
    compatibleBlocks: ['FormulaBlock', 'StatCards', 'CodeBlock'],
  },
  {
    id: 'highlight-step',
    name: '步骤高亮',
    category: 'emphasis',
    description: '逐步高亮推导步骤',
    cssKeyframe: 'from { background: transparent } to { background: rgba(255,215,0,0.1) }',
    defaults: { stepDelay: 15, glowColor: '#ffd700' },
    params: [
      { key: 'stepDelay', label: '步间隔(帧)', type: 'number', min: 5, max: 30, step: 1, default: 15 },
      { key: 'glowColor', label: '颜色', type: 'select', options: [{ value: '#ffd700', label: '金色' }, { value: '#4ea8de', label: '蓝色' }], default: '#ffd700' },
    ],
    compatibleBlocks: ['FormulaDerivation', 'Timeline'],
  },

  // ── 数据动画 Data ──
  {
    id: 'progress-fill',
    name: '进度填充',
    category: 'data',
    description: '数值从0增长到目标值',
    cssKeyframe: 'from { width: 0% }',
    defaults: { duration: 0.8, easing: 'ease-out' },
    params: [
      { key: 'duration', label: '时长(s)', type: 'number', min: 0.2, max: 3, step: 0.1, default: 0.8 },
      { key: 'easing', label: '缓动', type: 'select', options: [{ value: 'ease-out', label: '减速' }, { value: 'linear', label: '匀速' }, { value: 'ease-in-out', label: '平滑' }], default: 'ease-out' },
    ],
    compatibleBlocks: ['ProgressBars', 'UCurve'],
  },
  {
    id: 'count-up',
    name: '数字递增',
    category: 'data',
    description: '数字从 0 递增到目标',
    cssKeyframe: '',
    defaults: { duration: 1.0 },
    params: [
      { key: 'duration', label: '时长(s)', type: 'number', min: 0.3, max: 3, step: 0.1, default: 1.0 },
    ],
    compatibleBlocks: ['StatCards', 'ProgressBars'],
  },
  {
    id: 'chart-draw',
    name: '曲线绘制',
    category: 'data',
    description: '逐点绘制曲线/折线',
    cssKeyframe: 'from { stroke-dashoffset: 2000 } to { stroke-dashoffset: 0 }',
    defaults: { pointsPerFrame: 1, drawDuration: 40 },
    params: [
      { key: 'pointsPerFrame', label: '点/帧', type: 'number', min: 0.5, max: 5, step: 0.5, default: 1 },
      { key: 'drawDuration', label: '绘制帧数', type: 'number', min: 10, max: 90, step: 5, default: 40 },
    ],
    compatibleBlocks: ['UCurve'],
  },

  // ── 组合动画 Transition ──
  {
    id: 'stagger',
    name: '交错入场',
    category: 'transition',
    description: '多个元素依次出现',
    cssKeyframe: '',
    defaults: { staggerDelay: 8, itemAnimation: 'slide-up' },
    params: [
      { key: 'staggerDelay', label: '间隔(帧)', type: 'number', min: 3, max: 30, step: 1, default: 8 },
      { key: 'itemAnimation', label: '子动画', type: 'select', options: [{ value: 'slide-up', label: '上滑' }, { value: 'fade-in', label: '淡入' }, { value: 'spring-scale', label: '弹簧' }], default: 'slide-up' },
    ],
    compatibleBlocks: ['FormulaDerivation', 'Timeline', 'StatCards', 'ComparisonSplit'],
  },
  {
    id: 'split-reveal',
    name: '左右分裂',
    category: 'transition',
    description: '左右元素分别从两侧滑入',
    cssKeyframe: '',
    defaults: { delay: 5 },
    params: [
      { key: 'delay', label: '间隔(帧)', type: 'number', min: 0, max: 20, step: 1, default: 5 },
    ],
    compatibleBlocks: ['ComparisonSplit'],
  },
];

// ─────────── 分类元数据 ───────────

export const ANIMATION_CATEGORIES = [
  { id: 'entrance',   name: '入场', icon: '🎬', color: '#2ecc71' },
  { id: 'emphasis',   name: '强调', icon: '✨', color: '#ffd700' },
  { id: 'data',       name: '数据', icon: '📊', color: '#4ea8de' },
  { id: 'transition', name: '组合', icon: '🔀', color: '#e67e22' },
  { id: 'loop',       name: '循环', icon: '🔁', color: '#9b59b6' },
] as const;

// ─────────── 辅助 ───────────

export function getAnimationAtom(id: string) {
  return ANIMATION_ATOMS.find(a => a.id === id);
}

export function getAnimationsForBlock(blockName: string) {
  return ANIMATION_ATOMS.filter(a =>
    a.compatibleBlocks === 'all' || a.compatibleBlocks.includes(blockName)
  );
}

export function getAnimationCategoryMeta(catId: string) {
  return ANIMATION_CATEGORIES.find(c => c.id === catId);
}

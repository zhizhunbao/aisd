// ═══════════════════════════════════════════════════════════
// M6 积木编辑器 — 每种积木的默认数据 + 字段 Schema
// Block Editor — Default data & field schema per block
//
// 添加新积木时，在此文件增加对应的 defaults 和 schema
// ═══════════════════════════════════════════════════════════

import type { BlockDataMap, BlockName } from '@/lib/types'
import type { BlockFieldSchema } from './types'

// ─────────── 默认数据 Default Data ───────────

export const BLOCK_DEFAULTS: Record<string, unknown> = {
  FormulaBlock: {
    latex: 'E = mc^2',
    label: '质能方程',
    color: '#ffd700',
  },
  FormulaDerivation: {
    steps: [
      { latex: 'a^2 + b^2 = c^2', annotation: '勾股定理' },
      { latex: 'c = \\sqrt{a^2 + b^2}', annotation: '解出距离', highlight: true },
    ],
    source: '教科书 Ch.1',
  },
  FormulaComparison: {
    left: { latex: 'O(n)', label: '线性搜索', color: '#e74c3c' },
    right: { latex: 'O(\\log n)', label: '二分搜索', color: '#2ecc71' },
  },
  ComparisonSplit: {
    left: { icon: '🐌', value: '方案 A', label: '慢', color: '#e74c3c', subItems: ['特点 1', '特点 2'] },
    right: { icon: '⚡', value: '方案 B', label: '快', color: '#2ecc71', subItems: ['优势 1', '优势 2'] },
  },
  Timeline: {
    events: [
      { year: '1950', text: '事件一', color: '#ffd700', icon: '📜' },
      { year: '1970', text: '事件二', color: '#4ea8de', icon: '💡' },
      { year: '2000', text: '事件三', color: '#2ecc71', icon: '🚀' },
    ],
  },
  ProgressBars: {
    bars: [
      { label: '指标 A', value: 85, color: '#2ecc71', displayValue: '85%' },
      { label: '指标 B', value: 62, color: '#4ea8de', displayValue: '62%' },
      { label: '指标 C', value: 40, color: '#e67e22', displayValue: '40%' },
    ],
  },
  StatCards: {
    cards: [
      { icon: '🎯', value: '99%', label: '准确率', color: '#ffd700' },
      { icon: '⏱', value: '0.5ms', label: '延迟', color: '#4ea8de' },
      { icon: '📊', value: '1M', label: '样本量', color: '#2ecc71' },
      { icon: '📐', value: '128', label: '维度', color: '#e67e22' },
    ],
  },
  CodeBlock: {
    code: 'import numpy as np\n\nX = np.array([[1, 2], [3, 4]])\nprint(X.shape)',
    language: 'python',
    label: 'Python 示例',
    color: '#4ea8de',
  },
  ImageDisplay: {
    src: '',
    caption: '图片说明',
    maxHeight: 400,
  },
  UCurve: {
    points: Array.from({ length: 20 }, (_, i) => {
      const x = i + 1
      const y = 0.8 * Math.pow((x - 10) / 8, 2) + 0.15
      return { x, y: Math.round(y * 1000) / 1000 }
    }),
    xLabel: 'X 轴',
    yLabel: 'Y 轴',
    zones: [
      { start: 1, end: 5, color: '#e74c3c', label: '区域 A' },
      { start: 15, end: 20, color: '#e67e22', label: '区域 B' },
    ],
    bestPoint: { x: 10, annotation: '最优点' },
  },
  KeyPoints: {
    points: [
      { icon: '✅', text: '要点一', color: '#2ecc71' },
      { icon: '💡', text: '要点二', color: '#ffd700' },
      { icon: '⚠️', text: '要点三', color: '#e67e22' },
    ],
  },
  ConclusionBanner: {
    text: '总结结论文字',
    icon: '🎯',
  },
}

// ─────────── 字段 Schema ───────────

export const BLOCK_SCHEMAS: Record<string, BlockFieldSchema> = {
  FormulaBlock: {
    fields: [
      { key: 'latex', label: 'LaTeX 公式', type: 'latex', required: true, placeholder: 'E = mc^2' },
      { key: 'label', label: '标签', type: 'text', placeholder: '公式名称' },
      { key: 'color', label: '颜色', type: 'color', defaultValue: '#ffd700' },
    ],
    arrayFields: [],
  },
  FormulaDerivation: {
    fields: [
      { key: 'source', label: '来源', type: 'text', placeholder: '教科书 Ch.X' },
    ],
    arrayFields: [
      {
        key: 'steps', label: '推导步骤', itemDefault: { latex: '', annotation: '', highlight: false },
        itemFields: [
          { key: 'latex', label: 'LaTeX', type: 'latex', required: true },
          { key: 'annotation', label: '注释', type: 'text' },
          { key: 'highlight', label: '高亮', type: 'boolean' },
        ],
      },
    ],
  },
  FormulaComparison: {
    fields: [],
    arrayFields: [],
  },
  ComparisonSplit: {
    fields: [
      { key: 'left.icon', label: '左图标', type: 'text', group: '左侧' },
      { key: 'left.value', label: '左标题', type: 'text', group: '左侧', required: true },
      { key: 'left.label', label: '左副标题', type: 'text', group: '左侧' },
      { key: 'left.color', label: '左颜色', type: 'color', group: '左侧' },
      { key: 'right.icon', label: '右图标', type: 'text', group: '右侧' },
      { key: 'right.value', label: '右标题', type: 'text', group: '右侧', required: true },
      { key: 'right.label', label: '右副标题', type: 'text', group: '右侧' },
      { key: 'right.color', label: '右颜色', type: 'color', group: '右侧' },
    ],
    arrayFields: [
      {
        key: 'left.subItems', label: '左侧子项', group: '左侧',
        itemDefault: '', itemFields: [{ key: '_value', label: '文字', type: 'text' }],
      },
      {
        key: 'right.subItems', label: '右侧子项', group: '右侧',
        itemDefault: '', itemFields: [{ key: '_value', label: '文字', type: 'text' }],
      },
    ],
  },
  Timeline: {
    fields: [],
    arrayFields: [
      {
        key: 'events', label: '事件列表',
        itemDefault: { year: '', text: '', color: '#4ea8de', icon: '📌' },
        itemFields: [
          { key: 'year', label: '年份', type: 'text', required: true },
          { key: 'text', label: '描述', type: 'text', required: true },
          { key: 'color', label: '颜色', type: 'color' },
          { key: 'icon', label: '图标', type: 'text', placeholder: 'emoji' },
        ],
      },
    ],
  },
  ProgressBars: {
    fields: [],
    arrayFields: [
      {
        key: 'bars', label: '进度条列表',
        itemDefault: { label: '', value: 50, color: '#4ea8de', displayValue: '50%' },
        itemFields: [
          { key: 'label', label: '标签', type: 'text', required: true },
          { key: 'value', label: '数值 (0-100)', type: 'number' },
          { key: 'color', label: '颜色', type: 'color' },
          { key: 'displayValue', label: '显示值', type: 'text', placeholder: 'e.g. 85%' },
        ],
      },
    ],
  },
  StatCards: {
    fields: [],
    arrayFields: [
      {
        key: 'cards', label: '卡片列表',
        itemDefault: { icon: '📊', value: '', label: '', color: '#4ea8de' },
        itemFields: [
          { key: 'icon', label: '图标', type: 'text', placeholder: 'emoji' },
          { key: 'value', label: '数值', type: 'text', required: true },
          { key: 'label', label: '标签', type: 'text', required: true },
          { key: 'color', label: '颜色', type: 'color' },
          { key: 'description', label: '描述', type: 'text' },
        ],
      },
    ],
  },
  CodeBlock: {
    fields: [
      { key: 'code', label: '代码', type: 'code', required: true },
      { key: 'language', label: '语言', type: 'select', options: [
        { value: 'python', label: 'Python' },
        { value: 'javascript', label: 'JavaScript' },
        { value: 'typescript', label: 'TypeScript' },
        { value: 'java', label: 'Java' },
        { value: 'cpp', label: 'C++' },
        { value: 'sql', label: 'SQL' },
        { value: 'bash', label: 'Bash' },
      ]},
      { key: 'label', label: '标签', type: 'text', placeholder: '代码说明' },
      { key: 'color', label: '颜色', type: 'color' },
    ],
    arrayFields: [],
  },
  ImageDisplay: {
    fields: [
      { key: 'src', label: '图片地址', type: 'text', required: true, placeholder: 'URL or public path' },
      { key: 'caption', label: '说明文字', type: 'text' },
      { key: 'maxHeight', label: '最大高度', type: 'number' },
    ],
    arrayFields: [],
  },
  UCurve: {
    fields: [
      { key: 'xLabel', label: 'X 轴标签', type: 'text', required: true },
      { key: 'yLabel', label: 'Y 轴标签', type: 'text', required: true },
    ],
    arrayFields: [
      {
        key: 'points', label: '数据点',
        itemDefault: { x: 0, y: 0 },
        itemFields: [
          { key: 'x', label: 'X', type: 'number', required: true },
          { key: 'y', label: 'Y', type: 'number', required: true },
        ],
      },
      {
        key: 'zones', label: '区域标注',
        itemDefault: { start: 0, end: 5, color: '#e74c3c', label: '' },
        itemFields: [
          { key: 'start', label: '起始', type: 'number' },
          { key: 'end', label: '结束', type: 'number' },
          { key: 'color', label: '颜色', type: 'color' },
          { key: 'label', label: '标签', type: 'text' },
        ],
      },
    ],
  },
  KeyPoints: {
    fields: [],
    arrayFields: [
      {
        key: 'points', label: '要点列表',
        itemDefault: { icon: '✅', text: '', color: '#2ecc71' },
        itemFields: [
          { key: 'icon', label: '图标', type: 'text', placeholder: 'emoji' },
          { key: 'text', label: '文字', type: 'text', required: true },
          { key: 'color', label: '颜色', type: 'color' },
          { key: 'bold', label: '加粗', type: 'boolean' },
        ],
      },
    ],
  },
  ConclusionBanner: {
    fields: [
      { key: 'text', label: '结论文字', type: 'textarea', required: true },
      { key: 'icon', label: '图标', type: 'text', placeholder: 'emoji', defaultValue: '🎯' },
    ],
    arrayFields: [],
  },
}

/** 获取积木默认数据 */
export function getBlockDefault<T extends BlockName>(name: T): BlockDataMap[T] {
  return (BLOCK_DEFAULTS[name] ?? {}) as BlockDataMap[T]
}

/** 获取积木字段 Schema */
export function getBlockSchema(name: string): BlockFieldSchema {
  return BLOCK_SCHEMAS[name] ?? { fields: [], arrayFields: [] }
}

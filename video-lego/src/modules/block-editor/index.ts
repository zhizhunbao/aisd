// ═══════════════════════════════════════════════════════════
// M6 积木编辑器 — 模块入口
// Block Editor Module — barrel export
//
// 模块自治原则:
//   types.ts      → 本模块的类型定义
//   defaults.ts   → 积木默认数据 + 字段 Schema
//   components/   → 本模块的 UI 组件
//   index.ts      → 对外暴露的公共 API
// ═══════════════════════════════════════════════════════════

export { BlockEditorPage } from './BlockEditorPage'
export type { BlockEditorState, BlockFieldSchema, FieldDescriptor } from './types'
export { getBlockDefault, getBlockSchema } from './defaults'

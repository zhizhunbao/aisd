// ═══════════════════════════════════════════════════════════
// M9 场景编排器 — 模块入口
// Scene Composer Module — barrel export
//
// 模块自治原则:
//   types.ts   → 本模块的类型定义
//   data.ts    → 本模块的数据
//   components/ → 本模块的 UI 组件
//   index.ts   → 对外暴露的公共 API
// ═══════════════════════════════════════════════════════════

export { SceneComposerPage } from './SceneComposerPage'
export type { VideoSceneProject } from './types'

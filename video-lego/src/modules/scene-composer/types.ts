// ═══════════════════════════════════════════════════════════
// M9 场景编排器 — 模块内部类型
// Scene Composer — Module-local types
//
// 这些类型只在 M9 模块内部使用。
// 跨模块共享的类型（SceneData, KeyPoint...）在 @/lib/types.ts
// ═══════════════════════════════════════════════════════════

import type { SceneData } from '@/lib/types'

/** 一个视频的场景数据集 — M9 管理的核心对象 */
export interface VideoSceneProject {
  /** 课程 */
  course: string
  /** 主题 */
  topic: string
  /** 幕列表（用于分组） */
  acts: Record<string, string>
  /** 场景数据数组 */
  scenes: SceneData[]
}

/** 场景编排器注册表 — 所有已知的视频场景项目 */
export type SceneRegistry = VideoSceneProject[]

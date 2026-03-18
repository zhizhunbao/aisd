// ═══════════════════════════════════════════════════════════
// M6 积木编辑器 — 模块内部类型
// Block Editor — Module-local types
//
// 这些类型只在 M6 编辑器模块内部使用。
// 积木元数据（BlockMeta）和积木数据（BlockDataMap）在 @blocks/ 和 @/lib/
// ═══════════════════════════════════════════════════════════

import type { BlockName, BlockDataMap } from '@/lib/types'

/** 字段描述 — 描述积木 props 中的一个可编辑字段 */
export interface FieldDescriptor {
  /** 字段 key（对应 data 中的 key） */
  key: string
  /** 显示标签 */
  label: string
  /** 字段类型 */
  type: 'text' | 'number' | 'color' | 'textarea' | 'latex' | 'code' | 'boolean' | 'select' | 'json'
  /** 默认值 */
  defaultValue?: unknown
  /** 占位提示 */
  placeholder?: string
  /** select 下拉选项 */
  options?: { value: string; label: string }[]
  /** 是否必填 */
  required?: boolean
  /** 分组标签 */
  group?: string
}

/** 数组字段描述 — 描述积木 props 中的一个数组类型字段 */
export interface ArrayFieldDescriptor {
  /** 字段 key（对应 data 中的数组 key） */
  key: string
  /** 显示标签 */
  label: string
  /** 数组中每个元素的字段描述 */
  itemFields: FieldDescriptor[]
  /** 新增元素的默认值模板 */
  itemDefault: Record<string, unknown>
  /** 分组标签 */
  group?: string
}

/** 积木的完整字段 schema — 用于自动生成编辑表单 */
export interface BlockFieldSchema {
  /** 简单字段列表 */
  fields: FieldDescriptor[]
  /** 数组字段列表 */
  arrayFields: ArrayFieldDescriptor[]
}

/** 编辑器中一个积木实例的状态 */
export interface BlockEditorState {
  /** 当前选中的积木名称 */
  blockName: BlockName
  /** 当前编辑的数据 */
  data: BlockDataMap[BlockName]
  /** 是否有未保存的修改 */
  dirty: boolean
}

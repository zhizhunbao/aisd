// ═══════════════════════════════════════════════════════════
// M6 积木编辑器 — 主页面（统一 ModuleLayout 三栏）
// Block Editor — Main page with unified ModuleLayout
//
// 左侧: ModuleHeader + 积木列表（分类+搜索+新建）
// 中间: 实时预览画布
// 右侧: 参数编辑面板
// ═══════════════════════════════════════════════════════════

import { useState, useCallback } from 'react'
import { IconBlocks, IconEdit } from '@/components/Icons'
import type { BlockName, BlockDataMap } from '@/lib/types'
import { getBlockDefault } from './defaults'
import { BlockList } from './components/BlockList'
import { PreviewCanvas } from './components/PreviewCanvas'
import { PropsEditor } from './components/PropsEditor'
import { ModuleLayout, ModuleHeader } from '@/components/ModuleLayout'
import { MGMT } from '@/theme'

const COLOR = '#f59e0b'

export function BlockEditorPage() {
  const [selectedBlock, setSelectedBlock] = useState<BlockName | null>(null)
  const [blockData, setBlockData] = useState<BlockDataMap[BlockName] | null>(null)

  const selectBlock = useCallback((name: string) => {
    const blockName = name as BlockName
    setSelectedBlock(blockName)
    setBlockData(getBlockDefault(blockName))
  }, [])

  const handleDataChange = useCallback((data: Record<string, unknown>) => {
    setBlockData(data as BlockDataMap[BlockName])
  }, [])

  const handleCreate = useCallback(() => {
    alert('新建积木功能即将上线\n\n计划流程:\n1. 选择分类\n2. 输入名称\n3. 定义 Props Schema\n4. 生成三层骨架代码')
  }, [])

  return (
    <ModuleLayout
      left={
        <>
          <ModuleHeader
            icon={<IconBlocks size={16} />}
            title="M6 积木编辑器"
            subtitle="Block Editor · 分类浏览 + 实时预览"
            color={COLOR}
          />
          <BlockList
            selectedBlock={selectedBlock}
            onSelect={selectBlock}
            onCreate={handleCreate}
          />
        </>
      }
      center={
        <PreviewCanvas blockName={selectedBlock} data={blockData} />
      }
      right={
        selectedBlock ? (
          <PropsEditor
            blockName={selectedBlock}
            data={(blockData || {}) as Record<string, unknown>}
            onChange={handleDataChange}
          />
        ) : (
          <div style={{
            flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center',
            flexDirection: 'column', color: MGMT.grayLight, gap: 12,
          }}>
            <div style={{ display: 'flex', justifyContent: 'center', opacity: 0.3, marginBottom: 8 }}>
              <IconEdit size={40} />
            </div>
            <div style={{ fontSize: 13 }}>选择积木后编辑参数</div>
          </div>
        )
      }
    />
  )
}

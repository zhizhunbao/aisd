// ═══════════════════════════════════════════════════════════
// M6 积木编辑器 — 中间预览画布
// Block Editor — Center Panel: Live preview canvas
//
// 实时渲染积木的 .view 组件 + 缩放控制
// ═══════════════════════════════════════════════════════════

import { useState } from 'react'
import { MGMT } from '@/theme'
import { getBlockMeta } from '@blocks/catalog'
import { IconBlocks, IconBox, IconWarning } from '@/components/Icons'
import { SmallBtn } from './shared'
import { IconPreview } from '@/components/Icons'
import type { BlockName, BlockDataMap } from '@/lib/types'

// ── View 组件导入 ──
import { FormulaBlockView } from '@blocks/formula/FormulaBlock'
import { FormulaDerivationView } from '@blocks/formula/FormulaDerivation'
import { UCurveView } from '@blocks/chart/UCurve'
import { ComparisonSplitView } from '@blocks/structure/ComparisonSplit'
import { TimelineView } from '@blocks/structure/Timeline'
import { ProgressBarsView } from '@blocks/data/ProgressBars'
import { StatCardsView } from '@blocks/data/StatCards'
import { CodeBlockView } from '@blocks/data/CodeBlock'
import { ImageDisplayView } from '@blocks/data/ImageDisplay'

interface PreviewCanvasProps {
  blockName: BlockName | null
  data: BlockDataMap[BlockName] | null
}

export function PreviewCanvas({ blockName, data }: PreviewCanvasProps) {
  const [zoom, setZoom] = useState(0.65)

  const meta = blockName ? getBlockMeta(blockName) : null

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      {/* 工具栏 */}
      <div style={{
        display: 'flex', alignItems: 'center', gap: 8,
        padding: '8px 16px', borderBottom: `1px solid ${MGMT.border}`,
        minHeight: 40,
      }}>
        <IconPreview size={14} style={{ color: MGMT.grayLight }} />
        <span style={{ fontSize: 12, color: MGMT.grayLight, flex: 1 }}>
          {meta ? (
            <>
              <span style={{ color: meta.category.color }}>{meta.category.icon}</span>{' '}
              <span style={{ color: MGMT.white, fontWeight: 600, fontFamily: MGMT.codeFontFamily }}>{blockName}</span>
            </>
          ) : '选择积木开始编辑'}
        </span>

        {/* 缩放控制 */}
        <SmallBtn color={MGMT.grayLight} onClick={() => setZoom(z => Math.max(0.25, z - 0.1))}>−</SmallBtn>
        <span style={{ fontSize: 11, color: MGMT.grayLight, minWidth: 36, textAlign: 'center', fontFamily: MGMT.codeFontFamily }}>
          {Math.round(zoom * 100)}%
        </span>
        <SmallBtn color={MGMT.grayLight} onClick={() => setZoom(z => Math.min(1.5, z + 0.1))}>+</SmallBtn>
        <SmallBtn color={MGMT.dimWhite} onClick={() => setZoom(0.65)}>重置</SmallBtn>
      </div>

      {/* 画布区域 */}
      <div style={{
        flex: 1, overflow: 'auto', display: 'flex', alignItems: 'center', justifyContent: 'center',
        background: `radial-gradient(circle at center, ${MGMT.bgCard} 0%, ${MGMT.bg} 100%)`,
        position: 'relative',
      }}>
        {/* 网格背景 */}
        <div style={{
          position: 'absolute', inset: 0, opacity: 0.08,
          backgroundImage: `linear-gradient(${MGMT.white}15 1px, transparent 1px), linear-gradient(90deg, ${MGMT.white}15 1px, transparent 1px)`,
          backgroundSize: '40px 40px',
        }} />

        {blockName && data ? (
          <div style={{
            transform: `scale(${zoom})`, transformOrigin: 'center center',
            transition: 'transform 0.2s ease',
            position: 'relative', zIndex: 1,
          }}>
            {/* 1920×1080 虚拟画布 */}
            <div style={{
              width: 960, minHeight: 400,
              padding: 40,
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              borderRadius: 12,
              background: 'linear-gradient(180deg, rgba(26,26,46,0.95), rgba(15,15,30,0.95))',
              border: `1px solid ${MGMT.border}`,
              boxShadow: '0 20px 60px rgba(0,0,0,0.4)',
            }}>
              <BlockRenderer blockName={blockName} data={data} />
            </div>
          </div>
        ) : (
          <EmptyState />
        )}
      </div>
    </div>
  )
}

// ─── 积木渲染器 ───

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function BlockRenderer({ blockName, data }: { blockName: string; data: any }) {
  try {
    switch (blockName) {
      case 'FormulaBlock':
        return <FormulaBlockView
          latex={data.latex || ''}
          label={data.label}
          color={data.color}
        />
      case 'FormulaDerivation':
        return <FormulaDerivationView
          steps={data.steps || []}
          source={data.source}
        />
      case 'ComparisonSplit':
        return <ComparisonSplitView
          left={data.left}
          right={data.right}
        />
      case 'Timeline':
        return <TimelineView
          events={data.events || []}
        />
      case 'ProgressBars':
        return <ProgressBarsView
          bars={data.bars || []}
        />
      case 'StatCards':
        return <StatCardsView
          cards={data.cards || []}
        />
      case 'CodeBlock':
        return <CodeBlockView
          code={data.code || ''}
          language={data.language}
          label={data.label}
          color={data.color}
        />
      case 'ImageDisplay':
        return <ImageDisplayView
          src={data.src || ''}
          caption={data.caption}
          maxHeight={data.maxHeight}
        />
      case 'UCurve':
        return <UCurveView
          points={data.points || []}
          xLabel={data.xLabel || ''}
          yLabel={data.yLabel || ''}
          zones={data.zones}
          bestPoint={data.bestPoint}
          axisOpacity={1}
          visiblePointCount={(data.points || []).length}
          zoneOpacity={1}
          bestOpacity={data.bestPoint ? 1 : 0}
          bestScale={1}
        />
      default:
        return (
          <div style={{ color: MGMT.dimWhite, textAlign: 'center', padding: 40 }}>
            <div style={{ display: 'flex', justifyContent: 'center', marginBottom: 12, opacity: 0.4 }}><IconBox size={48} /></div>
            <div style={{ fontSize: 14 }}>「{blockName}」预览未实现</div>
            <div style={{ fontSize: 12, color: MGMT.grayLight, marginTop: 6 }}>JSON 数据编辑可用</div>
          </div>
        )
    }
  } catch {
    return (
      <div style={{ color: MGMT.red, textAlign: 'center', padding: 40 }}>
        <div style={{ display: 'flex', justifyContent: 'center', marginBottom: 8 }}><IconWarning size={36} style={{ color: MGMT.red }} /></div>
        <div style={{ fontSize: 13 }}>渲染出错，请检查数据</div>
      </div>
    )
  }
}

// ─── 空状态 ───

function EmptyState() {
  return (
    <div style={{ textAlign: 'center', color: MGMT.grayLight }}>
      <div style={{ display: 'flex', justifyContent: 'center', marginBottom: 16, opacity: 0.3 }}>
        <IconBlocks size={64} />
      </div>
      <div style={{ fontSize: 16, fontWeight: 600, color: MGMT.dimWhite, marginBottom: 8 }}>
        积木编辑器
      </div>
      <div style={{ fontSize: 13, lineHeight: 1.8, maxWidth: 280 }}>
        从左侧选择一个积木<br />
        右侧面板编辑参数<br />
        中间实时预览效果
      </div>
    </div>
  )
}

// ═══════════════════════════════════════════════════════════
// M9 积木预览渲染器
// 积木名 + 数据 → 渲染实际 React 组件
// ═══════════════════════════════════════════════════════════

import React from 'react'
import { MGMT } from '@/theme'
import { getBlockMeta } from '@blocks/catalog'

// ── 积木 view 组件导入 ──
import { FormulaBlockView } from '@blocks/formula/FormulaBlock.view'
import { FormulaDerivationView } from '@blocks/formula/FormulaDerivation.view'
import { ComparisonSplitView } from '@blocks/structure/ComparisonSplit.view'
import { TimelineView } from '@blocks/structure/Timeline.view'
import { StatCardsView } from '@blocks/data/StatCards.view'
import { ProgressBarsView } from '@blocks/data/ProgressBars.view'
import { CodeBlockView } from '@blocks/data/CodeBlock.view'
import { ImageDisplayView } from '@blocks/data/ImageDisplay.view'
import { UCurveView } from '@blocks/chart/UCurve.view'
import { KeyPointsView } from '@blocks/text/KeyPoints.view'
import { ConclusionBannerView } from '@blocks/text/ConclusionBanner.view'

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const BLOCK_RENDERERS: Record<string, React.FC<any>> = {
  FormulaBlock: FormulaBlockView,
  FormulaDerivation: FormulaDerivationView,
  ComparisonSplit: ComparisonSplitView,
  Timeline: TimelineView,
  StatCards: StatCardsView,
  ProgressBars: ProgressBarsView,
  CodeBlock: CodeBlockView,
  ImageDisplay: ImageDisplayView,
  UCurve: UCurveView,
  KeyPoints: KeyPointsView,
  ConclusionBanner: ConclusionBannerView,
}

/** 获取积木中文短名 */
function getLabel(name: string): string {
  const meta = getBlockMeta(name)
  if (!meta) return name
  const desc = meta.description
  return desc.includes('，') ? desc.split('，')[0] : desc
}

/**
 * 预处理积木数据 — 适配管理 UI 环境
 * 比如 ImageDisplay 的 src 在 Remotion 用 staticFile()，
 * 这里需要转成可访问的 URL
 */
function preprocessData(blockName: string, data: unknown): Record<string, unknown> {
  const d = { ...(data as Record<string, unknown>) }

  // 防御性默认值 — 避免 view 组件因空 data 崩溃
  if (blockName === 'StatCards' && !d.cards) d.cards = []
  if (blockName === 'ProgressBars' && !d.bars) d.bars = []
  if (blockName === 'Timeline' && !d.events) d.events = []
  if (blockName === 'FormulaDerivation' && !d.steps) d.steps = []
  if (blockName === 'ComparisonSplit' && !d.left) {
    d.left = { label: '', value: '', color: '#888' }
    d.right = { label: '', value: '', color: '#888' }
  }
  if (blockName === 'UCurve' && !d.points) {
    d.points = []; d.xLabel = ''; d.yLabel = ''
  }
  if (blockName === 'CodeBlock' && !d.code) d.code = ''
  if (blockName === 'FormulaBlock' && !d.latex) d.latex = ''
  if (blockName === 'KeyPoints' && !d.points) d.points = []
  if (blockName === 'ConclusionBanner' && !d.text) d.text = ''

  if (blockName === 'ImageDisplay' && d.src && typeof d.src === 'string') {
    if (!d.src.startsWith('http') && !d.src.startsWith('/')) {
      d.resolvedSrc = `/${d.src}`
    }
  }

  return d
}

/** 渲染单个积木预览 */
export function BlockPreview({ blockName, data }: { blockName: string; data: unknown }) {
  const Renderer = BLOCK_RENDERERS[blockName]

  if (!Renderer) {
    const zhLabel = getLabel(blockName)
    return (
      <div style={{
        height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center',
        background: `${MGMT.white}04`, color: MGMT.grayLight, fontSize: 11,
      }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: 11 }}>{zhLabel}</div>
          <div style={{ fontSize: 9, opacity: 0.5, marginTop: 2 }}>积木未实现，无法预览</div>
        </div>
      </div>
    )
  }

  const processedData = preprocessData(blockName, data)

  return (
    <div style={{
      width: '100%', height: '100%',
      overflow: 'hidden', position: 'relative',
    }}>
      {/* 积木按 1080p 设计，缩放到画布容器 */}
      <div style={{
        transform: 'scale(0.5)', transformOrigin: 'top left',
        width: '200%',
      }}>
        <Renderer {...processedData} />
      </div>
    </div>
  )
}

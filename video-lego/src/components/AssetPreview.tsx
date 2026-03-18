// ═══════════════════════════════════════════════════════════
// 素材预览 — 精简为 3 类核心素材预览
// AssetPreview — Formula, Code, Person previews only
//
// 支持两种模式:
//   static=false (默认): 详情页，带循环动画
//   static=true:         卡片缩略图，静态无动画
// ═══════════════════════════════════════════════════════════

import React, { useEffect, useState } from 'react'
import 'katex/dist/katex.min.css'
import { BlockMath } from 'react-katex'
import { MGMT } from '@/theme'
import type { Asset } from '@/lib/asset-types'
import { IconPackage } from './Icons'
import { getDiagramComponent } from './diagrams'

// ─────────── CSS Keyframes ───────────

const KF_ID = 'asset-preview-kf'
function ensureKF() {
  if (document.getElementById(KF_ID)) return
  const s = document.createElement('style')
  s.id = KF_ID
  s.textContent = `
    @keyframes ap-fade { from { opacity:0; transform:scale(0.9) } to { opacity:1; transform:scale(1) } }
    @keyframes ap-slide { from { opacity:0; transform:translateY(12px) } to { opacity:1; transform:translateY(0) } }
  `
  document.head.appendChild(s)
}

function useLoop(ms = 4000, enabled = true) {
  const [k, setK] = useState(0)
  useEffect(() => {
    if (!enabled) return
    ensureKF()
    const t = setInterval(() => setK(n => n + 1), ms)
    return () => clearInterval(t)
  }, [ms, enabled])
  return enabled ? k : 0
}

// ─────────── Props ───────────

interface PreviewProps {
  asset: Asset
  isStatic?: boolean
}

function anim(isStatic: boolean, name: string, delay = 0): React.CSSProperties {
  if (isStatic) return {}
  return { animation: `${name} 0.5s ease-out ${delay}s both` }
}

// ─────────── 公式 / 代码 预览 ───────────

const TextOverlayPreview: React.FC<PreviewProps> = ({ asset, isStatic }) => {
  const key = useLoop(4000, !isStatic)
  const d = asset.content.data as any

  // 公式渲染 (LaTeX)
  if (d.overlayType === 'formula' && d.latex) {
    // 合并组件: LaTeX + 动态图 在一个 .tsx 里
    const DiagramComp = getDiagramComponent(asset.id)

    // 如果有注册的合并组件，直接渲染（它自带公式+图）
    if (DiagramComp) {
      return (
        <div style={{ ...anim(!!isStatic, 'ap-fade') }}>
          <DiagramComp compact={!!isStatic} />
        </div>
      )
    }

    // 兜底: 无合并组件时用原始 LaTeX + diagramSvg
    return (
      <div style={{ textAlign: 'center', padding: isStatic ? '8px 6px' : 12, ...anim(!!isStatic, 'ap-fade') }}>
        <div style={{ fontSize: isStatic ? 16 : 22, color: d.color || '#ffd700' }}>
          <BlockMath math={d.latex} />
        </div>
        {d.intuition && <div style={{ color: MGMT.dimWhite, fontSize: isStatic ? 9 : 11, marginTop: 2, fontFamily: MGMT.fontFamily }}>{d.intuition}</div>}
        {d.diagramSvg && (
          <div style={{
            marginTop: isStatic ? 4 : 10, padding: isStatic ? '2px 4px' : '6px 10px',
            background: 'rgba(255,255,255,0.03)', borderRadius: 6,
            border: '1px solid rgba(255,255,255,0.06)', display: 'inline-block',
          }}>
            <div
              style={{ width: isStatic ? 60 : 120, height: isStatic ? 40 : 80, opacity: 0.9 }}
              dangerouslySetInnerHTML={{ __html: d.diagramSvg }}
            />
          </div>
        )}
      </div>
    )
  }

  // 代码渲染
  if (d.overlayType === 'code') {
    return (
      <div key={key} style={{ padding: isStatic ? '8px 10px' : '10px 12px', ...anim(!!isStatic, 'ap-fade') }}>
        {d.language && <div style={{ fontSize: 9, color: MGMT.blue, fontWeight: 600, marginBottom: 4 }}>{d.language}</div>}
        <pre style={{
          fontSize: isStatic ? 8 : 10, color: '#e6edf3', fontFamily: MGMT.codeFontFamily,
          margin: 0, whiteSpace: 'pre-wrap', lineHeight: 1.4, background: '#0d1117',
          borderRadius: 4, padding: 6, overflow: 'hidden', maxHeight: isStatic ? 80 : 120,
        }}>
          {d.text}
        </pre>
      </div>
    )
  }

  // 文字/标题
  return (
    <div key={key} style={{ padding: '10px 14px', ...anim(!!isStatic, 'ap-fade') }}>
      <div style={{ fontSize: 11, color: d.color || MGMT.gold, lineHeight: 1.5, fontFamily: MGMT.fontFamily, whiteSpace: 'pre-line' }}>
        {d.text}
      </div>
    </div>
  )
}

// ─────────── 人物 预览 ───────────

const PersonPreview: React.FC<PreviewProps> = ({ asset, isStatic }) => {
  const key = useLoop(5000, !isStatic)
  const d = asset.content.data as any
  return (
    <div key={key} style={{ padding: isStatic ? '10px' : '14px', textAlign: 'center', ...anim(!!isStatic, 'ap-fade') }}>
      {/* 头像占位 */}
      <div style={{
        width: isStatic ? 40 : 56, height: isStatic ? 40 : 56, borderRadius: '50%',
        background: `${MGMT.blue}25`, border: `2px solid ${MGMT.blue}50`,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        margin: '0 auto 6px', fontSize: isStatic ? 18 : 24, color: `${MGMT.blue}60`,
      }}>
        {(d.name || asset.name).charAt(0)}
      </div>
      <div style={{ fontSize: isStatic ? 11 : 14, fontWeight: 700, color: MGMT.white, marginBottom: 2 }}>
        {d.name || asset.name}
      </div>
      {d.title && <div style={{ fontSize: isStatic ? 9 : 11, color: MGMT.dimWhite }}>{d.title}</div>}
      {!isStatic && d.bio && (
        <div style={{ fontSize: 10, color: MGMT.grayLight, marginTop: 4, lineHeight: 1.3,
          overflow: 'hidden', display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical' as const }}>
          {d.bio}
        </div>
      )}
    </div>
  )
}

// ─────────── 兜底 ───────────

function FallbackPreview() {
  return (
    <div style={{ color: MGMT.grayLight, textAlign: 'center', padding: 16 }}>
      <div style={{ display: 'flex', justifyContent: 'center', marginBottom: 4 }}>
        <IconPackage size={28} style={{ opacity: 0.4 }} />
      </div>
      <div style={{ fontSize: 10 }}>预览</div>
    </div>
  )
}

// ─────────── 预览路由 ───────────

const PREVIEW_MAP: Record<string, React.FC<PreviewProps>> = {
  text_overlay: TextOverlayPreview,
  person: PersonPreview,
}

/**
 * 素材预览组件
 * @param asset 素材对象
 * @param isStatic true = 静态模式（卡片缩略图），false = 带动画（详情页）
 */
export function AssetPreview({ asset, isStatic = false }: { asset: Asset; isStatic?: boolean }) {
  const contentCategory = asset.content?.category
  const Preview = contentCategory ? PREVIEW_MAP[contentCategory] : undefined
  if (!Preview) return <FallbackPreview />
  return <Preview asset={asset} isStatic={isStatic} />
}

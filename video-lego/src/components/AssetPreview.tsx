// ═══════════════════════════════════════════════════════════
// 素材预览 — 根据视频制作维度渲染迷你预览
// AssetPreview — Mini preview based on video production dimension
// ═══════════════════════════════════════════════════════════

import React, { useEffect, useState } from 'react'
import 'katex/dist/katex.min.css'
import { BlockMath } from 'react-katex'
import { MGMT } from '@/theme'
import type { Asset } from '@/lib/asset-types'

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

function useLoop(ms = 4000) {
  const [k, setK] = useState(0)
  useEffect(() => { ensureKF(); const t = setInterval(() => setK(n => n + 1), ms); return () => clearInterval(t) }, [ms])
  return k
}

// ─────────── 各维度预览 ───────────

/** 🎙️ 旁白 — 文字 + 时长 + 语气 */
const NarrationPreview: React.FC<{ asset: Asset }> = ({ asset }) => {
  const key = useLoop(6000)
  const d = asset.content.data as any
  const toneIcon = ({ casual: '😄', serious: '🧐', humorous: '😂', dramatic: '🎭' } as Record<string, string>)[d.tone || 'casual'] || '🎙️'
  return (
    <div key={key} style={{ padding: '12px 16px', animation: 'ap-fade 0.5s ease-out both' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 8 }}>
        <span style={{ fontSize: 16 }}>{toneIcon}</span>
        {d.durationSec && <span style={{ fontSize: 10, padding: '1px 6px', borderRadius: 3, background: `${MGMT.blue}20`, color: MGMT.blue, fontWeight: 600 }}>{d.durationSec}s</span>}
      </div>
      <div style={{ fontSize: 12, color: MGMT.dimWhite, lineHeight: 1.6, fontFamily: MGMT.fontFamily, overflow: 'hidden', display: '-webkit-box', WebkitLineClamp: 4, WebkitBoxOrient: 'vertical' as const }}>
        {d.text}
      </div>
      {d.keywords && (
        <div style={{ marginTop: 8, display: 'flex', flexWrap: 'wrap', gap: 4 }}>
          {(d.keywords as string[]).slice(0, 4).map((kw: string, i: number) => (
            <span key={i} style={{ fontSize: 9, padding: '1px 6px', borderRadius: 3, background: `${MGMT.gold}15`, color: MGMT.gold, animation: `ap-slide 0.3s ease-out ${0.3 + i * 0.1}s both` }}>{kw}</span>
          ))}
        </div>
      )}
    </div>
  )
}

/** 🎨 视觉 — 描述 + 元素列表 */
const VisualPreview: React.FC<{ asset: Asset }> = ({ asset }) => {
  const key = useLoop(5000)
  const d = asset.content.data as any
  const typeIcon = ({ animation: '🎬', diagram: '📐', chart: '📊', screencast: '🖥️', illustration: '🖼️', photo: '📷' } as Record<string, string>)[d.visualType] || '🎨'
  return (
    <div key={key} style={{ padding: '12px 16px', animation: 'ap-fade 0.5s ease-out both' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 8 }}>
        <span style={{ fontSize: 18 }}>{typeIcon}</span>
        <span style={{ fontSize: 11, color: MGMT.green, fontWeight: 600 }}>{d.visualType}</span>
      </div>
      <div style={{ fontSize: 12, color: MGMT.dimWhite, lineHeight: 1.5, fontFamily: MGMT.fontFamily, overflow: 'hidden', display: '-webkit-box', WebkitLineClamp: 3, WebkitBoxOrient: 'vertical' as const }}>
        {d.description}
      </div>
      {d.elements && (
        <div style={{ marginTop: 6 }}>
          {(d.elements as string[]).slice(0, 3).map((el: string, i: number) => (
            <div key={i} style={{ fontSize: 10, color: MGMT.gray, marginBottom: 2, animation: `ap-slide 0.3s ease-out ${0.3 + i * 0.1}s both` }}>
              • {el}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

/** ✏️ 文字叠层 — 公式/代码/标题/要点 */
const TextOverlayPreview: React.FC<{ asset: Asset }> = ({ asset }) => {
  const key = useLoop(4000)
  const d = asset.content.data as any

  // 公式渲染
  if (d.overlayType === 'formula' && d.latex) {
    return (
      <div key={key} style={{ animation: 'ap-fade 0.5s ease-out both', textAlign: 'center', padding: 12 }}>
        <div style={{ fontSize: 22 }}>
          <BlockMath math={`\\color{${d.color || '#ffd700'}}{${d.latex}}`} />
        </div>
        {d.intuition && <div style={{ color: MGMT.dimWhite, fontSize: 11, marginTop: 4, fontFamily: MGMT.fontFamily }}>{d.intuition}</div>}
      </div>
    )
  }

  // 代码渲染
  if (d.overlayType === 'code') {
    return (
      <div key={key} style={{ padding: '10px 12px', animation: 'ap-fade 0.4s ease-out both' }}>
        {d.language && <div style={{ fontSize: 10, color: MGMT.blue, fontWeight: 600, marginBottom: 6 }}>{d.language}</div>}
        <pre style={{ fontSize: 10, color: '#e6edf3', fontFamily: MGMT.codeFontFamily, margin: 0, whiteSpace: 'pre-wrap', lineHeight: 1.5, background: '#0d1117', borderRadius: 6, padding: 8, overflow: 'hidden', maxHeight: 120 }}>
          {d.text}
        </pre>
      </div>
    )
  }

  // 要点/标题
  return (
    <div key={key} style={{ padding: '12px 16px', animation: 'ap-fade 0.5s ease-out both' }}>
      <div style={{ fontSize: 12, color: d.color || MGMT.gold, lineHeight: 1.6, fontFamily: MGMT.fontFamily, whiteSpace: 'pre-line' }}>
        {d.text}
      </div>
    </div>
  )
}

/** 🔊 音频 — 类型 + 描述 + 时长 */
const AudioPreview: React.FC<{ asset: Asset }> = ({ asset }) => {
  const key = useLoop(5000)
  const d = asset.content.data as any
  const typeIcon = ({ bgm: '🎵', sfx: '💥', alert: '🔔', ambient: '🌊' } as Record<string, string>)[d.audioType] || '🔊'
  return (
    <div key={key} style={{ padding: '14px 16px', animation: 'ap-fade 0.5s ease-out both', textAlign: 'center' }}>
      <div style={{ fontSize: 32, marginBottom: 8 }}>{typeIcon}</div>
      <div style={{ fontSize: 13, fontWeight: 600, color: MGMT.purple, marginBottom: 4 }}>{d.audioType}</div>
      <div style={{ fontSize: 11, color: MGMT.dimWhite }}>{d.description}</div>
      {d.durationSec && <div style={{ fontSize: 10, color: MGMT.gray, marginTop: 4 }}>⏱ {d.durationSec}s</div>}
    </div>
  )
}

/** 📊 数据 — 时间线/对比/表格 */
const DataPreview: React.FC<{ asset: Asset }> = ({ asset }) => {
  const key = useLoop(5000)
  const d = asset.content.data as any

  // 时间线事件
  if (d.events) {
    return (
      <div key={key} style={{ padding: '10px 14px', position: 'relative' }}>
        <div style={{ position: 'absolute', left: 22, top: 10, bottom: 10, width: 2, background: `linear-gradient(${MGMT.gold}60, #9b59b660)` }} />
        {(d.events as any[]).slice(0, 4).map((e: any, i: number) => (
          <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 6, paddingLeft: 6, animation: `ap-slide 0.3s ease-out ${0.2 + i * 0.3}s both` }}>
            <div style={{ width: 14, height: 14, borderRadius: '50%', background: e.color || MGMT.gold, flexShrink: 0, fontSize: 8, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>•</div>
            <span style={{ fontSize: 11, color: e.color || MGMT.gold, fontWeight: 600, fontFamily: MGMT.fontFamily, minWidth: 32 }}>{e.year}</span>
            <span style={{ fontSize: 11, color: MGMT.dimWhite, fontFamily: MGMT.fontFamily }}>{e.text}</span>
          </div>
        ))}
      </div>
    )
  }

  // 对比结构
  if (d.comparison) {
    const { left, right } = d.comparison
    return (
      <div key={key} style={{ display: 'flex', gap: 8, padding: '14px 12px' }}>
        {[left, right].map((col: any, ci: number) => (
          <div key={ci} style={{
            flex: 1, background: `${MGMT.white}04`, borderRadius: 8, padding: '10px 8px',
            borderTop: `2px solid ${col.color}`, textAlign: 'center',
            animation: `ap-slide 0.4s ease-out ${0.1 + ci * 0.2}s both`,
          }}>
            <div style={{ fontSize: 18, marginBottom: 2 }}>{col.icon || ''}</div>
            <div style={{ fontSize: 14, fontWeight: 700, color: col.color, fontFamily: MGMT.fontFamily }}>{col.value}</div>
            <div style={{ fontSize: 10, color: MGMT.dimWhite, fontFamily: MGMT.fontFamily }}>{col.label}</div>
          </div>
        ))}
      </div>
    )
  }

  return <FallbackPreview />
}

/** 📖 引用来源 */
const ReferencePreview: React.FC<{ asset: Asset }> = ({ asset }) => {
  const key = useLoop(6000)
  const d = asset.content.data as any
  return (
    <div key={key} style={{ padding: '14px 16px', animation: 'ap-fade 0.5s ease-out both' }}>
      <div style={{ fontSize: 14, fontWeight: 700, color: MGMT.red, marginBottom: 6 }}>📖 引用</div>
      <div style={{ fontSize: 12, color: MGMT.dimWhite, lineHeight: 1.5 }}>{d.citation}</div>
      {d.location && <div style={{ fontSize: 10, color: MGMT.gray, marginTop: 4 }}>📍 {d.location}</div>}
    </div>
  )
}

/** 🔄 转场衔接 */
const TransitionPreview: React.FC<{ asset: Asset }> = ({ asset }) => {
  const key = useLoop(5000)
  const d = asset.content.data as any
  return (
    <div key={key} style={{ padding: '14px 16px', animation: 'ap-fade 0.5s ease-out both', textAlign: 'center' }}>
      {d.chapterNum && (
        <div style={{ fontSize: 32, fontWeight: 800, color: '#1abc9c', marginBottom: 4, fontFamily: 'Inter, sans-serif' }}>
          {d.chapterNum}
        </div>
      )}
      {d.title && <div style={{ fontSize: 15, fontWeight: 700, color: '#1abc9c', marginBottom: 6, fontFamily: MGMT.fontFamily }}>{d.title}</div>}
      {d.content && <div style={{ fontSize: 11, color: MGMT.dimWhite }}>{d.content}</div>}
      {d.progress != null && (
        <div style={{ marginTop: 8, height: 4, borderRadius: 2, background: MGMT.border, overflow: 'hidden' }}>
          <div style={{ width: `${d.progress}%`, height: '100%', background: '#1abc9c', borderRadius: 2 }} />
        </div>
      )}
    </div>
  )
}

function FallbackPreview() {
  return (
    <div style={{ color: MGMT.grayLight, textAlign: 'center', padding: 20 }}>
      <div style={{ fontSize: 32, marginBottom: 4 }}>📦</div>
      <div style={{ fontSize: 11 }}>预览</div>
    </div>
  )
}

// ─────────── 预览路由 ───────────

const PREVIEW_MAP: Record<string, React.FC<{ asset: Asset }>> = {
  narration: NarrationPreview,
  visual: VisualPreview,
  text_overlay: TextOverlayPreview,
  audio: AudioPreview,
  data: DataPreview,
  reference: ReferencePreview,
  transition: TransitionPreview,
}

export function AssetPreview({ asset }: { asset: Asset }) {
  const Preview = PREVIEW_MAP[asset.category]
  if (!Preview) return <FallbackPreview />
  return <Preview asset={asset} />
}

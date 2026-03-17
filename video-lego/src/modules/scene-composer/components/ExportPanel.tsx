// ═══════════════════════════════════════════════════════════
// 场景编排器 — 导出面板
// Scene Composer — Export Panel & Code Generation
// ═══════════════════════════════════════════════════════════

import React, { useState, useCallback, useMemo } from 'react'
import { MGMT } from '@/theme'
import { IconUpload, IconCopy, IconX, IconReady } from '@/components/Icons'
import type { SceneData } from '@/lib/types'

function generateExport(scenes: SceneData[], meta: { course: string; topic: string; title: string }): string {
  const acts = new Map<string, string>()
  scenes.forEach(s => { if (s.act && !acts.has(s.act)) acts.set(s.act, `a${acts.size + 1}`) })
  const actsObj = [...acts.entries()].map(([l, k]) => `  ${k}: '${l}',`).join('\n')
  const v = meta.topic.toUpperCase().replace(/-/g, '_')
  const sc = scenes.map((s, i) => {
    const ar = acts.has(s.act) ? `ACTS.${acts.get(s.act)}` : `'${s.act}'`
    const vis = s.visuals.map(vv =>
      `      { block: '${vv.block}', data: ${JSON.stringify(vv.data, null, 6).replace(/\n/g, '\n        ')} }`
    ).join(',\n')
    return `    // 场景 ${String(i + 1).padStart(2, '0')}: ${s.title}\n    { layout: '${s.layout}', act: ${ar}, title: '${s.title.replace(/'/g, "\\'")}',\n      visuals: [\n${vis}\n      ],\n      points: [],\n    }`
  }).join(',\n\n')
  return `// ${meta.title}\n// 由场景编排器生成 ${new Date().toISOString()}\n\nimport type { VideoData } from '@lego/types';\n\nconst ACTS = {\n${actsObj}\n};\n\nexport const ${v}_VIDEO: VideoData = {\n  meta: { topic: '${meta.topic}', course: '${meta.course}', title: '${meta.title.replace(/'/g, "\\'")}', totalDurationSec: 0 },\n  narration: { audioFile: 'narration/${meta.topic}/full_narration.mp3', timestamps: [], subtitles: [] },\n  scenes: [\n${sc}\n  ],\n};\n`
}

export function ExportPanel({ scenes, meta, onClose }: {
  scenes: SceneData[]; meta: { course: string; topic: string; title: string }; onClose: () => void
}) {
  const code = useMemo(() => generateExport(scenes, meta), [scenes, meta])
  const [copied, setCopied] = useState(false)

  const handleCopy = useCallback(() => {
    navigator.clipboard.writeText(code).then(() => { setCopied(true); setTimeout(() => setCopied(false), 2000) })
  }, [code])

  return (
    <div style={{
      position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
      background: 'rgba(0,0,0,0.6)', display: 'flex',
      alignItems: 'center', justifyContent: 'center', zIndex: 1000,
    }} onClick={onClose}>
      <div onClick={e => e.stopPropagation()} style={{
        width: 720, maxHeight: '80vh', display: 'flex', flexDirection: 'column',
        overflow: 'hidden', borderRadius: 12, border: `1px solid ${MGMT.border}`,
        background: MGMT.bgCard, boxShadow: '0 20px 60px rgba(0,0,0,0.6)',
      }}>
        {/* 头部 */}
        <div style={{
          display: 'flex', alignItems: 'center', gap: 10,
          padding: '14px 20px', borderBottom: `1px solid ${MGMT.border}`,
        }}>
          <span style={{ flex: 1, display: 'flex', alignItems: 'center', gap: 6, fontSize: 15, fontWeight: 700, color: MGMT.gold }}>
            <IconUpload size={16} /> 导出代码
          </span>
          <button onClick={handleCopy} style={{
            background: copied ? `${MGMT.green}20` : `${MGMT.gold}14`,
            border: `1px solid ${copied ? `${MGMT.green}30` : `${MGMT.gold}30`}`,
            color: copied ? MGMT.green : MGMT.gold,
            borderRadius: 6, padding: '6px 16px', fontSize: 12, fontWeight: 600,
            cursor: 'pointer', fontFamily: MGMT.fontFamily, transition: 'all 0.2s',
          }}>
            {copied ? <><IconReady size={14} /> 已复制</> : <><IconCopy size={14} /> 复制</>}
          </button>
          <button onClick={onClose} style={{
            background: 'none', border: 'none', cursor: 'pointer',
            color: MGMT.grayLight, fontSize: 18,
          }}><IconX size={18} /></button>
        </div>

        {/* 代码区 */}
        <pre style={{
          flex: 1, overflow: 'auto', margin: 0, padding: 20,
          fontFamily: MGMT.codeFontFamily, fontSize: 11,
          color: MGMT.dimWhite, lineHeight: 1.6,
          whiteSpace: 'pre-wrap',
        }}>{code}</pre>

        {/* 底部统计 */}
        <div style={{
          borderTop: `1px solid ${MGMT.border}`, padding: '8px 20px',
          fontSize: 11, color: MGMT.grayLight,
        }}>
          {scenes.length} 个场景 · {scenes.reduce((s, sc) => s + sc.visuals.length, 0)} 个积木
        </div>
      </div>
    </div>
  )
}

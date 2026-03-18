// ═══════════════════════════════════════════════════════════
// 导数 Derivative — 切线斜率
// ═══════════════════════════════════════════════════════════

import React from 'react'
import 'katex/dist/katex.min.css'
import { BlockMath } from 'react-katex'
import { colStyle, dividerStyle, colLabelStyle, boardStyle, conclusionStyle } from './boardStyles'

const LATEX = String.raw`f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}`
const COLOR = '#e74c3c'

const animCSS = `
  @keyframes fadeIn { from { opacity: 0 } to { opacity: 1 } }
  @keyframes drawPath { from { stroke-dashoffset: 400 } to { stroke-dashoffset: 0 } }
  .dv-f1 { opacity: 0; animation: fadeIn 0.3s ease-out 0.2s forwards }
  .dv-f2 { opacity: 0; animation: fadeIn 0.3s ease-out 0.5s forwards }
  .dv-f3 { opacity: 0; animation: fadeIn 0.3s ease-out 0.8s forwards }
  .dv-curve { stroke-dasharray: 400; stroke-dashoffset: 400; animation: drawPath 0.8s ease-out 0.3s forwards }
`

const mapX = (v: number) => 20 + ((v + 1) / 5) * 180
const mapY = (v: number) => 130 - v * 25

export const DerivativeDiagram: React.FC<{ compact?: boolean }> = ({ compact }) => {
  if (compact) return (
    <div style={{ textAlign: 'center', padding: '6px' }}>
      <div style={{ fontSize: 14, color: COLOR }}><BlockMath math={LATEX} /></div>
      <div style={{ color: '#888', fontSize: 9 }}>切线斜率</div>
    </div>
  )

  // f(x) = x²
  const pts: string[] = []
  for (let x = -0.5; x <= 3.5; x += 0.1) pts.push(`${mapX(x).toFixed(1)},${mapY(x*x).toFixed(1)}`)

  return (
    <div style={{ padding: '8px 0' }}>
      <div style={{ padding: '4px 8px', display: 'flex', alignItems: 'center', gap: 8, background: 'rgba(255,255,255,0.02)', borderRadius: '8px 8px 0 0', border: '1px solid rgba(255,255,255,0.06)', borderBottom: 'none' }}>
        <span style={{ fontSize: 14, color: '#fff', fontWeight: 700, whiteSpace: 'nowrap' }}>导数</span>
        <div style={{ flex: 1, fontSize: 20, color: COLOR, textAlign: 'center' }}><BlockMath math={LATEX} /></div>
      </div>
      <div style={{ ...boardStyle, borderRadius: '0 0 8px 8px' }}>
        <div style={{ ...colStyle(1), minWidth: 150 }}>
          <div style={colLabelStyle}>解释</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
            <div>函数在某点的<b>瞬时变化率</b></div>
            <div style={{ marginTop: 6, color: '#aaa', fontSize: 11 }}>
              <div>• 几何意义: 切线的斜率</div>
              <div>• 物理意义: 速度</div>
              <div>• ML意义: 告诉你<b>往哪调参</b></div>
              <div>• 所有优化的数学基础</div>
            </div>
          </div>
        </div>
        <div style={dividerStyle} />
        <div style={{ ...colStyle(1), minWidth: 140 }}>
          <div style={colLabelStyle}>已知</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
            <div>例: f(x) = x²</div>
            <div style={{ marginTop: 6, color: '#aaa', fontSize: 11 }}>
              <div>f(2) = 4</div>
              <div>f(2.01) = 4.0401</div>
              <div style={{ marginTop: 4, color: '#FFD700' }}>求 f'(2) = ?</div>
            </div>
          </div>
        </div>
        <div style={dividerStyle} />
        <div style={{ ...colStyle(1.3), minWidth: 240 }}>
          <div style={colLabelStyle}>解题过程</div>
          <style>{animCSS}</style>
          <div style={{ fontSize: 11, color: '#aaa', lineHeight: 1.7, marginBottom: 4 }}>
            <div className="dv-f1">① Δy/Δx = (4.0401-4)/0.01 = 4.01</div>
            <div className="dv-f2">② h→0 时极限 = 2x</div>
            <div className="dv-f3" style={conclusionStyle}>
              <span style={{ color: '#FFD700', fontWeight: 700 }}>∴</span> f'(2) = 2×2 = <b>4</b>
            </div>
          </div>
          <svg width={220} height={140} viewBox="0 0 220 140" style={{ display: 'block' }}>
            <line x1={20} y1={130} x2={200} y2={130} stroke="#ffffff15" strokeWidth={1} />
            <line x1={20} y1={130} x2={20} y2={10} stroke="#ffffff15" strokeWidth={1} />
            <path d={`M ${pts.join(' L ')}`} className="dv-curve" fill="none" stroke={COLOR} strokeWidth={2} />
            {/* tangent at x=2 */}
            <line x1={mapX(1)} y1={mapY(4-(2-1)*4)} x2={mapX(3)} y2={mapY(4+(3-2)*4)} stroke="#FFD700" strokeWidth={1.5} className="dv-f3" />
            <circle cx={mapX(2)} cy={mapY(4)} r={3} fill="#FFD700" className="dv-f2" />
            <text x={mapX(2)+6} y={mapY(4)-4} fill="#FFD700" fontSize={9} className="dv-f2">(2,4)</text>
          </svg>
        </div>
      </div>
    </div>
  )
}

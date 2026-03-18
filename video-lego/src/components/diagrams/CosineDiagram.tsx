// ═══════════════════════════════════════════════════════════
// 余弦相似度 — 顶部公式 + 三栏: 解释 | 已知 | 解题过程
// ═══════════════════════════════════════════════════════════

import React from 'react'
import 'katex/dist/katex.min.css'
import { BlockMath, InlineMath } from 'react-katex'
import {
  colStyle, dividerStyle, colLabelStyle,
  boardStyle, conclusionStyle,
} from './boardStyles'

const LATEX = String.raw`\cos(\theta) = \frac{\vec{a} \cdot \vec{b}}{\|\vec{a}\| \|\vec{b}\|}`
const COLOR = '#e67e22'

const a = { x: 3, y: 2 }
const b = { x: 1, y: 3 }
const dotProd = a.x * b.x + a.y * b.y
const magA = Math.sqrt(a.x ** 2 + a.y ** 2)
const magB = Math.sqrt(b.x ** 2 + b.y ** 2)
const cosVal = dotProd / (magA * magB)
const thetaDeg = Math.acos(cosVal) * 180 / Math.PI

function arcPath(cx: number, cy: number, r: number, a1: number, a2: number) {
  const x1 = cx + r * Math.cos(-a1), y1 = cy + r * Math.sin(-a1)
  const x2 = cx + r * Math.cos(-a2), y2 = cy + r * Math.sin(-a2)
  return `M ${x1} ${y1} A ${r} ${r} 0 0 0 ${x2} ${y2}`
}

const mapSX = (v: number, w: number) => 30 + (v / 4.5) * (w - 60)
const mapSY = (v: number, h: number) => h - 30 - (v / 4.5) * (h - 60)

const animCSS = `
  @keyframes drawLine { from { stroke-dashoffset: 500 } to { stroke-dashoffset: 0 } }
  @keyframes fadeIn { from { opacity: 0 } to { opacity: 1 } }
  @keyframes arcDraw { from { stroke-dashoffset: 200 } to { stroke-dashoffset: 0 } }
  .cos-v1 { stroke-dasharray: 500; stroke-dashoffset: 500; animation: drawLine 0.5s ease-out 0.2s forwards }
  .cos-v2 { stroke-dasharray: 500; stroke-dashoffset: 500; animation: drawLine 0.5s ease-out 0.5s forwards }
  .cos-arc { stroke-dasharray: 200; stroke-dashoffset: 200; animation: arcDraw 0.4s ease-out 0.8s forwards }
  .cos-f1 { opacity: 0; animation: fadeIn 0.3s ease-out 0.4s forwards }
  .cos-f2 { opacity: 0; animation: fadeIn 0.3s ease-out 0.7s forwards }
  .cos-f3 { opacity: 0; animation: fadeIn 0.3s ease-out 1.0s forwards }
`

export const CosineDiagram: React.FC<{ compact?: boolean }> = ({ compact }) => {
  if (compact) {
    return (
      <div style={{ textAlign: 'center', padding: '6px' }}>
        <div style={{ fontSize: 14, color: COLOR }}><BlockMath math={LATEX} /></div>
        <div style={{ color: '#888', fontSize: 9 }}>方向是否一致</div>
      </div>
    )
  }

  const svgW = 200, svgH = 150
  const ox = mapSX(0, svgW), oy = mapSY(0, svgH)
  const ax2 = mapSX(a.x, svgW), ay2 = mapSY(a.y, svgH)
  const bx2 = mapSX(b.x, svgW), by2 = mapSY(b.y, svgH)
  const angleA = Math.atan2(a.y, a.x), angleB = Math.atan2(b.y, b.x)
  const arc = arcPath(ox, oy, 30, angleA, angleB)

  return (
    <div style={{ padding: '8px 0' }}>
      <div style={{
        padding: '4px 8px', display: 'flex', alignItems: 'center', gap: 8,
        background: 'rgba(255,255,255,0.02)', borderRadius: '8px 8px 0 0',
        border: '1px solid rgba(255,255,255,0.06)', borderBottom: 'none',
      }}>
        <span style={{ fontSize: 14, color: '#fff', fontWeight: 700, whiteSpace: 'nowrap' }}>余弦相似度</span>
        <div style={{ flex: 1, fontSize: 20, color: COLOR, textAlign: 'center' }}><BlockMath math={LATEX} /></div>
      </div>

      <div style={{ ...boardStyle, borderRadius: '0 0 8px 8px' }}>
        <div style={{ ...colStyle(1), minWidth: 150 }}>
          <div style={colLabelStyle}>解释</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
            <div>衡量两个向量<b>方向</b>的一致性</div>
            <div style={{ marginTop: 6, color: '#aaa', fontSize: 11 }}>
              <div>• 只看角度，忽略长度</div>
              <div>• 1 = 完全同向</div>
              <div>• 0 = 垂直/无关</div>
              <div>• -1 = 完全反向</div>
            </div>
            <div style={{ marginTop: 8, color: '#888', fontSize: 10 }}>
              文本相似、推荐系统常用
            </div>
          </div>
        </div>

        <div style={dividerStyle} />

        <div style={{ ...colStyle(1), minWidth: 140 }}>
          <div style={colLabelStyle}>已知</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
            <div style={{ color: '#FF862F' }}>
              <InlineMath math="\vec{a}" /> = ({a.x}, {a.y})
            </div>
            <div style={{ color: '#FFFF00' }}>
              <InlineMath math="\vec{b}" /> = ({b.x}, {b.y})
            </div>
            <div style={{ marginTop: 8, borderTop: '1px dashed rgba(255,255,255,0.1)', paddingTop: 6 }}>
              <span style={{ color: '#FFD700' }}>求</span>{' '}
              <InlineMath math="\cos(\theta)" /> = ?
            </div>
          </div>
        </div>

        <div style={dividerStyle} />

        <div style={{ ...colStyle(1.3), minWidth: 240 }}>
          <div style={colLabelStyle}>解题过程</div>
          <style>{animCSS}</style>

          <div style={{ fontSize: 11, color: '#aaa', lineHeight: 1.7, marginBottom: 4 }}>
            <div className="cos-f1">
              ① <InlineMath math={`\\vec{a}\\cdot\\vec{b} = ${a.x}\\times${b.x}+${a.y}\\times${b.y} = ${dotProd}`} />
            </div>
            <div className="cos-f2">
              ② <InlineMath math={`\\|\\vec{a}\\|=${magA.toFixed(2)},\\ \\|\\vec{b}\\|=${magB.toFixed(2)}`} />
            </div>
            <div className="cos-f3" style={conclusionStyle}>
              <span style={{ color: '#FFD700', fontWeight: 700 }}>∴</span>{' '}
              <InlineMath math={`\\cos\\theta = \\frac{${dotProd}}{${magA.toFixed(2)}\\times${magB.toFixed(2)}} = ${cosVal.toFixed(3)}`} />
              <div style={{ color: '#888', fontSize: 10 }}>θ ≈ {Math.round(thetaDeg)}° (方向较接近)</div>
            </div>
          </div>

          <svg width={svgW} height={svgH} viewBox={`0 0 ${svgW} ${svgH}`} style={{ display: 'block' }}>
            <defs>
              <marker id="cosArrA" markerWidth="7" markerHeight="5" refX="7" refY="2.5" orient="auto">
                <path d="M0,0 L7,2.5 L0,5" fill="#FF862F" />
              </marker>
              <marker id="cosArrB" markerWidth="7" markerHeight="5" refX="7" refY="2.5" orient="auto">
                <path d="M0,0 L7,2.5 L0,5" fill="#FFFF00" />
              </marker>
            </defs>
            <line x1={ox} y1={oy} x2={mapSX(4.5,svgW)} y2={oy} stroke="#ffffff15" strokeWidth={1} />
            <line x1={ox} y1={oy} x2={ox} y2={mapSY(4.5,svgH)} stroke="#ffffff15" strokeWidth={1} />
            <line x1={ox} y1={oy} x2={ax2} y2={ay2} className="cos-v1"
              stroke="#FF862F" strokeWidth={2.5} markerEnd="url(#cosArrA)" />
            <text x={ax2+6} y={ay2+14} className="cos-f1" fill="#FF862F" fontSize={10} fontWeight="bold">a</text>
            <line x1={ox} y1={oy} x2={bx2} y2={by2} className="cos-v2"
              stroke="#FFFF00" strokeWidth={2.5} markerEnd="url(#cosArrB)" />
            <text x={bx2-8} y={by2-6} className="cos-f2" fill="#FFFF00" fontSize={10} fontWeight="bold">b</text>
            <path d={arc} fill="none" stroke="#FFD700" strokeWidth={1.5} className="cos-arc" />
            <text x={ox + 28} y={oy - 22} className="cos-f3"
              fill="#FFD700" fontSize={11} fontWeight="bold">θ≈{Math.round(thetaDeg)}°</text>
          </svg>
        </div>
      </div>
    </div>
  )
}

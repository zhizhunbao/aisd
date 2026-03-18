// ═══════════════════════════════════════════════════════════
// 欧氏距离 — 顶部公式 + 三栏: 解释 | 已知 | 解题过程
// ═══════════════════════════════════════════════════════════

import React from 'react'
import 'katex/dist/katex.min.css'
import { BlockMath, InlineMath } from 'react-katex'
import {
  colStyle, dividerStyle, colLabelStyle,
  boardStyle, conclusionStyle,
} from './boardStyles'

const LATEX = String.raw`d(x,y) = \sqrt{\sum_{i=1}^{n}(x_i - y_i)^2}`
const COLOR = '#4ea8de'

const ptX = { x: 1, y: 1 }
const ptY = { x: 4, y: 5 }
const dx = ptY.x - ptX.x, dy = ptY.y - ptX.y
const dist = Math.sqrt(dx * dx + dy * dy)

const mapSX = (v: number, w: number) => 20 + (v / 6) * (w - 40)
const mapSY = (v: number, h: number) => h - 20 - (v / 6) * (h - 40)

const animCSS = `
  @keyframes drawLine { from { stroke-dashoffset: 500 } to { stroke-dashoffset: 0 } }
  @keyframes fadeIn { from { opacity: 0 } to { opacity: 1 } }
  @keyframes popIn { from { opacity: 0; transform: scale(0) } to { opacity: 1; transform: scale(1) } }
  .euc-draw { stroke-dasharray: 500; animation: drawLine 0.6s ease-out forwards }
  .euc-f1 { opacity: 0; animation: fadeIn 0.3s ease-out 0.3s forwards }
  .euc-f2 { opacity: 0; animation: fadeIn 0.3s ease-out 0.5s forwards }
  .euc-f3 { opacity: 0; animation: fadeIn 0.3s ease-out 0.8s forwards }
  .euc-pop { opacity: 0; transform-box: fill-box; transform-origin: center; animation: popIn 0.3s ease-out 0.2s forwards }
`

export const EuclideanDiagram: React.FC<{ compact?: boolean }> = ({ compact }) => {
  if (compact) {
    return (
      <div style={{ textAlign: 'center', padding: '6px' }}>
        <div style={{ fontSize: 14, color: COLOR }}><BlockMath math={LATEX} /></div>
        <div style={{ color: '#888', fontSize: 9 }}>两点直线距离</div>
      </div>
    )
  }

  const svgW = 220, svgH = 160
  const ax = mapSX(ptX.x, svgW), ay = mapSY(ptX.y, svgH)
  const bx = mapSX(ptY.x, svgW), by = mapSY(ptY.y, svgH)

  return (
    <div style={{ padding: '8px 0' }}>
      {/* 顶部: 名称 + 公式 */}
      <div style={{
        padding: '4px 8px', display: 'flex', alignItems: 'center', gap: 8,
        background: 'rgba(255,255,255,0.02)', borderRadius: '8px 8px 0 0',
        border: '1px solid rgba(255,255,255,0.06)', borderBottom: 'none',
      }}>
        <span style={{ fontSize: 14, color: '#fff', fontWeight: 700, whiteSpace: 'nowrap' }}>欧氏距离</span>
        <div style={{ flex: 1, fontSize: 20, color: COLOR, textAlign: 'center' }}><BlockMath math={LATEX} /></div>
      </div>

      <div style={{ ...boardStyle, borderRadius: '0 0 8px 8px' }}>
        {/* 左栏: 解释 */}
        <div style={{ ...colStyle(1), minWidth: 150 }}>
          <div style={colLabelStyle}>解释</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
            <div>两个点在空间中的<b>直线距离</b></div>
            <div style={{ marginTop: 6, color: '#aaa', fontSize: 11 }}>
              <div>• 勾股定理在 n 维的推广</div>
              <div>• L₂ 范数</div>
              <div>• d ≥ 0, 且 d=0 当 x=y</div>
              <div>• 满足三角不等式</div>
            </div>
          </div>
        </div>

        <div style={dividerStyle} />

        {/* 中栏: 已知 */}
        <div style={{ ...colStyle(1), minWidth: 140 }}>
          <div style={colLabelStyle}>已知</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
            <div>n = 2 (二维平面)</div>
            <div style={{ color: COLOR, marginTop: 4 }}>
              <InlineMath math="x" /> = ({ptX.x}, {ptX.y})
            </div>
            <div style={{ color: COLOR }}>
              <InlineMath math="y" /> = ({ptY.x}, {ptY.y})
            </div>
            <div style={{ marginTop: 8, borderTop: '1px dashed rgba(255,255,255,0.1)', paddingTop: 6 }}>
              <span style={{ color: '#FFD700' }}>求</span>{' '}
              <InlineMath math="d(x,y)" /> = ?
            </div>
          </div>
        </div>

        <div style={dividerStyle} />

        {/* 右栏: 解题过程 */}
        <div style={{ ...colStyle(1.3), minWidth: 240 }}>
          <div style={colLabelStyle}>解题过程</div>
          <style>{animCSS}</style>

          <div style={{ fontSize: 11, color: '#aaa', lineHeight: 1.7, marginBottom: 4 }}>
            <div className="euc-f1">
              ① <InlineMath math={`(x_1-y_1)^2 = (${ptX.x}-${ptY.x})^2 = ${dx*dx}`} />
            </div>
            <div className="euc-f2">
              ② <InlineMath math={`(x_2-y_2)^2 = (${ptX.y}-${ptY.y})^2 = ${dy*dy}`} />
            </div>
            <div className="euc-f3" style={conclusionStyle}>
              <span style={{ color: '#FFD700', fontWeight: 700 }}>∴</span>{' '}
              <InlineMath math={`d = \\sqrt{${dx*dx}+${dy*dy}} = ${dist.toFixed(2)}`} />
            </div>
          </div>

          <svg width={svgW} height={svgH} viewBox={`0 0 ${svgW} ${svgH}`} style={{ display: 'block' }}>
            {[0,1,2,3,4,5,6].map(i => (
              <React.Fragment key={i}>
                <line x1={mapSX(i,svgW)} y1={mapSY(0,svgH)} x2={mapSX(i,svgW)} y2={mapSY(6,svgH)} stroke="#ffffff08" strokeWidth={1} />
                <line x1={mapSX(0,svgW)} y1={mapSY(i,svgH)} x2={mapSX(6,svgW)} y2={mapSY(i,svgH)} stroke="#ffffff08" strokeWidth={1} />
              </React.Fragment>
            ))}
            <line x1={ax} y1={ay} x2={bx} y2={ay} className="euc-draw"
              stroke="#ff6b6b" strokeWidth={1.5} strokeDasharray="4 3" opacity={0.6} />
            <line x1={bx} y1={ay} x2={bx} y2={by} className="euc-draw"
              stroke="#4ecdc4" strokeWidth={1.5} strokeDasharray="4 3" opacity={0.6}
              style={{ animationDelay: '0.2s' }} />
            <polyline className="euc-f2" points={`${bx-6},${ay} ${bx-6},${ay-6} ${bx},${ay-6}`}
              fill="none" stroke="#ffffff30" strokeWidth={1} />
            <line x1={ax} y1={ay} x2={bx} y2={by} className="euc-draw"
              stroke={COLOR} strokeWidth={2.5} style={{ animationDelay: '0.4s' }} />
            <circle cx={ax} cy={ay} r={4} fill={COLOR} className="euc-pop" />
            <text x={ax-6} y={ay+14} fill={COLOR} fontSize={10} textAnchor="end">x</text>
            <circle cx={bx} cy={by} r={4} fill={COLOR} className="euc-pop" style={{ animationDelay: '0.3s' }} />
            <text x={bx+6} y={by-6} fill={COLOR} fontSize={10}>y</text>
            <text x={(ax+bx)/2-14} y={(ay+by)/2-6} className="euc-f3"
              fill="#FFD700" fontSize={14} fontWeight="bold" textAnchor="middle">
              d={dist.toFixed(2)}
            </text>
          </svg>
        </div>
      </div>
    </div>
  )
}

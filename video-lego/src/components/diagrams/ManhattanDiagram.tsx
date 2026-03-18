// ═══════════════════════════════════════════════════════════
// 曼哈顿距离 — 顶部公式 + 三栏: 解释 | 已知 | 解题过程
// ═══════════════════════════════════════════════════════════

import React from 'react'
import 'katex/dist/katex.min.css'
import { BlockMath, InlineMath } from 'react-katex'
import {
  colStyle, dividerStyle, colLabelStyle, givenLineStyle,
  boardStyle, conclusionStyle,
} from './boardStyles'

const LATEX = String.raw`d(x,y) = \sum_{i=1}^{n}|x_i - y_i|`
const COLOR = '#2ecc71'

const ptX = { x: 1, y: 1 }
const ptY = { x: 4, y: 5 }
const manhattan = Math.abs(ptY.x - ptX.x) + Math.abs(ptY.y - ptX.y)
const euclidean = Math.sqrt((ptY.x - ptX.x) ** 2 + (ptY.y - ptX.y) ** 2)

const mapSX = (v: number, w: number) => 20 + (v / 6) * (w - 40)
const mapSY = (v: number, h: number) => h - 20 - (v / 6) * (h - 40)

const animCSS = `
  @keyframes drawLine { from { stroke-dashoffset: 500 } to { stroke-dashoffset: 0 } }
  @keyframes fadeIn { from { opacity: 0 } to { opacity: 1 } }
  @keyframes popIn { from { opacity: 0; transform: scale(0) } to { opacity: 1; transform: scale(1) } }
  .mh-d1 { stroke-dasharray: 500; stroke-dashoffset: 500; animation: drawLine 0.5s ease-out 0.2s forwards }
  .mh-d2 { stroke-dasharray: 500; stroke-dashoffset: 500; animation: drawLine 0.5s ease-out 0.5s forwards }
  .mh-d3 { stroke-dasharray: 500; stroke-dashoffset: 500; animation: drawLine 0.5s ease-out 0.8s forwards }
  .mh-f1 { opacity: 0; animation: fadeIn 0.3s ease-out 0.3s forwards }
  .mh-f2 { opacity: 0; animation: fadeIn 0.3s ease-out 0.6s forwards }
  .mh-f3 { opacity: 0; animation: fadeIn 0.3s ease-out 1.0s forwards }
  .mh-pop { opacity: 0; transform-box: fill-box; transform-origin: center; animation: popIn 0.3s ease-out 0.1s forwards }
`

export const ManhattanDiagram: React.FC<{ compact?: boolean }> = ({ compact }) => {
  if (compact) {
    return (
      <div style={{ textAlign: 'center', padding: '6px' }}>
        <div style={{ fontSize: 14, color: COLOR }}><BlockMath math={LATEX} /></div>
        <div style={{ color: '#888', fontSize: 9 }}>沿网格线走的距离</div>
      </div>
    )
  }

  const svgW = 220, svgH = 160
  const ax = mapSX(ptX.x, svgW), ay = mapSY(ptX.y, svgH)
  const bx = mapSX(ptY.x, svgW), by = mapSY(ptY.y, svgH)
  const cx = mapSX(ptY.x, svgW), cy = mapSY(ptX.y, svgH)

  return (
    <div style={{ padding: '8px 0' }}>
      <div style={{
        padding: '4px 8px', display: 'flex', alignItems: 'center', gap: 8,
        background: 'rgba(255,255,255,0.02)', borderRadius: '8px 8px 0 0',
        border: '1px solid rgba(255,255,255,0.06)', borderBottom: 'none',
      }}>
        <span style={{ fontSize: 14, color: '#fff', fontWeight: 700, whiteSpace: 'nowrap' }}>曼哈顿距离</span>
        <div style={{ flex: 1, fontSize: 20, color: COLOR, textAlign: 'center' }}><BlockMath math={LATEX} /></div>
      </div>

      <div style={{ ...boardStyle, borderRadius: '0 0 8px 8px' }}>
        <div style={{ ...colStyle(1), minWidth: 150 }}>
          <div style={colLabelStyle}>解释</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
            <div>沿坐标轴方向的<b>路径总长度</b></div>
            <div style={{ marginTop: 6, color: '#aaa', fontSize: 11 }}>
              <div>• 只能走横/竖，不能斜着</div>
              <div>• 像出租车在网格城市行驶</div>
              <div>• L₁ 范数</div>
              <div>• 总是 ≥ 欧氏距离</div>
            </div>
          </div>
        </div>

        <div style={dividerStyle} />

        <div style={{ ...colStyle(1), minWidth: 140 }}>
          <div style={colLabelStyle}>已知</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
            <div>n = 2</div>
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

        <div style={{ ...colStyle(1.3), minWidth: 240 }}>
          <div style={colLabelStyle}>解题过程</div>
          <style>{animCSS}</style>

          <div style={{ fontSize: 11, color: '#aaa', lineHeight: 1.7, marginBottom: 4 }}>
            <div className="mh-f1">
              ① <InlineMath math={`|x_1-y_1| = |${ptX.x}-${ptY.x}| = ${Math.abs(ptY.x-ptX.x)}`} />
            </div>
            <div className="mh-f2">
              ② <InlineMath math={`|x_2-y_2| = |${ptX.y}-${ptY.y}| = ${Math.abs(ptY.y-ptX.y)}`} />
            </div>
            <div className="mh-f3" style={conclusionStyle}>
              <span style={{ color: '#FFD700', fontWeight: 700 }}>∴</span>{' '}
              <InlineMath math={`d = ${Math.abs(ptY.x-ptX.x)}+${Math.abs(ptY.y-ptX.y)} = ${manhattan}`} />
              <span style={{ color: '#888', fontSize: 10, marginLeft: 6 }}>(L₂={euclidean.toFixed(1)})</span>
            </div>
          </div>

          <svg width={svgW} height={svgH} viewBox={`0 0 ${svgW} ${svgH}`} style={{ display: 'block' }}>
            {[0,1,2,3,4,5,6].map(i => (
              <React.Fragment key={i}>
                <line x1={mapSX(i,svgW)} y1={mapSY(0,svgH)} x2={mapSX(i,svgW)} y2={mapSY(6,svgH)} stroke="#ffffff08" strokeWidth={1} />
                <line x1={mapSX(0,svgW)} y1={mapSY(i,svgH)} x2={mapSX(6,svgW)} y2={mapSY(i,svgH)} stroke="#ffffff08" strokeWidth={1} />
              </React.Fragment>
            ))}
            <line x1={ax} y1={ay} x2={bx} y2={by} className="mh-d3"
              stroke="#666" strokeWidth={1.5} strokeDasharray="5 3" opacity={0.4} />
            <line x1={ax} y1={ay} x2={cx} y2={cy} className="mh-d1"
              stroke={COLOR} strokeWidth={3} strokeLinecap="round" />
            <line x1={cx} y1={cy} x2={bx} y2={by} className="mh-d2"
              stroke={COLOR} strokeWidth={3} strokeLinecap="round" />
            <circle cx={ax} cy={ay} r={4} fill={COLOR} className="mh-pop" />
            <text x={ax-6} y={ay+14} fill={COLOR} fontSize={10} textAnchor="end">x</text>
            <circle cx={bx} cy={by} r={4} fill={COLOR} className="mh-pop" />
            <text x={bx+6} y={by-6} fill={COLOR} fontSize={10}>y</text>
            <text x={(ax+cx)/2} y={ay+14} className="mh-f1" fill={COLOR} fontSize={9} textAnchor="middle">3</text>
            <text x={bx+6} y={(cy+by)/2} className="mh-f2" fill={COLOR} fontSize={9}>4</text>
            <text x={svgW/2} y={14} className="mh-f3" fill="#FFD700" fontSize={13} fontWeight="bold" textAnchor="middle">
              d = {manhattan}
            </text>
          </svg>
        </div>
      </div>
    </div>
  )
}

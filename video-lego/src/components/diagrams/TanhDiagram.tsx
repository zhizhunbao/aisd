// ═══════════════════════════════════════════════════════════
// Tanh — 顶部公式 + 三栏: 解释 | 已知 | 解题过程
// ═══════════════════════════════════════════════════════════

import React from 'react'
import 'katex/dist/katex.min.css'
import { BlockMath } from 'react-katex'
import { colStyle, dividerStyle, colLabelStyle, boardStyle, conclusionStyle } from './boardStyles'

const LATEX = String.raw`\tanh(x) = \frac{e^x - e^{-x}}{e^x + e^{-x}}`
const COLOR = '#f39c12'
const tanh = (x: number) => (Math.exp(x) - Math.exp(-x)) / (Math.exp(x) + Math.exp(-x))
const mapX = (v: number) => 30 + ((v + 4) / 8) * 170
const mapY = (v: number) => 75 - v * 55

const animCSS = `
  @keyframes fadeIn { from { opacity: 0 } to { opacity: 1 } }
  @keyframes drawPath { from { stroke-dashoffset: 400 } to { stroke-dashoffset: 0 } }
  .th-f1 { opacity: 0; animation: fadeIn 0.3s ease-out 0.2s forwards }
  .th-f2 { opacity: 0; animation: fadeIn 0.3s ease-out 0.5s forwards }
  .th-f3 { opacity: 0; animation: fadeIn 0.3s ease-out 0.8s forwards }
  .th-curve { stroke-dasharray: 400; stroke-dashoffset: 400; animation: drawPath 0.8s ease-out 0.3s forwards }
`

export const TanhDiagram: React.FC<{ compact?: boolean }> = ({ compact }) => {
  if (compact) return (
    <div style={{ textAlign: 'center', padding: '6px' }}>
      <div style={{ fontSize: 14, color: COLOR }}><BlockMath math={LATEX} /></div>
      <div style={{ color: '#888', fontSize: 9 }}>输出(-1,1)</div>
    </div>
  )

  const pts: string[] = []
  for (let x = -4; x <= 4; x += 0.2) pts.push(`${mapX(x).toFixed(1)},${mapY(tanh(x)).toFixed(1)}`)

  return (
    <div style={{ padding: '8px 0' }}>
      <div style={{ padding: '4px 8px', display: 'flex', alignItems: 'center', gap: 8, background: 'rgba(255,255,255,0.02)', borderRadius: '8px 8px 0 0', border: '1px solid rgba(255,255,255,0.06)', borderBottom: 'none' }}>
        <span style={{ fontSize: 14, color: '#fff', fontWeight: 700, whiteSpace: 'nowrap' }}>Tanh 函数</span>
        <div style={{ flex: 1, fontSize: 20, color: COLOR, textAlign: 'center' }}><BlockMath math={LATEX} /></div>
      </div>
      <div style={{ ...boardStyle, borderRadius: '0 0 8px 8px' }}>
        <div style={{ ...colStyle(1), minWidth: 150 }}>
          <div style={colLabelStyle}>解释</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
            <div>将<b>任意实数</b>压缩到 <b>(-1, 1)</b> 区间</div>
            <div style={{ marginTop: 6, color: '#aaa', fontSize: 11 }}>
              <div>• 关于原点对称（奇函数）</div>
              <div>• x = 0 → tanh = 0</div>
              <div>• 比 Sigmoid 中心化更好</div>
              <div>• RNN/LSTM 常用</div>
            </div>
          </div>
        </div>
        <div style={dividerStyle} />
        <div style={{ ...colStyle(1), minWidth: 140 }}>
          <div style={colLabelStyle}>已知</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
            {[{x: -2, c: '#888'}, {x: 0, c: '#FFD700'}, {x: 2, c: COLOR}].map(({ x, c }) => (
              <div key={x} style={{ color: c, fontSize: 11 }}>x = {x} → tanh = {tanh(x).toFixed(3)}</div>
            ))}
            <div style={{ marginTop: 8, color: '#888', fontSize: 10 }}>tanh(x) = 2σ(2x) - 1</div>
          </div>
        </div>
        <div style={dividerStyle} />
        <div style={{ ...colStyle(1.3), minWidth: 240 }}>
          <div style={colLabelStyle}>解题过程</div>
          <style>{animCSS}</style>
          <div style={{ fontSize: 11, color: '#aaa', lineHeight: 1.7, marginBottom: 4 }}>
            <div className="th-f1">① 分子 = eˣ - e⁻ˣ, 分母 = eˣ + e⁻ˣ</div>
            <div className="th-f2">② x=0 → (1-1)/(1+1) = 0</div>
            <div className="th-f3" style={conclusionStyle}>
              <span style={{ color: '#FFD700', fontWeight: 700 }}>∴</span> S 形曲线，过原点
            </div>
          </div>
          <svg width={220} height={150} viewBox="0 0 220 150" style={{ display: 'block' }}>
            <line x1={30} y1={75} x2={210} y2={75} stroke="#ffffff15" strokeWidth={1} />
            <line x1={mapX(0)} y1={10} x2={mapX(0)} y2={140} stroke="#ffffff15" strokeWidth={1} />
            <line x1={30} y1={mapY(1)} x2={210} y2={mapY(1)} stroke="#ffffff08" strokeWidth={1} strokeDasharray="3 3" />
            <line x1={30} y1={mapY(-1)} x2={210} y2={mapY(-1)} stroke="#ffffff08" strokeWidth={1} strokeDasharray="3 3" />
            <text x={12} y={mapY(1) + 3} fill="#888" fontSize={8}>1</text>
            <text x={8} y={mapY(-1) + 3} fill="#888" fontSize={8}>-1</text>
            <path d={`M ${pts.join(' L ')}`} className="th-curve" fill="none" stroke={COLOR} strokeWidth={2.5} />
            <circle cx={mapX(0)} cy={mapY(0)} r={3} fill="#FFD700" className="th-f2" />
          </svg>
        </div>
      </div>
    </div>
  )
}

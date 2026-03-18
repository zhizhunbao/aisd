// ═══════════════════════════════════════════════════════════
// 高斯分布 Gaussian — 钟形曲线
// ═══════════════════════════════════════════════════════════

import React from 'react'
import 'katex/dist/katex.min.css'
import { BlockMath } from 'react-katex'
import { colStyle, dividerStyle, colLabelStyle, boardStyle, conclusionStyle } from './boardStyles'

const LATEX = String.raw`f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}`
const COLOR = '#9b59b6'
const gaussian = (x: number, mu: number, sigma: number) =>
  (1 / (sigma * Math.sqrt(2 * Math.PI))) * Math.exp(-((x - mu) ** 2) / (2 * sigma ** 2))
const mapX = (v: number) => 20 + ((v + 4) / 8) * 180
const mapY = (v: number) => 130 - v * 280

const animCSS = `
  @keyframes fadeIn { from { opacity: 0 } to { opacity: 1 } }
  @keyframes drawPath { from { stroke-dashoffset: 400 } to { stroke-dashoffset: 0 } }
  .gs-f1 { opacity: 0; animation: fadeIn 0.3s ease-out 0.2s forwards }
  .gs-f2 { opacity: 0; animation: fadeIn 0.3s ease-out 0.5s forwards }
  .gs-f3 { opacity: 0; animation: fadeIn 0.3s ease-out 0.8s forwards }
  .gs-curve { stroke-dasharray: 400; stroke-dashoffset: 400; animation: drawPath 0.8s ease-out 0.3s forwards }
`

export const GaussianDiagram: React.FC<{ compact?: boolean }> = ({ compact }) => {
  if (compact) return (
    <div style={{ textAlign: 'center', padding: '6px' }}>
      <div style={{ fontSize: 14, color: COLOR }}><BlockMath math={LATEX} /></div>
      <div style={{ color: '#888', fontSize: 9 }}>钟形曲线</div>
    </div>
  )
  const pts: string[] = []
  for (let x = -4; x <= 4; x += 0.15) pts.push(`${mapX(x).toFixed(1)},${mapY(gaussian(x, 0, 1)).toFixed(1)}`)

  return (
    <div style={{ padding: '8px 0' }}>
      <div style={{ padding: '4px 8px', display: 'flex', alignItems: 'center', gap: 8, background: 'rgba(255,255,255,0.02)', borderRadius: '8px 8px 0 0', border: '1px solid rgba(255,255,255,0.06)', borderBottom: 'none' }}>
        <span style={{ fontSize: 14, color: '#fff', fontWeight: 700, whiteSpace: 'nowrap' }}>高斯分布</span>
        <div style={{ flex: 1, fontSize: 18, color: COLOR, textAlign: 'center' }}><BlockMath math={LATEX} /></div>
      </div>
      <div style={{ ...boardStyle, borderRadius: '0 0 8px 8px' }}>
        <div style={{ ...colStyle(1), minWidth: 150 }}>
          <div style={colLabelStyle}>解释</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
            <div><b>正态分布</b>/钟形曲线</div>
            <div style={{ marginTop: 6, color: '#aaa', fontSize: 11 }}>
              <div>• μ = 均值 (峰值位置)</div>
              <div>• σ = 标准差 (胖/瘦)</div>
              <div>• 68% 数据在 μ±σ 内</div>
              <div>• 自然界最常见的分布</div>
            </div>
          </div>
        </div>
        <div style={dividerStyle} />
        <div style={{ ...colStyle(1), minWidth: 140 }}>
          <div style={colLabelStyle}>已知</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
            <div>μ = 0, σ = 1 (标准正态)</div>
            <div style={{ marginTop: 6, color: '#aaa', fontSize: 11 }}>
              <div>f(0) = {gaussian(0,0,1).toFixed(3)} (峰值)</div>
              <div>f(1) = {gaussian(1,0,1).toFixed(3)}</div>
              <div>f(2) = {gaussian(2,0,1).toFixed(3)}</div>
            </div>
          </div>
        </div>
        <div style={dividerStyle} />
        <div style={{ ...colStyle(1.3), minWidth: 240 }}>
          <div style={colLabelStyle}>解题过程</div>
          <style>{animCSS}</style>
          <div style={{ fontSize: 11, color: '#aaa', lineHeight: 1.7, marginBottom: 4 }}>
            <div className="gs-f1">① 指数部分决定曲线形状</div>
            <div className="gs-f2">② 前面系数保证面积=1</div>
            <div className="gs-f3" style={conclusionStyle}>
              <span style={{ color: '#FFD700', fontWeight: 700 }}>∴</span> 对称钟形，面积为1
            </div>
          </div>
          <svg width={220} height={150} viewBox="0 0 220 150" style={{ display: 'block' }}>
            <line x1={20} y1={135} x2={200} y2={135} stroke="#ffffff15" strokeWidth={1} />
            <line x1={mapX(0)} y1={10} x2={mapX(0)} y2={140} stroke="#ffffff08" strokeWidth={1} strokeDasharray="3 3" />
            <path d={`M ${pts.join(' L ')}`} className="gs-curve" fill="none" stroke={COLOR} strokeWidth={2.5} />
            <text x={mapX(0)-4} y={145} fill="#888" fontSize={8}>μ</text>
            <text x={mapX(1)-4} y={145} fill="#888" fontSize={8}>σ</text>
            <text x={mapX(-1)-6} y={145} fill="#888" fontSize={8}>-σ</text>
            <circle cx={mapX(0)} cy={mapY(gaussian(0,0,1))} r={3} fill="#FFD700" className="gs-f2" />
          </svg>
        </div>
      </div>
    </div>
  )
}

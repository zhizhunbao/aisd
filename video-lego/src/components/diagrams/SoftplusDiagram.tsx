// ═══════════════════════════════════════════════════════════
// Softplus — 顶部公式 + 三栏: 解释 | 已知 | 解题过程
// ═══════════════════════════════════════════════════════════

import React from 'react'
import 'katex/dist/katex.min.css'
import { BlockMath } from 'react-katex'
import { colStyle, dividerStyle, colLabelStyle, boardStyle, conclusionStyle } from './boardStyles'

const LATEX = String.raw`\zeta(x) = \log(1 + e^x)`
const COLOR = '#27ae60'

const softplus = (x: number) => Math.log(1 + Math.exp(x))
const relu = (x: number) => Math.max(0, x)

const animCSS = `
  @keyframes fadeIn { from { opacity: 0 } to { opacity: 1 } }
  @keyframes drawPath { from { stroke-dashoffset: 400 } to { stroke-dashoffset: 0 } }
  .sp-f1 { opacity: 0; animation: fadeIn 0.3s ease-out 0.2s forwards }
  .sp-f2 { opacity: 0; animation: fadeIn 0.3s ease-out 0.5s forwards }
  .sp-f3 { opacity: 0; animation: fadeIn 0.3s ease-out 0.8s forwards }
  .sp-curve { stroke-dasharray: 400; stroke-dashoffset: 400; animation: drawPath 0.8s ease-out 0.3s forwards }
  .sp-relu { stroke-dasharray: 400; stroke-dashoffset: 400; animation: drawPath 0.8s ease-out 0.1s forwards }
`

const mapX = (v: number) => 30 + ((v + 5) / 10) * 170
const mapY = (v: number) => 125 - v * 18

export const SoftplusDiagram: React.FC<{ compact?: boolean }> = ({ compact }) => {
  if (compact) {
    return (
      <div style={{ textAlign: 'center', padding: '6px' }}>
        <div style={{ fontSize: 14, color: COLOR }}><BlockMath math={LATEX} /></div>
        <div style={{ color: '#888', fontSize: 9 }}>ReLU 的平滑版</div>
      </div>
    )
  }

  // Softplus 曲线
  const spPts: string[] = []
  const reluPts: string[] = []
  for (let x = -5; x <= 5; x += 0.2) {
    spPts.push(`${mapX(x).toFixed(1)},${mapY(softplus(x)).toFixed(1)}`)
    reluPts.push(`${mapX(x).toFixed(1)},${mapY(relu(x)).toFixed(1)}`)
  }

  return (
    <div style={{ padding: '8px 0' }}>
      <div style={{
        padding: '4px 8px', display: 'flex', alignItems: 'center', gap: 8,
        background: 'rgba(255,255,255,0.02)', borderRadius: '8px 8px 0 0',
        border: '1px solid rgba(255,255,255,0.06)', borderBottom: 'none',
      }}>
        <span style={{ fontSize: 14, color: '#fff', fontWeight: 700, whiteSpace: 'nowrap' }}>Softplus</span>
        <div style={{ flex: 1, fontSize: 20, color: COLOR, textAlign: 'center' }}><BlockMath math={LATEX} /></div>
      </div>

      <div style={{ ...boardStyle, borderRadius: '0 0 8px 8px' }}>
        <div style={{ ...colStyle(1), minWidth: 150 }}>
          <div style={colLabelStyle}>解释</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
            <div><b>ReLU 的平滑近似</b></div>
            <div style={{ marginTop: 6, color: '#aaa', fontSize: 11 }}>
              <div>• 输出恒为正 ({'>'}0)</div>
              <div>• 处处可微 (无折点)</div>
              <div>• x→∞ 时接近 ReLU</div>
              <div>• VAE 中参数化方差</div>
            </div>
            <div style={{ marginTop: 8, color: '#888', fontSize: 10 }}>
              ζ'(x) = σ(x) (导数就是 Sigmoid!)
            </div>
          </div>
        </div>

        <div style={dividerStyle} />

        <div style={{ ...colStyle(1), minWidth: 140 }}>
          <div style={colLabelStyle}>已知</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
            <div>取几个典型值:</div>
            {[{ x: -3, c: '#666' }, { x: 0, c: '#FFD700' }, { x: 3, c: COLOR }].map(({ x, c }) => (
              <div key={x} style={{ color: c, fontSize: 11 }}>
                x={x} → ζ={softplus(x).toFixed(3)}
              </div>
            ))}
            <div style={{ marginTop: 6 }}>
              对比: ReLU(0) = 0, ζ(0) = <b style={{ color: '#FFD700' }}>0.693</b>
            </div>
            <div style={{ marginTop: 6, borderTop: '1px dashed rgba(255,255,255,0.1)', paddingTop: 4 }}>
              <span style={{ color: '#FFD700' }}>求</span> Softplus vs ReLU 对比图
            </div>
          </div>
        </div>

        <div style={dividerStyle} />

        <div style={{ ...colStyle(1.3), minWidth: 240 }}>
          <div style={colLabelStyle}>解题过程</div>
          <style>{animCSS}</style>

          <div style={{ fontSize: 11, color: '#aaa', lineHeight: 1.7, marginBottom: 4 }}>
            <div className="sp-f1">① x≪0 → e<sup>x</sup>≈0 → log(1)=<b style={{ color: '#666' }}>0</b></div>
            <div className="sp-f2">② x≫0 → log(e<sup>x</sup>)=<b style={{ color: COLOR }}>x</b> (≈ReLU)</div>
            <div className="sp-f3" style={conclusionStyle}>
              <span style={{ color: '#FFD700', fontWeight: 700 }}>∴</span> 平滑版 ReLU，原点附近圆滑过渡
            </div>
          </div>

          <svg width={220} height={140} viewBox="0 0 220 140" style={{ display: 'block' }}>
            {/* 坐标轴 */}
            <line x1={20} y1={mapY(0)} x2={210} y2={mapY(0)} stroke="#ffffff15" strokeWidth={1} />
            <line x1={mapX(0)} y1={10} x2={mapX(0)} y2={135} stroke="#ffffff15" strokeWidth={1} />
            {/* ReLU (虚线) */}
            <polyline points={reluPts.join(' ')} fill="none" stroke="#e74c3c40" strokeWidth={2} strokeDasharray="4 3" className="sp-relu" />
            <text x={mapX(3.5)} y={mapY(relu(3.5)) - 4} fill="#e74c3c60" fontSize={8} className="sp-f2">ReLU</text>
            {/* Softplus (实线) */}
            <polyline points={spPts.join(' ')} fill="none" stroke={COLOR} strokeWidth={2.5} className="sp-curve" />
            <text x={mapX(3)} y={mapY(softplus(3)) + 14} fill={COLOR} fontSize={9} className="sp-f2">Softplus</text>
            {/* 关键点 */}
            <circle cx={mapX(0)} cy={mapY(softplus(0))} r={3} fill="#FFD700" className="sp-f1" />
            <text x={mapX(0) + 5} y={mapY(softplus(0)) - 5} fill="#FFD700" fontSize={8} className="sp-f1">ln2≈0.69</text>
          </svg>
        </div>
      </div>
    </div>
  )
}

// ═══════════════════════════════════════════════════════════
// Sigmoid — 顶部公式 + 三栏: 解释 | 已知 | 解题过程
// ═══════════════════════════════════════════════════════════

import React from 'react'
import 'katex/dist/katex.min.css'
import { BlockMath, InlineMath } from 'react-katex'
import { colStyle, dividerStyle, colLabelStyle, boardStyle, conclusionStyle } from './boardStyles'

const LATEX = String.raw`\sigma(x) = \frac{1}{1 + e^{-x}}`
const COLOR = '#3498db'

const xs = [-3, -2, -1, 0, 1, 2, 3]
const sigmoid = (x: number) => 1 / (1 + Math.exp(-x))
const vals = xs.map(x => ({ x, y: sigmoid(x) }))

const animCSS = `
  @keyframes fadeIn { from { opacity: 0 } to { opacity: 1 } }
  @keyframes drawPath { from { stroke-dashoffset: 400 } to { stroke-dashoffset: 0 } }
  .sig-f1 { opacity: 0; animation: fadeIn 0.3s ease-out 0.2s forwards }
  .sig-f2 { opacity: 0; animation: fadeIn 0.3s ease-out 0.5s forwards }
  .sig-f3 { opacity: 0; animation: fadeIn 0.3s ease-out 0.8s forwards }
  .sig-curve { stroke-dasharray: 400; stroke-dashoffset: 400; animation: drawPath 0.8s ease-out 0.3s forwards }
`

const mapX = (v: number) => 30 + ((v + 4) / 8) * 170
const mapY = (v: number) => 130 - v * 110

export const SigmoidDiagram: React.FC<{ compact?: boolean }> = ({ compact }) => {
  if (compact) {
    return (
      <div style={{ textAlign: 'center', padding: '6px' }}>
        <div style={{ fontSize: 14, color: COLOR }}><BlockMath math={LATEX} /></div>
        <div style={{ color: '#888', fontSize: 9 }}>实数→(0,1)</div>
      </div>
    )
  }

  // 生成 S 曲线路径
  const points: string[] = []
  for (let x = -4; x <= 4; x += 0.2) {
    points.push(`${mapX(x).toFixed(1)},${mapY(sigmoid(x)).toFixed(1)}`)
  }
  const curvePath = `M ${points.join(' L ')}`

  return (
    <div style={{ padding: '8px 0' }}>
      <div style={{
        padding: '4px 8px', display: 'flex', alignItems: 'center', gap: 8,
        background: 'rgba(255,255,255,0.02)', borderRadius: '8px 8px 0 0',
        border: '1px solid rgba(255,255,255,0.06)', borderBottom: 'none',
      }}>
        <span style={{ fontSize: 14, color: '#fff', fontWeight: 700, whiteSpace: 'nowrap' }}>Sigmoid 函数</span>
        <div style={{ flex: 1, fontSize: 20, color: COLOR, textAlign: 'center' }}><BlockMath math={LATEX} /></div>
      </div>

      <div style={{ ...boardStyle, borderRadius: '0 0 8px 8px' }}>
        <div style={{ ...colStyle(1), minWidth: 150 }}>
          <div style={colLabelStyle}>解释</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
            <div>将<b>任意实数</b>压缩到 <b>(0, 1)</b> 区间</div>
            <div style={{ marginTop: 6, color: '#aaa', fontSize: 11 }}>
              <div>• x 很大 → 接近 1</div>
              <div>• x = 0 → 正好 0.5</div>
              <div>• x 很小 → 接近 0</div>
              <div>• 输出可解释为"概率"</div>
            </div>
            <div style={{ marginTop: 8, color: '#888', fontSize: 10 }}>
              二分类问题的标准输出函数
            </div>
          </div>
        </div>

        <div style={dividerStyle} />

        <div style={{ ...colStyle(1), minWidth: 140 }}>
          <div style={colLabelStyle}>已知</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
            <div>x 为模型输出值</div>
            <div style={{ marginTop: 4 }}>取几个典型值:</div>
            {[{x: -2, c: '#888'}, {x: 0, c: '#FFD700'}, {x: 2, c: COLOR}].map(({ x, c }) => (
              <div key={x} style={{ color: c, fontSize: 11 }}>
                x = {x} → σ = {sigmoid(x).toFixed(3)}
              </div>
            ))}
            <div style={{ marginTop: 8, borderTop: '1px dashed rgba(255,255,255,0.1)', paddingTop: 6 }}>
              <span style={{ color: '#FFD700' }}>求</span> S 形曲线图
            </div>
          </div>
        </div>

        <div style={dividerStyle} />

        <div style={{ ...colStyle(1.3), minWidth: 240 }}>
          <div style={colLabelStyle}>解题过程</div>
          <style>{animCSS}</style>

          <div style={{ fontSize: 11, color: '#aaa', lineHeight: 1.7, marginBottom: 4 }}>
            <div className="sig-f1">① 分母 = 1 + e<sup>-x</sup>, 分子 = 1</div>
            <div className="sig-f2">② x=0 → 1/(1+1) = 0.5 (中心点)</div>
            <div className="sig-f3" style={conclusionStyle}>
              <span style={{ color: '#FFD700', fontWeight: 700 }}>∴</span> 单调递增的 S 形曲线
            </div>
          </div>

          <svg width={220} height={150} viewBox="0 0 220 150" style={{ display: 'block' }}>
            {/* 坐标轴 */}
            <line x1={30} y1={mapY(0)} x2={210} y2={mapY(0)} stroke="#ffffff15" strokeWidth={1} />
            <line x1={mapX(0)} y1={10} x2={mapX(0)} y2={140} stroke="#ffffff15" strokeWidth={1} />
            {/* y=0.5 参考线 */}
            <line x1={30} y1={mapY(0.5)} x2={210} y2={mapY(0.5)} stroke="#ffffff08" strokeWidth={1} strokeDasharray="3 3" />
            <text x={12} y={mapY(0.5) + 3} fill="#888" fontSize={8}>0.5</text>
            <text x={12} y={mapY(1) + 3} fill="#888" fontSize={8}>1</text>
            <text x={12} y={mapY(0) + 3} fill="#888" fontSize={8}>0</text>
            {/* S 曲线 */}
            <path d={curvePath} className="sig-curve" fill="none" stroke={COLOR} strokeWidth={2.5} />
            {/* 标注点 */}
            <circle cx={mapX(0)} cy={mapY(0.5)} r={3} fill="#FFD700" className="sig-f2" />
            <text x={mapX(0) + 5} y={mapY(0.5) - 5} className="sig-f2" fill="#FFD700" fontSize={9}>(0, 0.5)</text>
          </svg>
        </div>
      </div>
    </div>
  )
}

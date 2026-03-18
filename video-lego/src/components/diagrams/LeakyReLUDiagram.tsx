// ═══════════════════════════════════════════════════════════
// Leaky ReLU — 顶部公式 + 三栏: 解释 | 已知 | 解题过程
// ═══════════════════════════════════════════════════════════

import React from 'react'
import 'katex/dist/katex.min.css'
import { BlockMath } from 'react-katex'
import { colStyle, dividerStyle, colLabelStyle, boardStyle, conclusionStyle } from './boardStyles'

const LATEX = String.raw`f(x) = \begin{cases} x & x > 0 \\ \alpha x & x \leq 0 \end{cases}`
const COLOR = '#e74c3c'
const ALPHA = 0.2  // 用较大 α 方便可视化

const animCSS = `
  @keyframes drawLine { from { stroke-dashoffset: 300 } to { stroke-dashoffset: 0 } }
  @keyframes fadeIn { from { opacity: 0 } to { opacity: 1 } }
  .lrelu-d1 { stroke-dasharray: 300; stroke-dashoffset: 300; animation: drawLine 0.4s ease-out 0.2s forwards }
  .lrelu-d2 { stroke-dasharray: 300; stroke-dashoffset: 300; animation: drawLine 0.4s ease-out 0.5s forwards }
  .lrelu-f1 { opacity: 0; animation: fadeIn 0.3s ease-out 0.3s forwards }
  .lrelu-f2 { opacity: 0; animation: fadeIn 0.3s ease-out 0.6s forwards }
  .lrelu-f3 { opacity: 0; animation: fadeIn 0.3s ease-out 0.9s forwards }
`

const mapX = (v: number) => 110 + v * 18
const mapY = (v: number) => 100 - v * 18

export const LeakyReLUDiagram: React.FC<{ compact?: boolean }> = ({ compact }) => {
  if (compact) {
    return (
      <div style={{ textAlign: 'center', padding: '6px' }}>
        <div style={{ fontSize: 14, color: COLOR }}><BlockMath math={LATEX} /></div>
        <div style={{ color: '#888', fontSize: 9 }}>负数有小斜率</div>
      </div>
    )
  }

  return (
    <div style={{ padding: '8px 0' }}>
      <div style={{
        padding: '4px 8px', display: 'flex', alignItems: 'center', gap: 8,
        background: 'rgba(255,255,255,0.02)', borderRadius: '8px 8px 0 0',
        border: '1px solid rgba(255,255,255,0.06)', borderBottom: 'none',
      }}>
        <span style={{ fontSize: 14, color: '#fff', fontWeight: 700, whiteSpace: 'nowrap' }}>Leaky ReLU</span>
        <div style={{ flex: 1, fontSize: 20, color: COLOR, textAlign: 'center' }}><BlockMath math={LATEX} /></div>
      </div>

      <div style={{ ...boardStyle, borderRadius: '0 0 8px 8px' }}>
        <div style={{ ...colStyle(1), minWidth: 150 }}>
          <div style={colLabelStyle}>解释</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
            <div>负数区域有<b>小斜率 α</b></div>
            <div style={{ marginTop: 6, color: '#aaa', fontSize: 11 }}>
              <div>• 解决 ReLU 的<b>死亡</b>问题</div>
              <div>• α 通常取 0.01</div>
              <div>• 所有神经元都有梯度</div>
              <div>• GAN 中常用</div>
            </div>
            <div style={{ marginTop: 8, color: '#888', fontSize: 10 }}>
              ReLU: x{'<'}0 → 梯度=0 (死了!)
            </div>
          </div>
        </div>

        <div style={dividerStyle} />

        <div style={{ ...colStyle(1), minWidth: 140 }}>
          <div style={colLabelStyle}>已知</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
            <div>α = {ALPHA} (示意用)</div>
            {[{ x: -3, c: '#666' }, { x: 0, c: '#FFD700' }, { x: 3, c: COLOR }].map(({ x, c }) => (
              <div key={x} style={{ color: c, fontSize: 11 }}>
                x={x} → f = {x > 0 ? x : (ALPHA * x).toFixed(1)}
              </div>
            ))}
            <div style={{ marginTop: 8, borderTop: '1px dashed rgba(255,255,255,0.1)', paddingTop: 6 }}>
              <span style={{ color: '#FFD700' }}>对比</span> ReLU vs Leaky ReLU
            </div>
          </div>
        </div>

        <div style={dividerStyle} />

        <div style={{ ...colStyle(1.3), minWidth: 240 }}>
          <div style={colLabelStyle}>解题过程</div>
          <style>{animCSS}</style>

          <div style={{ fontSize: 11, color: '#aaa', lineHeight: 1.7, marginBottom: 4 }}>
            <div className="lrelu-f1">① x {'>'} 0: 斜率 = 1 (和 ReLU 一样)</div>
            <div className="lrelu-f2">② x ≤ 0: 斜率 = α = {ALPHA} (不再是 0!)</div>
            <div className="lrelu-f3" style={conclusionStyle}>
              <span style={{ color: '#FFD700', fontWeight: 700 }}>∴</span> 梯度永不为零 → 没有死亡神经元
            </div>
          </div>

          <svg width={220} height={130} viewBox="0 0 220 130" style={{ display: 'block' }}>
            {/* 坐标轴 */}
            <line x1={20} y1={mapY(0)} x2={210} y2={mapY(0)} stroke="#ffffff15" strokeWidth={1} />
            <line x1={mapX(0)} y1={10} x2={mapX(0)} y2={125} stroke="#ffffff15" strokeWidth={1} />

            {/* ReLU (虚线灰) */}
            <line x1={mapX(-5)} y1={mapY(0)} x2={mapX(0)} y2={mapY(0)}
              stroke="#ffffff20" strokeWidth={1.5} strokeDasharray="4 3" />
            <line x1={mapX(0)} y1={mapY(0)} x2={mapX(5)} y2={mapY(5)}
              stroke="#ffffff20" strokeWidth={1.5} strokeDasharray="4 3" />
            <text x={mapX(4.5)} y={mapY(4.5) - 8} fill="#666" fontSize={7}>ReLU</text>

            {/* Leaky ReLU: x<0 段 (αx, 小斜率) */}
            <line x1={mapX(-5)} y1={mapY(-5 * ALPHA)} x2={mapX(0)} y2={mapY(0)}
              className="lrelu-d1" stroke="#e67e22" strokeWidth={2.5} />

            {/* Leaky ReLU: x>0 段 (y=x) */}
            <line x1={mapX(0)} y1={mapY(0)} x2={mapX(5)} y2={mapY(5)}
              className="lrelu-d2" stroke={COLOR} strokeWidth={2.5} />

            {/* 原点 */}
            <circle cx={mapX(0)} cy={mapY(0)} r={4} fill="#FFD700" className="lrelu-f2" />
            <text x={mapX(0) + 6} y={mapY(0) - 5} fill="#FFD700" fontSize={9} className="lrelu-f2">(0,0)</text>

            {/* 标注斜率 */}
            <text x={mapX(-4)} y={mapY(-4 * ALPHA) - 6} fill="#e67e22" fontSize={8} className="lrelu-f1">
              斜率=α
            </text>
            <text x={mapX(2.5)} y={mapY(2.5) - 6} fill={COLOR} fontSize={8} className="lrelu-f2">
              斜率=1
            </text>
          </svg>
        </div>
      </div>
    </div>
  )
}

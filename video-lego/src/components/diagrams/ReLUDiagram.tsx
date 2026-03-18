// ═══════════════════════════════════════════════════════════
// ReLU — 顶部公式 + 三栏: 解释 | 已知 | 解题过程
// ═══════════════════════════════════════════════════════════

import React from 'react'
import 'katex/dist/katex.min.css'
import { BlockMath } from 'react-katex'
import { colStyle, dividerStyle, colLabelStyle, boardStyle, conclusionStyle } from './boardStyles'

const LATEX = String.raw`\text{ReLU}(x) = \max(0, x)`
const COLOR = '#e74c3c'

const animCSS = `
  @keyframes drawLine { from { stroke-dashoffset: 300 } to { stroke-dashoffset: 0 } }
  @keyframes fadeIn { from { opacity: 0 } to { opacity: 1 } }
  .relu-d1 { stroke-dasharray: 300; stroke-dashoffset: 300; animation: drawLine 0.4s ease-out 0.2s forwards }
  .relu-d2 { stroke-dasharray: 300; stroke-dashoffset: 300; animation: drawLine 0.4s ease-out 0.5s forwards }
  .relu-f1 { opacity: 0; animation: fadeIn 0.3s ease-out 0.3s forwards }
  .relu-f2 { opacity: 0; animation: fadeIn 0.3s ease-out 0.6s forwards }
  .relu-f3 { opacity: 0; animation: fadeIn 0.3s ease-out 0.9s forwards }
`

const mapX = (v: number) => 110 + v * 20
const mapY = (v: number) => 120 - v * 20

export const ReLUDiagram: React.FC<{ compact?: boolean }> = ({ compact }) => {
  if (compact) {
    return (
      <div style={{ textAlign: 'center', padding: '6px' }}>
        <div style={{ fontSize: 14, color: COLOR }}><BlockMath math={LATEX} /></div>
        <div style={{ color: '#888', fontSize: 9 }}>负数归零</div>
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
        <span style={{ fontSize: 14, color: '#fff', fontWeight: 700, whiteSpace: 'nowrap' }}>ReLU 函数</span>
        <div style={{ flex: 1, fontSize: 20, color: COLOR, textAlign: 'center' }}><BlockMath math={LATEX} /></div>
      </div>

      <div style={{ ...boardStyle, borderRadius: '0 0 8px 8px' }}>
        <div style={{ ...colStyle(1), minWidth: 150 }}>
          <div style={colLabelStyle}>解释</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
            <div><b>负数 → 0</b>，正数保持不变</div>
            <div style={{ marginTop: 6, color: '#aaa', fontSize: 11 }}>
              <div>• 计算极快 (只需比较)</div>
              <div>• 缓解梯度消失问题</div>
              <div>• 稀疏激活 (部分神经元为0)</div>
              <div>• 深度学习最常用的激活函数</div>
            </div>
          </div>
        </div>

        <div style={dividerStyle} />

        <div style={{ ...colStyle(1), minWidth: 140 }}>
          <div style={colLabelStyle}>已知</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
            {[{x: -3, r: 0}, {x: -1, r: 0}, {x: 0, r: 0}, {x: 1, r: 1}, {x: 3, r: 3}].map(({x, r}) => (
              <div key={x} style={{ color: r > 0 ? COLOR : '#666', fontSize: 11 }}>
                x = {x} → ReLU = {r}
              </div>
            ))}
            <div style={{ marginTop: 8, borderTop: '1px dashed rgba(255,255,255,0.1)', paddingTop: 6 }}>
              <span style={{ color: '#FFD700' }}>求</span> 折线图
            </div>
          </div>
        </div>

        <div style={dividerStyle} />

        <div style={{ ...colStyle(1.3), minWidth: 240 }}>
          <div style={colLabelStyle}>解题过程</div>
          <style>{animCSS}</style>

          <div style={{ fontSize: 11, color: '#aaa', lineHeight: 1.7, marginBottom: 4 }}>
            <div className="relu-f1">① x {'<'} 0: 输出 0 (水平线)</div>
            <div className="relu-f2">② x ≥ 0: 输出 x (45°线)</div>
            <div className="relu-f3" style={conclusionStyle}>
              <span style={{ color: '#FFD700', fontWeight: 700 }}>∴</span> 一条折线，拐点在原点
            </div>
          </div>

          <svg width={220} height={140} viewBox="0 0 220 140" style={{ display: 'block' }}>
            <line x1={20} y1={mapY(0)} x2={210} y2={mapY(0)} stroke="#ffffff15" strokeWidth={1} />
            <line x1={mapX(0)} y1={10} x2={mapX(0)} y2={130} stroke="#ffffff15" strokeWidth={1} />
            {/* x<0: 沿 y=0 */}
            <line x1={mapX(-5)} y1={mapY(0)} x2={mapX(0)} y2={mapY(0)}
              className="relu-d1" stroke="#666" strokeWidth={2.5} />
            {/* x>=0: y=x */}
            <line x1={mapX(0)} y1={mapY(0)} x2={mapX(5)} y2={mapY(5)}
              className="relu-d2" stroke={COLOR} strokeWidth={2.5} />
            <circle cx={mapX(0)} cy={mapY(0)} r={4} fill="#FFD700" className="relu-f2" />
            <text x={mapX(0) + 5} y={mapY(0) - 5} className="relu-f2" fill="#FFD700" fontSize={9}>(0,0)</text>
            <text x={mapX(-3)} y={mapY(0) - 5} className="relu-f1" fill="#666" fontSize={9}>= 0</text>
            <text x={mapX(3)} y={mapY(3) - 5} className="relu-f2" fill={COLOR} fontSize={9}>= x</text>
          </svg>
        </div>
      </div>
    </div>
  )
}

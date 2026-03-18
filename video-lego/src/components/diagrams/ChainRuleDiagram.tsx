// ═══════════════════════════════════════════════════════════
// 链式法则 Chain Rule — 反向传播的核心
// ═══════════════════════════════════════════════════════════

import React from 'react'
import 'katex/dist/katex.min.css'
import { BlockMath } from 'react-katex'
import { colStyle, dividerStyle, colLabelStyle, boardStyle, conclusionStyle } from './boardStyles'

const LATEX = String.raw`\frac{\partial L}{\partial x} = \frac{\partial L}{\partial y} \cdot \frac{\partial y}{\partial x}`
const COLOR = '#9b59b6'

const animCSS = `
  @keyframes fadeIn { from { opacity: 0 } to { opacity: 1 } }
  .cr-f1 { opacity: 0; animation: fadeIn 0.3s ease-out 0.2s forwards }
  .cr-f2 { opacity: 0; animation: fadeIn 0.3s ease-out 0.5s forwards }
  .cr-f3 { opacity: 0; animation: fadeIn 0.3s ease-out 0.8s forwards }
  .cr-f4 { opacity: 0; animation: fadeIn 0.3s ease-out 1.1s forwards }
`

export const ChainRuleDiagram: React.FC<{ compact?: boolean }> = ({ compact }) => {
  if (compact) return (
    <div style={{ textAlign: 'center', padding: '6px' }}>
      <div style={{ fontSize: 14, color: COLOR }}><BlockMath math={LATEX} /></div>
      <div style={{ color: '#888', fontSize: 9 }}>逐层求导相乘</div>
    </div>
  )

  return (
    <div style={{ padding: '8px 0' }}>
      <div style={{ padding: '4px 8px', display: 'flex', alignItems: 'center', gap: 8, background: 'rgba(255,255,255,0.02)', borderRadius: '8px 8px 0 0', border: '1px solid rgba(255,255,255,0.06)', borderBottom: 'none' }}>
        <span style={{ fontSize: 14, color: '#fff', fontWeight: 700, whiteSpace: 'nowrap' }}>链式法则</span>
        <div style={{ flex: 1, fontSize: 20, color: COLOR, textAlign: 'center' }}><BlockMath math={LATEX} /></div>
      </div>
      <div style={{ ...boardStyle, borderRadius: '0 0 8px 8px' }}>
        <div style={{ ...colStyle(1), minWidth: 150 }}>
          <div style={colLabelStyle}>解释</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
            <div><b>反向传播</b>的数学基础</div>
            <div style={{ marginTop: 6, color: '#aaa', fontSize: 11 }}>
              <div>• 复合函数求导 = 各层导数<b>相乘</b></div>
              <div>• 从输出端往输入端逐层传播</div>
              <div>• 每一层只需计算自己的局部梯度</div>
              <div>• 所有DL训练的核心</div>
            </div>
          </div>
        </div>
        <div style={dividerStyle} />
        <div style={{ ...colStyle(1), minWidth: 140 }}>
          <div style={colLabelStyle}>已知</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
            <div>例: y = 2x, L = y²</div>
            <div style={{ marginTop: 6, color: '#aaa', fontSize: 11 }}>
              <div>∂L/∂y = 2y = 4x</div>
              <div>∂y/∂x = 2</div>
              <div style={{ marginTop: 6, color: '#FFD700' }}>∂L/∂x = 4x × 2 = 8x</div>
            </div>
          </div>
        </div>
        <div style={dividerStyle} />
        <div style={{ ...colStyle(1.3), minWidth: 240 }}>
          <div style={colLabelStyle}>解题过程</div>
          <style>{animCSS}</style>
          <div style={{ fontSize: 11, color: '#aaa', lineHeight: 1.7, marginBottom: 4 }}>
            <div className="cr-f1">① 前向: x → y=f(x) → L=g(y)</div>
            <div className="cr-f2">② 反向: 先算 ∂L/∂y (输出层梯度)</div>
            <div className="cr-f3">③ 再算 ∂y/∂x (本层局部梯度)</div>
            <div className="cr-f4" style={conclusionStyle}>
              <span style={{ color: '#FFD700', fontWeight: 700 }}>∴</span> ∂L/∂x = 两个梯度相乘
            </div>
          </div>
          <svg width={220} height={100} viewBox="0 0 220 100" style={{ display: 'block' }}>
            {/* 前向传播箭头 */}
            <rect x={20} y={20} width={40} height={30} rx={4} fill={`${COLOR}30`} stroke={COLOR} strokeWidth={1} className="cr-f1" />
            <text x={40} y={40} fill="#fff" fontSize={12} textAnchor="middle" className="cr-f1">x</text>
            <line x1={65} y1={35} x2={85} y2={35} stroke="#555" strokeWidth={1} markerEnd="url(#arrowCR)" className="cr-f1" />

            <rect x={90} y={20} width={40} height={30} rx={4} fill={`${COLOR}30`} stroke={COLOR} strokeWidth={1} className="cr-f2" />
            <text x={110} y={40} fill="#fff" fontSize={12} textAnchor="middle" className="cr-f2">y</text>
            <line x1={135} y1={35} x2={155} y2={35} stroke="#555" strokeWidth={1} markerEnd="url(#arrowCR)" className="cr-f2" />

            <rect x={160} y={20} width={40} height={30} rx={4} fill="#e74c3c30" stroke="#e74c3c" strokeWidth={1} className="cr-f3" />
            <text x={180} y={40} fill="#e74c3c" fontSize={12} textAnchor="middle" className="cr-f3">L</text>

            {/* 反向传播箭头 */}
            <line x1={155} y1={70} x2={135} y2={70} stroke="#FFD700" strokeWidth={1.5} markerEnd="url(#arrowGold)" className="cr-f3" />
            <text x={145} y={85} fill="#FFD700" fontSize={8} textAnchor="middle" className="cr-f3">∂L/∂y</text>

            <line x1={85} y1={70} x2={65} y2={70} stroke="#FFD700" strokeWidth={1.5} markerEnd="url(#arrowGold)" className="cr-f4" />
            <text x={75} y={85} fill="#FFD700" fontSize={8} textAnchor="middle" className="cr-f4">∂L/∂x</text>

            <defs>
              <marker id="arrowCR" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6" fill="#555" /></marker>
              <marker id="arrowGold" markerWidth="6" markerHeight="6" refX="1" refY="3" orient="auto"><path d="M6,0 L0,3 L6,6" fill="#FFD700" /></marker>
            </defs>
          </svg>
        </div>
      </div>
    </div>
  )
}

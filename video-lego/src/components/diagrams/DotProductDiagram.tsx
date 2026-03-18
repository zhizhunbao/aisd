// ═══════════════════════════════════════════════════════════
// 点积 Dot Product
// ═══════════════════════════════════════════════════════════

import React from 'react'
import 'katex/dist/katex.min.css'
import { BlockMath } from 'react-katex'
import { colStyle, dividerStyle, colLabelStyle, boardStyle, conclusionStyle } from './boardStyles'

const LATEX = String.raw`\vec{a} \cdot \vec{b} = \sum_{i=1}^{n} a_i b_i`
const COLOR = '#2ecc71'

const animCSS = `
  @keyframes fadeIn { from { opacity: 0 } to { opacity: 1 } }
  .dp-f1 { opacity: 0; animation: fadeIn 0.3s ease-out 0.2s forwards }
  .dp-f2 { opacity: 0; animation: fadeIn 0.3s ease-out 0.5s forwards }
  .dp-f3 { opacity: 0; animation: fadeIn 0.3s ease-out 0.8s forwards }
`

export const DotProductDiagram: React.FC<{ compact?: boolean }> = ({ compact }) => {
  if (compact) return (
    <div style={{ textAlign: 'center', padding: '6px' }}>
      <div style={{ fontSize: 14, color: COLOR }}><BlockMath math={LATEX} /></div>
      <div style={{ color: '#888', fontSize: 9 }}>对应元素相乘求和</div>
    </div>
  )

  return (
    <div style={{ padding: '8px 0' }}>
      <div style={{ padding: '4px 8px', display: 'flex', alignItems: 'center', gap: 8, background: 'rgba(255,255,255,0.02)', borderRadius: '8px 8px 0 0', border: '1px solid rgba(255,255,255,0.06)', borderBottom: 'none' }}>
        <span style={{ fontSize: 14, color: '#fff', fontWeight: 700, whiteSpace: 'nowrap' }}>点积</span>
        <div style={{ flex: 1, fontSize: 20, color: COLOR, textAlign: 'center' }}><BlockMath math={LATEX} /></div>
      </div>
      <div style={{ ...boardStyle, borderRadius: '0 0 8px 8px' }}>
        <div style={{ ...colStyle(1), minWidth: 150 }}>
          <div style={colLabelStyle}>解释</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
            <div>两个向量的<b>投影</b>关系</div>
            <div style={{ marginTop: 6, color: '#aaa', fontSize: 11 }}>
              <div>• 结果 {'>'} 0 → 方向大致相同</div>
              <div>• 结果 = 0 → 正交/无关</div>
              <div>• 结果 {'<'} 0 → 方向相反</div>
              <div>• Attention 的核心运算</div>
            </div>
          </div>
        </div>
        <div style={dividerStyle} />
        <div style={{ ...colStyle(1), minWidth: 140 }}>
          <div style={colLabelStyle}>已知</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
            <div>a⃗ = [1, 2, 3]</div>
            <div>b⃗ = [4, 5, 6]</div>
            <div style={{ marginTop: 8, color: '#FFD700', fontSize: 11 }}>
              求 a⃗ · b⃗ = ?
            </div>
          </div>
        </div>
        <div style={dividerStyle} />
        <div style={{ ...colStyle(1.3), minWidth: 240 }}>
          <div style={colLabelStyle}>解题过程</div>
          <style>{animCSS}</style>
          <div style={{ fontSize: 11, color: '#aaa', lineHeight: 1.7 }}>
            <div className="dp-f1">① 1×4 = 4</div>
            <div className="dp-f1">② 2×5 = 10</div>
            <div className="dp-f2">③ 3×6 = 18</div>
            <div className="dp-f3" style={conclusionStyle}>
              <span style={{ color: '#FFD700', fontWeight: 700 }}>∴</span> a⃗·b⃗ = 4 + 10 + 18 = <b>32</b>
            </div>
          </div>
          <svg width={220} height={100} viewBox="0 0 220 100" style={{ display: 'block' }}>
            <line x1={30} y1={80} x2={190} y2={80} stroke="#ffffff15" strokeWidth={1} />
            <line x1={30} y1={80} x2={30} y2={10} stroke="#ffffff15" strokeWidth={1} />
            {/* 向量 a */}
            <line x1={30} y1={80} x2={120} y2={30} stroke={COLOR} strokeWidth={2} className="dp-f1" />
            <text x={80} y={45} fill={COLOR} fontSize={10} className="dp-f1">a⃗</text>
            {/* 向量 b */}
            <line x1={30} y1={80} x2={170} y2={50} stroke="#e67e22" strokeWidth={2} className="dp-f2" />
            <text x={110} y={70} fill="#e67e22" fontSize={10} className="dp-f2">b⃗</text>
            {/* 投影虚线 */}
            <line x1={120} y1={30} x2={140} y2={65} stroke="#FFD700" strokeWidth={1} strokeDasharray="3 3" className="dp-f3" />
            <text x={150} y={55} fill="#FFD700" fontSize={8} className="dp-f3">θ</text>
          </svg>
        </div>
      </div>
    </div>
  )
}

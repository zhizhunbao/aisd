// ═══════════════════════════════════════════════════════════
// 行列式 — 顶部公式 + 三栏: 解释 | 已知 | 解题过程
// ═══════════════════════════════════════════════════════════

import React from 'react'
import 'katex/dist/katex.min.css'
import { BlockMath, InlineMath } from 'react-katex'
import { colStyle, dividerStyle, colLabelStyle, boardStyle, conclusionStyle } from './boardStyles'

const LATEX = String.raw`\det\begin{pmatrix} a & b \\ c & d \end{pmatrix} = ad - bc`
const COLOR = '#8e44ad'

const animCSS = `
  @keyframes fadeIn { from { opacity: 0 } to { opacity: 1 } }
  @keyframes pop { from { opacity: 0; transform: scale(0.6) } to { opacity: 1; transform: scale(1) } }
  .det-f1 { opacity: 0; animation: fadeIn 0.3s ease-out 0.2s forwards }
  .det-f2 { opacity: 0; animation: fadeIn 0.3s ease-out 0.5s forwards }
  .det-f3 { opacity: 0; animation: fadeIn 0.3s ease-out 0.8s forwards }
  .det-done { opacity: 0; animation: pop 0.3s ease-out 1.0s forwards }
`

export const DeterminantDiagram: React.FC<{ compact?: boolean }> = ({ compact }) => {
  if (compact) {
    return (
      <div style={{ textAlign: 'center', padding: '6px' }}>
        <div style={{ fontSize: 14, color: COLOR }}><BlockMath math={LATEX} /></div>
        <div style={{ color: '#888', fontSize: 9 }}>面积缩放因子</div>
      </div>
    )
  }

  // 单位正方形 → 平行四边形 变换 (A = [[2,1],[0,3]])
  const ox = 15, oy = 15
  // 原始单位正方形
  const sq = [[0, 0], [1, 0], [1, 1], [0, 1]].map(([x, y]) => [ox + x * 40, oy + (1 - y) * 45])
  // 变换后平行四边形: A*[x,y]ᵀ  → [2x+y, 3y]
  const ox2 = 130, oy2 = 15
  const tf = [[0, 0], [2, 0], [3, 3], [1, 3]].map(([x, y]) => [ox2 + x * 18, oy2 + (3 - y) * 15])

  return (
    <div style={{ padding: '8px 0' }}>
      <div style={{
        padding: '4px 8px', display: 'flex', alignItems: 'center', gap: 8,
        background: 'rgba(255,255,255,0.02)', borderRadius: '8px 8px 0 0',
        border: '1px solid rgba(255,255,255,0.06)', borderBottom: 'none',
      }}>
        <span style={{ fontSize: 14, color: '#fff', fontWeight: 700, whiteSpace: 'nowrap' }}>行列式</span>
        <div style={{ flex: 1, fontSize: 18, color: COLOR, textAlign: 'center' }}><BlockMath math={LATEX} /></div>
      </div>

      <div style={{ ...boardStyle, borderRadius: '0 0 8px 8px' }}>
        <div style={{ ...colStyle(1), minWidth: 150 }}>
          <div style={colLabelStyle}>解释</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
            <div>矩阵的<b>面积/体积缩放因子</b></div>
            <div style={{ marginTop: 6, color: '#aaa', fontSize: 11 }}>
              <div>• det ≠ 0 → 矩阵<b>可逆</b></div>
              <div>• det = 0 → 不可逆 (压扁了)</div>
              <div>• |det| = 面积缩放倍数</div>
              <div>• det {'<'} 0 → 翻转了方向</div>
            </div>
          </div>
        </div>

        <div style={dividerStyle} />

        <div style={{ ...colStyle(1), minWidth: 140 }}>
          <div style={colLabelStyle}>已知</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.6 }}>
            <div><InlineMath math="A = \begin{pmatrix} 2 & 1 \\ 0 & 3 \end{pmatrix}" /></div>
            <div style={{ marginTop: 6 }}>求 det(A)</div>
            <div style={{ marginTop: 6, borderTop: '1px dashed rgba(255,255,255,0.1)', paddingTop: 4 }}>
              <span style={{ color: '#FFD700' }}>观察</span> 单位正方形如何变形
            </div>
          </div>
        </div>

        <div style={dividerStyle} />

        <div style={{ ...colStyle(1.5), minWidth: 260 }}>
          <div style={colLabelStyle}>解题过程</div>
          <style>{animCSS}</style>

          <div style={{ fontSize: 11, color: '#aaa', lineHeight: 1.7, marginBottom: 4 }}>
            <div className="det-f1">① det = a·d - b·c = 2×3 - 1×0</div>
            <div className="det-f2">② = 6 - 0 = <b style={{ color: COLOR }}>6</b></div>
            <div className="det-done" style={conclusionStyle}>
              <span style={{ color: '#FFD700', fontWeight: 700 }}>∴</span> 面积放大 <b style={{ color: '#2ecc71' }}>6</b> 倍
            </div>
          </div>

          <svg width={220} height={100} viewBox="0 0 220 100" style={{ display: 'block' }}>
            {/* 原始单位正方形 */}
            <polygon points={sq.map(p => p.join(',')).join(' ')}
              fill={`${COLOR}15`} stroke={COLOR} strokeWidth={1.5} className="det-f1" />
            <text x={ox + 20} y={oy + 25} fill="#aaa" fontSize={8} textAnchor="middle" className="det-f1">面积=1</text>

            {/* 箭头 */}
            <text x={100} y={50} fill={COLOR} fontSize={14} textAnchor="middle" className="det-f2">→</text>
            <text x={100} y={62} fill="#888" fontSize={7} textAnchor="middle" className="det-f2">×A</text>

            {/* 变换后平行四边形 */}
            <polygon points={tf.map(p => p.join(',')).join(' ')}
              fill={`${COLOR}25`} stroke={COLOR} strokeWidth={2} className="det-f3" />
            <text x={ox2 + 28} y={oy2 + 30} fill={COLOR} fontSize={9} textAnchor="middle" className="det-f3">面积=6</text>
          </svg>
        </div>
      </div>
    </div>
  )
}

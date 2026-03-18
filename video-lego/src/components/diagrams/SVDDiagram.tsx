// ═══════════════════════════════════════════════════════════
// SVD 奇异值分解 — 顶部公式 + 三栏: 解释 | 已知 | 解题过程
// ═══════════════════════════════════════════════════════════

import React from 'react'
import 'katex/dist/katex.min.css'
import { BlockMath, InlineMath } from 'react-katex'
import { colStyle, dividerStyle, colLabelStyle, boardStyle, conclusionStyle } from './boardStyles'

const LATEX = String.raw`A = U \Sigma V^T`
const COLOR = '#3498db'

const animCSS = `
  @keyframes fadeIn { from { opacity: 0 } to { opacity: 1 } }
  @keyframes pop { from { opacity: 0; transform: scale(0.6) } to { opacity: 1; transform: scale(1) } }
  .svd-f1 { opacity: 0; animation: fadeIn 0.3s ease-out 0.2s forwards }
  .svd-f2 { opacity: 0; animation: fadeIn 0.3s ease-out 0.5s forwards }
  .svd-f3 { opacity: 0; animation: fadeIn 0.3s ease-out 0.8s forwards }
  .svd-done { opacity: 0; animation: pop 0.3s ease-out 1.1s forwards }
`

export const SVDDiagram: React.FC<{ compact?: boolean }> = ({ compact }) => {
  if (compact) {
    return (
      <div style={{ textAlign: 'center', padding: '6px' }}>
        <div style={{ fontSize: 14, color: COLOR }}><BlockMath math={LATEX} /></div>
        <div style={{ color: '#888', fontSize: 9 }}>旋转×缩放×旋转</div>
      </div>
    )
  }

  // SVG: 圆 → 椭圆分解 (V旋转 → Σ拉伸 → U旋转)
  const cy = 55, r = 22
  const boxW = 44, boxH = 32, gap = 8
  const sx = 16 // 起始 x

  return (
    <div style={{ padding: '8px 0' }}>
      <div style={{
        padding: '4px 8px', display: 'flex', alignItems: 'center', gap: 8,
        background: 'rgba(255,255,255,0.02)', borderRadius: '8px 8px 0 0',
        border: '1px solid rgba(255,255,255,0.06)', borderBottom: 'none',
      }}>
        <span style={{ fontSize: 14, color: '#fff', fontWeight: 700, whiteSpace: 'nowrap' }}>SVD 奇异值分解</span>
        <div style={{ flex: 1, fontSize: 20, color: COLOR, textAlign: 'center' }}><BlockMath math={LATEX} /></div>
      </div>

      <div style={{ ...boardStyle, borderRadius: '0 0 8px 8px' }}>
        <div style={{ ...colStyle(1), minWidth: 150 }}>
          <div style={colLabelStyle}>解释</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
            <div>任意矩阵 = <b>旋转×缩放×旋转</b></div>
            <div style={{ marginTop: 6, color: '#aaa', fontSize: 11 }}>
              <div>• V<sup>T</sup>: 输入空间旋转</div>
              <div>• Σ: 沿轴缩放 (奇异值)</div>
              <div>• U: 输出空间旋转</div>
              <div>• PCA/降维/压缩的核心</div>
            </div>
            <div style={{ marginTop: 8, color: '#888', fontSize: 10 }}>
              保留前 k 个奇异值 → 降维
            </div>
          </div>
        </div>

        <div style={dividerStyle} />

        <div style={{ ...colStyle(1), minWidth: 140 }}>
          <div style={colLabelStyle}>已知</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.6 }}>
            <div><InlineMath math="A \in \mathbb{R}^{m \times n}" /></div>
            <div style={{ marginTop: 6, color: '#aaa', fontSize: 11 }}>
              <div>U ∈ R<sup>m×m</sup> (正交)</div>
              <div>Σ ∈ R<sup>m×n</sup> (对角)</div>
              <div>V ∈ R<sup>n×n</sup> (正交)</div>
            </div>
            <div style={{ marginTop: 6, borderTop: '1px dashed rgba(255,255,255,0.1)', paddingTop: 4 }}>
              <span style={{ color: '#FFD700' }}>观察</span> 圆如何变成椭圆
            </div>
          </div>
        </div>

        <div style={dividerStyle} />

        <div style={{ ...colStyle(1.5), minWidth: 260 }}>
          <div style={colLabelStyle}>解题过程</div>
          <style>{animCSS}</style>

          <div style={{ fontSize: 11, color: '#aaa', lineHeight: 1.7, marginBottom: 4 }}>
            <div className="svd-f1">① V<sup>T</sup>: 先在输入空间旋转对齐</div>
            <div className="svd-f2">② Σ: 沿主轴缩放 (σ₁ ≥ σ₂ ≥ ...)</div>
            <div className="svd-f3">③ U: 在输出空间旋转到位</div>
            <div className="svd-done" style={conclusionStyle}>
              <span style={{ color: '#FFD700', fontWeight: 700 }}>∴</span> 圆 → 旋转+拉伸 = 椭圆
            </div>
          </div>

          <svg width={220} height={100} viewBox="0 0 220 100" style={{ display: 'block' }}>
            {/* Step 1: 圆 (原始) */}
            <circle cx={sx + r} cy={cy} r={r} fill="none" stroke="#ffffff30" strokeWidth={1.5} className="svd-f1" />
            <text x={sx + r} y={cy + r + 12} fill="#888" fontSize={7} textAnchor="middle" className="svd-f1">单位圆</text>

            {/* 箭头 V^T */}
            <text x={sx + boxW + 6} y={cy + 3} fill="#e67e22" fontSize={10} className="svd-f1">→</text>
            <text x={sx + boxW + 6} y={cy + 14} fill="#e67e2280" fontSize={6} className="svd-f1">V<tspan baselineShift="super" fontSize="5">T</tspan></text>

            {/* Step 2: 旋转后的圆 */}
            <circle cx={sx + boxW + 26 + r} cy={cy} r={r} fill="none" stroke="#e67e2250" strokeWidth={1.5} className="svd-f2" />
            {/* 十字线显示旋转 */}
            <line x1={sx + boxW + 26 + r - 18} y1={cy - 10} x2={sx + boxW + 26 + r + 18} y2={cy + 10} stroke="#e67e2240" strokeWidth={1} className="svd-f2" />

            {/* 箭头 Σ */}
            <text x={sx + 2 * boxW + 26} y={cy + 3} fill={COLOR} fontSize={10} className="svd-f2">→</text>
            <text x={sx + 2 * boxW + 26} y={cy + 14} fill={`${COLOR}80`} fontSize={7} className="svd-f2">Σ</text>

            {/* Step 3: 拉伸后椭圆 */}
            <ellipse cx={sx + 2 * boxW + 44 + r} cy={cy} rx={r * 1.5} ry={r * 0.6}
              fill="none" stroke={`${COLOR}70`} strokeWidth={1.5}
              transform={`rotate(-20 ${sx + 2 * boxW + 44 + r} ${cy})`} className="svd-f3" />

            {/* 箭头 U */}
            <text x={sx + 3 * boxW + 32} y={cy + 3} fill="#2ecc71" fontSize={10} className="svd-f3">→</text>
            <text x={sx + 3 * boxW + 32} y={cy + 14} fill="#2ecc7180" fontSize={7} className="svd-f3">U</text>

            {/* Step 4: 最终椭圆 */}
            <ellipse cx={sx + 3 * boxW + 50 + r - 4} cy={cy} rx={r * 1.5} ry={r * 0.6}
              fill={`${COLOR}10`} stroke={COLOR} strokeWidth={2}
              transform={`rotate(15 ${sx + 3 * boxW + 50 + r - 4} ${cy})`} className="svd-done" />
            <text x={sx + 3 * boxW + 50 + r - 4} y={cy + r + 12} fill={COLOR} fontSize={7} textAnchor="middle" className="svd-done">最终映射</text>
          </svg>
        </div>
      </div>
    </div>
  )
}

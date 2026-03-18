// ═══════════════════════════════════════════════════════════
// Hessian 矩阵 — 顶部公式 + 三栏: 解释 | 已知 | 解题过程
// ═══════════════════════════════════════════════════════════

import React from 'react'
import 'katex/dist/katex.min.css'
import { BlockMath, InlineMath } from 'react-katex'
import { colStyle, dividerStyle, colLabelStyle, boardStyle, conclusionStyle } from './boardStyles'

const LATEX = String.raw`H_{ij} = \frac{\partial^2 f}{\partial x_i \partial x_j}`
const COLOR = '#8e44ad'

const animCSS = `
  @keyframes fadeIn { from { opacity: 0 } to { opacity: 1 } }
  @keyframes pop { from { opacity: 0; transform: scale(0.6) } to { opacity: 1; transform: scale(1) } }
  .hes-f1 { opacity: 0; animation: fadeIn 0.3s ease-out 0.2s forwards }
  .hes-f2 { opacity: 0; animation: fadeIn 0.3s ease-out 0.5s forwards }
  .hes-f3 { opacity: 0; animation: fadeIn 0.3s ease-out 0.8s forwards }
  .hes-done { opacity: 0; animation: pop 0.3s ease-out 1.1s forwards }
`

// 3D 曲面等高线 (鞍面/碗形)
const ctrColor = (v: number) => {
  const t = Math.min(1, v / 5)
  const r = Math.round(142 + t * 113)
  const g = Math.round(68 + t * (40 - 68))
  const b = Math.round(173 + t * (60 - 173))
  return `rgb(${r},${g},${b})`
}

export const HessianDiagram: React.FC<{ compact?: boolean }> = ({ compact }) => {
  if (compact) {
    return (
      <div style={{ textAlign: 'center', padding: '6px' }}>
        <div style={{ fontSize: 14, color: COLOR }}><BlockMath math={LATEX} /></div>
        <div style={{ color: '#888', fontSize: 9 }}>曲率矩阵</div>
      </div>
    )
  }

  // 等高线数据: f(x,y) = x² + 2y²  (碗形，正定 Hessian)
  const levels = [0.5, 1.5, 3, 5, 8]
  const cx = 110, cy = 70

  return (
    <div style={{ padding: '8px 0' }}>
      <div style={{
        padding: '4px 8px', display: 'flex', alignItems: 'center', gap: 8,
        background: 'rgba(255,255,255,0.02)', borderRadius: '8px 8px 0 0',
        border: '1px solid rgba(255,255,255,0.06)', borderBottom: 'none',
      }}>
        <span style={{ fontSize: 14, color: '#fff', fontWeight: 700, whiteSpace: 'nowrap' }}>Hessian 矩阵</span>
        <div style={{ flex: 1, fontSize: 20, color: COLOR, textAlign: 'center' }}><BlockMath math={LATEX} /></div>
      </div>

      <div style={{ ...boardStyle, borderRadius: '0 0 8px 8px' }}>
        <div style={{ ...colStyle(1), minWidth: 150 }}>
          <div style={colLabelStyle}>解释</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
            <div><b>二阶偏导</b>组成的对称方阵</div>
            <div style={{ marginTop: 6, color: '#aaa', fontSize: 11 }}>
              <div>• 描述曲面的<b>曲率</b></div>
              <div>• 正定 → 极小值 (碗形)</div>
              <div>• 负定 → 极大值 (倒碗)</div>
              <div>• 不定 → 鞍点 (马鞍)</div>
            </div>
            <div style={{ marginTop: 8, color: '#888', fontSize: 10 }}>
              Newton法: Δθ = -H⁻¹∇f
            </div>
          </div>
        </div>

        <div style={dividerStyle} />

        <div style={{ ...colStyle(1), minWidth: 150 }}>
          <div style={colLabelStyle}>已知</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.6 }}>
            <div><InlineMath math="f(x,y) = x^2 + 2y^2" /></div>
            <div style={{ marginTop: 6 }}>求 Hessian 矩阵 H</div>
            <div style={{ marginTop: 6, borderTop: '1px dashed rgba(255,255,255,0.1)', paddingTop: 4 }}>
              <span style={{ color: '#FFD700' }}>判断</span> 极值类型
            </div>
          </div>
        </div>

        <div style={dividerStyle} />

        <div style={{ ...colStyle(1.5), minWidth: 260 }}>
          <div style={colLabelStyle}>解题过程</div>
          <style>{animCSS}</style>

          <div style={{ fontSize: 11, color: '#aaa', lineHeight: 1.7, marginBottom: 4 }}>
            <div className="hes-f1">① ∂²f/∂x² = <b style={{ color: COLOR }}>2</b>, ∂²f/∂x∂y = <b style={{ color: COLOR }}>0</b></div>
            <div className="hes-f2">② ∂²f/∂y∂x = <b style={{ color: COLOR }}>0</b>, ∂²f/∂y² = <b style={{ color: COLOR }}>4</b></div>
            <div className="hes-f3">
              ③ H = <InlineMath math="\begin{bmatrix} 2 & 0 \\ 0 & 4 \end{bmatrix}" />
              , λ₁=2, λ₂=4
            </div>
            <div className="hes-done" style={conclusionStyle}>
              <span style={{ color: '#FFD700', fontWeight: 700 }}>∴</span>{' '}
              正定 (λ{'>'}0) → <b style={{ color: '#2ecc71' }}>极小值</b>
            </div>
          </div>

          {/* SVG: 等高线图 */}
          <svg width={220} height={130} viewBox="0 0 220 130" style={{ display: 'block' }}>
            {/* 坐标轴 */}
            <line x1={20} y1={cy} x2={200} y2={cy} stroke="#ffffff12" strokeWidth={1} />
            <line x1={cx} y1={10} x2={cx} y2={125} stroke="#ffffff12" strokeWidth={1} />
            <text x={202} y={cy + 3} fill="#666" fontSize={8}>x</text>
            <text x={cx + 4} y={12} fill="#666" fontSize={8}>y</text>

            {/* 等高线椭圆: f = x² + 2y² = c  → 椭圆 x²/c + y²/(c/2) = 1 */}
            {levels.map((c, i) => {
              const rx = Math.sqrt(c) * 18   // x 半径
              const ry = Math.sqrt(c / 2) * 18 // y 半径
              return (
                <ellipse key={i} cx={cx} cy={cy} rx={rx} ry={ry}
                  fill="none" stroke={ctrColor(c)} strokeWidth={1.5} opacity={0.7}
                  className={`hes-f${Math.min(i + 1, 3)}`} />
              )
            })}

            {/* 极小值点 */}
            <circle cx={cx} cy={cy} r={3} fill="#2ecc71" className="hes-done" />
            <text x={cx + 6} y={cy - 4} fill="#2ecc71" fontSize={9} className="hes-done">min</text>

            {/* 标注 */}
            <text x={30} y={120} fill="#666" fontSize={8} className="hes-f3">等高线: 正定→椭圆(碗形)</text>
          </svg>
        </div>
      </div>
    </div>
  )
}

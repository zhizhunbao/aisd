// ═══════════════════════════════════════════════════════════
// Jacobian 矩阵 — 顶部公式 + 三栏: 解释 | 已知 | 解题过程
// ═══════════════════════════════════════════════════════════

import React from 'react'
import 'katex/dist/katex.min.css'
import { BlockMath, InlineMath } from 'react-katex'
import { colStyle, dividerStyle, colLabelStyle, boardStyle, conclusionStyle } from './boardStyles'

const LATEX = String.raw`J = \begin{bmatrix} \frac{\partial f_1}{\partial x_1} & \cdots & \frac{\partial f_1}{\partial x_n} \\ \vdots & \ddots & \vdots \\ \frac{\partial f_m}{\partial x_1} & \cdots & \frac{\partial f_m}{\partial x_n} \end{bmatrix}`
const COLOR = '#e67e22'

const animCSS = `
  @keyframes fadeIn { from { opacity: 0 } to { opacity: 1 } }
  @keyframes pop { from { opacity: 0; transform: scale(0.6) } to { opacity: 1; transform: scale(1) } }
  .jac-f1 { opacity: 0; animation: fadeIn 0.3s ease-out 0.2s forwards }
  .jac-f2 { opacity: 0; animation: fadeIn 0.3s ease-out 0.5s forwards }
  .jac-f3 { opacity: 0; animation: fadeIn 0.3s ease-out 0.8s forwards }
  .jac-done { opacity: 0; animation: pop 0.3s ease-out 1.0s forwards }
`

export const JacobianDiagram: React.FC<{ compact?: boolean }> = ({ compact }) => {
  if (compact) {
    return (
      <div style={{ textAlign: 'center', padding: '6px' }}>
        <div style={{ fontSize: 14, color: COLOR }}><BlockMath math={LATEX} /></div>
        <div style={{ color: '#888', fontSize: 9 }}>多维导数矩阵</div>
      </div>
    )
  }

  // SVG: 向量函数映射 R² → R²，网格变形可视化
  const gridColor = '#ffffff12'
  const N = 5
  const cellW = 30, cellH = 22
  const ox1 = 15, oy1 = 15   // 输入网格偏移
  const ox2 = 15, oy2 = 15   // 输出网格偏移（SVG 右半区域）

  return (
    <div style={{ padding: '8px 0' }}>
      <div style={{
        padding: '4px 8px', display: 'flex', alignItems: 'center', gap: 8,
        background: 'rgba(255,255,255,0.02)', borderRadius: '8px 8px 0 0',
        border: '1px solid rgba(255,255,255,0.06)', borderBottom: 'none',
      }}>
        <span style={{ fontSize: 14, color: '#fff', fontWeight: 700, whiteSpace: 'nowrap' }}>Jacobian 矩阵</span>
        <div style={{ flex: 1, fontSize: 18, color: COLOR, textAlign: 'center' }}><BlockMath math={LATEX} /></div>
      </div>

      <div style={{ ...boardStyle, borderRadius: '0 0 8px 8px' }}>
        <div style={{ ...colStyle(1), minWidth: 150 }}>
          <div style={colLabelStyle}>解释</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
            <div><b>向量函数</b>对向量变量的一阶导数矩阵</div>
            <div style={{ marginTop: 6, color: '#aaa', fontSize: 11 }}>
              <div>• J<sub>ij</sub> = ∂fᵢ/∂xⱼ</div>
              <div>• m×n 矩阵 (m个输出, n个输入)</div>
              <div>• 反向传播的核心计算</div>
              <div>• 描述局部线性近似</div>
            </div>
            <div style={{ marginTop: 8, color: '#888', fontSize: 10 }}>
              f(x+δ) ≈ f(x) + J·δ
            </div>
          </div>
        </div>

        <div style={dividerStyle} />

        <div style={{ ...colStyle(1), minWidth: 150 }}>
          <div style={colLabelStyle}>已知</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.6 }}>
            <div><InlineMath math="f_1 = x_1^2 + x_2" /></div>
            <div><InlineMath math="f_2 = x_1 \cdot x_2" /></div>
            <div style={{ marginTop: 6 }}>在点 (1, 2) 处求 J</div>
            <div style={{ marginTop: 6, borderTop: '1px dashed rgba(255,255,255,0.1)', paddingTop: 4 }}>
              <span style={{ color: '#FFD700' }}>求</span> 2×2 Jacobian 矩阵
            </div>
          </div>
        </div>

        <div style={dividerStyle} />

        <div style={{ ...colStyle(1.5), minWidth: 260 }}>
          <div style={colLabelStyle}>解题过程</div>
          <style>{animCSS}</style>

          <div style={{ fontSize: 11, color: '#aaa', lineHeight: 1.7, marginBottom: 4 }}>
            <div className="jac-f1">① ∂f₁/∂x₁ = 2x₁ = <b style={{ color: COLOR }}>2</b>,  ∂f₁/∂x₂ = <b style={{ color: COLOR }}>1</b></div>
            <div className="jac-f2">② ∂f₂/∂x₁ = x₂ = <b style={{ color: COLOR }}>2</b>,  ∂f₂/∂x₂ = x₁ = <b style={{ color: COLOR }}>1</b></div>
            <div className="jac-f3" style={conclusionStyle}>
              <span style={{ color: '#FFD700', fontWeight: 700 }}>∴</span>{' '}
              <InlineMath math="J = \begin{bmatrix} 2 & 1 \\ 2 & 1 \end{bmatrix}" />
            </div>
          </div>

          {/* SVG: 输入规则网格 → 输出变形网格 */}
          <svg width={220} height={130} viewBox="0 0 220 130" style={{ display: 'block' }}>
            {/* 左: 输入空间 (规则网格) */}
            <text x={ox1 + cellW * 2} y={10} fill="#888" fontSize={9} textAnchor="middle">输入空间</text>
            {Array.from({ length: N + 1 }).map((_, i) => (
              <React.Fragment key={`g1-${i}`}>
                <line x1={ox1} y1={oy1 + i * cellH} x2={ox1 + N * cellW}  y2={oy1 + i * cellH} stroke={gridColor} strokeWidth={1} />
                <line x1={ox1 + i * cellW} y1={oy1} x2={ox1 + i * cellW} y2={oy1 + N * cellH} stroke={gridColor} strokeWidth={1} />
              </React.Fragment>
            ))}
            <circle cx={ox1 + 1 * cellW} cy={oy1 + 2 * cellH} r={3} fill={COLOR} className="jac-f1" />
            <text x={ox1 + 1 * cellW} y={oy1 + 2 * cellH - 6} fill={COLOR} fontSize={8} textAnchor="middle" className="jac-f1">(1,2)</text>

            {/* 箭头 */}
            <text x={110} y={75} fill={COLOR} fontSize={16} textAnchor="middle" className="jac-f2">→</text>
            <text x={110} y={88} fill="#888" fontSize={8} textAnchor="middle" className="jac-f2">J 变换</text>

            {/* 右: 输出空间 (变形网格) */}
            <g transform="translate(125, 0)">
              <text x={cellW * 2} y={10} fill="#888" fontSize={9} textAnchor="middle">输出空间</text>
              {/* 变形网格: 用 J=[[2,1],[2,1]] 做线性变形 */}
              {Array.from({ length: N + 1 }).map((_, i) => {
                // 水平线: 固定 y=i, x 从 0..N
                const pts = Array.from({ length: N + 1 }).map((_, j) => {
                  const tx = ox2 + (2 * j + i) * (cellW / 2.5)
                  const ty = oy1 + (2 * j + i) * (cellH / 3.5)
                  return `${tx},${ty}`
                }).join(' ')
                return <polyline key={`h-${i}`} points={pts} fill="none" stroke={`${COLOR}40`} strokeWidth={1} />
              })}
              {Array.from({ length: N + 1 }).map((_, j) => {
                const pts = Array.from({ length: N + 1 }).map((_, i) => {
                  const tx = ox2 + (2 * j + i) * (cellW / 2.5)
                  const ty = oy1 + (2 * j + i) * (cellH / 3.5)
                  return `${tx},${ty}`
                }).join(' ')
                return <polyline key={`v-${j}`} points={pts} fill="none" stroke={`${COLOR}40`} strokeWidth={1} />
              })}
            </g>
          </svg>
        </div>
      </div>
    </div>
  )
}

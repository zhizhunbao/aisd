// ═══════════════════════════════════════════════════════════
// 正规方程 — 顶部公式 + 三栏: 解释 | 已知 | 解题过程
// ═══════════════════════════════════════════════════════════

import React from 'react'
import 'katex/dist/katex.min.css'
import { BlockMath, InlineMath } from 'react-katex'
import { colStyle, dividerStyle, colLabelStyle, boardStyle, conclusionStyle } from './boardStyles'

const LATEX = String.raw`\hat{\theta} = (X^T X)^{-1} X^T y`
const COLOR = '#e67e22'

const animCSS = `
  @keyframes fadeIn { from { opacity: 0 } to { opacity: 1 } }
  @keyframes pop { from { opacity: 0; transform: scale(0.6) } to { opacity: 1; transform: scale(1) } }
  .ne-f1 { opacity: 0; animation: fadeIn 0.3s ease-out 0.2s forwards }
  .ne-f2 { opacity: 0; animation: fadeIn 0.3s ease-out 0.5s forwards }
  .ne-f3 { opacity: 0; animation: fadeIn 0.3s ease-out 0.8s forwards }
  .ne-done { opacity: 0; animation: pop 0.3s ease-out 1.0s forwards }
`

// 散点 + 回归线
const points = [{ x: 1, y: 1.2 }, { x: 2, y: 1.9 }, { x: 3, y: 3.1 }, { x: 4, y: 3.8 }, { x: 5, y: 5.2 }]
const mapX = (v: number) => 25 + (v / 6) * 190
const mapY = (v: number) => 115 - v * 18

export const NormalEquationDiagram: React.FC<{ compact?: boolean }> = ({ compact }) => {
  if (compact) {
    return (
      <div style={{ textAlign: 'center', padding: '6px' }}>
        <div style={{ fontSize: 14, color: COLOR }}><BlockMath math={LATEX} /></div>
        <div style={{ color: '#888', fontSize: 9 }}>解析解</div>
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
        <span style={{ fontSize: 14, color: '#fff', fontWeight: 700, whiteSpace: 'nowrap' }}>正规方程</span>
        <div style={{ flex: 1, fontSize: 20, color: COLOR, textAlign: 'center' }}><BlockMath math={LATEX} /></div>
      </div>

      <div style={{ ...boardStyle, borderRadius: '0 0 8px 8px' }}>
        <div style={{ ...colStyle(1), minWidth: 150 }}>
          <div style={colLabelStyle}>解释</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
            <div>线性回归的<b>解析解</b></div>
            <div style={{ marginTop: 6, color: '#aaa', fontSize: 11 }}>
              <div>• 一步求最优，无需迭代</div>
              <div>• 需要 X<sup>T</sup>X 可逆</div>
              <div>• O(n³) 复杂度</div>
              <div>• 数据量大时用 SGD 替代</div>
            </div>
          </div>
        </div>

        <div style={dividerStyle} />

        <div style={{ ...colStyle(1), minWidth: 150 }}>
          <div style={colLabelStyle}>已知</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.6 }}>
            <div>5 个数据点:</div>
            <div style={{ fontSize: 10, color: '#aaa' }}>
              (1,1.2) (2,1.9) (3,3.1) (4,3.8) (5,5.2)
            </div>
            <div style={{ marginTop: 6, borderTop: '1px dashed rgba(255,255,255,0.1)', paddingTop: 4 }}>
              <span style={{ color: '#FFD700' }}>求</span> 最佳拟合直线 y = θ₀ + θ₁x
            </div>
          </div>
        </div>

        <div style={dividerStyle} />

        <div style={{ ...colStyle(1.5), minWidth: 260 }}>
          <div style={colLabelStyle}>解题过程</div>
          <style>{animCSS}</style>

          <div style={{ fontSize: 11, color: '#aaa', lineHeight: 1.7, marginBottom: 4 }}>
            <div className="ne-f1">① 构造 X = [[1,1],[1,2],...,[1,5]], y = [1.2,...,5.2]</div>
            <div className="ne-f2">② <InlineMath math="\hat{\theta} = (X^TX)^{-1}X^Ty" /></div>
            <div className="ne-done" style={conclusionStyle}>
              <span style={{ color: '#FFD700', fontWeight: 700 }}>∴</span>{' '}
              θ̂ ≈ [0.04, 1.00] → <b style={{ color: '#2ecc71' }}>y ≈ x</b>
            </div>
          </div>

          <svg width={220} height={130} viewBox="0 0 220 130" style={{ display: 'block' }}>
            <line x1={20} y1={mapY(0)} x2={210} y2={mapY(0)} stroke="#ffffff12" strokeWidth={1} />
            <line x1={mapX(0)} y1={10} x2={mapX(0)} y2={120} stroke="#ffffff12" strokeWidth={1} />
            {/* 散点 */}
            {points.map((p, i) => (
              <circle key={i} cx={mapX(p.x)} cy={mapY(p.y)} r={3.5}
                fill={COLOR} className={`ne-f${Math.min(i + 1, 3)}`} />
            ))}
            {/* 最佳拟合直线: y ≈ 0.04 + 1.0x */}
            <line x1={mapX(0.5)} y1={mapY(0.54)} x2={mapX(5.5)} y2={mapY(5.54)}
              stroke="#2ecc71" strokeWidth={2} className="ne-f3" />
            <text x={mapX(4.5)} y={mapY(4.5) - 8} fill="#2ecc71" fontSize={9} className="ne-done">y ≈ x</text>
            {/* 残差虚线 */}
            {points.map((p, i) => (
              <line key={`r-${i}`} x1={mapX(p.x)} y1={mapY(p.y)}
                x2={mapX(p.x)} y2={mapY(0.04 + p.x)}
                stroke="#FFD70040" strokeWidth={1} strokeDasharray="2 2" className="ne-f3" />
            ))}
          </svg>
        </div>
      </div>
    </div>
  )
}

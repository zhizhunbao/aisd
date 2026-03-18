// ═══════════════════════════════════════════════════════════
// 多元高斯分布 — 顶部公式 + 三栏: 解释 | 已知 | 解题过程
// ═══════════════════════════════════════════════════════════

import React from 'react'
import 'katex/dist/katex.min.css'
import { BlockMath, InlineMath } from 'react-katex'
import { colStyle, dividerStyle, colLabelStyle, boardStyle, conclusionStyle } from './boardStyles'

const LATEX = String.raw`p(\mathbf{x}) = \frac{1}{(2\pi)^{d/2}|\Sigma|^{1/2}} \exp\!\left(-\tfrac{1}{2}(\mathbf{x}-\boldsymbol{\mu})^T \Sigma^{-1} (\mathbf{x}-\boldsymbol{\mu})\right)`
const COLOR = '#8e44ad'

const animCSS = `
  @keyframes fadeIn { from { opacity: 0 } to { opacity: 1 } }
  .mvg-f1 { opacity: 0; animation: fadeIn 0.3s ease-out 0.2s forwards }
  .mvg-f2 { opacity: 0; animation: fadeIn 0.3s ease-out 0.5s forwards }
  .mvg-f3 { opacity: 0; animation: fadeIn 0.3s ease-out 0.8s forwards }
  .mvg-done { opacity: 0; animation: fadeIn 0.3s ease-out 1.1s forwards }
`

export const MultivariateGaussianDiagram: React.FC<{ compact?: boolean }> = ({ compact }) => {
  if (compact) {
    return (
      <div style={{ textAlign: 'center', padding: '6px' }}>
        <div style={{ fontSize: 12, color: COLOR }}><BlockMath math={String.raw`\mathcal{N}(\boldsymbol{\mu}, \Sigma)`} /></div>
        <div style={{ color: '#888', fontSize: 9 }}>多维钟形</div>
      </div>
    )
  }

  const cx = 110, cy = 65

  // 三种协方差矩阵形状
  const shapes: Array<{ rx: number; ry: number; rot: number; label: string; color: string }> = [
    { rx: 35, ry: 35, rot: 0, label: 'σ₁=σ₂, ρ=0', color: '#3498db' },
    { rx: 45, ry: 20, rot: 0, label: 'σ₁>σ₂, ρ=0', color: '#e67e22' },
    { rx: 45, ry: 20, rot: -30, label: 'σ₁>σ₂, ρ≠0', color: COLOR },
  ]

  return (
    <div style={{ padding: '8px 0' }}>
      <div style={{
        padding: '4px 8px', display: 'flex', alignItems: 'center', gap: 8,
        background: 'rgba(255,255,255,0.02)', borderRadius: '8px 8px 0 0',
        border: '1px solid rgba(255,255,255,0.06)', borderBottom: 'none',
      }}>
        <span style={{ fontSize: 14, color: '#fff', fontWeight: 700, whiteSpace: 'nowrap' }}>多元高斯分布</span>
        <div style={{ flex: 1, fontSize: 16, color: COLOR, textAlign: 'center' }}>
          <BlockMath math={String.raw`p(\mathbf{x}) \propto \exp\!\left(-\tfrac{1}{2}(\mathbf{x}-\boldsymbol{\mu})^T \Sigma^{-1} (\mathbf{x}-\boldsymbol{\mu})\right)`} />
        </div>
      </div>

      <div style={{ ...boardStyle, borderRadius: '0 0 8px 8px' }}>
        <div style={{ ...colStyle(1), minWidth: 150 }}>
          <div style={colLabelStyle}>解释</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
            <div>多维的<b>钟形分布</b></div>
            <div style={{ marginTop: 6, color: '#aaa', fontSize: 11 }}>
              <div>• μ: 中心位置 (均值向量)</div>
              <div>• Σ: 形状 (协方差矩阵)</div>
              <div>• 等高线是<b>椭圆</b></div>
              <div>• GMM / VAE / PCA 的基础</div>
            </div>
          </div>
        </div>

        <div style={dividerStyle} />

        <div style={{ ...colStyle(1), minWidth: 140 }}>
          <div style={colLabelStyle}>已知</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.6 }}>
            <div><InlineMath math="\boldsymbol{\mu} = [0,0]" /></div>
            <div style={{ marginTop: 4, color: '#aaa', fontSize: 11 }}>
              <div>Σ 决定椭圆形状:</div>
              <div>• 对角矩阵 → 轴对齐</div>
              <div>• 非对角 → 旋转椭圆</div>
            </div>
            <div style={{ marginTop: 6, borderTop: '1px dashed rgba(255,255,255,0.1)', paddingTop: 4 }}>
              <span style={{ color: '#FFD700' }}>对比</span> 三种 Σ 的等高线
            </div>
          </div>
        </div>

        <div style={dividerStyle} />

        <div style={{ ...colStyle(1.5), minWidth: 260 }}>
          <div style={colLabelStyle}>解题过程</div>
          <style>{animCSS}</style>

          <div style={{ fontSize: 11, color: '#aaa', lineHeight: 1.7, marginBottom: 4 }}>
            <div className="mvg-f1">① Σ=I → 圆形等高线 (各向同性)</div>
            <div className="mvg-f2">② Σ 对角 → 轴对齐椭圆</div>
            <div className="mvg-f3">③ Σ 非对角 → 旋转椭圆 (有相关性)</div>
            <div className="mvg-done" style={conclusionStyle}>
              <span style={{ color: '#FFD700', fontWeight: 700 }}>∴</span> 协方差控制分布形状+朝向
            </div>
          </div>

          {/* 等高线对比图 */}
          <svg width={220} height={130} viewBox="0 0 220 130" style={{ display: 'block' }}>
            <line x1={20} y1={cy} x2={200} y2={cy} stroke="#ffffff10" strokeWidth={1} />
            <line x1={cx} y1={5} x2={cx} y2={125} stroke="#ffffff10" strokeWidth={1} />

            {shapes.map((s, i) => (
              <React.Fragment key={i}>
                <ellipse cx={cx} cy={cy} rx={s.rx} ry={s.ry}
                  fill="none" stroke={s.color} strokeWidth={1.5} opacity={0.6}
                  transform={`rotate(${s.rot} ${cx} ${cy})`}
                  className={`mvg-f${i + 1}`} />
                <ellipse cx={cx} cy={cy} rx={s.rx * 0.5} ry={s.ry * 0.5}
                  fill="none" stroke={s.color} strokeWidth={1} opacity={0.3}
                  transform={`rotate(${s.rot} ${cx} ${cy})`}
                  className={`mvg-f${i + 1}`} />
              </React.Fragment>
            ))}
            {/* 中心点 */}
            <circle cx={cx} cy={cy} r={3} fill="#FFD700" className="mvg-f1" />
            <text x={cx + 6} y={cy - 4} fill="#FFD700" fontSize={8} className="mvg-f1">μ</text>

            {/* 图例 */}
            {shapes.map((s, i) => (
              <text key={i} x={20} y={115 - i * 11} fill={s.color} fontSize={7} className={`mvg-f${i + 1}`}>
                ● {s.label}
              </text>
            ))}
          </svg>
        </div>
      </div>
    </div>
  )
}

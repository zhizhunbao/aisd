// ═══════════════════════════════════════════════════════════
// 梯度下降 (SGD) — 顶部公式 + 三栏: 解释 | 已知 | 解题过程
// ═══════════════════════════════════════════════════════════

import React from 'react'
import 'katex/dist/katex.min.css'
import { BlockMath, InlineMath } from 'react-katex'
import { colStyle, dividerStyle, colLabelStyle, givenLineStyle, boardStyle, conclusionStyle } from './boardStyles'

const LATEX = String.raw`\theta_{t+1} = \theta_t - \eta \nabla_\theta L(\theta_t)`
const COLOR = '#e74c3c'

const eta = 0.1
const steps = [
  { t: 0, theta: 5.0, grad: 4.0 },
  { t: 1, theta: 4.6, grad: 3.2 },
  { t: 2, theta: 4.28, grad: 2.56 },
]

const animCSS = `
  @keyframes slideR { from { opacity: 0; transform: translateX(-8px) } to { opacity: 1; transform: translateX(0) } }
  @keyframes fadeIn { from { opacity: 0 } to { opacity: 1 } }
  @keyframes pop { from { opacity: 0; transform: scale(0.6) } to { opacity: 1; transform: scale(1) } }
  .sgd-s1 { opacity: 0; animation: slideR 0.3s ease-out 0.1s forwards }
  .sgd-s2 { opacity: 0; animation: slideR 0.3s ease-out 0.4s forwards }
  .sgd-f1 { opacity: 0; animation: fadeIn 0.3s ease-out 0.2s forwards }
  .sgd-f2 { opacity: 0; animation: fadeIn 0.3s ease-out 0.5s forwards }
  .sgd-f3 { opacity: 0; animation: fadeIn 0.3s ease-out 0.8s forwards }
  .sgd-done { opacity: 0; animation: pop 0.3s ease-out 1.0s forwards }
`

// 模拟抛物线 Loss 曲线
const mapX = (v: number) => 20 + (v / 8) * 190
const mapY = (v: number) => 130 - (v / 20) * 110

export const SGDDiagram: React.FC<{ compact?: boolean }> = ({ compact }) => {
  if (compact) {
    return (
      <div style={{ textAlign: 'center', padding: '6px' }}>
        <div style={{ fontSize: 14, color: COLOR }}><BlockMath math={LATEX} /></div>
        <div style={{ color: '#888', fontSize: 9 }}>沿梯度反方向</div>
      </div>
    )
  }

  // Loss 曲线: L(θ) = (θ-2)²
  const curvePts: string[] = []
  for (let t = 0; t <= 8; t += 0.1) {
    const loss = (t - 2) ** 2
    curvePts.push(`${mapX(t).toFixed(1)},${mapY(loss).toFixed(1)}`)
  }

  return (
    <div style={{ padding: '8px 0' }}>
      <div style={{
        padding: '4px 8px', display: 'flex', alignItems: 'center', gap: 8,
        background: 'rgba(255,255,255,0.02)', borderRadius: '8px 8px 0 0',
        border: '1px solid rgba(255,255,255,0.06)', borderBottom: 'none',
      }}>
        <span style={{ fontSize: 14, color: '#fff', fontWeight: 700, whiteSpace: 'nowrap' }}>梯度下降</span>
        <div style={{ flex: 1, fontSize: 20, color: COLOR, textAlign: 'center' }}><BlockMath math={LATEX} /></div>
      </div>

      <div style={{ ...boardStyle, borderRadius: '0 0 8px 8px' }}>
        <div style={{ ...colStyle(1), minWidth: 150 }}>
          <div style={colLabelStyle}>解释</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
            <div>沿<b>梯度反方向</b>更新参数</div>
            <div style={{ marginTop: 6, color: '#aaa', fontSize: 11 }}>
              <div>• θ = 参数 (要优化的值)</div>
              <div>• η = 学习率 (步长大小)</div>
              <div>• ∇L = 梯度 (下坡方向)</div>
              <div>• 反复迭代直到收敛</div>
            </div>
            <div style={{ marginTop: 8, color: '#888', fontSize: 10 }}>
              所有深度学习的基石
            </div>
          </div>
        </div>

        <div style={dividerStyle} />

        <div style={{ ...colStyle(1), minWidth: 150 }}>
          <div style={colLabelStyle}>已知</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.6 }}>
            <div style={givenLineStyle}>
              <InlineMath math="L(\theta) = (\theta - 2)^2" />
            </div>
            <div style={givenLineStyle}>η = {eta} (学习率)</div>
            <div style={givenLineStyle}>θ₀ = 5.0 (初始值)</div>
            <div style={{ marginTop: 6, borderTop: '1px dashed rgba(255,255,255,0.1)', paddingTop: 4 }}>
              <span style={{ color: '#FFD700' }}>求</span> θ 如何接近最优值 2
            </div>
          </div>
        </div>

        <div style={dividerStyle} />

        <div style={{ ...colStyle(1.5), minWidth: 260 }}>
          <div style={colLabelStyle}>解题过程</div>
          <style>{animCSS}</style>

          <div className="sgd-s1" style={{ marginBottom: 4 }}>
            <div style={{ fontSize: 12, color: '#ddd', fontWeight: 700, marginBottom: 2 }}>
              迭代过程 <span style={{ color: '#888', fontWeight: 400, fontSize: 10 }}>— θ 逐步接近 2</span>
            </div>
            {steps.map((s, i) => (
              <div key={i} style={{ fontSize: 11, color: '#aaa', marginLeft: 8, lineHeight: 1.6 }}>
                t={s.t}: θ={s.theta} → θ-0.1×{s.grad} = <b style={{ color: COLOR }}>{(s.theta - eta * s.grad).toFixed(2)}</b>
              </div>
            ))}
          </div>

          <div className="sgd-done" style={{ ...conclusionStyle, marginBottom: 4 }}>
            <span style={{ color: '#FFD700', fontWeight: 700 }}>∴</span>{' '}
            <span style={{ color: '#ddd' }}>θ: 5.0 → 4.6 → 4.28 → ... → <b style={{ color: '#2ecc71' }}>2.0</b></span>
          </div>

          <svg width={220} height={140} viewBox="0 0 220 140" style={{ display: 'block' }}>
            <line x1={20} y1={130} x2={210} y2={130} stroke="#ffffff15" strokeWidth={1} />
            <polyline points={curvePts.join(' ')} fill="none" stroke="#ffffff20" strokeWidth={1.5} />
            {/* 标注步骤 */}
            {[{t: 5, loss: 9}, {t: 4.6, loss: 6.76}, {t: 4.28, loss: 5.2}].map((p, i) => (
              <React.Fragment key={i}>
                <circle cx={mapX(p.t)} cy={mapY(p.loss)} r={3} fill={COLOR} className={`sgd-f${i+1}`} />
                {i < 2 && (
                  <line x1={mapX(p.t)} y1={mapY(p.loss)}
                    x2={mapX(i === 0 ? 4.6 : 4.28)} y2={mapY(i === 0 ? 6.76 : 5.2)}
                    stroke={COLOR} strokeWidth={1.5} strokeDasharray="3 2" className={`sgd-f${i+2}`}
                    markerEnd="url(#sgdArr)" />
                )}
              </React.Fragment>
            ))}
            {/* 最优点 */}
            <circle cx={mapX(2)} cy={mapY(0)} r={4} fill="#2ecc71" className="sgd-f3" />
            <text x={mapX(2)} y={mapY(0) - 6} className="sgd-f3" fill="#2ecc71" fontSize={9} textAnchor="middle">最优</text>
            <defs>
              <marker id="sgdArr" markerWidth="6" markerHeight="4" refX="5" refY="2" orient="auto">
                <path d="M0,0 L6,2 L0,4" fill={COLOR} />
              </marker>
            </defs>
          </svg>
        </div>
      </div>
    </div>
  )
}

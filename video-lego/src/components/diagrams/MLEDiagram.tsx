// ═══════════════════════════════════════════════════════════
// 最大似然估计 — 顶部公式 + 三栏: 解释 | 已知 | 解题过程
// ═══════════════════════════════════════════════════════════

import React from 'react'
import 'katex/dist/katex.min.css'
import { BlockMath, InlineMath } from 'react-katex'
import { colStyle, dividerStyle, colLabelStyle, boardStyle, conclusionStyle } from './boardStyles'

const LATEX = String.raw`\hat{\theta}_{MLE} = \arg\max_\theta \sum_{i=1}^{n} \log p(x_i | \theta)`
const COLOR = '#e74c3c'

const animCSS = `
  @keyframes fadeIn { from { opacity: 0 } to { opacity: 1 } }
  @keyframes pop { from { opacity: 0; transform: scale(0.6) } to { opacity: 1; transform: scale(1) } }
  .mle-f1 { opacity: 0; animation: fadeIn 0.3s ease-out 0.2s forwards }
  .mle-f2 { opacity: 0; animation: fadeIn 0.3s ease-out 0.5s forwards }
  .mle-f3 { opacity: 0; animation: fadeIn 0.3s ease-out 0.8s forwards }
  .mle-done { opacity: 0; animation: pop 0.3s ease-out 1.1s forwards }
`

// 似然函数曲线: L(θ) = Π p(xi|θ)  → log-likelihood 有一个峰值
const mapX = (v: number) => 20 + (v / 1) * 180
const mapY = (v: number) => 120 - (v + 5) * 16

export const MLEDiagram: React.FC<{ compact?: boolean }> = ({ compact }) => {
  if (compact) {
    return (
      <div style={{ textAlign: 'center', padding: '6px' }}>
        <div style={{ fontSize: 13, color: COLOR }}><BlockMath math={String.raw`\hat{\theta} = \arg\max_\theta \log L`} /></div>
        <div style={{ color: '#888', fontSize: 9 }}>找最大似然参数</div>
      </div>
    )
  }

  // log-likelihood 曲线: 高斯形状的 -( θ-0.5 )² * 8 - 1
  const curvePts: string[] = []
  let peakX = 0, peakY = -Infinity
  for (let t = 0; t <= 1; t += 0.01) {
    const ll = -((t - 0.5) ** 2) * 8 - 1
    const px = mapX(t), py = mapY(ll)
    curvePts.push(`${px.toFixed(1)},${py.toFixed(1)}`)
    if (ll > peakY) { peakY = ll; peakX = px }
  }

  return (
    <div style={{ padding: '8px 0' }}>
      <div style={{
        padding: '4px 8px', display: 'flex', alignItems: 'center', gap: 8,
        background: 'rgba(255,255,255,0.02)', borderRadius: '8px 8px 0 0',
        border: '1px solid rgba(255,255,255,0.06)', borderBottom: 'none',
      }}>
        <span style={{ fontSize: 14, color: '#fff', fontWeight: 700, whiteSpace: 'nowrap' }}>最大似然估计</span>
        <div style={{ flex: 1, fontSize: 16, color: COLOR, textAlign: 'center' }}><BlockMath math={LATEX} /></div>
      </div>

      <div style={{ ...boardStyle, borderRadius: '0 0 8px 8px' }}>
        <div style={{ ...colStyle(1), minWidth: 150 }}>
          <div style={colLabelStyle}>解释</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
            <div>找使数据出现<b>概率最大</b>的参数</div>
            <div style={{ marginTop: 6, color: '#aaa', fontSize: 11 }}>
              <div>• "数据告诉我参数该是多少"</div>
              <div>• log 把乘法变加法</div>
              <div>• 逻辑回归/神经网络的训练目标</div>
              <div>• 本质: 令 ∂logL/∂θ = 0</div>
            </div>
          </div>
        </div>

        <div style={dividerStyle} />

        <div style={{ ...colStyle(1), minWidth: 140 }}>
          <div style={colLabelStyle}>已知</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.6 }}>
            <div>抛硬币 n=10 次</div>
            <div>正面 k=7 次</div>
            <div style={{ marginTop: 6 }}><InlineMath math="p(x_i|\theta) = \theta^{x_i}(1-\theta)^{1-x_i}" /></div>
            <div style={{ marginTop: 6, borderTop: '1px dashed rgba(255,255,255,0.1)', paddingTop: 4 }}>
              <span style={{ color: '#FFD700' }}>求</span> θ̂<sub>MLE</sub>
            </div>
          </div>
        </div>

        <div style={dividerStyle} />

        <div style={{ ...colStyle(1.5), minWidth: 260 }}>
          <div style={colLabelStyle}>解题过程</div>
          <style>{animCSS}</style>

          <div style={{ fontSize: 11, color: '#aaa', lineHeight: 1.7, marginBottom: 4 }}>
            <div className="mle-f1">① log L = 7·log θ + 3·log(1-θ)</div>
            <div className="mle-f2">② ∂/∂θ = 7/θ - 3/(1-θ) = 0</div>
            <div className="mle-f3">③ θ = 7/(7+3)</div>
            <div className="mle-done" style={conclusionStyle}>
              <span style={{ color: '#FFD700', fontWeight: 700 }}>∴</span>{' '}
              θ̂ = <b style={{ color: '#2ecc71' }}>0.7</b> (就是频率!)
            </div>
          </div>

          {/* log-likelihood 曲线 */}
          <svg width={220} height={130} viewBox="0 0 220 130" style={{ display: 'block' }}>
            <line x1={20} y1={120} x2={200} y2={120} stroke="#ffffff15" strokeWidth={1} />
            <text x={200} y={118} fill="#666" fontSize={7}>θ</text>
            <text x={12} y={20} fill="#666" fontSize={7}>log L</text>
            <polyline points={curvePts.join(' ')} fill="none" stroke={COLOR} strokeWidth={2} className="mle-f1" />
            {/* MLE 峰点 */}
            <circle cx={peakX} cy={mapY(-1)} r={4} fill="#2ecc71" className="mle-done" />
            <line x1={peakX} y1={mapY(-1)} x2={peakX} y2={120} stroke="#2ecc7140" strokeWidth={1} strokeDasharray="3 2" className="mle-f3" />
            <text x={peakX} y={mapY(-1) - 8} fill="#2ecc71" fontSize={9} textAnchor="middle" fontWeight={700} className="mle-done">θ̂=0.7</text>
            {/* θ 刻度 */}
            <text x={mapX(0)} y={130} fill="#888" fontSize={7} textAnchor="middle">0</text>
            <text x={mapX(0.5)} y={130} fill="#888" fontSize={7} textAnchor="middle">0.5</text>
            <text x={mapX(1)} y={130} fill="#888" fontSize={7} textAnchor="middle">1</text>
          </svg>
        </div>
      </div>
    </div>
  )
}

// ═══════════════════════════════════════════════════════════
// MSE (均方误差) — 顶部公式 + 三栏: 解释 | 已知 | 解题过程
// ═══════════════════════════════════════════════════════════

import React from 'react'
import 'katex/dist/katex.min.css'
import { BlockMath, InlineMath } from 'react-katex'
import { colStyle, dividerStyle, colLabelStyle, boardStyle, conclusionStyle } from './boardStyles'

const LATEX = String.raw`\text{MSE} = \frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2`
const COLOR = '#e67e22'

const data = [
  { y: 3, yhat: 2.5 },
  { y: 5, yhat: 4.8 },
  { y: 2, yhat: 3.0 },
  { y: 7, yhat: 6.5 },
]
const errors = data.map(d => (d.y - d.yhat) ** 2)
const mse = errors.reduce((a, b) => a + b, 0) / data.length

const animCSS = `
  @keyframes slideR { from { opacity: 0; transform: translateX(-8px) } to { opacity: 1; transform: translateX(0) } }
  @keyframes expand { from { transform: scaleX(0) } to { transform: scaleX(1) } }
  @keyframes pop { from { opacity: 0; transform: scale(0.6) } to { opacity: 1; transform: scale(1) } }
  .mse-s1 { opacity: 0; animation: slideR 0.3s ease-out 0.1s forwards }
  .mse-s2 { opacity: 0; animation: slideR 0.3s ease-out 0.4s forwards }
  .mse-bar { transform-origin: left; animation: expand 0.4s ease-out 0.6s both }
  .mse-done { opacity: 0; animation: pop 0.3s ease-out 0.9s forwards }
`

export const MSEDiagram: React.FC<{ compact?: boolean }> = ({ compact }) => {
  if (compact) {
    return (
      <div style={{ textAlign: 'center', padding: '6px' }}>
        <div style={{ fontSize: 14, color: COLOR }}><BlockMath math={LATEX} /></div>
        <div style={{ color: '#888', fontSize: 9 }}>预测偏差</div>
      </div>
    )
  }

  const barMaxW = 100

  return (
    <div style={{ padding: '8px 0' }}>
      <div style={{
        padding: '4px 8px', display: 'flex', alignItems: 'center', gap: 8,
        background: 'rgba(255,255,255,0.02)', borderRadius: '8px 8px 0 0',
        border: '1px solid rgba(255,255,255,0.06)', borderBottom: 'none',
      }}>
        <span style={{ fontSize: 14, color: '#fff', fontWeight: 700, whiteSpace: 'nowrap' }}>均方误差</span>
        <div style={{ flex: 1, fontSize: 20, color: COLOR, textAlign: 'center' }}><BlockMath math={LATEX} /></div>
      </div>

      <div style={{ ...boardStyle, borderRadius: '0 0 8px 8px' }}>
        <div style={{ ...colStyle(1), minWidth: 150 }}>
          <div style={colLabelStyle}>解释</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
            <div>预测值与真实值的<b>平均平方偏差</b></div>
            <div style={{ marginTop: 6, color: '#aaa', fontSize: 11 }}>
              <div>• 平方: 放大大误差</div>
              <div>• 求平均: 不受样本量影响</div>
              <div>• MSE = 0 表示完美预测</div>
              <div>• 回归任务最常用损失</div>
            </div>
          </div>
        </div>

        <div style={dividerStyle} />

        <div style={{ ...colStyle(1), minWidth: 140 }}>
          <div style={colLabelStyle}>已知</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.6 }}>
            <div>n = {data.length} 个样本</div>
            <div style={{ marginTop: 4 }}>
              {data.map((d, i) => (
                <div key={i} style={{ fontSize: 11 }}>
                  <span style={{ color: '#4ea8de' }}>y{'\u2081\u2082\u2083\u2084'[i]}={d.y}</span>
                  <span style={{ color: '#888' }}>, </span>
                  <span style={{ color: COLOR }}>ŷ{'\u2081\u2082\u2083\u2084'[i]}={d.yhat}</span>
                </div>
              ))}
            </div>
            <div style={{ marginTop: 6, borderTop: '1px dashed rgba(255,255,255,0.1)', paddingTop: 4 }}>
              <span style={{ color: '#FFD700' }}>求</span> MSE = ?
            </div>
          </div>
        </div>

        <div style={dividerStyle} />

        <div style={{ ...colStyle(1.5), minWidth: 260 }}>
          <div style={colLabelStyle}>解题过程</div>
          <style>{animCSS}</style>

          <div className="mse-s1" style={{ marginBottom: 6 }}>
            <div style={{ fontSize: 12, color: '#ddd', fontWeight: 700 }}>
              ① 每项 (y - ŷ)²
            </div>
            {data.map((d, i) => (
              <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 6, marginLeft: 8, marginTop: 3 }}>
                <span style={{ fontSize: 10, color: '#aaa', width: 100 }}>
                  ({d.y}-{d.yhat})² = {errors[i].toFixed(2)}
                </span>
                <div className="mse-bar" style={{
                  width: (errors[i] / Math.max(...errors)) * barMaxW, height: 10,
                  background: COLOR, borderRadius: 3, opacity: 0.5 + (errors[i] / Math.max(...errors)) * 0.5,
                }} />
              </div>
            ))}
          </div>

          <div className="mse-s2" style={{ marginBottom: 6 }}>
            <div style={{ fontSize: 12, color: '#ddd', fontWeight: 700 }}>② 求平均</div>
            <div style={{ fontSize: 11, color: '#aaa', marginLeft: 8 }}>
              ({errors.map(e => e.toFixed(2)).join(' + ')}) / {data.length}
            </div>
          </div>

          <div className="mse-done" style={conclusionStyle}>
            <span style={{ color: '#FFD700', fontWeight: 700 }}>∴</span>{' '}
            MSE = <b style={{ color: '#FFD700' }}>{mse.toFixed(4)}</b>
            <div style={{ color: '#888', fontSize: 10 }}>
              最大误差来源: 第3项 (偏差1.0)
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

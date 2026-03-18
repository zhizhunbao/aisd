// ═══════════════════════════════════════════════════════════
// 贝叶斯定理 — 顶部公式 + 三栏: 解释 | 已知 | 解题过程
// ═══════════════════════════════════════════════════════════

import React from 'react'
import 'katex/dist/katex.min.css'
import { BlockMath, InlineMath } from 'react-katex'
import { colStyle, dividerStyle, colLabelStyle, givenLineStyle, boardStyle, conclusionStyle } from './boardStyles'

const LATEX = String.raw`P(A|B) = \frac{P(B|A) \cdot P(A)}{P(B)}`
const COLOR = '#3498db'

// 例子: 检测阳性，实际患病的概率
const pDisease = 0.01      // 患病率 P(A)
const pPosGivenDis = 0.95  // 灵敏度 P(B|A)
const pPosGivenNot = 0.05  // 假阳性率 P(B|¬A)
const pPos = pPosGivenDis * pDisease + pPosGivenNot * (1 - pDisease) // P(B)
const pDisGivenPos = (pPosGivenDis * pDisease) / pPos // P(A|B)

const animCSS = `
  @keyframes slideR { from { opacity: 0; transform: translateX(-8px) } to { opacity: 1; transform: translateX(0) } }
  @keyframes pop { from { opacity: 0; transform: scale(0.6) } to { opacity: 1; transform: scale(1) } }
  .bay-s1 { opacity: 0; animation: slideR 0.3s ease-out 0.1s forwards }
  .bay-s2 { opacity: 0; animation: slideR 0.3s ease-out 0.4s forwards }
  .bay-s3 { opacity: 0; animation: slideR 0.3s ease-out 0.7s forwards }
  .bay-done { opacity: 0; animation: pop 0.3s ease-out 1.0s forwards }
`

export const BayesDiagram: React.FC<{ compact?: boolean }> = ({ compact }) => {
  if (compact) {
    return (
      <div style={{ textAlign: 'center', padding: '6px' }}>
        <div style={{ fontSize: 14, color: COLOR }}><BlockMath math={LATEX} /></div>
        <div style={{ color: '#888', fontSize: 9 }}>更新信念</div>
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
        <span style={{ fontSize: 14, color: '#fff', fontWeight: 700, whiteSpace: 'nowrap' }}>贝叶斯定理</span>
        <div style={{ flex: 1, fontSize: 20, color: COLOR, textAlign: 'center' }}><BlockMath math={LATEX} /></div>
      </div>

      <div style={{ ...boardStyle, borderRadius: '0 0 8px 8px' }}>
        <div style={{ ...colStyle(1), minWidth: 150 }}>
          <div style={colLabelStyle}>解释</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
            <div>根据<b>新证据</b>更新<b>原有信念</b></div>
            <div style={{ marginTop: 6, color: '#aaa', fontSize: 11 }}>
              <div>• P(A) = 先验 (之前相信多少)</div>
              <div>• P(B|A) = 似然 (证据有多强)</div>
              <div>• P(A|B) = 后验 (更新后的信念)</div>
              <div>• P(B) = 边际 (证据出现概率)</div>
            </div>
          </div>
        </div>

        <div style={dividerStyle} />

        <div style={{ ...colStyle(1), minWidth: 160 }}>
          <div style={colLabelStyle}>已知</div>
          <div style={{ fontSize: 11, color: '#ccc', lineHeight: 1.6 }}>
            <div style={{ fontWeight: 700, color: '#FFD700', marginBottom: 4 }}>场景: 医学检测</div>
            <div style={{ ...givenLineStyle, fontSize: 11 }}>A = 患病, B = 检测阳性</div>
            <div style={{ ...givenLineStyle, fontSize: 11 }}>P(A) = {pDisease} (患病率1%)</div>
            <div style={{ ...givenLineStyle, fontSize: 11 }}>P(B|A) = {pPosGivenDis} (灵敏度95%)</div>
            <div style={{ ...givenLineStyle, fontSize: 11 }}>P(B|¬A) = {pPosGivenNot} (假阳性5%)</div>
            <div style={{ marginTop: 6, borderTop: '1px dashed rgba(255,255,255,0.1)', paddingTop: 4 }}>
              <span style={{ color: '#FFD700' }}>求</span>{' '}
              <InlineMath math="P(A|B)" /> = ?
            </div>
          </div>
        </div>

        <div style={dividerStyle} />

        <div style={{ ...colStyle(1.5), minWidth: 260 }}>
          <div style={colLabelStyle}>解题过程</div>
          <style>{animCSS}</style>

          <div className="bay-s1" style={{ marginBottom: 6 }}>
            <div style={{ fontSize: 12, color: '#ddd', fontWeight: 700 }}>
              ① 求 P(B) <span style={{ color: '#888', fontWeight: 400, fontSize: 10 }}>— 全概率公式</span>
            </div>
            <div style={{ fontSize: 11, color: '#aaa', marginLeft: 8 }}>
              P(B) = 0.95×0.01 + 0.05×0.99 = <b style={{ color: '#fff' }}>{pPos.toFixed(4)}</b>
            </div>
          </div>

          <div className="bay-s2" style={{ marginBottom: 6 }}>
            <div style={{ fontSize: 12, color: '#ddd', fontWeight: 700 }}>
              ② 代入公式
            </div>
            <div style={{ fontSize: 11, color: '#aaa', marginLeft: 8 }}>
              P(A|B) = (0.95 × 0.01) / {pPos.toFixed(4)}
            </div>
          </div>

          <div className="bay-s3" style={{ marginBottom: 6 }}>
            <div style={{ fontSize: 12, color: '#ddd', fontWeight: 700 }}>③ 计算</div>
            <div style={{ fontSize: 11, color: '#aaa', marginLeft: 8 }}>
              = 0.0095 / {pPos.toFixed(4)} = <b style={{ color: COLOR }}>{pDisGivenPos.toFixed(4)}</b>
            </div>
          </div>

          <div className="bay-done" style={conclusionStyle}>
            <span style={{ color: '#FFD700', fontWeight: 700 }}>∴</span>{' '}
            <span style={{ color: '#ddd' }}>
              阳性后实际患病概率仅 <b style={{ color: '#e74c3c' }}>{(pDisGivenPos * 100).toFixed(1)}%</b>
            </span>
            <div style={{ color: '#888', fontSize: 10 }}>
              直觉: 1%患病率太低，即使检测准确，多数阳性仍是假阳性
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

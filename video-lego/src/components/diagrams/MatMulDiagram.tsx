// ═══════════════════════════════════════════════════════════
// 矩阵乘法 Matrix Multiply
// ═══════════════════════════════════════════════════════════

import React from 'react'
import 'katex/dist/katex.min.css'
import { BlockMath } from 'react-katex'
import { colStyle, dividerStyle, colLabelStyle, boardStyle, conclusionStyle } from './boardStyles'

const LATEX = String.raw`(AB)_{ij} = \sum_{k=1}^{n} a_{ik} b_{kj}`
const COLOR = '#e67e22'

const animCSS = `
  @keyframes fadeIn { from { opacity: 0 } to { opacity: 1 } }
  .mm-f1 { opacity: 0; animation: fadeIn 0.3s ease-out 0.2s forwards }
  .mm-f2 { opacity: 0; animation: fadeIn 0.3s ease-out 0.5s forwards }
  .mm-f3 { opacity: 0; animation: fadeIn 0.3s ease-out 0.8s forwards }
`

export const MatMulDiagram: React.FC<{ compact?: boolean }> = ({ compact }) => {
  if (compact) return (
    <div style={{ textAlign: 'center', padding: '6px' }}>
      <div style={{ fontSize: 14, color: COLOR }}><BlockMath math={LATEX} /></div>
      <div style={{ color: '#888', fontSize: 9 }}>行×列求和</div>
    </div>
  )

  const cell = (v: string, bg: string, delay: string) => (
    <div className={delay} style={{ width: 28, height: 22, display: 'flex', alignItems: 'center', justifyContent: 'center', border: '1px solid rgba(255,255,255,0.15)', background: bg, fontSize: 11, color: '#fff', borderRadius: 2 }}>{v}</div>
  )

  return (
    <div style={{ padding: '8px 0' }}>
      <div style={{ padding: '4px 8px', display: 'flex', alignItems: 'center', gap: 8, background: 'rgba(255,255,255,0.02)', borderRadius: '8px 8px 0 0', border: '1px solid rgba(255,255,255,0.06)', borderBottom: 'none' }}>
        <span style={{ fontSize: 14, color: '#fff', fontWeight: 700, whiteSpace: 'nowrap' }}>矩阵乘法</span>
        <div style={{ flex: 1, fontSize: 20, color: COLOR, textAlign: 'center' }}><BlockMath math={LATEX} /></div>
      </div>
      <div style={{ ...boardStyle, borderRadius: '0 0 8px 8px' }}>
        <div style={{ ...colStyle(1), minWidth: 150 }}>
          <div style={colLabelStyle}>解释</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
            <div>A的<b>行</b> × B的<b>列</b> → 对应位置的值</div>
            <div style={{ marginTop: 6, color: '#aaa', fontSize: 11 }}>
              <div>• 全连接层: y = Wx + b</div>
              <div>• Transformer: Q·K^T</div>
              <div>• 线性变换的基本运算</div>
              <div>• A(m×n) × B(n×p) = C(m×p)</div>
            </div>
          </div>
        </div>
        <div style={dividerStyle} />
        <div style={{ ...colStyle(1), minWidth: 140 }}>
          <div style={colLabelStyle}>已知</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
            <div style={{ display: 'flex', gap: 2 }}>A = {cell('1', `${COLOR}30`, 'mm-f1')}{cell('2', `${COLOR}30`, 'mm-f1')}</div>
            <div style={{ display: 'flex', gap: 2, marginTop: 2 }}>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{cell('3', `${COLOR}15`, 'mm-f1')}{cell('4', `${COLOR}15`, 'mm-f1')}</div>
            <div style={{ marginTop: 8 }}>
              <div style={{ display: 'flex', gap: 2 }}>B = {cell('5', '#3498db30', 'mm-f1')}{cell('6', '#3498db15', 'mm-f1')}</div>
              <div style={{ display: 'flex', gap: 2, marginTop: 2 }}>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{cell('7', '#3498db30', 'mm-f1')}{cell('8', '#3498db15', 'mm-f1')}</div>
            </div>
          </div>
        </div>
        <div style={dividerStyle} />
        <div style={{ ...colStyle(1.3), minWidth: 240 }}>
          <div style={colLabelStyle}>解题过程</div>
          <style>{animCSS}</style>
          <div style={{ fontSize: 11, color: '#aaa', lineHeight: 1.7 }}>
            <div className="mm-f1">① C₁₁ = 1×5 + 2×7 = 5+14 = <b style={{color:COLOR}}>19</b></div>
            <div className="mm-f2">② C₁₂ = 1×6 + 2×8 = 6+16 = <b style={{color:COLOR}}>22</b></div>
            <div className="mm-f2">③ C₂₁ = 3×5 + 4×7 = 15+28 = <b style={{color:COLOR}}>43</b></div>
            <div className="mm-f3">④ C₂₂ = 3×6 + 4×8 = 18+32 = <b style={{color:COLOR}}>50</b></div>
            <div className="mm-f3" style={conclusionStyle}>
              <span style={{ color: '#FFD700', fontWeight: 700 }}>∴</span> C = [[19,22],[43,50]]
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

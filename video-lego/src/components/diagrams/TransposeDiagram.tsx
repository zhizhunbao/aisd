// ═══════════════════════════════════════════════════════════
// 矩阵转置 Transpose
// ═══════════════════════════════════════════════════════════

import React from 'react'
import 'katex/dist/katex.min.css'
import { BlockMath } from 'react-katex'
import { colStyle, dividerStyle, colLabelStyle, boardStyle, conclusionStyle } from './boardStyles'

const LATEX = String.raw`(A^T)_{ij} = A_{ji}`
const COLOR = '#1abc9c'

const animCSS = `
  @keyframes fadeIn { from { opacity: 0 } to { opacity: 1 } }
  .tp-f1 { opacity: 0; animation: fadeIn 0.3s ease-out 0.2s forwards }
  .tp-f2 { opacity: 0; animation: fadeIn 0.3s ease-out 0.6s forwards }
  .tp-f3 { opacity: 0; animation: fadeIn 0.3s ease-out 1.0s forwards }
`

export const TransposeDiagram: React.FC<{ compact?: boolean }> = ({ compact }) => {
  if (compact) return (
    <div style={{ textAlign: 'center', padding: '6px' }}>
      <div style={{ fontSize: 14, color: COLOR }}><BlockMath math={LATEX} /></div>
      <div style={{ color: '#888', fontSize: 9 }}>行列互换</div>
    </div>
  )

  const cell = (v: string, bg: string, cls: string) => (
    <div className={cls} style={{ width: 28, height: 22, display: 'flex', alignItems: 'center', justifyContent: 'center', border: '1px solid rgba(255,255,255,0.15)', background: bg, fontSize: 11, color: '#fff', borderRadius: 2 }}>{v}</div>
  )

  return (
    <div style={{ padding: '8px 0' }}>
      <div style={{ padding: '4px 8px', display: 'flex', alignItems: 'center', gap: 8, background: 'rgba(255,255,255,0.02)', borderRadius: '8px 8px 0 0', border: '1px solid rgba(255,255,255,0.06)', borderBottom: 'none' }}>
        <span style={{ fontSize: 14, color: '#fff', fontWeight: 700, whiteSpace: 'nowrap' }}>矩阵转置</span>
        <div style={{ flex: 1, fontSize: 20, color: COLOR, textAlign: 'center' }}><BlockMath math={LATEX} /></div>
      </div>
      <div style={{ ...boardStyle, borderRadius: '0 0 8px 8px' }}>
        <div style={{ ...colStyle(1), minWidth: 150 }}>
          <div style={colLabelStyle}>解释</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
            <div><b>行</b>变<b>列</b>，列变行</div>
            <div style={{ marginTop: 6, color: '#aaa', fontSize: 11 }}>
              <div>• 第 i 行 → 第 i 列</div>
              <div>• (m×n) → (n×m)</div>
              <div>• 反向传播必用</div>
              <div>• (AB)ᵀ = BᵀAᵀ</div>
            </div>
          </div>
        </div>
        <div style={dividerStyle} />
        <div style={{ ...colStyle(1.5), minWidth: 200 }}>
          <div style={colLabelStyle}>已知 → 结果</div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <div>
              <div style={{ fontSize: 10, color: '#888', marginBottom: 4 }}>A (2×3)</div>
              <div style={{ display: 'flex', gap: 2 }}>{cell('1','#e74c3c30','tp-f1')}{cell('2',`${COLOR}30`,'tp-f1')}{cell('3','#3498db30','tp-f1')}</div>
              <div style={{ display: 'flex', gap: 2, marginTop: 2 }}>{cell('4','#e74c3c15','tp-f1')}{cell('5',`${COLOR}15`,'tp-f1')}{cell('6','#3498db15','tp-f1')}</div>
            </div>
            <span className="tp-f2" style={{ fontSize: 18, color: '#FFD700' }}>→</span>
            <div>
              <div style={{ fontSize: 10, color: '#888', marginBottom: 4 }}>Aᵀ (3×2)</div>
              <div style={{ display: 'flex', gap: 2 }}>{cell('1','#e74c3c30','tp-f2')}{cell('4','#e74c3c15','tp-f2')}</div>
              <div style={{ display: 'flex', gap: 2, marginTop: 2 }}>{cell('2',`${COLOR}30`,'tp-f2')}{cell('5',`${COLOR}15`,'tp-f2')}</div>
              <div style={{ display: 'flex', gap: 2, marginTop: 2 }}>{cell('3','#3498db30','tp-f2')}{cell('6','#3498db15','tp-f2')}</div>
            </div>
          </div>
        </div>
        <div style={dividerStyle} />
        <div style={{ ...colStyle(1), minWidth: 160 }}>
          <div style={colLabelStyle}>解题过程</div>
          <style>{animCSS}</style>
          <div style={{ fontSize: 11, color: '#aaa', lineHeight: 1.7 }}>
            <div className="tp-f1">① 第1行[1,2,3] → 第1列</div>
            <div className="tp-f2">② 第2行[4,5,6] → 第2列</div>
            <div className="tp-f3" style={conclusionStyle}>
              <span style={{ color: '#FFD700', fontWeight: 700 }}>∴</span> 沿对角线翻折
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

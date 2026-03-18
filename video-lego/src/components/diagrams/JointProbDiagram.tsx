// ═══════════════════════════════════════════════════════════
// 联合概率 — 顶部公式 + 三栏: 解释 | 已知 | 解题过程
// ═══════════════════════════════════════════════════════════

import React from 'react'
import 'katex/dist/katex.min.css'
import { BlockMath } from 'react-katex'
import { colStyle, dividerStyle, colLabelStyle, boardStyle, conclusionStyle } from './boardStyles'

const LATEX = String.raw`P(A \cap B) = P(A|B) \cdot P(B)`
const COLOR = '#27ae60'

const animCSS = `
  @keyframes fadeIn { from { opacity: 0 } to { opacity: 1 } }
  @keyframes pop { from { opacity: 0; transform: scale(0.6) } to { opacity: 1; transform: scale(1) } }
  .jp-f1 { opacity: 0; animation: fadeIn 0.3s ease-out 0.2s forwards }
  .jp-f2 { opacity: 0; animation: fadeIn 0.3s ease-out 0.5s forwards }
  .jp-f3 { opacity: 0; animation: fadeIn 0.3s ease-out 0.8s forwards }
  .jp-done { opacity: 0; animation: pop 0.3s ease-out 1.0s forwards }
`

export const JointProbDiagram: React.FC<{ compact?: boolean }> = ({ compact }) => {
  if (compact) {
    return (
      <div style={{ textAlign: 'center', padding: '6px' }}>
        <div style={{ fontSize: 14, color: COLOR }}><BlockMath math={LATEX} /></div>
        <div style={{ color: '#888', fontSize: 9 }}>两事件同时发生</div>
      </div>
    )
  }

  // Venn 图
  const cx1 = 85, cx2 = 135, cy = 60, r = 38

  return (
    <div style={{ padding: '8px 0' }}>
      <div style={{
        padding: '4px 8px', display: 'flex', alignItems: 'center', gap: 8,
        background: 'rgba(255,255,255,0.02)', borderRadius: '8px 8px 0 0',
        border: '1px solid rgba(255,255,255,0.06)', borderBottom: 'none',
      }}>
        <span style={{ fontSize: 14, color: '#fff', fontWeight: 700, whiteSpace: 'nowrap' }}>联合概率</span>
        <div style={{ flex: 1, fontSize: 20, color: COLOR, textAlign: 'center' }}><BlockMath math={LATEX} /></div>
      </div>

      <div style={{ ...boardStyle, borderRadius: '0 0 8px 8px' }}>
        <div style={{ ...colStyle(1), minWidth: 150 }}>
          <div style={colLabelStyle}>解释</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
            <div>两事件<b>同时发生</b>的概率</div>
            <div style={{ marginTop: 6, color: '#aaa', fontSize: 11 }}>
              <div>• A∩B = 交集区域</div>
              <div>• 独立时: P(A∩B) = P(A)·P(B)</div>
              <div>• 朴素贝叶斯的核心假设</div>
              <div>• 条件概率的分子</div>
            </div>
          </div>
        </div>

        <div style={dividerStyle} />

        <div style={{ ...colStyle(1), minWidth: 140 }}>
          <div style={colLabelStyle}>已知</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.6 }}>
            <div>P(下雨) = 0.3</div>
            <div>P(带伞|下雨) = 0.9</div>
            <div style={{ marginTop: 6, borderTop: '1px dashed rgba(255,255,255,0.1)', paddingTop: 4 }}>
              <span style={{ color: '#FFD700' }}>求</span> P(下雨 ∩ 带伞)
            </div>
          </div>
        </div>

        <div style={dividerStyle} />

        <div style={{ ...colStyle(1.3), minWidth: 240 }}>
          <div style={colLabelStyle}>解题过程</div>
          <style>{animCSS}</style>

          <div style={{ fontSize: 11, color: '#aaa', lineHeight: 1.7, marginBottom: 4 }}>
            <div className="jp-f1">① P(A|B) · P(B) = 0.9 × 0.3</div>
            <div className="jp-f2">② = <b style={{ color: COLOR }}>0.27</b></div>
            <div className="jp-done" style={conclusionStyle}>
              <span style={{ color: '#FFD700', fontWeight: 700 }}>∴</span> P(雨∩伞) = 27%
            </div>
          </div>

          {/* Venn 图 */}
          <svg width={220} height={120} viewBox="0 0 220 120" style={{ display: 'block' }}>
            {/* 样本空间 */}
            <rect x={20} y={10} width={180} height={100} rx={8} fill="none" stroke="#ffffff15" strokeWidth={1} />
            <text x={25} y={22} fill="#666" fontSize={8}>S (样本空间)</text>
            {/* A 圆 */}
            <circle cx={cx1} cy={cy} r={r} fill="#3498db15" stroke="#3498db50" strokeWidth={1.5} className="jp-f1" />
            <text x={cx1 - 20} y={cy + 3} fill="#3498db80" fontSize={10} className="jp-f1">A</text>
            {/* B 圆 */}
            <circle cx={cx2} cy={cy} r={r} fill={`${COLOR}15`} stroke={`${COLOR}50`} strokeWidth={1.5} className="jp-f1" />
            <text x={cx2 + 12} y={cy + 3} fill={`${COLOR}80`} fontSize={10} className="jp-f1">B</text>
            {/* 交集高亮 */}
            <clipPath id="clipA"><circle cx={cx1} cy={cy} r={r} /></clipPath>
            <circle cx={cx2} cy={cy} r={r} fill={`${COLOR}40`} clipPath="url(#clipA)" className="jp-f2" />
            <text x={(cx1 + cx2) / 2} y={cy + 4} fill="#fff" fontSize={9} fontWeight={700} textAnchor="middle" className="jp-f3">A∩B</text>
          </svg>
        </div>
      </div>
    </div>
  )
}

// ═══════════════════════════════════════════════════════════
// 全概率公式 — 顶部公式 + 三栏: 解释 | 已知 | 解题过程
// ═══════════════════════════════════════════════════════════

import React from 'react'
import 'katex/dist/katex.min.css'
import { BlockMath } from 'react-katex'
import { colStyle, dividerStyle, colLabelStyle, boardStyle, conclusionStyle } from './boardStyles'

const LATEX = String.raw`P(A) = \sum_{i} P(A|B_i) P(B_i)`
const COLOR = '#4ea8de'

const animCSS = `
  @keyframes fadeIn { from { opacity: 0 } to { opacity: 1 } }
  @keyframes pop { from { opacity: 0; transform: scale(0.6) } to { opacity: 1; transform: scale(1) } }
  .tp-f1 { opacity: 0; animation: fadeIn 0.3s ease-out 0.2s forwards }
  .tp-f2 { opacity: 0; animation: fadeIn 0.3s ease-out 0.5s forwards }
  .tp-f3 { opacity: 0; animation: fadeIn 0.3s ease-out 0.8s forwards }
  .tp-done { opacity: 0; animation: pop 0.3s ease-out 1.1s forwards }
`

export const TotalProbDiagram: React.FC<{ compact?: boolean }> = ({ compact }) => {
  if (compact) {
    return (
      <div style={{ textAlign: 'center', padding: '6px' }}>
        <div style={{ fontSize: 14, color: COLOR }}><BlockMath math={LATEX} /></div>
        <div style={{ color: '#888', fontSize: 9 }}>按所有路径加总</div>
      </div>
    )
  }

  // 树形图: 两个分支 B1, B2，各有 A 和 ¬A
  const parts = [
    { label: 'B₁', p: 0.4, pa: 0.7, color: '#e67e22' },
    { label: 'B₂', p: 0.35, pa: 0.3, color: '#3498db' },
    { label: 'B₃', p: 0.25, pa: 0.5, color: '#2ecc71' },
  ]

  return (
    <div style={{ padding: '8px 0' }}>
      <div style={{
        padding: '4px 8px', display: 'flex', alignItems: 'center', gap: 8,
        background: 'rgba(255,255,255,0.02)', borderRadius: '8px 8px 0 0',
        border: '1px solid rgba(255,255,255,0.06)', borderBottom: 'none',
      }}>
        <span style={{ fontSize: 14, color: '#fff', fontWeight: 700, whiteSpace: 'nowrap' }}>全概率公式</span>
        <div style={{ flex: 1, fontSize: 20, color: COLOR, textAlign: 'center' }}><BlockMath math={LATEX} /></div>
      </div>

      <div style={{ ...boardStyle, borderRadius: '0 0 8px 8px' }}>
        <div style={{ ...colStyle(1), minWidth: 150 }}>
          <div style={colLabelStyle}>解释</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
            <div>按所有可能<b>拆分求总概率</b></div>
            <div style={{ marginTop: 6, color: '#aaa', fontSize: 11 }}>
              <div>• B₁,B₂,...完全分割样本空间</div>
              <div>• 每条路径的贡献相加</div>
              <div>• 贝叶斯定理的<b>分母</b></div>
              <div>• 边缘化隐变量</div>
            </div>
          </div>
        </div>

        <div style={dividerStyle} />

        <div style={{ ...colStyle(1), minWidth: 140 }}>
          <div style={colLabelStyle}>已知</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.6 }}>
            {parts.map(p => (
              <div key={p.label} style={{ fontSize: 11, color: p.color }}>
                P({p.label})={p.p}, P(A|{p.label})={p.pa}
              </div>
            ))}
            <div style={{ marginTop: 6, borderTop: '1px dashed rgba(255,255,255,0.1)', paddingTop: 4 }}>
              <span style={{ color: '#FFD700' }}>求</span> P(A)
            </div>
          </div>
        </div>

        <div style={dividerStyle} />

        <div style={{ ...colStyle(1.5), minWidth: 260 }}>
          <div style={colLabelStyle}>解题过程</div>
          <style>{animCSS}</style>

          <div style={{ fontSize: 11, color: '#aaa', lineHeight: 1.7, marginBottom: 4 }}>
            {parts.map((p, i) => (
              <div key={i} className={`tp-f${Math.min(i + 1, 3)}`}>
                {`${i + 1}⃣ P(A|${p.label})·P(${p.label}) = ${p.pa}×${p.p} = `}
                <b style={{ color: p.color }}>{(p.pa * p.p).toFixed(3)}</b>
              </div>
            ))}
            <div className="tp-done" style={conclusionStyle}>
              <span style={{ color: '#FFD700', fontWeight: 700 }}>∴</span>{' '}
              P(A) = {parts.reduce((s, p) => s + p.pa * p.p, 0).toFixed(3)}
            </div>
          </div>

          {/* 树形图 SVG */}
          <svg width={220} height={110} viewBox="0 0 220 110" style={{ display: 'block' }}>
            {/* 根节点 */}
            <circle cx={30} cy={55} r={6} fill="#fff" stroke="#ffffff40" strokeWidth={1.5} />
            <text x={30} y={58} fill="#333" fontSize={7} textAnchor="middle" fontWeight={700}>S</text>

            {/* 三个分支 */}
            {parts.map((p, i) => {
              const ty = 20 + i * 35
              return (
                <React.Fragment key={i}>
                  <line x1={36} y1={55} x2={80} y2={ty} stroke={p.color} strokeWidth={1.5} className={`tp-f${Math.min(i + 1, 3)}`} />
                  <circle cx={80} cy={ty} r={5} fill={p.color} className={`tp-f${Math.min(i + 1, 3)}`} />
                  <text x={88} y={ty + 3} fill={p.color} fontSize={8} className={`tp-f${Math.min(i + 1, 3)}`}>
                    {p.label} ({p.p})
                  </text>
                  {/* A 分支 */}
                  <line x1={85} y1={ty} x2={150} y2={ty - 8} stroke={`${p.color}60`} strokeWidth={1} className={`tp-f${Math.min(i + 1, 3)}`} />
                  <text x={155} y={ty - 5} fill={p.color} fontSize={7} className={`tp-f${Math.min(i + 1, 3)}`}>
                    A ({p.pa}) → {(p.pa * p.p).toFixed(3)}
                  </text>
                </React.Fragment>
              )
            })}
            {/* 总和 */}
            <text x={155} y={105} fill={COLOR} fontSize={9} fontWeight={700} className="tp-done">
              ΣP = {parts.reduce((s, p) => s + p.pa * p.p, 0).toFixed(3)}
            </text>
          </svg>
        </div>
      </div>
    </div>
  )
}

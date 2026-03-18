// ═══════════════════════════════════════════════════════════
// L1 范数 — 顶部公式 + 三栏: 解释 | 已知 | 解题过程
// ═══════════════════════════════════════════════════════════

import React from 'react'
import 'katex/dist/katex.min.css'
import { BlockMath } from 'react-katex'
import { colStyle, dividerStyle, colLabelStyle, boardStyle, conclusionStyle } from './boardStyles'

const LATEX = String.raw`\|\vec{x}\|_1 = \sum_{i=1}^{n} |x_i|`
const COLOR = '#27ae60'

const animCSS = `
  @keyframes fadeIn { from { opacity: 0 } to { opacity: 1 } }
  @keyframes drawPath { from { stroke-dashoffset: 300 } to { stroke-dashoffset: 0 } }
  .l1-f1 { opacity: 0; animation: fadeIn 0.3s ease-out 0.2s forwards }
  .l1-f2 { opacity: 0; animation: fadeIn 0.3s ease-out 0.5s forwards }
  .l1-f3 { opacity: 0; animation: fadeIn 0.3s ease-out 0.8s forwards }
  .l1-diamond { stroke-dasharray: 300; stroke-dashoffset: 300; animation: drawPath 0.6s ease-out 0.3s forwards }
`

export const L1NormDiagram: React.FC<{ compact?: boolean }> = ({ compact }) => {
  if (compact) {
    return (
      <div style={{ textAlign: 'center', padding: '6px' }}>
        <div style={{ fontSize: 14, color: COLOR }}><BlockMath math={LATEX} /></div>
        <div style={{ color: '#888', fontSize: 9 }}>绝对值之和</div>
      </div>
    )
  }

  const cx = 110, cy = 65, r = 40
  // L1 单位球是菱形: |x|+|y|=1
  const diamond = `M ${cx},${cy - r} L ${cx + r},${cy} L ${cx},${cy + r} L ${cx - r},${cy} Z`
  // L2 单位球是圆 (对比)
  return (
    <div style={{ padding: '8px 0' }}>
      <div style={{
        padding: '4px 8px', display: 'flex', alignItems: 'center', gap: 8,
        background: 'rgba(255,255,255,0.02)', borderRadius: '8px 8px 0 0',
        border: '1px solid rgba(255,255,255,0.06)', borderBottom: 'none',
      }}>
        <span style={{ fontSize: 14, color: '#fff', fontWeight: 700, whiteSpace: 'nowrap' }}>L1 范数</span>
        <div style={{ flex: 1, fontSize: 20, color: COLOR, textAlign: 'center' }}><BlockMath math={LATEX} /></div>
      </div>

      <div style={{ ...boardStyle, borderRadius: '0 0 8px 8px' }}>
        <div style={{ ...colStyle(1), minWidth: 150 }}>
          <div style={colLabelStyle}>解释</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
            <div>向量各分量<b>绝对值之和</b></div>
            <div style={{ marginTop: 6, color: '#aaa', fontSize: 11 }}>
              <div>• LASSO 正则化核心</div>
              <div>• 促进<b>稀疏</b>解 (权重归零)</div>
              <div>• 单位球是<b>菱形</b></div>
              <div>• 菱形尖角碰坐标轴 → 稀疏</div>
            </div>
          </div>
        </div>

        <div style={dividerStyle} />

        <div style={{ ...colStyle(1), minWidth: 140 }}>
          <div style={colLabelStyle}>已知</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
            <div>x⃗ = [3, -4, 2]</div>
            <div>求 ‖x⃗‖₁</div>
            <div style={{ marginTop: 6, borderTop: '1px dashed rgba(255,255,255,0.1)', paddingTop: 4 }}>
              <span style={{ color: '#FFD700' }}>对比</span> L2 范数的圆形
            </div>
          </div>
        </div>

        <div style={dividerStyle} />

        <div style={{ ...colStyle(1.3), minWidth: 240 }}>
          <div style={colLabelStyle}>解题过程</div>
          <style>{animCSS}</style>

          <div style={{ fontSize: 11, color: '#aaa', lineHeight: 1.7, marginBottom: 4 }}>
            <div className="l1-f1">① |3| + |-4| + |2|</div>
            <div className="l1-f2">② = 3 + 4 + 2</div>
            <div className="l1-f3" style={conclusionStyle}>
              <span style={{ color: '#FFD700', fontWeight: 700 }}>∴</span> ‖x⃗‖₁ = <b style={{ color: COLOR }}>9</b>
            </div>
          </div>

          {/* SVG: L1 菱形 vs L2 圆 */}
          <svg width={220} height={130} viewBox="0 0 220 130" style={{ display: 'block' }}>
            <line x1={20} y1={cy} x2={200} y2={cy} stroke="#ffffff12" strokeWidth={1} />
            <line x1={cx} y1={10} x2={cx} y2={125} stroke="#ffffff12" strokeWidth={1} />
            {/* L2 球 (虚线圆) */}
            <circle cx={cx} cy={cy} r={r} fill="none" stroke="#4ea8de40" strokeWidth={1.5} strokeDasharray="4 3" className="l1-f2" />
            <text x={cx + r + 4} y={cy - 2} fill="#4ea8de60" fontSize={8} className="l1-f2">L2 球</text>
            {/* L1 球 (菱形) */}
            <path d={diamond} fill={`${COLOR}10`} stroke={COLOR} strokeWidth={2} className="l1-diamond" />
            <text x={cx + r + 4} y={cy + 12} fill={COLOR} fontSize={8} className="l1-f1">L1 球</text>
            {/* 尖角碰轴标注 */}
            <circle cx={cx} cy={cy - r} r={3} fill={COLOR} className="l1-f3" />
            <circle cx={cx + r} cy={cy} r={3} fill={COLOR} className="l1-f3" />
            <text x={cx + 4} y={cy - r - 4} fill={COLOR} fontSize={8} className="l1-f3">稀疏!</text>
          </svg>
        </div>
      </div>
    </div>
  )
}

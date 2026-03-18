// ═══════════════════════════════════════════════════════════
// Softmax — 顶部公式 + 三栏: 解释 | 已知 | 解题过程
// ═══════════════════════════════════════════════════════════

import React from 'react'
import 'katex/dist/katex.min.css'
import { BlockMath, InlineMath } from 'react-katex'
import {
  colStyle, dividerStyle, colLabelStyle, givenLineStyle,
  boardStyle, conclusionStyle,
} from './boardStyles'

const LATEX = String.raw`\sigma(z_i) = \frac{e^{z_i}}{\sum_{j=1}^{K} e^{z_j}}`
const COLOR = '#9b59b6'

const items = [
  { name: '猫', score: 2.0, color: '#FC6255' },
  { name: '狗', score: 1.0, color: '#58C4DD' },
  { name: '鸟', score: 0.5, color: '#FFDD44' },
]
const expScores = items.map(it => Math.exp(it.score))
const sumExp = expScores.reduce((a, b) => a + b, 0)
const probs = expScores.map(e => e / sumExp)

const animCSS = `
  @keyframes slideR { from { opacity: 0; transform: translateX(-8px) } to { opacity: 1; transform: translateX(0) } }
  @keyframes expand { from { transform: scaleX(0) } to { transform: scaleX(1) } }
  @keyframes pop { from { opacity: 0; transform: scale(0.6) } to { opacity: 1; transform: scale(1) } }
  .sm-s1 { opacity: 0; animation: slideR 0.3s ease-out 0.1s forwards }
  .sm-s3 { opacity: 0; animation: slideR 0.3s ease-out 0.5s forwards }
  .sm-s4 { opacity: 0; animation: slideR 0.3s ease-out 0.7s forwards }
  .sm-bar { transform-origin: left; animation: expand 0.4s ease-out 1.1s both }
  .sm-done { opacity: 0; animation: pop 0.3s ease-out 1.4s forwards }
`

export const SoftmaxDiagram: React.FC<{ compact?: boolean }> = ({ compact }) => {
  if (compact) {
    return (
      <div style={{ textAlign: 'center', padding: '6px' }}>
        <div style={{ fontSize: 14, color: COLOR }}><BlockMath math={LATEX} /></div>
        <div style={{ color: '#888', fontSize: 9 }}>分数→概率</div>
      </div>
    )
  }

  const barMaxW = 140

  return (
    <div style={{ padding: '8px 0' }}>
      {/* ═══ 顶部: 名称 + 公式 ═══ */}
      <div style={{
        padding: '4px 8px', display: 'flex', alignItems: 'center', gap: 8,
        background: 'rgba(255,255,255,0.02)', borderRadius: '8px 8px 0 0',
        border: '1px solid rgba(255,255,255,0.06)', borderBottom: 'none',
      }}>
        <span style={{ fontSize: 14, color: '#fff', fontWeight: 700, whiteSpace: 'nowrap' }}>Softmax 函数</span>
        <div style={{ flex: 1, fontSize: 20, color: COLOR, textAlign: 'center' }}>
          <BlockMath math={LATEX} />
        </div>
      </div>

      {/* ═══ 三栏: 解释 | 已知 | 解题过程 ═══ */}
      <div style={{ ...boardStyle, borderRadius: '0 0 8px 8px' }}>
        {/* 左栏: 解释 */}
        <div style={{ ...colStyle(1), minWidth: 150 }}>
          <div style={colLabelStyle}>解释</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
            <div>Softmax 函数将<b>任意实数向量</b>转化为<b>概率分布</b></div>
            <div style={{ marginTop: 6, color: '#aaa', fontSize: 11 }}>
              <div>• 所有输出在 [0, 1] 之间</div>
              <div>• 所有输出之和 = 1</div>
              <div>• 大的值 → 大的概率</div>
              <div>• 名称来源: argmax 的"柔性"版本</div>
            </div>
            <div style={{ marginTop: 8, color: '#888', fontSize: 10 }}>
              用于分类任务的最后一层，把原始打分变成概率
            </div>
          </div>
        </div>

        <div style={dividerStyle} />

        {/* 中栏: 已知 */}
        <div style={{ ...colStyle(1), minWidth: 150 }}>
          <div style={colLabelStyle}>已知</div>
          <div style={givenLineStyle}>K = 3 个类别</div>
          <div style={{ ...givenLineStyle, marginTop: 4 }}>
            <InlineMath math="z" /> = 模型的原始打分
          </div>
          <div style={{ marginTop: 6 }}>
            {items.map((it, i) => (
              <div key={i} style={{ ...givenLineStyle, color: it.color }}>
                <InlineMath math={`z_${i + 1}`} /> = {it.score.toFixed(1)}{' '}
                <span style={{ opacity: 0.7 }}>({it.name})</span>
              </div>
            ))}
          </div>
          <div style={{ ...givenLineStyle, marginTop: 8, borderTop: '1px dashed rgba(255,255,255,0.1)', paddingTop: 6 }}>
            <span style={{ color: '#FFD700' }}>求</span>{' '}
            <InlineMath math="\sigma(z_i)" /> = ?
          </div>
        </div>

        <div style={dividerStyle} />

        {/* 右栏: 解题过程 */}
        <div style={{ ...colStyle(1.5), minWidth: 240 }}>
          <div style={colLabelStyle}>解题过程</div>
          <style>{animCSS}</style>

          <div className="sm-s1" style={{ marginBottom: 6 }}>
            <div style={{ fontSize: 12, color: '#ddd', fontWeight: 700 }}>
              ① 取指数 e<sup>zᵢ</sup> <span style={{ color: '#888', fontWeight: 400, fontSize: 10 }}>— 拉大差距</span>
            </div>
            {items.map((it, i) => (
              <div key={i} style={{ fontSize: 11, color: it.color, lineHeight: 1.6, marginLeft: 8 }}>
                e<sup>{it.score}</sup> = <b>{expScores[i].toFixed(2)}</b>
              </div>
            ))}
          </div>

          <div className="sm-s3" style={{ marginBottom: 6 }}>
            <div style={{ fontSize: 12, color: '#ddd', fontWeight: 700 }}>
              ② 求和 <span style={{ color: '#888', fontWeight: 400, fontSize: 10 }}>— 分母</span>
            </div>
            <div style={{ fontSize: 11, color: '#aaa', marginLeft: 8, lineHeight: 1.6 }}>
              Σe<sup>zⱼ</sup> = {expScores.map(e => e.toFixed(1)).join(' + ')} = <b style={{ color: '#fff' }}>{sumExp.toFixed(2)}</b>
            </div>
          </div>

          <div className="sm-s4" style={{ marginBottom: 6 }}>
            <div style={{ fontSize: 12, color: '#ddd', fontWeight: 700 }}>
              ③ 除以总和 <span style={{ color: '#888', fontWeight: 400, fontSize: 10 }}>— 得概率</span>
            </div>
            {items.map((it, i) => (
              <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 6, marginLeft: 8, marginTop: 3 }}>
                <span style={{ fontSize: 11, color: it.color, width: 80 }}>
                  σ(z{'\u2081\u2082\u2083'[i]}) = {expScores[i].toFixed(1)}/{sumExp.toFixed(1)}
                </span>
                <div className="sm-bar" style={{
                  width: probs[i] * barMaxW, height: 12,
                  background: it.color, borderRadius: 3, opacity: 0.75,
                }} />
                <span style={{ fontSize: 12, color: it.color, fontWeight: 700 }}>
                  {(probs[i] * 100).toFixed(1)}%
                </span>
              </div>
            ))}
          </div>

          <div className="sm-done" style={conclusionStyle}>
            <span style={{ color: '#FFD700', fontWeight: 700 }}>∴</span>{' '}
            <span style={{ color: '#ddd' }}>最可能是 <b style={{ color: '#FC6255' }}>猫</b> (62.9%)</span>
            <div style={{ color: '#888', fontSize: 10 }}>✓ 62.9+23.1+14.0 = 100%</div>
          </div>
        </div>
      </div>
    </div>
  )
}

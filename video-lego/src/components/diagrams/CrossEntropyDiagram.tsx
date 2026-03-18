// ═══════════════════════════════════════════════════════════
// 交叉熵损失 — 顶部公式 + 三栏: 解释 | 已知 | 解题过程
// ═══════════════════════════════════════════════════════════

import React from 'react'
import 'katex/dist/katex.min.css'
import { BlockMath, InlineMath } from 'react-katex'
import {
  colStyle, dividerStyle, colLabelStyle, givenLineStyle,
  boardStyle, conclusionStyle,
} from './boardStyles'

const LATEX = String.raw`H(p,q) = -\sum_{x} p(x) \log q(x)`
const COLOR = '#e74c3c'

const items = [
  { name: '猫', p: 0.7, q: 0.5, color: '#FC6255' },
  { name: '狗', p: 0.2, q: 0.3, color: '#58C4DD' },
  { name: '鸟', p: 0.1, q: 0.2, color: '#FFDD44' },
]
const losses = items.map(it => -it.p * Math.log(it.q))
const H = losses.reduce((a, b) => a + b, 0)

const animCSS = `
  @keyframes slideR { from { opacity: 0; transform: translateX(-8px) } to { opacity: 1; transform: translateX(0) } }
  @keyframes expand { from { transform: scaleX(0) } to { transform: scaleX(1) } }
  @keyframes pop { from { opacity: 0; transform: scale(0.6) } to { opacity: 1; transform: scale(1) } }
  @keyframes pulse { 0%,100% { opacity: 1 } 50% { opacity: 0.4 } }
  .ce-s1 { opacity: 0; animation: slideR 0.3s ease-out 0.1s forwards }
  .ce-s2 { opacity: 0; animation: slideR 0.3s ease-out 0.4s forwards }
  .ce-s3 { opacity: 0; animation: slideR 0.3s ease-out 0.7s forwards }
  .ce-bar { transform-origin: left; animation: expand 0.4s ease-out 0.9s both }
  .ce-done { opacity: 0; animation: pop 0.3s ease-out 1.2s forwards }
  .ce-blink { animation: pulse 2s ease-in-out 1.5s infinite }
`

export const CrossEntropyDiagram: React.FC<{ compact?: boolean }> = ({ compact }) => {
  if (compact) {
    return (
      <div style={{ textAlign: 'center', padding: '6px' }}>
        <div style={{ fontSize: 14, color: COLOR }}><BlockMath math={LATEX} /></div>
        <div style={{ color: '#888', fontSize: 9 }}>预测和真实的差距</div>
      </div>
    )
  }

  const barMaxW = 120

  return (
    <div style={{ padding: '8px 0' }}>
      {/* 顶部: 名称 + 公式 */}
      <div style={{
        padding: '4px 8px', display: 'flex', alignItems: 'center', gap: 8,
        background: 'rgba(255,255,255,0.02)', borderRadius: '8px 8px 0 0',
        border: '1px solid rgba(255,255,255,0.06)', borderBottom: 'none',
      }}>
        <span style={{ fontSize: 14, color: '#fff', fontWeight: 700, whiteSpace: 'nowrap' }}>交叉熵损失</span>
        <div style={{ flex: 1, fontSize: 20, color: COLOR, textAlign: 'center' }}>
          <BlockMath math={LATEX} />
        </div>
      </div>

      <div style={{ ...boardStyle, borderRadius: '0 0 8px 8px' }}>
        {/* 左栏: 解释 */}
        <div style={{ ...colStyle(1), minWidth: 150 }}>
          <div style={colLabelStyle}>解释</div>
          <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
            <div>交叉熵度量两个概率分布之间的差异</div>
            <div style={{ marginTop: 6, color: '#aaa', fontSize: 11 }}>
              <div>• p(x) = 真实分布 (标准答案)</div>
              <div>• q(x) = 预测分布 (AI的回答)</div>
              <div>• H 越小 → 预测越准确</div>
              <div>• H = 0 当且仅当 p = q</div>
            </div>
            <div style={{ marginTop: 8, color: '#888', fontSize: 10 }}>
              分类任务中最常用的损失函数
            </div>
          </div>
        </div>

        <div style={dividerStyle} />

        {/* 中栏: 已知 */}
        <div style={{ ...colStyle(1), minWidth: 150 }}>
          <div style={colLabelStyle}>已知</div>
          <div style={givenLineStyle}>x ∈ {'{'}猫, 狗, 鸟{'}'}</div>
          <div style={{ marginTop: 6 }}>
            <div style={{ fontSize: 11, color: '#FC6255', fontWeight: 700, marginBottom: 2 }}>
              p(x) 真实分布:
            </div>
            {items.map((it, i) => (
              <div key={i} style={{ ...givenLineStyle, fontSize: 11, color: it.color, marginLeft: 8 }}>
                p({it.name}) = {(it.p * 100).toFixed(0)}%
              </div>
            ))}
          </div>
          <div style={{ marginTop: 6 }}>
            <div style={{ fontSize: 11, color: '#58C4DD', fontWeight: 700, marginBottom: 2 }}>
              q(x) 预测分布:
            </div>
            {items.map((it, i) => (
              <div key={i} style={{ ...givenLineStyle, fontSize: 11, color: it.color, marginLeft: 8 }}>
                q({it.name}) = {(it.q * 100).toFixed(0)}%
              </div>
            ))}
          </div>
          <div style={{
            ...givenLineStyle, marginTop: 6,
            borderTop: '1px dashed rgba(255,255,255,0.1)', paddingTop: 4,
          }}>
            <span style={{ color: '#FFD700' }}>求</span>{' '}
            <InlineMath math="H(p,q)" /> = ?
          </div>
        </div>

        <div style={dividerStyle} />

        {/* 右栏: 解题过程 */}
        <div style={{ ...colStyle(1.5), minWidth: 260 }}>
          <div style={colLabelStyle}>解题过程</div>
          <style>{animCSS}</style>

          <div className="ce-s1" style={{ marginBottom: 6 }}>
            <div style={{ fontSize: 12, color: '#ddd', fontWeight: 700 }}>
              ① 对比答案 <span style={{ color: '#888', fontWeight: 400, fontSize: 10 }}>— 找差距</span>
            </div>
            {items.map((it, i) => {
              const diff = Math.abs(it.p - it.q)
              return (
                <div key={i} style={{ fontSize: 11, marginLeft: 8, lineHeight: 1.6 }}>
                  <span style={{ color: it.color }}>{it.name}</span>
                  {' '}
                  <span style={{ color: '#FC6255' }}>{(it.p * 100).toFixed(0)}%</span>
                  <span style={{ color: '#888' }}> vs </span>
                  <span style={{ color: '#58C4DD' }}>{(it.q * 100).toFixed(0)}%</span>
                  {' '}
                  <span style={{ color: diff > 0.15 ? '#ff4444' : '#44cc44', fontSize: 10 }}>
                    {diff > 0.15 ? '差20%' : '接近'}
                  </span>
                </div>
              )
            })}
          </div>

          <div className="ce-s2" style={{ marginBottom: 6 }}>
            <div style={{ fontSize: 12, color: '#ddd', fontWeight: 700 }}>
              ② 计算 -p(x)·log q(x) <span style={{ color: '#888', fontWeight: 400, fontSize: 10 }}>— 每项损失</span>
            </div>
            {items.map((it, i) => (
              <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 6, marginLeft: 8, marginTop: 3 }}>
                <span style={{ fontSize: 10, color: '#aaa', width: 110 }}>
                  -{it.p}×log({it.q})
                </span>
                <div className="ce-bar" style={{
                  width: (losses[i] / H) * barMaxW, height: 12,
                  background: '#ff8c00', borderRadius: 3,
                  opacity: 0.4 + (losses[i] / H) * 0.6,
                }} />
                <span style={{ fontSize: 12, color: '#ff8c00', fontWeight: 700 }}>
                  {losses[i].toFixed(3)}
                </span>
                {losses[i] > 0.3 && (
                  <span className="ce-blink" style={{ fontSize: 10, color: '#ff4444' }}>!</span>
                )}
              </div>
            ))}
          </div>

          <div className="ce-s3" style={{ marginBottom: 6 }}>
            <div style={{ fontSize: 12, color: '#ddd', fontWeight: 700 }}>③ 求和</div>
            <div style={{ fontSize: 11, color: '#aaa', marginLeft: 8 }}>
              H = {losses.map(l => l.toFixed(3)).join(' + ')}
            </div>
          </div>

          <div className="ce-done" style={conclusionStyle}>
            <span style={{ color: '#FFD700', fontWeight: 700 }}>∴</span>{' '}
            <span style={{ color: '#ddd' }}>
              H(p,q) = <b style={{ color: '#FFD700' }}>{H.toFixed(3)}</b>
            </span>
            <div style={{ color: '#888', fontSize: 10 }}>
              主要损失来源: 猫差20% → 贡献{(losses[0] / H * 100).toFixed(0)}%
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

// ═══════════════════════════════════════════════════════════
// 积木预览 — 用 CSS 动画驱动 View 组件（轻量可靠）
// BlockPreview — CSS animations + View components (lightweight)
//
// 卡片预览：CSS 动画（无 Remotion 依赖）
// 详情页预览：Remotion Player（完整帧动画）
// ═══════════════════════════════════════════════════════════

import React, { useEffect, useState } from 'react'
import 'katex/dist/katex.min.css'
import { MGMT } from '@/theme'

// ── 导入 View 组件（零 Remotion 依赖！）──
import { FormulaBlockView } from '@blocks/formula/FormulaBlock'
import { FormulaDerivationView } from '@blocks/formula/FormulaDerivation'
import { UCurveView } from '@blocks/chart/UCurve'
import { ComparisonSplitView } from '@blocks/structure/ComparisonSplit'
import { TimelineView } from '@blocks/structure/Timeline'


// ─────────── CSS Keyframes 注入 ───────────

const KEYFRAMES_ID = 'lego-preview-keyframes'

function ensureKeyframes() {
  if (document.getElementById(KEYFRAMES_ID)) return
  const style = document.createElement('style')
  style.id = KEYFRAMES_ID
  style.textContent = `
    @keyframes lego-fade-in { from { opacity: 0; transform: scale(0.85); } to { opacity: 1; transform: scale(1); } }
    @keyframes lego-slide-up { from { opacity: 0; transform: translateY(18px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes lego-slide-left { from { opacity: 0; transform: translateX(-24px); } to { opacity: 1; transform: translateX(0); } }
    @keyframes lego-slide-right { from { opacity: 0; transform: translateX(24px); } to { opacity: 1; transform: translateX(0); } }
    @keyframes lego-grow { from { width: 0%; } }
    @keyframes lego-draw { from { stroke-dashoffset: 2000; } to { stroke-dashoffset: 0; } }
  `
  document.head.appendChild(style)
}

// ─────────── 动画钩子：循环触发重播 ───────────

function useLoopTrigger(intervalMs = 4000) {
  const [key, setKey] = useState(0)
  useEffect(() => {
    ensureKeyframes()
    const timer = setInterval(() => setKey((k) => k + 1), intervalMs)
    return () => clearInterval(timer)
  }, [intervalMs])
  return key
}

// ─────────── 各积木动画预览 ───────────

function FormulaBlockPreview() {
  const key = useLoopTrigger(3500)
  return (
    <div key={key} style={{ transform: 'scale(0.5)', transformOrigin: 'center' }}>
      <FormulaBlockView
        latex="P^{*} \leq P_{\text{1-NN}} \leq 2P^{*}"
        label="Cover-Hart 最近邻误差上界"
        color="#ffd700"
        containerStyle={{ animation: 'lego-fade-in 0.6s ease-out both' }}
      />
    </div>
  )
}

function FormulaDerivationPreview() {
  const key = useLoopTrigger(5000)
  return (
    <div key={key} style={{ transform: 'scale(0.42)', transformOrigin: 'center' }}>
      <FormulaDerivationView
        steps={[
          { latex: 'a^2 + b^2 = c^2', annotation: '勾股定理' },
          { latex: 'c = \\sqrt{a^2 + b^2}', annotation: '解出距离' },
          { latex: 'd = \\sqrt{\\sum_{i=1}^{n}(x_i - y_i)^2}', annotation: '推广到 n 维 — 欧氏距离', highlight: true },
        ]}
        source="PRML Ch.2.5.2"
        getItemStyle={(i) => ({
          animation: `lego-slide-up 0.5s ease-out ${0.3 + i * 0.6}s both`,
        })}
      />
    </div>
  )
}

function UCurvePreview() {
  const key = useLoopTrigger(5000)
  const points = Array.from({ length: 25 }, (_, i) => {
    const x = i + 1
    const y = 0.8 * Math.pow((x - 12) / 10, 2) + 0.15
    return { x, y: Math.round(y * 1000) / 1000 }
  })
  // 渐进动画：先显示坐标轴，再画曲线
  const [phase, setPhase] = useState(0)
  useEffect(() => {
    const t1 = setTimeout(() => setPhase(1), 300)  // 坐标轴
    const t2 = setTimeout(() => setPhase(2), 800)  // 曲线
    const t3 = setTimeout(() => setPhase(3), 1800) // 最优点
    return () => { clearTimeout(t1); clearTimeout(t2); clearTimeout(t3) }
  }, [key])

  return (
    <div key={key} style={{ transform: 'scale(0.4)', transformOrigin: 'center', width: 960 }}>
      <UCurveView
        points={points}
        xLabel="模型复杂度 (K)"
        yLabel="测试误差"
        zones={[
          { start: 1, end: 8, color: '#e74c3c', label: '欠拟合' },
          { start: 16, end: 25, color: '#e67e22', label: '过拟合' },
        ]}
        bestPoint={{ x: 12, annotation: '最优 K' }}
        axisOpacity={phase >= 1 ? 1 : 0}
        visiblePointCount={phase >= 2 ? points.length : 0}
        zoneOpacity={phase >= 2 ? 1 : 0}
        bestOpacity={phase >= 3 ? 1 : 0}
        bestScale={phase >= 3 ? 1 : 0.01}
      />
    </div>
  )
}

function ComparisonSplitPreview() {
  const key = useLoopTrigger(4000)
  return (
    <div key={key} style={{ transform: 'scale(0.42)', transformOrigin: 'center' }}>
      <ComparisonSplitView
        left={{ icon: '🐌', value: '暴力搜索', label: 'O(nd)', color: '#e74c3c', subItems: ['逐个遍历', '保证精确', '小数据OK'] }}
        right={{ icon: '⚡', value: 'KD-Tree', label: 'O(log n)', color: '#2ecc71', subItems: ['分治递归', '近似搜索', '高维退化'] }}
        getItemStyle={(ci) => ({
          animation: `${ci === 0 ? 'lego-slide-left' : 'lego-slide-right'} 0.5s ease-out ${0.2 + ci * 0.3}s both`,
        })}
      />
    </div>
  )
}

function TimelinePreview() {
  const key = useLoopTrigger(5000)
  return (
    <div key={key} style={{ transform: 'scale(0.46)', transformOrigin: 'center' }}>
      <TimelineView
        events={[
          { year: '1967', text: 'Cover-Hart 定理', color: '#ffd700', icon: '📜' },
          { year: '1975', text: 'KD-Tree', color: '#4ea8de', icon: '🌲' },
          { year: '1998', text: 'LSH 近似搜索', color: '#2ecc71', icon: '🎲' },
          { year: '2019', text: 'HNSW (Faiss)', color: '#e74c3c', icon: '⚡' },
        ]}
        getItemStyle={(i) => ({
          animation: `lego-slide-up 0.4s ease-out ${0.2 + i * 0.5}s both`,
        })}
      />
    </div>
  )
}

function DataBlockPlaceholder({ icon, label }: { icon: string; label: string }) {
  return (
    <div style={{
      display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
      width: '100%', height: '100%', gap: 6,
    }}>
      <div style={{ fontSize: 36, opacity: 0.5 }}>{icon}</div>
      <div style={{ color: MGMT.dimWhite, fontSize: 11, fontFamily: MGMT.fontFamily }}>{label}</div>
    </div>
  )
}



// ─────────── 预览注册表 Preview Registry ───────────

const PREVIEW_REGISTRY: Record<string, React.FC> = {
  FormulaBlock: FormulaBlockPreview,
  FormulaDerivation: FormulaDerivationPreview,
  UCurve: UCurvePreview,
  ComparisonSplit: ComparisonSplitPreview,
  Timeline: TimelinePreview,
  ProgressBars: () => <DataBlockPlaceholder icon="📊" label="进度条对比" />,
  StatCards: () => <DataBlockPlaceholder icon="🎯" label="统计卡片" />,
  CodeBlock: () => <DataBlockPlaceholder icon="💻" label="代码块" />,
  ImageDisplay: () => <DataBlockPlaceholder icon="📸" label="图片展示" />,
}

// ─────────── 主预览组件 Main Preview ───────────

export function BlockPreview({ blockName }: { blockName: string }) {
  const PreviewComponent = PREVIEW_REGISTRY[blockName]

  if (!PreviewComponent) {
    return (
      <div style={{ color: MGMT.dimWhite, textAlign: 'center' }}>
        <div style={{ fontSize: 48, marginBottom: MGMT.sp.sm }}>⬜</div>
        <div style={{ fontSize: MGMT.fontSize.small }}>积木待实现</div>
      </div>
    )
  }

  return (
    <div style={{
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      width: '100%', height: '100%', overflow: 'hidden',
      background: 'linear-gradient(180deg, rgba(26,26,46,0.95), rgba(15,15,30,0.95))',
      borderRadius: 12,
    }}>
      <PreviewComponent />
    </div>
  )
}

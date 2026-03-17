// ═══════════════════════════════════════════════════════════
// 视频制作流水线 — 9 阶段可视化 + 阶段详情
// ═══════════════════════════════════════════════════════════

import { useState } from 'react'
import { MGMT } from '@/theme'
import { StatusNode, Badge } from '@/components/ui'
import { useNav } from '@/App'

// ─────────── 阶段定义 ───────────

const PHASES = [
  { id: 'init', name: '初始化', icon: '⚙️', order: 0 },
  { id: 'content', name: '内容提取', icon: '📚', order: 1 },
  { id: 'script', name: '脚本写作', icon: '✍️', order: 2 },
  { id: 'storyboard', name: '分镜设计', icon: '🎨', order: 3 },
  { id: 'assets', name: '素材制作', icon: '🧱', order: 4 },
  { id: 'voice', name: '语音合成', icon: '🎙️', order: 5 },
  { id: 'captions', name: '字幕生成', icon: '💬', order: 6 },
  { id: 'render', name: '组装渲染', icon: '🎬', order: 7 },
  { id: 'review', name: '质量审查', icon: '🔍', order: 8 },
]

const PHASE_STATUS: Record<string, string> = {
  init: 'completed', content: 'completed', script: 'completed', storyboard: 'completed',
  assets: 'completed', voice: 'completed', captions: 'completed',
  render: 'in_progress', review: 'pending',
}

export function VideoPipeline({ course, topic }: { course: string; topic: string }) {
  const { navigate } = useNav()
  const [selectedPhase, setSelectedPhase] = useState<string | null>(null)

  return (
    <div style={{ padding: MGMT.sp.xl }}>
      {/* 面包屑 */}
      <div style={{ marginBottom: MGMT.sp.lg, display: 'flex', alignItems: 'center', gap: MGMT.sp.sm }}>
        <span onClick={() => navigate({ page: 'videos' })} style={{ fontSize: MGMT.fontSize.small, color: MGMT.dimWhite, cursor: 'pointer' }}>← 视频项目</span>
        <span style={{ color: MGMT.gray }}>·</span>
        <span style={{ fontSize: MGMT.fontSize.small, color: MGMT.blue }}>{course}/{topic}</span>
      </div>

      <h1 style={{ fontSize: MGMT.fontSize.h1, fontWeight: 800, marginBottom: MGMT.sp.xs }}>🎬 KNN — 从抄作业到 AI 基础设施</h1>
      <div style={{ fontSize: MGMT.fontSize.small, color: MGMT.dimWhite, marginBottom: MGMT.sp.xl }}>{course} · 20 场景 · 395s</div>

      {/* 流水线图 */}
      <div style={{ background: MGMT.bgCard, borderRadius: MGMT.radius.lg, border: `1px solid ${MGMT.border}`, padding: MGMT.sp.xl, marginBottom: MGMT.sp.xl }}>
        <h3 style={{ fontSize: MGMT.fontSize.h3, fontWeight: 600, marginBottom: MGMT.sp.lg, color: MGMT.dimWhite }}>📋 制作流水线</h3>

        {/* 顺序阶段 P0-P3 */}
        <div style={{ display: 'flex', alignItems: 'center', gap: MGMT.sp.md, marginBottom: MGMT.sp.lg }}>
          {PHASES.slice(0, 4).map((phase, i) => (
            <span key={phase.id} style={{ display: 'contents' }}>
              {i > 0 && <Arrow />}
              <StatusNode label={phase.name} status={PHASE_STATUS[phase.id]} onClick={() => setSelectedPhase(phase.id)} isActive={selectedPhase === phase.id} />
            </span>
          ))}
        </div>

        {/* 并行分支：素材 ↔ 语音 → 字幕 */}
        <div style={{ display: 'flex', gap: MGMT.sp.xl, marginLeft: 60, marginBottom: MGMT.sp.lg }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: MGMT.sp.md }}>
            <DownArrow />
            <StatusNode label="素材制作" status={PHASE_STATUS.assets} onClick={() => setSelectedPhase('assets')} isActive={selectedPhase === 'assets'} />
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: MGMT.sp.md }}>
            <StatusNode label="语音合成" status={PHASE_STATUS.voice} onClick={() => setSelectedPhase('voice')} isActive={selectedPhase === 'voice'} />
            <Arrow />
            <StatusNode label="字幕生成" status={PHASE_STATUS.captions} onClick={() => setSelectedPhase('captions')} isActive={selectedPhase === 'captions'} />
          </div>
        </div>

        {/* 汇合 P7-P8 */}
        <div style={{ display: 'flex', alignItems: 'center', gap: MGMT.sp.md, marginLeft: 120 }}>
          <StatusNode label="组装渲染" status={PHASE_STATUS.render} onClick={() => setSelectedPhase('render')} isActive={selectedPhase === 'render'} />
          <Arrow />
          <StatusNode label="质量审查" status={PHASE_STATUS.review} onClick={() => setSelectedPhase('review')} isActive={selectedPhase === 'review'} />
        </div>
      </div>

      {/* 阶段详情 */}
      {selectedPhase && (
        <div style={{ background: MGMT.bgCard, borderRadius: MGMT.radius.lg, border: `1px solid ${MGMT.border}`, padding: MGMT.sp.xl }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: MGMT.sp.md, marginBottom: MGMT.sp.md }}>
            <h3 style={{ fontSize: MGMT.fontSize.h2, fontWeight: 700 }}>
              {PHASES.find((p) => p.id === selectedPhase)?.icon} {PHASES.find((p) => p.id === selectedPhase)?.name}
            </h3>
            <Badge status={PHASE_STATUS[selectedPhase]} />
          </div>
          <div style={{ fontSize: MGMT.fontSize.small, color: MGMT.dimWhite }}>
            产出物路径：
            <code style={{ fontFamily: MGMT.codeFontFamily, color: MGMT.blue, marginLeft: 8 }}>
              {getPhaseOutput(selectedPhase)}
            </code>
          </div>
          <div style={{ marginTop: MGMT.sp.md, padding: MGMT.sp.md, background: 'rgba(255,255,255,0.02)', borderRadius: MGMT.radius.sm, fontSize: MGMT.fontSize.small, color: MGMT.grayLight, textAlign: 'center' }}>
            📂 阶段详情子模块待实现
          </div>
        </div>
      )}
    </div>
  )
}

function Arrow() { return <div style={{ color: MGMT.gray, fontSize: 18, padding: '0 4px' }}>→</div> }
function DownArrow() { return <div style={{ color: MGMT.gray, fontSize: 18, padding: '0 4px' }}>↓</div> }

function getPhaseOutput(phase: string): string {
  const outputs: Record<string, string> = {
    init: '.video-state.yaml', content: 'content_brief.md', script: 'script.md + script_tts.txt',
    storyboard: 'storyboard.md', assets: 'assets/', voice: 'narration/', captions: 'captions.json',
    render: 'video.data.ts → final.mp4', review: 'review_report.md',
  }
  return outputs[phase] || ''
}

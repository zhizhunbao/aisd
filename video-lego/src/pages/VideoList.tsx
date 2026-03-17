// ═══════════════════════════════════════════════════════════
// 视频项目列表 — 显示所有视频项目和进度
// ═══════════════════════════════════════════════════════════

import { MGMT } from '@/theme'
import { Card, Badge } from '@/components/ui'
import { useNav } from '@/App'
import { VIDEO_PROJECTS } from '@/data/video-projects'

export function VideoList() {
  const { navigate } = useNav()

  return (
    <div style={{ padding: MGMT.sp.xl }}>
      <h1 style={{ fontSize: MGMT.fontSize.h1, fontWeight: 800, marginBottom: MGMT.sp.lg }}>🎬 视频项目</h1>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: MGMT.sp.md }}>
        {VIDEO_PROJECTS.map((proj) => {
          const completedPhases = proj.phases.filter((p) => p.status === 'completed').length
          const pct = Math.round((completedPhases / proj.totalPhases) * 100)
          return (
            <Card key={`${proj.course}/${proj.topic}`}
              onClick={() => navigate({ page: 'video-pipeline', course: proj.course, topic: proj.topic })}
              accentColor={MGMT.blue}>
              <div style={{ padding: MGMT.sp.lg }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: MGMT.sp.md, marginBottom: MGMT.sp.md }}>
                  <h2 style={{ fontSize: MGMT.fontSize.h2, fontWeight: 700, flex: 1 }}>🎬 {proj.title}</h2>
                  <Badge status={pct === 100 ? 'completed' : 'in_progress'} />
                </div>
                <div style={{ fontSize: MGMT.fontSize.small, color: MGMT.dimWhite, marginBottom: MGMT.sp.md }}>
                  📂 {proj.course} · 🎞 {proj.sceneCount} 场景 · ⏱ {Math.round(proj.durationSec)}s
                </div>
                <div style={{ display: 'flex', gap: 4, marginBottom: MGMT.sp.sm }}>
                  {proj.phases.map((phase, i) => (
                    <div key={i} style={{
                      flex: 1, height: 8, borderRadius: 4,
                      background: phase.status === 'completed' ? MGMT.green : phase.status === 'in_progress' ? MGMT.blue : MGMT.border,
                      transition: 'all 0.3s',
                    }} title={`${phase.name} — ${phase.status}`} />
                  ))}
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: MGMT.fontSize.tiny, color: MGMT.grayLight }}>
                  <span>Phase {completedPhases}/{proj.totalPhases}</span>
                  <span>{pct}%</span>
                </div>
              </div>
            </Card>
          )
        })}
      </div>
    </div>
  )
}

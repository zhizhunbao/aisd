// ═══════════════════════════════════════════════════════════
// Dashboard — 素材积木管理系统首页
// ═══════════════════════════════════════════════════════════

import { MGMT } from '@/theme'
import { Card, ProgressBar } from '@/components/ui'
import { useNav } from '@/App'
import { BLOCK_CATEGORIES, getCatalogStats } from '@blocks/catalog'
import { VIDEO_PROJECTS } from '@/data/video-projects'
import { ASSET_CATEGORIES } from '@/lib/asset-types'
import { DEMO_ASSETS } from '@/data/demo-assets'

// ─────────── Dashboard ───────────

export function Dashboard() {
  const { navigate } = useNav()
  const stats = getCatalogStats()

  return (
    <div style={{ padding: MGMT.sp.xl }}>
      <h1 style={{ fontSize: MGMT.fontSize.h1, fontWeight: 800, marginBottom: MGMT.sp.lg }}>
        🏠 Dashboard
      </h1>

      {/* 积木统计 */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: MGMT.sp.md, marginBottom: MGMT.sp.xl }}>
        {[
          { label: '总素材', value: DEMO_ASSETS.length, color: MGMT.blue, icon: '📦' },
          { label: '总积木', value: stats.total, color: MGMT.gold, icon: '🧱' },
          { label: '已完成', value: stats.ready, color: MGMT.green, icon: '✅' },
          { label: '待实现', value: stats.todo, color: MGMT.grayLight, icon: '⬜' },
          { label: '平均评分', value: stats.avgScore, color: MGMT.gold, icon: '⭐' },
        ].map((stat) => (
          <Card key={stat.label}>
            <div style={{ padding: `${MGMT.sp.lg}px ${MGMT.sp.lg}px`, textAlign: 'center' }}>
              <div style={{ fontSize: 28, marginBottom: MGMT.sp.xs }}>{stat.icon}</div>
              <div style={{ fontSize: 36, fontWeight: 800, color: stat.color, fontFamily: 'Inter, sans-serif' }}>
                {stat.value}
              </div>
              <div style={{ fontSize: MGMT.fontSize.small, color: MGMT.dimWhite, marginTop: MGMT.sp.xs }}>
                {stat.label}
              </div>
            </div>
          </Card>
        ))}
      </div>

      {/* 素材分类概览 */}
      <h2 style={{ fontSize: MGMT.fontSize.h3, fontWeight: 700, marginBottom: MGMT.sp.md, color: MGMT.dimWhite }}>
        📦 素材库
      </h2>
      <div style={{ display: 'flex', gap: MGMT.sp.sm, marginBottom: MGMT.sp.xl, flexWrap: 'wrap' }}>
        {ASSET_CATEGORIES.map(cat => {
          const count = DEMO_ASSETS.filter(a => a.category === cat.id).length
          if (count === 0) return null
          return (
            <Card key={cat.id} onClick={() => navigate({ page: 'assets', filter: cat.id })} accentColor={cat.color}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '10px 16px' }}>
                <span style={{ fontSize: 20 }}>{cat.icon}</span>
                <span style={{ fontSize: MGMT.fontSize.small, fontWeight: 500 }}>{cat.name}</span>
                <span style={{ fontSize: MGMT.fontSize.small, fontWeight: 700, color: cat.color, marginLeft: 4 }}>{count}</span>
              </div>
            </Card>
          )
        })}
      </div>

      {/* 分类进度 */}
      <h2 style={{ fontSize: MGMT.fontSize.h3, fontWeight: 700, marginBottom: MGMT.sp.md, color: MGMT.dimWhite }}>
        📂 分类进度
      </h2>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: MGMT.sp.md, marginBottom: MGMT.sp.xl }}>
        {BLOCK_CATEGORIES.map((cat) => {
          const ready = cat.blocks.filter((b) => b.status === 'ready').length
          const pct = cat.blocks.length > 0 ? Math.round((ready / cat.blocks.length) * 100) : 0
          return (
            <Card key={cat.id} onClick={() => navigate({ page: 'blocks', filter: cat.id })}>
              <div style={{ padding: MGMT.sp.md }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: MGMT.sp.sm, marginBottom: MGMT.sp.sm }}>
                  <span style={{ fontSize: 22 }}>{cat.icon}</span>
                  <span style={{ fontSize: MGMT.fontSize.body, fontWeight: 600 }}>{cat.name}</span>
                  <span style={{ marginLeft: 'auto', fontSize: MGMT.fontSize.small, color: MGMT.dimWhite }}>
                    {ready}/{cat.blocks.length}
                  </span>
                </div>
                <ProgressBar value={pct} color={cat.color} />
              </div>
            </Card>
          )
        })}
      </div>

      {/* 视频项目 */}
      <h2 style={{ fontSize: MGMT.fontSize.h3, fontWeight: 700, marginBottom: MGMT.sp.md, color: MGMT.dimWhite }}>
        🎬 视频项目
      </h2>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: MGMT.sp.md }}>
        {VIDEO_PROJECTS.map((proj) => {
          const pct = Math.round((proj.currentPhase / proj.totalPhases) * 100)
          return (
            <Card
              key={`${proj.course}/${proj.topic}`}
              onClick={() => navigate({ page: 'video-pipeline', course: proj.course, topic: proj.topic })}
              accentColor={MGMT.blue}
            >
              <div style={{ padding: MGMT.sp.lg }}>
                <div style={{ fontSize: MGMT.fontSize.h3, fontWeight: 700, marginBottom: MGMT.sp.sm }}>
                  🎬 {proj.title}
                </div>
                <div style={{ fontSize: MGMT.fontSize.small, color: MGMT.dimWhite, marginBottom: MGMT.sp.md }}>
                  {proj.course} · {proj.sceneCount} 场景 · {Math.round(proj.durationSec)}s
                </div>
                <ProgressBar value={pct} color={MGMT.blue} />
                <div style={{ fontSize: MGMT.fontSize.tiny, color: MGMT.grayLight, marginTop: MGMT.sp.xs }}>
                  Phase {proj.currentPhase}/{proj.totalPhases}
                </div>
              </div>
            </Card>
          )
        })}
      </div>
    </div>
  )
}

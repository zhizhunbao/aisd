// ═══════════════════════════════════════════════════════════
// App — 素材积木管理系统主组件
// App — Material & Block Management System
// ═══════════════════════════════════════════════════════════

import { useState, useMemo, createContext, useContext, type ReactNode } from 'react'
import { MGMT } from './theme'
import { Dashboard } from './pages/Dashboard'
import { AssetLibrary } from './pages/AssetLibrary'
import { AssetDetail } from './pages/AssetDetail'
import { BlockCatalog } from './pages/BlockCatalog'
import { BlockDetail } from './pages/BlockDetail'
import { VideoList } from './pages/VideoList'
import { VideoPipeline } from './pages/VideoPipeline'
import { SceneComposerPage } from './modules/scene-composer'
import { VIDEO_PROJECTS } from './data/video-projects'
import { IconDashboard, IconPackage, IconBlocks, IconVideo, IconFilm } from './components/Icons'

// ─────────── 路由类型 Route Types ───────────

export type Route =
  | { page: 'dashboard' }
  | { page: 'assets'; filter?: string }
  | { page: 'asset-detail'; assetId: string }
  | { page: 'blocks'; filter?: string }
  | { page: 'block-detail'; blockName: string }
  | { page: 'videos' }
  | { page: 'video-pipeline'; course: string; topic: string }
  | { page: 'scene-composer'; course: string; topic: string }

// ─────────── 导航上下文 ───────────

interface NavContextType {
  route: Route
  navigate: (route: Route) => void
}

export const NavContext = createContext<NavContextType>({
  route: { page: 'dashboard' },
  navigate: () => {},
})

export const useNav = () => useContext(NavContext)

// ─────────── 侧边栏配置 ───────────

const NAV_SECTIONS: { label: string; items: { page: string; icon: ReactNode; label: string }[] }[] = [
  {
    label: '管理',
    items: [
      { page: 'dashboard', icon: <IconDashboard size={18} />, label: 'Dashboard' },
    ],
  },
  {
    label: '内容',
    items: [
      { page: 'assets', icon: <IconPackage size={18} />, label: '素材库' },
      { page: 'blocks', icon: <IconBlocks size={18} />, label: '积木组件' },
    ],
  },
  {
    label: '制作',
    items: [
      { page: 'videos', icon: <IconVideo size={18} />, label: '视频项目' },
    ],
  },
  {
    label: '组装',
    items: [
      { page: 'scene-composer', icon: <IconFilm size={18} />, label: 'M9 场景编排' },
    ],
  },
]

// ─────────── App ───────────

export function App() {
  const [route, setRoute] = useState<Route>({ page: 'dashboard' })
  const contextValue = useMemo(() => ({ route, navigate: setRoute }), [route])

  function isActive(page: string) {
    if (route.page === page) return true
    if (page === 'assets' && route.page === 'asset-detail') return true
    if (page === 'blocks' && route.page === 'block-detail') return true
    if (page === 'videos' && route.page === 'video-pipeline') return true
    if (page === 'scene-composer' && route.page === 'scene-composer') return true
    return false
  }

  return (
    <NavContext.Provider value={contextValue}>
      <div style={{
        display: 'flex', width: '100vw', height: '100vh',
        background: MGMT.bg, fontFamily: MGMT.fontFamily, color: MGMT.white, overflow: 'hidden',
      }}>
        {/* ══════ 侧边栏 ══════ */}
        <aside style={{
          width: MGMT.sidebar.width, minWidth: MGMT.sidebar.width,
          background: MGMT.bgSidebar, borderRight: `1px solid ${MGMT.border}`,
          display: 'flex', flexDirection: 'column', height: '100%',
        }}>
          {/* Logo */}
          <div style={{
            padding: `${MGMT.sp.lg}px ${MGMT.sp.lg}px ${MGMT.sp.md}px`,
            borderBottom: `1px solid ${MGMT.border}`,
          }}>
            <div style={{
              fontSize: MGMT.fontSize.h2, fontWeight: 800,
              background: `linear-gradient(135deg, ${MGMT.gold}, #ffaa00)`,
              WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
            }}>
              Video Lego
            </div>
            <div style={{ fontSize: MGMT.fontSize.tiny, color: MGMT.grayLight, marginTop: 4 }}>
              素材积木管理系统
            </div>
          </div>

          {/* 导航分组 */}
          <nav style={{ flex: 1, padding: `${MGMT.sp.sm}px ${MGMT.sp.sm}px`, overflowY: 'auto' }}>
            {NAV_SECTIONS.map(section => (
              <div key={section.label} style={{ marginBottom: MGMT.sp.sm }}>
                <div style={{
                  fontSize: 10, textTransform: 'uppercase', letterSpacing: 2,
                  color: MGMT.gray, padding: '10px 14px 4px', fontWeight: 600,
                }}>
                  {section.label}
                </div>
                {section.items.map(item => {
                  const active = isActive(item.page)
                  const handleClick = () => {
                    if (item.page === 'scene-composer') {
                      // 场景编排需要 course/topic — 默认选第一个项目
                      const first = VIDEO_PROJECTS[0]
                      if (first) setRoute({ page: 'scene-composer', course: first.course, topic: first.topic })
                    } else {
                      setRoute({ page: item.page } as Route)
                    }
                  }
                  return (
                    <div key={item.page}
                      onClick={handleClick}
                      style={{
                        display: 'flex', alignItems: 'center', gap: 12,
                        padding: '10px 14px', borderRadius: MGMT.radius.md,
                        cursor: 'pointer', marginBottom: 2,
                        background: active ? `${MGMT.gold}0A` : 'transparent',
                        border: `1px solid ${active ? `${MGMT.gold}22` : 'transparent'}`,
                        transition: 'all 0.15s',
                      }}
                    >
                      <span style={{ display: 'flex', alignItems: 'center' }}>{item.icon}</span>
                      <span style={{
                        fontSize: MGMT.fontSize.body,
                        fontWeight: active ? 600 : 400,
                        color: active ? MGMT.gold : MGMT.white,
                      }}>
                        {item.label}
                      </span>
                    </div>
                  )
                })}
              </div>
            ))}
          </nav>

          {/* 底部 */}
          <div style={{ padding: MGMT.sp.md, borderTop: `1px solid ${MGMT.border}`, fontSize: MGMT.fontSize.tiny, color: MGMT.gray }}>
            Video Lego v2.0
          </div>
        </aside>

        {/* ══════ 主内容 ══════ */}
        <main style={{ flex: 1, overflow: 'auto', height: '100%' }}>
          <PageRouter route={route} />
        </main>
      </div>
    </NavContext.Provider>
  )
}

// ─────────── 页面路由器 ───────────

function PageRouter({ route }: { route: Route }) {
  switch (route.page) {
    case 'dashboard':      return <Dashboard />
    case 'assets':         return <AssetLibrary />
    case 'asset-detail':   return <AssetDetail assetId={route.assetId} />
    case 'blocks':         return <BlockCatalog />
    case 'block-detail':   return <BlockDetail blockName={route.blockName} />
    case 'videos':         return <VideoList />
    case 'video-pipeline': return <VideoPipeline course={route.course} topic={route.topic} />
    case 'scene-composer': return <SceneComposerPage course={route.course} topic={route.topic} />
    default:               return <Dashboard />
  }
}

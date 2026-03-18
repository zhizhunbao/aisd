// ═══════════════════════════════════════════════════════════
// App — Video Lego 管理系统主组件（注册表驱动）
// App — Video Lego Management System (registry-driven)
//
// 架构:
//   模块注册表 (module-registry.ts)
//     → 左侧导航自动生成
//     → 模块页面自动路由
//     → 侧栏结构可配置
//
//   特殊模块（有实际功能）仍用自定义组件:
//     M0  素材管理器  → AssetManagerPage
//     M6  积木编辑器  → BlockEditorPage
//     M9  场景编排    → SceneComposerPage
//     视频管理        → VideoManagerPage
// ═══════════════════════════════════════════════════════════

import { useState, useMemo, useEffect, useCallback, createContext, useContext, type ReactNode } from 'react'
import { MGMT } from './theme'
import { Dashboard } from './pages/Dashboard'
import { VIDEO_PROJECTS } from './data/video-projects'
import { DEFAULT_MODULES, LAYERS, type ModuleDef } from './data/module-registry'
import { GenericModulePage } from './components/GenericModulePage'

// ─── 特殊模块导入（有实际功能的） ───
import { AssetManagerPage } from './modules/asset-manager'
import { BlockEditorPage } from './modules/block-editor'
import { SceneComposerPage } from './modules/scene-composer'
import { VideoManagerPage } from './modules/video-manager'

// ─── 图标 Icons ───
import {
  IconDashboard, IconPackage, IconBlocks, IconVideo, IconFilm,
  IconMic, IconSparkles, IconClock, IconDatabase, IconBookOpen,
  IconPalette2, IconType, IconVolume, IconListChecks,
} from './components/Icons'

// ─── 图标 key → React 组件映射 ───

const ICON_KEY_MAP: Record<string, React.ComponentType<{ size: number }>> = {
  package: IconPackage,
  mic: IconMic,
  palette: IconPalette2,
  type: IconType,
  database: IconDatabase,
  volume: IconVolume,
  blocks: IconBlocks,
  sparkles: IconSparkles,
  listChecks: IconListChecks,
  bookOpen: IconBookOpen,
  film: IconFilm,
  clock: IconClock,
}

function resolveIcon(key: string, size: number) {
  const Icon = ICON_KEY_MAP[key] || IconPackage
  return <Icon size={size} />
}

// ─────────── 路由类型 Route Types ───────────

export type Route =
  | { page: 'dashboard' }
  | { page: 'scene-composer'; course: string; topic: string }
  | { page: 'video-manager' }
  | { page: string }  // 通用: 所有注册表模块

// ─────────── Hash ↔ Route 转换 ───────────

function routeToHash(route: Route): string {
  if (route.page === 'dashboard') return '#/'
  if (route.page === 'scene-composer' && 'course' in route) {
    return `#/scene-composer/${encodeURIComponent(route.course)}/${encodeURIComponent(route.topic)}`
  }
  return `#/${route.page}`
}

function hashToRoute(hash: string): Route {
  const raw = hash.replace(/^#\/?/, '')  // 去掉 #/ 前缀
  if (!raw || raw === '/') return { page: 'dashboard' }

  const parts = raw.split('/')
  if (parts[0] === 'scene-composer' && parts.length >= 3) {
    return {
      page: 'scene-composer',
      course: decodeURIComponent(parts[1]),
      topic: decodeURIComponent(parts[2]),
    }
  }
  return { page: parts[0] }
}

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

// ─────────── 特殊模块页面 (有实际功能) ───────────

const CUSTOM_PAGES: Record<string, string> = {
  'asset-manager': 'custom',
  'block-editor': 'custom',
  'scene-composer': 'custom',
  'video-manager': 'custom',
}

// ─────────── 导航分组: 从注册表 + LAYERS 自动生成 ───────────

interface NavSection {
  label: string
  labelEn?: string
  items: { page: string; icon: ReactNode; label: string; moduleId?: string }[]
}

function buildNavSections(modules: ModuleDef[]): NavSection[] {
  const sections: NavSection[] = [
    { label: '总览', items: [
      { page: 'dashboard', icon: <IconDashboard size={18} />, label: 'Dashboard' },
    ]},
  ]

  // 按 layer 分组
  for (const layer of LAYERS) {
    const layerModules = modules.filter(m => m.layer === layer.id)
    if (layerModules.length === 0) continue
    sections.push({
      label: `${layer.emoji} ${layer.label}`,
      labelEn: layer.labelEn,
      items: layerModules.map(m => ({
        page: m.page,
        icon: resolveIcon(m.icon, 18),
        label: m.label,
        moduleId: m.id,
      })),
    })
  }

  // 输出层
  sections.push({
    label: '⚡ 输出',
    labelEn: 'Output',
    items: [
      { page: 'video-manager', icon: <IconVideo size={18} />, label: '视频管理' },
    ],
  })

  return sections
}

// ─────────── App ───────────

export function App() {
  // 从 URL hash 初始化路由状态
  const [route, setRouteState] = useState<Route>(() => hashToRoute(window.location.hash))
  const navSections = useMemo(() => buildNavSections(DEFAULT_MODULES), [])

  // navigate: 同时更新 state 和 URL hash
  const navigate = useCallback((newRoute: Route) => {
    setRouteState(newRoute)
    const newHash = routeToHash(newRoute)
    if (window.location.hash !== newHash) {
      window.location.hash = newHash
    }
  }, [])

  // 监听浏览器前进/后退
  useEffect(() => {
    const onHashChange = () => {
      setRouteState(hashToRoute(window.location.hash))
    }
    window.addEventListener('hashchange', onHashChange)
    return () => window.removeEventListener('hashchange', onHashChange)
  }, [])

  const contextValue = useMemo(() => ({ route, navigate }), [route, navigate])

  function isActive(page: string) {
    return route.page === page
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
              {DEFAULT_MODULES.length} 模块 · 注册表驱动 · 可配置
            </div>
          </div>

          {/* 导航分组（从注册表自动生成） */}
          <nav style={{ flex: 1, padding: `${MGMT.sp.sm}px ${MGMT.sp.sm}px`, overflowY: 'auto' }}>
            {navSections.map(section => (
              <div key={section.label} style={{ marginBottom: MGMT.sp.sm }}>
                <div style={{
                  fontSize: 10, textTransform: 'uppercase', letterSpacing: 1.5,
                  color: MGMT.gray, padding: '10px 14px 4px', fontWeight: 600,
                  display: 'flex', alignItems: 'center', gap: 6,
                }}>
                  <span>{section.label}</span>
                  {section.labelEn && (
                    <span style={{ fontSize: 8, color: MGMT.gray, opacity: 0.6, letterSpacing: 0.5 }}>
                      {section.labelEn}
                    </span>
                  )}
                </div>
                {section.items.map(item => {
                  const active = isActive(item.page)
                  const handleClick = () => {
                    if (item.page === 'scene-composer') {
                      const first = VIDEO_PROJECTS[0]
                      if (first) navigate({ page: 'scene-composer', course: first.course, topic: first.topic })
                    } else {
                      navigate({ page: item.page } as Route)
                    }
                  }
                  return (
                    <div key={item.page}
                      onClick={handleClick}
                      style={{
                        display: 'flex', alignItems: 'center', gap: 10,
                        padding: '8px 14px', borderRadius: MGMT.radius.md,
                        cursor: 'pointer', marginBottom: 2,
                        background: active ? `${MGMT.gold}0A` : 'transparent',
                        border: `1px solid ${active ? `${MGMT.gold}22` : 'transparent'}`,
                        transition: 'all 0.15s',
                      }}
                    >
                      {/* 模块编号 */}
                      {item.moduleId && (
                        <span style={{
                          fontSize: 8, fontWeight: 700, color: active ? MGMT.gold : MGMT.gray,
                          width: 22, textAlign: 'right', flexShrink: 0, letterSpacing: 0.5,
                          fontFamily: MGMT.codeFontFamily,
                        }}>
                          {item.moduleId}
                        </span>
                      )}
                      <span style={{ display: 'flex', alignItems: 'center' }}>{item.icon}</span>
                      <span style={{
                        fontSize: MGMT.fontSize.body,
                        fontWeight: active ? 600 : 400,
                        color: active ? MGMT.gold : MGMT.white,
                        flex: 1,
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
            Video Lego v3.0 · Registry
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

// ─────────── 页面路由器（注册表驱动） ───────────

function PageRouter({ route }: { route: Route }) {
  // 1. Dashboard
  if (route.page === 'dashboard') return <Dashboard />

  // 2. 特殊模块（有实际功能的自定义页面）
  if (route.page === 'asset-manager') return <AssetManagerPage />
  if (route.page === 'block-editor') return <BlockEditorPage />
  if (route.page === 'scene-composer' && 'course' in route) {
    return <SceneComposerPage course={route.course} topic={route.topic} />
  }
  if (route.page === 'video-manager') return <VideoManagerPage />

  // 3. 通用模块：从注册表查找，用 GenericModulePage 渲染
  const moduleDef = DEFAULT_MODULES.find(m => m.page === route.page)
  if (moduleDef) {
    return <GenericModulePage key={moduleDef.id} moduleDef={moduleDef} />
  }

  // 4. 兜底
  return <Dashboard />
}

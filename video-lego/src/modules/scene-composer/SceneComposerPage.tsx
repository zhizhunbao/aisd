// ═══════════════════════════════════════════════════════════
// M9 场景编排器 — 主页面组件
// Scene Composer — Main Page (orchestration only)
//
// 所有子组件已拆分到 components/ 目录
// ═══════════════════════════════════════════════════════════

import { useState, useCallback, useRef, useEffect } from 'react'
import { MGMT } from '@/theme'
import { useNav } from '@/App'
import { VIDEO_PROJECTS } from '@/data/video-projects'
import type { SceneData } from '@/lib/types'
import { findSceneProject } from './data'
import { emptyScene } from './components/constants'
import { DividerHandle } from './components/shared'
import { SceneList } from './components/SceneList'
import { PreviewCanvas } from './components/PreviewCanvas'
import { EditPanel } from './components/EditPanel'
import { ExportPanel } from './components/ExportPanel'
import { IconFilm, IconUpload } from '@/components/Icons'

export function SceneComposerPage({ course, topic }: { course: string; topic: string }) {
  const { navigate } = useNav()
  const project = VIDEO_PROJECTS.find(p => p.course === course && p.topic === topic)
  const sceneProject = findSceneProject(course, topic)

  const [scenes, setScenes] = useState<SceneData[]>(() => sceneProject?.scenes ? [...sceneProject.scenes] : [])
  const [selIdx, setSelIdx] = useState(0)
  const [selBlock, setSelBlock] = useState(0)
  const [showExport, setShowExport] = useState(false)
  const [dirty, setDirty] = useState(false)

  const update = useCallback((fn: (p: SceneData[]) => SceneData[]) => {
    setScenes(p => { setDirty(true); return fn(p) })
  }, [])

  const current = scenes[selIdx]

  const addScene = useCallback(() => {
    const lastAct = scenes.length > 0 ? scenes[scenes.length - 1].act : ''
    update(p => [...p, emptyScene(lastAct)])
    setSelIdx(scenes.length)
  }, [scenes.length, update])

  const deleteScene = useCallback((i: number) => {
    if (scenes.length <= 1) return
    update(p => p.filter((_, j) => j !== i))
    setSelIdx(j => Math.min(j, scenes.length - 2))
  }, [scenes.length, update])

  const moveScene = useCallback((i: number, d: -1 | 1) => {
    const t = i + d; if (t < 0 || t >= scenes.length) return
    update(p => { const a = [...p]; [a[i], a[t]] = [a[t], a[i]]; return a })
    setSelIdx(t)
  }, [scenes.length, update])

  const updateScene = useCallback((i: number, s: SceneData) => {
    update(p => { const a = [...p]; a[i] = s; return a })
  }, [update])

  if (!project) {
    return (
      <div style={{ padding: 40, textAlign: 'center', color: MGMT.grayLight }}>
        <div style={{ fontSize: 18, marginBottom: 12 }}>未找到 {course}/{topic}</div>
        <button onClick={() => navigate({ page: 'videos' })} style={{
          background: `${MGMT.grayLight}15`, border: `1px solid ${MGMT.grayLight}30`,
          color: MGMT.grayLight, borderRadius: 8, padding: '8px 20px',
          fontSize: 13, cursor: 'pointer', fontFamily: MGMT.fontFamily,
        }}>返回</button>
      </div>
    )
  }

  // ─── 可拖拽调整宽度 ───
  const [leftW, setLeftW] = useState(280)
  const [rightW, setRightW] = useState(320)
  const draggingRef = useRef<'left' | 'right' | null>(null)

  useEffect(() => {
    const onMove = (e: MouseEvent) => {
      if (!draggingRef.current) return
      e.preventDefault()
      if (draggingRef.current === 'left') {
        setLeftW(Math.max(200, Math.min(500, e.clientX - 220)))
      } else {
        setRightW(Math.max(240, Math.min(500, window.innerWidth - e.clientX)))
      }
    }
    const onUp = () => { draggingRef.current = null; document.body.style.cursor = '' }
    document.addEventListener('mousemove', onMove)
    document.addEventListener('mouseup', onUp)
    return () => { document.removeEventListener('mousemove', onMove); document.removeEventListener('mouseup', onUp) }
  }, [])

  return (
    <div style={{ display: 'flex', height: '100%' }}>
      {/* ═══ 左: 场景列表 ═══ */}
      <div style={{
        width: leftW, minWidth: 200, borderRight: `1px solid ${MGMT.border}`,
        display: 'flex', flexDirection: 'column',
        background: MGMT.bgSidebar,
      }}>
        <div style={{ padding: '14px 16px', borderBottom: `1px solid ${MGMT.border}` }}>
          <div style={{
            fontSize: 15, fontWeight: 800, color: MGMT.white,
            display: 'flex', alignItems: 'center', gap: 6,
          }}>
            <IconFilm size={16} /> 场景编排
          </div>
          <div style={{ fontSize: 12, color: MGMT.dimWhite, marginTop: 4 }}>
            {project.title}
          </div>
          {dirty && (
            <div style={{
              fontSize: 11, color: MGMT.gold, marginTop: 4,
              display: 'flex', alignItems: 'center', gap: 4,
            }}>
              <span style={{ fontSize: 8 }}>●</span> 有修改未导出
            </div>
          )}
        </div>
        <SceneList scenes={scenes} sel={selIdx}
          onSelect={i => { setSelIdx(i); setSelBlock(0) }}
          onMove={moveScene} onDelete={deleteScene} onAdd={addScene} />
        <div style={{
          padding: '8px 10px', borderTop: `1px solid ${MGMT.border}`,
          display: 'flex', gap: 6,
        }}>
          <button onClick={() => setShowExport(true)}
            style={{
              flex: 1, background: `${MGMT.gold}15`, border: `1px solid ${MGMT.gold}30`,
              color: MGMT.gold, borderRadius: 6, padding: 8, fontSize: 12,
              fontWeight: 700, cursor: 'pointer', fontFamily: MGMT.fontFamily,
              display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 4,
            }}>
            <IconUpload size={14} /> 导出
          </button>
          <button onClick={() => navigate({ page: 'videos' })}
            style={{
              background: `${MGMT.grayLight}10`, border: `1px solid ${MGMT.border}`,
              color: MGMT.grayLight, borderRadius: 6, padding: '8px 12px', fontSize: 12,
              cursor: 'pointer', fontFamily: MGMT.fontFamily,
            }}>
            返回
          </button>
        </div>
      </div>

      <DividerHandle side="left" draggingRef={draggingRef} />

      {/* ═══ 中: 画布 ═══ */}
      {current ? (
        <PreviewCanvas scene={current} selBlock={selBlock} onSelectBlock={setSelBlock}
          onChangeScene={s => updateScene(selIdx, s)} />
      ) : (
        <div style={{
          flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center',
          flexDirection: 'column', gap: 12, color: MGMT.grayLight,
        }}>
          <IconFilm size={36} style={{ opacity: 0.3 }} />
          <span style={{ fontSize: 14 }}>点击「+ 添加场景」开始</span>
        </div>
      )}

      {/* ═══ 右: 编辑面板 ═══ */}
      {current && (
        <>
          <DividerHandle side="right" draggingRef={draggingRef} />
          <div style={{
            width: rightW, minWidth: 240, borderLeft: `1px solid ${MGMT.border}`,
            overflowY: 'auto', background: MGMT.bgSidebar,
          }}>
            <EditPanel scene={current} selBlock={selBlock}
              onChange={s => updateScene(selIdx, s)} onSelectBlock={setSelBlock} />
          </div>
        </>
      )}

      {showExport && <ExportPanel scenes={scenes} meta={{ course, topic, title: project.title }} onClose={() => setShowExport(false)} />}
    </div>
  )
}

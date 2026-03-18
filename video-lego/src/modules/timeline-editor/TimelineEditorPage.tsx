// ═══════════════════════════════════════════════════════════
// M10 时间线编辑器 — 三级侧栏（SVG 图标版）
// ═══════════════════════════════════════════════════════════

import { useState } from 'react'
import { MGMT } from '@/theme'
import { IconClock, IconFilm, IconWaves } from '@/components/Icons'
import {
  ModuleLayout, ModuleHeader, ModuleSidebar, RightPlaceholder,
  type SidebarCategory,
} from '@/components/ModuleLayout'

const COLOR = '#e67e22'

const CATEGORIES: SidebarCategory[] = [
  {
    label: '时序编排',
    icon: <IconClock size={12} />,
    subModules: [
      { id: 'M10.1', label: '场景时序', leaves: [
        { id: 'scene_order', label: '场景排序' },
        { id: 'duration_adj', label: '时长调节' },
        { id: 'gap_setting', label: '间隙设置' },
      ]},
      { id: 'M10.4', label: '总时长计算', leaves: [
        { id: 'total_frames', label: '总帧数' },
        { id: 'target_dur', label: '目标时长' },
        { id: 'overflow_check', label: '溢出检查' },
      ]},
    ],
  },
  {
    label: '音轨对齐',
    icon: <IconWaves size={12} />,
    subModules: [
      { id: 'M10.2', label: '旁白对齐', leaves: [
        { id: 'time_mapping', label: '时间映射' },
        { id: 'auto_align', label: '自动对齐' },
        { id: 'manual_tweak', label: '手动微调' },
      ]},
      { id: 'M10.3', label: '字幕时序', leaves: [
        { id: 'sub_gen', label: '字幕生成' },
        { id: 'time_calibrate', label: '时间校准' },
      ]},
    ],
  },
]

export function TimelineEditorPage() {
  const [selected, setSelected] = useState<string | null>(null)
  return (
    <ModuleLayout
      left={<>
        <ModuleHeader icon={<IconClock size={16} />} title="M10 时间线" subtitle="Timeline Editor · Mayer Temporal" color={COLOR} />
        <ModuleSidebar categories={CATEGORIES} color={COLOR} selectedId={selected} onSelect={setSelected} />
      </>}
      center={
        <>
          <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <div style={{ textAlign: 'center', color: MGMT.grayLight, maxWidth: 440 }}>
              <div style={{ opacity: 0.15, marginBottom: 16, display: 'flex', justifyContent: 'center' }}>
                <IconClock size={64} />
              </div>
              <div style={{ fontSize: 18, fontWeight: 600, color: MGMT.dimWhite, marginBottom: 8 }}>时间线编辑器</div>
              <div style={{ fontSize: 13, lineHeight: 1.8 }}>
                将场景排列在时间线上<br />拖拽排序 · 调整时长 · 多轨道预览<br />导出为 Remotion Composition
              </div>
              <div style={{
                marginTop: 20, padding: '8px 16px', borderRadius: 6,
                background: `${COLOR}10`, border: `1px solid ${COLOR}20`,
                color: COLOR, fontSize: 12, display: 'inline-flex', alignItems: 'center', gap: 6,
              }}>⚡ 模块开发中</div>
            </div>
          </div>
          <div style={{
            height: 140, borderTop: `1px solid ${MGMT.border}`,
            background: `${MGMT.white}02`, padding: '12px 24px', flexShrink: 0,
          }}>
            <div style={{ fontSize: 10, color: MGMT.grayLight, textTransform: 'uppercase', letterSpacing: 1, marginBottom: 8 }}>轨道预览</div>
            {['视觉', '旁白', '音频'].map(track => (
              <div key={track} style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 6 }}>
                <span style={{ fontSize: 10, color: MGMT.grayLight, width: 40, textAlign: 'right' }}>{track}</span>
                <div style={{
                  flex: 1, height: 28, borderRadius: 4,
                  background: `${MGMT.white}04`, border: `1px solid ${MGMT.border}`,
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                }}>
                  <IconFilm size={12} style={{ color: MGMT.grayLight, opacity: 0.3 }} />
                </div>
              </div>
            ))}
          </div>
        </>
      }
      right={<RightPlaceholder icon={<IconClock size={24} />} label="时间线属性" />}
    />
  )
}

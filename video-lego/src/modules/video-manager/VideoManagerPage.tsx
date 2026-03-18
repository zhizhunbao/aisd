// ═══════════════════════════════════════════════════════════
// 视频管理 — 主页面（合并视频列表 + 流水线）
// Video Manager — Main page (merged VideoList + Pipeline)
//
// 功能规划:
//   - 视频项目列表 + 进度概览
//   - 选中项目 → 右侧流水线详情
//   - 各阶段状态 (脚本→素材→积木→场景→时间线→渲染)
//   - 一键渲染 / 导出
// ═══════════════════════════════════════════════════════════

import { MGMT } from '@/theme'
import { VIDEO_PROJECTS } from '@/data/video-projects'
import { IconVideo, IconZap, IconChevronRight, IconCheck } from '@/components/Icons'
import { useState } from 'react'

export function VideoManagerPage() {
  const [selectedIdx, setSelectedIdx] = useState(0)
  const project = VIDEO_PROJECTS[selectedIdx]

  return (
    <div style={{ display: 'flex', height: '100%' }}>
      {/* 左: 项目列表 */}
      <div style={{
        width: 320, minWidth: 320, borderRight: `1px solid ${MGMT.border}`,
        display: 'flex', flexDirection: 'column',
      }}>
        <div style={{ padding: '16px 14px', borderBottom: `1px solid ${MGMT.border}` }}>
          <div style={{ fontSize: 14, fontWeight: 700, display: 'flex', alignItems: 'center', gap: 8 }}>
            <IconVideo size={18} style={{ color: '#e74c3c' }} /> 视频管理
          </div>
          <div style={{ fontSize: 11, color: MGMT.grayLight, marginTop: 4 }}>{VIDEO_PROJECTS.length} 个项目</div>
        </div>

        <div style={{ flex: 1, overflowY: 'auto' }}>
          {VIDEO_PROJECTS.map((p, i) => {
            const isSelected = i === selectedIdx
            return (
              <div key={i} onClick={() => setSelectedIdx(i)}
                style={{
                  padding: '12px 14px', cursor: 'pointer',
                  borderLeft: `3px solid ${isSelected ? '#e74c3c' : 'transparent'}`,
                  background: isSelected ? '#e74c3c08' : 'transparent',
                  borderBottom: `1px solid ${MGMT.border}`,
                  transition: 'all 0.1s',
                }}
                onMouseEnter={e => { if (!isSelected) e.currentTarget.style.background = `${MGMT.white}04` }}
                onMouseLeave={e => { if (!isSelected) e.currentTarget.style.background = isSelected ? '#e74c3c08' : 'transparent' }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <span style={{ fontSize: 14, fontWeight: 600, flex: 1, color: isSelected ? MGMT.white : MGMT.dimWhite }}>
                    {p.title}
                  </span>
                  <IconChevronRight size={12} style={{ color: MGMT.grayLight, opacity: isSelected ? 1 : 0 }} />
                </div>
                <div style={{ fontSize: 11, color: MGMT.grayLight, marginTop: 2 }}>{p.course} · {p.topic}</div>
              </div>
            )
          })}
        </div>
      </div>

      {/* 右: 项目详情 + 流水线 */}
      <div style={{ flex: 1, overflow: 'auto', padding: 24 }}>
        {project ? (
          <>
            <div style={{ fontSize: 22, fontWeight: 700, marginBottom: 4 }}>{project.title}</div>
            <div style={{ fontSize: 13, color: MGMT.grayLight, marginBottom: 24 }}>
              {project.course} · {project.topic} · {project.scenes?.length || 0} 场景
            </div>

            {/* 流水线阶段 */}
            <div style={{ fontSize: 10, color: MGMT.grayLight, textTransform: 'uppercase', letterSpacing: 1, marginBottom: 12 }}>
              制作流水线
            </div>
            {[
              { label: '脚本编辑', color: '#4ea8de', done: true },
              { label: '素材准备', color: '#2ecc71', done: true },
              { label: '积木组装', color: '#ffd700', done: false },
              { label: '场景编排', color: '#e67e22', done: false },
              { label: '时间线', color: '#9b59b6', done: false },
              { label: '渲染导出', color: '#e74c3c', done: false },
            ].map((stage, i) => (
              <div key={i} style={{
                display: 'flex', alignItems: 'center', gap: 12, padding: '12px 16px',
                background: `${MGMT.white}04`, borderRadius: 8, marginBottom: 8,
                border: `1px solid ${stage.done ? `${stage.color}20` : MGMT.border}`,
              }}>
                <div style={{
                  width: 24, height: 24, borderRadius: '50%',
                  background: stage.done ? `${stage.color}20` : `${MGMT.white}06`,
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                }}>
                  {stage.done
                    ? <IconCheck size={14} style={{ color: stage.color }} />
                    : <span style={{ fontSize: 11, color: MGMT.grayLight, fontWeight: 600 }}>{i + 1}</span>
                  }
                </div>
                <span style={{
                  fontSize: 13, flex: 1,
                  color: stage.done ? MGMT.white : MGMT.grayLight,
                  fontWeight: stage.done ? 600 : 400,
                }}>
                  {stage.label}
                </span>
                <span style={{
                  fontSize: 10, padding: '2px 8px', borderRadius: 4,
                  background: stage.done ? `${stage.color}10` : `${MGMT.white}06`,
                  color: stage.done ? stage.color : MGMT.grayLight,
                }}>
                  {stage.done ? '已完成' : '待处理'}
                </span>
              </div>
            ))}
          </>
        ) : (
          <div style={{ textAlign: 'center', color: MGMT.grayLight, paddingTop: 80 }}>
            <IconVideo size={48} style={{ opacity: 0.2, marginBottom: 12 }} />
            <div>选择项目查看详情</div>
          </div>
        )}
      </div>
    </div>
  )
}

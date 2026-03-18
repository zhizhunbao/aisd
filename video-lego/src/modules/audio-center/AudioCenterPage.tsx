// ═══════════════════════════════════════════════════════════
// M5 音频中心 — 三级侧栏（SVG 图标版）
// ═══════════════════════════════════════════════════════════

import { useState } from 'react'
import { IconVolume, IconMusic, IconMic, IconWaves } from '@/components/Icons'
import {
  ModuleLayout, ModuleHeader, ModuleSidebar, CenterPlaceholder, RightPlaceholder,
  type SidebarCategory,
} from '@/components/ModuleLayout'

const COLOR = '#9b59b6'

const CATEGORIES: SidebarCategory[] = [
  {
    label: '语音',
    icon: <IconMic size={12} />,
    subModules: [
      { id: 'M5.1', label: 'TTS 合成', leaves: [
        { id: 'voice_clone', label: '声音克隆' },
        { id: 'standard_tts', label: '标准语音' },
        { id: 'multi_lang', label: '多语言' },
      ]},
      { id: 'M5.5', label: '时间戳', leaves: [
        { id: 'sentence_ts', label: '句级时间戳' },
        { id: 'word_ts', label: '词级时间戳' },
      ]},
    ],
  },
  {
    label: '音效',
    icon: <IconMusic size={12} />,
    subModules: [
      { id: 'M5.2', label: 'BGM', leaves: [
        { id: 'light_music', label: '轻音乐' },
        { id: 'ambient_bgm', label: '氛围音' },
        { id: 'rhythmic', label: '节奏感' },
      ]},
      { id: 'M5.3', label: '转场音效', leaves: [
        { id: 'whoosh', label: 'whoosh' },
        { id: 'ding', label: 'ding' },
        { id: 'swoosh', label: 'swoosh' },
      ]},
      { id: 'M5.4', label: '提示音', leaves: [
        { id: 'correct', label: '正确' },
        { id: 'error', label: '错误' },
        { id: 'remind', label: '提醒' },
      ]},
    ],
  },
]

export function AudioCenterPage() {
  const [selected, setSelected] = useState<string | null>(null)
  return (
    <ModuleLayout
      left={<>
        <ModuleHeader icon={<IconVolume size={16} />} title="M5 音频中心" subtitle="Audio Center · Mayer Modality" color={COLOR} />
        <ModuleSidebar categories={CATEGORIES} color={COLOR} selectedId={selected} onSelect={setSelected} />
      </>}
      center={<CenterPlaceholder icon={<IconVolume size={64} />} title="音频中心"
        lines={['TTS 合成 · BGM 管理', '转场音效 · 提示音', 'Mayer Modality + Voice 原则']} color={COLOR} />}
      right={<RightPlaceholder icon={<IconWaves size={24} />} label="音频播放器" />}
    />
  )
}

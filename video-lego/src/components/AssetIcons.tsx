// ═══════════════════════════════════════════════════════════
// 素材图标映射 — emoji → SVG 图标集
// Asset Icon Mapping — emoji to SVG icons
//
// 使用方式:
//   <AssetCatIcon catId="narration" size={18} />
//   <AssetSubIcon catId="text_overlay" subId="formula" size={14} />
//   <SourceIcon type="textbook" size={12} />
// ═══════════════════════════════════════════════════════════

import React from 'react'
import {
  IconMic, IconPalette2, IconType, IconVolume, IconDatabase,
  IconBookOpen, IconShuffle, IconFileCode, IconClock, IconMusic,
  IconZap, IconAlarmClock, IconWaves, IconMonitorPlay, IconImage2,
  IconCamera, IconPenTool, IconQuote, IconChart, IconBlocks,
  IconListChecks, IconHash, IconCode2, IconTable, IconSplitH,
  IconBookmark, IconInfo, IconLayers, IconClapperboard, IconGauge,
  IconRewind, IconSparkles, IconFormula, IconSearch, IconPackage,
  IconCpu, IconGitBranch, IconBinary, IconShield, IconTrendingDown,
  IconTarget, IconActivity, IconCalculator,
} from './Icons'
import { User } from 'lucide-react'
import type { IconProps } from './Icons'

// ─── 分类图标 Category Icons ───

const CAT_ICONS: Record<string, React.FC<IconProps>> = {
  // 新 ID
  image:         IconImage2,
  person:        User as React.FC<IconProps>,
  formula:       IconFormula,
  code:          IconCode2,
  animation:     IconClapperboard,
  audio:         IconVolume,
  data:          IconDatabase,
  transition:    IconShuffle,
  // 旧 ID (兼容)
  narration:     IconMic,
  visual:        IconPalette2,
  text_overlay:  IconType,
  reference:     IconBookOpen,
}

/** 素材分类 SVG 图标 */
export function AssetCatIcon({ catId, ...props }: { catId: string } & IconProps) {
  const Icon = CAT_ICONS[catId] || IconPackage
  return <Icon {...props} />
}

// ─── 子分类图标 Sub-Category Icons ───

const SUB_ICONS: Record<string, React.FC<IconProps>> = {
  // narration
  hook:          IconZap,
  explain:       IconMic,
  transition_sub: IconShuffle,
  summary:       IconListChecks,
  aside:         IconInfo,
  // visual
  animation:     IconClapperboard,
  diagram:       IconLayers,
  chart:         IconChart,
  screencast:    IconMonitorPlay,
  illustration:  IconPenTool,
  photo:         IconCamera,
  // text_overlay
  title:         IconHash,
  bullet:        IconListChecks,
  formula:       IconFormula,
  code:          IconCode2,
  caption:       IconType,
  quote:         IconQuote,
  // audio
  bgm:           IconMusic,
  sfx:           IconZap,
  alert:         IconAlarmClock,
  ambient:       IconWaves,
  // data
  dataset:       IconDatabase,
  timeline:      IconClock,
  comparison:    IconSplitH,
  code_sample:   IconFileCode,
  table:         IconTable,
  // reference
  textbook:      IconBookOpen,
  paper:         IconFileCode,
  docs:          IconBookmark,
  wiki:          IconInfo,
  // transition
  chapter_card:  IconLayers,
  progress:      IconGauge,
  recap:         IconRewind,
  bridge_anim:   IconSparkles,
  // formula sub-categories (公式子分类)
  calculus:      IconFormula,
  linear:        IconLayers,
  probability:   IconChart,
  statistics:    IconChart,
  optimization:  IconGauge,
  information:   IconInfo,
  deep_learning: IconCpu,
  sequence_model: IconGitBranch,
  ml_algorithm:  IconBinary,
  regularization: IconShield,
  loss_function: IconTrendingDown,
  evaluation:    IconTarget,
  distribution:  IconActivity,
  basic_math:    IconCalculator,
}

/** 素材子分类 SVG 图标 */
export function AssetSubIcon({ subId, ...props }: { subId: string } & IconProps) {
  const Icon = SUB_ICONS[subId] || IconBlocks
  return <Icon {...props} />
}

// ─── 来源类型图标 Source Icons ───

const SOURCE_ICON_MAP: Record<string, React.FC<IconProps>> = {
  textbook:      IconBookOpen,
  paper:         IconFileCode,
  wikipedia:     IconInfo,
  documentation: IconBookmark,
  course:        IconLayers,
  original:      IconPenTool,
}

/** 来源类型 SVG 图标 */
export function SourceIcon({ type, ...props }: { type: string } & IconProps) {
  const Icon = SOURCE_ICON_MAP[type] || IconBookmark
  return <Icon {...props} />
}

// ─── 旁白语气图标 Tone Icons ───

const TONE_ICONS: Record<string, React.FC<IconProps>> = {
  casual:    IconMic,
  serious:   IconBookOpen,
  humorous:  IconSparkles,
  dramatic:  IconZap,
}

/** 旁白语气 SVG 图标 */
export function ToneIcon({ tone, ...props }: { tone: string } & IconProps) {
  const Icon = TONE_ICONS[tone] || IconMic
  return <Icon {...props} />
}

// ─── 视觉类型图标 ───

const VISUAL_TYPE_ICONS: Record<string, React.FC<IconProps>> = {
  animation:     IconClapperboard,
  diagram:       IconLayers,
  chart:         IconChart,
  screencast:    IconMonitorPlay,
  illustration:  IconPenTool,
  photo:         IconCamera,
}

export function VisualTypeIcon({ type, ...props }: { type: string } & IconProps) {
  const Icon = VISUAL_TYPE_ICONS[type] || IconImage2
  return <Icon {...props} />
}

// ─── 音频类型图标 ───

const AUDIO_TYPE_ICONS: Record<string, React.FC<IconProps>> = {
  bgm:     IconMusic,
  sfx:     IconZap,
  alert:   IconAlarmClock,
  ambient: IconWaves,
}

export function AudioTypeIcon({ type, ...props }: { type: string } & IconProps) {
  const Icon = AUDIO_TYPE_ICONS[type] || IconVolume
  return <Icon {...props} />
}

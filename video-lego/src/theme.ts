// ═══════════════════════════════════════════════════════════
// 管理系统主题 — 独立于视频积木的 UI 样式参数
// Management UI Theme — separate from video block styles
// ═══════════════════════════════════════════════════════════

export const MGMT = {
  // 背景色 Backgrounds
  bg: '#0a0a14',
  bgSidebar: '#0f0f1e',
  bgCard: '#151528',
  bgCardHover: '#1c1c38',
  bgInput: '#12122a',

  // 主色调 Accents
  gold: '#ffd700',
  blue: '#4ea8de',
  red: '#e74c3c',
  green: '#2ecc71',
  purple: '#9b59b6',
  orange: '#e67e22',

  // 文字色 Text
  white: '#eeeeee',
  dimWhite: '#aaaaaa',
  gray: '#666666',
  grayLight: '#888888',

  // 边框 Borders
  border: '#1e1e3a',
  borderHover: 'rgba(255,255,255,0.1)',

  // 字号 Font sizes
  fontSize: {
    h1: 28,
    h2: 22,
    h3: 18,
    body: 14,
    small: 12,
    tiny: 10,
    code: 13,
  },

  // 间距 Spacing
  sp: {
    xs: 4,
    sm: 8,
    md: 16,
    lg: 24,
    xl: 32,
    xxl: 48,
  },

  // 圆角 Border radius
  radius: {
    sm: 6,
    md: 10,
    lg: 14,
  },

  // 侧边栏 Sidebar
  sidebar: {
    width: 240,
  },

  // 字体 Fonts
  fontFamily: 'Noto Sans SC, Inter, sans-serif',
  codeFontFamily: 'JetBrains Mono, Consolas, monospace',

  // 分类颜色 Category colors (视频制作维度)
  categoryColors: {
    narration: '#4ea8de',
    visual: '#2ecc71',
    text_overlay: '#ffd700',
    audio: '#9b59b6',
    data: '#e67e22',
    reference: '#888888',
    transition: '#1abc9c',
  } as Record<string, string>,

  // 状态颜色 Status colors
  statusColors: {
    ready: '#2ecc71',
    todo: '#666666',
    in_progress: '#4ea8de',
    review: '#e67e22',
    rework: '#e74c3c',
  } as Record<string, string>,
} as const;

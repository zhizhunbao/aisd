// ═══════════════════════════════════════════════════════════
// 全局主题 — 配色、字号、安全区、动画参数
// Global Theme — Colors, Typography, Safe Zones, Animation
// ═══════════════════════════════════════════════════════════

export const THEME = {
  // 背景色 Background
  bg: '#1a1a2e',
  bgLight: '#16213e',

  // 主色调 Primary colors
  gold: '#ffd700',       // 结论/重点 Conclusions
  blue: '#4ea8de',       // 概念/定义 Concepts
  red: '#e74c3c',        // 警告/转折 Warnings
  green: '#2ecc71',      // 正确/通过 Correct

  // 辅助色 Secondary
  gray: '#888888',       // 标注/注释 Annotations
  white: '#f0f0f0',      // 正文 Body text
  dimWhite: '#cccccc',   // 次要文字 Secondary text

  // 字体大小 Font sizes
  fontSize: {
    title: 72,           // 大标题 Big title
    subtitle: 48,        // 副标题 Subtitle
    body: 36,            // 正文 Body
    label: 24,           // 标签 Label
    code: 28,            // 代码 Code
  },

  // 字体族 Font family
  fontFamily: 'Noto Sans SC, sans-serif',
  codeFontFamily: 'JetBrains Mono, Consolas, monospace',

  // 安全区 Safe zones
  subtitleSafeY: 918,    // 1080 * 0.85 — 底部 15% 留给字幕
  padding: 60,           // 画面边距

  // 动画参数 Animation params
  fadeInDuration: 15,    // frames (0.5s @ 30fps)
  staggerDelay: 8,       // frames between staggered elements
} as const;

export const CANVAS = {
  width: 1920,
  height: 1080,
  fps: 30,
} as const;

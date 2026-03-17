// ═══════════════════════════════════════════════════════════
// 积木动画注入接口 — View 与 Motion 的契约
// Animation Injection Interface — Contract between View & Motion
// ═══════════════════════════════════════════════════════════

import type { CSSProperties } from 'react';

/**
 * 单容器动画注入
 * Single-container animation injection
 * 用于只有一个主容器的积木（FormulaBlock, CodeBlock, ImageDisplay）
 */
export interface AnimProps {
  /** 容器动画样式 Container animation style (opacity, transform, etc.) */
  containerStyle?: CSSProperties;
}

/**
 * 多元素交错动画注入
 * Multi-item stagger animation injection
 * 用于包含多个子元素的积木（FormulaDerivation, Timeline, ProgressBars, StatCards, ComparisonSplit）
 */
export interface StaggerAnimProps extends AnimProps {
  /** 每个子元素的动画样式生成器 Per-item animation style */
  getItemStyle?: (index: number) => CSSProperties;
}

/**
 * 复杂动画参数注入
 * Complex animation parameter injection
 * 用于动画控制渲染逻辑的积木（UCurve — 控制可见点数、区域透明度等）
 */
export interface ChartAnimProps {
  /** 坐标轴透明度 Axis opacity (0-1) */
  axisOpacity?: number;
  /** 可见数据点数 Number of visible data points */
  visiblePointCount?: number;
  /** 区域标注透明度 Zone opacity (0-1) */
  zoneOpacity?: number;
  /** 最优点透明度 Best point opacity (0-1) */
  bestOpacity?: number;
  /** 最优点缩放 Best point scale */
  bestScale?: number;
}

// ═══════════════════════════════════════════════════════════
// UCurve — 动画层（坐标轴 → 曲线绘制 → 区域 → 最优点）
// UCurve — Motion layer (axes → curve draw → zones → best point)
// ═══════════════════════════════════════════════════════════

import React from 'react';
import { interpolate, useCurrentFrame, spring, useVideoConfig } from 'remotion';
import { UCurveView } from './UCurve.view';
import type { UCurveData } from '../../lib/types';

export const UCurve: React.FC<UCurveData> = (data) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const axisOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });
  const curveProgress = interpolate(frame, [25, 120], [0, 1], { extrapolateRight: 'clamp' });
  const visiblePointCount = Math.floor(curveProgress * data.points.length);
  const zoneOpacity = interpolate(frame, [60, 90], [0, 1], { extrapolateRight: 'clamp' });
  const bestOpacity = interpolate(frame, [140, 165], [0, 1], { extrapolateRight: 'clamp' });
  const bestScale = spring({ frame: frame - 140, fps, config: { damping: 12 } });

  return (
    <UCurveView
      {...data}
      axisOpacity={axisOpacity}
      visiblePointCount={visiblePointCount}
      zoneOpacity={zoneOpacity}
      bestOpacity={bestOpacity}
      bestScale={bestScale}
    />
  );
};

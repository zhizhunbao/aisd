// ═══════════════════════════════════════════════════════════
// FormulaBlock — 动画层（Remotion hooks → 注入 containerStyle）
// FormulaBlock — Motion layer (Remotion hooks → inject style)
// ═══════════════════════════════════════════════════════════

import React from 'react';
import { interpolate, useCurrentFrame, spring, useVideoConfig } from 'remotion';
import { FormulaBlockView } from './FormulaBlock.view';
import type { FormulaBlockData } from '../../lib/types';

export const FormulaBlock: React.FC<FormulaBlockData & { startFrame?: number }> = ({
  startFrame = 10,
  ...data
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const opacity = interpolate(frame, [startFrame, startFrame + 20], [0, 1], {
    extrapolateRight: 'clamp',
    extrapolateLeft: 'clamp',
  });
  const scale = spring({
    frame: frame - startFrame,
    fps,
    config: { damping: 14, stiffness: 80 },
  });
  const safeScale = Math.max(0.01, Math.min(scale, 2));

  return (
    <FormulaBlockView
      {...data}
      containerStyle={{
        opacity,
        transform: `scale(${safeScale})`,
      }}
    />
  );
};

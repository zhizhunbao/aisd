// ═══════════════════════════════════════════════════════════
// FormulaDerivation — 动画层（逐步滑入 + 高亮脉冲）
// FormulaDerivation — Motion layer (stagger slide-in + glow pulse)
// ═══════════════════════════════════════════════════════════

import React from 'react';
import { interpolate, useCurrentFrame, spring, useVideoConfig } from 'remotion';
import { FormulaDerivationView } from './FormulaDerivation.view';
import type { FormulaDerivationData } from '../../lib/types';

const STEP_STAGGER = 25;
const FIRST_STEP_FRAME = 15;

export const FormulaDerivation: React.FC<FormulaDerivationData> = (data) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <FormulaDerivationView
      {...data}
      getItemStyle={(i) => {
        const stepStart = FIRST_STEP_FRAME + i * STEP_STAGGER;

        const opacity = interpolate(frame, [stepStart, stepStart + 15], [0, 1], {
          extrapolateRight: 'clamp',
          extrapolateLeft: 'clamp',
        });
        const slideY = interpolate(frame, [stepStart, stepStart + 15], [20, 0], {
          extrapolateRight: 'clamp',
          extrapolateLeft: 'clamp',
        });
        const glowScale = spring({
          frame: frame - stepStart,
          fps,
          config: { damping: 12, stiffness: 60 },
        });
        const safeGlow = Math.max(0.01, Math.min(glowScale, 2));

        const isHighlighted = data.steps[i]?.highlight;

        return {
          opacity,
          transform: `translateY(${slideY}px) scale(${isHighlighted ? safeGlow : 1})`,
        };
      }}
    />
  );
};

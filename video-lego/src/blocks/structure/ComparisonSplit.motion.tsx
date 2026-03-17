// ComparisonSplit — 动画层（左右滑入）
import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';
import { ComparisonSplitView } from './ComparisonSplit.view';
import type { ComparisonSplitData } from '../../lib/types';

export const ComparisonSplit: React.FC<ComparisonSplitData & { startFrame?: number }> = ({
  startFrame = 10,
  ...data
}) => {
  const frame = useCurrentFrame();

  return (
    <ComparisonSplitView
      {...data}
      getItemStyle={(ci) => {
        const colDelay = startFrame + ci * 10;
        const opacity = interpolate(frame, [colDelay, colDelay + 15], [0, 1], { extrapolateRight: 'clamp', extrapolateLeft: 'clamp' });
        const slideX = interpolate(frame, [colDelay, colDelay + 15], [ci === 0 ? -30 : 30, 0], { extrapolateRight: 'clamp', extrapolateLeft: 'clamp' });
        return { opacity, transform: `translateX(${slideX}px)` };
      }}
    />
  );
};

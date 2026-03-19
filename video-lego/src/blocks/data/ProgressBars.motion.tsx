// ProgressBars — 动画层
import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';
import { ProgressBarsView } from './ProgressBars.view';
import type { ProgressBarData } from '../../lib/types';

export const ProgressBars: React.FC<{ bars: ProgressBarData[]; startFrame?: number }> = ({
  bars,
  startFrame = 10,
}) => {
  const frame = useCurrentFrame();

  const containerOpacity = interpolate(frame, [startFrame, startFrame + 20], [0, 1], {
    extrapolateRight: 'clamp', extrapolateLeft: 'clamp',
  });

  return (
    <ProgressBarsView
      bars={bars}
      containerStyle={{ opacity: containerOpacity }}
      getBarProgress={(bi) => {
        const barDelay = startFrame + bi * 15;
        return interpolate(frame, [barDelay + 5, barDelay + 30], [0, bars[bi].value], {
          extrapolateRight: 'clamp', extrapolateLeft: 'clamp',
        });
      }}
    />
  );
};

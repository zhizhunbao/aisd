// Timeline — 动画层（逐条淡入）
import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';
import { TimelineView } from './Timeline.view';
import type { TimelineData } from '../../lib/types';

export const Timeline: React.FC<TimelineData & { startFrame?: number }> = ({
  startFrame = 10,
  ...data
}) => {
  const frame = useCurrentFrame();

  const containerOpacity = interpolate(frame, [startFrame, startFrame + 20], [0, 1], {
    extrapolateRight: 'clamp', extrapolateLeft: 'clamp',
  });

  return (
    <TimelineView
      {...data}
      containerStyle={{ opacity: containerOpacity }}
      getItemStyle={(ei) => {
        const evtDelay = startFrame + ei * 12;
        const opacity = interpolate(frame, [evtDelay, evtDelay + 12], [0, 1], { extrapolateRight: 'clamp', extrapolateLeft: 'clamp' });
        return { opacity };
      }}
    />
  );
};

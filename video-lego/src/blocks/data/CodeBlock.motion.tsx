// CodeBlock — 动画层
import React from 'react';
import { interpolate, useCurrentFrame, spring, useVideoConfig } from 'remotion';
import { CodeBlockView } from './CodeBlock.view';
import type { CodeBlockData } from '../../lib/types';

export const CodeBlock: React.FC<CodeBlockData & { startFrame?: number }> = ({
  startFrame = 10,
  ...data
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const opacity = interpolate(frame, [startFrame, startFrame + 20], [0, 1], { extrapolateRight: 'clamp', extrapolateLeft: 'clamp' });
  const scale = spring({ frame: frame - startFrame, fps, config: { damping: 14, stiffness: 80 } });
  const safeScale = Math.max(0.01, Math.min(scale, 2));

  return (
    <CodeBlockView
      {...data}
      containerStyle={{ opacity, transform: `scale(${safeScale})` }}
    />
  );
};

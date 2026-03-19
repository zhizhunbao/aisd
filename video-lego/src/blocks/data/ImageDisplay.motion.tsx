// ImageDisplay — 动画层（Remotion 专用，使用 Img + staticFile）
import React from 'react';
import { Img, interpolate, useCurrentFrame, spring, useVideoConfig, staticFile } from 'remotion';
import { THEME } from '../../lib/video-theme';
import type { ImageDisplayData } from '../../lib/types';

export const ImageDisplay: React.FC<ImageDisplayData & { startFrame?: number }> = ({
  src,
  caption,
  maxHeight = 420,
  startFrame = 10,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const opacity = interpolate(frame, [startFrame, startFrame + 20], [0, 1], { extrapolateRight: 'clamp', extrapolateLeft: 'clamp' });
  const scale = spring({ frame: frame - startFrame, fps, config: { damping: 14, stiffness: 80 } });
  const safeScale = Math.max(0.01, Math.min(scale, 2));

  return (
    <div style={{ opacity, transform: `scale(${safeScale})`, display: 'flex', flexDirection: 'column', alignItems: 'center', width: '100%' }}>
      <Img
        src={src.startsWith('http') ? src : staticFile(src)}
        style={{ maxWidth: '90%', maxHeight, borderRadius: 16, border: `1px solid ${THEME.gray}30`, objectFit: 'contain' }}
      />
      {caption && (
        <div style={{ color: THEME.dimWhite, fontSize: 18, marginTop: 10, fontFamily: THEME.fontFamily, textAlign: 'center' }}>
          {caption}
        </div>
      )}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════
// ImageDisplay — 纯视觉层
// ═══════════════════════════════════════════════════════════

import React from 'react';
import { THEME } from '../../lib/video-theme';
import type { ImageDisplayData } from '../../lib/types';
import type { AnimProps } from '../../lib/anim-types';

export const ImageDisplayView: React.FC<ImageDisplayData & AnimProps & {
  /** 图片 URL（已解析）— Remotion 用 staticFile()，管理 UI 用普通 URL */
  resolvedSrc?: string;
}> = ({
  src,
  caption,
  maxHeight = 420,
  containerStyle,
  resolvedSrc,
}) => {
  const imgSrc = resolvedSrc || src;

  return (
    <div style={{
      display: 'flex', flexDirection: 'column', alignItems: 'center', width: '100%',
      ...containerStyle,
    }}>
      <img
        src={imgSrc}
        style={{
          maxWidth: '90%', maxHeight,
          borderRadius: 16, border: `1px solid ${THEME.gray}30`,
          objectFit: 'contain',
        }}
      />
      {caption && (
        <div style={{ color: THEME.dimWhite, fontSize: 18, marginTop: 10, fontFamily: THEME.fontFamily, textAlign: 'center' }}>
          {caption}
        </div>
      )}
    </div>
  );
};

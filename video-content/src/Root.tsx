// ═══════════════════════════════════════════════════════════
// Remotion 根组件 — 注册所有视频 Composition
// Root — Register all video compositions
// 加新视频 = 导入数据 + 加一行 Composition
// ═══════════════════════════════════════════════════════════

import React from 'react';
import { Composition } from 'remotion';
import { VideoEngine } from './lib/engine/VideoEngine';
import { CANVAS } from '@lego/video-theme';

// 导入视频数据 Import video data
import { KNN_VIDEO } from './videos/machine-learning/knn/video.data';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {/* ══════ 视频 Compositions ══════ */}
      <Composition
        id="knn"
        component={VideoEngine}
        defaultProps={{ data: KNN_VIDEO }}
        durationInFrames={Math.ceil(KNN_VIDEO.meta.totalDurationSec * CANVAS.fps)}
        fps={CANVAS.fps}
        width={CANVAS.width}
        height={CANVAS.height}
      />

      {/* 加新视频只需要：
       * 1. import { XXX_VIDEO } from './videos/xxx/video.data';
       * 2. 加一个 <Composition id="xxx" ... defaultProps={{ data: XXX_VIDEO }} />
       */}
    </>
  );
};

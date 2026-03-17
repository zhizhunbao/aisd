// ═══════════════════════════════════════════════════════════
// 视频引擎 — 读取数据文件，自动编排场景序列
// VideoEngine — Reads video data, auto-composes scene sequence
// 所有视频共用这一个引擎组件
// ═══════════════════════════════════════════════════════════

import React from 'react';
import { AbsoluteFill, Audio, Series, staticFile } from 'remotion';
import { THEME, CANVAS } from '@lego/video-theme';
import { SceneRenderer } from './SceneRenderer';
import { Subtitle } from './Subtitle';
import type { VideoData } from '@lego/types';

interface VideoEngineProps {
  data: VideoData;
}

export const VideoEngine: React.FC<VideoEngineProps> = ({ data }) => {
  const { scenes, narration } = data;

  return (
    <AbsoluteFill style={{ backgroundColor: THEME.bg }}>
      {/* 旁白音频 */}
      <Audio src={staticFile(narration.audioFile)} />

      {/* 场景序列 — 自动根据 timestamps 编排 */}
      <Series>
        {scenes.map((scene, i) => {
          const ts = narration.timestamps[i];
          if (!ts) return null;

          const durationSec = ts.end - ts.start;
          const gapSec =
            i < narration.timestamps.length - 1
              ? narration.timestamps[i + 1].start - ts.end
              : 0;
          const totalFrames = Math.round((durationSec + gapSec) * CANVAS.fps);

          return (
            <Series.Sequence key={i} durationInFrames={totalFrames}>
              <SceneRenderer scene={scene} />
            </Series.Sequence>
          );
        })}
      </Series>

      {/* 字幕叠加层 */}
      <Subtitle
        entries={narration.subtitles}
        maxCharsPerLine={20}
        fontSize={30}
        bottomOffset={36}
      />
    </AbsoluteFill>
  );
};

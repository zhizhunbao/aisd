// ═══════════════════════════════════════════════════════════
// KnowledgeUnit — 动画层（Remotion hooks → 注入 element styles）
// KnowledgeUnit — Motion layer (Remotion hooks → inject styles)
//
// 快闪节奏（2.5s = 75f @30fps）：
//  ① zhName     0-5f    快速淡入 + scale
//  ② enName     3-8f    从下方滑入
//  ③ aliases    6-11f   淡入
//  ④ diagram    8-16f   scale(0→1) + 淡入
//  ⑤ formula    12-20f  淡入 + scale
//  ⑥ explanation 18-25f 从底部滑入
//  ⑦ 全部停留    25-末   静止
// ═══════════════════════════════════════════════════════════

import React from 'react';
import { interpolate, useCurrentFrame, spring, useVideoConfig } from 'remotion';
import { KnowledgeUnitView } from './KnowledgeUnit.view';
import type { KnowledgeUnitData } from '../../lib/types';

/** 动画辅助：淡入 */
const fadeIn = (frame: number, start: number, dur: number = 6) =>
  interpolate(frame, [start, start + dur], [0, 1], {
    extrapolateRight: 'clamp',
    extrapolateLeft: 'clamp',
  });

/** 动画辅助：从下方滑入 */
const slideUp = (frame: number, start: number, dur: number = 6, dist: number = 20) =>
  interpolate(frame, [start, start + dur], [dist, 0], {
    extrapolateRight: 'clamp',
    extrapolateLeft: 'clamp',
  });

/** 动画辅助：缩放弹入 */
const scaleIn = (frame: number, start: number, fps: number) => {
  const s = spring({
    frame: Math.max(0, frame - start),
    fps,
    config: { damping: 16, stiffness: 120 },
  });
  return Math.max(0.01, s);
};

export const KnowledgeUnit: React.FC<KnowledgeUnitData> = (data) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // ① 中文名：淡入 + 弹性缩放
  const zhScale = scaleIn(frame, 0, fps);
  const zhOpacity = fadeIn(frame, 0, 5);

  // ② 英文名：淡入 + 从下方滑入
  const enOpacity = fadeIn(frame, 3, 5);
  const enSlide = slideUp(frame, 3, 5, 15);

  // ③ 别名：淡入
  const aliasOpacity = fadeIn(frame, 6, 5);

  // ④ 图解：淡入 + 弹性缩放
  const diagScale = scaleIn(frame, 8, fps);
  const diagOpacity = fadeIn(frame, 8, 8);

  // ⑤ 公式：淡入 + 弹性缩放
  const formulaScale = scaleIn(frame, 12, fps);
  const formulaOpacity = fadeIn(frame, 12, 8);

  // ⑥ 释义：淡入 + 从下方滑入
  const explOpacity = fadeIn(frame, 18, 7);
  const explSlide = slideUp(frame, 18, 7, 20);

  return (
    <KnowledgeUnitView
      {...data}
      zhNameStyle={{
        opacity: zhOpacity,
        transform: `scale(${zhScale})`,
      }}
      enNameStyle={{
        opacity: enOpacity,
        transform: `translateY(${enSlide}px)`,
      }}
      aliasesStyle={{
        opacity: aliasOpacity,
      }}
      diagramStyle={{
        opacity: diagOpacity,
        transform: `scale(${diagScale})`,
      }}
      formulaStyle={{
        opacity: formulaOpacity,
        transform: `scale(${formulaScale})`,
      }}
      explanationStyle={{
        opacity: explOpacity,
        transform: `translateY(${explSlide}px)`,
      }}
    />
  );
};

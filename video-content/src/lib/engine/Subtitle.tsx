// ═══════════════════════════════════════════════════════════
// 字幕组件 — 微信短视频友好
// Subtitle — WeChat short video friendly
// ═══════════════════════════════════════════════════════════

import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';
import { CANVAS } from '@lego/video-theme';
import type { SubtitleEntry } from '@lego/types';

interface SubtitleProps {
  entries: SubtitleEntry[];
  maxCharsPerLine?: number;
  fontSize?: number;
  bottomOffset?: number;
}

/** 按最大字数分行 */
const splitLines = (text: string, maxChars: number): string[] => {
  if (text.length <= maxChars) return [text];

  const lines: string[] = [];
  let remaining = text;

  while (remaining.length > 0) {
    if (remaining.length <= maxChars) {
      lines.push(remaining);
      break;
    }

    let breakAt = maxChars;
    const punctuation = '，。？！、；：—…';
    for (let i = maxChars; i >= maxChars - 5 && i >= 0; i--) {
      if (punctuation.includes(remaining[i])) {
        breakAt = i + 1;
        break;
      }
    }

    lines.push(remaining.slice(0, breakAt));
    remaining = remaining.slice(breakAt);
  }

  return lines;
};

export const Subtitle: React.FC<SubtitleProps> = ({
  entries,
  maxCharsPerLine = 20,
  fontSize = 30,
  bottomOffset = 36,
}) => {
  const frame = useCurrentFrame();
  const currentTime = frame / CANVAS.fps;

  const current = entries.find((e) => currentTime >= e.start && currentTime <= e.end);
  if (!current) return null;

  const fadeIn = interpolate(
    currentTime,
    [current.start, current.start + 0.25],
    [0, 1],
    { extrapolateRight: 'clamp', extrapolateLeft: 'clamp' }
  );
  const fadeOut = interpolate(
    currentTime,
    [current.end - 0.25, current.end],
    [1, 0],
    { extrapolateRight: 'clamp', extrapolateLeft: 'clamp' }
  );
  const opacity = Math.min(fadeIn, fadeOut);

  const lines = splitLines(current.text, maxCharsPerLine);

  return (
    <div
      style={{
        position: 'absolute',
        bottom: bottomOffset,
        left: '50%',
        transform: 'translateX(-50%)',
        opacity,
        zIndex: 100,
        maxWidth: '88%',
        textAlign: 'center',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: 4,
      }}
    >
      {lines.map((line, i) => (
        <span
          key={i}
          style={{
            color: '#f0f0f0',
            fontSize,
            fontFamily: 'Noto Sans SC, sans-serif',
            backgroundColor: 'rgba(0, 0, 0, 0.72)',
            padding: '6px 22px',
            borderRadius: 6,
            lineHeight: 1.6,
            display: 'inline-block',
            letterSpacing: 1,
          }}
        >
          {line}
        </span>
      ))}
    </div>
  );
};

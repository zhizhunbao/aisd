// ═══════════════════════════════════════════════════════════
// 黑板全屏布局 — 60 秒快闪知识视频专用
// BlackboardLayout — Fullscreen chalkboard for 60s flash videos
// 底部 140px 字幕安全区
// 左上角显示已闪过的"钉住"知识点
// ═══════════════════════════════════════════════════════════

import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame, spring, useVideoConfig } from 'remotion';
import { THEME } from '@lego/video-theme';

// ══════ 黑板主题配色 ══════

const BLACKBOARD = {
  /** 墨绿黑板色 */
  bg: '#1a2820',
  /** 淡色粉笔线条 */
  chalkLine: 'rgba(255, 255, 255, 0.04)',
  /** 顶部标题栏背景 */
  topBar: 'rgba(0, 0, 0, 0.35)',
  /** 进度数字颜色 */
  progressColor: '#ffd700',
  /** 钉住项背景 */
  pinBg: 'rgba(255, 255, 255, 0.06)',
  /** 钉住项边框 */
  pinBorder: 'rgba(255, 255, 255, 0.1)',
} as const;

// ══════ 黑板背景纹理（CSS 叠加噪点） ══════

const boardStyle: React.CSSProperties = {
  background: `
    radial-gradient(ellipse at 50% 0%, rgba(40, 70, 50, 0.4) 0%, transparent 70%),
    repeating-linear-gradient(
      0deg,
      ${BLACKBOARD.chalkLine} 0px,
      transparent 1px,
      transparent 60px
    ),
    repeating-linear-gradient(
      90deg,
      ${BLACKBOARD.chalkLine} 0px,
      transparent 1px,
      transparent 60px
    ),
    ${BLACKBOARD.bg}
  `,
};

// ══════ 钉住项组件 ══════

interface PinnedItem {
  zhName: string;
  enName: string;
  color?: string;
}

const PinnedItems: React.FC<{ items: PinnedItem[] }> = ({ items }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  if (items.length === 0) return null;

  return (
    <div
      style={{
        position: 'absolute',
        top: 64,
        left: 24,
        display: 'flex',
        flexDirection: 'column',
        gap: 3,
        zIndex: 10,
      }}
    >
      {items.map((item, i) => {
        const isNewest = i === items.length - 1;
        const pinScale = isNewest
          ? spring({
              frame,
              fps,
              config: { damping: 15, stiffness: 120 },
            })
          : 1;
        const pinOpacity = isNewest
          ? interpolate(frame, [0, 8], [0, 0.85], { extrapolateRight: 'clamp' })
          : 0.6;

        return (
          <div
            key={`${item.zhName}-${i}`}
            style={{
              display: 'flex',
              alignItems: 'baseline',
              gap: 8,
              opacity: pinOpacity,
              transform: `scale(${pinScale})`,
              transformOrigin: 'left center',
              height: 22,
            }}
          >
            {/* 序号 */}
            <span
              style={{
                color: '#555',
                fontSize: 11,
                fontFamily: 'Inter, sans-serif',
                minWidth: 16,
                textAlign: 'right',
              }}
            >
              {i + 1}.
            </span>
            {/* 中文名 */}
            <span
              style={{
                color: item.color || '#ccc',
                fontSize: 14,
                fontWeight: 600,
                fontFamily: 'Noto Sans SC, sans-serif',
              }}
            >
              {item.zhName}
            </span>
            {/* 英文名 */}
            <span
              style={{
                color: '#666',
                fontSize: 11,
                fontFamily: 'Inter, sans-serif',
              }}
            >
              {item.enName}
            </span>
          </div>
        );
      })}
    </div>
  );
};

// ══════ BlackboardLayout 主组件 ══════

interface BlackboardLayoutProps {
  /** 课程/幕名（如 "MIT 线性代数"） */
  act: string;
  /** 当前知识单元标题 */
  title: string;
  titleColor?: string;
  /** 进度（如 {current: 3, total: 12}） */
  progress?: { current: number; total: number };
  /** 已闪过的知识点（钉在左上角） */
  pinnedItems?: PinnedItem[];
  /** 中间内容通过 children 传入 */
  children: React.ReactNode;
}

export const BlackboardLayout: React.FC<BlackboardLayoutProps> = ({
  act,
  title,
  titleColor,
  progress,
  pinnedItems = [],
  children,
}) => {
  const frame = useCurrentFrame();

  // 顶部标题栏动画
  const topBarOpacity = interpolate(frame, [0, 12], [0, 1], {
    extrapolateRight: 'clamp',
  });

  // 内容区域淡入
  const contentOpacity = interpolate(frame, [3, 15], [0, 1], {
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill
      style={{
        ...boardStyle,
        fontFamily: THEME.fontFamily,
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      {/* ══════ 顶部标题栏 ══════ */}
      <div
        style={{
          opacity: topBarOpacity,
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          padding: '14px 56px',
          backgroundColor: BLACKBOARD.topBar,
          borderBottom: `1px solid rgba(255, 255, 255, 0.06)`,
          minHeight: 56,
        }}
      >
        {/* 左侧：课程名 */}
        <span
          style={{
            color: THEME.dimWhite,
            fontSize: 20,
            letterSpacing: 2,
          }}
        >
          {act}
        </span>

        {/* 右侧：进度 */}
        {progress && (
          <span
            style={{
              color: BLACKBOARD.progressColor,
              fontSize: 20,
              fontWeight: 'bold',
              letterSpacing: 1,
            }}
          >
            {progress.current}/{progress.total}
          </span>
        )}
      </div>

      {/* ══════ 左上角钉住的知识点 ══════ */}
      <PinnedItems items={pinnedItems} />

      {/* ══════ 主体内容区 ══════ */}
      <div
        style={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          padding: '20px 80px',
          paddingBottom: 140, // 字幕安全区
          opacity: contentOpacity,
          overflow: 'hidden',
        }}
      >
        {children}
      </div>
    </AbsoluteFill>
  );
};

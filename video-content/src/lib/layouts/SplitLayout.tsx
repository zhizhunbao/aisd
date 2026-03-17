// ═══════════════════════════════════════════════════════════
// 左右分栏布局 — 左侧 55% 可视化，右侧 45% 要点
// SplitLayout — Left 55% visuals, Right 45% key points
// 底部 140px 字幕安全区
// ═══════════════════════════════════════════════════════════

import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';
import { THEME } from '@lego/video-theme';
import type { KeyPoint } from '@lego/types';
import 'katex/dist/katex.min.css';
import { BlockMath } from 'react-katex';

// ══════ 动画常量 ══════

const POINT_STAGGER = 10;
const POINT_START = 25;

// ══════ 右侧要点渲染 ══════

const RenderPoint: React.FC<{ point: KeyPoint; index: number }> = ({ point, index }) => {
  const frame = useCurrentFrame();

  const startFrame = POINT_START + index * POINT_STAGGER;
  const opacity = interpolate(frame, [startFrame, startFrame + 10], [0, 1], {
    extrapolateRight: 'clamp',
    extrapolateLeft: 'clamp',
  });
  const slideX = interpolate(frame, [startFrame, startFrame + 10], [20, 0], {
    extrapolateRight: 'clamp',
    extrapolateLeft: 'clamp',
  });

  const isHighlight = point.variant === 'highlight';
  const isWarning = point.variant === 'warning';
  const isFormula = point.variant === 'formula';

  if (isFormula && point.latex) {
    return (
      <div
        style={{
          opacity,
          transform: `translateX(${slideX}px)`,
          backgroundColor: `${THEME.gold}08`,
          borderRadius: 12,
          padding: '14px 16px',
          marginBottom: 10,
          borderLeft: `3px solid ${THEME.gold}60`,
        }}
      >
        <div style={{ fontSize: 28 }}>
          <BlockMath math={`\\color{${THEME.gold}}{${point.latex}}`} />
        </div>
        {point.text && (
          <div
            style={{
              color: THEME.dimWhite,
              fontSize: 16,
              fontFamily: THEME.fontFamily,
              textAlign: 'center',
              marginTop: 4,
            }}
          >
            {point.text}
          </div>
        )}
      </div>
    );
  }

  return (
    <div
      style={{
        opacity,
        transform: `translateX(${slideX}px)`,
        display: 'flex',
        alignItems: 'flex-start',
        gap: 12,
        marginBottom: 12,
        padding: '10px 14px',
        backgroundColor: isHighlight
          ? `${point.color || THEME.gold}12`
          : isWarning
          ? `${THEME.red}10`
          : 'transparent',
        borderRadius: 10,
        borderLeft: isHighlight
          ? `3px solid ${point.color || THEME.gold}`
          : isWarning
          ? `3px solid ${THEME.red}`
          : '3px solid transparent',
      }}
    >
      {point.icon && (
        <span style={{ fontSize: 26, flexShrink: 0, lineHeight: 1 }}>{point.icon}</span>
      )}
      <span
        style={{
          color: point.color || (isWarning ? THEME.red : THEME.white),
          fontSize: 24,
          fontWeight: point.bold || isHighlight ? 'bold' : 'normal',
          fontFamily: THEME.fontFamily,
          lineHeight: 1.5,
        }}
      >
        {point.text}
      </span>
    </div>
  );
};

// ══════ SplitLayout 主组件 ══════

interface SplitLayoutProps {
  act: string;
  title: string;
  titleColor?: string;
  points: KeyPoint[];
  conclusion?: { text: string; icon?: string };
  /** 左侧内容通过 children 传入 */
  children: React.ReactNode;
}

export const SplitLayout: React.FC<SplitLayoutProps> = ({
  act,
  title,
  titleColor,
  points,
  conclusion,
  children,
}) => {
  const frame = useCurrentFrame();

  // 标题动画
  const titleOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });
  const titleSlide = interpolate(frame, [0, 20], [-15, 0], { extrapolateRight: 'clamp' });
  const actOpacity = interpolate(frame, [5, 15], [0, 0.5], { extrapolateRight: 'clamp' });

  // 结论横幅
  const conclusionDelay = POINT_START + points.length * POINT_STAGGER + 10;
  const conclusionOpacity = conclusion
    ? interpolate(frame, [conclusionDelay, conclusionDelay + 15], [0, 1], {
        extrapolateRight: 'clamp',
        extrapolateLeft: 'clamp',
      })
    : 0;
  const conclusionScale = conclusion
    ? interpolate(frame, [conclusionDelay, conclusionDelay + 15], [0.95, 1], {
        extrapolateRight: 'clamp',
        extrapolateLeft: 'clamp',
      })
    : 1;

  // 分割线
  const dividerOpacity = interpolate(frame, [8, 20], [0, 0.3], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: THEME.bg,
        fontFamily: THEME.fontFamily,
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      {/* ══════ 顶部：幕名 + 标题 ══════ */}
      <div
        style={{
          padding: '16px 56px 0 56px',
          display: 'flex',
          alignItems: 'center',
          gap: 16,
          minHeight: 72,
        }}
      >
        <span
          style={{
            opacity: actOpacity,
            color: THEME.gray,
            fontSize: 15,
            letterSpacing: 2,
            flexShrink: 0,
          }}
        >
          {act}
        </span>
        <h1
          style={{
            opacity: titleOpacity,
            transform: `translateX(${titleSlide}px)`,
            color: titleColor || THEME.white,
            fontSize: 40,
            fontWeight: 'bold',
            margin: 0,
            borderBottom: `3px solid ${titleColor || THEME.gold}40`,
            paddingBottom: 8,
          }}
        >
          {title}
        </h1>
      </div>

      {/* ══════ 主体：左右分栏 ══════ */}
      <div
        style={{
          flex: 1,
          display: 'flex',
          padding: '16px 56px',
          gap: 0,
          paddingBottom: 140, // 字幕安全区
          overflow: 'hidden',
        }}
      >
        {/* ═══ 左栏：可视化 55% ═══ */}
        <div
          style={{
            width: '55%',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            gap: 20,
            paddingRight: 20,
          }}
        >
          {children}
        </div>

        {/* ═══ 分割线 ═══ */}
        <div
          style={{
            width: 2,
            opacity: dividerOpacity,
            background: `linear-gradient(transparent, ${THEME.gray}60, ${THEME.gray}60, transparent)`,
            borderRadius: 1,
            flexShrink: 0,
          }}
        />

        {/* ═══ 右栏：要点 45% ═══ */}
        <div
          style={{
            width: '45%',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            paddingLeft: 28,
          }}
        >
          {points.map((pt, i) => (
            <RenderPoint key={i} point={pt} index={i} />
          ))}

          {/* 结论横幅 */}
          {conclusion && (
            <div
              style={{
                opacity: conclusionOpacity,
                transform: `scale(${conclusionScale})`,
                backgroundColor: `${THEME.gold}10`,
                border: `2px solid ${THEME.gold}60`,
                borderRadius: 14,
                padding: '14px 20px',
                marginTop: 16,
                textAlign: 'center',
              }}
            >
              <span
                style={{
                  color: THEME.gold,
                  fontSize: 22,
                  fontWeight: 'bold',
                  fontFamily: THEME.fontFamily,
                }}
              >
                {conclusion.icon || '💡'} {conclusion.text}
              </span>
            </div>
          )}
        </div>
      </div>
    </AbsoluteFill>
  );
};

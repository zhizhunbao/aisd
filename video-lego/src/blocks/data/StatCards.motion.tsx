// StatCards — 动画层（弹簧缩放入场）
import React from 'react';
import { useCurrentFrame, spring, useVideoConfig } from 'remotion';
import { StatCardsView } from './StatCards.view';
import type { StatCardData } from '../../lib/types';

export const StatCards: React.FC<{ cards: StatCardData[]; startFrame?: number }> = ({
  cards,
  startFrame = 10,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <StatCardsView
      cards={cards}
      getItemStyle={(ci) => {
        const cardDelay = startFrame + ci * 8;
        const cardScale = spring({ frame: frame - cardDelay, fps, config: { damping: 12, stiffness: 80 } });
        const safeScale = Math.max(0.01, Math.min(cardScale, 2));
        return { transform: `scale(${safeScale})` };
      }}
    />
  );
};

// ═══════════════════════════════════════════════════════════
// StatCards — 纯视觉层
// ═══════════════════════════════════════════════════════════

import React from 'react';
import { THEME } from '../../lib/video-theme';
import type { StatCardData } from '../../lib/types';
import type { StaggerAnimProps } from '../../lib/anim-types';

export const StatCardsView: React.FC<{ cards: StatCardData[] } & StaggerAnimProps> = ({
  cards,
  containerStyle,
  getItemStyle,
}) => {
  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: `repeat(${Math.min(cards.length, 2)}, 1fr)`,
      gap: 16, width: '95%',
      ...containerStyle,
    }}>
      {cards.map((card, ci) => {
        const itemStyle = getItemStyle?.(ci);
        return (
          <div key={ci} style={{
            backgroundColor: THEME.bgLight,
            borderRadius: 16, padding: '20px 16px',
            borderLeft: `4px solid ${card.color}`,
            textAlign: 'center',
            ...itemStyle,
          }}>
            {card.icon && <div style={{ fontSize: 36, marginBottom: 8 }}>{card.icon}</div>}
            <div style={{ color: card.color, fontSize: 36, fontWeight: 'bold', fontFamily: THEME.fontFamily }}>{card.value}</div>
            <div style={{ color: THEME.dimWhite, fontSize: 18, fontFamily: THEME.fontFamily, marginTop: 6 }}>{card.label}</div>
            {card.description && (
              <div style={{ color: THEME.gray, fontSize: 16, fontFamily: THEME.fontFamily, marginTop: 4 }}>{card.description}</div>
            )}
          </div>
        );
      })}
    </div>
  );
};

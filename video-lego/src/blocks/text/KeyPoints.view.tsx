// ═══════════════════════════════════════════════════════════
// KeyPoints — 要点列表积木（纯视觉层）
// KeyPoints — Bullet-point list block (view layer)
// ═══════════════════════════════════════════════════════════

import React from 'react';
import { THEME } from '../../lib/video-theme';

interface KeyPointsViewProps {
  points: { icon?: string; text: string; color?: string; bold?: boolean }[];
}

export const KeyPointsView: React.FC<KeyPointsViewProps> = ({ points }) => {
  if (!points || points.length === 0) {
    return (
      <div style={{
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        height: '100%', color: THEME.dimWhite, fontSize: 16,
        fontFamily: THEME.fontFamily,
      }}>
        (空要点列表)
      </div>
    );
  }

  return (
    <div style={{
      display: 'flex', flexDirection: 'column', gap: 10,
      padding: '20px 24px', width: '100%', boxSizing: 'border-box',
    }}>
      {points.map((pt, i) => (
        <div key={i} style={{
          display: 'flex', alignItems: 'flex-start', gap: 10,
          fontSize: 18, color: pt.color || THEME.white,
          fontWeight: pt.bold ? 700 : 400,
          fontFamily: THEME.fontFamily, lineHeight: 1.5,
        }}>
          {pt.icon && (
            <span style={{ fontSize: 20, flexShrink: 0, width: 28, textAlign: 'center' }}>
              {pt.icon}
            </span>
          )}
          <span>{pt.text}</span>
        </div>
      ))}
    </div>
  );
};
